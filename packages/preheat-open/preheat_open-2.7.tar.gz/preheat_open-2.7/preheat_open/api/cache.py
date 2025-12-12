import logging
import os
import pickle
import shelve
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Optional

from preheat_open.configuration import CacheConfig

from ..interfaces import log_method_call
from ..time import datetime, timedelta

logger = logging.getLogger(__name__)


def io_decorator():
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.open()
            result = func(self, *args, **kwargs)
            self.close()
            return result

        return wrapper

    return decorator


@dataclass
class Cache(ABC):
    config: CacheConfig = field(default_factory=CacheConfig)

    def __post_init__(self) -> None:
        """
        Post-initialization processing to set up the cache configuration.
        """
        self.directory = (
            os.path.expanduser(self.config.directory) + f"/{self.__class__.__name__}"
        )
        os.makedirs(self.directory, exist_ok=True)

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, expire: int | None = None) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def open(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def check_key(self, key: str) -> bool:
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        methods_to_log = ["clear", "delete", "get", "set", "check_key"]
        for method_name in methods_to_log:
            method = getattr(cls, method_name, None)
            if method:
                decorated_method = log_method_call(logger=logger)(method)
                decorated_method = io_decorator()(decorated_method)
                setattr(cls, method_name, decorated_method)


def easy_cache(cache_attr: str = "_cache"):
    def decorator_cache(func):
        @wraps(func)
        def wrapper_cache(self, *args, **kwargs):
            prefix = f"{self.__class__.__name__}_{func.__name__}"
            key = f"{prefix}_{args}_{kwargs}"
            cache = getattr(self, cache_attr, None)
            if cache and cache.check_key(key):
                return cache.get(key)
            result = func(self, *args, **kwargs)
            if cache:
                cache.set(key, result)
            return result

        return wrapper_cache

    return decorator_cache


def get_cache(config: Optional[CacheConfig] = None) -> Cache | None:
    """
    Factory function to create a cache instance based on the configuration.

    :param config: Cache configuration.
    :return: An instance of a Cache subclass.
    """
    config = config or CacheConfig()
    classes = Cache.__subclasses__()
    cache_class = next((cls for cls in classes if cls.__name__ == config.type), None)
    if cache_class:
        return cache_class(config=config)


@dataclass
class CacheItem:
    key: str
    expires: datetime
    path: Optional[str] = None
    value: Optional[Any] = None


@dataclass
class SimplePickleCache(Cache):
    _registry: dict[str, CacheItem] = field(default_factory=dict)

    def __post_init__(self) -> None:
        super().__post_init__()
        self._registry_path = os.path.join(self.directory, "book.pkl")

    def open(self) -> None:
        # Load the _book mapping from a file if it exists
        if os.path.exists(self._registry_path):
            with open(self._registry_path, "rb") as f:
                self._registry = pickle.load(f)

    def close(self) -> None:
        # Save the _book mapping to a file
        with open(self._registry_path, "wb") as f:
            pickle.dump(self._registry, f)

    def set(self, key: str, value: Any, expire: timedelta | None = None) -> None:
        # Save the value to a file and update the _book mapping
        if expire is None and self.config.time_to_live is not None:
            expire = timedelta(seconds=self.config.time_to_live)
        if self.check_key(key):
            item = self._registry.get(key)
            file_path = item.path
        else:
            file_path = os.path.join(self.directory, f"{uuid.uuid4()}.pkl")
            item = CacheItem(key=key, path=file_path, expires=datetime.now() + expire)
        with open(file_path, "wb") as f:
            pickle.dump(value, f)
        self._registry[key] = item

    def __get(self, key: str) -> Any:
        if self.check_key(key):
            item = self._registry.get(key)
            if item.path and os.path.exists(item.path):
                with open(item.path, "rb") as f:
                    return pickle.load(f)
        return None

    def get(self, key: str) -> Any:
        # Retrieve the value from the file using the _book mapping
        return self.__get(key)

    def delete(self, key: str) -> None:
        # Delete the file and remove the key from the _book mapping
        if key in self._registry:
            item = self._registry.pop(key, None)
            if item.path and os.path.exists(item.path):
                os.remove(item.path)

    def clear(self) -> None:
        # Clear all cache files and the _book mapping
        for item in self._registry.values():
            if os.path.exists(item.path):
                os.remove(item.path)
        self._registry.clear()

    def check_key(self, key: str) -> bool:
        # Check if the key exists in the _book mapping
        item = self._registry.get(key)
        if not item or item.expires < datetime.now():
            self.delete(key)
            return False
        return True


@dataclass
class ShelveCache(Cache):
    def __post_init__(self) -> None:
        """
        Post-initialization processing to set up the cache configuration.
        """
        self._shelf: shelve.Shelf
        super().__post_init__()

    def open(self) -> None:
        """
        Opens the cache.
        """
        self._shelf = shelve.open(self.directory)

    def close(self) -> None:
        """
        Closes the cache.
        """
        self._shelf.close()

    def get(self, key: str) -> Any:
        """
        Gets a value from the cache.

        :param key: The key for the value.
        :type key: str
        :return: The value.
        :rtype: Any
        """
        try:
            item = self._shelf[key]
        except KeyError:
            return None
        return item.value

    def set(self, key: str, value: Any, expire: timedelta | None = None) -> None:
        """
        Sets a value in the cache.

        :param key: The key for the value.
        :type key: str
        :param value: The value to set.
        :type value: Any
        :param expire: The expiration time for the value.
        :type expire: int
        """
        if self.config.time_to_live is not None and expire is None:
            expire = timedelta(self.config.time_to_live)
        self._shelf[key] = CacheItem(
            key=key, value=value, expires=datetime.now() + expire.total_seconds()
        )

    def delete(self, key: str) -> None:
        """
        Deletes a value from the cache.

        :param key: The key for the value.
        :type key: str
        """
        del self._shelf[key]

    def clear(self) -> None:
        """
        Clears the cache.
        """
        self._shelf.clear()

    def check_key(self, key: str) -> bool:
        """
        Checks whether the key is present within the cache
        """
        return key in self._shelf
