import os
from loguru import logger

logger.add(os.devnull, format="{time} {level} {message}", level="INFO")
