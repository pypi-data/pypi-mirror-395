import logging
from logging.handlers import RotatingFileHandler
import platformdirs
from pathlib import Path

log_dir = Path(platformdirs.user_log_dir("pushtunes", ensure_exists=True))
log_file = log_dir / "pushtunes.log"

logger = logging.getLogger("pushtunes")
logger.setLevel(logging.DEBUG)

fh = RotatingFileHandler(
    log_file,
    maxBytes=1_000_000,  # 1 MB
    backupCount=5,
    encoding="utf-8",
)
fh.setLevel(logging.DEBUG)

# Console gets INFO and above by default
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

file_fmt = logging.Formatter(
    "%(asctime)s  %(levelname)-7s  %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)


console_fmt = logging.Formatter("%(asctime)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


fh.setFormatter(file_fmt)
ch.setFormatter(console_fmt)

logger.addHandler(fh)
logger.addHandler(ch)


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name or "pushtunes")


def set_console_log_level(level: str | int) -> None:
    """Set the console log level.

    Args:
        level: Log level as string ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
               or as int (logging.DEBUG, logging.INFO, etc.)
    """
    if isinstance(level, str):
        level = level.upper()
        level_int = getattr(logging, level, None)
        if level_int is None:
            raise ValueError(
                f"Invalid log level: {level}. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"
            )
    else:
        level_int = level

    # Find the console handler and update its level
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler) and not isinstance(
            handler, RotatingFileHandler
        ):
            handler.setLevel(level_int)
            break
