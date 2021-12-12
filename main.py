from lib.engine import Engine
import os
from loguru import logger

db_path = "sqlite:///test.db"
logger.info(db_path)

x = Engine(db_path)
