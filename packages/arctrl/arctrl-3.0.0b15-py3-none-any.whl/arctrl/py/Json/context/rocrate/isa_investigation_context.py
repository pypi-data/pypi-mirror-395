from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr1919() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.Investigation.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("Investigation", string_type), ("identifier", string_type), ("title", string_type), ("description", string_type), ("submission_date", string_type), ("public_release_date", string_type), ("publications", string_type), ("people", string_type), ("studies", string_type), ("ontology_source_references", string_type), ("comments", string_type), ("publications_003F", string_type), ("filename", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    Investigation: str
    identifier: str
    title: str
    description: str
    submission_date: str
    public_release_date: str
    publications: str
    people: str
    studies: str
    ontology_source_references: str
    comments: str
    publications_003F: str
    filename: str

IContext_reflection = _expr1919

def _arrow1935(__unit: None=None) -> IEncodable:
    class ObjectExpr1920(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1921(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("sdo:Dataset")

    class ObjectExpr1922(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("sdo:identifier")

    class ObjectExpr1923(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("sdo:name")

    class ObjectExpr1924(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("sdo:additionalType")

    class ObjectExpr1925(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            return helpers_5.encode_string("sdo:description")

    class ObjectExpr1926(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
            return helpers_6.encode_string("sdo:dateCreated")

    class ObjectExpr1927(IEncodable):
        def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
            return helpers_7.encode_string("sdo:datePublished")

    class ObjectExpr1928(IEncodable):
        def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
            return helpers_8.encode_string("sdo:citation")

    class ObjectExpr1929(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any]) -> Any:
            return helpers_9.encode_string("sdo:creator")

    class ObjectExpr1930(IEncodable):
        def Encode(self, helpers_10: IEncoderHelpers_1[Any]) -> Any:
            return helpers_10.encode_string("sdo:hasPart")

    class ObjectExpr1931(IEncodable):
        def Encode(self, helpers_11: IEncoderHelpers_1[Any]) -> Any:
            return helpers_11.encode_string("sdo:mentions")

    class ObjectExpr1932(IEncodable):
        def Encode(self, helpers_12: IEncoderHelpers_1[Any]) -> Any:
            return helpers_12.encode_string("sdo:comment")

    class ObjectExpr1933(IEncodable):
        def Encode(self, helpers_13: IEncoderHelpers_1[Any]) -> Any:
            return helpers_13.encode_string("sdo:alternateName")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1920()), ("Investigation", ObjectExpr1921()), ("identifier", ObjectExpr1922()), ("title", ObjectExpr1923()), ("additionalType", ObjectExpr1924()), ("description", ObjectExpr1925()), ("submissionDate", ObjectExpr1926()), ("publicReleaseDate", ObjectExpr1927()), ("publications", ObjectExpr1928()), ("people", ObjectExpr1929()), ("studies", ObjectExpr1930()), ("ontologySourceReferences", ObjectExpr1931()), ("comments", ObjectExpr1932()), ("filename", ObjectExpr1933())])
    class ObjectExpr1934(IEncodable):
        def Encode(self, helpers_14: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_14))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_14.encode_object(arg)

    return ObjectExpr1934()


context_jsonvalue: IEncodable = _arrow1935()

context_str: str = "\r\n{\r\n  \"@context\": {\r\n    \"sdo\": \"http://schema.org/\",\r\n    \"arc\": \"http://purl.org/nfdi4plants/ontology/\",\r\n\r\n    \"Investigation\": \"sdo:Dataset\",\r\n\r\n    \"identifier\" : \"sdo:identifier\",\r\n    \"title\": \"sdo:name\",\r\n    \"description\": \"sdo:description\",\r\n    \"submissionDate\": \"sdo:dateCreated\",\r\n    \"publicReleaseDate\": \"sdo:datePublished\",\r\n    \"publications\": \"sdo:citation\",\r\n    \"people\": \"sdo:creator\",\r\n    \"studies\": \"sdo:hasPart\",\r\n    \"ontologySourceReferences\": \"sdo:mentions\",\r\n    \"comments\": \"sdo:disambiguatingDescription\",\r\n\r\n    \"publications?\": \"sdo:SubjectOf?\",\r\n    \"filename\": \"sdo:alternateName\"\r\n  }\r\n}\r\n    "

__all__ = ["IContext_reflection", "context_jsonvalue", "context_str"]

