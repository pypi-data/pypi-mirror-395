from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.dynamic_obj.dynamic_obj import DynamicObj
from ...fable_modules.dynamic_obj.dyn_obj import (try_get_property_value, set_property, set_optional_property)
from ...fable_modules.fable_library.option import value as value_1
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import FSharpRef
from .dataset import (Dataset, Dataset_reflection)

def _expr1799() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Investigation", None, Investigation, Dataset_reflection())


class Investigation(Dataset):
    def __init__(self, id: str, identifier: str, citation: Any | None=None, comment: Any | None=None, creator: Any | None=None, date_created: Any | None=None, date_modified: Any | None=None, date_published: Any | None=None, has_part: Any | None=None, headline: Any | None=None, mentions: Any | None=None, url: Any | None=None, description: Any | None=None) -> None:
        super().__init__(id, ["Investigation"])
        this: FSharpRef[Investigation] = FSharpRef(None)
        this.contents = self
        self.init_00408_1: int = 1
        set_property("identifier", identifier, this.contents)
        set_optional_property("citation", citation, this.contents)
        set_optional_property("comment", comment, this.contents)
        set_optional_property("creator", creator, this.contents)
        set_optional_property("dateCreated", date_created, this.contents)
        set_optional_property("dateModified", date_modified, this.contents)
        set_optional_property("datePublished", date_published, this.contents)
        set_optional_property("hasPart", has_part, this.contents)
        set_optional_property("headline", headline, this.contents)
        set_optional_property("mentions", mentions, this.contents)
        set_optional_property("url", url, this.contents)
        set_optional_property("description", description, this.contents)

    def GetIdentifier(self, __unit: None=None) -> str:
        this: Investigation = self
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
                raise Exception(((((("Property \'" + "identifier") + "\' is set on this \'") + "Investigation") + "\' object but cannot be cast to \'") + "String") + "\'")

            else: 
                return match_value


        else: 
            raise Exception(((("No property \'" + "identifier") + "\' set on this \'") + "Investigation") + "\' object although it is mandatory. Was it created correctly?")


    @staticmethod
    def get_identifier() -> Callable[[Investigation], str]:
        def _arrow1798(inv: Investigation) -> str:
            return inv.GetIdentifier()

        return _arrow1798


Investigation_reflection = _expr1799

def Investigation__ctor_Z47833D48(id: str, identifier: str, citation: Any | None=None, comment: Any | None=None, creator: Any | None=None, date_created: Any | None=None, date_modified: Any | None=None, date_published: Any | None=None, has_part: Any | None=None, headline: Any | None=None, mentions: Any | None=None, url: Any | None=None, description: Any | None=None) -> Investigation:
    return Investigation(id, identifier, citation, comment, creator, date_created, date_modified, date_published, has_part, headline, mentions, url, description)


__all__ = ["Investigation_reflection"]

