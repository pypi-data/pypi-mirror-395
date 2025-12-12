from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.dynamic_obj.dynamic_obj import DynamicObj
from ...fable_modules.dynamic_obj.dyn_obj import (try_get_property_value, set_property, set_optional_property)
from ...fable_modules.fable_library.option import (value as value_1, default_arg)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import (FSharpRef, Array)
from ..ldobject import (LDNode, LDNode_reflection)

def _expr1831() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.PropertyValue", None, PropertyValue, LDNode_reflection())


class PropertyValue(LDNode):
    def __init__(self, id: str, name: Any=None, value: Any=None, property_id: Any | None=None, unit_code: Any | None=None, unit_text: Any | None=None, value_reference: Any | None=None, additional_type: Array[str] | None=None) -> None:
        super().__init__(id, ["schema.org/PropertyValue"], default_arg(additional_type, []))
        this: FSharpRef[PropertyValue] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("name", name, this.contents)
        set_property("value", value, this.contents)
        set_optional_property("propertyID", property_id, this.contents)
        set_optional_property("unitCode", unit_code, this.contents)
        set_optional_property("unitText", unit_text, this.contents)
        set_optional_property("valueReference", value_reference, this.contents)

    def GetName(self, __unit: None=None) -> str:
        this: PropertyValue = self
        obj: DynamicObj = this
        if try_get_property_value("name", obj) is not None:
            match_value: str | None
            match_value_1: Any | None = obj.TryGetPropertyValue("name")
            if match_value_1 is not None:
                o: Any = value_1(match_value_1)
                match_value = o if (str(type(o)) == "<class \'str\'>") else None

            else: 
                match_value = None

            if match_value is None:
                raise Exception(((((("Property \'" + "name") + "\' is set on this \'") + "PropertyValue") + "\' object but cannot be cast to \'") + "String") + "\'")

            else: 
                return match_value


        else: 
            raise Exception(((("No property \'" + "name") + "\' set on this \'") + "PropertyValue") + "\' object although it is mandatory. Was it created correctly?")


    @staticmethod
    def get_name() -> Callable[[PropertyValue], str]:
        def _arrow1829(lp: PropertyValue) -> str:
            return lp.GetName()

        return _arrow1829

    def GetValue(self, __unit: None=None) -> str:
        this: PropertyValue = self
        obj: DynamicObj = this
        if try_get_property_value("name", obj) is not None:
            match_value: str | None
            match_value_1: Any | None = obj.TryGetPropertyValue("name")
            if match_value_1 is not None:
                o: Any = value_1(match_value_1)
                match_value = o if (str(type(o)) == "<class \'str\'>") else None

            else: 
                match_value = None

            if match_value is None:
                raise Exception(((((("Property \'" + "name") + "\' is set on this \'") + "PropertyValue") + "\' object but cannot be cast to \'") + "String") + "\'")

            else: 
                return match_value


        else: 
            raise Exception(((("No property \'" + "name") + "\' set on this \'") + "PropertyValue") + "\' object although it is mandatory. Was it created correctly?")


    @staticmethod
    def get_value() -> Callable[[PropertyValue], str]:
        def _arrow1830(lp: PropertyValue) -> str:
            return lp.GetValue()

        return _arrow1830


PropertyValue_reflection = _expr1831

def PropertyValue__ctor_Z5E5247A6(id: str, name: Any=None, value: Any=None, property_id: Any | None=None, unit_code: Any | None=None, unit_text: Any | None=None, value_reference: Any | None=None, additional_type: Array[str] | None=None) -> PropertyValue:
    return PropertyValue(id, name, value, property_id, unit_code, unit_text, value_reference, additional_type)


__all__ = ["PropertyValue_reflection"]

