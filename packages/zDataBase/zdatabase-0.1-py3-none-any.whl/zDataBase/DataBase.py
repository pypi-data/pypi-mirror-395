import sqlite3
import json
import os
import threading
import time
from collections import deque
from contextlib import contextmanager
from shutil import copyfile
from typing import Optional, Type, get_type_hints

# -----------------------
# JSON helpers
# -----------------------
def _json_dumps(v):
    return json.dumps(v, separators=(",", ":"), ensure_ascii=False)

def _json_loads(s):
    return json.loads(s)

# -----------------------
# Proxy types
# -----------------------
class ZValue:
    def __init__(self, db, key, value):
        self._db = db
        self._key = key
        self._val = value

    def get(self):
        return self._val

    def set(self, value):
        self._val = value
        self._db._queue_set(self._key, self._val)

    def save(self):
        self._db._queue_set(self._key, self._val)

    def __str__(self):
        return str(self._val)

    def __repr__(self):
        return f"ZValue({self._val!r})"

class ZList(list):
    _mutating = {"append","extend","insert","pop","remove","clear","reverse","sort","__setitem__","__delitem__"}

    def __init__(self, initial, db, key):
        super().__init__(initial)
        self._db = db
        self._key = key

    def _mark(self):
        self._db._queue_set(self._key, list(self))

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if callable(attr) and name in ZList._mutating:
            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                self._mark()
                return result
            return wrapper
        return attr

    def save(self):
        self._mark()

class ZDict(dict):
    _mutating = {"__setitem__","__delitem__","pop","popitem","clear","update","setdefault"}

    def __init__(self, initial, db, key):
        super().__init__(initial)
        self._db = db
        self._key = key

    def _mark(self):
        self._db._queue_set(self._key, dict(self))

    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        self._mark()

    def __delitem__(self, k):
        super().__delitem__(k)
        self._mark()

    def save(self):
        self._mark()

# -----------------------
# Model base
# -----------------------
class Model:
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
# Main DataBase class
# -----------------------
class DataBase:
    def __init__(
        self,
        name_db: str,
        auto_save = True,
        use_queue = True,
        queue_interval = 0.5,
        max_batch = 500,
        backup: Optional[str] = None,
        backup_interval = 60,
        use_sqlcipher = False,
        cipher_key = None,
        cache_enabled = True,
        cache_max_items = 10000
    ):
        self.name = name_db
        self.file = f"{name_db}.db"
        self.auto_save = auto_save
        self.use_queue = use_queue
        self.queue_interval = queue_interval
        self.max_batch = max_batch
        self.backup = backup
        self.backup_interval = backup_interval
        self.use_sqlcipher = use_sqlcipher
        self.cipher_key = cipher_key
        self.cache_enabled = cache_enabled
        self.cache_max_items = cache_max_items

        self._conn = None
        self._cursor = None
        self._lock = threading.RLock()
        self._queue = deque()
        self._queue_cond = threading.Condition()
        self._worker = None
        self._stop_worker = False
        self._cache = {}
        self._cache_order = deque()

        self._open()
        self._setup_table()
        if self.use_queue:
            self._start_worker()
        if self.backup == "interval":
            self._start_backup_loop()

    def _open(self):
        self._conn = sqlite3.connect(self.file, check_same_thread=False, isolation_level=None)
        self._cursor = self._conn.cursor()
        if self.use_sqlcipher and self.cipher_key:
            try:
                self._cursor.execute(f"PRAGMA key = '{self.cipher_key}';")
            except:
                pass

    def _setup_table(self):
        with self._lock:
            self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS "{self.name}" (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at REAL
                );
            """)
            self._conn.commit()

    # Backup
    def _backup_now(self):
        backup_file = f"{self.name}_backup.db"
        with self._lock:
            self._conn.commit()
            copyfile(self.file, backup_file)

    def _start_backup_loop(self):
        def loop():
            while True:
                time.sleep(self.backup_interval)
                try:
                    self._backup_now()
                except:
                    pass
        t = threading.Thread(target=loop, daemon=True)
        t.start()

    # Write queue
    def _start_worker(self):
        self._worker = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker.start()

    def _worker_loop(self):
        while not self._stop_worker:
            with self._queue_cond:
                self._queue_cond.wait(timeout=self.queue_interval)
                to_flush = []
                while self._queue and len(to_flush) < self.max_batch:
                    to_flush.append(self._queue.popleft())
            if to_flush:
                try:
                    self._flush_batch(to_flush)
                except:
                    pass

    def _queue_set(self, key, value):
        entry = ("SET", key, value)
        with self._queue_cond:
            self._queue.append(entry)
            self._queue_cond.notify()
        if self.cache_enabled:
            self._cache_set(key, value)
        if not self.use_queue and self.auto_save:
            self.save()

    def _queue_delete(self, key):
        entry = ("DEL", key, None)
        with self._queue_cond:
            self._queue.append(entry)
            self._queue_cond.notify()
        if self.cache_enabled and key in self._cache:
            with self._lock:
                self._cache.pop(key, None)
        if not self.use_queue and self.auto_save:
            self.save()

    def _flush_batch(self, ops):
        with self._lock:
            try:
                self._cursor.execute("BEGIN;")
                ts = time.time()
                for op, key, val in ops:
                    if op == "SET":
                        s = _json_dumps(val)
                        self._cursor.execute(
                            f'REPLACE INTO "{self.name}" (key, value, updated_at) VALUES (?, ?, ?);',
                            (key, s, ts)
                        )
                    elif op == "DEL":
                        self._cursor.execute(f'DELETE FROM "{self.name}" WHERE key=?;', (key,))
                self._conn.commit()
            except:
                try: self._conn.rollback()
                except: pass
                raise
        if self.backup == "always":
            self._backup_now()

    # Cache
    def _cache_set(self, key, value):
        if not self.cache_enabled:
            return
        self._cache[key] = value
        self._cache_order.append(key)
        while len(self._cache_order) > self.cache_max_items:
            k = self._cache_order.popleft()
            self._cache.pop(k, None)

    def _cache_get(self, key):
        if not self.cache_enabled:
            return None
        v = self._cache.get(key)
        if v is not None:
            try: self._cache_order.remove(key)
            except ValueError: pass
            self._cache_order.append(key)
        return v

    # KV API
    def __setitem__(self, key, value):
        if isinstance(value, (ZList,ZDict,ZValue)):
            if isinstance(value,ZList): value=list(value)
            elif isinstance(value,ZDict): value=dict(value)
            elif isinstance(value,ZValue): value=value.get()
        if not isinstance(key,str): key=str(key)
        self._queue_set(key,value)

    def __getitem__(self,key):
        if not isinstance(key,str): key=str(key)
        cached = self._cache_get(key)
        if cached is not None:
            return self._wrap_proxy(key,cached)
        with self._lock:
            self._cursor.execute(f'SELECT value FROM "{self.name}" WHERE key=?;', (key,))
            row = self._cursor.fetchone()
        if not row:
            raise KeyError(key)
        val = _json_loads(row[0])
        self._cache_set(key,val)
        return self._wrap_proxy(key,val)

    def get(self,key,default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __delitem__(self,key):
        if not isinstance(key,str): key=str(key)
        self._queue_delete(key)

    def clear(self):
        with self._lock:
            self._cursor.execute(f'DELETE FROM "{self.name}";')
            self._conn.commit()
        self._cache.clear()
        self._cache_order.clear()

    def drop(self):
        with self._lock:
            self._cursor.execute(f'DROP TABLE IF EXISTS "{self.name}";')
            self._conn.commit()
            self._conn.close()
            self._conn=None
        try: os.remove(self.file)
        except: pass

    def save(self):
        if self.use_queue:
            with self._queue_cond:
                to_flush=[]
                while self._queue: to_flush.append(self._queue.popleft())
            if to_flush: self._flush_batch(to_flush)
        else:
            with self._lock:
                self._conn.commit()

    def close(self):
        self.save()
        self._stop_worker = True
        if self._worker and self._worker.is_alive():
            with self._queue_cond: self._queue_cond.notify_all()
            self._worker.join(timeout=1.0)
        with self._lock:
            try: self._conn.close()
            except: pass

    def _wrap_proxy(self,key,val):
        if isinstance(val,list): return ZList(val,self,key)
        if isinstance(val,dict): return ZDict(val,self,key)
        return ZValue(self,key,val)

    # Transactions
    @contextmanager
    def transaction(self):
        self.save()
        with self._lock:
            try:
                self._cursor.execute("BEGIN;")
                yield
                self._conn.commit()
            except:
                try: self._conn.rollback()
                except: pass
                raise

    # Atomic utils
    def increment(self,key,delta=1,default=0):
        with self._lock:
            self._cursor.execute(f'SELECT value FROM "{self.name}" WHERE key=?;', (key,))
            row=self._cursor.fetchone()
            if not row: value=default
            else:
                v=_json_loads(row[0])
                if not isinstance(v,(int,float)): raise TypeError("Value not numeric")
                value=v
            value+=delta
            s=_json_dumps(value)
            ts=time.time()
            self._cursor.execute(f'REPLACE INTO "{self.name}" (key,value,updated_at) VALUES(?,?,?);',(key,s,ts))
            self._conn.commit()
            self._cache_set(key,value)
            return value

    def append_if_not_exists(self,key,element):
        with self._lock:
            self._cursor.execute(f'SELECT value FROM "{self.name}" WHERE key=?;', (key,))
            row=self._cursor.fetchone()
            if not row: lst=[element]
            else:
                v=_json_loads(row[0])
                if not isinstance(v,list): raise TypeError("Value not list")
                lst=v
                if element in lst: return False
                lst.append(element)
            s=_json_dumps(lst)
            ts=time.time()
            self._cursor.execute(f'REPLACE INTO "{self.name}" (key,value,updated_at) VALUES(?,?,?);',(key,s,ts))
            self._conn.commit()
            self._cache_set(key,lst)
            return True

    # Model layer
    def register_model(self,model_cls: Type[Model]):
        tbl=model_cls.table_name()
        with self._lock:
            self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS "{tbl}" (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at REAL
                );
            """)
            self._conn.commit()

    def model_save(self,model_obj: Model,key:str):
        tbl=model_obj.table_name()
        data=model_obj.to_dict()
        s=_json_dumps(data)
        ts=time.time()
        with self._lock:
            self._cursor.execute(f'REPLACE INTO "{tbl}" (key,value,updated_at) VALUES(?,?,?);',(key,s,ts))
            self._conn.commit()

    def model_get(self,model_cls: Type[Model],key:str):
        tbl=model_cls.table_name()
        with self._lock:
            self._cursor.execute(f'SELECT value FROM "{tbl}" WHERE key=?;', (key,))
            row=self._cursor.fetchone()
        if not row: raise KeyError(key)
        d=_json_loads(row[0])
        return model_cls.from_dict(d)

    # Listing
    def keys(self,prefix: Optional[str]=None):
        with self._lock:
            if prefix:
                like=f"{prefix}%"
                self._cursor.execute(f'SELECT key FROM "{self.name}" WHERE key LIKE ?;', (like,))
            else:
                self._cursor.execute(f'SELECT key FROM "{self.name}";')
            return [r[0] for r in self._cursor.fetchall()]

    def items(self,prefix: Optional[str]=None):
        with self._lock:
            if prefix:
                like=f"{prefix}%"
                self._cursor.execute(f'SELECT key,value FROM "{self.name}" WHERE key LIKE ?;', (like,))
            else:
                self._cursor.execute(f'SELECT key,value FROM "{self.name}";')
            return [(r[0],_json_loads(r[1])) for r in self._cursor.fetchall()]

    def __del__(self):
        try: self.close()
        except: pass
