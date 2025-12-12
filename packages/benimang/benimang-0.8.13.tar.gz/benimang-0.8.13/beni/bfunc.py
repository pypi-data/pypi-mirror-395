import asyncio
import binascii
import hashlib
import json
import os
import pickle
import random
import sys
import uuid
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Coroutine

import psutil

from .btype import AnyType, AsyncFuncType, FuncType, IfsType, Params, XPath


def splitLines(value: str) -> list[str]:
    '''
    将字符串按行拆分为数组
    去掉每行首尾空格和空行
    过滤掉空白行
    '''
    lines = value.replace('\r\n', '\n').split('\n')
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]
    return lines


def splitWords(value: str) -> list[str]:
    '''
    将字符串按行和按空格拆分为数组
    去掉每个单词首尾空格和空单词
    过滤掉空白单词
    过滤掉重复单词
    '''
    value = value.replace('\r\n', '\n')
    value = value.replace('\n', ' ')
    words = value.split(' ')
    words = [word.strip() for word in words]
    words = [word for word in words if word]
    words = list(set(words))
    return words


def jsonDumpsMini(value: Any):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def md5Bytes(data: bytes):
    return hashlib.md5(data).hexdigest()


def md5Str(content: str):
    return md5Bytes(
        content.encode()
    )


def md5Data(data: Any):
    return md5Bytes(
        pickle.dumps(data)
    )


def crcBytes(data: bytes):
    return hex(binascii.crc32(data))[2:].zfill(8)


def crcStr(content: str):
    return crcBytes(
        content.encode()
    )


def crcData(data: Any):
    return crcBytes(
        pickle.dumps(data)
    )


def isExe() -> bool:
    return hasattr(sys, '_MEIPASS')


def sysUtf8():
    if isPlatformWindows():
        os.system('chcp 65001')


def addEnvPath(path: XPath):
    value = os.getenv('path') or ''
    value = ';'.join([value, str(path)])
    os.putenv('path', value)


def makeValidateCode(length: int):
    minValue = 10 ** (length - 1)
    maxValue = int('9' * length)
    return str(random.randrange(minValue, maxValue))


def getValueInside(value: IfsType, minValue: IfsType, maxValue: IfsType):
    '包括最小值和最大值'
    value = min(value, maxValue)
    value = max(value, minValue)
    return value


def getPercentValue(targetValue: float, minValue: float, maxValue: float, minResult: float, maxResult: float):
    '根据百分之计算指定数值'
    if targetValue >= maxValue:
        return maxResult
    elif targetValue <= minValue:
        return minResult
    else:
        percent = (targetValue - minValue) / (maxValue - minValue)
        return minResult + (maxResult - minResult) * percent


def getIncrease(fromValue: float, toValue: float):
    return toValue / fromValue - 1


def toFloat(value: IfsType, default: float = 0):
    result = default
    try:
        result = float(value)
    except:
        pass
    return result


def toInt(value: IfsType, default: int = 0):
    result = default
    try:
        result = int(value)
    except:
        pass
    return result


def toAny(value: Any):
    return value


def getSqlPlacement(ary: list[Any] | set[Any], placement: str = '?'):
    return '(' + ','.join([placement for _ in range(len(ary))]) + ')'


def getWrapped(data: Any):
    result = data
    while hasattr(result, '__wrapped__'):
        result = getattr(result, '__wrapped__')
    return result


def retry(times: int):
    def func(func: AsyncFuncType) -> AsyncFuncType:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any):
            current = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except:
                    current += 1
                    if current >= times:
                        raise
        return toAny(wrapper)
    return func


def syncCall(func: Callable[Params, Coroutine[Any, Any, AnyType]]) -> Callable[Params, AnyType]:
    @wraps(func)
    def wraper(*args: Params.args, **kwargs: Params.kwargs):
        return asyncio.run(func(*args, **kwargs))
    return toAny(wraper)


_onceCallSet: set[int] = set()


def onceCall(func: FuncType) -> FuncType:
    @wraps(func)
    def wraper(*args: Any, **kwargs: Any):
        assert id(func) not in _onceCallSet, f'函数 {func.__module__}.{func.__name__} 只能调用一次'
        _onceCallSet.add(id(func))
        return func(*args, **kwargs)
    return toAny(wraper)


def Counter(value: int = 0):
    def _(v: int = 1):
        nonlocal value
        value += v
        return value
    return _


def getMacAddress():
    return uuid.UUID(int=uuid.getnode()).hex[-12:]


@contextmanager
def tryRun():
    try:
        yield
    except:
        pass


def obfuscate(s: bytes) -> bytes:
    n = random.randint(1, min(9, len(s) // 4))
    chunks = [s[i:i + n] for i in range(0, len(s), n)]
    even_chunks = chunks[::2]
    odd_chunks = chunks[1::2]
    if len(chunks) % 2 == 1:
        odd_chunks.append(even_chunks.pop())
    obfuscated = b''.join(even_chunks + odd_chunks)
    mid = len(obfuscated) // 2
    obfuscated = obfuscated[:mid] + str(n).encode() + obfuscated[mid:]
    return obfuscated


def deobfuscate(s: bytes) -> bytes:
    mid = len(s) // 2
    if len(s) % 2 == 0:
        n = int(chr(s[mid - 1]))
        s = s[:mid - 1] + s[mid:]
    else:
        n = int(chr(s[mid]))
        s = s[:mid] + s[mid + 1:]
    chunks = [s[i:i + n] for i in range(0, len(s), n)]
    half = len(chunks) // 2
    even_chunks = chunks[:half]
    odd_chunks = chunks[half:]
    if len(chunks) % 2 == 1:
        even_chunks.append(b'')
    deobfuscated = b''.join(sum(zip(even_chunks, odd_chunks), ())) + b''.join(even_chunks[len(odd_chunks):])
    return deobfuscated


def shuffleSequence(data: AnyType) -> AnyType:
    '打乱序列'
    tempData = toAny(data)
    size = len(tempData)
    n = int(size / 3) - size % 10
    return tempData[:size - n * 2] + tempData[size - n:] + tempData[size - n * 2:size - n]


def isPlatformWindows() -> bool:
    return sys.platform == 'win32'


def isPlatformLinux() -> bool:
    return sys.platform == 'linux'


def isWindowsPowershell() -> bool:
    return isPlatformWindows() and _checkProcess('powershell.exe', 'pwsh.exe')


def isWindowsCmd() -> bool:
    return isPlatformWindows() and _checkProcess('cmd.exe')


def _checkProcess(*targetAry: str):
    process = psutil.Process().parent()
    while process:
        if process.name() in targetAry:
            return True
        process = process.parent()
    return False
