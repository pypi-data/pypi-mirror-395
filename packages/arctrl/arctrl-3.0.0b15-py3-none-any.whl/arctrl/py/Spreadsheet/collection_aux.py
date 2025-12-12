from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.array_ import (initialize, skip as skip_1, try_item)
from ..fable_modules.fable_library.list import (try_pick, FSharpList, is_empty, reverse, head, cons, tail, empty)
from ..fable_modules.fable_library.map_util import try_get_value
from ..fable_modules.fable_library.option import (value, some)
from ..fable_modules.fable_library.seq import (skip, max_by, try_find)
from ..fable_modules.fable_library.types import (Array, FSharpRef)
from ..fable_modules.fable_library.util import (IEnumerable_1, compare_primitives)

__A = TypeVar("__A")

_T = TypeVar("_T")

_A = TypeVar("_A")

_B = TypeVar("_B")

_C = TypeVar("_C")

_D = TypeVar("_D")

_U = TypeVar("_U")

__B = TypeVar("__B")

__C = TypeVar("__C")

__D = TypeVar("__D")

_V = TypeVar("_V")

def Seq_trySkip(i: int, s: IEnumerable_1[Any]) -> IEnumerable_1[Any] | None:
    try: 
        return skip(i, s)

    except Exception as match_value:
        return None



def Array_ofIndexedSeq(s: IEnumerable_1[tuple[int, str]]) -> Array[str]:
    def _arrow990(tuple: tuple[int, str], s: Any=s) -> int:
        return tuple[0]

    class ObjectExpr991:
        @property
        def Compare(self) -> Callable[[int, int], int]:
            return compare_primitives

    def _arrow993(i: int, s: Any=s) -> str:
        def _arrow992(arg: tuple[int, str]) -> bool:
            return i == arg[0]

        match_value: tuple[int, str] | None = try_find(_arrow992, s)
        if match_value is None:
            return ""

        else: 
            i_1: int = match_value[0] or 0
            return match_value[1]


    return initialize(1 + max_by(_arrow990, s, ObjectExpr991())[0], _arrow993, None)


def Array_trySkip(i: int, a: Array[Any]) -> Array[Any] | None:
    try: 
        return skip_1(i, a, None)

    except Exception as match_value:
        return None



def Array_tryItemDefault(i: int, d: Any, a: Array[Any]) -> Any:
    match_value: __A | None = try_item(i, a)
    if match_value is None:
        return d

    else: 
        return value(match_value)



def Array_map4(f: Callable[[_A, _B, _C, _D], _T], aa: Array[Any], ba: Array[Any], ca: Array[Any], da: Array[Any]) -> Array[Any]:
    if not ((len(ca) == len(da)) if ((len(ba) == len(ca)) if (len(aa) == len(ba)) else False) else False):
        raise Exception("")

    def _arrow994(i: int, f: Any=f, aa: Any=aa, ba: Any=ba, ca: Any=ca, da: Any=da) -> _T:
        return f(aa[i], ba[i], ca[i], da[i])

    return initialize(len(aa), _arrow994, None)


def List_tryPickDefault(chooser: Callable[[_T], _U | None], d: Any, list_1: FSharpList[Any]) -> Any:
    match_value: _U | None = try_pick(chooser, list_1)
    if match_value is None:
        return d

    else: 
        return value(match_value)



def List_unzip4(l: FSharpList[tuple[_A, _B, _C, _D]]) -> tuple[FSharpList[_A], FSharpList[_B], FSharpList[_C], FSharpList[_D]]:
    def loop(la_mut: FSharpList[Any], lb_mut: FSharpList[Any], lc_mut: FSharpList[Any], ld_mut: FSharpList[Any], l_1_mut: FSharpList[tuple[__A, __B, __C, __D]], l: Any=l) -> tuple[FSharpList[__A], FSharpList[__B], FSharpList[__C], FSharpList[__D]]:
        while True:
            (la, lb, lc, ld, l_1) = (la_mut, lb_mut, lc_mut, ld_mut, l_1_mut)
            if is_empty(l_1):
                return (reverse(la), reverse(lb), reverse(lc), reverse(ld))

            else: 
                la_mut = cons(head(l_1)[0], la)
                lb_mut = cons(head(l_1)[1], lb)
                lc_mut = cons(head(l_1)[2], lc)
                ld_mut = cons(head(l_1)[3], ld)
                l_1_mut = tail(l_1)
                continue

            break

    return loop(empty(), empty(), empty(), empty(), l)


def Dictionary_tryGetValue(k: Any, dict_1: Any) -> Any | None:
    pattern_input: tuple[bool, _V]
    out_arg: _V = None
    def _arrow995(__unit: None=None, k: Any=k, dict_1: Any=dict_1) -> _V:
        return out_arg

    def _arrow996(v: _V | None=None, k: Any=k, dict_1: Any=dict_1) -> None:
        nonlocal out_arg
        out_arg = v

    pattern_input = (try_get_value(dict_1, k, FSharpRef(_arrow995, _arrow996)), out_arg)
    if pattern_input[0]:
        return some(pattern_input[1])

    else: 
        return None



def Dictionary_tryGetString(k: Any, dict_1: Any) -> str | None:
    pattern_input: tuple[bool, str]
    out_arg: str = None
    def _arrow997(__unit: None=None, k: Any=k, dict_1: Any=dict_1) -> str:
        return out_arg

    def _arrow998(v: str, k: Any=k, dict_1: Any=dict_1) -> None:
        nonlocal out_arg
        out_arg = v

    pattern_input = (try_get_value(dict_1, k, FSharpRef(_arrow997, _arrow998)), out_arg)
    v_1: str = pattern_input[1]
    if (v_1.strip() != "") if pattern_input[0] else False:
        return v_1.strip()

    else: 
        return None



__all__ = ["Seq_trySkip", "Array_ofIndexedSeq", "Array_trySkip", "Array_tryItemDefault", "Array_map4", "List_tryPickDefault", "List_unzip4", "Dictionary_tryGetValue", "Dictionary_tryGetString"]

