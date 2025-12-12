# standard
# third party
# custom
from sunwaee_gen.logger import logger
from sunwaee_gen.providers.anthropic import *
from sunwaee_gen.providers.deepseek import *
from sunwaee_gen.providers.google import *
from sunwaee_gen.providers.openai import *
from sunwaee_gen.providers.xai import *

PROVIDERS = {
    p.name: p
    for p in [
        ANTHROPIC,
        DEEPSEEK,
        GOOGLE,
        OPENAI,
        XAI,
    ]
}

logger.debug(f"AVAILABLE PROVIDERS: {PROVIDERS.keys()}")
