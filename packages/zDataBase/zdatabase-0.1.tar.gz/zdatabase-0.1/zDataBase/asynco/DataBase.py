import aiosqlite
import asyncio
import json
from collections import deque
from shutil import copyfile
from typing import Optional, get_type_hints
import time

# -----------------------
# JSON helpers
# -----------------------
def _json_dumps(v):
    return json.dumps(v, separators=(",", ":"), ensure_ascii=False)

def _json_loads(s):
    return json.loads(s)

# -----------------------
# Proxy types async
# -----------------------
class AZValue:
    def __init__(self, db, key, value):
        self._db = db
        self._key = key
        self._val = value

    def get(self):
        return self._val

    async def set(self, value):
        self._val = value
        await self._db._queue_set(self._key, self._val)

    async def save(self):
        await self._db._queue_set(self._key, self._val)

    def __str__(self):
        return str(self._val)

    def __repr__(self):
        return f"AZValue({self._val!r})"

class AZList(list):
    _mutating = {"append","extend","insert","pop","remove","clear","reverse","sort","__setitem__","__delitem__"}

    def __init__(self, initial, db, key):
        super().__init__(initial)
        self._db = db
        self._key = key

    def _mark(self):
        return self._db._queue_set(self._key, list(self))

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if callable(attr) and name in AZList._mutating:
            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                asyncio.create_task(self._mark())
                return result
            return wrapper
        return attr

    async def save(self):
        await self._mark()

class AZDict(dict):
    _mutating = {"__setitem__","__delitem__","pop","popitem","clear","update","setdefault"}

    def __init__(self, initial, db, key):
        super().__init__(initial)
        self._db = db
        self._key = key

    def _mark(self):
        return self._db._queue_set(self._key, dict(self))

    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        asyncio.create_task(self._mark())

    def __delitem__(self, k):
        super().__delitem__(k)
        asyncio.create_task(self._mark())

    async def save(self):
        await self._mark()

# -----------------------
# Async Model base
# -----------------------
class AModel:
    __table__: Optional[str] = None

    def __init__(self, **kwargs):
        hints = get_type_hints(self.__class__)
        for k in hints:
            setattr(self, k, kwargs.get(k, None))

    @classmethod
    def table_name(cls):
        return cls.__table__ or cls.__name__.lower()

    def to_dict(self):
        hints = get_type_hints(self.__class__)
        return {k: getattr(self, k) for k in hints}

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

# -----------------------
# Main Async DataBase class
# -----------------------
class AsyncDataBase:
    def __init__(self, name_db: str, auto_save=True, use_queue=True, queue_interval=0.5,
                 max_batch=500, backup: Optional[str]=None, backup_interval=60,
                 cache_enabled=True, cache_max_items=10000):
        self.name = name_db
        self.file = f"{name_db}.db"
        self.auto_save = auto_save
        self.use_queue = use_queue
        self.queue_interval = queue_interval
        self.max_batch = max_batch
        self.backup = backup
        self.backup_interval = backup_interval
        self.cache_enabled = cache_enabled
        self.cache_max_items = cache_max_items

        self._conn: Optional[aiosqlite.Connection] = None
        self._lock = asyncio.Lock()
        self._queue = deque()
        self._cache = {}
        self._cache_order = deque()
        self._worker_task: Optional[asyncio.Task] = None
        self._stop_worker = False

    async def open(self):
        self._conn = await aiosqlite.connect(self.file)
        await self._setup_table()
        if self.use_queue:
            self._worker_task = asyncio.create_task(self._worker_loop())
        if self.backup == "interval":
            asyncio.create_task(self._backup_loop())

    async def _setup_table(self):
        async with self._lock:
            await self._conn.execute(f"""
                CREATE TABLE IF NOT EXISTS "{self.name}" (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at REAL
                );
            """)
            await self._conn.commit()

    # -----------------------
    # Backup
    async def _backup_now(self):
        backup_file = f"{self.name}_backup.db"
        async with self._lock:
            await self._conn.commit()
            copyfile(self.file, backup_file)

    async def _backup_loop(self):
        while True:
            await asyncio.sleep(self.backup_interval)
            try:
                await self._backup_now()
            except:
                pass

    # -----------------------
    # Queue
    async def _queue_set(self, key, value):
        self._queue.append(("SET", key, value))
        if not self.use_queue and self.auto_save:
            await self.save()
        if self.cache_enabled:
            self._cache_set(key,value)

    async def _queue_delete(self, key):
        self._queue.append(("DEL", key, None))
        if not self.use_queue and self.auto_save:
            await self.save()
        if self.cache_enabled:
            self._cache.pop(key,None)

    async def _worker_loop(self):
        while not self._stop_worker:
            await asyncio.sleep(self.queue_interval)
            to_flush=[]
            while self._queue and len(to_flush)<self.max_batch:
                to_flush.append(self._queue.popleft())
            if to_flush:
                await self._flush_batch(to_flush)

    async def _flush_batch(self, ops):
        async with self._lock:
            ts=time.time()
            async with self._conn.execute("BEGIN"):
                for op,key,val in ops:
                    if op=="SET":
                        s=_json_dumps(val)
                        await self._conn.execute(f'REPLACE INTO "{self.name}" (key,value,updated_at) VALUES(?,?,?);',(key,s,ts))
                    elif op=="DEL":
                        await self._conn.execute(f'DELETE FROM "{self.name}" WHERE key=?;',(key,))
                await self._conn.commit()

    # -----------------------
    # Cache
    def _cache_set(self,key,val):
        if not self.cache_enabled:
            return
        self._cache[key]=val
        self._cache_order.append(key)
        while len(self._cache_order)>self.cache_max_items:
            k=self._cache_order.popleft()
            self._cache.pop(k,None)

    def _cache_get(self,key):
        if not self.cache_enabled:
            return None
        v=self._cache.get(key)
        if v is not None:
            try: self._cache_order.remove(key)
            except ValueError: pass
            self._cache_order.append(key)
        return v

    # -----------------------
    # KV API
    async def set(self,key,value):
        await self._queue_set(key,value)

    async def get(self,key,default=None):
        cached=self._cache_get(key)
        if cached is not None:
            return self._wrap_proxy(key,cached)
        async with self._lock:
            async with self._conn.execute(f'SELECT value FROM "{self.name}" WHERE key=?;', (key,)) as cursor:
                row = await cursor.fetchone()
        if not row:
            return default
        val=_json_loads(row[0])
        self._cache_set(key,val)
        return self._wrap_proxy(key,val)

    async def delete(self,key):
        await self._queue_delete(key)

    async def clear(self):
        async with self._lock:
            await self._conn.execute(f'DELETE FROM "{self.name}";')
            await self._conn.commit()
        self._cache.clear()
        self._cache_order.clear()

    async def save(self):
        if self.use_queue:
            to_flush=[]
            while self._queue: to_flush.append(self._queue.popleft())
            if to_flush:
                await self._flush_batch(to_flush)
        else:
            async with self._lock:
                await self._conn.commit()

    def _wrap_proxy(self,key,val):
        if isinstance(val,list): return AZList(val,self,key)
        if isinstance(val,dict): return AZDict(val,self,key)
        return AZValue(self,key,val)

    async def close(self):
        await self.save()
        self._stop_worker=True
        if self._worker_task:
            await asyncio.sleep(self.queue_interval)
        if self._conn:
            await self._conn.close()
