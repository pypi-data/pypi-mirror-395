import hashlib
import json
import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class CacheEntry(Base):
  __tablename__ = 'tool_cache'

  id = Column(Integer, primary_key=True, autoincrement=True)
  tool_name = Column(String(512), nullable=False)
  params_hash = Column(String(512), nullable=False)
  params = Column(Text, nullable=False)
  result = Column(Text, nullable=True)
  last_modified = Column(DateTime, default=datetime.now())


class ToolCache:
  def __init__(self, db_path="tool_cache.db"):
    self.db_path = f"sqlite:///{db_path}"
    self.engine = create_engine(self.db_path)
    self.Session = sessionmaker(bind=self.engine)
    self.cache_expire_time = int(os.getenv('CACHE_EXPIRE_TIME', default='0'))
    Base.metadata.create_all(self.engine)

  def _hash_params(self, tool_name, params):
    """Create a hash of the tool name and parameters."""
    params_str = f"{tool_name}_{params}"
    return hashlib.sha256(params_str.encode()).hexdigest()

  def get_cached_result(self, tool_name, **kwargs):
    """
    Retrieve cached result if it exists and is not expired.
    Returns None if no valid cache entry found.
    """
    if self.cache_expire_time == 0:
      return None

    params_str = json.dumps(kwargs, sort_keys=True)
    params_hash = self._hash_params(tool_name, params_str)
    session = self.Session()

    try:
      entry = session.query(CacheEntry).filter(
        CacheEntry.tool_name == tool_name,
        CacheEntry.params_hash == params_hash,
      ).first()

      if entry:
        if self.cache_expire_time < 0 or (datetime.now() - entry.last_modified).total_seconds() < self.cache_expire_time:
          return entry.result
    finally:
      session.close()

    return None

  def save_result(self, tool_name, result, **kwargs):
    """Save the result to cache."""
    params_str = json.dumps(kwargs, sort_keys=True)
    params_hash = self._hash_params(tool_name, params_str)
    result_str = json.dumps(result) if not isinstance(result, str) else result

    session = self.Session()
    try:
      entry = session.query(CacheEntry).filter(
        CacheEntry.tool_name == tool_name,
        CacheEntry.params_hash == params_hash,
      ).first()

      if entry:
        # Update existing entry
        entry.params = params_str
        entry.result = result_str
        entry.last_modified = datetime.now()
      else:
        # Create new entry
        entry = CacheEntry(
          tool_name=tool_name,
          params_hash=params_hash,
          params=params_str,
          result=result_str,
          last_modified=datetime.now()
        )
        session.add(entry)

      session.commit()
    except Exception as e:
      print(f"Failed to save cache: {e}")
      session.rollback()
    finally:
      session.close()
