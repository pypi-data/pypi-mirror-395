from __future__ import annotations

import logging
import re
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Sequence, Type, TypeVar, cast

import aiomysql
import aiosqlite
from pydantic import BaseModel

from beni import bpath
from beni.btype import XPath

from .bfunc import getSqlPlacement, toAny
from .btype import Null


class BModel(BaseModel):

    _tableName: str = ''

    @classmethod
    def tableName(cls):
        if type(cls._tableName) is not str:
            className = cls.__name__
            result = [className[0].lower()]
            for char in className[1:]:
                if char.isupper():
                    result.extend(['_', char.lower()])
                else:
                    result.append(char)
            cls._tableName = ''.join(result)
        return cls._tableName


_BModel = TypeVar('_BModel', bound=BModel)
_T = TypeVar('_T')


class ConditionMaker:

    _statement = ''

    def __init__(self):
        self._ary: list[str] = []
        self._args: list[Any] = []

    def add(self, sql: str, *args: Any):
        self._ary.append(sql)
        self._args.extend(args)

    @property
    def args(self) -> list[Any]:
        return self._args

    def __str__(self) -> str:
        if self._ary:
            return f'{self._statement} ' + ' AND '.join([f'({x})' for x in self._ary])
        else:
            return ''


class WhereMaker(ConditionMaker):
    _statement = 'WHERE'


class HavingMaker(ConditionMaker):
    _statement = 'HAVING'


class OnMaker(ConditionMaker):
    _statement = 'ON'


# ============================================================

AioCursor = aiomysql.Cursor | aiosqlite.Cursor
AioConnection = aiomysql.Connection | aiosqlite.Connection


class DbCursor:

    def __init__(self, cursor: AioCursor):
        self.cursor = cursor

    @property
    def connection(self) -> AioConnection:
        return toAny(self.cursor.connection)

    @property
    def lastrowid(self):
        return self.cursor.lastrowid

    @property
    def rowcount(self):
        return self.cursor.rowcount

    _sqlFormatRe = re.compile(r'\s*\n\s*')

    def sqlFormat(self, sql: str) -> str:
        return self._sqlFormatRe.sub(' ', sql).strip()

    async def commit(self):
        await self.connection.commit()

    async def rollback(self):
        await self.connection.rollback()

    async def execute(self, sql: str, *args: Any):
        sql = self.sqlFormat(sql)
        return await self.cursor.execute(sql, args)

    async def getTupleOne(self, sql: str, *args: Any) -> tuple[Any, ...] | None:
        '获取单行数据，以 tuple 形式返回'
        await self.execute(sql, *args)
        result = cast(tuple[Any], await self.cursor.fetchone())
        return result or None

    async def getDictOne(self, sql: str, *args: Any) -> dict[str, Any] | None:
        '获取单行数据，以 dict 形式返回'
        result = await self.getTupleOne(sql, *args)
        if result:
            columns = self._getColumns()
            result = {v: result[i] for i, v in enumerate(columns)}
            return result
        return None

    async def getOne(self, modelClass: Type[_BModel], sql: str, *args: Any) -> _BModel | None:
        '获取单行数据，以 modelClass 实例返回'
        data = await self.getDictOne(sql, *args)
        if data:
            return modelClass(**data)
        return None

    async def getTupleList(self, sql: str, *args: Any) -> list[tuple[Any, ...]]:
        '获取多行数据，以 tuple 形式返回'
        await self.execute(sql, *args)
        result = cast(list[tuple[Any]], await self.cursor.fetchall())
        return result or []

    async def getDictList(self, sql: str, *args: Any) -> list[dict[str, Any]]:
        '获取多行数据，以 dict 形式返回'
        result = await self.getTupleList(sql, *args)
        if result:
            columns = self._getColumns()
            return [{v: row[i] for i, v in enumerate(columns)} for row in result]
        return []

    async def getList(self, modelClass: Type[_BModel], sql: str, *args: Any) -> list[_BModel]:
        '获取多行数据，以 modelClass 实例返回'
        result = await self.getDictList(sql, *args)
        return [modelClass(**x) for x in result]

    async def getValue(self, valueClass: Type[_T], sql: str, *args: Any) -> _T | None:
        '获取单个值'
        await self.execute(sql, *args)
        result: Sequence[Any] = toAny(await self.cursor.fetchone())
        return result[0] if result else None

    async def getValueList(self, valueClass: Type[_T], sql: str, *args: Any) -> list[_T] | None:
        '获取多个值'
        await self.execute(sql, *args)
        result: Sequence[Sequence[Any]] = toAny(await self.cursor.fetchall())
        return [x[0] for x in result] if result else []

    async def addOne(self, model: BModel, *, tableName: str = '') -> Any:
        columns: list[str] = []
        values: list[Any] = []
        for k, v in model.model_dump(exclude_unset=True).items():
            columns.append(f'`{k}`')
            values.append(v)
        tableName = tableName or model.__class__.tableName()
        sql = f'INSERT INTO `{tableName}` ( {",".join(columns)} ) VALUES %s'
        await self.execute(sql, values)
        return self.lastrowid

    async def saveOne(self, model: BModel, *, tableName: str = ''):
        columns: list[str] = []
        values: list[Any] = []
        for k, v in model.model_dump(exclude_unset=True).items():
            columns.append(f'`{k}`')
            values.append(v)
        tableName = tableName or model.__class__.tableName()
        updateSql = ','.join([f'{x} = VALUES( {x} )' for x in columns])
        sql = f'''INSERT INTO `{tableName}` ( {','.join(columns)} ) VALUES %s ON DUPLICATE KEY UPDATE {updateSql}'''
        return await self.execute(sql, values)

    async def addList(self, modelList: Sequence[BModel], *, tableName: str = ''):
        assert modelList, 'modelList 必须至少有一个元素'
        columns: list[str] = []
        values: list[Sequence[Any]] = []
        for k in modelList[0].model_dump(exclude_unset=True).keys():
            columns.append(k)
        for model in modelList:
            values.append([getattr(model, x) for x in columns])
        columns = [f'`{x}`' for x in columns]
        tableName = tableName or modelList[0].__class__.tableName()
        sql = f'''INSERT INTO `{tableName}` ( {','.join(columns)} ) VALUES {getSqlPlacement(columns, '%s')}'''
        sql = self.sqlFormat(sql)
        return await self.cursor.executemany(sql, values)

    async def saveList(self, modelList: Sequence[BModel], *, tableName: str = ''):
        assert modelList, 'modelList 必须至少有一个元素'
        columns: list[str] = []
        values: list[Sequence[Any]] = []
        for k in modelList[0].model_dump(exclude_unset=True).keys():
            columns.append(k)
        for model in modelList:
            values.append([getattr(model, x) for x in columns])
        columns = [f'`{x}`' for x in columns]
        tableName = tableName or modelList[0].__class__.tableName()
        updateSql = ','.join([f'{x} = VALUES( {x} )' for x in columns])
        sql = f'''INSERT INTO `{tableName}` ( {','.join(columns)} ) VALUES {getSqlPlacement(columns, '%s')} ON DUPLICATE KEY UPDATE {updateSql}'''
        sql = self.sqlFormat(sql)
        return await self.cursor.executemany(sql, values)

    def _getColumns(self) -> tuple[str, ...]:
        return tuple(x[0] for x in toAny(self.cursor.description))


class Db:
    @asynccontextmanager
    async def getCursor(self) -> AsyncGenerator[DbCursor, None]:
        yield Null

    def asMySqlDb(self):
        return cast(MysqlDb, self)

    def asSqliteDb(self):
        return cast(SqliteDb, self)


# ==============================================================================

class MysqlCursor(DbCursor):
    pass


@dataclass
class MysqlDb(Db):
    host: str
    port: int
    user: str
    password: str
    db: str = ''
    _pool: aiomysql.Pool = Null

    @asynccontextmanager
    async def getCursor(self) -> AsyncGenerator[MysqlCursor, None]:
        isEcho = logging.getLogger().level is logging.DEBUG
        if not self._pool:
            self._pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db or None,
                echo=isEcho,
            )
        async with cast(aiomysql.Connection, self._pool.acquire()) as connection:
            async with cast(aiomysql.Cursor, connection.cursor()) as cursor:
                isAnyException = False
                try:
                    yield MysqlCursor(cursor)
                except Exception:
                    isAnyException = True
                    raise
                finally:
                    if isAnyException:
                        await connection.rollback()
                    else:
                        await connection.commit()

    async def close(self):
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()


# ==============================================================================


class SqliteCursor(DbCursor):

    async def execute(self, sql: str, *args: Any):
        sql = super().sqlFormat(sql)
        values = []
        if args:
            for value in args:
                if type(value) in [set, list, tuple]:
                    sql = sql.replace('%s', self._makePlacement(value), 1)
                    values.extend(list(value))
                else:
                    sql = sql.replace('%s', '?', 1)
                    values.append(value)
        return await self.cursor.execute(sql, values)

    def _makePlacement(self, value: Sequence[Any] | set[Any]) -> str:
        return f'( {', '.join(['?'] * len(value))} )'

    async def saveOne(self, model: BModel, *, tableName: str = ''):
        columns: list[str] = []
        values: list[Any] = []
        for k, v in model.model_dump(exclude_unset=True).items():
            columns.append(f'`{k}`')
            values.append(v)
        tableName = tableName or model.__class__.tableName()
        sql = f'''
            INSERT OR REPLACE INTO
                `{tableName}` ( {','.join(columns)} )
            VALUES
                %s
        '''
        return await self.execute(sql, values)

    async def saveList(self, modelList: Sequence[BModel], *, tableName: str = ''):
        assert modelList, 'modelList 必须至少有一个元素'

        # 遍历所有modelList里面所有的modeul_dumps(exclude_unset=True).keys()，取并集
        columns: list[str] = []
        for model in modelList:
            columns.extend(model.model_dump(exclude_unset=True).keys())
        columns = list(set(columns))
        values: list[Sequence[Any]] = []
        for model in modelList:
            values.append([getattr(model, x) for x in columns])
        columns = [f'`{x}`' for x in columns]
        tableName = tableName or modelList[0].__class__.tableName()
        sql = f'INSERT OR REPLACE INTO `{tableName}` ( {','.join(columns)} ) VALUES {self._makePlacement(columns)}'
        sql = self.sqlFormat(sql)
        return await self.cursor.executemany(sql, values)


_isInitedSqlite = False


def _initSqlite():
    global _isInitedSqlite
    if not _isInitedSqlite:
        import sqlite3
        sqlite3.register_converter(
            'bool',
            lambda x: x not in (
                b'',
                b'0',
                # None, # 如果是None根本就不会进来，这里判断也没有意义
            )
        )
        _isInitedSqlite = True


class SqliteDb:

    def __init__(self, file: XPath):
        self.file = file
        _initSqlite()

    @asynccontextmanager
    async def getCursor(self) -> AsyncGenerator[SqliteCursor, None]:
        bpath.make(bpath.get(self.file).parent)
        async with aiosqlite.connect(self.file) as connection:
            async with connection.cursor() as cursor:
                isAnyException = False
                try:
                    yield SqliteCursor(cursor)
                except Exception:
                    isAnyException = True
                    raise
                finally:
                    if isAnyException:
                        await connection.rollback()
                    else:
                        await connection.commit()
