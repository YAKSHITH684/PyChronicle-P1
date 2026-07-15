"""
logger.py

Central logging utility for PyChronicle.

Features:
- Console logging
- File logging
- Timestamped messages
- Prevents duplicate handlers
"""

import logging
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "pychronicle.log"


def get_logger(name="PyChronicle", level=logging.INFO):
    """
    Create and return a configured logger.

    Parameters
    ----------
    name : str
        Logger name.

    level : int
        Logging level.

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File Handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


# -------------------------------------------------------------

if __name__ == "__main__":

    logger = get_logger()

    logger.info("PyChronicle started.")

    logger.warning("This is a warning.")

    logger.error("Example error.")

    logger.debug("Debug message.")

    logger.critical("Critical message.")