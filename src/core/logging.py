import os
from loguru import logger

os.makedirs("logs", exist_ok=True)
logger.remove()

fmt = "{time:DD-MMM-YYYY HH:mm:ss TZ} | {level} | {name} | {function} | {line} | {message}"

logger.add(
    "logs/debug_{time:YYYY-MM-DD}.log",
    level="DEBUG",
    rotation="00:00",
    retention="7 days",
    compression="zip",
    filter=lambda record: record["level"].no <= 20,
    format=fmt,
)
logger.add(
    "logs/error_{time:YYYY-MM-DD}.log",
    level="WARNING",
    rotation="00:00",
    retention="7 days",
    compression="zip",
    format=fmt,
)
