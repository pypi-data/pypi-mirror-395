from __future__ import annotations
from typing import Any
from ..Core.comment import Comment
from ..Core.Helper.collections_ import (Option_fromSeq, ResizeArray_map)
from ..Core.Helper.orcid import try_get_orcid_number
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from ..Json.ROCrate.ldnode import (decoder as decoder_1, encoder)
from ..ROCrate.ldcontext import LDContext
from ..ROCrate.ldobject import (LDNode, LDGraph)
from ..ROCrate.LDTypes.organization import LDOrganization
from ..ROCrate.LDTypes.person import LDPerson
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.seq import (is_empty, filter)
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.fable_library.types import (Array, to_string as to_string_1)
from .basic import (BaseTypes_composeDefinedTerm_ZDED3A0F, BaseTypes_decomposeDefinedTerm_Z2F770004)

def _expr3884() -> TypeInfo:
    return class_type("ARCtrl.Conversion.PersonConversion", None, PersonConversion)


class PersonConversion:
    ...

PersonConversion_reflection = _expr3884

def PersonConversion_get_orcidKey(__unit: None=None) -> str:
    return "ORCID"


def PersonConversion_composeAffiliation_Z721C83C5(affiliation: str) -> LDNode:
    try: 
        match_value: FSharpResult_2[LDNode, str] = Decode_fromString(decoder_1, affiliation)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as match_value_1:
        return LDOrganization.create(affiliation)



def PersonConversion_decomposeAffiliation_Z2F770004(affiliation: LDNode, context: LDContext | None=None) -> str:
    def predicate(n: str, affiliation: Any=affiliation, context: Any=context) -> bool:
        return n != LDOrganization.name()

    if is_empty(filter(predicate, affiliation.GetPropertyNames(context))):
        return LDOrganization.get_name_as_string(affiliation, context)

    else: 
        return to_string(0, encoder(affiliation))



def PersonConversion_composeAddress_Z721C83C5(address: str) -> Any:
    try: 
        def _arrow3885(__unit: None=None) -> LDNode:
            match_value: FSharpResult_2[LDNode, str] = Decode_fromString(decoder_1, address)
            if match_value.tag == 1:
                raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

            else: 
                return match_value.fields[0]


        return _arrow3885()

    except Exception as match_value_1:
        return address



def PersonConversion_decomposeAddress_4E60E31B(address: Any=None) -> str:
    if str(type(address)) == "<class \'str\'>":
        return address

    elif isinstance(address, LDNode):
        return to_string(0, encoder(address))

    else: 
        raise Exception("Address must be a string or a Json.LDNode")



def PersonConversion_composePerson_Z64D846DC(person: Person) -> LDNode:
    given_name: str
    match_value: str | None = person.FirstName
    if match_value is None:
        raise Exception("Person must have a given name")

    else: 
        given_name = match_value

    def f(term: OntologyAnnotation, person: Any=person) -> LDNode:
        return BaseTypes_composeDefinedTerm_ZDED3A0F(term)

    job_titles: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f, person.Roles))
    def f_1(c: Comment, person: Any=person) -> str:
        return to_string_1(c)

    disambiguating_descriptions: Array[str] | None = Option_fromSeq(ResizeArray_map(f_1, person.Comments))
    def mapping(address: str, person: Any=person) -> Any:
        return PersonConversion_composeAddress_Z721C83C5(address)

    address_1: Any | None = map(mapping, person.Address)
    def mapping_1(affiliation: str, person: Any=person) -> LDNode:
        return PersonConversion_composeAffiliation_Z721C83C5(affiliation)

    affiliation_1: LDNode | None = map(mapping_1, person.Affiliation)
    return LDPerson.create(given_name, person.ORCID, None, affiliation_1, person.EMail, person.LastName, None, job_titles, person.MidInitials, address_1, disambiguating_descriptions, person.Fax, person.Phone)


def PersonConversion_decomposePerson_Z6839B9E8(person: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Person:
    orcid: str | None = try_get_orcid_number(person.Id)
    address: str | None
    match_value: str | None = LDPerson.try_get_address_as_string(person, context)
    if match_value is None:
        match_value_1: LDNode | None = LDPerson.try_get_address_as_postal_address(person, graph, context)
        address = None if (match_value_1 is None) else PersonConversion_decomposeAddress_4E60E31B(match_value_1)

    else: 
        address = match_value

    def f(r: LDNode, person: Any=person, graph: Any=graph, context: Any=context) -> OntologyAnnotation:
        return BaseTypes_decomposeDefinedTerm_Z2F770004(r, context)

    roles: Array[OntologyAnnotation] = ResizeArray_map(f, LDPerson.get_job_titles_as_defined_term(person, graph, context))
    def f_1(s_1: str, person: Any=person, graph: Any=graph, context: Any=context) -> Comment:
        return Comment.from_string(s_1)

    comments: Array[Comment] = ResizeArray_map(f_1, LDPerson.get_disambiguating_descriptions_as_string(person, context))
    def mapping(a_3: LDNode, person: Any=person, graph: Any=graph, context: Any=context) -> str:
        return PersonConversion_decomposeAffiliation_Z2F770004(a_3, context)

    affiliation: str | None = map(mapping, LDPerson.try_get_affiliation(person, graph, context))
    return Person.create(orcid, LDPerson.try_get_family_name_as_string(person, context), LDPerson.get_given_name_as_string(person, context), LDPerson.try_get_additional_name_as_string(person, context), LDPerson.try_get_email_as_string(person, context), LDPerson.try_get_telephone_as_string(person, context), LDPerson.try_get_fax_number_as_string(person, context), address, affiliation, roles, comments)


__all__ = ["PersonConversion_reflection", "PersonConversion_get_orcidKey", "PersonConversion_composeAffiliation_Z721C83C5", "PersonConversion_decomposeAffiliation_Z2F770004", "PersonConversion_composeAddress_Z721C83C5", "PersonConversion_decomposeAddress_4E60E31B", "PersonConversion_composePerson_Z64D846DC", "PersonConversion_decomposePerson_Z6839B9E8"]

