from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_library.array_ import fold
from ..fable_library.date import (year, month, day, hour, minute, second)
from ..fable_library.option import value as value_1
from ..fable_library.seq import fold as fold_1
from ..fable_library.types import Array
from ..fable_library.util import (equals, identity_hash, number_hash, IEnumerable_1)

__A = TypeVar("__A")

_A = TypeVar("_A")

_B = TypeVar("_B")

def merge_hashes(hash1: int, hash2: int) -> int:
    return ((-1640531527 + hash2) + (hash1 << 6)) + (hash1 >> 2)


def hash_date_time(dt: Any) -> int:
    acc: int = 0
    acc = merge_hashes(acc, year(dt)) or 0
    acc = merge_hashes(acc, month(dt)) or 0
    acc = merge_hashes(acc, day(dt)) or 0
    acc = merge_hashes(acc, hour(dt)) or 0
    acc = merge_hashes(acc, minute(dt)) or 0
    acc = merge_hashes(acc, second(dt)) or 0
    return acc


def hash_1(obj: Any | None=None) -> int:
    if equals(obj, None):
        return 0

    else: 
        copy_of_struct: __A = obj
        return identity_hash(copy_of_struct)



def box_hash_option(a: Any | None=None) -> Any:
    def _arrow1(__unit: None=None, a: Any=a) -> int:
        copy_of_struct: _A = value_1(a)
        return identity_hash(copy_of_struct)

    def _arrow2(__unit: None=None, a: Any=a) -> int:
        copy_of_struct_1: int = 0
        return number_hash(copy_of_struct_1)

    return _arrow1() if (a is not None) else _arrow2()


def box_hash_array(a: Array[Any]) -> Any:
    def folder(acc: int, o: _A, a: Any=a) -> int:
        return merge_hashes(acc, hash_1(o))

    return fold(folder, 0, a)


def box_hash_seq(a: IEnumerable_1[Any]) -> Any:
    def folder(acc: int, o: _A, a: Any=a) -> int:
        return merge_hashes(acc, hash_1(o))

    return fold_1(folder, 0, a)


def box_hash_key_val_seq(a: IEnumerable_1[Any]) -> Any:
    def folder(acc: int, o: Any, a: Any=a) -> int:
        return merge_hashes(acc, merge_hashes(hash_1(o[0]), hash_1(o[1])))

    return fold_1(folder, 0, a)


def box_hash_key_val_seq_by(f: Callable[[_B], int], a: IEnumerable_1[Any]) -> Any:
    def folder(acc: int, o: Any, f: Any=f, a: Any=a) -> int:
        return merge_hashes(acc, merge_hashes(hash_1(o[0]), f(o[1])))

    return fold_1(folder, 0, a)


__all__ = ["merge_hashes", "hash_date_time", "hash_1", "box_hash_option", "box_hash_array", "box_hash_seq", "box_hash_key_val_seq", "box_hash_key_val_seq_by"]

