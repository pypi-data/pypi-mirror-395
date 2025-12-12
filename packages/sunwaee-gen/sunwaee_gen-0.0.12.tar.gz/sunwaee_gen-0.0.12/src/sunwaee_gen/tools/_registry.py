# standard
# third party
# custom
from sunwaee_gen.logger import logger
from sunwaee_gen.tools.execute_command import execute_command

TOOLS = {
    tool.function.name: tool
    for tool in [
        execute_command,
    ]
}

logger.debug(f"AVAILABLE TOOLS: {list(TOOLS.keys())}")
