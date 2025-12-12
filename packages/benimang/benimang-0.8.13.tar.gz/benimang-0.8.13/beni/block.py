from __future__ import annotations

import asyncio
import inspect
import socket
import sys
from contextlib import asynccontextmanager, contextmanager
from functools import wraps
from typing import Any

import async_timeout

from .bfunc import toAny
from .btype import AsyncFuncType, Func

# ------------------------------------------------------------------------------------------------------------------------
# 根据端口限制多开


@contextmanager
def portLock(port: int, errMsg: str = '程序禁止多开'):
    '占用端口方式实现多开限制 port=0 表示不限制'
    if port == 0:
        yield
    else:
        assert 60000 <= port <= 65535, '端口范围为 60000 ~ 65535'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', port))
            sock.listen(1)
        except:
            raise Exception(errMsg)
        try:
            yield
        finally:
            sock.close()


# ------------------------------------------------------------------------------------------------------------------------
# 限制并执行数量

def limit(value: int = 1):
    def wraperfun(func: AsyncFuncType) -> AsyncFuncType:
        @wraps(func)
        async def wraper(*args: Any, **kwargs: Any):
            funid = id(inspect.unwrap(func))
            if funid not in _limitDict:
                _limitDict[funid] = _Limit(value)
            try:
                await _limitDict[funid].wait()
                return await func(*args, **kwargs)
            finally:
                await _limitDict[funid].release()
        return toAny(wraper)
    return wraperfun


async def setLimit(func: Func, limit: int):
    funid = id(inspect.unwrap(func))
    if funid not in _limitDict:
        _limitDict[funid] = _Limit(limit)
    await _limitDict[funid].set_limit(limit)


_limitDict: dict[int, _Limit] = {}


class _Limit():

    _queue: asyncio.Queue[Any]
    _running: int

    def __init__(self, limit: int):
        self._limit = limit
        self._queue = asyncio.Queue()
        self._running = 0
        while self._queue.qsize() < self._limit:
            self._queue.put_nowait(True)

    async def wait(self):
        await self._queue.get()
        self._running += 1

    async def release(self):
        if self._queue.qsize() < self._limit:
            await self._queue.put(True)
        self._running -= 1

    async def set_limit(self, limit: int):
        self._limit = limit
        while self._running + self._queue.qsize() < self._limit:
            await self._queue.put(True)
        while self._running + self._queue.qsize() > self._limit:
            if self._queue.empty():
                break
            await self._queue.get()


# ------------------------------------------------------------------------------------------------------------------------
# 超时锁


class TimeoutLock:
    def __init__(self, timeout: float | None = None) -> None:
        self._lock: asyncio.Lock = asyncio.Lock()
        self._timeout: float = sys.float_info.max if timeout is None else timeout

    async def acquire(self) -> None:
        async with async_timeout.timeout(self._timeout):
            await self._lock.acquire()

    def release(self) -> None:
        self._lock.release()

    def locked(self) -> bool:
        return self._lock.locked()

    async def __aenter__(self) -> None:
        await self.acquire()

    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.release()


# ------------------------------------------------------------------------------------------------------------------------
# 读写锁


class RWLock:
    def __init__(self, timeout: float | None = None) -> None:
        timeout = sys.float_info.max if timeout is None else timeout
        self._lock: TimeoutLock = TimeoutLock(timeout)
        self._readNum: int = 0

    async def acquireRead(self) -> None:
        if self._readNum:
            self._readNum += 1
        else:
            await self._lock.acquire()
            self._readNum += 1

    async def releaseRead(self) -> None:
        self._readNum -= 1
        if self._readNum == 0:
            self._lock.release()

    async def acquireWrite(self) -> None:
        await self._lock.acquire()

    async def releaseWrite(self) -> None:
        self._lock.release()

    @asynccontextmanager
    async def useRead(self):
        await self.acquireRead()
        try:
            yield
        finally:
            await self.releaseRead()

    @asynccontextmanager
    async def useWrite(self):
        await self.acquireWrite()
        try:
            yield
        finally:
            await self.releaseWrite()
