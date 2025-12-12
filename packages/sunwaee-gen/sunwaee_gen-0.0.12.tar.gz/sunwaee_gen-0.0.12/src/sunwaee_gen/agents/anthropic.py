# standard
# third party
# custom
from sunwaee_gen.agent import Agent, AgentCost, AgentFeatures, AgentSpecs
from sunwaee_gen.models.anthropic import *
from sunwaee_gen.providers.anthropic import ANTHROPIC

CLAUDE_4_5_HAIKU_AGENT = Agent(
    name="anthropic/claude-4-5-haiku",
    model=CLAUDE_4_5_HAIKU,
    provider=ANTHROPIC,
    cost=AgentCost(input_per_1m_token=1, output_per_1m_token=5),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=True,
    ),
    specs=AgentSpecs(max_input_tokens=200000, max_output_tokens=64000),
)


CLAUDE_4_5_SONNET_AGENT = Agent(
    name="anthropic/claude-4-5-sonnet",
    model=CLAUDE_4_5_SONNET,
    provider=ANTHROPIC,
    cost=AgentCost(input_per_1m_token=3, output_per_1m_token=15),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=True,
    ),
    specs=AgentSpecs(max_input_tokens=200000, max_output_tokens=64000),
)

CLAUDE_4_1_OPUS_AGENT = Agent(
    name="anthropic/claude-4-1-opus",
    model=CLAUDE_4_1_OPUS,
    provider=ANTHROPIC,
    cost=AgentCost(input_per_1m_token=15, output_per_1m_token=75),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=True,
    ),
    specs=AgentSpecs(max_input_tokens=200000, max_output_tokens=32000),
)


CLAUDE_4_OPUS_AGENT = Agent(
    name="anthropic/claude-4-opus",
    model=CLAUDE_4_OPUS,
    provider=ANTHROPIC,
    cost=AgentCost(input_per_1m_token=15, output_per_1m_token=75),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=True,
    ),
    specs=AgentSpecs(max_input_tokens=200000, max_output_tokens=32000),
)

CLAUDE_4_SONNET_AGENT = Agent(
    name="anthropic/claude-4-sonnet",
    model=CLAUDE_4_SONNET,
    provider=ANTHROPIC,
    cost=AgentCost(input_per_1m_token=3, output_per_1m_token=15),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=True,
    ),
    specs=AgentSpecs(max_input_tokens=200000, max_output_tokens=64000),
)

CLAUDE_3_7_SONNET_AGENT = Agent(
    name="anthropic/claude-3-7-sonnet",
    model=CLAUDE_3_7_SONNET,
    provider=ANTHROPIC,
    cost=AgentCost(input_per_1m_token=3, output_per_1m_token=15),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=True,
    ),
    specs=AgentSpecs(max_input_tokens=200000, max_output_tokens=64000),
)


ANTHROPIC_AGENTS = [
    CLAUDE_4_1_OPUS_AGENT,
    CLAUDE_4_OPUS_AGENT,
    CLAUDE_4_SONNET_AGENT,
    CLAUDE_3_7_SONNET_AGENT,
]
