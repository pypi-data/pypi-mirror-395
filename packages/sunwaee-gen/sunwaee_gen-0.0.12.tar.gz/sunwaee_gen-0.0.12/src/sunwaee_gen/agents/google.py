# standard
# third party
# custom
from sunwaee_gen.agent import Agent, AgentCost, AgentFeatures, AgentSpecs
from sunwaee_gen.models.google import *
from sunwaee_gen.providers.google import *

GEMINI_2_5_PRO_AGENT = Agent(
    name="google/gemini-2.5-pro",
    model=GEMINI_2_5_PRO,
    provider=GOOGLE,
    cost=AgentCost(input_per_1m_token=1.25, output_per_1m_token=10),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=1048576, max_output_tokens=65536),
)

GEMINI_2_5_FLASH_AGENT = Agent(
    name="google/gemini-2.5-flash",
    model=GEMINI_2_5_FLASH,
    provider=GOOGLE,
    cost=AgentCost(input_per_1m_token=0.3, output_per_1m_token=2.5),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=1048576, max_output_tokens=65536),
)

GEMINI_2_5_FLASH_LITE_AGENT = Agent(
    name="google/gemini-2.5-flash-lite",
    model=GEMINI_2_5_FLASH_LITE,
    provider=GOOGLE,
    cost=AgentCost(input_per_1m_token=0.1, output_per_1m_token=0.4),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=False,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=1048576, max_output_tokens=65536),
)


GOOGLE_AGENTS = [
    GEMINI_2_5_PRO_AGENT,
    GEMINI_2_5_FLASH_AGENT,
    GEMINI_2_5_FLASH_LITE_AGENT,
]
