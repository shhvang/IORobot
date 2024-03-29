import sys
import time
import logging
import pathlib
import loguru
from logging.handlers import RotatingFileHandler
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # avoid sphinx autodoc resolve annotation failed
    # because loguru module do not have `Logger` class actually
    from loguru import Logger, Record

logger: "Logger" = loguru.logger

class TornadoLogFormatter(logging.Formatter):
    """
    Advanced Loguru-based formatter for Tornado-style logging.
    """
    colors = {
        logging.DEBUG: "<cyan>",
        logging.INFO: "<green>",
        logging.WARNING: "<yellow>",
        logging.ERROR: "<red>",
        logging.CRITICAL: "<light-red>",
    }

    def format(self, record):
        loguru_record = {
            "name": record.name,
            "level": record.levelname,
            "asctime": time.strftime("%m-%d %H:%M:%S", self.converter(record.created)),
            "message": record.getMessage(),
            **record.__dict__,
        }

        # Additional details excluding standard LogRecord attributes
        extra_details = ' '.join(
            f"<magenta>{k}</magenta>=<blue>{v}</blue>" for k, v in record.__dict__.items()
            if k not in {
                'levelname', 'asctime', 'module', 'lineno', 'args', 'message',
                'filename', 'exc_info', 'exc_text', 'created', 'funcName',
                'processName', 'process', 'msecs', 'relativeCreated', 'thread',
                'threadName', 'name', 'levelno', 'msg', 'pathname', 'stack_info',
            }
        )
        loguru_record['extra'] = extra_details

        color = self.colors.get(record.levelno, "")
        reset_color = "</>"
        log_message = "<level>{asctime}</level> | <level>{name}</level> | <level>{level}</level>: {message} {extra}"

        return color + log_message.format(**loguru_record) + reset_color

def enablelogging(level=logging.DEBUG, color=True):
    """
    Enable pretty logging with Tornado-style formatting.

    Args:
        level: Logging level.
        color: Boolean to enable or disable color (default: True).
    """
    # Create Loguru logger
    logger.remove()  # Remove any default handlers
    logger.add(sys.stdout, level=level)  # Add a stream handler for console output

    # Set up file rotation with Loguru
    log_path = pathlib.Path('./Main/logger') / 'kiyo.log'
    logger.add(log_path, rotation="1 week", retention="7 days", level=level)

    # Set up Loguru handler for logging module
    loguru_handler = logging.StreamHandler(sys.stdout)
    loguru_handler.setLevel(level)
    loguru_handler.setFormatter(TornadoLogFormatter())
    logging.getLogger().addHandler(loguru_handler)

    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('psycopg2').setLevel(logging.WARNING)
    logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)
    logging.getLogger('apscheduler.scheduler').setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    if color and sys.stderr.isatty():
        try:
            import curses
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                logger.info("Terminal supports colors")
        except Exception:
            pass

    logger.info('Initialized Logger')
