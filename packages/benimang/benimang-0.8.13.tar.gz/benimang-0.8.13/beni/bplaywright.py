from contextlib import asynccontextmanager
from typing import Any

import nest_asyncio
from playwright.async_api import BrowserContext, async_playwright

from . import bpath
from .btype import Null, XPath


@asynccontextmanager
async def page(
    *,
    browser: dict[str, Any] = {},
    context: dict[str, Any] = {},
    page: dict[str, Any] = {},
):
    '''
    ```py
    browser={
        'headless': False,    # 显示浏览器UI
        'channel': 'chrome',  # 使用系统 Chrome 浏览器
    },
    context={
        'storage_state': FILE_STATE,
    },
    ```
    '''
    async with async_playwright() as p:
        async with await p.chromium.launch(**browser) as b:
            async with await b.new_context(**context) as c:
                async with await c.new_page(**page) as p:
                    yield p


@asynccontextmanager
async def context(
    *,
    browser: dict[str, Any] = {},
    context: dict[str, Any] = {},
):
    '''
    ```py
    browser={
        'headless': False,    # 显示浏览器UI
        'channel': 'chrome',  # 使用系统 Chrome 浏览器
    },
    context={
        'storage_state': FILE_STATE,
    },
    ```
    '''
    async with async_playwright() as p:
        async with await p.chromium.launch(**browser) as b:
            async with await b.new_context(**context) as c:
                yield c


@asynccontextmanager
async def browser(
    *,
    browser: dict[str, Any] = {},
):
    '''```py
    browser={
        'headless': False,    # 显示浏览器UI
        'channel': 'chrome',  # 使用系统 Chrome 浏览器
    }
    ```'''
    async with async_playwright() as p:
        async with await p.chromium.launch(**browser) as b:
            yield b


# ------------------------------------------------------------------------------------------------

_testContext: BrowserContext | None = None


async def testPage(*, headless: bool = False, url: str = '', storageState: XPath = Null):
    global _testContext
    if not _testContext:
        nest_asyncio.apply()
        # os.environ['PWDEBUG'] = 'console' # 导致了不能隐藏浏览器
        p = await async_playwright().start()
        browser = await p.chromium.launch(
            headless=headless,  # False 表示显示浏览器
            channel='chrome',
            args=[
                '--disable-blink-features=AutomationControlled',
            ],
        )
        _testContext = await browser.new_context(
            no_viewport=True,
            storage_state=storageState,
        )
    page = await _testContext.new_page()
    if url:
        await page.goto(url)
    return page


async def testStorageState(file: XPath = Null):
    if _testContext:
        file = file or bpath.desktop('storage_state.dat')
        await _testContext.storage_state(path=file)
