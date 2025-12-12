from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.option import (value as value_1, map, some, bind)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import Array
from ...Core.Helper.collections_ import ResizeArray_map
from ...Core.Helper.orcid import try_get_orcid_url
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import (LDNode, LDGraph, LDRef)
from .defined_term import LDDefinedTerm
from .organization import LDOrganization
from .postal_address import LDPostalAddress

def _expr1761() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDPerson", None, LDPerson)


class LDPerson:
    @staticmethod
    def schema_type() -> str:
        return "http://schema.org/Person"

    @staticmethod
    def given_name() -> str:
        return "http://schema.org/givenName"

    @staticmethod
    def affiliation() -> str:
        return "http://schema.org/affiliation"

    @staticmethod
    def email() -> str:
        return "http://schema.org/email"

    @staticmethod
    def family_name() -> str:
        return "http://schema.org/familyName"

    @staticmethod
    def identifier() -> str:
        return "http://schema.org/identifier"

    @staticmethod
    def job_title() -> str:
        return "http://schema.org/jobTitle"

    @staticmethod
    def additional_name() -> str:
        return "http://schema.org/additionalName"

    @staticmethod
    def address() -> str:
        return "http://schema.org/address"

    @staticmethod
    def disambiguating_description() -> str:
        return "http://schema.org/disambiguatingDescription"

    @staticmethod
    def fax_number() -> str:
        return "http://schema.org/faxNumber"

    @staticmethod
    def telephone() -> str:
        return "http://schema.org/telephone"

    @staticmethod
    def try_get_given_name_as_string(p: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = p.TryGetPropertyAsSingleton(LDPerson.given_name(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_given_name_as_string(p: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = p.TryGetPropertyAsSingleton(LDPerson.given_name(), context)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                n: str = value_1(match_value)
                return n

            else: 
                raise Exception(("Property of `givenName` of object with @id `" + p.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `givenName` of object with @id `" + p.Id) + "`")


    @staticmethod
    def set_given_name_as_string(p: LDNode, n: str, context: LDContext | None=None) -> Any:
        return p.SetProperty(LDPerson.given_name(), n, context)

    @staticmethod
    def try_get_affiliation(p: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = p.TryGetPropertyAsSingleNode(LDPerson.affiliation(), graph, context)
        (pattern_matching_result, n_1) = (None, None)
        if match_value is not None:
            def _arrow1757(__unit: None=None) -> bool:
                n: LDNode = match_value
                return LDOrganization.validate(n, context)

            if _arrow1757():
                pattern_matching_result = 0
                n_1 = match_value

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n_1

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_affiliation(p: LDNode, a: LDNode, context: LDContext | None=None) -> Any:
        return p.SetProperty(LDPerson.affiliation(), a, context)

    @staticmethod
    def try_get_email_as_string(p: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = p.TryGetPropertyAsSingleton(LDPerson.email(), context)
        (pattern_matching_result, e) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                e = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return e

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_email_as_string(p: LDNode, e: str, context: LDContext | None=None) -> Any:
        return p.SetProperty(LDPerson.email(), e, context)

    @staticmethod
    def try_get_family_name_as_string(p: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = p.TryGetPropertyAsSingleton(LDPerson.family_name(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_family_name_as_string(p: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = p.TryGetPropertyAsSingleton(LDPerson.family_name(), context)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                n: str = value_1(match_value)
                return n

            else: 
                raise Exception(("Property of `familyName` of object with @id `" + p.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `familyName` of object with @id `" + p.Id) + "`")


    @staticmethod
    def set_family_name_as_string(p: LDNode, n: str, context: LDContext | None=None) -> Any:
        return p.SetProperty(LDPerson.family_name(), n, context)

    @staticmethod
    def try_get_identifier(p: LDNode, context: LDContext | None=None) -> LDNode | None:
        match_value: Any | None = p.TryGetPropertyAsSingleton(LDPerson.identifier(), context)
        (pattern_matching_result, i) = (None, None)
        if match_value is not None:
            if isinstance(value_1(match_value), LDNode):
                pattern_matching_result = 0
                i = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return i

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_identifier(p: LDNode, i: LDNode, context: LDContext | None=None) -> Any:
        return p.SetProperty(LDPerson.identifier(), i, context)

    @staticmethod
    def get_job_titles_as_defined_term(p: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDDefinedTerm.validate(ld_object, context_1)

        return p.GetPropertyNodes(LDPerson.job_title(), filter, graph, context)

    @staticmethod
    def set_job_title_as_defined_term(p: LDNode, j: Array[LDNode], context: LDContext | None=None) -> Any:
        return p.SetProperty(LDPerson.job_title(), j, context)

    @staticmethod
    def try_get_additional_name_as_string(p: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = p.TryGetPropertyAsSingleton(LDPerson.additional_name(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_additional_name_as_string(p: LDNode, n: str, context: LDContext | None=None) -> Any:
        return p.SetProperty(LDPerson.additional_name(), n, context)

    @staticmethod
    def try_get_address(p: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Any | None:
        match_value: Any | None = p.TryGetPropertyAsSingleton(LDPerson.address(), context)
        (pattern_matching_result, r_1, a, s) = (None, None, None, None)
        if match_value is not None:
            if isinstance(value_1(match_value), LDRef):
                def _arrow1758(__unit: None=None) -> bool:
                    r: LDRef = value_1(match_value)
                    return graph is not None

                if _arrow1758():
                    pattern_matching_result = 0
                    r_1 = value_1(match_value)

                else: 
                    pattern_matching_result = 3


            elif isinstance(value_1(match_value), LDNode):
                pattern_matching_result = 1
                a = value_1(match_value)

            elif str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 2
                s = value_1(match_value)

            else: 
                pattern_matching_result = 3


        else: 
            pattern_matching_result = 3

        if pattern_matching_result == 0:
            def mapping(value: LDNode) -> Any:
                return value

            return map(mapping, value_1(graph).TryGetNode(r_1.Id))

        elif pattern_matching_result == 1:
            return some(a)

        elif pattern_matching_result == 2:
            return some(s)

        elif pattern_matching_result == 3:
            return None


    @staticmethod
    def try_get_address_as_postal_address(p: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = p.TryGetPropertyAsSingleNode(LDPerson.address(), graph, context)
        (pattern_matching_result, n_1) = (None, None)
        if match_value is not None:
            def _arrow1759(__unit: None=None) -> bool:
                n: LDNode = match_value
                return LDPostalAddress.validate(n, context)

            if _arrow1759():
                pattern_matching_result = 0
                n_1 = match_value

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n_1

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def try_get_address_as_string(p: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = p.TryGetPropertyAsSingleton(LDPerson.address(), context)
        (pattern_matching_result, a) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                a = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return a

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_address_as_postal_address(p: LDNode, a: LDNode, context: LDContext | None=None) -> Any:
        return p.SetProperty(LDPerson.address(), a, context)

    @staticmethod
    def set_address_as_string(p: LDNode, a: str, context: LDContext | None=None) -> Any:
        return p.SetProperty(LDPerson.address(), a, context)

    @staticmethod
    def get_disambiguating_descriptions_as_string(p: LDNode, context: LDContext | None=None) -> Array[str]:
        def f(v: Any=None) -> Any:
            return v

        def filter(value: Any=None, context_1: LDContext | None=None) -> bool:
            return str(type(value)) == "<class \'str\'>"

        return ResizeArray_map(f, p.GetPropertyValues(LDPerson.disambiguating_description(), filter, context))

    @staticmethod
    def set_disambiguating_descriptions_as_string(p: LDNode, d: Array[str], context: LDContext | None=None) -> Any:
        return p.SetProperty(LDPerson.disambiguating_description(), d, context)

    @staticmethod
    def try_get_fax_number_as_string(p: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = p.TryGetPropertyAsSingleton(LDPerson.fax_number(), context)
        (pattern_matching_result, f) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                f = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return f

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_fax_number_as_string(p: LDNode, f: str, context: LDContext | None=None) -> Any:
        return p.SetProperty(LDPerson.fax_number(), f, context)

    @staticmethod
    def try_get_telephone_as_string(p: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = p.TryGetPropertyAsSingleton(LDPerson.telephone(), context)
        (pattern_matching_result, t) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                t = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return t

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_telephone_as_string(p: LDNode, t: str, context: LDContext | None=None) -> Any:
        return p.SetProperty(LDPerson.telephone(), t, context)

    @staticmethod
    def gen_id(given_name: Any, orcid: str | None=None, family_name: Any | None=None) -> str:
        def _arrow1760(__unit: None=None) -> str:
            match_value: str | None = bind(try_get_orcid_url, orcid)
            return ((("#Person_" + str(given_name)) + "") if (family_name is None) else (((("#Person_" + str(given_name)) + "_") + str(value_1(family_name))) + "")) if (match_value is None) else match_value

        return clean(_arrow1760())

    @staticmethod
    def validate(p: LDNode, context: LDContext | None=None) -> bool:
        return p.HasProperty(LDPerson.given_name(), context) if p.HasType(LDPerson.schema_type(), context) else False

    @staticmethod
    def create(given_name: str, orcid: str | None=None, id: str | None=None, affiliation: Any | None=None, email: str | None=None, family_name: str | None=None, identifier: Any | None=None, job_titles: Array[LDNode] | None=None, additional_name: str | None=None, address: Any | None=None, disambiguating_descriptions: Array[str] | None=None, fax_number: str | None=None, telephone: str | None=None, context: LDContext | None=None) -> LDNode:
        person: LDNode = LDNode(LDPerson.gen_id(given_name, orcid, family_name) if (id is None) else id, [LDPerson.schema_type()], None, context)
        person.SetProperty(LDPerson.given_name(), given_name, context)
        person.SetOptionalProperty(LDPerson.affiliation(), affiliation, context)
        person.SetOptionalProperty(LDPerson.email(), email, context)
        person.SetOptionalProperty(LDPerson.family_name(), family_name, context)
        person.SetOptionalProperty(LDPerson.identifier(), identifier, context)
        person.SetOptionalProperty(LDPerson.job_title(), job_titles, context)
        person.SetOptionalProperty(LDPerson.additional_name(), additional_name, context)
        person.SetOptionalProperty(LDPerson.address(), address, context)
        person.SetOptionalProperty(LDPerson.disambiguating_description(), disambiguating_descriptions, context)
        person.SetOptionalProperty(LDPerson.fax_number(), fax_number, context)
        person.SetOptionalProperty(LDPerson.telephone(), telephone, context)
        return person


LDPerson_reflection = _expr1761

__all__ = ["LDPerson_reflection"]

