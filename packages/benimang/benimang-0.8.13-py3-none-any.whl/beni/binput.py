import getpass
import random
import re
import string
from typing import Any, Callable, Coroutine, cast

import aioconsole

from . import bcolor


async def hold(msg: str | None = None, isShowInput: bool = True, *exits: str):
    msg = msg or '测试暂停，输入exit可以退出'
    msg = f'{msg}: '
    exits = tuple([x.lower() for x in exits]) or ('exit', )
    while True:
        if isShowInput:
            result = cast(str, await aioconsole.ainput(msg))
        else:
            result = getpass.getpass(msg)
        result = result.lower()
        if (result in exits) or ('*' in exits):
            return result


async def holdLambda(msg: str, isShowInput: bool, isPass: Callable[[str], bool]):
    msg = f'{msg}: '
    while True:
        if isShowInput:
            result = cast(str, await aioconsole.ainput(msg))
        else:
            result = getpass.getpass(msg)
        if isPass(result):
            return result


async def confirm(msg: str = '确认', isShowInput: bool = False):
    codeAry = random.sample(string.ascii_uppercase, 3)
    codeMsg = ' '.join(codeAry)
    code = ''.join(codeAry)
    await holdLambda(f'{msg} [ {_getRemindMsg(codeMsg)} ]', not isShowInput, lambda x: re.sub(r'\s+', '', x).upper() == code)


async def select(*data: tuple[str, str, str | Callable[[str], Any] | None, Callable[[str], Coroutine[Any, Any, Any]] | None]):
    '''
    value = binput.select(
        ('descA', 'confirmDescA', 'quanbuqueren', __handlerA),
        ('descB', 'confirmDescB', lambda x: ..., __handlerB),
    )
    '''
    print()
    print('-' * 30)
    print()
    for msg, inputDisplay, _, _ in data:
        if inputDisplay:
            msg += f' [ {_getRemindMsg(inputDisplay)} ]'
        print(msg)
    print()
    while True:
        value = cast(str, await aioconsole.ainput('输入选择：'))
        isMatch = False
        result = None
        for msg, inputDisplay, inputValue, handler in data:
            inputValue = inputValue or inputDisplay or msg
            if type(inputValue) is str:
                isMatch = value == inputValue
            else:
                try:
                    isMatch = cast(Callable[[str], bool], inputValue)(value)
                except:
                    pass
            if isMatch:
                if handler:
                    result = await handler(value)
                    break
        if isMatch and result is not False:
            return value


async def inputCheck(msg: str, check: Callable[[str], Any]):
    while True:
        try:
            value = cast(str, await aioconsole.ainput(f'{msg}：'))
            if check(value):
                return value
        except:
            pass


def genPassword():
    print('正在创建密码')
    password = ''
    while not password:
        password = getpass.getpass('输入密码：')
    while password != getpass.getpass('再次密码：'):
        pass
    return password


def _getRemindMsg(msg: str):
    return bcolor.yellow(msg)
