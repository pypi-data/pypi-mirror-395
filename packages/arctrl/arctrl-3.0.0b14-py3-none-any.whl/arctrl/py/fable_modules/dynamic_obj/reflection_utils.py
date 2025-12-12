from __future__ import annotations
from typing import Any
from ..fable_library.option import (some, map)
from ..fable_library.types import Array
from .fable_py import (get_static_property_helpers, try_get_static_property_helper)
from .property_helper import PropertyHelper

def get_static_properties(o: Any=None) -> Array[PropertyHelper]:
    return get_static_property_helpers(o)


def try_get_static_property_info(o: Any, prop_name: str) -> PropertyHelper | None:
    return try_get_static_property_helper(o, prop_name)


def try_set_property_value(o: Any, prop_name: str, value: Any=None) -> bool:
    match_value: PropertyHelper | None = try_get_static_property_info(o, prop_name)
    (pattern_matching_result, property_1) = (None, None)
    if match_value is not None:
        if match_value.IsMutable:
            pattern_matching_result = 0
            property_1 = match_value

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        property_1.SetValue(o, value)
        return True

    elif pattern_matching_result == 1:
        return False



def try_get_property_value(o: Any, prop_name: str) -> Any | None:
    try: 
        match_value: PropertyHelper | None = try_get_static_property_info(o, prop_name)
        return None if (match_value is None) else some(match_value.GetValue(o))

    except Exception as match_value_1:
        return None



def try_get_property_value_as(o: Any, prop_name: str) -> Any | None:
    try: 
        def mapping(v: Any=None) -> Any:
            return v

        return map(mapping, try_get_property_value(o, prop_name))

    except Exception as match_value:
        return None



def remove_property(o: Any, prop_name: str) -> bool:
    match_value: PropertyHelper | None = try_get_static_property_info(o, prop_name)
    (pattern_matching_result, property_1) = (None, None)
    if match_value is not None:
        if match_value.IsMutable:
            pattern_matching_result = 0
            property_1 = match_value

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        property_1.RemoveValue(o)
        return True

    elif pattern_matching_result == 1:
        return False



__all__ = ["get_static_properties", "try_get_static_property_info", "try_set_property_value", "try_get_property_value", "try_get_property_value_as", "remove_property"]

