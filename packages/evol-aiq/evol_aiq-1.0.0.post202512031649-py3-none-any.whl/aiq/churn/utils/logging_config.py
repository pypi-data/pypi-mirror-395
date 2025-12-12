import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logging(log_file: str, log_level: str, max_bytes: int, backup_count: int):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    log_level = getattr(logging, log_level.upper(), logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(log_level)

    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s')

    if not logger.hasHandlers():
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
