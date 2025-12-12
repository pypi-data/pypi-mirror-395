# standard
import os
import logging

# third party
import rich.logging as richlogging

# custom


def get_logger(name: str | None = None) -> logging.Logger:
    """Get a configured logger with Rich output."""
    logger = logging.getLogger(name)

    log_level = os.getenv("SUNWAEE_LOG_LEVEL", "INFO")

    if not logger.handlers:
        logger.setLevel(log_level)

        rich_handler = richlogging.RichHandler(
            markup=True,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            show_path=False,
        )

        formatter = logging.Formatter(
            "%(filename)s:%(lineno)d:%(funcName)s | %(message)s"
        )
        rich_handler.setFormatter(formatter)

        logger.addHandler(rich_handler)
        logger.propagate = False

    return logger


logger = get_logger(__name__)

# SAMPLES
# logger.debug("debug")
# logger.info("info")
# logger.warning("warning")
# logger.error("error")
