from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.array_ import contains
from ...fable_modules.fable_library.list import (is_empty as is_empty_1, tail, FSharpList, head, append, singleton, empty)
from ...fable_modules.fable_library.map_util import (add_to_dict, try_get_value, remove_from_dict)
from ...fable_modules.fable_library.mutable_map import Dictionary
from ...fable_modules.fable_library.option import (some, value as value_1)
from ...fable_modules.fable_library.range import range_big_int
from ...fable_modules.fable_library.seq import (is_empty, iterate, map)
from ...fable_modules.fable_library.seq2 import group_by
from ...fable_modules.fable_library.types import (FSharpRef, Array)
from ...fable_modules.fable_library.util import (equals, structural_hash, IEnumerable_1, ignore, get_enumerator, dispose, min, compare_primitives)

_T = TypeVar("_T")

_U = TypeVar("_U")

_KEY_ = TypeVar("_KEY_")

_KEY = TypeVar("_KEY")

__B = TypeVar("__B")

__A = TypeVar("__A")

__C = TypeVar("__C")

__A_ = TypeVar("__A_")

_A = TypeVar("_A")

_A_ = TypeVar("_A_")

def Option_fromValueWithDefault(d: Any, v: Any) -> Any | None:
    if equals(d, v):
        return None

    else: 
        return some(v)



def Option_mapDefault(d: Any, f: Callable[[_T], _T], o: Any | None=None) -> Any | None:
    return Option_fromValueWithDefault(d, f(d) if (o is None) else f(value_1(o)))


def Option_mapOrDefault(d: Any | None, f: Callable[[_U], _T], o: Any | None=None) -> Any | None:
    if o is None:
        return d

    else: 
        return some(f(value_1(o)))



def Option_fromSeq(v: Any | None=None) -> Any | None:
    if is_empty(v):
        return None

    else: 
        return some(v)



def List_tryPickAndRemove(f: Callable[[_T], _U | None], lst: FSharpList[Any]) -> tuple[_U | None, FSharpList[_T]]:
    def loop(new_list_mut: FSharpList[_T], remaining_list_mut: FSharpList[_T], f: Any=f, lst: Any=lst) -> tuple[_U | None, FSharpList[_T]]:
        while True:
            (new_list, remaining_list) = (new_list_mut, remaining_list_mut)
            if not is_empty_1(remaining_list):
                t: FSharpList[_T] = tail(remaining_list)
                h: _T = head(remaining_list)
                match_value: _U | None = f(h)
                if match_value is None:
                    new_list_mut = append(new_list, singleton(h))
                    remaining_list_mut = t
                    continue

                else: 
                    return (some(value_1(match_value)), append(new_list, t))


            else: 
                return (None, new_list)

            break

    return loop(empty(), lst)


def Dictionary_addOrUpdate(key: Any, value: Any, dict_1: Any) -> None:
    if key in dict_1:
        dict_1[key] = value

    else: 
        add_to_dict(dict_1, key, value)



def Dictionary_ofSeq(s: IEnumerable_1[tuple[_KEY, _T]]) -> Any:
    class ObjectExpr637:
        @property
        def Equals(self) -> Callable[[_KEY_, _KEY_], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[_KEY_], int]:
            return structural_hash

    dict_1: Any = Dictionary([], ObjectExpr637())
    def action(tupled_arg: tuple[_KEY, _T], s: Any=s) -> None:
        add_to_dict(dict_1, tupled_arg[0], tupled_arg[1])

    iterate(action, s)
    return dict_1


def Dictionary_tryFind(key: Any, dict_1: Any) -> Any | None:
    pattern_input: tuple[bool, _T]
    out_arg: _T = None
    def _arrow638(__unit: None=None, key: Any=key, dict_1: Any=dict_1) -> _T:
        return out_arg

    def _arrow639(v: _T | None=None, key: Any=key, dict_1: Any=dict_1) -> None:
        nonlocal out_arg
        out_arg = v

    pattern_input = (try_get_value(dict_1, key, FSharpRef(_arrow638, _arrow639)), out_arg)
    if pattern_input[0]:
        return some(pattern_input[1])

    else: 
        return None



def Dictionary_ofSeqWithMerge(merge: Callable[[_T, _T], _T], s: IEnumerable_1[tuple[_KEY, _T]]) -> Any:
    class ObjectExpr640:
        @property
        def Equals(self) -> Callable[[_KEY_, _KEY_], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[_KEY_], int]:
            return structural_hash

    dict_1: Any = Dictionary([], ObjectExpr640())
    def action(tupled_arg: tuple[_KEY, _T], merge: Any=merge, s: Any=s) -> None:
        k: _KEY = tupled_arg[0]
        v: _T = tupled_arg[1]
        match_value: _T | None = Dictionary_tryFind(k, dict_1)
        if match_value is None:
            add_to_dict(dict_1, k, v)

        else: 
            v_0027: _T = value_1(match_value)
            ignore(remove_from_dict(dict_1, k))
            add_to_dict(dict_1, k, merge(v_0027, v))


    iterate(action, s)
    return dict_1


def Dictionary_init(__unit: None=None) -> Any:
    return dict()


def Dictionary_items(dict_1: Any) -> IEnumerable_1[Any]:
    return dict_1.items()


def StringDictionary_ofSeq(s: IEnumerable_1[tuple[str, str]]) -> Any:
    return dict(s)


def IntDictionary_ofSeq(s: IEnumerable_1[tuple[int, _T]]) -> Any:
    return dict(s)


def ResizeArray_create(i: int, v: Any) -> Array[Any]:
    a: Array[_T] = []
    if i > 0:
        for for_loop_var in range(1, i + 1, 1):
            (a.append(v))

    return a


def ResizeArray_singleton(a: Any | None=None) -> Array[Any]:
    b: Array[_T] = []
    (b.append(a))
    return b


def ResizeArray_map(f: Callable[[__A], __B], a: Array[Any]) -> Array[Any]:
    b: Array[__B] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: __A = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            (b.append(f(i)))

    finally: 
        dispose(enumerator)

    return b


def ResizeArray_mapi(f: Callable[[int, __A], __B], a: Array[Any]) -> Array[Any]:
    b: Array[__B] = []
    for i in range(0, (len(a) - 1) + 1, 1):
        (b.append(f(i, a[i])))
    return b


def ResizeArray_map2(f: Callable[[__A, __B], __C], a: Array[Any], b: Array[Any]) -> Array[Any]:
    c: Array[__C] = []
    def _arrow641(x: int, y: int, f: Any=f, a: Any=a, b: Any=b) -> int:
        return compare_primitives(x, y)

    n: int = min(_arrow641, len(a), len(b)) or 0
    for i in range(0, (n - 1) + 1, 1):
        (c.append(f(a[i], b[i])))
    return c


def ResizeArray_choose(f: Callable[[__A], __B | None], a: Array[Any]) -> Array[Any]:
    b: Array[__B] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            match_value: __B | None = f(enumerator.System_Collections_Generic_IEnumerator_1_get_Current())
            if match_value is None:
                pass

            else: 
                x: __B = value_1(match_value)
                (b.append(x))


    finally: 
        dispose(enumerator)

    return b


def ResizeArray_filter(f: Callable[[__A], bool], a: Array[Any]) -> Array[Any]:
    b: Array[__A] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: __A = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            if f(i):
                (b.append(i))


    finally: 
        dispose(enumerator)

    return b


def ResizeArray_fold(f: Callable[[__A, __B], __A], s: Any, a: Array[Any]) -> Any:
    state: __A = s
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: __B = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            state = f(state, i)

    finally: 
        dispose(enumerator)

    return state


def ResizeArray_foldBack(f: Callable[[__A, __B], __B], a: Array[Any], s: Any) -> Any:
    state: __B = s
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: __A = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            state = f(i, state)

    finally: 
        dispose(enumerator)

    return state


def ResizeArray_iter(f: Callable[[__A], None], a: Array[Any]) -> None:
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            f(enumerator.System_Collections_Generic_IEnumerator_1_get_Current())

    finally: 
        dispose(enumerator)



def ResizeArray_iteri(f: Callable[[int, __A], None], a: Array[Any]) -> None:
    for i in range(0, (len(a) - 1) + 1, 1):
        f(i, a[i])


def ResizeArray_init(n: int, f: Callable[[int], _T]) -> Array[Any]:
    a: Array[_T] = []
    for i in range(0, (n - 1) + 1, 1):
        (a.append(f(i)))
    return a


def ResizeArray_reduce(f: Callable[[__A, __A], __A], a: Array[Any]) -> Any:
    if len(a) == 0:
        raise Exception("ResizeArray.reduce: empty array")

    elif len(a) == 1:
        return a[0]

    else: 
        a_5: Array[__A] = a
        state: __A = a_5[0]
        for i in range(1, (len(a_5) - 1) + 1, 1):
            state = f(state, a_5[i])
        return state



def ResizeArray_collect(f: Callable[[__A], __B], a: Array[Any]) -> Array[Any]:
    b: Array[__C] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            with get_enumerator(f(enumerator.System_Collections_Generic_IEnumerator_1_get_Current())) as enumerator_1:
                while enumerator_1.System_Collections_IEnumerator_MoveNext():
                    j: __C = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                    (b.append(j))

    finally: 
        dispose(enumerator)

    return b


def ResizeArray_distinct(a: Array[Any]) -> Array[Any]:
    b: Array[__A] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: __A = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            class ObjectExpr642:
                @property
                def Equals(self) -> Callable[[__A_, __A_], bool]:
                    return equals

                @property
                def GetHashCode(self) -> Callable[[__A_], int]:
                    return structural_hash

            if not contains(i, b, ObjectExpr642()):
                (b.append(i))


    finally: 
        dispose(enumerator)

    return b


def ResizeArray_isEmpty(a: Array[Any]) -> bool:
    return len(a) == 0


def ResizeArray_append(a: Array[Any], b: Array[Any]) -> Array[Any]:
    c: Array[__A] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: __A = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            (c.append(i))

    finally: 
        dispose(enumerator)

    enumerator_1: Any = get_enumerator(b)
    try: 
        while enumerator_1.System_Collections_IEnumerator_MoveNext():
            i_1: __A = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
            (c.append(i_1))

    finally: 
        dispose(enumerator_1)

    return c


def ResizeArray_appendSingleton(b: Any, a: Array[Any]) -> Array[Any]:
    c: Array[_T] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: _T = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            (c.append(i))

    finally: 
        dispose(enumerator)

    (c.append(b))
    return c


def ResizeArray_indexed(a: Array[Any]) -> Array[tuple[int, __A]]:
    b: Array[tuple[int, __A]] = []
    for i in range(0, (len(a) - 1) + 1, 1):
        (b.append((i, a[i])))
    return b


def ResizeArray_rev(a: Array[Any]) -> Array[Any]:
    b: Array[__A] = []
    with get_enumerator(range_big_int(len(a) - 1, -1, 0)) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: int = enumerator.System_Collections_Generic_IEnumerator_1_get_Current() or 0
            (b.append(a[i]))
    return b


def ResizeArray_take(n: int, a: Array[Any]) -> Array[Any]:
    b: Array[__A] = []
    def _arrow643(x: int, y: int, n: Any=n, a: Any=a) -> int:
        return compare_primitives(x, y)

    n_1: int = min(_arrow643, n, len(a)) or 0
    for i in range(0, (n_1 - 1) + 1, 1):
        (b.append(a[i]))
    return b


def ResizeArray_groupBy(f: Callable[[_T], _A], a: Array[Any]) -> Array[tuple[_A, Array[_T]]]:
    def mapping(tupled_arg: tuple[_A, IEnumerable_1[_T]], f: Any=f, a: Any=a) -> tuple[_A, Array[_T]]:
        return (tupled_arg[0], list(tupled_arg[1]))

    class ObjectExpr644:
        @property
        def Equals(self) -> Callable[[_A_, _A_], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[_A_], int]:
            return structural_hash

    return list(map(mapping, group_by(f, a, ObjectExpr644())))


def ResizeArray_tryPick(f: Callable[[_T], __A | None], a: Array[Any]) -> Any | None:
    def loop(i_mut: int, f: Any=f, a: Any=a) -> __A | None:
        while True:
            (i,) = (i_mut,)
            if i < len(a):
                match_value: __A | None = f(a[i])
                if match_value is None:
                    i_mut = i + 1
                    continue

                else: 
                    return some(value_1(match_value))


            else: 
                return None

            break

    return loop(0)


def ResizeArray_zip(a: Array[Any], b: Array[Any]) -> Array[tuple[_T, _U]]:
    c: Array[tuple[_T, _U]] = []
    def _arrow645(x: int, y: int, a: Any=a, b: Any=b) -> int:
        return compare_primitives(x, y)

    n: int = min(_arrow645, len(a), len(b)) or 0
    for i in range(0, (n - 1) + 1, 1):
        (c.append((a[i], b[i])))
    return c


def ResizeArray_tryFind(f: Callable[[_T], bool], a: Array[Any]) -> Any | None:
    def loop(i_mut: int, f: Any=f, a: Any=a) -> _T | None:
        while True:
            (i,) = (i_mut,)
            if i < len(a):
                if f(a[i]):
                    return some(a[i])

                else: 
                    i_mut = i + 1
                    continue


            else: 
                return None

            break

    return loop(0)


__all__ = ["Option_fromValueWithDefault", "Option_mapDefault", "Option_mapOrDefault", "Option_fromSeq", "List_tryPickAndRemove", "Dictionary_addOrUpdate", "Dictionary_ofSeq", "Dictionary_tryFind", "Dictionary_ofSeqWithMerge", "Dictionary_init", "Dictionary_items", "StringDictionary_ofSeq", "IntDictionary_ofSeq", "ResizeArray_create", "ResizeArray_singleton", "ResizeArray_map", "ResizeArray_mapi", "ResizeArray_map2", "ResizeArray_choose", "ResizeArray_filter", "ResizeArray_fold", "ResizeArray_foldBack", "ResizeArray_iter", "ResizeArray_iteri", "ResizeArray_init", "ResizeArray_reduce", "ResizeArray_collect", "ResizeArray_distinct", "ResizeArray_isEmpty", "ResizeArray_append", "ResizeArray_appendSingleton", "ResizeArray_indexed", "ResizeArray_rev", "ResizeArray_take", "ResizeArray_groupBy", "ResizeArray_tryPick", "ResizeArray_zip", "ResizeArray_tryFind"]

