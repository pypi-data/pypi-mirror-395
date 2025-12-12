"""
Netrun Unified Logging Service
Structured logging with structlog backend, correlation ID tracking, and Azure App Insights integration

Usage:
    from netrun_logging import configure_logging, get_logger

    configure_logging(app_name="my-service", environment="production")
    logger = get_logger(__name__)
    logger.info("application_started", version="1.1.0")

New in v1.1.0:
    - Structlog backend for improved performance and flexibility
    - Async logging support (logger.ainfo, logger.aerror, etc.)
    - Enhanced context management with bind_context()
    - OpenTelemetry trace injection
    - Automatic sensitive field sanitization
"""

from netrun_logging.logger import configure_logging, get_logger
from netrun_logging.correlation import (
    generate_correlation_id,
    get_correlation_id,
    set_correlation_id,
    correlation_id_context,
    bind_context,
    clear_context,
)
from netrun_logging.context import (
    LogContext,
    get_context,
    set_context,
    clear_context as clear_log_context,
)
from netrun_logging.formatters.json_formatter import JsonFormatter

__version__ = "1.1.0"
__all__ = [
    # Core configuration
    "configure_logging",
    "get_logger",
    # Correlation ID management
    "generate_correlation_id",
    "get_correlation_id",
    "set_correlation_id",
    "correlation_id_context",
    # Context management (structlog)
    "bind_context",
    "clear_context",
    # Legacy context management (LogContext)
    "LogContext",
    "get_context",
    "set_context",
    "clear_log_context",
    # Formatters
    "JsonFormatter",
]
