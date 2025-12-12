# standard
# third party
# custom
from sunwaee_gen.logger import logger
from sunwaee_gen.models.anthropic import *
from sunwaee_gen.models.deepseek import *
from sunwaee_gen.models.google import *
from sunwaee_gen.models.openai import *
from sunwaee_gen.models.xai import *

MODELS = {
    m.name: m
    for m in ANTHROPIC_MODELS
    + DEEPSEEK_MODELS
    + GOOGLE_MODELS
    + OPENAI_MODELS
    + XAI_MODELS
}

logger.debug(f"AVAILABLE MODELS: {MODELS.keys()}")
