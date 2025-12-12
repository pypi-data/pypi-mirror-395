from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.dynamic_obj.dynamic_obj import DynamicObj
from ...fable_modules.dynamic_obj.dyn_obj import (try_get_property_value, set_property, set_optional_property)
from ...fable_modules.fable_library.option import (value as value_1, default_arg)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import (FSharpRef, Array)
from ..ldobject import (LDNode, LDNode_reflection)

def _expr1837() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.ScholarlyArticle", None, ScholarlyArticle, LDNode_reflection())


class ScholarlyArticle(LDNode):
    def __init__(self, id: str, headline: Any=None, identifier: Any=None, additional_type: Array[str] | None=None, author: Any | None=None, url: Any | None=None, creative_work_status: Any | None=None, disambiguating_description: Any | None=None) -> None:
        super().__init__(id, ["schema.org/ScholarlyArticle"], default_arg(additional_type, []))
        this: FSharpRef[ScholarlyArticle] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("headline", headline, this.contents)
        set_property("identifier", identifier, this.contents)
        set_optional_property("author", author, this.contents)
        set_optional_property("url", url, this.contents)
        set_optional_property("creativeWorkStatus", creative_work_status, this.contents)
        set_optional_property("disambiguatingDescription", disambiguating_description, this.contents)

    def GetHeadline(self, __unit: None=None) -> str:
        this: ScholarlyArticle = self
        obj: DynamicObj = this
        if try_get_property_value("headline", obj) is not None:
            match_value: str | None
            match_value_1: Any | None = obj.TryGetPropertyValue("headline")
            if match_value_1 is not None:
                o: Any = value_1(match_value_1)
                match_value = o if (str(type(o)) == "<class \'str\'>") else None

            else: 
                match_value = None

            if match_value is None:
                raise Exception(((((("Property \'" + "headline") + "\' is set on this \'") + "ScholarlyArticle") + "\' object but cannot be cast to \'") + "String") + "\'")

            else: 
                return match_value


        else: 
            raise Exception(((("No property \'" + "headline") + "\' set on this \'") + "ScholarlyArticle") + "\' object although it is mandatory. Was it created correctly?")


    @staticmethod
    def get_headline() -> Callable[[ScholarlyArticle], str]:
        def _arrow1835(s: ScholarlyArticle) -> str:
            return s.GetHeadline()

        return _arrow1835

    def GetIdentifier(self, __unit: None=None) -> str:
        this: ScholarlyArticle = self
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
                raise Exception(((((("Property \'" + "identifier") + "\' is set on this \'") + "ScholarlyArticle") + "\' object but cannot be cast to \'") + "String") + "\'")

            else: 
                return match_value


        else: 
            raise Exception(((("No property \'" + "identifier") + "\' set on this \'") + "ScholarlyArticle") + "\' object although it is mandatory. Was it created correctly?")


    @staticmethod
    def get_identifier() -> Callable[[ScholarlyArticle], str]:
        def _arrow1836(s: ScholarlyArticle) -> str:
            return s.GetIdentifier()

        return _arrow1836


ScholarlyArticle_reflection = _expr1837

def ScholarlyArticle__ctor_Z22702026(id: str, headline: Any=None, identifier: Any=None, additional_type: Array[str] | None=None, author: Any | None=None, url: Any | None=None, creative_work_status: Any | None=None, disambiguating_description: Any | None=None) -> ScholarlyArticle:
    return ScholarlyArticle(id, headline, identifier, additional_type, author, url, creative_work_status, disambiguating_description)


__all__ = ["ScholarlyArticle_reflection"]

