from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.list import (FSharpList, is_empty, reduce)
from ...fable_modules.fable_library.option import value
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.seq import (to_list, delay, append, singleton, empty)
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.fable_library.util import IEnumerable_1
from ...Core.Helper.identifier import create_missing_identifier
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import LDNode

def _expr1729() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDPostalAddress", None, LDPostalAddress)


class LDPostalAddress:
    @staticmethod
    def schema_type() -> str:
        return "http://schema.org/PostalAddress"

    @staticmethod
    def address_country() -> str:
        return "http://schema.org/addressCountry"

    @staticmethod
    def postal_code() -> str:
        return "http://schema.org/postalCode"

    @staticmethod
    def street_address() -> str:
        return "http://schema.org/streetAddress"

    @staticmethod
    def try_get_address_country_as_string(s: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = s.TryGetPropertyAsSingleton(LDPostalAddress.address_country(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_address_country_as_string(s: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = s.TryGetPropertyAsSingleton(LDPostalAddress.address_country(), context)
        if match_value is None:
            raise Exception(("Could not access property `addressCountry` of object with @id `" + s.Id) + "`")

        elif str(type(value(match_value))) == "<class \'str\'>":
            n: str = value(match_value)
            return n

        else: 
            raise Exception(("Value of property `addressCountry` of object with @id `" + s.Id) + "` should have been a string")


    @staticmethod
    def set_address_country_as_string(s: LDNode, n: str) -> None:
        s.SetProperty(LDPostalAddress.address_country(), n)

    @staticmethod
    def try_get_postal_code_as_string(s: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = s.TryGetPropertyAsSingleton(LDPostalAddress.postal_code(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_postal_code_as_string(s: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = s.TryGetPropertyAsSingleton(LDPostalAddress.postal_code(), context)
        if match_value is None:
            raise Exception(("Could not access property `postalCode` of object with @id `" + s.Id) + "`")

        elif str(type(value(match_value))) == "<class \'str\'>":
            n: str = value(match_value)
            return n

        else: 
            raise Exception(("Value of property `postalCode` of object with @id `" + s.Id) + "` should have been a string")


    @staticmethod
    def set_postal_code_as_string(s: LDNode, n: str) -> None:
        s.SetProperty(LDPostalAddress.postal_code(), n)

    @staticmethod
    def try_get_street_address_as_string(s: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = s.TryGetPropertyAsSingleton(LDPostalAddress.street_address(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_street_address_as_string(s: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = s.TryGetPropertyAsSingleton(LDPostalAddress.street_address(), context)
        if match_value is None:
            raise Exception(("Could not access property `streetAddress` of object with @id `" + s.Id) + "`")

        elif str(type(value(match_value))) == "<class \'str\'>":
            n: str = value(match_value)
            return n

        else: 
            raise Exception(("Value of property `streetAddress` of object with @id `" + s.Id) + "` should have been a string")


    @staticmethod
    def set_street_address_as_string(s: LDNode, n: str) -> None:
        s.SetProperty(LDPostalAddress.street_address(), n)

    @staticmethod
    def gen_id(address_country: str | None=None, postal_code: str | None=None, street_address: str | None=None) -> str:
        def _arrow1727(__unit: None=None) -> IEnumerable_1[str]:
            def _arrow1726(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1725(__unit: None=None) -> IEnumerable_1[str]:
                    return singleton("streetAddress") if (street_address is not None) else empty()

                return append(singleton("postalCode") if (postal_code is not None) else empty(), delay(_arrow1725))

            return append(singleton("addressCountry") if (address_country is not None) else empty(), delay(_arrow1726))

        items: FSharpList[str] = to_list(delay(_arrow1727))
        def _arrow1728(__unit: None=None) -> str:
            def reduction(acc: str, x: str) -> str:
                return ((("" + acc) + "_") + x) + ""

            arg: str = reduce(reduction, items)
            return to_text(printf("#%s"))(arg)

        return clean(create_missing_identifier() if is_empty(items) else _arrow1728())

    @staticmethod
    def validate(o: LDNode, context: LDContext | None=None) -> bool:
        return o.HasType(LDPostalAddress.schema_type(), context)

    @staticmethod
    def create(id: str | None=None, address_country: str | None=None, postal_code: str | None=None, street_address: str | None=None, context: LDContext | None=None) -> LDNode:
        s: LDNode = LDNode(LDPostalAddress.gen_id(address_country, postal_code, street_address) if (id is None) else id, [LDPostalAddress.schema_type()], None, context)
        s.SetOptionalProperty(LDPostalAddress.address_country(), address_country)
        s.SetOptionalProperty(LDPostalAddress.postal_code(), postal_code)
        s.SetOptionalProperty(LDPostalAddress.street_address(), street_address)
        return s


LDPostalAddress_reflection = _expr1729

__all__ = ["LDPostalAddress_reflection"]

