from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_library.list import (FSharpList, is_empty, tail, head, of_seq as of_seq_1, empty, cons, reverse)
from ..fable_library.option import value as value_1
from ..fable_library.range import range_big_int
from ..fable_library.seq import (to_list, delay, map)
from ..fable_library.string_ import (join, to_console, printf)
from ..fable_library.types import Array
from ..fable_library.util import (IEnumerable_1, get_enumerator, ignore)
from .dynamic_obj import (DynamicObj, CopyUtils_tryDeepCopyObj_75B3D832)
from .property_helper import PropertyHelper

_TPROPERTYVALUE = TypeVar("_TPROPERTYVALUE")

_UPROPERTYVALUE = TypeVar("_UPROPERTYVALUE")

def of_dict(dynamic_properties: Any) -> DynamicObj:
    return DynamicObj.of_dict(dynamic_properties)


def of_seq(dynamic_properties: IEnumerable_1[tuple[str, Any]]) -> DynamicObj:
    dynamic_properties_1: Any = dict(dict(dynamic_properties))
    return DynamicObj.of_dict(dynamic_properties_1)


def of_list(dynamic_properties: FSharpList[tuple[str, Any]]) -> DynamicObj:
    return of_seq(dynamic_properties)


def of_array(dynamic_properties: Array[tuple[str, Any]]) -> DynamicObj:
    return of_seq(dynamic_properties)


def combine(first: DynamicObj, second: DynamicObj) -> DynamicObj:
    with get_enumerator(second.GetProperties(True)) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            kv: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            match_value: Any = kv[1]
            if isinstance(match_value, DynamicObj):
                match_value_1: Any | None = first.TryGetPropertyValue(kv[0])
                if match_value_1 is None:
                    first.SetProperty(kv[0], match_value)

                else: 
                    tmp: DynamicObj = combine(value_1(match_value_1), match_value)
                    first.SetProperty(kv[0], tmp)


            else: 
                first.SetProperty(kv[0], kv[1])

    return first


def set_property(property_name: str, property_value: Any, dyn_obj: DynamicObj) -> None:
    dyn_obj.SetProperty(property_name, property_value)


def set_optional_property(property_name: str, property_value: Any | None, dyn_obj: DynamicObj) -> None:
    if property_value is None:
        pass

    else: 
        set_property(property_name, value_1(property_value), dyn_obj)



def set_optional_property_by(property_name: str, property_value: Any | None, mapping: Callable[[_TPROPERTYVALUE], _UPROPERTYVALUE], dyn_obj: DynamicObj) -> None:
    if property_value is None:
        pass

    else: 
        set_property(property_name, mapping(value_1(property_value)), dyn_obj)



def try_get_property_value(property_name: str, dyn_obj: DynamicObj) -> Any | None:
    return dyn_obj.TryGetPropertyValue(property_name)


def remove_property(property_name: str, dyn_obj: DynamicObj) -> None:
    ignore(dyn_obj.RemoveProperty(property_name))


def format(dyn_obj: DynamicObj) -> str:
    def loop(object_mut: DynamicObj, indentation_level_mut: int, members_left_mut: FSharpList[PropertyHelper], acc_mut: FSharpList[str], dyn_obj: Any=dyn_obj) -> str:
        while True:
            (object, indentation_level, members_left, acc) = (object_mut, indentation_level_mut, members_left_mut, acc_mut)
            def _arrow24(__unit: None=None, object: Any=object, indentation_level: Any=indentation_level, members_left: Any=members_left, acc: Any=acc) -> IEnumerable_1[str]:
                def _arrow23(i: int) -> str:
                    return "    "

                return map(_arrow23, range_big_int(0, 1, indentation_level - 1))

            indent: str = join("", to_list(delay(_arrow24)))
            if not is_empty(members_left):
                rest: FSharpList[PropertyHelper] = tail(members_left)
                m: PropertyHelper = head(members_left)
                item: Any = m.GetValue(object)
                dynamic_indicator: str = "?" if m.IsDynamic else ""
                name: str = m.Name
                if isinstance(item, DynamicObj):
                    object_mut = object
                    indentation_level_mut = indentation_level
                    members_left_mut = rest
                    acc_mut = cons(((((((((("" + indent) + "") + dynamic_indicator) + "") + name) + ":") + "\n") + "") + loop(item, indentation_level + 1, of_seq_1(item.GetPropertyHelpers(True)), empty())) + "", acc)
                    continue

                else: 
                    object_mut = object
                    indentation_level_mut = indentation_level
                    members_left_mut = rest
                    acc_mut = cons(((((((("" + indent) + "") + dynamic_indicator) + "") + name) + ": ") + str(item)) + "", acc)
                    continue


            else: 
                return join("\n", reverse(acc))

            break

    return loop(dyn_obj, 0, of_seq_1(dyn_obj.GetPropertyHelpers(True)), empty())


def print(dyn_obj: DynamicObj) -> None:
    arg: str = format(dyn_obj)
    to_console(printf("%s"))(arg)


def try_deep_copy_obj(include_instance_properties: bool, o: DynamicObj) -> Any:
    return CopyUtils_tryDeepCopyObj_75B3D832(o, include_instance_properties)


__all__ = ["of_dict", "of_seq", "of_list", "of_array", "combine", "set_property", "set_optional_property", "set_optional_property_by", "try_get_property_value", "remove_property", "format", "print", "try_deep_copy_obj"]

