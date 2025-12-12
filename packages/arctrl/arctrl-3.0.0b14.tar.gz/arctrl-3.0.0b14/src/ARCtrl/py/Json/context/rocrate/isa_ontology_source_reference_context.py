from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr1974() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.OntologySourceReference.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("OntologySourceReference", string_type), ("description", string_type), ("name", string_type), ("file", string_type), ("version", string_type), ("comments", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    OntologySourceReference: str
    description: str
    name: str
    file: str
    version: str
    comments: str

IContext_reflection = _expr1974

def _arrow1983(__unit: None=None) -> IEncodable:
    class ObjectExpr1975(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1976(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("sdo:DefinedTermSet")

    class ObjectExpr1977(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("sdo:description")

    class ObjectExpr1978(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("sdo:name")

    class ObjectExpr1979(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("sdo:url")

    class ObjectExpr1980(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            return helpers_5.encode_string("sdo:version")

    class ObjectExpr1981(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
            return helpers_6.encode_string("sdo:disambiguatingDescription")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1975()), ("OntologySourceReference", ObjectExpr1976()), ("description", ObjectExpr1977()), ("name", ObjectExpr1978()), ("file", ObjectExpr1979()), ("version", ObjectExpr1980()), ("comments", ObjectExpr1981())])
    class ObjectExpr1982(IEncodable):
        def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_7))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_7.encode_object(arg)

    return ObjectExpr1982()


context_jsonvalue: IEncodable = _arrow1983()

context_str: str = "\r\n{\r\n  \"@context\": {\r\n    \"sdo\": \"http://schema.org/\",\r\n    \"arc\": \"http://purl.org/nfdi4plants/ontology/\",\r\n\r\n    \"OntologySourceReference\": \"sdo:DefinedTermSet\",\r\n    \r\n    \"description\": \"sdo:description\",\r\n    \"name\": \"sdo:name\",\r\n    \"file\": \"sdo:url\",\r\n    \"version\": \"sdo:version\",\r\n    \"comments\": \"sdo:disambiguatingDescription\"\r\n  }\r\n}\r\n    "

__all__ = ["IContext_reflection", "context_jsonvalue", "context_str"]

