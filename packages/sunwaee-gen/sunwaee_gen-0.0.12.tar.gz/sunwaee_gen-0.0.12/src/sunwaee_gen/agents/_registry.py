# standard
# third party
# custom
from sunwaee_gen.logger import logger
from sunwaee_gen.agents.anthropic import *
from sunwaee_gen.agents.deepseek import *
from sunwaee_gen.agents.google import *
from sunwaee_gen.agents.openai import *
from sunwaee_gen.agents.xai import *

AGENTS = {
    a.name: a
    for a in ANTHROPIC_AGENTS
    + DEEPSEEK_AGENTS
    + GOOGLE_AGENTS
    + OPENAI_AGENTS
    + XAI_AGENTS
}

logger.debug(f"AVAILABLE AGENTS: {AGENTS.keys()}")
