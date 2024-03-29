import sys
import time
import logging, pathlib
from logging.handlers import RotatingFileHandler 

class TornadoLogFormatter(logging.Formatter):
    colors = {
        logging.DEBUG: "\033[94m",  # Blue
        logging.INFO: "\033[92m",   # Green
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",   # Red
        logging.CRITICAL: "\033[1;91m"  # Bright Red
    }
    color_reset = "\033[0m"

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = f"Bad message ({e}): {record.__dict__}"
        record.asctime = time.strftime(
            "%m-%d %H:%M:%S", self.converter(record.created))
        prefix = f"{record.asctime} | {record.name} [{record.levelname}] :"
        color = self.colors.get(record.levelno, "")
        formatted = f"{color}{prefix}{self.color_reset} {record.message}"

        # Additional details
        extra_details = ' '.join(
            f"{k}={v}" for k, v in record.__dict__.items()
            if k not in {
                'levelname', 'asctime', 'module', 'lineno', 'args', 'message',
                'filename', 'exc_info', 'exc_text', 'created', 'funcName',
                'processName', 'process', 'msecs', 'relativeCreated', 'thread',
                'threadName', 'name', 'levelno', 'msg', 'pathname', 'stack_info',
            })
        if extra_details:
            formatted += f" {extra_details}"

        # Exception handling
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            formatted = f"{formatted.rstrip()}\n{record.exc_text}"
        return formatted.replace("\n", "\n    ")

LOGS = logging.getLogger('Kiyo')

def enable_pretty_logging(level=logging.DEBUG, color=None):
    """
    Enable pretty logging with Tornado-style formatting.

    Args:
        level: Logging level.
        color: Boolean to force color (default: autodetect based on terminal support).
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    log_path = pathlib.Path('./Main/logger') / 'kiyo.log'
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        log_path, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)

    formatter = TornadoLogFormatter()
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Set levels for specific loggers
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('psycopg2').setLevel(logging.WARNING)
    logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)
    logging.getLogger('apscheduler.scheduler').setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Apply color if requested
    if color is None:
        color = False
        if sys.stderr.isatty():
            try:
                import curses
                curses.setupterm()
                if curses.tigetnum("colors") > 0:
                    color = True
            except Exception:
                pass

    if color:
        formatter.colors = {
            logging.DEBUG: "\033[94m",    # Blue
            logging.INFO: "\033[92m",     # Green
            logging.WARNING: "\033[93m",  # Yellow
            logging.ERROR: "\033[91m",    # Red
            logging.CRITICAL: "\033[1;91m"  # Bright Red
        }
    LOGS.setLevel(level)
    LOGS.info('Initialized Logger')

