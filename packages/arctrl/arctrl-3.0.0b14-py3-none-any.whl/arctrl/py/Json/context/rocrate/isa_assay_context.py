from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr1853() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.Assay.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("Assay", string_type), ("ArcAssay", string_type), ("measurement_type", string_type), ("technology_type", string_type), ("technology_platform", string_type), ("data_files", string_type), ("materials", string_type), ("other_materials", string_type), ("samples", string_type), ("characteristic_categories", string_type), ("process_sequence", string_type), ("unit_categories", string_type), ("comments", string_type), ("filename", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    Assay: str
    ArcAssay: str
    measurement_type: str
    technology_type: str
    technology_platform: str
    data_files: str
    materials: str
    other_materials: str
    samples: str
    characteristic_categories: str
    process_sequence: str
    unit_categories: str
    comments: str
    filename: str

IContext_reflection = _expr1853

def _arrow1868(__unit: None=None) -> IEncodable:
    class ObjectExpr1854(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1855(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("sdo:Dataset")

    class ObjectExpr1856(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("sdo:identifier")

    class ObjectExpr1857(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("sdo:additionalType")

    class ObjectExpr1858(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("sdo:variableMeasured")

    class ObjectExpr1859(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            return helpers_5.encode_string("sdo:measurementTechnique")

    class ObjectExpr1860(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
            return helpers_6.encode_string("sdo:measurementMethod")

    class ObjectExpr1861(IEncodable):
        def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
            return helpers_7.encode_string("sdo:hasPart")

    class ObjectExpr1862(IEncodable):
        def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
            return helpers_8.encode_string("sdo:creator")

    class ObjectExpr1863(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any]) -> Any:
            return helpers_9.encode_string("sdo:about")

    class ObjectExpr1864(IEncodable):
        def Encode(self, helpers_10: IEncoderHelpers_1[Any]) -> Any:
            return helpers_10.encode_string("sdo:comment")

    class ObjectExpr1865(IEncodable):
        def Encode(self, helpers_11: IEncoderHelpers_1[Any]) -> Any:
            return helpers_11.encode_string("sdo:url")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1854()), ("Assay", ObjectExpr1855()), ("identifier", ObjectExpr1856()), ("additionalType", ObjectExpr1857()), ("measurementType", ObjectExpr1858()), ("technologyType", ObjectExpr1859()), ("technologyPlatform", ObjectExpr1860()), ("dataFiles", ObjectExpr1861()), ("performers", ObjectExpr1862()), ("processSequence", ObjectExpr1863()), ("comments", ObjectExpr1864()), ("filename", ObjectExpr1865())])
    class ObjectExpr1867(IEncodable):
        def Encode(self, helpers_12: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_12))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_12.encode_object(arg)

    return ObjectExpr1867()


context_jsonvalue: IEncodable = _arrow1868()

__all__ = ["IContext_reflection", "context_jsonvalue"]

