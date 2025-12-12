import json
import os
import pickle
import tomllib
from pathlib import Path
from typing import Any

import aiofiles
import orjson

from . import bcolor, bfile, bfunc, bpath
from .btype import Null, XPath


async def writeText(file: XPath, content: str, encoding: str = 'utf8', newline: str = '\n'):
    file = bpath.get(file)
    bpath.make(file.parent)
    async with aiofiles.open(file, 'w', encoding=encoding, newline=newline) as f:
        return await f.write(content)


async def writeBytes(file: XPath, data: bytes):
    file = bpath.get(file)
    bpath.make(file.parent)
    async with aiofiles.open(file, 'wb') as f:
        return await f.write(data)


async def writeJson(file: XPath, data: Any, mini: bool = True):
    if mini:
        content = bfunc.jsonDumpsMini(data)
    else:
        content = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)
    await writeText(file, content)


async def writePickle(file: XPath, data: Any):
    await writeBytes(file, pickle.dumps(data))


async def readText(file: XPath, encoding: str = 'utf8'):
    data = await readBytes(file)
    # 针对 UTF8 判断移除 BOM 头
    if encoding == 'utf8':
        if data.startswith(b'\xef\xbb\xbf'):
            data = data[3:]
    return data.decode(encoding)


async def readBytes(file: XPath):
    async with aiofiles.open(file, 'rb') as f:
        return await f.read()


async def readJson(file: XPath):
    return orjson.loads(await readBytes(file))


async def readPickle(file: XPath):
    return pickle.loads(
        await readBytes(file)
    )


async def readToml(file: XPath):
    return tomllib.loads(
        await readText(file)
    )


async def md5(file: XPath):
    return bfunc.md5Bytes(
        await readBytes(file)
    )


async def crc(file: XPath):
    return bfunc.crcBytes(
        await readBytes(file)
    )


async def makeFiles(content: str, output: Path = Null, key: str = '>>>'):
    if output is Null:
        output = Path(os.curdir).absolute()
    ary = content.split(key)
    ary = [x.strip() for x in ary]
    ary = [x for x in ary if x]
    ary.sort()
    for substr in ary:
        subAry = substr.replace('\r\n', '\n').split('\n')
        fileName = subAry.pop(0)
        file = output / fileName
        bcolor.printYellow(file)
        await bfile.writeText(
            file,
            '\n'.join(subAry).strip(),
        )


async def toLf(file: XPath):
    content = await readText(file)
    await writeText(file, content.replace('\r\n', '\n'))
