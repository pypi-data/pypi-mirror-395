# standard
# third party
# custom
from sunwaee_gen.agent import Agent, AgentCost, AgentFeatures, AgentSpecs
from sunwaee_gen.models.deepseek import *
from sunwaee_gen.providers.deepseek import *


DEEPSEEK_REASONER_AGENT = Agent(
    name="deepseek/deepseek-reasoner",
    model=DEEPSEEK_REASONER,
    provider=DEEPSEEK,
    cost=AgentCost(input_per_1m_token=0.56, output_per_1m_token=1.68),
    features=AgentFeatures(
        supports_tools=False,
        supports_reasoning=True,
        reasoning_tokens_access=True,
    ),
    specs=AgentSpecs(max_input_tokens=128000, max_output_tokens=64000),
)

DEEPSEEK_CHAT_AGENT = Agent(
    name="deepseek/deepseek-chat",
    model=DEEPSEEK_CHAT,
    provider=DEEPSEEK,
    cost=AgentCost(input_per_1m_token=0.56, output_per_1m_token=1.68),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=False,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=128000, max_output_tokens=64000),
)


DEEPSEEK_AGENTS = [
    DEEPSEEK_REASONER_AGENT,
    DEEPSEEK_CHAT_AGENT,
]
