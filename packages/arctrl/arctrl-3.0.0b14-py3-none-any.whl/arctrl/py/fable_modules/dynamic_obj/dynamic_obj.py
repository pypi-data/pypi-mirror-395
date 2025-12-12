from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_library.list import (FSharpList, is_empty, reduce)
from ..fable_library.map_util import add_to_dict
from ..fable_library.mutable_map import Dictionary
from ..fable_library.option import (map, value as value_2, default_arg)
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_library.seq import (filter, choose, map as map_1, iterate, sort_by, to_list, delay, enumerate_while, singleton)
from ..fable_library.util import (IEnumerable_1, safe_hash, compare_primitives, is_iterable, get_enumerator, IEnumerator, equals, structural_hash, dispose, is_array_like)
from .fable_py import (try_get_dynamic_property_helper, get_property_helpers)
from .hash_codes import (box_hash_key_val_seq_by, hash_1 as hash_1_1, merge_hashes)
from .property_helper import PropertyHelper
from .reflection_utils import try_get_static_property_info

def _expr27() -> TypeInfo:
    return class_type("DynamicObj.DynamicObj", None, DynamicObj)


class DynamicObj:
    def __init__(self, __unit: None=None) -> None:
        self.properties: Any = dict([])

    @property
    def Properties(self, __unit: None=None) -> Any:
        this: DynamicObj = self
        return this.properties

    @Properties.setter
    def Properties(self, value: Any) -> None:
        this: DynamicObj = self
        this.properties = value

    @staticmethod
    def of_dict(dynamic_properties: Any) -> DynamicObj:
        obj: DynamicObj = DynamicObj()
        obj.Properties = dynamic_properties
        return obj

    def TryGetStaticPropertyHelper(self, property_name: str) -> PropertyHelper | None:
        this: DynamicObj = self
        return try_get_static_property_info(this, property_name)

    def TryGetDynamicPropertyHelper(self, property_name: str) -> PropertyHelper | None:
        this: DynamicObj = self
        return try_get_dynamic_property_helper(this, property_name)

    def TryGetPropertyHelper(self, property_name: str) -> PropertyHelper | None:
        this: DynamicObj = self
        match_value: PropertyHelper | None = this.TryGetStaticPropertyHelper(property_name)
        return this.TryGetDynamicPropertyHelper(property_name) if (match_value is None) else match_value

    def TryGetPropertyValue(self, property_name: str) -> Any | None:
        this: DynamicObj = self
        def mapping(pi: PropertyHelper) -> Any:
            return pi.GetValue(this)

        return map(mapping, this.TryGetPropertyHelper(property_name))

    def GetPropertyValue(self, property_name: str) -> Any:
        this: DynamicObj = self
        match_value: Any | None = this.TryGetPropertyValue(property_name)
        if match_value is None:
            raise Exception(("No dynamic or static property \"" + property_name) + "\" does exist on object.")

        else: 
            return value_2(match_value)


    def SetProperty(self, property_name: str, property_value: Any=None) -> None:
        this: DynamicObj = self
        match_value: PropertyHelper | None = this.TryGetStaticPropertyHelper(property_name)
        if match_value is None:
            setattr(this,property_name,property_value)

        else: 
            pi: PropertyHelper = match_value
            if pi.IsMutable:
                pi.SetValue(this, property_value)

            else: 
                raise Exception(("Cannot set value for static, immutable property \"" + property_name) + "\"")



    def RemoveProperty(self, property_name: str) -> bool:
        this: DynamicObj = self
        match_value: PropertyHelper | None = this.TryGetPropertyHelper(property_name)
        if match_value is None:
            return False

        elif match_value.IsMutable:
            pi_1: PropertyHelper = match_value
            pi_1.RemoveValue(this)
            return True

        else: 
            raise Exception(("Cannot remove value for static, immutable property \"" + property_name) + "\"")


    def GetPropertyHelpers(self, include_instance_properties: bool) -> IEnumerable_1[PropertyHelper]:
        this: DynamicObj = self
        def predicate_1(p: PropertyHelper) -> bool:
            return p.Name.lower() != "properties"

        def predicate(pd: PropertyHelper) -> bool:
            if include_instance_properties:
                return True

            else: 
                return pd.IsDynamic


        return filter(predicate_1, filter(predicate, get_property_helpers(this)))

    def GetProperties(self, include_instance_properties: bool) -> IEnumerable_1[Any]:
        this: DynamicObj = self
        def chooser(kv: PropertyHelper) -> Any | None:
            if kv.Name != "properties":
                return (kv.Name, kv.GetValue(this))

            else: 
                return None


        return choose(chooser, this.GetPropertyHelpers(include_instance_properties))

    def GetPropertyNames(self, include_instance_properties: bool) -> IEnumerable_1[str]:
        this: DynamicObj = self
        def mapping(kv: Any) -> str:
            return kv[0]

        return map_1(mapping, this.GetProperties(include_instance_properties))

    def ShallowCopyDynamicPropertiesTo(self, target: Any, over_write: bool | None=None) -> None:
        this: DynamicObj = self
        over_write_1: bool = default_arg(over_write, False)
        def action(kv: Any) -> None:
            match_value: PropertyHelper | None = target.TryGetPropertyHelper(kv[0])
            if match_value is None:
                target.SetProperty(kv[0], kv[1])

            else: 
                def _arrow25(__unit: None=None, kv: Any=kv) -> bool:
                    pi: PropertyHelper = match_value
                    return over_write_1

                if _arrow25():
                    pi_1: PropertyHelper = match_value
                    pi_1.SetValue(target, kv[1])



        iterate(action, this.GetProperties(False))

    def ShallowCopyDynamicProperties(self, __unit: None=None) -> DynamicObj:
        this: DynamicObj = self
        target: DynamicObj = DynamicObj()
        this.ShallowCopyDynamicPropertiesTo(target, True)
        return target

    def DeepCopyPropertiesTo(self, target: Any, over_write: bool | None=None, include_instance_properties: bool | None=None) -> None:
        this: DynamicObj = self
        over_write_1: bool = default_arg(over_write, False)
        include_instance_properties_1: bool = default_arg(include_instance_properties, True)
        def action(kv: Any) -> None:
            match_value: PropertyHelper | None = target.TryGetPropertyHelper(kv[0])
            if match_value is None:
                target.SetProperty(kv[0], CopyUtils_tryDeepCopyObj_75B3D832(kv[1]))

            else: 
                def _arrow26(__unit: None=None, kv: Any=kv) -> bool:
                    pi: PropertyHelper = match_value
                    return over_write_1

                if _arrow26():
                    pi_1: PropertyHelper = match_value
                    pi_1.SetValue(target, CopyUtils_tryDeepCopyObj_75B3D832(kv[1]))



        iterate(action, this.GetProperties(include_instance_properties_1))

    def DeepCopyProperties(self, include_instance_properties: bool | None=None) -> Any:
        this: DynamicObj = self
        return CopyUtils_tryDeepCopyObj_75B3D832(this, default_arg(include_instance_properties, True))

    @staticmethod
    def op_dynamic(lookup: Any, name: str) -> Any:
        match_value: Any | None = lookup.TryGetPropertyValue(name)
        if match_value is None:
            raise Exception()

        else: 
            return value_2(match_value)


    @staticmethod
    def op_dynamic_assignment(lookup: Any, name: str, value: Any) -> None:
        lookup.SetProperty(name, value)

    def ReferenceEquals(self, other: DynamicObj) -> bool:
        this: DynamicObj = self
        return this is other

    def StructurallyEquals(self, other: DynamicObj) -> bool:
        this: DynamicObj = self
        return safe_hash(this) == safe_hash(other)

    def __hash__(self, __unit: None=None) -> int:
        this: DynamicObj = self
        return HashUtils_deepHash_4E60E31B(this)

    def __eq__(self, o: Any=None) -> bool:
        this: DynamicObj = self
        return this.StructurallyEquals(o) if isinstance(o, DynamicObj) else False


DynamicObj_reflection = _expr27

def DynamicObj__ctor(__unit: None=None) -> DynamicObj:
    return DynamicObj(__unit)


def _expr28() -> TypeInfo:
    return class_type("DynamicObj.HashUtils", None, HashUtils)


class HashUtils:
    ...

HashUtils_reflection = _expr28

def _expr29() -> TypeInfo:
    return class_type("DynamicObj.CopyUtils", None, CopyUtils)


class CopyUtils:
    ...

CopyUtils_reflection = _expr29

def HashUtils_deepHash_4E60E31B(o: Any=None) -> int:
    if isinstance(o, DynamicObj):
        def f(o_2: Any=None, o: Any=o) -> int:
            return HashUtils_deepHash_4E60E31B(o_2)

        def projection(pair: Any, o: Any=o) -> str:
            return pair[0]

        class ObjectExpr30:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        return box_hash_key_val_seq_by(f, sort_by(projection, o.GetProperties(True), ObjectExpr30()))

    elif str(type(o)) == "<class \'str\'>":
        return hash_1_1(o)

    elif is_iterable(o):
        en: IEnumerator[Any] = get_enumerator(o)
        def _arrow33(__unit: None=None, o: Any=o) -> IEnumerable_1[int]:
            def _arrow31(__unit: None=None) -> bool:
                return en.System_Collections_IEnumerator_MoveNext()

            def _arrow32(__unit: None=None) -> IEnumerable_1[int]:
                return singleton(HashUtils_deepHash_4E60E31B(en.System_Collections_IEnumerator_get_Current()))

            return enumerate_while(_arrow31, delay(_arrow32))

        l: FSharpList[int] = to_list(delay(_arrow33))
        if is_empty(l):
            return 0

        else: 
            def _arrow34(hash_1: int, hash_2: int, o: Any=o) -> int:
                return merge_hashes(hash_1, hash_2)

            return reduce(_arrow34, l)


    else: 
        return hash_1_1(o)



def CopyUtils_tryDeepCopyObj_75B3D832(o: Any=None, include_instance_properties: bool | None=None) -> Any:
    include_instance_properties_1: bool = default_arg(include_instance_properties, True)
    def try_deep_copy_obj(o_1: Any=None, o: Any=o, include_instance_properties: Any=include_instance_properties) -> Any:
        (pattern_matching_result, o_7) = (None, None)
        if str(type(o_1)) == "<class \'bool\'>":
            pattern_matching_result = 0

        elif str(type(o_1)) == "<fable_modules.fable_library.types.uint8\'>>":
            pattern_matching_result = 0

        elif str(type(o_1)) == "<class \'fable_modules.fable_library.types.int8\'>":
            pattern_matching_result = 0

        elif str(type(o_1)) == "<class \'fable_modules.fable_library.types.int16\'>":
            pattern_matching_result = 0

        elif str(type(o_1)) == "<class \'fable_modules.fable_library.types.uint16\'>":
            pattern_matching_result = 0

        elif str(type(o_1)) == "<class \'int\'>":
            pattern_matching_result = 0

        elif str(type(o_1)) == "<class \'fable_modules.fable_library.types.uint32>":
            pattern_matching_result = 0

        elif str(type(o_1)) == "<class \'fable_modules.fable_library.types.int64\'>":
            pattern_matching_result = 0

        elif str(type(o_1)) == "<class \'fable_modules.fable_library.types.uint32\'>":
            pattern_matching_result = 0

        elif str(type(o_1)) == "<class \'float\'>":
            pattern_matching_result = 0

        elif str(type(o_1)) == "<class \'fable_modules.fable_library.types.float32\'>":
            pattern_matching_result = 0

        elif str(type(o_1)) == "<class \'str\'>":
            pattern_matching_result = 0

        elif str(type(o_1)) == "<class \'str\'>":
            pattern_matching_result = 0

        elif o_1 is None:
            pattern_matching_result = 0

        elif isinstance(o_1, dict):
            pattern_matching_result = 1

        elif is_array_like(o_1):
            pattern_matching_result = 2

        elif isinstance(o_1, FSharpList):
            pattern_matching_result = 3

        elif isinstance(o_1, DynamicObj):
            if hasattr(o_1, 'System_ICloneable_Clone') and callable(o_1.System_ICloneable_Clone):
                pattern_matching_result = 4
                o_7 = o_1

            else: 
                pattern_matching_result = 5


        elif hasattr(o_1, 'System_ICloneable_Clone') and callable(o_1.System_ICloneable_Clone):
            pattern_matching_result = 4
            o_7 = o_1

        else: 
            pattern_matching_result = 6

        if pattern_matching_result == 0:
            return o_1

        elif pattern_matching_result == 1:
            class ObjectExpr35:
                @property
                def Equals(self) -> Callable[[Any, Any], bool]:
                    return equals

                @property
                def GetHashCode(self) -> Callable[[Any], int]:
                    return structural_hash

            new_dict: Any = Dictionary([], ObjectExpr35())
            enumerator: Any = get_enumerator(o_1)
            try: 
                while enumerator.System_Collections_IEnumerator_MoveNext():
                    kv: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                    add_to_dict(new_dict, try_deep_copy_obj(kv[0]), try_deep_copy_obj(kv[1]))

            finally: 
                dispose(enumerator)

            return new_dict

        elif pattern_matching_result == 2:
            def _arrow36(__unit: None=None, o_1: Any=o_1) -> IEnumerable_1[DynamicObj]:
                return map_1(try_deep_copy_obj, o_1)

            return list(to_list(delay(_arrow36)))

        elif pattern_matching_result == 3:
            def _arrow37(__unit: None=None, o_1: Any=o_1) -> IEnumerable_1[DynamicObj]:
                return map_1(try_deep_copy_obj, o_1)

            return to_list(delay(_arrow37))

        elif pattern_matching_result == 4:
            return o_7.System_ICloneable_Clone()

        elif pattern_matching_result == 5:
            new_dyn: DynamicObj = DynamicObj()
            with get_enumerator(o_1.GetProperties(include_instance_properties_1)) as enumerator_1:
                while enumerator_1.System_Collections_IEnumerator_MoveNext():
                    kv_1: Any = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                    new_dyn.SetProperty(kv_1[0], try_deep_copy_obj(kv_1[1]))
            return new_dyn

        elif pattern_matching_result == 6:
            return o_1


    return try_deep_copy_obj(o)


__all__ = ["DynamicObj_reflection", "HashUtils_reflection", "CopyUtils_reflection", "HashUtils_deepHash_4E60E31B", "CopyUtils_tryDeepCopyObj_75B3D832"]

