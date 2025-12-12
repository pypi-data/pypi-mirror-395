import os
import sys

import structlog
from structlog import get_logger

LOG_LEVELS = ['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG']
DEFAULT_LOG_LEVEL = 'WARNING'

__all__ = [
    'configure_structlog_console',
    'configure_structlog_console_from_env',
    'LOG_LEVELS',
    'get_logger',
]


def configure_structlog_console(log_level=DEFAULT_LOG_LEVEL):
    """
    Opinionated structlog config:

    - log to STDERR instead of STDOUT (useful for scripts that print stuff as output)
    - stuff from https://www.structlog.org/en/stable/performance.html
    """
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt='iso', utc=True),
            # structlog.processors.CallsiteParameterAdder([
            #     structlog.processors.CallsiteParameter.MODULE,
            #     structlog.processors.CallsiteParameter.FUNC_NAME,
            #     structlog.processors.CallsiteParameter.LINENO,
            # ]),
            structlog.dev.ConsoleRenderer(),
        ],
        # log_level may be a string. needs structlog 25.1.0
        # https://github.com/hynek/structlog/blob/main/CHANGELOG.md#2510---2025-01-16
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
    )


def configure_structlog_console_from_env(log_level=DEFAULT_LOG_LEVEL):
    level = os.environ.get('LOGLEVEL', log_level)
    configure_structlog_console(level)
