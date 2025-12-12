from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.option import (default_arg, bind)
from ...fable_modules.fable_library.reg_exp import (get_item, groups)
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...Core.comment import Comment
from ...Core.Helper.regex import ActivePatterns__007CRegex_007C__007C
from .conversions import Option_fromValueWithDefault

Comment_commentValueKey: str = "commentValue"

Comment_commentPattern: str = ("Comment\\s*\\[<(?<" + Comment_commentValueKey) + ">.+)>\\]"

Comment_commentPatternNoAngleBrackets: str = ("Comment\\s*\\[(?<" + Comment_commentValueKey) + ">.+)\\]"

def Comment__007CComment_007C__007C(key: str) -> str | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C(Comment_commentPattern, key)
    if active_pattern_result is not None:
        r: Any = active_pattern_result
        return get_item(groups(r), Comment_commentValueKey) or ""

    else: 
        active_pattern_result_1: Any | None = ActivePatterns__007CRegex_007C__007C(Comment_commentPatternNoAngleBrackets, key)
        if active_pattern_result_1 is not None:
            r_1: Any = active_pattern_result_1
            v: str = get_item(groups(r_1), Comment_commentValueKey) or ""
            if v == "<>":
                return None

            else: 
                return v


        else: 
            return None




def Comment_wrapCommentKey(k: str) -> str:
    return to_text(printf("Comment[%s]"))(k)


def Comment_fromString(k: str, v: str) -> Comment:
    name: str | None = Option_fromValueWithDefault("", k)
    value: str | None = Option_fromValueWithDefault("", v)
    return Comment.make(name, value)


def Comment_toString(c: Comment) -> tuple[str, str]:
    return (default_arg(c.Name, ""), default_arg(c.Value, ""))


Remark_remarkValueKey: str = "remarkValue"

Remark_remarkPattern: str = ("#(?<" + Remark_remarkValueKey) + ">.+)"

def Remark__007CRemark_007C__007C(key: str | None=None) -> str | None:
    def binder(k: str, key: Any=key) -> str | None:
        active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C(Remark_remarkPattern, k)
        if active_pattern_result is not None:
            r: Any = active_pattern_result
            return get_item(groups(r), Remark_remarkValueKey) or ""

        else: 
            return None


    return bind(binder, key)


def Remark_wrapRemark(r: str) -> str:
    return to_text(printf("#%s"))(r)


__all__ = ["Comment_commentValueKey", "Comment_commentPattern", "Comment_commentPatternNoAngleBrackets", "Comment__007CComment_007C__007C", "Comment_wrapCommentKey", "Comment_fromString", "Comment_toString", "Remark_remarkValueKey", "Remark_remarkPattern", "Remark__007CRemark_007C__007C", "Remark_wrapRemark"]

