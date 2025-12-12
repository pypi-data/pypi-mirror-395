import asyncio
from typing import Any

from . import bbyte, bpath
from .btype import XPath


async def winscp(winscp_exe: XPath, key_file: str, server: str, cmd_list: list[str], show_cmd: bool = True):
    logFile = bpath.user('executeWinScp.log')
    bpath.remove(logFile)
    ary = [
        'option batch abort',
        'option transfer binary',
        f'open sftp://{server} -privatekey={key_file} -hostkey=*',
    ]
    ary += cmd_list
    ary += [
        'close',
        'exit',
    ]
    # /console
    cmd = f'{winscp_exe} /log={logFile} /loglevel=0 /command ' + ' '.join("%s" % x for x in ary)
    if show_cmd:
        print(cmd)
    return await run(cmd)


async def runExpect(*args: Any, output: str = '', error: str = ''):
    outputBytes, errorBytes, _ = await runQuiet(*args)
    if output and output not in bbyte.decode(outputBytes):
        raise Exception(f'命令执行失败: {" ".join([str(x) for x in args])}')
    if error and error not in bbyte.decode(errorBytes):
        raise Exception(f'命令执行失败: {" ".join([str(x) for x in args])}')


async def runQuiet(*args: Any):
    proc = await asyncio.create_subprocess_shell(
        ' '.join([str(x) for x in args]),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    return await proc.communicate() + (proc.returncode or 0,)


async def run(*args: Any):
    proc = await asyncio.create_subprocess_shell(
        ' '.join([str(x) for x in args]),
    )
    await proc.communicate()
    return proc.returncode or 0
