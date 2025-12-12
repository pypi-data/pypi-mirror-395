from typing import Any

import aiofiles
import aiohttp
import orjson
from httpx import AsyncClient

from beni.bdefine import MB

from . import bpath
from .btype import Null, XPath


async def getBytes(
    url: str,
    *,
    headers: dict[str, Any] = Null,
    timeout: int = 10,
):
    async with AsyncClient() as client:
        client.headers.update(headers)
        client.timeout = timeout
        response = await client.get(url)
        return response.content


async def getStr(
    url: str,
    *,
    encoding: str = 'UTF8',
    headers: dict[str, Any] = Null,
    timeout: int = 10,
):
    data = await getBytes(url, headers=headers, timeout=timeout)
    return data.decode(encoding)


async def getJson(
    url: str,
    *,
    headers: dict[str, Any] = Null,
    timeout: int = 10,
):
    data = await getBytes(url, headers=headers, timeout=timeout)
    return orjson.loads(data)


async def postBytes(
    url: str,
    *,
    data: bytes | dict[str, Any] = Null,
    headers: dict[str, Any] = Null,
    timeout: int = 10,
):
    async with AsyncClient() as client:
        client.headers.update(headers)
        client.timeout = timeout
        response = await client.post(url, json=data)
        return response.content


async def postStr(
    url: str,
    *,
    encoding: str = 'UTF8',
    data: bytes | dict[str, Any] = Null,
    headers: dict[str, Any] = Null,
    timeout: int = 10,
):
    data = await postBytes(url, data=data, headers=headers, timeout=timeout)
    return data.decode(encoding)


async def postJson(
    url: str,
    *,
    data: bytes | dict[str, Any] = Null,
    headers: dict[str, Any] = Null,
    timeout: int = 10,
):
    data = await postBytes(url, data=data, headers=headers, timeout=timeout)
    return orjson.loads(data)


async def download(url: str, file: XPath, timeout: int = 300, headers: dict[str, Any] = Null,):
    try:
        file = bpath.get(file)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                bpath.make(file.parent)
                sizeLoaded = 0
                async with aiofiles.open(file, 'wb') as f:
                    while True:
                        data = await response.content.read(1 * MB)
                        if data:
                            await f.write(data)
                            sizeLoaded += len(data)
                        else:
                            if 'Content-Encoding' not in response.headers:
                                assert response.content_length, '下载内容为空'
                                assert response.content_length == sizeLoaded, '下载为文件不完整'
                            break
    except:
        bpath.remove(file)
        raise
