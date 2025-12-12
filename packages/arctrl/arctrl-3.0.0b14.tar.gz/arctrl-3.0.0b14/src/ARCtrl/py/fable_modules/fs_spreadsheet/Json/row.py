from __future__ import annotations
from typing import (Any, TypeVar)
from ...fable_library.option import default_arg
from ...fable_library.seq import (map, empty)
from ...fable_library.util import (to_enumerable, IEnumerable_1)
from ...thoth_json_core.decode import (object, IOptionalGetter, int_1, seq as seq_1, IGetters)
from ...thoth_json_core.encode import seq
from ...thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Cells.fs_cell import FsCell
from ..fs_row import FsRow
from .cell import (encode_rows, encode_no_number, decode_rows)

__A_ = TypeVar("__A_")

def encode(row: FsRow) -> IEncodable:
    def _arrow311(__unit: None=None, row: Any=row) -> IEncodable:
        value: int = row.Index or 0
        class ObjectExpr310(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_signed_integral_number(value)

        return ObjectExpr310()

    def mapping(cell: FsCell, row: Any=row) -> IEncodable:
        return encode_rows(cell)

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("number", _arrow311()), ("cells", seq(map(mapping, row.Cells)))])
    class ObjectExpr312(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], row: Any=row) -> Any:
            def mapping_1(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_1))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping_1, values)
            return helpers_1.encode_object(arg)

    return ObjectExpr312()


def encode_no_numbers(row: IEnumerable_1[FsCell]) -> IEncodable:
    def mapping(cell: FsCell, row: Any=row) -> IEncodable:
        return encode_no_number(cell)

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("cells", seq(map(mapping, row)))])
    class ObjectExpr313(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], row: Any=row) -> Any:
            def mapping_1(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping_1, values)
            return helpers.encode_object(arg)

    return ObjectExpr313()


def _arrow315(builder: IGetters) -> tuple[int | None, IEnumerable_1[FsCell]]:
    n: int | None
    object_arg: IOptionalGetter = builder.Optional
    n = object_arg.Field("number", int_1)
    def _arrow314(__unit: None=None) -> IEnumerable_1[FsCell] | None:
        arg_3: Decoder_1[IEnumerable_1[FsCell]] = seq_1(decode_rows(n))
        object_arg_1: IOptionalGetter = builder.Optional
        return object_arg_1.Field("cells", arg_3)

    return (n, default_arg(_arrow314(), empty()))


decode: Decoder_1[tuple[int | None, IEnumerable_1[FsCell]]] = object(_arrow315)

__all__ = ["encode", "encode_no_numbers", "decode"]

