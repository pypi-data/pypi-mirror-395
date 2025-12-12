import inspect
import re
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime as Datetime
from pathlib import Path
from types import FrameType
from typing import Any, Final, cast

import nest_asyncio
from colorama import Fore
from typer import Typer
from typer.testing import CliRunner

from beni.btype import Null

from . import bcolor, bfunc, block, blog, bpath, btime
from .btype import Null

app = Typer()

nest_asyncio.apply()


@dataclass
class _Options:
    lock: int = 60001
    logPath: Path = Null
    binPath: Path = Null
    logFilesLimit: int = 100


options: Final = _Options()
isShowSummary: bool = False

_subApps: list[Typer] = []


def newSubApp(help: str, *, subAppName: str = ''):
    frame = (cast(FrameType, inspect.currentframe())).f_back
    assert frame
    fileName = Path(inspect.getframeinfo(frame).filename).stem
    subAppName = subAppName or re.sub(r'(?<!^)(?=[A-Z])', '-', fileName).lower()
    subApp = Typer(name=subAppName, help=help)
    _subApps.append(subApp)
    return subApp


async def main():
    async with _task():
        try:
            for subApp in _subApps:
                app.add_typer(subApp)
            app()
        except BaseException as ex:
            if type(ex) is SystemExit and ex.code in (0, 1, 2):
                # 0 - 正常结束
                # 1 - 手动中断（Ctrl+C）
                # 2 - Error: Missing command.
                pass
            else:
                raise


@asynccontextmanager
async def _task():
    # bfunc.sysUtf8() # 由于不是每次都需要用到，界面显示了不美观 Active code page: 65001
    if options.binPath:
        bfunc.addEnvPath(options.binPath)
    start_time = Datetime.now()
    if options.logPath:
        logFile = bpath.get(options.logPath, btime.datetimeStr('%Y%m%d_%H%M%S.log'))
        assert logFile.is_file(), f'日志文件创建失败（已存在） {logFile}'
    else:
        logFile = None
    try:
        blog.init(logFile=logFile)
        if options.lock:
            with block.portLock(options.lock):
                yield
        else:
            yield
    except _AbortException as ex:
        bcolor.printRed(ex.msg)
    except BaseException as ex:
        bcolor.set(Fore.LIGHTRED_EX)
        blog.error(str(ex))
        blog.error('执行失败')
        raise
    finally:
        if isShowSummary:
            criticalNum = blog.getCountCritical()
            errorNum = blog.getCountError()
            warningNum = blog.getCountWarning()
            if criticalNum:
                color = Fore.LIGHTMAGENTA_EX
            elif errorNum:
                color = Fore.LIGHTRED_EX
            elif warningNum:
                color = Fore.YELLOW
            else:
                color = Fore.LIGHTGREEN_EX
            msgAry = ['', '-' * 75]
            if criticalNum:
                msgAry.append(f'critical：{criticalNum}')
            if errorNum:
                msgAry.append(f'error：{errorNum}')
            if warningNum:
                msgAry.append(f'warning：{warningNum}')
            duration = str(Datetime.now() - start_time)
            if duration.startswith('0:'):
                duration = '0' + duration
            msgAry.append(f'任务结束（{duration}）')
            bcolor.set(color)
            blog.info('\n'.join(msgAry))

        # 删除多余的日志
        try:
            if logFile:
                logFileAry = list(logFile.parent.glob('*.log'))
                logFileAry.remove(logFile)
                logFileAry.sort()
                logFileAry = logFileAry[options.logFilesLimit:]
                bpath.remove(*logFileAry)
        except:
            pass


def abort(*errorMsgs: Any):
    msg = '\n'.join([str(x) for x in errorMsgs])
    if not msg:
        raise Exception('程序中断，未提供错误信息')
    raise _AbortException(msg)


def assertTrue(condition: Any, *errorMsgs: Any):
    if not condition:
        abort(*errorMsgs)


class _AbortException(BaseException):
    def __init__(self, msg: str):
        super().__init__()
        self.msg = msg


_runner: CliRunner = Null


def testCall(*args: Any):
    global _runner
    if not _runner:
        for subApp in _subApps:
            app.add_typer(subApp)
        _runner = CliRunner()
    return _runner.invoke(app, args)
