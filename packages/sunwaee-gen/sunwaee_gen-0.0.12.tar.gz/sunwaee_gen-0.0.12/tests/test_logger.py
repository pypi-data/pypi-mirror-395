# standard
import logging

# third party
# custom
from sunwaee_gen.logger import get_logger, logger


class TestLogger:

    def test_get_logger_no_name(self):
        test_logger = get_logger()
        assert isinstance(test_logger, logging.Logger)
        assert test_logger.handlers

    def test_get_logger_with_name(self):
        test_logger = get_logger("test_logger")
        assert isinstance(test_logger, logging.Logger)
        assert test_logger.name == "test_logger"
        assert test_logger.handlers

    def test_default_logger(self):
        assert isinstance(logger, logging.Logger)
        assert logger.handlers
