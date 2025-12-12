import asyncio
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Any, Final

from . import bfile, bfunc, bpath, btime
from .bdefine import END_DATETIME
from .bfunc import crcStr, toAny
from .btype import Null


class BStoreManager:

    def __init__(self, cachePath: Path) -> None:
        self._cachePath = cachePath.absolute()
        self._deadlineFile = self._cachePath / 'deadline.dat'
        self._updating = False
        self._deadline: dict[Path, datetime] = {}
        if self._deadlineFile.exists():
            try:
                self._deadline = asyncio.run(
                    bfile.readPickle(self._deadlineFile)
                )
            except:
                raise Exception('BCacheManager 缓存文件异常', self._deadlineFile)

    async def put(self, key: str, data: Any, duration: timedelta = Null):
        file = self._getFile(key)
        try:
            await bfile.writePickle(file, data)
            await self._updateDeadline(
                file,
                btime.datetime() + duration if duration else END_DATETIME,
            )
            return True
        except:
            bpath.remove(file)
            if file in self._deadline:
                await self._updateDeadline(file, None)
            return False

    async def get(self, key: str):
        file = self._getFile(key)
        if file in self._deadline:
            if btime.datetime() > self._deadline[file]:
                await self._updateDeadline(file, None)
                bpath.remove(file)
                return
            if file.is_file():
                return await bfile.readPickle(file)
            else:
                await self._updateDeadline(file, None)
        else:
            bpath.remove(file)

    async def clear(self, key: str):
        bpath.remove(self._getFile(key))

    def _getFile(self, key: str):
        return self._cachePath / bfunc.crcStr(key)

    async def _updateDeadline(self, file: Path, deadline: datetime | None):
        if deadline:
            self._deadline[file] = deadline
        else:
            del self._deadline[file]
        if not self._updating:
            self._updating = True
            asyncio.create_task(
                self._writeDeadlineFile()
            )

    async def _writeDeadlineFile(self):
        await asyncio.sleep(2)
        self._updating = False
        try:
            await bfile.writePickle(self._deadlineFile, self._deadline)
        except:
            pass

    def cache(self, key: str, duration: timedelta = Null):
        def func(func: bfunc.AsyncFuncType) -> bfunc.AsyncFuncType:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any):
                try:
                    cacheResult = await self.get(key)
                    if cacheResult is not None:
                        return cacheResult
                    else:
                        result = await func(*args, **kwargs)
                        await self.put(key, result, duration)
                        return result
                except:
                    await self.clear(key)
                    raise
            return toAny(wrapper)
        return func


# ------------------------------------------------------------------------------------------


async def get(key: str, default: Any = None):
    storeFile = _getStoreFile(key)
    if storeFile.is_file():
        return await bfile.readPickle(storeFile)
    else:
        return default


async def set(key: str, value: Any):
    storeFile = _getStoreFile(key)
    await bfile.writePickle(storeFile, value)


async def clear(*keys: str):
    bpath.remove(*[_getStoreFile(key) for key in keys])


async def clearAll():
    files = bpath.listFile(_storePath)
    bpath.remove(*files)


_storePath: Final = bpath.workspace('.store')


def _getStoreFile(key: str):
    return bpath.get(_storePath, f'{crcStr(key)}.dat')
