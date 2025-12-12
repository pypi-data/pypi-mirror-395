import asyncio
from contextlib import asynccontextmanager
from typing import Any, Coroutine, Sequence

from tqdm import tqdm

from . import block
from .btype import AnyType


@asynccontextmanager
async def show(total: int):
    # 示例
    # async with bprogress.show(100) as update:
    #     while True:
    #         await asyncio.sleep(1)
    #         update()
    print()
    with tqdm(total=total, ncols=70) as progress:
        yield progress.update
    print()


async def run(
    taskList: Sequence[Coroutine[Any, Any, AnyType]],
    itemLimit: int = 999999,
) -> Sequence[AnyType]:
    # 示例
    # await bprogress.run(
    #     [myfun() for _ in range(100)],
    #     10,
    # )
    print()
    with tqdm(total=len(taskList), ncols=70) as progress:
        @block.limit(itemLimit)
        async def task(x: Coroutine[Any, Any, AnyType]):
            result = await x
            progress.update()
            return result
        resultList = await asyncio.gather(*[task(x) for x in taskList])
    print()
    return resultList
