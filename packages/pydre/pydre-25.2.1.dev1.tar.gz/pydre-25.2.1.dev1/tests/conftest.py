import warnings
import pytest
from loguru import logger
import logging
from _pytest.logging import LogCaptureFixture


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    try:
        yield caplog
    finally:
        try:
            logger.remove(handler_id)
        except ValueError:
            # Handler was already removed, possibly by another fixture.
            pass


@pytest.fixture
def reportlog(pytestconfig):
    logging_plugin = pytestconfig.pluginmanager.getplugin("logging-plugin")
    handler_id = logger.add(logging_plugin.report_handler, format="{message}")
    try:
        yield
    finally:
        try:
            logger.remove(handler_id)
        except ValueError:
            # Handler was already removed, possibly by another fixture.
            pass


@pytest.fixture(autouse=True)
def propagate_logs():
    class PropagateHandler(logging.Handler):
        def emit(self, record):
            if logging.getLogger(record.name).isEnabledFor(record.levelno):
                logging.getLogger(record.name).handle(record)

    propagate_id = logger.add(PropagateHandler(), format="{message}")
    try:
        yield
    finally:
        try:
            logger.remove(propagate_id)
        except ValueError:
            # Handler was already removed, possibly by another fixture.
            pass


def pytest_configure(config):
    warnings.filterwarnings("ignore", category=DeprecationWarning)
