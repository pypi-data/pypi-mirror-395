import threading
from abc import ABCMeta


class Singleton(ABCMeta):
    """A thread-safe implementation of Singleton using metaclass."""

    _instances = {}  # type: ignore
    _lock = threading.Lock()  # Lock object for thread-safety

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:  # Ensure only one thread enters at a time
                if cls not in cls._instances:  # Double-check locking
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
