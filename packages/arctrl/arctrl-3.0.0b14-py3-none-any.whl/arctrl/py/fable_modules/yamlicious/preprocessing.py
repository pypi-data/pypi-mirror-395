from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_library.list import (is_empty, tail, FSharpList, head, cons, take_while as take_while_1, skip_while, reverse, empty, of_array, of_seq)
from ..fable_library.option import value as value_1
from ..fable_library.seq import (length, take_while)
from ..fable_library.system_text import (StringBuilder__ctor, StringBuilder__AppendLine_Z721C83C5)
from ..fable_library.types import to_string
from ..fable_library.util import (get_enumerator, ignore)
from .persil import pipeline
from .yamlicious_types import (Config, Config_init_71136F3F, Config__get_WhitespaceString, PreprocessorElement, Preprocessor)

def ReadHelpers_indentLevel(line: str) -> int:
    def predicate(c: str, line: Any=line) -> bool:
        return c == " "

    return length(take_while(predicate, line))


def write(root_element: PreprocessorElement, fconfig: Callable[[Config], Config] | None=None) -> str:
    config_1: Config
    config: Config = Config_init_71136F3F()
    config_1 = value_1(fconfig)(config) if (fconfig is not None) else config
    sb: Any = StringBuilder__ctor()
    def loop(current: PreprocessorElement, sb_1: Any, config_2: Config, root_element: Any=root_element, fconfig: Any=fconfig) -> None:
        if current.tag == 1:
            next_config: Config = Config(config_2.Whitespace, config_2.Level + 1)
            with get_enumerator(current.fields[0]) as enumerator:
                while enumerator.System_Collections_IEnumerator_MoveNext():
                    loop(enumerator.System_Collections_Generic_IEnumerator_1_get_Current(), sb_1, next_config)

        elif current.tag == 0:
            with get_enumerator(current.fields[0]) as enumerator_1:
                while enumerator_1.System_Collections_IEnumerator_MoveNext():
                    loop(enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current(), sb_1, config_2)

        elif current.tag == 3:
            pass

        else: 
            ignore(StringBuilder__AppendLine_Z721C83C5(sb_1, Config__get_WhitespaceString(config_2) + current.fields[0]))


    loop(root_element, sb, config_1)
    return to_string(sb)


def read(yaml_str: str) -> Preprocessor:
    content: dict[str, Any] = pipeline(yaml_str)
    def loop(lines_mut: FSharpList[str], current_intendation_mut: int, acc_mut: FSharpList[PreprocessorElement], yaml_str: Any=yaml_str) -> FSharpList[PreprocessorElement]:
        while True:
            (lines, current_intendation, acc) = (lines_mut, current_intendation_mut, acc_mut)
            if not is_empty(lines):
                rest: FSharpList[str] = tail(lines)
                line: str = head(lines)
                line_ele: PreprocessorElement = PreprocessorElement(2, line.strip())
                next_intendation: int = ReadHelpers_indentLevel(line) or 0
                if next_intendation == current_intendation:
                    lines_mut = rest
                    current_intendation_mut = current_intendation
                    acc_mut = cons(PreprocessorElement(2, line.strip()), acc)
                    continue

                else: 
                    def predicate(l: str, lines: Any=lines, current_intendation: Any=current_intendation, acc: Any=acc) -> bool:
                        return ReadHelpers_indentLevel(l) > current_intendation

                    next_level_lines: FSharpList[str] = take_while_1(predicate, rest)
                    def predicate_1(l_1: str, lines: Any=lines, current_intendation: Any=current_intendation, acc: Any=acc) -> bool:
                        return ReadHelpers_indentLevel(l_1) > current_intendation

                    lines_mut = skip_while(predicate_1, rest)
                    current_intendation_mut = current_intendation
                    acc_mut = cons(PreprocessorElement(1, cons(line_ele, reverse(loop(next_level_lines, next_intendation, empty())))), acc)
                    continue


            else: 
                return acc

            break

    return Preprocessor(PreprocessorElement(0, reverse(loop(of_array(content["Lines"]), 0, empty()))), content["StringMap"], content["CommentMap"])


def mk_line(line: str) -> PreprocessorElement:
    return PreprocessorElement(2, line)


def mkl_level(children: Any | None=None) -> PreprocessorElement:
    return PreprocessorElement(0, of_seq(children))


def mk_intendation(children: Any | None=None) -> PreprocessorElement:
    return PreprocessorElement(1, of_seq(children))


__all__ = ["ReadHelpers_indentLevel", "write", "read", "mk_line", "mkl_level", "mk_intendation"]

