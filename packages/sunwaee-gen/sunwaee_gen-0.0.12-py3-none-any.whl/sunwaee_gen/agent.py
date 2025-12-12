# standard
import uuid
import json
import time

# third party
import aiohttp
import pydantic

# custom
from sunwaee_gen.model import Model
from sunwaee_gen.provider import Provider
from sunwaee_gen.response import Cost, Error, Performance, Response, Usage
from sunwaee_gen.helpers import get_nested_dict_value
from sunwaee_gen.logger import logger


class AgentCost(pydantic.BaseModel):
    input_per_1m_token: float
    output_per_1m_token: float

    @pydantic.computed_field()
    def input_per_token(self) -> float:
        return self.input_per_1m_token / 1_000_000

    @pydantic.computed_field()
    def output_per_token(self) -> float:
        return self.output_per_1m_token / 1_000_000


class AgentFeatures(pydantic.BaseModel):
    supports_tools: bool = False
    supports_reasoning: bool = False
    reasoning_tokens_access: bool = False


class AgentSpecs(pydantic.BaseModel):
    max_input_tokens: int
    max_output_tokens: int


class Agent(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,  # Model and Provider custom
        extra="allow",  # allows testing/mocking
    )

    name: str
    model: Model
    provider: Provider

    cost: AgentCost
    features: AgentFeatures
    specs: AgentSpecs

    async def async_completion(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        streaming: bool = False,
        api_key: str | None = None,
    ):

        url = self.provider.url

        # NOTE google you weirdos..
        if "<|model_name|>" in url:
            url = url.replace("<|model_name|>", self.model.name)
        if "<|gen_method|>" in url:
            url = url.replace(
                "<|gen_method|>",
                "streamGenerateContent" if streaming else "generateContent",
            )
        logger.debug(f"url is `{url}`")

        # --- HEADERS

        headers = self.provider.headers_adapter(
            provider=self.provider.name,
            api_key=api_key,
        )

        # --- PAYLOAD

        model = self.model.name
        if self.model.version:
            model += f"-{self.model.version}"

        system_prompt = None
        if messages[0].get("role") == "system":
            system_prompt = messages[0].get("content")
            messages = messages[1:]

        messages = self.provider.messages_adapter(
            system_prompt=system_prompt,
            messages=messages,
        )

        if self.features.supports_tools and tools:
            tools = self.provider.tools_adapter(tools=tools)

        payload = self.provider.payload_adapter(
            model=model,
            system_prompt=system_prompt,
            messages=messages,
            tools=tools,
            max_tokens=self.specs.max_output_tokens,
            streaming=streaming,
        )
        logger.debug(f"payload is:\n{json.dumps(payload, indent=2, default=str)}")

        if streaming:
            async for block in self._async_stream_completion(url, headers, payload):
                yield block
        else:
            yield await self._async_completion(url, headers, payload)

    async def _async_completion(self, url: str, headers: dict, payload: dict):
        # perf
        start = time.time()
        latency = 0.0
        total_duration = 0.0

        # main
        reasoning = ""
        content = ""
        tool_calls = []

        # usage
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=headers,
                json=payload,
                timeout=None,
            ) as response:
                if response.status != 200:
                    error_message = await response.text()
                    return Response(
                        model=self.model,
                        provider=self.provider,
                        error=Error(status=response.status, message=error_message),
                        streaming=False,
                    ).model_dump(mode="json")

                data = await response.json()
                latency = time.time() - start

                adapter = self.provider.response_adapter()

                reasoning = get_nested_dict_value(
                    data, path=adapter.get("reasoning", "")
                )
                content = get_nested_dict_value(data, path=adapter.get("content", ""))

                # tool calls
                tool_call_ids = get_nested_dict_value(
                    data, path=adapter.get("tool_call_id", "")
                )
                tool_call_names = get_nested_dict_value(
                    data, path=adapter.get("tool_call_name", "")
                )
                tool_call_arguments = get_nested_dict_value(
                    data, path=adapter.get("tool_call_arguments", "")
                )

                if tool_call_names:
                    if isinstance(tool_call_names, list):
                        # multiple tool calls - zip the arrays
                        ids = (
                            tool_call_ids
                            if isinstance(tool_call_ids, list)
                            else [tool_call_ids] * len(tool_call_names)
                        )
                        args = (
                            tool_call_arguments
                            if isinstance(tool_call_arguments, list)
                            else [tool_call_arguments] * len(tool_call_names)
                        )

                        for i, name in enumerate(tool_call_names):
                            if name:  # only add if name exists
                                tool_call = {
                                    "id": (
                                        ids[i]
                                        if i < len(ids) and ids[i]
                                        else str(uuid.uuid4())
                                    ),
                                    "name": name,
                                    "arguments": args[i] if i < len(args) else {},
                                }
                                tool_calls.append(tool_call)
                    else:  # pragma: no cover
                        # single tool call
                        tool_call = {
                            "id": tool_call_ids if tool_call_ids else str(uuid.uuid4()),
                            "name": tool_call_names,
                            "arguments": (
                                tool_call_arguments if tool_call_arguments else {}
                            ),
                        }
                        tool_calls.append(tool_call)

                # usage
                if pt := get_nested_dict_value(
                    data, path=adapter.get("prompt_tokens", "")
                ):
                    if isinstance(pt, int):
                        prompt_tokens = pt
                if ct := get_nested_dict_value(
                    data, path=adapter.get("completion_tokens", "")
                ):
                    if isinstance(ct, int):
                        completion_tokens = ct
                if tt := get_nested_dict_value(
                    data, path=adapter.get("total_tokens", "")
                ):
                    if isinstance(tt, int):
                        total_tokens = tt

        # raw
        raw = ""
        if reasoning:
            raw += f"<think>{reasoning}</think>"
        if content:
            raw += content
        if tool_calls:
            for tc in tool_calls:
                raw += f"<tool_call>{json.dumps(tc)}</tool_call>"

        # reasoning and content durations
        raw_length = len(raw)
        if raw_length > 0 and latency > 0:
            reasoning_duration = (
                (len(reasoning) / raw_length) * latency if reasoning else 0.0
            )
            content_duration = (len(content) / raw_length) * latency if content else 0.0
        else:  # pragma: no cover
            reasoning_duration = 0.0
            content_duration = 0.0

        total_tokens = (
            total_tokens if total_tokens else prompt_tokens + completion_tokens
        )
        total_duration = latency
        throughput = int(total_tokens / total_duration) if total_duration > 0 else 0

        prompt_cost = prompt_tokens * self.cost.input_per_token
        completion_cost = completion_tokens * self.cost.output_per_token
        total_cost = prompt_cost + completion_cost

        return Response(
            model=self.model,
            provider=self.provider,
            streaming=False,
            reasoning=reasoning,
            content=content,
            tool_calls=tool_calls,
            raw=raw,
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
            ),
            cost=Cost(
                prompt_cost=prompt_cost,
                completion_cost=completion_cost,
                total_cost=total_cost,
            ),
            performance=Performance(
                latency=latency,
                reasoning_duration=reasoning_duration,
                content_duration=content_duration,
                total_duration=total_duration,
                throughput=throughput,
            ),
        ).model_dump(mode="json")

    async def _async_stream_completion(self, url: str, headers: dict, payload: dict):

        # just making the main code easier to read
        async def sse_data(sse_stream, is_google_trash_format: bool = False):
            buffer = ""
            async for line in sse_stream.content:
                if line:
                    decoded_line = line.decode("utf-8")
                    # the folks from google doing garbage as usual...
                    # accumulate chars until we reach a json decodable str...
                    # not really resilient but hey google small indie company...
                    if is_google_trash_format:
                        if decoded_line.rstrip() == "[{":
                            buffer = "{"
                        elif decoded_line.rstrip() == ",":
                            buffer = ""
                        # NOTE not needed
                        # elif decoded_line.rstrip() == "]":
                        #     buffer = ""
                        else:
                            buffer += decoded_line
                            try:
                                json_data = json.loads(buffer)
                                yield json_data
                            except json.JSONDecodeError:  # pragma: no cover
                                pass
                    # regular sse format
                    else:
                        if decoded_line.startswith("data:"):
                            try:
                                json_data = json.loads(decoded_line[len("data:") :])
                                yield json_data
                            except json.JSONDecodeError:  # pragma: no cover
                                pass

        # main
        reasoning: str = ""
        content: str = ""
        tool_calls: list[dict] = []
        tool_call: dict[str, str] = {"id": "", "name": "", "arguments": ""}

        # usage
        prompt_tokens: int = 0
        completion_tokens: int = 0
        total_tokens: int = 0

        # perf
        start = time.time()
        latency = 0.0
        reasoning_start = None
        reasoning_duration = None
        content_start = None
        content_duration = None

        # NOTE for models without access to reasoning tokens, we start the timer
        # as the requests starts as we have no more accurate approach
        if (
            self.features.supports_reasoning
            and not self.features.reasoning_tokens_access
        ):
            reasoning_start = time.time()
            yield Response(
                model=self.model,
                provider=self.provider,
                streaming=True,
                reasoning="reasoning started, but reasoning tokens are not avaiable for this model...",
            ).model_dump(mode="json")

        sse_adapter = self.provider.sse_adapter()

        # make it async
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=headers,
                json=payload,
                timeout=None,
            ) as sse_stream:

                # --- DATA PARSING

                async for data in sse_data(
                    sse_stream,
                    is_google_trash_format=(self.provider.name == "google"),
                ):
                    # latency at first fragment
                    if not latency:
                        latency = time.time() - start

                    # reasoning
                    if r := get_nested_dict_value(
                        data, path=sse_adapter.get("reasoning", "")
                    ):
                        if isinstance(r, str):
                            # start reasoning timer
                            if reasoning_start is None:
                                reasoning_start = time.time()
                            reasoning += r
                            yield Response(
                                model=self.model,
                                provider=self.provider,
                                streaming=True,
                                reasoning=r,
                            ).model_dump(mode="json")

                    # content
                    if c := get_nested_dict_value(
                        data, path=sse_adapter.get("content", "")
                    ):
                        if isinstance(c, str):
                            # start content timer
                            if content_start is None:
                                content_start = time.time()
                            # end reasoning timer
                            if reasoning_start is not None:
                                reasoning_duration = time.time() - reasoning_start
                                reasoning_start = None
                                yield Response(
                                    model=self.model,
                                    provider=self.provider,
                                    streaming=True,
                                    reasoning_duration=reasoning_duration,
                                ).model_dump(mode="json")
                            content += c
                            yield Response(
                                model=self.model,
                                provider=self.provider,
                                streaming=True,
                                content=c,
                            ).model_dump(mode="json")

                    # tool calls
                    # name
                    if tn := get_nested_dict_value(
                        data, path=sse_adapter.get("tool_call_name", "")
                    ):
                        if isinstance(tn, str):
                            # end content timer
                            if content_start is not None:
                                content_duration = time.time() - content_start
                                content_start = None
                                yield Response(
                                    model=self.model,
                                    provider=self.provider,
                                    streaming=True,
                                    content_duration=content_duration,
                                ).model_dump(mode="json")
                            # end reasoning timer
                            if reasoning_start is not None:
                                reasoning_duration = time.time() - reasoning_start
                                reasoning_start = None
                                yield Response(
                                    model=self.model,
                                    provider=self.provider,
                                    streaming=True,
                                    reasoning_duration=reasoning_duration,
                                ).model_dump(mode="json")
                            tool_call = {"id": "", "name": "", "arguments": ""}
                            tool_call["name"] = tn
                    # id
                    if tid := get_nested_dict_value(
                        data, path=sse_adapter.get("tool_call_id", "")
                    ):
                        if isinstance(tid, str):
                            tool_call["id"] = tid
                    # arguments
                    if ta := get_nested_dict_value(
                        data, path=sse_adapter.get("tool_call_arguments", "")
                    ):
                        if isinstance(ta, str):
                            tool_call["arguments"] += ta

                            try:
                                tool_call_final = {
                                    "id": (
                                        tool_call["id"]
                                        if tool_call["id"]
                                        else f"tc_{str(uuid.uuid4())}"
                                    ),
                                    "name": tool_call["name"],
                                    "arguments": json.loads(tool_call["arguments"]),
                                }

                                tool_calls.append(tool_call_final)
                                yield Response(
                                    model=self.model,
                                    provider=self.provider,
                                    streaming=True,
                                    tool_calls=[tool_call_final],
                                ).model_dump(mode="json")

                                # reset after yield
                                tool_call = {"id": "", "name": "", "arguments": ""}
                            except json.JSONDecodeError:  # pragma: no cover
                                pass
                        elif isinstance(ta, dict):
                            tool_call_final = {
                                "id": (
                                    tool_call["id"]
                                    if tool_call["id"]
                                    else f"tc_{str(uuid.uuid4())}"
                                ),
                                "name": tool_call["name"],
                                "arguments": ta,
                            }

                            tool_calls.append(tool_call_final)
                            yield Response(
                                model=self.model,
                                provider=self.provider,
                                streaming=True,
                                tool_calls=[tool_call_final],
                            ).model_dump(mode="json")

                            # reset after yield
                            tool_call = {"id": "", "name": "", "arguments": ""}

                    # usage
                    if pt := get_nested_dict_value(
                        data, path=sse_adapter.get("prompt_tokens", "")
                    ):
                        if isinstance(pt, int):
                            prompt_tokens = pt
                    if ct := get_nested_dict_value(
                        data, path=sse_adapter.get("completion_tokens", "")
                    ):
                        if isinstance(ct, int):
                            completion_tokens = ct
                    if tt := get_nested_dict_value(
                        data, path=sse_adapter.get("total_tokens", "")
                    ):
                        if isinstance(tt, int):
                            total_tokens = tt

        # end content timer
        if content_start is not None:
            content_duration = time.time() - content_start
            content_start = None
            yield Response(
                model=self.model,
                provider=self.provider,
                streaming=True,
                content_duration=content_duration,
            ).model_dump(mode="json")
        # end reasoning timer
        if reasoning_start is not None:
            reasoning_duration = time.time() - reasoning_start
            reasoning_start = None
            yield Response(
                model=self.model,
                provider=self.provider,
                streaming=True,
                reasoning_duration=reasoning_duration,
            ).model_dump(mode="json")

        # build raw
        raw = ""
        if reasoning:
            raw += f"<think>{reasoning}</think>"
        if content:
            raw += content
        if tool_calls:
            for tc in tool_calls:
                raw += f"<tool_call>{json.dumps(tc)}</tool_call>"

        # perf
        total_tokens = (
            total_tokens if total_tokens else prompt_tokens + completion_tokens
        )
        total_duration = (content_duration or 0.0) + (reasoning_duration or 0.0)
        throughput = int(total_tokens / total_duration) if total_duration > 0 else 0

        # cost
        prompt_cost = prompt_tokens * self.cost.input_per_token
        completion_cost = completion_tokens * self.cost.output_per_token
        total_cost = prompt_cost + completion_cost

        yield Response(
            model=self.model,
            provider=self.provider,
            streaming=True,
            raw=raw,
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
            ),
            cost=Cost(
                prompt_cost=prompt_cost,
                completion_cost=completion_cost,
                total_cost=total_cost,
            ),
            performance=Performance(
                latency=latency,
                reasoning_duration=reasoning_duration or 0.0,
                content_duration=content_duration or 0.0,
                total_duration=total_duration,
                throughput=throughput,
            ),
        ).model_dump(mode="json")
