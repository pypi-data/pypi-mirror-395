from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from .fable_modules.fable_library.array_ import append
from .fable_modules.fable_library.async_ import (sequential, catch_async)
from .fable_modules.fable_library.async_builder import (singleton, Async)
from .fable_modules.fable_library.result import FSharpResult_2
from .fable_modules.fable_library.types import (Array, to_string)
from .fable_modules.fable_library.util import (IEnumerator, get_enumerator, IEnumerable_1)

_U = TypeVar("_U")

_T = TypeVar("_T")

__A = TypeVar("__A")

__B = TypeVar("__B")

def start_sequential(starter_f: Callable[[_T], Async[_U]], tasks: IEnumerable_1[Any]) -> Async[Array[Any]]:
    def loop(en: IEnumerator[_T], starter_f: Any=starter_f, tasks: Any=tasks) -> Async[Array[_U]]:
        def _arrow3772(__unit: None=None, en: Any=en) -> Async[Array[_U]]:
            def _arrow3771(_arg: _U | None=None) -> Async[Array[_U]]:
                def _arrow3770(_arg_1: Array[_U]) -> Async[Array[_U]]:
                    return singleton.Return(append([_arg], _arg_1, None))

                return singleton.Bind(loop(en), _arrow3770)

            return singleton.Bind(starter_f(en.System_Collections_Generic_IEnumerator_1_get_Current()), _arrow3771) if en.System_Collections_IEnumerator_MoveNext() else singleton.Return([])

        return singleton.Delay(_arrow3772)

    return loop(get_enumerator(tasks))


def all(tasks: IEnumerable_1[Async[Any]]) -> Async[Array[Any]]:
    return sequential(tasks)


def map(f: Callable[[__A], __B], v: Async[Any]) -> Async[Any]:
    def _arrow3774(__unit: None=None, f: Any=f, v: Any=v) -> Async[__B]:
        def _arrow3773(_arg: __A | None=None) -> Async[__B]:
            return singleton.Return(f(_arg))

        return singleton.Bind(v, _arrow3773)

    return singleton.Delay(_arrow3774)


def as_async(v: Async[Any]) -> Async[Any]:
    return v


def catch_with(f: Callable[[Exception], _T], p: Async[Any]) -> Async[Any]:
    def _arrow3776(__unit: None=None, f: Any=f, p: Any=p) -> Async[_T]:
        def _arrow3775(_arg: Any) -> Async[_T]:
            r: Any = _arg
            return singleton.Return(f(r.fields[0])) if (r.tag == 1) else singleton.Return(r.fields[0])

        return singleton.Bind(catch_async(p), _arrow3775)

    return singleton.Delay(_arrow3776)


def catch_as_result(p: Async[Any]) -> Async[FSharpResult_2[Any, str]]:
    def _arrow3778(__unit: None=None, p: Any=p) -> Async[FSharpResult_2[_T, str]]:
        def _arrow3777(_arg: Any) -> Async[FSharpResult_2[_T, str]]:
            r: Any = _arg
            return singleton.Return(FSharpResult_2(1, to_string(r.fields[0]))) if (r.tag == 1) else singleton.Return(FSharpResult_2(0, r.fields[0]))

        return singleton.Bind(catch_async(p), _arrow3777)

    return singleton.Delay(_arrow3778)


__all__ = ["start_sequential", "all", "map", "as_async", "catch_with", "catch_as_result"]

