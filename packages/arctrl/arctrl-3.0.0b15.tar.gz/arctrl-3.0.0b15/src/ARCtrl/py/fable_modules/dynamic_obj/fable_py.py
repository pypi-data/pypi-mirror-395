from __future__ import annotations
from abc import abstractmethod
from collections.abc import Callable
from typing import (Any, Protocol, TypeVar)
from ..fable_library.array_ import (append, map as map_1)
from ..fable_library.map_util import add_to_dict
from ..fable_library.mutable_map import Dictionary
from ..fable_library.option import value as value_1
from ..fable_library.reg_exp import (is_match, create)
from ..fable_library.seq import (iterate, to_array, choose, map)
from ..fable_library.types import Array
from ..fable_library.util import (equals, structural_hash, IEnumerable_1, get_enumerator, dispose)
from .property_helper import PropertyHelper

__A_ = TypeVar("__A_")

_U = TypeVar("_U")

_T = TypeVar("_T")

def Dictionary_ofSeq(s: IEnumerable_1[Any]) -> Any:
    class ObjectExpr3:
        @property
        def Equals(self) -> Callable[[__A_, __A_], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[__A_], int]:
            return structural_hash

    d: Any = Dictionary([], ObjectExpr3())
    def action(kv: Any, s: Any=s) -> None:
        add_to_dict(d, kv[0], kv[1])

    iterate(action, s)
    return d


def Dictionary_choose(f: Callable[[_T], _U | None], d: Any) -> Any:
    class ObjectExpr4:
        @property
        def Equals(self) -> Callable[[__A_, __A_], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[__A_], int]:
            return structural_hash

    nd: Any = Dictionary([], ObjectExpr4())
    enumerator: Any = get_enumerator(d)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            kv: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            match_value: _U | None = f(kv[1])
            if match_value is None:
                pass

            else: 
                add_to_dict(nd, kv[0], value_1(match_value))


    finally: 
        dispose(enumerator)

    return nd


class PropertyObject(Protocol):
    @property
    @abstractmethod
    def fget(self) -> Any:
        ...

    @property
    @abstractmethod
    def fset(self) -> Any:
        ...


def PropertyObjectModule_getGetter(o: PropertyObject) -> Callable[[Any], Any]:
    match_value: Callable[[Any], Any] | None = o.fget
    if match_value is None:
        def _arrow5(o_1: Any=None, o: Any=o) -> Any:
            raise Exception("Property does not contain getter")

        return _arrow5

    else: 
        return match_value



def PropertyObjectModule_getSetter(o: PropertyObject) -> Callable[[Any, Any], None]:
    match_value: Callable[[Any, Any], None] | None = o.fset
    if match_value is None:
        def _arrow7(s: Any=None, o: Any=o) -> Callable[[Any], None]:
            def _arrow6(o_1: Any=None) -> None:
                raise Exception("Property does not contain setter")

            return _arrow6

        return _arrow7

    else: 
        return match_value



def PropertyObjectModule_containsGetter(o: PropertyObject) -> bool:
    match_value: Callable[[Any], Any] | None = o.fget
    if match_value is None:
        return False

    else: 
        return True



def PropertyObjectModule_containsSetter(o: PropertyObject) -> bool:
    match_value: Callable[[Any, Any], None] | None = o.fset
    if match_value is None:
        return False

    else: 
        return True



def PropertyObjectModule_isWritable(o: PropertyObject) -> bool:
    return PropertyObjectModule_containsSetter(o)


def PropertyObjectModule_tryProperty(o: Any=None) -> PropertyObject | None:
    if isinstance(o, property):
        return o

    else: 
        return None



def create_getter(prop_name: str, o: Any=None) -> Any:
    return getattr(o,prop_name)


def create_setter(prop_name: str, o: Any=None, value: Any=None) -> None:
    setattr(o,prop_name,value)


def get_static_property_objects(o: Any=None) -> Any:
    def f(o_2: Any=None, o: Any=o) -> PropertyObject | None:
        return PropertyObjectModule_tryProperty(o_2)

    def _arrow8(__unit: None=None, o: Any=o) -> Any:
        o_1: Any = o.__class__
        return vars(o_1).items()

    return Dictionary_choose(f, _arrow8())


def remove_static_property_value(o: Any, prop_name: str) -> None:
    setattr(o,prop_name,None)


def create_remover(prop_name: str, is_static: bool) -> Callable[[Any], None]:
    if is_static:
        def _arrow9(o: Any=None, prop_name: Any=prop_name, is_static: Any=is_static) -> None:
            remove_static_property_value(o, prop_name)

        return _arrow9

    else: 
        def _arrow10(o_1: Any=None, prop_name: Any=prop_name, is_static: Any=is_static) -> None:
            delattr(o_1,prop_name)

        return _arrow10



def try_get_property_object(o: Any, prop_name: str) -> PropertyObject | None:
    match_value: PropertyObject | None = PropertyObjectModule_tryProperty(o.__dict__.get(prop_name))
    if match_value is None:
        return None

    else: 
        return match_value



def try_get_dynamic_property_helper(o: Any, prop_name: str) -> PropertyHelper | None:
    match_value: Any | None = o.__dict__.get(prop_name)
    if match_value is None:
        return None

    else: 
        def _arrow11(o_1: Any=None, o: Any=o, prop_name: Any=prop_name) -> Any:
            return create_getter(prop_name, o_1)

        def _arrow12(o_2: Any=None, value: Any=None, o: Any=o, prop_name: Any=prop_name) -> None:
            create_setter(prop_name, o_2, value)

        def _arrow13(o_3: Any=None, o: Any=o, prop_name: Any=prop_name) -> None:
            delattr(o_3,prop_name)

        return PropertyHelper(prop_name, False, True, True, False, _arrow11, _arrow12, _arrow13)



def try_get_static_property_helper(o: Any, prop_name: str) -> PropertyHelper | None:
    match_value: PropertyObject | None = try_get_property_object(o.__class__, prop_name)
    if match_value is None:
        return None

    else: 
        is_writable: bool = PropertyObjectModule_isWritable(match_value)
        def _arrow14(o_1: Any=None, o: Any=o, prop_name: Any=prop_name) -> Any:
            return create_getter(prop_name, o_1)

        def _arrow15(o_2: Any=None, value: Any=None, o: Any=o, prop_name: Any=prop_name) -> None:
            create_setter(prop_name, o_2, value)

        def _arrow16(o_3: Any=None, o: Any=o, prop_name: Any=prop_name) -> None:
            remove_static_property_value(o_3, prop_name)

        return PropertyHelper(prop_name, True, False, is_writable, not is_writable, _arrow14, _arrow15, _arrow16)



transpiled_property_regex: str = "^([a-zA-Z]+_)+[0-9]+$"

def is_transpiled_property_helper(property_name: str) -> bool:
    return is_match(create(transpiled_property_regex), property_name)


def get_dynamic_property_helpers(o: Any=None) -> Array[PropertyHelper]:
    def chooser(kv: Any, o: Any=o) -> PropertyHelper | None:
        n: str = kv[0]
        if is_transpiled_property_helper(n):
            return None

        else: 
            def _arrow17(o_1: Any=None, kv: Any=kv) -> Any:
                return create_getter(n, o_1)

            def _arrow18(o_2: Any=None, value: Any=None, kv: Any=kv) -> None:
                create_setter(n, o_2, value)

            def _arrow19(o_3: Any=None, kv: Any=kv) -> None:
                delattr(o_3,n)

            return PropertyHelper(n, False, True, True, False, _arrow17, _arrow18, _arrow19)


    return to_array(choose(chooser, vars(o).items()))


def get_static_property_helpers(o: Any=None) -> Array[PropertyHelper]:
    def mapping(kv: Any, o: Any=o) -> PropertyHelper:
        n: str = kv[0]
        po: PropertyObject = kv[1]
        def _arrow20(o_1: Any=None, kv: Any=kv) -> Any:
            return create_getter(n, o_1)

        def _arrow21(o_2: Any=None, value: Any=None, kv: Any=kv) -> None:
            create_setter(n, o_2, value)

        def _arrow22(o_3: Any=None, kv: Any=kv) -> None:
            remove_static_property_value(o_3, n)

        return PropertyHelper(n, True, False, PropertyObjectModule_isWritable(po), not PropertyObjectModule_isWritable(po), _arrow20, _arrow21, _arrow22)

    return to_array(map(mapping, get_static_property_objects(o)))


def get_property_helpers(o: Any=None) -> Array[PropertyHelper]:
    array_1: Array[PropertyHelper] = get_dynamic_property_helpers(o)
    return append(get_static_property_helpers(o), array_1, None)


def get_property_names(o: Any=None) -> Array[str]:
    def mapping(h: PropertyHelper, o: Any=o) -> str:
        return h.Name

    return map_1(mapping, get_property_helpers(o), None)


__all__ = ["Dictionary_ofSeq", "Dictionary_choose", "PropertyObjectModule_getGetter", "PropertyObjectModule_getSetter", "PropertyObjectModule_containsGetter", "PropertyObjectModule_containsSetter", "PropertyObjectModule_isWritable", "PropertyObjectModule_tryProperty", "create_getter", "create_setter", "get_static_property_objects", "remove_static_property_value", "create_remover", "try_get_property_object", "try_get_dynamic_property_helper", "try_get_static_property_helper", "transpiled_property_regex", "is_transpiled_property_helper", "get_dynamic_property_helpers", "get_static_property_helpers", "get_property_helpers", "get_property_names"]

