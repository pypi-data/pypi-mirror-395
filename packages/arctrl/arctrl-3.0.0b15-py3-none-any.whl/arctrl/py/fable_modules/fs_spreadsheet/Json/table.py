from __future__ import annotations
from typing import (Any, TypeVar)
from ...fable_library.seq import map
from ...fable_library.util import (to_enumerable, IEnumerable_1)
from ...thoth_json_core.decode import (object, IRequiredGetter, string, IGetters)
from ...thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Ranges.fs_range_address import FsRangeAddress
from ..Tables.fs_table import FsTable

__A_ = TypeVar("__A_")

def encode(sheet: FsTable) -> IEncodable:
    def _arrow323(__unit: None=None, sheet: Any=sheet) -> IEncodable:
        value: str = sheet.Name
        class ObjectExpr322(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr322()

    def _arrow325(__unit: None=None, sheet: Any=sheet) -> IEncodable:
        value_1: str = sheet.RangeAddress.Range
        class ObjectExpr324(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr324()

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("name", _arrow323()), ("range", _arrow325())])
    class ObjectExpr326(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], sheet: Any=sheet) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_2))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_2.encode_object(arg)

    return ObjectExpr326()


def _arrow327(builder: IGetters) -> FsTable:
    n: str
    object_arg: IRequiredGetter = builder.Required
    n = object_arg.Field("name", string)
    r: str
    object_arg_1: IRequiredGetter = builder.Required
    r = object_arg_1.Field("range", string)
    return FsTable(n, FsRangeAddress.from_string(r))


decode: Decoder_1[FsTable] = object(_arrow327)

__all__ = ["encode", "decode"]

