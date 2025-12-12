from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr1956() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.Material.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("Material", string_type), ("ArcMaterial", string_type), ("type", string_type), ("name", string_type), ("characteristics", string_type), ("derives_from", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    Material: str
    ArcMaterial: str
    type: str
    name: str
    characteristics: str
    derives_from: str

IContext_reflection = _expr1956

def _arrow1964(__unit: None=None) -> IEncodable:
    class ObjectExpr1957(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1958(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("https://bioschemas.org/")

    class ObjectExpr1959(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("bio:Sample")

    class ObjectExpr1960(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("sdo:disambiguatingDescription")

    class ObjectExpr1961(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("sdo:name")

    class ObjectExpr1962(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            return helpers_5.encode_string("bio:additionalProperty")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1957()), ("bio", ObjectExpr1958()), ("Material", ObjectExpr1959()), ("type", ObjectExpr1960()), ("name", ObjectExpr1961()), ("characteristics", ObjectExpr1962())])
    class ObjectExpr1963(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr1963()


context_jsonvalue: IEncodable = _arrow1964()

context_str: str = "\r\n{\r\n  \"@context\": {\r\n    \"sdo\": \"http://schema.org/\",\r\n    \"arc\": \"http://purl.org/nfdi4plants/ontology/\",\r\n\r\n    \"ArcMaterial\": \"arc:ARC#ARC_00000108\",\r\n    \"Material\": \"sdo:Thing\",\r\n\r\n    \"type\": \"arc:ARC#ARC_00000085\",\r\n    \"name\": \"arc:ARC#ARC_00000019\",\r\n    \"characteristics\": \"arc:ARC#ARC_00000080\",\r\n    \"derivesFrom\": \"arc:ARC#ARC_00000082\"\r\n  }\r\n}\r\n    "

__all__ = ["IContext_reflection", "context_jsonvalue", "context_str"]

