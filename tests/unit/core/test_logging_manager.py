"""test logging_manager file."""

import logging
import os

import pytest
from assertpy import assert_that, contents_of

from src.common.constants import CommonPaths
from src.core.logging_manager import LoggingManager


@pytest.mark.core
class TestLoggingManager:
    """Unit Tests class to cover LoggingManager methods."""

    def test_setup_logger_main(self, caplog):
        """Test: Validate setup app logger.

        :return:
        """
        log_path = CommonPaths.tests_path.joinpath("unit").joinpath("core").joinpath("logs")
        os.makedirs(log_path, exist_ok=True)
        logger = LoggingManager.setup_logger()
        # Validation
        assert_that(logger).is_not_none()

    def test_debug_log(self, caplog):
        """Test: Validate that debug log message was captured.

        :return:
        """
        debug_msg = "This is Debug log."
        logging.debug(debug_msg)

        # Validation
        assert_that(caplog.text).contains(debug_msg)
        assert_that(caplog.messages).contains(debug_msg)
        assert_that(len(caplog.records)).is_equal_to(1)
        assert_that(caplog.records[0].levelname).is_equal_to("DEBUG")

    def test_error_log(self, caplog):
        """Test: Validate that error log message was captured.

        :return:
        """
        error_msg = "This is Error log."
        logging.error(error_msg)

        # Validation
        assert_that(caplog.text).contains(error_msg)
        assert_that(caplog.messages).contains(error_msg)
        assert_that(len(caplog.records)).is_equal_to(1)
        assert_that(caplog.records[0].levelname).is_equal_to("ERROR")

    def test_info_log(self, caplog):
        """Test: Validate that info log message was captured.

        :return:
        """
        info_msg = "This is Information log."
        logging.info(info_msg)

        # Validation
        assert_that(caplog.text).contains(info_msg)
        assert_that(caplog.messages).contains(info_msg)
        assert_that(len(caplog.records)).is_equal_to(1)
        assert_that(caplog.records[0].levelname).is_equal_to("INFO")

    def test_warning_log(self, caplog):
        """Test: Validate that info log message was captured.

        :return:
        """
        warn_msg = "This is Warning log."
        logging.warning(warn_msg)

        # Validation
        assert_that(caplog.text).contains(warn_msg)
        assert_that(caplog.messages).contains(warn_msg)
        assert_that(len(caplog.records)).is_equal_to(1)
        assert_that(caplog.records[0].levelname).is_equal_to("WARNING")

    def test_file_handlers(self, tmp_path):
        """Test: Validate that logs was captured by file handlers.

        :return:
        """
        log_file = tmp_path.joinpath("test_log.log")
        my_logging_dict = {
            "version": 1,
            "disable_existing_loggers": False,
            "loggers": {
                "": {
                    "level": logging.DEBUG,
                    "handlers": ["file"],
                }
            },
            "formatters": {
                "standard": {
                    "format": "%(asctime)s - %(name)s - [%(levelname)s] -  %(filename)s:%(lineno)d - %(message)s",
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                }
            },
            "handlers": {
                "file": {
                    "level": "DEBUG",
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "standard",
                    "filename": str(log_file),
                    "maxBytes": 500000,
                    "backupCount": 5,
                }
            },
        }
        LoggingManager.init_logger(my_logging_dict)
        msg = "This is an info log message."
        logging.info(msg)
        # Validate file exists
        assert_that(str(log_file)).exists()
        # Validate content
        contents = contents_of(log_file, "utf-8")
        assert_that(contents).contains(msg)
