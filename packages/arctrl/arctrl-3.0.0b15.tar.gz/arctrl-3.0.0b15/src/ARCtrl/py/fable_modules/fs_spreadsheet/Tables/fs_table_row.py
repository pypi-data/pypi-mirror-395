from __future__ import annotations
from ...fable_library.reflection import (TypeInfo, class_type)
from ..Ranges.fs_range_address import FsRangeAddress
from ..Ranges.fs_range_row import (FsRangeRow, FsRangeRow_reflection)

def _expr202() -> TypeInfo:
    return class_type("FsSpreadsheet.FsTableRow", None, FsTableRow, FsRangeRow_reflection())


class FsTableRow(FsRangeRow):
    def __init__(self, range_address: FsRangeAddress) -> None:
        super().__init__(range_address)
        pass


FsTableRow_reflection = _expr202

def FsTableRow__ctor_6A2513BC(range_address: FsRangeAddress) -> FsTableRow:
    return FsTableRow(range_address)


__all__ = ["FsTableRow_reflection"]

