from __future__ import annotations
from typing import (Any, TypeVar)
from ...fable_library.option import default_arg
from ...fable_library.seq import map
from ...fable_library.util import (to_enumerable, IEnumerable_1)
from ...thoth_json_core.decode import (object, IOptionalGetter, int_1, IGetters)
from ...thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Cells.fs_cell import (FsCell, DataType)
from ..fs_address import FsAddress
from .value import (encode, decode)

__A_ = TypeVar("__A_")

def encode_no_number(cell: FsCell) -> IEncodable:
    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("value", encode(cell.Value))])
    class ObjectExpr297(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], cell: Any=cell) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers.encode_object(arg)

    return ObjectExpr297()


def encode_rows(cell: FsCell) -> IEncodable:
    def _arrow299(__unit: None=None, cell: Any=cell) -> IEncodable:
        value_1: int = cell.ColumnNumber or 0
        class ObjectExpr298(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_signed_integral_number(value_1)

        return ObjectExpr298()

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("column", _arrow299()), ("value", encode(cell.Value))])
    class ObjectExpr300(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], cell: Any=cell) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_1))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_1.encode_object(arg)

    return ObjectExpr300()


def decode_rows(row_number: int | None=None) -> Decoder_1[FsCell]:
    def _arrow303(builder: IGetters, row_number: Any=row_number) -> FsCell:
        def _arrow301(__unit: None=None) -> tuple[Any, DataType] | None:
            object_arg: IOptionalGetter = builder.Optional
            return object_arg.Field("value", decode)

        pattern_input: tuple[Any, DataType] = default_arg(_arrow301(), ("", DataType(4)))
        def _arrow302(__unit: None=None) -> int | None:
            object_arg_1: IOptionalGetter = builder.Optional
            return object_arg_1.Field("column", int_1)

        c: int = default_arg(_arrow302(), 0) or 0
        return FsCell(pattern_input[0], pattern_input[1], FsAddress(default_arg(row_number, 0), c))

    return object(_arrow303)


def encode_cols(cell: FsCell) -> IEncodable:
    def _arrow305(__unit: None=None, cell: Any=cell) -> IEncodable:
        value_1: int = cell.RowNumber or 0
        class ObjectExpr304(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_signed_integral_number(value_1)

        return ObjectExpr304()

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("row", _arrow305()), ("value", encode(cell.Value))])
    class ObjectExpr306(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], cell: Any=cell) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_1))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_1.encode_object(arg)

    return ObjectExpr306()


def decode_cols(col_number: int | None=None) -> Decoder_1[FsCell]:
    def _arrow309(builder: IGetters, col_number: Any=col_number) -> FsCell:
        def _arrow307(__unit: None=None) -> tuple[Any, DataType] | None:
            object_arg: IOptionalGetter = builder.Optional
            return object_arg.Field("value", decode)

        pattern_input: tuple[Any, DataType] = default_arg(_arrow307(), ("", DataType(4)))
        def _arrow308(__unit: None=None) -> int | None:
            object_arg_1: IOptionalGetter = builder.Optional
            return object_arg_1.Field("row", int_1)

        return FsCell(pattern_input[0], pattern_input[1], FsAddress(default_arg(_arrow308(), 0), default_arg(col_number, 0)))

    return object(_arrow309)


__all__ = ["encode_no_number", "encode_rows", "decode_rows", "encode_cols", "decode_cols"]

