from sqlalchemy import create_engine
from loguru import logger

class Engine:
  def __init__(self, db_connstring: str) -> None:
      self._engine = create_engine(db_connstring)
      self._engine.connect()
