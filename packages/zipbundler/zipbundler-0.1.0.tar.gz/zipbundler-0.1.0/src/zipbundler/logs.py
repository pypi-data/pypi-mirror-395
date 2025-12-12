# src/zipbundler/logs.py

import logging
from typing import cast

from apathetic_logging import (
    Logger,
    makeSafeTrace,
    registerDefaultLogLevel,
    registerLogger,
    registerLogLevelEnvVars,
)

from .constants import DEFAULT_ENV_LOG_LEVEL, DEFAULT_LOG_LEVEL
from .meta import PROGRAM_ENV, PROGRAM_PACKAGE


# --- Logger initialization ---------------------------------------------------

# Force the logging module to use the Logger class globally.
# This must happen *before* any loggers are created.
logging.setLoggerClass(Logger)

# Force registration of TRACE and SILENT levels
Logger.extendLoggingModule()

# Register log level environment variables and default
# This must happen before any loggers are created so they use the registered values
registerLogLevelEnvVars(
    [f"{PROGRAM_ENV}_{DEFAULT_ENV_LOG_LEVEL}", DEFAULT_ENV_LOG_LEVEL]
)
registerDefaultLogLevel(DEFAULT_LOG_LEVEL)

# Register the logger name so getLogger() can find it
registerLogger(PROGRAM_PACKAGE)

# Create the app logger instance via logging.getLogger()
# This ensures it's registered with the logging module and can be retrieved
# by other code that uses logging.getLogger()
_APP_LOGGER = cast("Logger", logging.getLogger(PROGRAM_PACKAGE))


# --- Convenience utils ---------------------------------------------------------


def getAppLogger() -> Logger:  # noqa: N802
    """Return the configured app logger.

    This is the app-specific logger getter that returns Logger type.
    Use this in application code instead of utils_logs.get_logger() for
    better type hints.
    """
    trace = makeSafeTrace()
    trace(
        "getAppLogger() called",
        f"id={id(_APP_LOGGER)}",
        f"name={_APP_LOGGER.name}",
        f"level={_APP_LOGGER.levelName}",
        f"handlers={[type(h).__name__ for h in _APP_LOGGER.handlers]}",
    )
    return _APP_LOGGER
