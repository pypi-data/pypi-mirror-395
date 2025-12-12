from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.option import (map, bind, default_arg)
from ...fable_modules.fable_library.types import Array
from ...Core.Helper.collections_ import Option_fromValueWithDefault
from ...Core.Table.composite_cell import CompositeCell

def term_from_string_cells(tsr_col: int | None, tan_col: int | None, cell_values: Array[str]) -> CompositeCell:
    def _arrow1446(i: int, tsr_col: Any=tsr_col, tan_col: Any=tan_col, cell_values: Any=cell_values) -> str:
        return cell_values[i]

    tan: str | None = map(_arrow1446, tan_col)
    def _arrow1447(i_1: int, tsr_col: Any=tsr_col, tan_col: Any=tan_col, cell_values: Any=cell_values) -> str:
        return cell_values[i_1]

    tsr: str | None = map(_arrow1447, tsr_col)
    return CompositeCell.create_term_from_string(cell_values[0], tsr, tan)


def unitized_from_string_cells(unit_col: int, tsr_col: int | None, tan_col: int | None, cell_values: Array[str]) -> CompositeCell:
    unit: str = cell_values[unit_col]
    def _arrow1448(i: int, unit_col: Any=unit_col, tsr_col: Any=tsr_col, tan_col: Any=tan_col, cell_values: Any=cell_values) -> str:
        return cell_values[i]

    tan: str | None = map(_arrow1448, tan_col)
    def _arrow1449(i_1: int, unit_col: Any=unit_col, tsr_col: Any=tsr_col, tan_col: Any=tan_col, cell_values: Any=cell_values) -> str:
        return cell_values[i_1]

    tsr: str | None = map(_arrow1449, tsr_col)
    return CompositeCell.create_unitized_from_string(cell_values[0], unit, tsr, tan)


def free_text_from_string_cells(cell_values: Array[str]) -> CompositeCell:
    return CompositeCell.create_free_text(cell_values[0])


def data_from_string_cells(format: int | None, selector_format: int | None, cell_values: Array[str]) -> CompositeCell:
    def _arrow1450(i: int, format: Any=format, selector_format: Any=selector_format, cell_values: Any=cell_values) -> str | None:
        return Option_fromValueWithDefault("", cell_values[i])

    format_1: str | None = bind(_arrow1450, format)
    def _arrow1451(i_1: int, format: Any=format, selector_format: Any=selector_format, cell_values: Any=cell_values) -> str | None:
        return Option_fromValueWithDefault("", cell_values[i_1])

    selector_format_1: str | None = bind(_arrow1451, selector_format)
    return CompositeCell.create_data_from_string(cell_values[0], format_1, selector_format_1)


def to_string_cells(is_term: bool, has_unit: bool, cell: CompositeCell) -> Array[str]:
    if cell.tag == 0:
        if has_unit:
            return [cell.fields[0].NameText, "", default_arg(cell.fields[0].TermSourceREF, ""), cell.fields[0].TermAccessionOntobeeUrl]

        else: 
            return [cell.fields[0].NameText, default_arg(cell.fields[0].TermSourceREF, ""), cell.fields[0].TermAccessionOntobeeUrl]


    elif cell.tag == 2:
        return [cell.fields[0], cell.fields[1].NameText, default_arg(cell.fields[1].TermSourceREF, ""), cell.fields[1].TermAccessionOntobeeUrl]

    elif cell.tag == 3:
        format: str = default_arg(cell.fields[0].Format, "")
        selector_format: str = default_arg(cell.fields[0].SelectorFormat, "")
        return [default_arg(cell.fields[0].Name, ""), format, selector_format]

    elif has_unit:
        return [cell.fields[0], "", "", ""]

    elif is_term:
        return [cell.fields[0], "", ""]

    else: 
        return [cell.fields[0]]



__all__ = ["term_from_string_cells", "unitized_from_string_cells", "free_text_from_string_cells", "data_from_string_cells", "to_string_cells"]

