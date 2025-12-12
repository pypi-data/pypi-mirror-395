import sys
from typing import IO, Any

from colorama import Fore, Style, init

init()


def printx(*values: Any, sep: str = ' ', end: str = '\n', file: IO[str] = sys.stdout, flush: bool = False, colors: list[Any] | None):
    'color 数组参数 colorama.Fore / colorama.Back / colorama.Style 的常量'
    if colors:
        set(*colors)
    print(*values, sep=sep, end=end, file=file, flush=flush)
    clear()


def getStr(value: Any, *colors: Any):
    if colors:
        value = ''.join(colors) + str(value) + Style.RESET_ALL
    return value


def set(*colors: Any):
    content = ''.join(colors)
    if content:
        sys.stdout.write(content)
        sys.stderr.write(content)


def clear():
    sys.stdout.write(Style.RESET_ALL)
    sys.stderr.write(Style.RESET_ALL)


def red(msg: str):
    return getStr(msg, Fore.LIGHTRED_EX)


def yellow(msg: str):
    return getStr(msg, Fore.YELLOW)


def green(msg: str):
    return getStr(msg, Fore.LIGHTGREEN_EX)


def cyan(msg: str):
    '蓝色'
    return getStr(msg, Fore.LIGHTCYAN_EX)


def magenta(msg: str):
    '紫色'
    return getStr(msg, Fore.LIGHTMAGENTA_EX)


def white(msg: str):
    return getStr(msg, Fore.LIGHTWHITE_EX)


def printRed(*values: Any):
    print(red(' '.join([str(x) for x in values])))


def printYellow(*values: Any):
    print(yellow(' '.join([str(x) for x in values])))


def printGreen(*values: Any):
    print(green(' '.join([str(x) for x in values])))


def printCyan(*values: Any):
    '蓝色'
    print(cyan(' '.join([str(x) for x in values])))


def printMagenta(*values: Any):
    '紫色'
    print(magenta(' '.join([str(x) for x in values])))


def printWhite(*values: Any):
    print(white(' '.join([str(x) for x in values])))
