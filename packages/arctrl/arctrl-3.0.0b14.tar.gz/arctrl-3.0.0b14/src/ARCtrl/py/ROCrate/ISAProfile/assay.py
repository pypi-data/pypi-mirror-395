from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.dynamic_obj.dynamic_obj import DynamicObj
from ...fable_modules.dynamic_obj.dyn_obj import (try_get_property_value, set_property, set_optional_property)
from ...fable_modules.fable_library.option import value as value_1
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import FSharpRef
from .dataset import (Dataset, Dataset_reflection)

def _expr1803() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Assay", None, Assay, Dataset_reflection())


class Assay(Dataset):
    def __init__(self, id: str, identifier: str, about: Any | None=None, comment: Any | None=None, creator: Any | None=None, has_part: Any | None=None, measurement_method: Any | None=None, measurement_technique: Any | None=None, url: Any | None=None, variable_measured: Any | None=None) -> None:
        super().__init__(id, ["Assay"])
        this: FSharpRef[Assay] = FSharpRef(None)
        this.contents = self
        self.init_00408_1: int = 1
        set_property("identifier", identifier, this.contents)
        set_optional_property("measurementMethod", measurement_method, this.contents)
        set_optional_property("measurementTechnique", measurement_technique, this.contents)
        set_optional_property("variableMeasured", variable_measured, this.contents)
        set_optional_property("about", about, this.contents)
        set_optional_property("comment", comment, this.contents)
        set_optional_property("creator", creator, this.contents)
        set_optional_property("hasPart", has_part, this.contents)
        set_optional_property("url", url, this.contents)

    def GetIdentifier(self, __unit: None=None) -> str:
        this: Assay = self
        obj: DynamicObj = this
        if try_get_property_value("identifier", obj) is not None:
            match_value: str | None
            match_value_1: Any | None = obj.TryGetPropertyValue("identifier")
            if match_value_1 is not None:
                o: Any = value_1(match_value_1)
                match_value = o if (str(type(o)) == "<class \'str\'>") else None

            else: 
                match_value = None

            if match_value is None:
                raise Exception(((((("Property \'" + "identifier") + "\' is set on this \'") + "Assay") + "\' object but cannot be cast to \'") + "String") + "\'")

            else: 
                return match_value


        else: 
            raise Exception(((("No property \'" + "identifier") + "\' set on this \'") + "Assay") + "\' object although it is mandatory. Was it created correctly?")


    @staticmethod
    def get_identifier() -> Callable[[Assay], str]:
        def _arrow1802(ass: Assay) -> str:
            return ass.GetIdentifier()

        return _arrow1802


Assay_reflection = _expr1803

def Assay__ctor_Z318F9460(id: str, identifier: str, about: Any | None=None, comment: Any | None=None, creator: Any | None=None, has_part: Any | None=None, measurement_method: Any | None=None, measurement_technique: Any | None=None, url: Any | None=None, variable_measured: Any | None=None) -> Assay:
    return Assay(id, identifier, about, comment, creator, has_part, measurement_method, measurement_technique, url, variable_measured)


__all__ = ["Assay_reflection"]

