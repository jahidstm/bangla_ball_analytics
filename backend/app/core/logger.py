import structlog
from .config import get_settings

settings = get_settings()


def setup_logging():
    """
    structlog কনফিগার করে।
    DEBUG mode এ pretty print, production এ JSON format।
    """
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if settings.DEBUG
            else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            20 if not settings.DEBUG else 10  # INFO : DEBUG
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )


# সব module এ এটা import করে ব্যবহার করবে
logger = structlog.get_logger("bangla_ball")
