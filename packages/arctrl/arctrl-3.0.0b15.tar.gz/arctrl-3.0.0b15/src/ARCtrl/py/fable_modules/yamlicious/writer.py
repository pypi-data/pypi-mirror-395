from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_library.list import (FSharpList, map as map_1, singleton, of_array)
from ..fable_library.option import (default_arg, map)
from ..fable_library.seq import (for_all, to_list, delay, map as map_2, collect, singleton as singleton_1)
from ..fable_library.string_ import join
from ..fable_library.util import IEnumerable_1
from .preprocessing import write as write_1
from .yamlicious_types import (YAMLElement, YAMLContent, PreprocessorElement, Config)

def StyleVerifier_checkInlineSequence(ele: FSharpList[YAMLElement]) -> bool:
    def predicate(x: YAMLElement, ele: Any=ele) -> bool:
        (pattern_matching_result,) = (None,)
        if x.tag == 1:
            if x.fields[0].Comment is None:
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return True

        elif pattern_matching_result == 1:
            return False


    return for_all(predicate, ele)


def Formatting_mkComment(comment: str) -> str:
    return "#" + comment


def Formatting_mkKey(key: str) -> str:
    return key + ":"


def Formatting_mkContent(content: YAMLContent) -> str:
    def mapping(s: str, content: Any=content) -> str:
        return " " + Formatting_mkComment(s)

    return content.Value + default_arg(map(mapping, content.Comment), "")


def Formatting_mkInlineSequence(seq: FSharpList[YAMLElement]) -> str:
    def mapping(x: YAMLElement, seq: Any=seq) -> str:
        (pattern_matching_result, v) = (None, None)
        if x.tag == 1:
            if x.fields[0].Comment is None:
                pattern_matching_result = 0
                v = x.fields[0].Value

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return v

        elif pattern_matching_result == 1:
            raise Exception("Invalid sequence element")


    return ("[" + join(", ", map_1(mapping, seq))) + "]"


def Formatting_mkMinusLine(c: str) -> str:
    return "- " + c


def detokenize(ele: YAMLElement) -> PreprocessorElement:
    def loop(ele_1: YAMLElement, ele: Any=ele) -> PreprocessorElement:
        if ele_1.tag == 0:
            v: YAMLElement = ele_1.fields[1]
            key: YAMLContent = ele_1.fields[0]
            (pattern_matching_result, v_1, seq_1, any_else) = (None, None, None, None)
            if v.tag == 1:
                pattern_matching_result = 0
                v_1 = v.fields[0]

            elif v.tag == 2:
                if StyleVerifier_checkInlineSequence(v.fields[0]):
                    pattern_matching_result = 1
                    seq_1 = v.fields[0]

                else: 
                    pattern_matching_result = 2
                    any_else = v


            else: 
                pattern_matching_result = 2
                any_else = v

            if pattern_matching_result == 0:
                return PreprocessorElement(2, (Formatting_mkKey(key.Value) + " ") + Formatting_mkContent(v_1))

            elif pattern_matching_result == 1:
                return PreprocessorElement(2, (Formatting_mkKey(key.Value) + " ") + Formatting_mkInlineSequence(seq_1))

            elif pattern_matching_result == 2:
                return PreprocessorElement(0, of_array([PreprocessorElement(2, Formatting_mkKey(Formatting_mkContent(key))), PreprocessorElement(1, singleton(loop(any_else)))]))


        elif ele_1.tag == 1:
            return PreprocessorElement(2, Formatting_mkContent(ele_1.fields[0]))

        elif ele_1.tag == 3:
            def _arrow376(__unit: None=None, ele_1: Any=ele_1) -> IEnumerable_1[PreprocessorElement]:
                return map_2(loop, ele_1.fields[0])

            return PreprocessorElement(0, to_list(delay(_arrow376)))

        elif ele_1.tag == 2:
            def _arrow378(__unit: None=None, ele_1: Any=ele_1) -> IEnumerable_1[PreprocessorElement]:
                def _arrow377(ele_3: YAMLElement) -> IEnumerable_1[PreprocessorElement]:
                    match_value: YAMLElement = ele_3
                    (pattern_matching_result_1, v_3, seq_5, any_else_1) = (None, None, None, None)
                    if match_value.tag == 1:
                        pattern_matching_result_1 = 0
                        v_3 = match_value.fields[0]

                    elif match_value.tag == 2:
                        if StyleVerifier_checkInlineSequence(match_value.fields[0]):
                            pattern_matching_result_1 = 1
                            seq_5 = match_value.fields[0]

                        else: 
                            pattern_matching_result_1 = 2
                            any_else_1 = match_value


                    else: 
                        pattern_matching_result_1 = 2
                        any_else_1 = match_value

                    if pattern_matching_result_1 == 0:
                        return singleton_1(PreprocessorElement(2, Formatting_mkMinusLine(Formatting_mkContent(v_3))))

                    elif pattern_matching_result_1 == 1:
                        return singleton_1(PreprocessorElement(2, Formatting_mkMinusLine(Formatting_mkInlineSequence(seq_5))))

                    elif pattern_matching_result_1 == 2:
                        return singleton_1(PreprocessorElement(0, of_array([PreprocessorElement(2, "-"), PreprocessorElement(1, singleton(loop(any_else_1)))])))


                return collect(_arrow377, ele_1.fields[0])

            return PreprocessorElement(0, to_list(delay(_arrow378)))

        elif ele_1.tag == 4:
            return PreprocessorElement(2, Formatting_mkComment(ele_1.fields[0]))

        else: 
            return PreprocessorElement(3)


    return loop(ele)


def write(ele: YAMLElement, fconfig: Callable[[Config], Config] | None=None) -> str:
    return write_1(detokenize(ele), fconfig)


__all__ = ["StyleVerifier_checkInlineSequence", "Formatting_mkComment", "Formatting_mkKey", "Formatting_mkContent", "Formatting_mkInlineSequence", "Formatting_mkMinusLine", "detokenize", "write"]

