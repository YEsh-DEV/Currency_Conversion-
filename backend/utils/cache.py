import time
from threading import Lock


class SimpleTTLCache:
    """A minimal in-memory TTL cache. Not distributed. Thread-safe for simple use."""

    def __init__(self):
        self._store = {}
        self._lock = Lock()

    def set(self, key, value, ttl_seconds: int):
        expire = time.time() + ttl_seconds
        with self._lock:
            self._store[key] = (value, expire)

    def get(self, key, default=None):
        with self._lock:
            val = self._store.get(key)
            if not val:
                return default
            value, expire = val
            if time.time() > expire:
                del self._store[key]
                return default
            return value

    def clear(self):
        with self._lock:
            self._store.clear()
