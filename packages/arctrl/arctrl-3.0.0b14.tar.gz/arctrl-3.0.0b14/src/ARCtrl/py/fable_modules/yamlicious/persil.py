from typing import Any
from ..fable_library.map_util import add_to_dict
from ..fable_library.reg_exp import (replace as replace_1, get_item, groups, create)
from ..fable_library.string_ import (replace, to_text, printf, split)
from ..fable_library.types import Array

def encoding_clean_up(s: str) -> str:
    return replace(s, "\r\n", "\n")


def string_clean_up(dict_1: Any, s: str) -> str:
    n: int = 0
    def matcheval(m: Any, dict_1: Any=dict_1, s: Any=s) -> str:
        nonlocal n
        if get_item(groups(m), "iscomment") is not None:
            return get_item(groups(m), "all") or ""

        else: 
            v: str = get_item(groups(m), "stringValue") or ""
            current_n: int = n or 0
            n = (n + 1) or 0
            add_to_dict(dict_1, current_n, v)
            return to_text(printf("<s f=%i/>"))(current_n)


    return replace_1(create("(?P<all>(?P<iscomment>#.*?)?\"(?P<stringValue>.+)\\\")"), s, matcheval)


def comment_clean_up(dict_1: Any, s: str) -> str:
    n: int = 0
    def matcheval(m: Any, dict_1: Any=dict_1, s: Any=s) -> str:
        nonlocal n
        v: str = get_item(groups(m), "comment") or ""
        current_n: int = n or 0
        n = (n + 1) or 0
        add_to_dict(dict_1, current_n, v)
        return to_text(printf("<c f=%i/>"))(current_n)

    return replace_1(create("#(?P<comment>.*)"), s, matcheval)


def cut(yaml_string: str) -> Array[str]:
    return split(yaml_string, ["\n"], None, 1)


def pipeline(yaml_string: str) -> dict[str, Any]:
    string_map: Any = dict([])
    comment_map: Any = dict([])
    return {
        "CommentMap": comment_map,
        "Lines": cut(comment_clean_up(comment_map, string_clean_up(string_map, encoding_clean_up(yaml_string)))),
        "StringMap": string_map
    }


__all__ = ["encoding_clean_up", "string_clean_up", "comment_clean_up", "cut", "pipeline"]

