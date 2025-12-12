from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Any
from ...fable_library.char import parse as parse_6
from ...fable_library.date import parse as parse_4
from ...fable_library.decimal_ import parse as parse_3
from ...fable_library.double import parse
from ...fable_library.guid import parse as parse_5
from ...fable_library.int32 import parse as parse_1
from ...fable_library.long import parse as parse_2
from ...fable_library.option import (default_arg, map)
from ...fable_library.reflection import (TypeInfo, union_type, class_type)
from ...fable_library.seq import for_all
from ...fable_library.types import (Array, Union, to_string, uint32, int64, uint64)
from ...fable_library.util import (equals, to_enumerable)
from ..fs_address import (FsAddress, CellReference_indexToColAdress)

def _expr75() -> TypeInfo:
    return union_type("FsSpreadsheet.DataType", [], DataType, lambda: [[], [], [], [], []])


class DataType(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["String", "Boolean", "Number", "Date", "Empty"]


DataType_reflection = _expr75

def FsCellAux_boolConverter(bool_1: bool) -> str:
    if bool_1:
        return "1"

    else: 
        return "0"



def _expr76() -> TypeInfo:
    return class_type("FsSpreadsheet.FsCell", None, FsCell)


class FsCell:
    def __init__(self, value: Any=None, data_type: DataType | None=None, address: FsAddress | None=None) -> None:
        self._cellValue: Any = value
        self._dataType: DataType = default_arg(data_type, DataType(0))
        self._comment: str = ""
        self._hyperlink: str = ""
        self._richText: str = ""
        self._formulaA1: str = ""
        self._formulaR1C1: str = ""
        def mapping(a: FsAddress) -> int:
            return a.RowNumber

        self._rowIndex: int = default_arg(map(mapping, address), 1) or 0
        def mapping_1(a_1: FsAddress) -> int:
            return a_1.ColumnNumber

        self._columnIndex: int = default_arg(map(mapping_1, address), 1) or 0

    @property
    def Value(self, __unit: None=None) -> Any:
        self_1: FsCell = self
        return self_1._cellValue

    @Value.setter
    def Value(self, value: Any=None) -> None:
        self_1: FsCell = self
        self_1._cellValue = value

    @property
    def DataType(self, __unit: None=None) -> DataType:
        self_1: FsCell = self
        return self_1._dataType

    @DataType.setter
    def DataType(self, data_type: DataType) -> None:
        self_1: FsCell = self
        self_1._dataType = data_type

    @property
    def ColumnNumber(self, __unit: None=None) -> int:
        self_1: FsCell = self
        return self_1._columnIndex

    @ColumnNumber.setter
    def ColumnNumber(self, col_i: int) -> None:
        self_1: FsCell = self
        self_1._columnIndex = col_i or 0

    @property
    def RowNumber(self, __unit: None=None) -> int:
        self_1: FsCell = self
        return self_1._rowIndex

    @RowNumber.setter
    def RowNumber(self, row_i: int) -> None:
        self_1: FsCell = self
        self_1._rowIndex = row_i or 0

    @property
    def Address(self, __unit: None=None) -> FsAddress:
        self_1: FsCell = self
        return FsAddress(self_1._rowIndex, self_1._columnIndex)

    @Address.setter
    def Address(self, address: FsAddress) -> None:
        self_1: FsCell = self
        self_1._rowIndex = address.RowNumber or 0
        self_1._columnIndex = address.ColumnNumber or 0

    @staticmethod
    def create(row_number: int, col_number: int, value: Any) -> FsCell:
        pattern_input: tuple[DataType, Any]
        value_1_1: Any = value
        pattern_input = ((DataType(0), value_1_1)) if (str(type(value_1_1)) == "<class \'str\'>") else ((((DataType(1), True)) if value_1_1 else ((DataType(1), False))) if (str(type(value_1_1)) == "<class \'bool\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<fable_modules.fable_library.types.uint8\'>>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.int8\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'int\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.int16\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.int64\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.uint32>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.uint16\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.uint32\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.float32\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'float\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'int\'>") else (((DataType(3), value_1_1)) if isinstance(value_1_1, datetime) else (((DataType(0), value_1_1)) if (str(type(value_1_1)) == "<class \'str\'>") else ((DataType(0), value_1_1))))))))))))))))
        return FsCell(pattern_input[1], pattern_input[0], FsAddress(row_number, col_number))

    @staticmethod
    def create_empty(__unit: None=None) -> FsCell:
        return FsCell("", DataType(4), FsAddress(0, 0))

    @staticmethod
    def create_with_adress(adress: FsAddress, value: Any) -> FsCell:
        pattern_input: tuple[DataType, Any]
        value_1_1: Any = value
        pattern_input = ((DataType(0), value_1_1)) if (str(type(value_1_1)) == "<class \'str\'>") else ((((DataType(1), True)) if value_1_1 else ((DataType(1), False))) if (str(type(value_1_1)) == "<class \'bool\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<fable_modules.fable_library.types.uint8\'>>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.int8\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'int\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.int16\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.int64\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.uint32>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.uint16\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.uint32\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.float32\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'float\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'int\'>") else (((DataType(3), value_1_1)) if isinstance(value_1_1, datetime) else (((DataType(0), value_1_1)) if (str(type(value_1_1)) == "<class \'str\'>") else ((DataType(0), value_1_1))))))))))))))))
        return FsCell(pattern_input[1], pattern_input[0], adress)

    @staticmethod
    def create_empty_with_adress(adress: FsAddress) -> FsCell:
        return FsCell("", DataType(4), adress)

    @staticmethod
    def create_with_data_type(data_type: DataType, row_number: int, col_number: int, value: Any=None) -> FsCell:
        return FsCell(value, data_type, FsAddress(row_number, col_number))

    def __str__(self, __unit: None=None) -> str:
        self_1: FsCell = self
        return ((((((("" + CellReference_indexToColAdress(int(self_1.ColumnNumber+0x100000000 if self_1.ColumnNumber < 0 else self_1.ColumnNumber))) + "") + str(self_1.RowNumber)) + " : ") + str(self_1.Value)) + " | ") + str(self_1.DataType)) + ""

    def CopyFrom(self, other_cell: FsCell) -> None:
        self_1: FsCell = self
        self_1.DataType = other_cell.DataType
        self_1.Value = other_cell.Value

    def CopyTo(self, target: FsCell) -> None:
        self_1: FsCell = self
        target.DataType = self_1.DataType
        target.Value = self_1.Value

    @staticmethod
    def copy_from_to(source_cell: FsCell, target_cell: FsCell) -> FsCell:
        target_cell.DataType = source_cell.DataType
        target_cell.Value = source_cell.Value
        return target_cell

    def Copy(self, __unit: None=None) -> FsCell:
        self_1: FsCell = self
        return FsCell(self_1.Value, self_1.DataType, self_1.Address.Copy())

    @staticmethod
    def copy(cell: FsCell) -> FsCell:
        return cell.Copy()

    def ValueAsString(self, __unit: None=None) -> str:
        self_1: FsCell = self
        v: Any = self_1.Value
        match_value: DataType = self_1.DataType
        if ((match_value.tag == 3) or (match_value.tag == 1)) or (match_value.tag == 4):
            return to_string(v)

        elif match_value.tag == 2:
            return to_string(v)

        else: 
            return to_string(v)


    @staticmethod
    def get_value_as_string(cell: FsCell) -> str:
        return cell.ValueAsString()

    def ValueAsBool(self, __unit: None=None) -> bool:
        self_1: FsCell = self
        match_value: str = to_string(self_1.Value).lower()
        (pattern_matching_result,) = (None,)
        if match_value == "1":
            pattern_matching_result = 0

        elif match_value == "true":
            pattern_matching_result = 0

        elif match_value == "true()":
            pattern_matching_result = 0

        elif match_value == "0":
            pattern_matching_result = 1

        elif match_value == "false":
            pattern_matching_result = 1

        elif match_value == "false()":
            pattern_matching_result = 1

        else: 
            pattern_matching_result = 2

        if pattern_matching_result == 0:
            return True

        elif pattern_matching_result == 1:
            return False

        elif pattern_matching_result == 2:
            raise Exception(("String \'" + match_value) + "\' was not recognized as a valid Boolean")


    @staticmethod
    def get_value_as_bool(cell: FsCell) -> bool:
        return cell.ValueAsBool()

    def ValueAsFloat(self, __unit: None=None) -> float:
        self_1: FsCell = self
        return parse(to_string(self_1.Value))

    @staticmethod
    def get_value_as_float(cell: FsCell) -> float:
        return cell.ValueAsFloat()

    def ValueAsInt(self, __unit: None=None) -> int:
        self_1: FsCell = self
        return parse_1(to_string(self_1.Value), 511, False, 32)

    @staticmethod
    def get_value_as_int(cell: FsCell) -> int:
        return cell.ValueAsInt()

    def ValueAsUInt(self, __unit: None=None) -> uint32:
        self_1: FsCell = self
        return parse_1(to_string(self_1.Value), 511, True, 32)

    @staticmethod
    def get_value_as_uint(cell: FsCell) -> uint32:
        return cell.ValueAsUInt()

    def ValueAsLong(self, __unit: None=None) -> int64:
        self_1: FsCell = self
        return parse_2(to_string(self_1.Value), 511, False, 64)

    @staticmethod
    def get_value_as_long(cell: FsCell) -> int64:
        return cell.ValueAsLong()

    def ValueAsULong(self, __unit: None=None) -> uint64:
        self_1: FsCell = self
        return parse_2(to_string(self_1.Value), 511, True, 64)

    @staticmethod
    def get_value_as_ulong(cell: FsCell) -> uint64:
        return cell.ValueAsULong()

    def ValueAsDouble(self, __unit: None=None) -> float:
        self_1: FsCell = self
        return parse(to_string(self_1.Value))

    @staticmethod
    def get_value_as_double(cell: FsCell) -> float:
        return cell.ValueAsDouble()

    def ValueAsDecimal(self, __unit: None=None) -> Decimal:
        self_1: FsCell = self
        return parse_3(to_string(self_1.Value))

    @staticmethod
    def get_value_as_decimal(cell: FsCell) -> Decimal:
        return cell.ValueAsDecimal()

    def ValueAsDateTime(self, __unit: None=None) -> Any:
        self_1: FsCell = self
        return parse_4(to_string(self_1.Value))

    @staticmethod
    def get_value_as_date_time(cell: FsCell) -> Any:
        return cell.ValueAsDateTime()

    def ValueAsGuid(self, __unit: None=None) -> str:
        self_1: FsCell = self
        return parse_5(to_string(self_1.Value))

    @staticmethod
    def get_value_as_guid(cell: FsCell) -> str:
        return cell.ValueAsGuid()

    def ValueAsChar(self, __unit: None=None) -> str:
        self_1: FsCell = self
        return parse_6(to_string(self_1.Value))

    @staticmethod
    def get_value_as_char(cell: FsCell) -> str:
        return cell.ValueAsChar()

    def SetValueAs(self, value: Any=None) -> None:
        self_1: FsCell = self
        pattern_input: tuple[DataType, Any]
        value_1_1: Any = value
        pattern_input = ((DataType(0), value_1_1)) if (str(type(value_1_1)) == "<class \'str\'>") else ((((DataType(1), True)) if value_1_1 else ((DataType(1), False))) if (str(type(value_1_1)) == "<class \'bool\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<fable_modules.fable_library.types.uint8\'>>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.int8\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'int\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.int16\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.int64\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.uint32>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.uint16\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.uint32\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'fable_modules.fable_library.types.float32\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'float\'>") else (((DataType(2), value_1_1)) if (str(type(value_1_1)) == "<class \'int\'>") else (((DataType(3), value_1_1)) if isinstance(value_1_1, datetime) else (((DataType(0), value_1_1)) if (str(type(value_1_1)) == "<class \'str\'>") else ((DataType(0), value_1_1))))))))))))))))
        self_1._dataType = pattern_input[0]
        self_1._cellValue = pattern_input[1]

    @staticmethod
    def set_value_as(value: Any, cell: FsCell) -> FsCell:
        cell.SetValueAs(value)
        return cell

    def StructurallyEquals(self, other: FsCell) -> bool:
        this: FsCell = self
        def predicate_1(x_1: bool) -> bool:
            return x_1 == True

        def predicate(x: bool) -> bool:
            return x == True

        return for_all(predicate_1, to_enumerable([equals(this.Value, other.Value), equals(this.DataType, other.DataType), for_all(predicate, to_enumerable([this.Address.Address == other.Address.Address, this.Address.ColumnNumber == other.Address.ColumnNumber, this.Address.RowNumber == other.Address.RowNumber, this.Address.FixedColumn == other.Address.FixedColumn, this.Address.FixedRow == other.Address.FixedRow])), this.ColumnNumber == other.ColumnNumber, this.RowNumber == other.RowNumber]))


FsCell_reflection = _expr76

def FsCell__ctor_2BEF9BB0(value: Any=None, data_type: DataType | None=None, address: FsAddress | None=None) -> FsCell:
    return FsCell(value, data_type, address)


__all__ = ["DataType_reflection", "FsCellAux_boolConverter", "FsCell_reflection"]

