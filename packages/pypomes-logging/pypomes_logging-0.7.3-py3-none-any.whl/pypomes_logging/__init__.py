from .logging_pomes import (
    PYPOMES_LOGGER, LogLevel, LogGetParam, LogPostParam,
    logging_startup, logging_shutdown, service_logging,
    logging_get_entries, logging_send_entries,
    logging_get_param, logging_get_params, logging_log_init
)

__all__ = [
    # logging_pomes
    "PYPOMES_LOGGER", "LogLevel", "LogGetParam", "LogPostParam",
    "logging_startup", "logging_shutdown", "service_logging",
    "logging_get_entries", "logging_send_entries",
    "logging_get_param", "logging_get_params", "logging_log_init"
]

from importlib.metadata import version
__version__ = version("pypomes_logging")
__version_info__ = tuple(int(i) for i in __version__.split(".") if i.isdigit())
