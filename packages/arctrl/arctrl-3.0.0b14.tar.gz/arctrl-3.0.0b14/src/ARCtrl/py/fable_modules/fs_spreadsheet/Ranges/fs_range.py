from __future__ import annotations
from typing import Any
from ...fable_library.option import some
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.string_ import (to_text, printf)
from ...fable_library.util import int32_to_string
from ..fs_address import FsAddress
from .fs_range_address import FsRangeAddress
from .fs_range_base import (FsRangeBase, FsRangeBase_reflection)
from .fs_range_row import FsRangeRow

def _expr185() -> TypeInfo:
    return class_type("FsSpreadsheet.FsRange", None, FsRange, FsRangeBase_reflection())


class FsRange(FsRangeBase):
    def __init__(self, range_address: FsRangeAddress, style_value: Any | None=None) -> None:
        super().__init__(range_address)
        pass

    @staticmethod
    def from_range_base(range_base: FsRangeBase) -> FsRange:
        return FsRange(range_base.RangeAddress, some(None))

    def Row(self, row: int) -> FsRangeRow:
        if True if (row <= 0) else (((row + super().RangeAddress.FirstAddress.RowNumber) - 1) > 1048576):
            raise Exception(int32_to_string(row), to_text(printf("Row number must be between 1 and %i"))(1048576))

        return FsRangeRow(FsRangeAddress(FsAddress((super().RangeAddress.FirstAddress.RowNumber + row) - 1, super().RangeAddress.FirstAddress.ColumnNumber), FsAddress((super().RangeAddress.FirstAddress.RowNumber + row) - 1, super().RangeAddress.LastAddress.ColumnNumber)))

    def FirstRow(self, __unit: None=None) -> FsRangeRow:
        self_1: FsRange = self
        return self_1.Row(1)


FsRange_reflection = _expr185

def FsRange__ctor_Z15E90CDC(range_address: FsRangeAddress, style_value: Any | None=None) -> FsRange:
    return FsRange(range_address, style_value)


__all__ = ["FsRange_reflection"]

