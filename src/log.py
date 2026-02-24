import logging
import sys
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger("infra_automation")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    os.makedirs("logs", exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s | %(message)s"
    )

    # Rotating file handler
    file_handler = RotatingFileHandler(
        "logs/provisioning.log",
        maxBytes=100_000,
        backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger