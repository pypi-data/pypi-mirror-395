from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr1936() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.MaterialAttribute.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("MaterialAttribute", string_type), ("ArcMaterialAttribute", string_type), ("characteristic_type", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    MaterialAttribute: str
    ArcMaterialAttribute: str
    characteristic_type: str

IContext_reflection = _expr1936

def _arrow1943(__unit: None=None) -> IEncodable:
    class ObjectExpr1937(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1938(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("http://purl.org/nfdi4plants/ontology/")

    class ObjectExpr1939(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("sdo:Property")

    class ObjectExpr1940(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("arc:ARC#ARC_00000050")

    class ObjectExpr1941(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("arc:ARC#ARC_00000098")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1937()), ("arc", ObjectExpr1938()), ("MaterialAttribute", ObjectExpr1939()), ("ArcMaterialAttribute", ObjectExpr1940()), ("characteristicType", ObjectExpr1941())])
    class ObjectExpr1942(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_5))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_5.encode_object(arg)

    return ObjectExpr1942()


context_jsonvalue: IEncodable = _arrow1943()

context_str: str = "\r\n{\r\n  \"@context\": {\r\n    \"sdo\": \"http://schema.org/\",\r\n    \"arc\": \"http://purl.org/nfdi4plants/ontology/\",\r\n\r\n    \"MaterialAttribute\": \"sdo:Property\",\r\n    \"ArcMaterialAttribute\": \"arc:ARC#ARC_00000050\",\r\n\r\n    \"characteristicType\": \"arc:ARC#ARC_00000098\"\r\n  }\r\n}\r\n    "

__all__ = ["IContext_reflection", "context_jsonvalue", "context_str"]

