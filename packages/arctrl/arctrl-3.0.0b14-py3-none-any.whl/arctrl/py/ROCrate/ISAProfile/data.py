from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.dynamic_obj.dynamic_obj import DynamicObj
from ...fable_modules.dynamic_obj.dyn_obj import (try_get_property_value, set_property, set_optional_property)
from ...fable_modules.fable_library.option import (value as value_1, default_arg)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import (FSharpRef, Array)
from ..ldobject import (LDNode, LDNode_reflection)

def _expr1816() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Data", None, Data, LDNode_reflection())


class Data(LDNode):
    def __init__(self, id: str, name: Any=None, additional_type: Array[str] | None=None, comment: Any | None=None, encoding_format: Any | None=None, disambiguating_description: Any | None=None) -> None:
        super().__init__(id, ["schema.org/MediaObject"], default_arg(additional_type, []))
        this: FSharpRef[Data] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("name", name, this.contents)
        set_optional_property("comment", comment, this.contents)
        set_optional_property("encodingFormat", encoding_format, this.contents)
        set_optional_property("disambiguatingDescription", disambiguating_description, this.contents)

    def GetName(self, __unit: None=None) -> str:
        this: Data = self
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
                raise Exception(((((("Property \'" + "name") + "\' is set on this \'") + "Data") + "\' object but cannot be cast to \'") + "String") + "\'")

            else: 
                return match_value


        else: 
            raise Exception(((("No property \'" + "name") + "\' set on this \'") + "Data") + "\' object although it is mandatory. Was it created correctly?")


    @staticmethod
    def get_name() -> Callable[[Data], str]:
        def _arrow1814(d: Data) -> str:
            return d.GetName()

        return _arrow1814


Data_reflection = _expr1816

def Data__ctor_Z11AF9DE7(id: str, name: Any=None, additional_type: Array[str] | None=None, comment: Any | None=None, encoding_format: Any | None=None, disambiguating_description: Any | None=None) -> Data:
    return Data(id, name, additional_type, comment, encoding_format, disambiguating_description)


__all__ = ["Data_reflection"]

