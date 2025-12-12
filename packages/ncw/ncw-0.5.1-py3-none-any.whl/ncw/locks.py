# -*- coding: utf-8 -*-

"""
locks module
"""

from collections.abc import Callable
from threading import Condition, RLock
from time import monotonic as _time


_ZERO = 0
_EXCLUSIVE_LOCK = -1
_UNLOCKED = 0


class LockManager:
    """Context manager for BoltTypeLock classes"""

    def __init__(self, btl: "BoltTypeLock", shared: bool = True) -> None:
        """Register the acquire and release methods"""
        if shared:
            self.__acquire: Callable = btl.acquire_shared
            self.__release: Callable = btl.release_shared
        else:
            self.__acquire = btl.acquire_exclusive
            self.__release = btl.release_exclusive
        #

    def __enter__(self) -> bool:
        """acquire the lock"""
        return self.__acquire()

    def __exit__(self, t, v, tb):
        """release the lock"""
        self.__release()


class BoltTypeLock:
    """This class implements a bolt-type lock for exclusive or shared access,
    heavily borrowing from the threading.Semaphore class.

    BoltTypeLock instances maintain an internal value representing
    one of the following states:

        0  → the resource is available
        1  → the resource is exclusively locked
        2+ → the resource is in shared lock

    acquiring an exclusive lock: 0 → -1 only
    releasing an exclusive lock: -1 → 0
    acquiring a shared lock: increase the value if it is 0 or more
    releasing a shared lock: decrease the value if it is 1 or greater

    """

    def __init__(self) -> None:
        """Initialize the value"""
        self._cond = Condition(RLock())
        self.__state: int = _UNLOCKED
        self.shared = LockManager(self, shared=True)
        self.exclusive = LockManager(self, shared=False)

    @property
    def state(self) -> int:
        """observable state"""
        return self.__state

    def __repr__(self) -> str:
        """String rpresentation"""
        cls = self.__class__
        return (
            f"<{cls.__module__}.{cls.__qualname__} at {id(self):#x}:"
            f" state={self.__state}>"
        )

    def acquire_exclusive(self, timeout: float = _ZERO) -> bool:
        """Acquire an exclusive lock

        When invoked with a timeout other than 0, it will block for at
        most timeout seconds.  If acquire_exclusove does not complete successfully
        in that interval, return false.  Return true otherwise.

        """
        rc = False
        endtime: float = _ZERO
        with self._cond:
            while self.__state != _UNLOCKED:
                if timeout is _ZERO:
                    self._cond.wait(None)
                else:
                    if endtime is _ZERO:
                        endtime = _time() + timeout
                    elif _time() > endtime:
                        break
                    #
                    self._cond.wait(timeout)
                #
                # re-notify on continued wait
                self._cond.notify(1)
            else:
                self.__state = _EXCLUSIVE_LOCK
                rc = True
            #
        #
        return rc

    def acquire_shared(self, timeout: float = _ZERO):
        """Acquire a shared lock

        When invoked with a timeout other than 0, it will block for at
        most timeout seconds.  If acquire_shared does not complete successfully
        in that interval, return false.  Return true otherwise.

        """
        rc = False
        endtime: float = _ZERO
        with self._cond:
            while self.__state < 0:
                if timeout is _ZERO:
                    self._cond.wait(None)
                else:
                    if endtime is _ZERO:
                        endtime = _time() + timeout
                    elif _time() > endtime:
                        break
                    #
                    self._cond.wait(timeout)
                #
                # re-notify on continued wait
                self._cond.notify(1)
            else:
                self.__state += 1
                rc = True
            #
        #
        return rc

    def release_exclusive(self):
        """Release an exclusive lock"""
        with self._cond:
            if self.__state == _EXCLUSIVE_LOCK:
                self.__state = _UNLOCKED
            else:
                raise ValueError(f"Not releasable (state {self.__state})")
            #
            self._cond.notify(1)
        #

    def release_shared(self):
        """Release a shared lock"""
        with self._cond:
            if self.__state > 0:
                self.__state -= 1
            else:
                raise ValueError(f"Not releasable (state {self.__state})")
            #
            self._cond.notify(1)
        #


# pylint: disable=too-few-public-methods ; minimal dummy classes


class DummyLockManager:
    """Context manager for DummyLock classes"""

    def __enter__(self) -> bool:
        """Do nothing except returning True"""
        return True

    def __exit__(self, t, v, tb):
        """Do nothing"""


class DummyLock:
    """Dummy lock with shared and exclusive context managers
    as a drop-in replacement for BoltTypeLock in immutable
    wrappers.BaseStructure subclasses that do not require locking
    """

    def __init__(self) -> None:
        """Initialize the value"""
        self.shared = DummyLockManager()
        self.exclusive = DummyLockManager()


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
