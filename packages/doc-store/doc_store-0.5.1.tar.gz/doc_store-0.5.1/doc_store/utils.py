import base64
import getpass
import io
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

import numpy as np


class BlockingThreadPool(ThreadPoolExecutor):
    """A thread pool that blocks submission
    if the maximum number of workers is reached."""

    def __init__(
        self,
        max_workers=None,
        thread_name_prefix="",
        initializer=None,
        initargs=(),
    ):
        super().__init__(
            max_workers=max_workers,
            thread_name_prefix=thread_name_prefix,
            initializer=initializer,
            initargs=initargs,
        )
        print(f"max_workers={self._max_workers}")
        self._semaphore = threading.Semaphore(self._max_workers)

    def submit(self, fn, /, *args, **kwargs):
        self._semaphore.acquire()
        future = super().submit(fn, *args, **kwargs)
        future.add_done_callback(lambda _: self._semaphore.release())
        return future


def get_username() -> str:
    """Get the current user name."""
    username = getpass.getuser()
    if not username:
        username = os.getlogin()
    if not username:
        username = "unknown"
    return username


def secs_to_readable(secs: int) -> str:
    """Convert seconds to a human-readable format."""
    hours, secs = secs // 3600, secs % 3600
    minutes, secs = secs // 60, secs % 60
    # return in 01:11:30 format
    return f"{hours:02}:{minutes:02}:{secs:02}"


def encode_ndarray(array: np.ndarray) -> str:
    with io.BytesIO() as buffer:
        np.save(buffer, array, allow_pickle=False)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")


def decode_ndarray(string: str) -> np.ndarray:
    with io.BytesIO(base64.b64decode(string)) as buffer:
        return np.load(buffer, allow_pickle=False)


def timed_property(ttl: int):
    """A decorator to create a cached property with a TTL."""

    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(self):
            key = id(self)
            now = time.time()

            if key in cache:
                value, expire_time = cache[key]
                if ttl <= 0 or now < expire_time:
                    return value

            value = func(self)
            expire_time = float("inf") if ttl <= 0 else now + ttl
            cache[key] = (value, expire_time)
            return value

        return property(wrapper)

    return decorator
