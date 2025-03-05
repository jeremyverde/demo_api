import logging
from src.settings import Settings

SETTINGS = Settings()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")
logger.info("Logger Initialization Complete")
