import asyncio
import locale
from typing import Any


async def run(*cmd: Any, isPrint: bool = True, encoding: str = '') -> tuple[str, int]:
    encoding = encoding or locale.getpreferredencoding()
    process = await asyncio.create_subprocess_shell(
        ' '.join([str(x) for x in cmd]),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    assert process.stdout and process.stderr, '初始化进程失败'

    resultList: list[str] = []
    taskList = [
        asyncio.create_task(
            _handleStream(process.stdout, isPrint, encoding, resultList)
        ),
        asyncio.create_task(
            _handleStream(process.stderr, isPrint, encoding, resultList)
        ),
    ]

    await process.wait()
    for task in taskList:
        task.cancel()

    return '\n'.join(resultList), process.returncode or 0


# ------------------------------------------------------------------------------------


async def _handleStream(stream: asyncio.StreamReader, isPrint: bool, encoding: str, resultList: list[str]) -> None:
    while True:
        line = await stream.readline()
        if line:
            msg = line.decode(encoding).replace('\r\n', '\n')
            if msg.endswith('\n'):
                msg = msg[:-1]
            resultList.append(msg)
            if isPrint:
                print(msg)
        else:
            break
