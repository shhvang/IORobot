import sys, re
import time
import logging
import pathlib
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)

class TornadoLogFormatter(logging.Formatter):
    colors = {
        logging.DEBUG: "\033[94m",   # Blue
        logging.INFO: "\033[92m",    # Green
        logging.WARNING: "\033[93m", # Yellow
        logging.ERROR: "\033[91m",   # Red
        logging.CRITICAL: "\033[1;91m"  # Bright Red
    }
    color_reset = "\033[0m"

    def __init__(self, include_logger_name=False, keyword_highlight=True, truncate_message=0):
        super().__init__()
        self.include_logger_name = include_logger_name
        self.keyword_highlight = keyword_highlight
        self.truncate_message = truncate_message

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = f"Bad message ({e}): {record.__dict__}"     
        record.asctime = time.strftime(
            "%Y-%m-%d %H:%M:%S", self.converter(record.created))
        levelname_color = self.colors.get(record.levelno, "")
        levelname = f"{levelname_color}[{record.levelname.upper()}]{self.color_reset}"
        
        prefix = f"{record.asctime} |"
        
        if self.include_logger_name:
            prefix += f" {record.name}"
        
        prefix += f" {levelname} :"
        formatted = f"{prefix} {record.message}"
        if self.keyword_highlight:
            keywords = ['error', 'exception', 'critical']
            for keyword in keywords:
                formatted = re.sub(rf"\b{keyword}\b", f"\033[1m{keyword.upper()}\033[0m", formatted, flags=re.IGNORECASE)
        
        if self.truncate_message and len(formatted) > self.truncate_message:
            formatted = formatted[:self.truncate_message] + "..."
        if '\n' in formatted:
            formatted_lines = formatted.split('\n')
            formatted = '\n'.join([formatted_lines[0]] +
                                  ['    ' + line for line in formatted_lines[1:]])
        extra_details = ' '.join(
            f"{k}={v}" for k, v in record.__dict__.items()
            if k not in {
                'levelname', 'asctime', 'module', 'lineno', 'args', 'message',
                'filename', 'exc_info', 'exc_text', 'created', 'funcName',
                'processName', 'process', 'msecs', 'relativeCreated', 'thread',
                'threadName', 'name', 'levelno', 'msg', 'pathname', 'stack_info',
            } and k != 'taskName') 
        if extra_details:
            formatted += f" {extra_details}"
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            formatted = f"{formatted.rstrip()}\n{record.exc_text}"
        
        return formatted

def enablelogging(level=logging.DEBUG, color=None):
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

    log_path = pathlib.Path('./kiyo/logger') / 'kiyo.log'
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        log_path, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)

    formatter = TornadoLogFormatter(
        include_logger_name=True, keyword_highlight=True, truncate_message=0
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Set levels for specific loggers
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('psycopg2').setLevel(logging.WARNING)
    logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)
    logging.getLogger('apscheduler.scheduler').setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger('telegram.ext').setLevel(logging.WARNING)

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
    logger.setLevel(level)
    logger.info('Initialized Logger')