# TODO
import asyncio
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

import a_sync
from concurrent.futures import ThreadPoolExecutor
from msgspec.json import encode
from pony.orm import Database, PrimaryKey, Required, db_session, select
from pony.orm.core import Query

from generic_exporters.processors.exporters.datastores.timeseries._base import TimeSeriesDataStoreBase


Jsonable = Any

db = Database()

class SQLTimeSeriesKeyValueStore(TimeSeriesDataStoreBase):
    push = None  # make abc work TODO refactor this out
    def __init__(self, **connection_params: Optional[Dict[str, Any]]) -> None:
        if not connection_params:
            from generic_exporters.processors.exporters.datastores.default import sqlite_settings as connection_params
        db.bind(**connection_params)
        db.generate_mapping(create_tables=True)
        self.push = a_sync.ProcessingQueue(self._push, num_workers=10_000, return_data=False)
    async def data_exists(self, key: Jsonable, ts: datetime) -> bool:
        """Returns True if `key` returns results from your Postgres db at `ts`, False if not."""
        if (result_count := await TimeSeriesKV.count(key, ts)) == 0:
            return False
        elif result_count == 1:
            return True
        raise ValueError(f"`result_count` should not be > 1 but is {result_count}")
    
    async def _push(self, key: Jsonable, ts: datetime, value: Jsonable) -> None:
        """Exports `data` to Victoria Metrics using `key` somehow. lol"""
        if isinstance(value, (int, float, Decimal)) and value >= 10 ** 20:  # max value in Decimal(38,18)
            logger.warning("%s at %s: %s exceeds the max size for Decimal(38,18)", key, ts, value)
        else:
            await TimeSeriesKV.insert(key, ts, value)


db_thread = ThreadPoolExecutor(1)

class TimeSeriesKV(db.Entity):
    key = Required(bytes)
    timestamp = Required(datetime)
    PrimaryKey(key, timestamp)

    value = Required(bytes)

    @classmethod
    async def count(cls, key: Jsonable, timestamp: datetime) -> int:
        return await asyncio.get_event_loop().run_in_executor(db_thread, cls._count, key, timestamp)

    @classmethod
    async def insert(cls, key: Jsonable, timestamp: datetime, value: Jsonable) -> int:
        return await asyncio.get_event_loop().run_in_executor(db_thread, cls._insert, key, timestamp, value)
    
    @classmethod
    @db_session
    def _count(cls, key: Jsonable, timestamp: datetime) -> int:
        return cls._select(key, timestamp).count()
    
    @classmethod
    @db_session
    def _select(cls, key: Jsonable, timestamp: datetime) -> Query:
        return select(data for data in cls if data.key == encode(key) and data.timestamp == timestamp)
    
    @classmethod
    @db_session
    def _insert(cls, key: Jsonable, timestamp: datetime, value: Jsonable) -> None:
        TimeSeriesKV(key=key, timestamp=timestamp, value=value)
