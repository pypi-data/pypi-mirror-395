import datetime as xdatetime
import time as xtime

from httpx import AsyncClient

from .btype import Ifs, Null

_serverTime: float = xtime.time()
_initTime: float = xtime.monotonic()
_defaultTimeOffset: xdatetime.timedelta = xdatetime.timedelta(hours=8)


async def networkTime(timeOffset: xdatetime.timedelta = _defaultTimeOffset):
    async with AsyncClient() as client:
        response = await client.get('https://www.baidu.com')
        date_str = response.headers['Date']
        return xdatetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT') + timeOffset


async def initServerDatetime(timeOffset: xdatetime.timedelta = _defaultTimeOffset):
    global _serverTime, _initTime
    _serverTime = (await networkTime(timeOffset)).timestamp()
    _initTime = xtime.monotonic()


def timestamp():
    return _serverTime + xtime.monotonic() - _initTime


def timestampSecond():
    return int(timestamp())


def timestampMillisecond():
    return int(timestamp() * 1000)


def datetime(t: Ifs = Null):
    t = float(t) if t else timestamp()
    return xdatetime.datetime.fromtimestamp(t)


def date(t: Ifs = Null):
    t = float(t) if t else timestamp()
    return xdatetime.date.fromtimestamp(t)


def time(t: Ifs = Null):
    return datetime(t).time()


def datetimeStr(t: Ifs = Null, fmt: str = r'%Y-%m-%d %H:%M:%S'):
    return datetime(t).strftime(fmt)


def dateStr(t: Ifs = Null, fmt: str = r'%Y-%m-%d'):
    return date(t).strftime(fmt)


def timeStr(t: Ifs = Null, fmt: str = r'%H:%M:%S'):
    return time(t).strftime(fmt)


def makeDatetime(date_str: str, fmt: str = r'%Y-%m-%d %H:%M:%S'):
    return xdatetime.datetime.strptime(date_str, fmt)


def makeDate(date_str: str, fmt: str = r'%Y-%m-%d'):
    return xdatetime.datetime.strptime(date_str, fmt).date()
