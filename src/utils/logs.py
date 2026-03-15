import logging

from config import config


def setup_logging():
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=config.LOG_FILE,
        filemode="a",
    )
