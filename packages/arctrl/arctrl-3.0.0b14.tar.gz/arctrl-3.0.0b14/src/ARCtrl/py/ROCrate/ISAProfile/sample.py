from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.dynamic_obj.dynamic_obj import DynamicObj
from ...fable_modules.dynamic_obj.dyn_obj import (try_get_property_value, set_property, set_optional_property)
from ...fable_modules.fable_library.option import (value as value_1, default_arg)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import (FSharpRef, Array)
from ..ldobject import (LDNode, LDNode_reflection)

def _expr1812() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Sample", None, Sample, LDNode_reflection())


class Sample(LDNode):
    def __init__(self, id: str, name: Any=None, additional_type: Array[str] | None=None, additional_property: Any | None=None, derives_from: Any | None=None) -> None:
        super().__init__(id, ["bioschemas.org/Sample"], default_arg(additional_type, []))
        this: FSharpRef[Sample] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("name", name, this.contents)
        set_optional_property("additionalProperty", additional_property, this.contents)
        set_optional_property("derivesFrom", derives_from, this.contents)

    def GetName(self, __unit: None=None) -> str:
        this: Sample = self
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
                raise Exception(((((("Property \'" + "name") + "\' is set on this \'") + "Sample") + "\' object but cannot be cast to \'") + "String") + "\'")

            else: 
                return match_value


        else: 
            raise Exception(((("No property \'" + "name") + "\' set on this \'") + "Sample") + "\' object although it is mandatory. Was it created correctly?")


    @staticmethod
    def get_name() -> Callable[[Sample], str]:
        def _arrow1810(s: Sample) -> str:
            return s.GetName()

        return _arrow1810


Sample_reflection = _expr1812

def Sample__ctor_Z502AA21F(id: str, name: Any=None, additional_type: Array[str] | None=None, additional_property: Any | None=None, derives_from: Any | None=None) -> Sample:
    return Sample(id, name, additional_type, additional_property, derives_from)


__all__ = ["Sample_reflection"]

