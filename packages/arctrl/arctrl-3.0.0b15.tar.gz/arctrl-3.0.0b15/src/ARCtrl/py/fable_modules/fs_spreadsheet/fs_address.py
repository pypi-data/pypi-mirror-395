from __future__ import annotations
from collections.abc import Callable
from math import pow
from typing import Any
from ..fable_library.char import (char_code_at, is_letter, is_digit)
from ..fable_library.int32 import parse
from ..fable_library.long import (op_addition, from_integer, to_int)
from ..fable_library.option import value as value_2
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_library.reg_exp import create
from ..fable_library.seq import iterate
from ..fable_library.string_ import (to_text, printf, to_fail)
from ..fable_library.system_text import (StringBuilder__ctor, StringBuilder__Append_244C7CD6)
from ..fable_library.types import (uint32, to_string, int64)
from ..fable_library.util import (ignore, string_hash, identity_hash)
from .hash_codes import merge_hashes

CellReference_indexRegex: Any = create("([A-Z]*)(\\d*)")

def CellReference_colAdressToIndex(column_adress: str) -> uint32:
    length: int = len(column_adress) or 0
    sum: uint32 = uint32(0)
    for i in range(0, (length - 1) + 1, 1):
        c_1: str
        c: str = column_adress[(length - 1) - i]
        c_1 = c.upper()
        factor: uint32
        value: float = pow(26.0, i)
        factor = int(value+0x100000000 if value < 0 else value)
        sum = sum + (((int(char_code_at(c_1, 0)+0x100000000 if char_code_at(c_1, 0) < 0 else char_code_at(c_1, 0))) - uint32(64)) * factor)
    return sum


def CellReference_indexToColAdress(i: uint32) -> str:
    def loop(index_mut: uint32, acc_mut: str, i: Any=i) -> str:
        while True:
            (index, acc) = (index_mut, acc_mut)
            if index == uint32(0):
                return acc

            else: 
                mod26: uint32 = (index - uint32(1)) % uint32(26)
                index_mut = (index - uint32(1)) // uint32(26)
                acc_mut = chr((int(char_code_at("A", 0)+0x100000000 if char_code_at("A", 0) < 0 else char_code_at("A", 0))) + mod26) + acc
                continue

            break

    return loop(i, "")


def CellReference_ofIndices(column: uint32, row: uint32) -> str:
    arg: str = CellReference_indexToColAdress(column)
    return to_text(printf("%s%i"))(arg)(row)


def CellReference_toIndices(reference: str) -> tuple[uint32, uint32]:
    char_part: Any = StringBuilder__ctor()
    num_part: Any = StringBuilder__ctor()
    def action(c: str, reference: Any=reference) -> None:
        if is_letter(c):
            ignore(StringBuilder__Append_244C7CD6(char_part, c))

        elif is_digit(c):
            ignore(StringBuilder__Append_244C7CD6(num_part, c))

        else: 
            to_fail(printf("Reference %s does not match Excel A1-style"))(reference)


    iterate(action, reference)
    return (CellReference_colAdressToIndex(to_string(char_part)), parse(to_string(num_part), 511, True, 32))


def CellReference_toColIndex(reference: str) -> uint32:
    return CellReference_toIndices(reference)[0]


def CellReference_toRowIndex(reference: str) -> uint32:
    return CellReference_toIndices(reference)[1]


def CellReference_setColIndex(col_i: uint32, reference: str) -> str:
    return CellReference_ofIndices(col_i, CellReference_toIndices(reference)[1])


def CellReference_setRowIndex(row_i: uint32, reference: str) -> str:
    return CellReference_ofIndices(CellReference_toIndices(reference)[0], row_i)


def CellReference_moveHorizontal(amount: int, reference: str) -> str:
    tupled_arg_1: tuple[uint32, uint32]
    tupled_arg: tuple[uint32, uint32] = CellReference_toIndices(reference)
    def _arrow70(__unit: None=None, amount: Any=amount, reference: Any=reference) -> uint32:
        value: int64 = op_addition(from_integer(tupled_arg[0], False, 6), from_integer(amount, False, 2))
        return int(to_int(value)+0x100000000 if to_int(value) < 0 else to_int(value))

    tupled_arg_1 = (_arrow70(), tupled_arg[1])
    return CellReference_ofIndices(tupled_arg_1[0], tupled_arg_1[1])


def CellReference_moveVertical(amount: int, reference: str) -> str:
    tupled_arg_1: tuple[uint32, uint32]
    tupled_arg: tuple[uint32, uint32] = CellReference_toIndices(reference)
    def _arrow71(__unit: None=None, amount: Any=amount, reference: Any=reference) -> uint32:
        value: int64 = op_addition(from_integer(tupled_arg[1], False, 6), from_integer(amount, False, 2))
        return int(to_int(value)+0x100000000 if to_int(value) < 0 else to_int(value))

    tupled_arg_1 = (tupled_arg[0], _arrow71())
    return CellReference_ofIndices(tupled_arg_1[0], tupled_arg_1[1])


def _expr74() -> TypeInfo:
    return class_type("FsSpreadsheet.FsAddress", None, FsAddress)


class FsAddress:
    def __init__(self, row_number: int, column_number: int, fixed_row: bool | None=None, fixed_column: bool | None=None) -> None:
        self._fixedRow: bool = value_2(fixed_row) if (fixed_row is not None) else False
        self._fixedColumn: bool = value_2(fixed_column) if (fixed_column is not None) else False
        self._rowNumber: int = row_number or 0
        self._columnNumber: int = column_number or 0
        self._trimmedAddress: str = ""

    @staticmethod
    def from_string(cell_address_string: str, fixed_row: bool | None=None, fixed_column: bool | None=None) -> FsAddress:
        pattern_input: tuple[uint32, uint32] = CellReference_toIndices(cell_address_string)
        return FsAddress(int(pattern_input[1]), int(pattern_input[0]), fixed_row, fixed_column)

    @property
    def ColumnNumber(self, __unit: None=None) -> int:
        self_1: FsAddress = self
        return self_1._columnNumber

    @ColumnNumber.setter
    def ColumnNumber(self, col_i: int) -> None:
        self_1: FsAddress = self
        self_1._columnNumber = col_i or 0

    @property
    def RowNumber(self, __unit: None=None) -> int:
        self_1: FsAddress = self
        return self_1._rowNumber

    @RowNumber.setter
    def RowNumber(self, row_i: int) -> None:
        self_1: FsAddress = self
        self_1._rowNumber = row_i or 0

    @property
    def Address(self, __unit: None=None) -> str:
        self_1: FsAddress = self
        return CellReference_ofIndices(int(self_1._columnNumber+0x100000000 if self_1._columnNumber < 0 else self_1._columnNumber), int(self_1._rowNumber+0x100000000 if self_1._rowNumber < 0 else self_1._rowNumber))

    @Address.setter
    def Address(self, address: str) -> None:
        self_1: FsAddress = self
        pattern_input: tuple[uint32, uint32] = CellReference_toIndices(address)
        self_1._rowNumber = int(pattern_input[1]) or 0
        self_1._columnNumber = int(pattern_input[0]) or 0

    @property
    def FixedRow(self, __unit: None=None) -> bool:
        return False

    @property
    def FixedColumn(self, __unit: None=None) -> bool:
        return False

    def Copy(self, __unit: None=None) -> FsAddress:
        this: FsAddress = self
        col_no: int = this.ColumnNumber or 0
        return FsAddress(this.RowNumber, col_no, this.FixedRow, this.FixedColumn)

    @staticmethod
    def copy(address: FsAddress) -> FsAddress:
        return address.Copy()

    def UpdateIndices(self, row_index: int, col_index: int) -> None:
        self_1: FsAddress = self
        self_1._columnNumber = col_index or 0
        self_1._rowNumber = row_index or 0

    @staticmethod
    def update_indices(row_index: int, col_index: int, address: FsAddress) -> FsAddress:
        address.UpdateIndices(row_index, col_index)
        return address

    def ToIndices(self, __unit: None=None) -> tuple[int, int]:
        self_1: FsAddress = self
        return (self_1._rowNumber, self_1._columnNumber)

    @staticmethod
    def to_indices(address: FsAddress) -> tuple[int, int]:
        return address.ToIndices()

    def Compare(self, address: FsAddress) -> bool:
        self_1: FsAddress = self
        return (self_1.FixedRow == address.FixedRow) if ((self_1.FixedColumn == address.FixedColumn) if ((self_1.RowNumber == address.RowNumber) if ((self_1.ColumnNumber == address.ColumnNumber) if (self_1.Address == address.Address) else False) else False) else False) else False

    @staticmethod
    def compare(address1: FsAddress, address2: FsAddress) -> bool:
        return address1.Compare(address2)

    def __hash__(self, __unit: None=None) -> int:
        this: FsAddress = self
        hash_8: int
        hash_6: int
        hash_4: int
        hash_2: int = string_hash(this.Address) or 0
        hash_4 = merge_hashes(this.ColumnNumber, hash_2)
        hash_6 = merge_hashes(this.RowNumber, hash_4)
        def _arrow72(__unit: None=None) -> int:
            copy_of_struct: bool = this.FixedColumn
            return identity_hash(copy_of_struct)

        hash_8 = merge_hashes(_arrow72(), hash_6)
        def _arrow73(__unit: None=None) -> int:
            copy_of_struct_1: bool = this.FixedRow
            return identity_hash(copy_of_struct_1)

        return merge_hashes(_arrow73(), hash_8)

    def __eq__(self, other: Any=None) -> bool:
        this: FsAddress = self
        return this.Compare(other) if isinstance(other, FsAddress) else False


FsAddress_reflection = _expr74

def FsAddress__ctor_42410CA0(row_number: int, column_number: int, fixed_row: bool | None=None, fixed_column: bool | None=None) -> FsAddress:
    return FsAddress(row_number, column_number, fixed_row, fixed_column)


__all__ = ["CellReference_indexRegex", "CellReference_colAdressToIndex", "CellReference_indexToColAdress", "CellReference_ofIndices", "CellReference_toIndices", "CellReference_toColIndex", "CellReference_toRowIndex", "CellReference_setColIndex", "CellReference_setRowIndex", "CellReference_moveHorizontal", "CellReference_moveVertical", "FsAddress_reflection"]

