from functools import wraps
import time

from .models import DbLock


class LockingFailed(Exception):
    pass


class Lock:

    def __init__(self, name, block=True, block_timeout=None, raise_exception=True, retry_delay=0.5):
        self.name = name
        self.block = block
        self.block_timeout = block_timeout
        self.raise_exception = raise_exception
        self.retry_delay = retry_delay
        self.acquired = False

    def acquire(self):
        started_at = time.time()

        while True:
            # Try to lock.
            self.acquired = DbLock.objects.get_or_create(name=self.name)[1]

            # Acquiring succeeded.
            if self.acquired:
                return True

            # Lock was already acquired by some other process.

            # If blocking is not requested, then just give up.
            if not self.block:
                if self.raise_exception:
                    raise LockingFailed()
                return False

            # If blocking timeout is reached, then give up.
            if self.block_timeout and (time.time() - started_at) > self.block_timeout:
                if self.raise_exception:
                    raise LockingFailed()
                return False

            # Wait a little bit before trying again.
            time.sleep(self.retry_delay)

    def release(self):
        if self.acquired:
            DbLock.objects.filter(name=self.name).delete()
            self.acquired = False

    def __enter__(self):
        if not self.acquire():
            raise LockingFailed()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.release()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.acquire():
                return None
            try:
                return func(*args, **kwargs)
            finally:
                self.release()
        return wrapper
