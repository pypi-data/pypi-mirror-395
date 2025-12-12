from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_library.int32 import parse
from ..fable_library.list import (cons, FSharpList, is_empty, empty, head, singleton as singleton_1, tail, of_array_with_tail, reverse, append as append_1)
from ..fable_library.map_util import get_item_from_dict
from ..fable_library.option import (map, value as value_2)
from ..fable_library.reg_exp import (match, create, get_item, groups)
from ..fable_library.seq import (to_list, delay, append, singleton, take_while, skip_while, map as map_1, collect, empty as empty_1)
from ..fable_library.string_ import (to_fail, printf, split as split_2, trim_end)
from ..fable_library.types import Array
from ..fable_library.util import IEnumerable_1
from .preprocessing import read as read_1
from .regex_active_patterns import (_007CSequenceMinusOpener_007C__007C, _007CYamlComment_007C__007C, _007CKeyValue_007C__007C, _007CYamlValue_007C__007C, _007CKey_007C__007C, _007CInlineJSON_007C__007C, _007CJSONKeyOpener_007C__007C, _007CJSONCloser_007C__007C, _007CInlineSequence_007C__007C, _007CSequenceSquareOpener_007C__007C, _007CSequenceSquareCloser_007C__007C, _007CSchemaNamespace_007C__007C)
from .yamlicious_types import (PreprocessorElement, YAMLElement, YAMLContent_create_27AED5E3, Preprocessor)

def restore_string_replace(string_dict: Any, v: str) -> str:
    m: Any = match(create("\\<s f=(?P<index>\\d+)\\/\\>"), v)
    if m is not None:
        return get_item_from_dict(string_dict, parse(get_item(groups(m), "index") or "", 511, False, 32))

    else: 
        return v



def restore_comment_replace(comment_dict: Any, comment_id: int | None=None) -> str | None:
    def mapping(id: int, comment_dict: Any=comment_dict, comment_id: Any=comment_id) -> str:
        return get_item_from_dict(comment_dict, id)

    return map(mapping, comment_id)


def collect_sequence_elements(eles: FSharpList[PreprocessorElement]) -> FSharpList[FSharpList[PreprocessorElement]]:
    (pattern_matching_result, rest, v, yaml_ast_list) = (None, None, None, None)
    if not is_empty(eles):
        active_pattern_result: dict[str, Any] | None = _007CSequenceMinusOpener_007C__007C(head(eles))
        if active_pattern_result is not None:
            if not is_empty(tail(eles)):
                if head(tail(eles)).tag == 1:
                    pattern_matching_result = 0
                    rest = tail(tail(eles))
                    v = active_pattern_result
                    yaml_ast_list = head(tail(eles)).fields[0]

                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def _arrow381(__unit: None=None, eles: Any=eles) -> IEnumerable_1[FSharpList[PreprocessorElement]]:
            def _arrow380(__unit: None=None) -> IEnumerable_1[FSharpList[PreprocessorElement]]:
                return collect_sequence_elements(rest)

            return append(singleton(cons(PreprocessorElement(2, value_2(v["Value"])), yaml_ast_list)) if (v["Value"] is not None) else singleton(yaml_ast_list), delay(_arrow380))

        return to_list(delay(_arrow381))

    elif pattern_matching_result == 1:
        if is_empty(eles):
            return empty()

        else: 
            active_pattern_result_1: dict[str, Any] | None = _007CSequenceMinusOpener_007C__007C(head(eles))
            if active_pattern_result_1 is not None:
                v_1: dict[str, Any] = active_pattern_result_1
                def _arrow383(__unit: None=None, eles: Any=eles) -> IEnumerable_1[FSharpList[PreprocessorElement]]:
                    def _arrow382(__unit: None=None) -> IEnumerable_1[FSharpList[PreprocessorElement]]:
                        return collect_sequence_elements(tail(eles))

                    return append(singleton(singleton_1(PreprocessorElement(2, value_2(v_1["Value"])))), delay(_arrow382))

                return to_list(delay(_arrow383))

            elif _007CYamlComment_007C__007C(head(eles)) is not None:
                def _arrow385(__unit: None=None, eles: Any=eles) -> IEnumerable_1[FSharpList[PreprocessorElement]]:
                    def _arrow384(__unit: None=None) -> IEnumerable_1[FSharpList[PreprocessorElement]]:
                        return collect_sequence_elements(tail(eles))

                    return append(singleton(singleton_1(head(eles))), delay(_arrow384))

                return to_list(delay(_arrow385))

            else: 
                return to_fail(printf("Unknown pattern for sequence elements: %A"))(eles)





def is_sequence_element(e: PreprocessorElement) -> bool:
    (pattern_matching_result,) = (None,)
    if e.tag == 1:
        pattern_matching_result = 0

    elif _007CSequenceMinusOpener_007C__007C(e) is not None:
        pattern_matching_result = 0

    elif _007CYamlComment_007C__007C(e) is not None:
        pattern_matching_result = 0

    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        return True

    elif pattern_matching_result == 1:
        return False



def tokenize(yaml_list: FSharpList[PreprocessorElement], string_dict: Any, comment_dict: Any) -> YAMLElement:
    def loop_read(restlist_mut: FSharpList[PreprocessorElement], acc_mut: FSharpList[YAMLElement], yaml_list: Any=yaml_list, string_dict: Any=string_dict, comment_dict: Any=comment_dict) -> YAMLElement:
        while True:
            (restlist, acc) = (restlist_mut, acc_mut)
            (pattern_matching_result, rest0, v, yaml_ast_list) = (None, None, None, None)
            if not is_empty(restlist):
                active_pattern_result: dict[str, Any] | None = _007CSchemaNamespace_007C__007C(head(restlist))
                if active_pattern_result is not None:
                    if not is_empty(tail(restlist)):
                        if head(tail(restlist)).tag == 1:
                            pattern_matching_result = 0
                            rest0 = tail(tail(restlist))
                            v = active_pattern_result
                            yaml_ast_list = head(tail(restlist)).fields[0]

                        else: 
                            pattern_matching_result = 1


                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1

            if pattern_matching_result == 0:
                def _arrow386(e: PreprocessorElement, restlist: Any=restlist, acc: Any=acc) -> bool:
                    return is_sequence_element(e)

                sequence_elements: FSharpList[FSharpList[PreprocessorElement]] = collect_sequence_elements(to_list(take_while(_arrow386, rest0)))
                def _arrow387(e_1: PreprocessorElement, restlist: Any=restlist, acc: Any=acc) -> bool:
                    return is_sequence_element(e_1)

                restlist_mut = to_list(skip_while(_arrow387, rest0))
                def _arrow393(__unit: None=None, restlist: Any=restlist, acc: Any=acc) -> IEnumerable_1[YAMLElement]:
                    def _arrow392(__unit: None=None) -> IEnumerable_1[YAMLElement]:
                        def _arrow391(i: FSharpList[PreprocessorElement]) -> YAMLElement:
                            return loop_read(i, empty())

                        return map_1(_arrow391, sequence_elements)

                    return append(singleton(loop_read(cons(PreprocessorElement(2, v["Key"]), yaml_ast_list), empty())), delay(_arrow392))

                acc_mut = cons(YAMLElement(2, to_list(delay(_arrow393))), acc)
                continue

            elif pattern_matching_result == 1:
                (pattern_matching_result_1, rest0_1, v_1, rest0_2, v_2, yaml_ast_list_1) = (None, None, None, None, None, None)
                if not is_empty(restlist):
                    active_pattern_result_1: dict[str, Any] | None = _007CSchemaNamespace_007C__007C(head(restlist))
                    if active_pattern_result_1 is not None:
                        pattern_matching_result_1 = 0
                        rest0_1 = tail(restlist)
                        v_1 = active_pattern_result_1

                    else: 
                        active_pattern_result_2: dict[str, Any] | None = _007CSequenceMinusOpener_007C__007C(head(restlist))
                        if active_pattern_result_2 is not None:
                            if not is_empty(tail(restlist)):
                                if head(tail(restlist)).tag == 1:
                                    pattern_matching_result_1 = 1
                                    rest0_2 = tail(tail(restlist))
                                    v_2 = active_pattern_result_2
                                    yaml_ast_list_1 = head(tail(restlist)).fields[0]

                                else: 
                                    pattern_matching_result_1 = 2


                            else: 
                                pattern_matching_result_1 = 2


                        else: 
                            pattern_matching_result_1 = 2



                else: 
                    pattern_matching_result_1 = 2

                if pattern_matching_result_1 == 0:
                    def _arrow394(e_2: PreprocessorElement, restlist: Any=restlist, acc: Any=acc) -> bool:
                        return is_sequence_element(e_2)

                    sequence_elements_1: FSharpList[FSharpList[PreprocessorElement]] = collect_sequence_elements(to_list(take_while(_arrow394, rest0_1)))
                    def _arrow395(e_3: PreprocessorElement, restlist: Any=restlist, acc: Any=acc) -> bool:
                        return is_sequence_element(e_3)

                    restlist_mut = to_list(skip_while(_arrow395, rest0_1))
                    def _arrow401(__unit: None=None, restlist: Any=restlist, acc: Any=acc) -> IEnumerable_1[YAMLElement]:
                        def _arrow400(__unit: None=None) -> IEnumerable_1[YAMLElement]:
                            def _arrow399(i_1: FSharpList[PreprocessorElement]) -> YAMLElement:
                                return loop_read(i_1, empty())

                            return map_1(_arrow399, sequence_elements_1)

                        return append(singleton(loop_read(singleton_1(PreprocessorElement(2, v_1["Key"])), empty())), delay(_arrow400))

                    acc_mut = cons(YAMLElement(2, to_list(delay(_arrow401))), acc)
                    continue

                elif pattern_matching_result_1 == 1:
                    object_list_1: FSharpList[PreprocessorElement] = cons(PreprocessorElement(2, value_2(v_2["Value"])), yaml_ast_list_1) if (v_2["Value"] is not None) else yaml_ast_list_1
                    def _arrow402(e_4: PreprocessorElement, restlist: Any=restlist, acc: Any=acc) -> bool:
                        return is_sequence_element(e_4)

                    sequence_elements_2: FSharpList[FSharpList[PreprocessorElement]] = collect_sequence_elements(to_list(take_while(_arrow402, rest0_2)))
                    def _arrow403(e_5: PreprocessorElement, restlist: Any=restlist, acc: Any=acc) -> bool:
                        return is_sequence_element(e_5)

                    restlist_mut = to_list(skip_while(_arrow403, rest0_2))
                    def _arrow409(__unit: None=None, restlist: Any=restlist, acc: Any=acc) -> IEnumerable_1[YAMLElement]:
                        def _arrow408(__unit: None=None) -> IEnumerable_1[YAMLElement]:
                            def _arrow407(i_2: FSharpList[PreprocessorElement]) -> YAMLElement:
                                return loop_read(i_2, empty())

                            return map_1(_arrow407, sequence_elements_2)

                        return append(singleton(loop_read(object_list_1, empty())), delay(_arrow408))

                    acc_mut = cons(YAMLElement(2, to_list(delay(_arrow409))), acc)
                    continue

                elif pattern_matching_result_1 == 2:
                    (pattern_matching_result_2, rest0_3, v_3, rest_4, v_4, closer, i_list, opener, rest_5) = (None, None, None, None, None, None, None, None, None)
                    if not is_empty(restlist):
                        active_pattern_result_3: dict[str, Any] | None = _007CSequenceMinusOpener_007C__007C(head(restlist))
                        if active_pattern_result_3 is not None:
                            pattern_matching_result_2 = 0
                            rest0_3 = tail(restlist)
                            v_3 = active_pattern_result_3

                        else: 
                            active_pattern_result_4: dict[str, Any] | None = _007CInlineSequence_007C__007C(head(restlist))
                            if active_pattern_result_4 is not None:
                                pattern_matching_result_2 = 1
                                rest_4 = tail(restlist)
                                v_4 = active_pattern_result_4

                            else: 
                                active_pattern_result_5: dict[str, Any] | None = _007CSequenceSquareOpener_007C__007C(head(restlist))
                                if active_pattern_result_5 is not None:
                                    if not is_empty(tail(restlist)):
                                        if head(tail(restlist)).tag == 1:
                                            if not is_empty(tail(tail(restlist))):
                                                active_pattern_result_6: dict[str, Any] | None = _007CSequenceSquareCloser_007C__007C(head(tail(tail(restlist))))
                                                if active_pattern_result_6 is not None:
                                                    pattern_matching_result_2 = 2
                                                    closer = active_pattern_result_6
                                                    i_list = head(tail(restlist)).fields[0]
                                                    opener = active_pattern_result_5
                                                    rest_5 = tail(tail(tail(restlist)))

                                                else: 
                                                    pattern_matching_result_2 = 3


                                            else: 
                                                pattern_matching_result_2 = 3


                                        else: 
                                            pattern_matching_result_2 = 3


                                    else: 
                                        pattern_matching_result_2 = 3


                                else: 
                                    pattern_matching_result_2 = 3




                    else: 
                        pattern_matching_result_2 = 3

                    if pattern_matching_result_2 == 0:
                        def _arrow410(e_6: PreprocessorElement, restlist: Any=restlist, acc: Any=acc) -> bool:
                            return is_sequence_element(e_6)

                        sequence_elements_3: FSharpList[FSharpList[PreprocessorElement]] = collect_sequence_elements(to_list(take_while(_arrow410, rest0_3)))
                        def _arrow411(e_7: PreprocessorElement, restlist: Any=restlist, acc: Any=acc) -> bool:
                            return is_sequence_element(e_7)

                        restlist_mut = to_list(skip_while(_arrow411, rest0_3))
                        def _arrow417(__unit: None=None, restlist: Any=restlist, acc: Any=acc) -> IEnumerable_1[YAMLElement]:
                            def _arrow416(__unit: None=None) -> IEnumerable_1[YAMLElement]:
                                def _arrow415(i_3: FSharpList[PreprocessorElement]) -> YAMLElement:
                                    return loop_read(i_3, empty())

                                return map_1(_arrow415, sequence_elements_3)

                            return append(singleton(loop_read(singleton_1(PreprocessorElement(2, value_2(v_3["Value"]))), empty())), delay(_arrow416))

                        acc_mut = cons(YAMLElement(2, to_list(delay(_arrow417))), acc)
                        continue

                    elif pattern_matching_result_2 == 1:
                        c: str | None = restore_comment_replace(comment_dict, v_4["Comment"])
                        split: Array[str] = split_2(v_4["Value"], [","], None, 1)
                        def _arrow419(__unit: None=None, restlist: Any=restlist, acc: Any=acc) -> IEnumerable_1[YAMLElement]:
                            def _arrow418(value: str) -> YAMLElement:
                                return loop_read(singleton_1(PreprocessorElement(2, value.strip())), empty())

                            return map_1(_arrow418, split)

                        current_4: YAMLElement = YAMLElement(2, to_list(delay(_arrow419)))
                        restlist_mut = rest_4
                        acc_mut = of_array_with_tail([current_4, YAMLElement(4, value_2(c))], acc) if (c is not None) else cons(current_4, acc)
                        continue

                    elif pattern_matching_result_2 == 2:
                        c1: str | None = restore_comment_replace(comment_dict, opener["Comment"])
                        c2: str | None = restore_comment_replace(comment_dict, closer["Comment"])
                        def _arrow421(__unit: None=None, restlist: Any=restlist, acc: Any=acc) -> IEnumerable_1[YAMLElement]:
                            def _arrow420(i_4: PreprocessorElement) -> IEnumerable_1[YAMLElement]:
                                return singleton(loop_read(singleton_1(PreprocessorElement(2, trim_end(i_4.fields[0], ",")) if (i_4.tag == 2) else to_fail(printf("Unexpected element in MultiLineSquareBrackets: %A"))(i_4)), empty()))

                            return collect(_arrow420, i_list)

                        current_5: YAMLElement = YAMLElement(2, to_list(delay(_arrow421)))
                        restlist_mut = rest_5
                        def _arrow422(__unit: None=None, restlist: Any=restlist, acc: Any=acc) -> FSharpList[YAMLElement]:
                            c2_2: str = c2
                            return of_array_with_tail([YAMLElement(4, c2_2), current_5], acc)

                        def _arrow423(__unit: None=None, restlist: Any=restlist, acc: Any=acc) -> FSharpList[YAMLElement]:
                            c1_2: str = c1
                            return of_array_with_tail([current_5, YAMLElement(4, c1_2)], acc)

                        def _arrow424(__unit: None=None, restlist: Any=restlist, acc: Any=acc) -> FSharpList[YAMLElement]:
                            c1_1: str = c1
                            c2_1: str = c2
                            return of_array_with_tail([YAMLElement(4, c2_1), current_5, YAMLElement(4, c1_1)], acc)

                        acc_mut = (cons(current_5, acc) if (c2 is None) else _arrow422()) if (c1 is None) else (_arrow423() if (c2 is None) else _arrow424())
                        continue

                    elif pattern_matching_result_2 == 3:
                        (pattern_matching_result_3, rest_6, v_5, closer_1, i_list_1, opener_1, rest_7) = (None, None, None, None, None, None, None)
                        if not is_empty(restlist):
                            active_pattern_result_7: dict[str, Any] | None = _007CInlineJSON_007C__007C(head(restlist))
                            if active_pattern_result_7 is not None:
                                pattern_matching_result_3 = 0
                                rest_6 = tail(restlist)
                                v_5 = active_pattern_result_7

                            else: 
                                active_pattern_result_8: dict[str, Any] | None = _007CJSONKeyOpener_007C__007C(head(restlist))
                                if active_pattern_result_8 is not None:
                                    if not is_empty(tail(restlist)):
                                        if head(tail(restlist)).tag == 1:
                                            if not is_empty(tail(tail(restlist))):
                                                active_pattern_result_9: dict[str, Any] | None = _007CJSONCloser_007C__007C(head(tail(tail(restlist))))
                                                if active_pattern_result_9 is not None:
                                                    pattern_matching_result_3 = 1
                                                    closer_1 = active_pattern_result_9
                                                    i_list_1 = head(tail(restlist)).fields[0]
                                                    opener_1 = active_pattern_result_8
                                                    rest_7 = tail(tail(tail(restlist)))

                                                else: 
                                                    pattern_matching_result_3 = 2


                                            else: 
                                                pattern_matching_result_3 = 2


                                        else: 
                                            pattern_matching_result_3 = 2


                                    else: 
                                        pattern_matching_result_3 = 2


                                else: 
                                    pattern_matching_result_3 = 2



                        else: 
                            pattern_matching_result_3 = 2

                        if pattern_matching_result_3 == 0:
                            c_1: str | None = restore_comment_replace(comment_dict, v_5["Comment"])
                            split_1: Array[str] = split_2(v_5["Value"], [","], None, 1)
                            def _arrow426(__unit: None=None, restlist: Any=restlist, acc: Any=acc) -> IEnumerable_1[YAMLElement]:
                                def _arrow425(value_1: str) -> IEnumerable_1[YAMLElement]:
                                    match_value_1: YAMLElement = loop_read(singleton_1(PreprocessorElement(2, value_1.strip())), empty())
                                    if match_value_1.tag == 3:
                                        return match_value_1.fields[0]

                                    else: 
                                        raise Exception("Unexpected element in InlineJSON")
                                        return empty_1()


                                return collect(_arrow425, split_1)

                            current_6: FSharpList[YAMLElement] = reverse(to_list(delay(_arrow426)))
                            restlist_mut = rest_6
                            acc_mut = append_1(current_6, cons(YAMLElement(4, value_2(c_1)), acc)) if (c_1 is not None) else append_1(current_6, acc)
                            continue

                        elif pattern_matching_result_3 == 1:
                            c1_3: str | None = restore_comment_replace(comment_dict, opener_1["Comment"])
                            c2_3: str | None = restore_comment_replace(comment_dict, closer_1["Comment"])
                            def _arrow428(__unit: None=None, restlist: Any=restlist, acc: Any=acc) -> IEnumerable_1[YAMLElement]:
                                def _arrow427(i_5: PreprocessorElement) -> IEnumerable_1[YAMLElement]:
                                    match_value_2: YAMLElement = loop_read(singleton_1(PreprocessorElement(2, trim_end(i_5.fields[0], ",")) if (i_5.tag == 2) else to_fail(printf("Unexpected element in MultiLineSquareBrackets: %A"))(i_5)), empty())
                                    if match_value_2.tag == 3:
                                        return match_value_2.fields[0]

                                    else: 
                                        raise Exception("Unexpected element in MultilineJSON")
                                        return empty_1()


                                return collect(_arrow427, i_list_1)

                            current_7: YAMLElement = YAMLElement(0, YAMLContent_create_27AED5E3(opener_1["Key"], c1_3), YAMLElement(3, to_list(delay(_arrow428))))
                            restlist_mut = rest_7
                            acc_mut = cons(current_7, acc) if (c2_3 is None) else of_array_with_tail([YAMLElement(4, c2_3), current_7], acc)
                            continue

                        elif pattern_matching_result_3 == 2:
                            (pattern_matching_result_4, rest_8, v_6, yaml_ast_list_2) = (None, None, None, None)
                            if not is_empty(restlist):
                                active_pattern_result_10: dict[str, Any] | None = _007CKey_007C__007C(head(restlist))
                                if active_pattern_result_10 is not None:
                                    if not is_empty(tail(restlist)):
                                        if head(tail(restlist)).tag == 1:
                                            pattern_matching_result_4 = 0
                                            rest_8 = tail(tail(restlist))
                                            v_6 = active_pattern_result_10
                                            yaml_ast_list_2 = head(tail(restlist)).fields[0]

                                        else: 
                                            pattern_matching_result_4 = 1


                                    else: 
                                        pattern_matching_result_4 = 1


                                else: 
                                    pattern_matching_result_4 = 1


                            else: 
                                pattern_matching_result_4 = 1

                            if pattern_matching_result_4 == 0:
                                restlist_mut = rest_8
                                acc_mut = cons(YAMLElement(0, YAMLContent_create_27AED5E3(v_6["Key"], restore_comment_replace(comment_dict, v_6["Comment"])), loop_read(yaml_ast_list_2, empty())), acc)
                                continue

                            elif pattern_matching_result_4 == 1:
                                (pattern_matching_result_5, rest0_4, v_7, w, yaml_ast_list_3) = (None, None, None, None, None)
                                if not is_empty(restlist):
                                    active_pattern_result_11: dict[str, Any] | None = _007CKey_007C__007C(head(restlist))
                                    if active_pattern_result_11 is not None:
                                        if not is_empty(tail(restlist)):
                                            active_pattern_result_12: dict[str, Any] | None = _007CSequenceMinusOpener_007C__007C(head(tail(restlist)))
                                            if active_pattern_result_12 is not None:
                                                if not is_empty(tail(tail(restlist))):
                                                    if head(tail(tail(restlist))).tag == 1:
                                                        pattern_matching_result_5 = 0
                                                        rest0_4 = tail(tail(tail(restlist)))
                                                        v_7 = active_pattern_result_11
                                                        w = active_pattern_result_12
                                                        yaml_ast_list_3 = head(tail(tail(restlist))).fields[0]

                                                    else: 
                                                        pattern_matching_result_5 = 1


                                                else: 
                                                    pattern_matching_result_5 = 1


                                            else: 
                                                pattern_matching_result_5 = 1


                                        else: 
                                            pattern_matching_result_5 = 1


                                    else: 
                                        pattern_matching_result_5 = 1


                                else: 
                                    pattern_matching_result_5 = 1

                                if pattern_matching_result_5 == 0:
                                    c_3: str | None = restore_comment_replace(comment_dict, v_7["Comment"])
                                    object_list_2: FSharpList[PreprocessorElement] = cons(PreprocessorElement(2, value_2(w["Value"])), yaml_ast_list_3) if (w["Value"] is not None) else yaml_ast_list_3
                                    def _arrow429(e_8: PreprocessorElement, restlist: Any=restlist, acc: Any=acc) -> bool:
                                        return is_sequence_element(e_8)

                                    sequence_elements_4: FSharpList[FSharpList[PreprocessorElement]] = collect_sequence_elements(to_list(take_while(_arrow429, rest0_4)))
                                    def _arrow430(e_9: PreprocessorElement, restlist: Any=restlist, acc: Any=acc) -> bool:
                                        return is_sequence_element(e_9)

                                    rest_9: FSharpList[PreprocessorElement] = to_list(skip_while(_arrow430, rest0_4))
                                    def _arrow433(__unit: None=None, restlist: Any=restlist, acc: Any=acc) -> IEnumerable_1[YAMLElement]:
                                        def _arrow432(__unit: None=None) -> IEnumerable_1[YAMLElement]:
                                            def _arrow431(i_6: FSharpList[PreprocessorElement]) -> YAMLElement:
                                                return loop_read(i_6, empty())

                                            return map_1(_arrow431, sequence_elements_4)

                                        return append(singleton(loop_read(object_list_2, empty())), delay(_arrow432))

                                    seq: YAMLElement = YAMLElement(2, to_list(delay(_arrow433)))
                                    restlist_mut = rest_9
                                    acc_mut = cons(YAMLElement(0, YAMLContent_create_27AED5E3(v_7["Key"], c_3), YAMLElement(3, singleton_1(seq))), acc)
                                    continue

                                elif pattern_matching_result_5 == 1:
                                    (pattern_matching_result_6, rest0_5, v_8, w_1) = (None, None, None, None)
                                    if not is_empty(restlist):
                                        active_pattern_result_13: dict[str, Any] | None = _007CKey_007C__007C(head(restlist))
                                        if active_pattern_result_13 is not None:
                                            if not is_empty(tail(restlist)):
                                                active_pattern_result_14: dict[str, Any] | None = _007CSequenceMinusOpener_007C__007C(head(tail(restlist)))
                                                if active_pattern_result_14 is not None:
                                                    pattern_matching_result_6 = 0
                                                    rest0_5 = tail(tail(restlist))
                                                    v_8 = active_pattern_result_13
                                                    w_1 = active_pattern_result_14

                                                else: 
                                                    pattern_matching_result_6 = 1


                                            else: 
                                                pattern_matching_result_6 = 1


                                        else: 
                                            pattern_matching_result_6 = 1


                                    else: 
                                        pattern_matching_result_6 = 1

                                    if pattern_matching_result_6 == 0:
                                        c_4: str | None = restore_comment_replace(comment_dict, v_8["Comment"])
                                        def _arrow434(e_10: PreprocessorElement, restlist: Any=restlist, acc: Any=acc) -> bool:
                                            return is_sequence_element(e_10)

                                        sequence_elements_5: FSharpList[FSharpList[PreprocessorElement]] = collect_sequence_elements(to_list(take_while(_arrow434, rest0_5)))
                                        def _arrow435(e_11: PreprocessorElement, restlist: Any=restlist, acc: Any=acc) -> bool:
                                            return is_sequence_element(e_11)

                                        rest_10: FSharpList[PreprocessorElement] = to_list(skip_while(_arrow435, rest0_5))
                                        def _arrow438(__unit: None=None, restlist: Any=restlist, acc: Any=acc) -> IEnumerable_1[YAMLElement]:
                                            def _arrow437(__unit: None=None) -> IEnumerable_1[YAMLElement]:
                                                def _arrow436(i_7: FSharpList[PreprocessorElement]) -> YAMLElement:
                                                    return loop_read(i_7, empty())

                                                return map_1(_arrow436, sequence_elements_5)

                                            return append(singleton(loop_read(singleton_1(PreprocessorElement(2, value_2(w_1["Value"]))), empty())), delay(_arrow437))

                                        seq_1: YAMLElement = YAMLElement(2, to_list(delay(_arrow438)))
                                        restlist_mut = rest_10
                                        acc_mut = cons(YAMLElement(0, YAMLContent_create_27AED5E3(v_8["Key"], c_4), YAMLElement(3, singleton_1(seq_1))), acc)
                                        continue

                                    elif pattern_matching_result_6 == 1:
                                        if is_empty(restlist):
                                            return YAMLElement(3, reverse(acc))

                                        else: 
                                            active_pattern_result_15: dict[str, Any] | None = _007CKeyValue_007C__007C(head(restlist))
                                            if active_pattern_result_15 is not None:
                                                v_9: dict[str, Any] = active_pattern_result_15
                                                restlist_mut = tail(restlist)
                                                acc_mut = cons(YAMLElement(0, YAMLContent_create_27AED5E3(v_9["Key"]), loop_read(singleton_1(PreprocessorElement(2, v_9["Value"])), empty())), acc)
                                                continue

                                            else: 
                                                active_pattern_result_16: dict[str, Any] | None = _007CYamlComment_007C__007C(head(restlist))
                                                if active_pattern_result_16 is not None:
                                                    v_10: dict[str, Any] = active_pattern_result_16
                                                    restlist_mut = tail(restlist)
                                                    acc_mut = cons(YAMLElement(4, get_item_from_dict(comment_dict, v_10["Comment"])), acc)
                                                    continue

                                                else: 
                                                    active_pattern_result_17: dict[str, Any] | None = _007CYamlValue_007C__007C(head(restlist))
                                                    if active_pattern_result_17 is not None:
                                                        v_11: dict[str, Any] = active_pattern_result_17
                                                        restlist_mut = tail(restlist)
                                                        acc_mut = cons(YAMLElement(1, YAMLContent_create_27AED5E3(restore_string_replace(string_dict, v_11["Value"]), restore_comment_replace(comment_dict, v_11["Comment"]))), acc)
                                                        continue

                                                    else: 
                                                        return to_fail(printf("Unknown pattern: %A"))(restlist)











            break

    return loop_read(yaml_list, empty())


def read(yaml: str) -> YAMLElement:
    ast: Preprocessor = read_1(yaml)
    match_value: PreprocessorElement = ast.AST
    if match_value.tag == 0:
        return tokenize(match_value.fields[0], ast.StringMap, ast.CommentMap)

    else: 
        raise Exception("Not a root!")



__all__ = ["restore_string_replace", "restore_comment_replace", "collect_sequence_elements", "is_sequence_element", "tokenize", "read"]

