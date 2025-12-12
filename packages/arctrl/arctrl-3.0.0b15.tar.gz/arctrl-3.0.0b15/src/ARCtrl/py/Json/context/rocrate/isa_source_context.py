from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr2079() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.Source.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("Source", string_type), ("ArcSource", string_type), ("identifier", string_type), ("characteristics", string_type), ("name", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    Source: str
    ArcSource: str
    identifier: str
    characteristics: str
    name: str

IContext_reflection = _expr2079

def _arrow2086(__unit: None=None) -> IEncodable:
    class ObjectExpr2080(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr2081(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("https://bioschemas.org/")

    class ObjectExpr2082(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("bio:Sample")

    class ObjectExpr2083(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("sdo:name")

    class ObjectExpr2084(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("bio:additionalProperty")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr2080()), ("bio", ObjectExpr2081()), ("Source", ObjectExpr2082()), ("name", ObjectExpr2083()), ("characteristics", ObjectExpr2084())])
    class ObjectExpr2085(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_5))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_5.encode_object(arg)

    return ObjectExpr2085()


context_jsonvalue: IEncodable = _arrow2086()

context_str: str = "\r\n{\r\n  \"@context\": {\r\n    \"sdo\": \"http://schema.org/\",\r\n    \"arc\": \"http://purl.org/nfdi4plants/ontology/\",\r\n\r\n    \"Source\": \"sdo:Thing\",\r\n    \"ArcSource\": \"arc:ARC#ARC_00000071\",\r\n\r\n    \"identifier\": \"sdo:identifier\",\r\n\r\n    \"name\": \"arc:ARC#ARC_00000019\",\r\n    \"characteristics\": \"arc:ARC#ARC_00000080\"\r\n  }\r\n}\r\n    "

__all__ = ["IContext_reflection", "context_jsonvalue", "context_str"]

