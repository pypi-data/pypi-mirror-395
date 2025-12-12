from __future__ import annotations

import struct
from typing import Any, Literal, cast

from .bfunc import getValueInside


def decode(value: bytes):
    import chardet
    data = chardet.detect(value)
    encoding = data['encoding'] or 'utf8'
    return value.decode(encoding)


class BytesWriter():

    def __init__(self, endian: _EndianType):
        self.endian = endian
        self.formats: list[str] = []
        self.values: list[Any] = []

    def toBytes(self):
        return struct.pack(
            f'{self.endian}{"".join(self.formats)}',
            *self.values
        )

    def _write(self, format: str, value: int | float | bool | str | bytes):
        self.formats.append(format)
        self.values.append(value)

    def _writeList(self, func: Any, ary: list[Any]):
        self.writeUint(len(ary))
        for value in ary:
            func(value)
        return self

    # ---------------------------------------------------------------------------

    def writeShort(self, value: int):
        'int16'
        self._write('h', getValueInside(value, -32768, 32767))
        return self

    def writeUshort(self, value: int):
        'int16'
        self._write('H', getValueInside(value, 0, 65535))
        return self

    def writeInt(self, value: int):
        'int32'
        self._write('i', getValueInside(value, -2147483648, 2147483647))
        return self

    def writeUint(self, value: int):
        'int32'
        self._write('I', getValueInside(value, 0, 4294967295))
        return self

    def writeLong(self, value: int):
        'int64'
        self._write('q', getValueInside(value, -9223372036854775808, 9223372036854775807))
        return self

    def writeUlong(self, value: int):
        'int64'
        self._write('Q', getValueInside(value, 0, 18446744073709551615))
        return self

    def writeFloat(self, value: float):
        self._write('f', value)
        return self

    def writeDouble(self, value: float):
        self._write('d', value)
        return self

    def writeBool(self, value: bool):
        self._write('?', value)
        return self

    def writeStr(self, value: str):
        valueBytes = value.encode('utf8')
        count = len(valueBytes)
        self.writeUshort(count)
        self._write(f'{count}s', valueBytes)
        return self

    # ---------------------------------------------------------------------------

    def writeListShort(self, ary: list[int]):
        'int16[]'
        return self._writeList(self.writeShort, ary)

    def writeListUshort(self, ary: list[int]):
        'int16[]'
        return self._writeList(self.writeUshort, ary)

    def writeListInt(self, ary: list[int]):
        'int32[]'
        return self._writeList(self.writeInt, ary)

    def writeListUint(self, ary: list[int]):
        'int32[]'
        return self._writeList(self.writeUint, ary)

    def writeListLong(self, ary: list[int]):
        'int64[]'
        return self._writeList(self.writeLong, ary)

    def writeListUlong(self, ary: list[int]):
        'int64[]'
        return self._writeList(self.writeUlong, ary)

    def writeListFloat(self, ary: list[float]):
        return self._writeList(self.writeFloat, ary)

    def writeListDouble(self, ary: list[float]):
        return self._writeList(self.writeDouble, ary)

    def writeListBool(self, ary: list[bool]):
        return self._writeList(self.writeBool, ary)

    def writeListStr(self, ary: list[str]):
        return self._writeList(self.writeStr, ary)


class BytesReader():

    offset: int
    data: bytes

    def __init__(self, endian: _EndianType, data: bytes):
        self.endian = endian
        self.offset = 0
        self.data = data

    def _read(self, fmt: str):
        result = struct.unpack_from(f'{self.endian}{fmt}', self.data, self.offset)[0]
        self.offset += struct.calcsize(fmt)
        return result

    def _readList(self, func: Any):
        ary: list[Any] = []
        count = self.readUint()
        for _ in range(count):
            ary.append(func())
        return ary

    # ---------------------------------------------------------------------------

    def readShort(self):
        'int16'
        return cast(int, self._read('h'))

    def readUshort(self):
        'int16'
        return cast(int, self._read('H'))

    def readInt(self):
        'int32'
        return cast(int, self._read('i'))

    def readUint(self):
        'int32'
        return cast(int, self._read('I'))

    def readLong(self):
        'int64'
        return cast(int, self._read('q'))

    def readUlong(self):
        'int64'
        return cast(int, self._read('Q'))

    def readFloat(self):
        return cast(float, self._read('f'))

    def readDouble(self):
        return cast(float, self._read('d'))

    def readBool(self):
        return cast(bool, self._read('?'))

    def readStr(self):
        count = self.readUshort()
        return cast(str, self._read(f'{count}s').decode())

    # ---------------------------------------------------------------------------

    def readListShort(self):
        'int16[]'
        return cast(list[int], self._readList(self.readShort))

    def readListUshort(self):
        'int16[]'
        return cast(list[int], self._readList(self.readUshort))

    def readListInt(self):
        'int32[]'
        return cast(list[int], self._readList(self.readInt))

    def readListUint(self):
        'int32[]'
        return cast(list[int], self._readList(self.readUint))

    def readListLong(self):
        'int64[]'
        return cast(list[int], self._readList(self.readLong))

    def readListUlong(self):
        'int64[]'
        return cast(list[int], self._readList(self.readUlong))

    def readListFloat(self):
        return cast(list[float], self._readList(self.readFloat))

    def readListDouble(self):
        return cast(list[float], self._readList(self.readDouble))

    def readListBool(self):
        return cast(list[bool], self._readList(self.readBool))

    def readListStr(self):
        return cast(list[str], self._readList(self.readStr))


# ------------------------------------------------------------------------------------


_EndianType = Literal[
    # https://docs.python.org/zh-cn/3/library/struct.html#byte-order-size-and-alignment
    '@',  # 按原字节
    '=',  # 按原字节
    '<',  # 小端
    '>',  # 大端
    '!',  # 网络（=大端）
]
