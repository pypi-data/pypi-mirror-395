import asyncio
import pickle
import zlib
from functools import wraps

import valkey
import valkey.asyncio as valkey_async
from django.core.cache.backends.base import BaseCache

try:
    import zstd
except ImportError:
    zstd = None


def ignore_connection_errors(func):
    """
    Decorator that catches connection errors and returns a default value.
    """
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(self, *args, **kwargs):
            if not self._ignore_exceptions:
                return await func(self, *args, **kwargs)
            try:
                return await func(self, *args, **kwargs)
            except (valkey.exceptions.ConnectionError, valkey.exceptions.TimeoutError):
                if func.__name__ in ["get", "aget"]:
                    return kwargs.get("default") or args[1] if len(args) > 1 else None
                elif func.__name__ in [
                    "set",
                    "aset",
                    "add",
                    "aadd",
                    "delete",
                    "adelete",
                    "touch",
                    "atouch",
                ]:
                    return False
                elif func.__name__ in [
                    "incr",
                    "aincr",
                    "decr",
                    "adecr",
                    "has_key",
                    "ahas_key",
                ]:
                    return 0
                return None

        return async_wrapper
    else:

        @wraps(func)
        def sync_wrapper(self, *args, **kwargs):
            if not self._ignore_exceptions:
                return func(self, *args, **kwargs)
            try:
                return func(self, *args, **kwargs)
            except (valkey.exceptions.ConnectionError, valkey.exceptions.TimeoutError):
                if func.__name__ in ["get", "aget"]:
                    return kwargs.get("default") or args[1] if len(args) > 1 else None
                elif func.__name__ in [
                    "set",
                    "aset",
                    "add",
                    "aadd",
                    "delete",
                    "adelete",
                    "touch",
                    "atouch",
                ]:
                    return False
                elif func.__name__ in [
                    "incr",
                    "aincr",
                    "decr",
                    "adecr",
                    "has_key",
                    "ahas_key",
                ]:
                    return 0
                return None

        return sync_wrapper


class ValkeyCache(BaseCache):
    def __init__(self, alias, params):
        super().__init__(params)
        self._location = params.get("LOCATION", "valkey://valkey:6379/1")
        self._options = params.get("OPTIONS", {})
        self._client = None
        self._async_client = None
        self._ignore_exceptions = self._options.get("IGNORE_EXCEPTIONS", False)
        self._compress_min_len = self._options.get("COMPRESS_MIN_LEN", 1024)

        if zstd:
            self._compressor = "zstd"
            self._compress = zstd.compress
            self._decompress = zstd.decompress
            self._magic_byte = b"z"
        else:
            self._compressor = "zlib"
            self._compress = zlib.compress
            self._decompress = zlib.decompress
            self._magic_byte = b"\x8f"

    def _get_valkey_client_kwargs(self):
        kwargs = self._options.copy()
        kwargs.pop("IGNORE_EXCEPTIONS", None)
        kwargs.pop("COMPRESS_MIN_LEN", None)
        return kwargs

    @property
    def client(self):
        if self._client is None:
            self._client = valkey.from_url(
                self._location, **self._get_valkey_client_kwargs()
            )
        return self._client

    @property
    def async_client(self):
        if self._async_client is None:
            self._async_client = valkey_async.from_url(
                self._location, **self._get_valkey_client_kwargs()
            )
        return self._async_client

    def get_raw_client(self, async_client=False):
        """
        Returns the underlying valkey connection object.
        """
        if async_client:
            return self.async_client
        return self.client

    def _get_expiration_time(self, timeout):
        if timeout is None:
            return None  # No expiration
        if timeout == 0:
            return 0  # Expire immediately
        return timeout  # Expire in seconds

    def _encode(self, value):
        pickled_value = pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
        if self._compress_min_len and len(pickled_value) > self._compress_min_len:
            return self._magic_byte + self._compress(pickled_value)
        return pickled_value

    def _decode(self, value):
        if value.startswith(b"z"):
            if zstd:
                return pickle.loads(zstd.decompress(value[1:]))
            return None
        if value.startswith(b"\x8f"):
            return pickle.loads(zlib.decompress(value[1:]))
        return pickle.loads(value)

    # Sync methods
    @ignore_connection_errors
    def get(self, key, default=None, version=None):
        _key = self.make_key(key, version=version)
        value = self.client.get(_key)
        if value is None:
            return default
        return self._decode(value)

    @ignore_connection_errors
    def set(self, key, value, timeout=None, version=None):
        _key = self.make_key(key, version=version)
        encoded_value = self._encode(value)
        ttl = self._get_expiration_time(timeout)
        if ttl == 0:
            self.client.delete(_key)
            return True
        elif ttl is None:
            return self.client.set(_key, encoded_value)
        else:
            return self.client.set(_key, encoded_value, ex=ttl)

    @ignore_connection_errors
    def add(self, key, value, timeout=None, version=None):
        _key = self.make_key(key, version=version)
        encoded_value = self._encode(value)
        ttl = self._get_expiration_time(timeout)
        if ttl == 0:
            return False  # if timeout is 0, treat as not adding.
        elif ttl is None:
            return self.client.set(_key, encoded_value, nx=True)
        else:
            return self.client.set(_key, encoded_value, ex=ttl, nx=True)

    @ignore_connection_errors
    def delete(self, key, version=None):
        _key = self.make_key(key, version=version)
        return self.client.delete(_key) > 0

    def close(self, **kwargs):
        # Clear the client instances so they can be re-lazy-loaded if needed.
        # This allows connections to be returned to the pool without killing the pool.
        self._client = None
        self._async_client = None

    @ignore_connection_errors
    def touch(self, key, timeout=0, version=None):
        _key = self.make_key(key, version=version)
        ttl = self._get_expiration_time(timeout)
        if ttl == 0:
            return self.client.delete(_key) > 0
        elif ttl is None:
            return self.client.persist(_key)
        else:
            return self.client.expire(_key, ttl)

    @ignore_connection_errors
    def incr(self, key, delta=1, version=None):
        value = self.get(key, version=version)
        if value is None:
            if self._ignore_exceptions:
                return 0
            raise ValueError("Key '%s' does not exist." % key)
        if not isinstance(value, int):
            raise ValueError("Key '%s' contains a non-integer value." % key)
        new_value = value + delta
        self.set(key, new_value, version=version)
        return new_value

    @ignore_connection_errors
    def decr(self, key, delta=1, version=None):
        value = self.get(key, version=version)
        if value is None:
            if self._ignore_exceptions:
                return 0
            raise ValueError("Key '%s' does not exist." % key)
        if not isinstance(value, int):
            raise ValueError("Key '%s' contains a non-integer value." % key)
        new_value = value - delta
        self.set(key, new_value, version=version)
        return new_value

    def lock(
        self,
        key,
        version=None,
        timeout=None,
        sleep=0.1,
        blocking=True,
        blocking_timeout=None,
        thread_local=True,
    ):
        _key = self.make_key(key, version=version)
        return self.client.lock(
            _key,
            timeout=timeout,
            sleep=sleep,
            blocking=blocking,
            blocking_timeout=blocking_timeout,
            thread_local=thread_local,
        )

    @ignore_connection_errors
    def has_key(self, key, version=None):
        _key = self.make_key(key, version=version)
        return self.client.exists(_key)

    # Async methods
    @ignore_connection_errors
    async def aget(self, key, default=None, version=None):
        _key = self.make_key(key, version=version)
        value = await self.async_client.get(_key)
        if value is None:
            return default
        return self._decode(value)

    @ignore_connection_errors
    async def aset(self, key, value, timeout=None, version=None):
        _key = self.make_key(key, version=version)
        encoded_value = self._encode(value)
        ttl = self._get_expiration_time(timeout)
        if ttl == 0:
            await self.async_client.delete(_key)
            return True
        elif ttl is None:
            return await self.async_client.set(_key, encoded_value)
        else:
            return await self.async_client.set(_key, encoded_value, ex=ttl)

    @ignore_connection_errors
    async def aadd(self, key, value, timeout=None, version=None):
        _key = self.make_key(key, version=version)
        encoded_value = self._encode(value)
        ttl = self._get_expiration_time(timeout)
        if ttl == 0:
            return False
        elif ttl is None:
            return await self.async_client.set(_key, encoded_value, nx=True)
        else:
            return await self.async_client.set(_key, encoded_value, ex=ttl, nx=True)

    @ignore_connection_errors
    async def adelete(self, key, version=None):
        _key = self.make_key(key, version=version)
        return await self.async_client.delete(_key) > 0

    async def aclose(self, **kwargs):
        # Similar to sync close, clear the client instances for re-lazy-loading.
        self._client = None
        self._async_client = None

    @ignore_connection_errors
    async def atouch(self, key, timeout=0, version=None):
        _key = self.make_key(key, version=version)
        ttl = self._get_expiration_time(timeout)
        if ttl == 0:
            return await self.async_client.delete(_key) > 0
        elif ttl is None:
            return await self.async_client.persist(_key)
        else:
            return await self.async_client.expire(_key, ttl)

    @ignore_connection_errors
    async def aincr(self, key, delta=1, version=None):
        value = await self.aget(key, version=version)
        if value is None:
            if self._ignore_exceptions:
                return 0
            raise ValueError("Key '%s' does not exist." % key)
        if not isinstance(value, int):
            raise ValueError("Key '%s' contains a non-integer value." % key)
        new_value = value + delta
        await self.aset(key, new_value, version=version)
        return new_value

    @ignore_connection_errors
    async def adecr(self, key, delta=1, version=None):
        value = await self.aget(key, version=version)
        if value is None:
            if self._ignore_exceptions:
                return 0
            raise ValueError("Key '%s' does not exist." % key)
        if not isinstance(value, int):
            raise ValueError("Key '%s' contains a non-integer value." % key)
        new_value = value - delta
        await self.aset(key, new_value, version=version)
        return new_value

    def alock(
        self,
        key,
        version=None,
        timeout=None,
        sleep=0.1,
        blocking=True,
        blocking_timeout=None,
        thread_local=True,
    ):
        _key = self.make_key(key, version=version)
        return self.async_client.lock(
            _key,
            timeout=timeout,
            sleep=sleep,
            blocking=blocking,
            blocking_timeout=blocking_timeout,
            thread_local=thread_local,
        )

    @ignore_connection_errors
    async def ahas_key(self, key, version=None):
        _key = self.make_key(key, version=version)
        return await self.async_client.exists(_key)
