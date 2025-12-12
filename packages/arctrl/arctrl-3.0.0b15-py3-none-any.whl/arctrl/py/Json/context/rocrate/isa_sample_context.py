from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr2071() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.Sample.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("Sample", string_type), ("ArcSample", string_type), ("name", string_type), ("characteristics", string_type), ("factor_values", string_type), ("derives_from", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    Sample: str
    ArcSample: str
    name: str
    characteristics: str
    factor_values: str
    derives_from: str

IContext_reflection = _expr2071

def _arrow2078(__unit: None=None) -> IEncodable:
    class ObjectExpr2072(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr2073(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("https://bioschemas.org/")

    class ObjectExpr2074(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("bio:Sample")

    class ObjectExpr2075(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("sdo:name")

    class ObjectExpr2076(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("bio:additionalProperty")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr2072()), ("bio", ObjectExpr2073()), ("Sample", ObjectExpr2074()), ("name", ObjectExpr2075()), ("additionalProperties", ObjectExpr2076())])
    class ObjectExpr2077(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_5))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_5.encode_object(arg)

    return ObjectExpr2077()


context_jsonvalue: IEncodable = _arrow2078()

__all__ = ["IContext_reflection", "context_jsonvalue"]

