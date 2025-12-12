from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from ..fable_library.option import default_arg
from ..fable_library.reflection import (TypeInfo, int32_type, record_type, string_type, class_type, list_type, union_type, option_type)
from ..fable_library.string_ import initialize
from ..fable_library.system_text import (StringBuilder__ctor, StringBuilder__AppendLine_Z721C83C5)
from ..fable_library.types import (Record, to_string, Array, Union)
from ..fable_library.util import (ignore, get_enumerator)

def _expr360() -> TypeInfo:
    return record_type("YAMLicious.YAMLiciousTypes.Config", [], Config, lambda: [("Whitespace", int32_type), ("Level", int32_type)])


@dataclass(eq = False, repr = False, slots = True)
class Config(Record):
    Whitespace: int
    Level: int

Config_reflection = _expr360

def Config_init_71136F3F(whitespace: int | None=None) -> Config:
    return Config(default_arg(whitespace, 4), 0)


def Config__get_WhitespaceString(this: Config) -> str:
    def _arrow361(_arg: int, this: Any=this) -> str:
        return " "

    return initialize(this.Level * this.Whitespace, _arrow361)


def _expr362() -> TypeInfo:
    return record_type("YAMLicious.YAMLiciousTypes.Preprocessor", [], Preprocessor, lambda: [("AST", PreprocessorElement_reflection()), ("StringMap", class_type("System.Collections.Generic.Dictionary`2", [int32_type, string_type])), ("CommentMap", class_type("System.Collections.Generic.Dictionary`2", [int32_type, string_type]))])


@dataclass(eq = False, repr = False, slots = True)
class Preprocessor(Record):
    AST: PreprocessorElement
    StringMap: Any
    CommentMap: Any

Preprocessor_reflection = _expr362

def _expr364() -> TypeInfo:
    return union_type("YAMLicious.YAMLiciousTypes.PreprocessorElement", [], PreprocessorElement, lambda: [[("Item", list_type(PreprocessorElement_reflection()))], [("Item", list_type(PreprocessorElement_reflection()))], [("Item", string_type)], []])


class PreprocessorElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Level", "Intendation", "Line", "Nil"]

    def __str__(self, __unit: None=None) -> str:
        this: PreprocessorElement = self
        sb: Any = StringBuilder__ctor()
        def innerprint(next_1: PreprocessorElement, level: int) -> None:
            def _arrow363(_arg: int, next_1: Any=next_1, level: Any=level) -> str:
                return " "

            indent: str = initialize(level * 2, _arrow363)
            if next_1.tag == 1:
                ignore(StringBuilder__AppendLine_Z721C83C5(sb, indent + "Intendation ["))
                with get_enumerator(next_1.fields[0]) as enumerator:
                    while enumerator.System_Collections_IEnumerator_MoveNext():
                        innerprint(enumerator.System_Collections_Generic_IEnumerator_1_get_Current(), level + 1)
                ignore(StringBuilder__AppendLine_Z721C83C5(sb, indent + "]"))

            elif next_1.tag == 0:
                ignore(StringBuilder__AppendLine_Z721C83C5(sb, indent + "Level ["))
                with get_enumerator(next_1.fields[0]) as enumerator_1:
                    while enumerator_1.System_Collections_IEnumerator_MoveNext():
                        innerprint(enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current(), level + 1)
                ignore(StringBuilder__AppendLine_Z721C83C5(sb, indent + "]"))

            elif next_1.tag == 3:
                pass

            else: 
                ignore(StringBuilder__AppendLine_Z721C83C5(sb, indent + (("Line \"" + next_1.fields[0]) + "\"")))


        innerprint(this, 0)
        return to_string(sb)


PreprocessorElement_reflection = _expr364

def _expr365() -> TypeInfo:
    return record_type("YAMLicious.YAMLiciousTypes.YAMLContent", [], YAMLContent, lambda: [("Value", string_type), ("Comment", option_type(string_type))])


@dataclass(eq = False, repr = False, slots = True)
class YAMLContent(Record):
    Value: str
    Comment: str | None

YAMLContent_reflection = _expr365

def YAMLContent_create_27AED5E3(value: str, comment: str | None=None) -> YAMLContent:
    return YAMLContent(value, comment)


def _expr366() -> TypeInfo:
    return union_type("YAMLicious.YAMLiciousTypes.YAMLElement", [], YAMLElement, lambda: [[("Item1", YAMLContent_reflection()), ("Item2", YAMLElement_reflection())], [("Item", YAMLContent_reflection())], [("Item", list_type(YAMLElement_reflection()))], [("Item", list_type(YAMLElement_reflection()))], [("Item", string_type)], []])


class YAMLElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Mapping", "Value", "Sequence", "Object", "Comment", "Nil"]


YAMLElement_reflection = _expr366

__all__ = ["Config_reflection", "Config_init_71136F3F", "Config__get_WhitespaceString", "Preprocessor_reflection", "PreprocessorElement_reflection", "YAMLContent_reflection", "YAMLContent_create_27AED5E3", "YAMLElement_reflection"]

