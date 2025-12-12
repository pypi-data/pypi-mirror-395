from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.map import of_seq
from ..fable_modules.fable_library.option import value
from ..fable_modules.fable_library.seq import (try_pick, exists)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (compare_primitives, equals)
from .comment import Comment
from .Helper.collections_ import (ResizeArray_choose, ResizeArray_map, ResizeArray_appendSingleton, ResizeArray_filter)

def try_item(key: str, comments: Array[Comment]) -> str | None:
    def chooser(c: Comment, key: Any=key, comments: Any=comments) -> str | None:
        match_value: str | None = c.Name
        (pattern_matching_result,) = (None,)
        if match_value is not None:
            if match_value == key:
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return c.Value

        elif pattern_matching_result == 1:
            return None


    return try_pick(chooser, comments)


def contains_key(key: str, comments: Array[Comment]) -> bool:
    def predicate(c: Comment, key: Any=key, comments: Any=comments) -> bool:
        match_value: str | None = c.Name
        (pattern_matching_result,) = (None,)
        if match_value is not None:
            if match_value == key:
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return True

        elif pattern_matching_result == 1:
            return False


    return exists(predicate, comments)


def item(key: str, comments: Array[Comment]) -> str:
    return value(try_item(key, comments))


def to_map(comments: Array[Comment]) -> Any:
    def f(c: Comment, comments: Any=comments) -> tuple[str, str | None] | None:
        match_value: str | None = c.Name
        if match_value is not None:
            return (match_value, c.Value)

        else: 
            return None


    class ObjectExpr699:
        @property
        def Compare(self) -> Callable[[str, str], int]:
            return compare_primitives

    return of_seq(ResizeArray_choose(f, comments), ObjectExpr699())


def set_1(comment: Comment, comments: Array[Comment]) -> Array[Comment]:
    if contains_key(value(comment.Name), comments):
        def f(c: Comment, comment: Any=comment, comments: Any=comments) -> Comment:
            if equals(c.Name, comment.Name):
                return comment

            else: 
                return c


        return ResizeArray_map(f, comments)

    else: 
        return ResizeArray_appendSingleton(comment, comments)



def drop_by_key(key: str, comments: Array[Comment]) -> Array[Comment]:
    def f(c: Comment, key: Any=key, comments: Any=comments) -> bool:
        match_value: str | None = c.Name
        (pattern_matching_result,) = (None,)
        if match_value is not None:
            if match_value == key:
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return False

        elif pattern_matching_result == 1:
            return True


    return ResizeArray_filter(f, comments)


__all__ = ["try_item", "contains_key", "item", "to_map", "set_1", "drop_by_key"]

