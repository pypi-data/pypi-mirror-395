import asyncio
import os
import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import aiofiles

from .btype import XPath


def get(path: XPath, *expand: Any):
    if type(path) is not Path:
        path = Path(path)
    if expand:
        return path.joinpath(
            '/'.join([str(x) for x in expand])
        ).resolve()
    else:
        return path.resolve()


def user(*expand: Any):
    return get(Path('~').expanduser(), *expand)


def desktop(*expand: Any):
    return user('Desktop', *expand)


def workspace(*expand: Any):
    return get('/.beni-workspace', *expand)


def tempFile():
    return workspace(f'temp/{uuid.uuid4()}.tmp')


def tempPath():
    return workspace(f'temp/{uuid.uuid4()}')


def changeRelative(target: XPath, fromRelative: XPath, toRelative: XPath):
    target = get(target)
    fromRelative = get(fromRelative)
    toRelative = get(toRelative)
    assert target.is_relative_to(fromRelative)
    return toRelative.joinpath(target.relative_to(fromRelative))


def openPath(path: XPath):
    os.system(f'start explorer {path}')


def remove(*paths: XPath):
    for path in paths:
        path = get(path)
        if path.is_file():
            path.unlink(True)
        elif path.is_dir():
            shutil.rmtree(path)


def make(*paths: XPath):
    for path in paths:
        path = get(path)
        path.mkdir(parents=True, exist_ok=True)


def clearDir(*dirList: XPath):
    for dir in dirList:
        remove(*[x for x in get(dir).iterdir()])


def copy(src: XPath, dst: XPath):
    src = get(src)
    dst = get(dst)
    make(dst.parent)
    if src.is_file():
        shutil.copyfile(src, dst)
    elif src.is_dir():
        shutil.copytree(src, dst)
    else:
        if not src.exists():
            raise Exception(f'copy error: src not exists {src}')
        else:
            raise Exception(f'copy error: src not support {src}')


def copyMany(dataDict: dict[XPath, XPath]):
    for src, dst in dataDict.items():
        copy(src, dst)


def copyOverwrite(src: XPath, dst: XPath):
    '强制覆盖（判断文件和目录类型，如果源位置和目标位置类型不同则失败）'
    for item in listFile(src, True):
        copy(item, changeRelative(item, src, dst))
    for item in listDir(src, True):
        dstDir = changeRelative(item, src, dst)
        if not dstDir.exists():
            make(dstDir)
        elif not dstDir.is_dir():
            raise Exception(f'copyOverwrite error: dst is not dir {dstDir}')


def move(src: XPath, dst: XPath, force: bool = False):
    src = get(src)
    dst = get(dst)
    if dst.exists():
        if force:
            remove(dst)
        else:
            raise Exception(f'move error: dst exists {dst}')
    make(dst.parent)
    os.rename(src, dst)


def moveMany(dataDict: dict[XPath, XPath], force: bool = False):
    for src, dst in dataDict.items():
        move(src, dst, force)


def renameName(src: XPath, name: str):
    src = get(src)
    src.rename(src.with_name(name))


def renameStem(src: XPath, stemName: str):
    src = get(src)
    src.rename(src.with_stem(stemName))


def renameSuffix(src: XPath, suffixName: str):
    src = get(src)
    src.rename(src.with_suffix(suffixName))


def listPath(path: XPath, recursive: bool = False):
    '获取指定路径下文件以及目录列表'
    path = get(path)
    if recursive:
        return list(path.glob('**/*'))
    else:
        return list(path.glob("*"))


def listFile(path: XPath, recursive: bool = False):
    '获取指定路径下文件列表'
    path = get(path)
    if recursive:
        return list(filter(lambda x: x.is_file(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_file(), path.glob('*')))


def listDir(path: XPath, recursive: bool = False):
    '获取指定路径下目录列表'
    path = get(path)
    if recursive:
        return list(filter(lambda x: x.is_dir(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_dir(), path.glob('*')))


@contextmanager
def useTempFile():
    file = tempFile()
    try:
        yield file
    finally:
        remove(file)


@contextmanager
def useTempPath(isMakePath: bool = False):
    path = tempPath()
    if isMakePath:
        make(path)
    try:
        yield path
    finally:
        remove(path)


@contextmanager
def changePath(path: XPath):
    path = Path(path)
    currentPath = os.getcwd()
    try:
        os.chdir(str(path))
        yield
    finally:
        os.chdir(currentPath)


async def removeSecure(*paths: XPath, passes: int = 7):
    fileList: list[Path] = []
    for path in paths:
        fileList.extend(listFile(path, True))
    fileList = list(set([x.absolute() for x in fileList]))
    await asyncio.gather(
        *[_removeFileSecure(x, passes) for x in fileList]
    )
    for path in paths:
        remove(path)


async def _removeFileSecure(file: Path, passes: int):
    # 获取文件大小
    file_size = file.stat().st_size

    # 多次覆写模式（符合DoD标准）
    patterns = [
        b'\x55' * 1024,  # 模式 0x55
        b'\xAA' * 1024,  # 模式 0xAA
        os.urandom(1024),  # 随机数据
        b'\x00' * 1024,  # 全零
        b'\xFF' * 1024,  # 全一
    ]

    async with aiofiles.open(file, 'rb+') as f:
        # 多次覆写
        for i in range(passes):
            # 选择覆写模式
            if i < len(patterns):
                pattern = patterns[i]
            else:
                pattern = os.urandom(1024)  # 后续用随机数据

            # 定位到文件开始
            await f.seek(0)

            # 分块写入防止内存溢出
            written = 0
            while written < file_size:
                block_size = min(1024, file_size - written)
                await f.write(pattern[:block_size])
                written += block_size

            # 强制写入磁盘
            await f.flush()
            os.fsync(f.fileno())

        # 最后用全零覆写文件元数据
        await f.truncate(0)
