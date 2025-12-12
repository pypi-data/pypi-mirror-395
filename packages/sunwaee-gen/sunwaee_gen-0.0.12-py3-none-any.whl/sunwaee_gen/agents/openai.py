# standard
# third party
# custom
from sunwaee_gen.agent import Agent, AgentCost, AgentFeatures, AgentSpecs
from sunwaee_gen.models.openai import *
from sunwaee_gen.providers.openai import *


GPT_5_AGENT = Agent(
    name="openai/gpt-5",
    model=GPT_5,
    provider=OPENAI,
    cost=AgentCost(input_per_1m_token=1.25, output_per_1m_token=10),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=400000, max_output_tokens=128000),
)

GPT_5_MINI_AGENT = Agent(
    name="openai/gpt-5-mini",
    model=GPT_5_MINI,
    provider=OPENAI,
    cost=AgentCost(input_per_1m_token=0.25, output_per_1m_token=2),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=400000, max_output_tokens=128000),
)

GPT_5_NANO_AGENT = Agent(
    name="openai/gpt-5-nano",
    model=GPT_5_NANO,
    provider=OPENAI,
    cost=AgentCost(input_per_1m_token=0.05, output_per_1m_token=0.4),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=400000, max_output_tokens=128000),
)

GPT_4_1_AGENT = Agent(
    name="openai/gpt-4-1",
    model=GPT_4_1,
    provider=OPENAI,
    cost=AgentCost(input_per_1m_token=3, output_per_1m_token=12),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=1048576, max_output_tokens=32768),
)

GPT_4_1_MINI_AGENT = Agent(
    name="openai/gpt-4-1-mini",
    model=GPT_4_1_MINI,
    provider=OPENAI,
    cost=AgentCost(input_per_1m_token=0.8, output_per_1m_token=3.2),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=1048576, max_output_tokens=32768),
)

GPT_4_1_NANO_AGENT = Agent(
    name="openai/gpt-4-1-nano",
    model=GPT_4_1_NANO,
    provider=OPENAI,
    cost=AgentCost(input_per_1m_token=0.2, output_per_1m_token=0.8),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=1048576, max_output_tokens=32768),
)


OPENAI_AGENTS = [
    GPT_5_AGENT,
    GPT_5_MINI_AGENT,
    GPT_5_NANO_AGENT,
    GPT_4_1_AGENT,
    GPT_4_1_MINI_AGENT,
    GPT_4_1_NANO_AGENT,
]
