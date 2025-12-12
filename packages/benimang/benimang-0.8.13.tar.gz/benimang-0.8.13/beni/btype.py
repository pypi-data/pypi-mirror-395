from pathlib import Path
from typing import Any, Callable, Coroutine, ParamSpec, Sequence, TypeVar, cast

Null = cast(Any, None)
Func = Callable[..., Any]
AsyncFunc = Callable[..., Coroutine[Any, Any, Any]]
XPath = Path | str
Ifs = int | float | str

FuncType = TypeVar("FuncType", bound=Func)
AsyncFuncType = TypeVar("AsyncFuncType", bound=AsyncFunc)
Params = ParamSpec('Params')
AnyType = TypeVar("AnyType")
IfsType = TypeVar("IfsType", int, float, str)
SomeType = set[AnyType] | Sequence[AnyType]
