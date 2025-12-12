from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.reflection import (TypeInfo, string_type, union_type)
from ...fable_modules.fable_library.types import (Array, Union)
from ..data import (Data, Data_reflection)
from ..ontology_annotation import (OntologyAnnotation, OntologyAnnotation_reflection)
from .composite_header import CompositeHeader

def _expr819() -> TypeInfo:
    return union_type("ARCtrl.CompositeCell", [], CompositeCell, lambda: [[("Item", OntologyAnnotation_reflection())], [("Item", string_type)], [("Item1", string_type), ("Item2", OntologyAnnotation_reflection())], [("Item", Data_reflection())]])


class CompositeCell(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Term", "FreeText", "Unitized", "Data"]

    @property
    def is_unitized(self, __unit: None=None) -> bool:
        this: CompositeCell = self
        return True if (this.tag == 2) else False

    @property
    def is_term(self, __unit: None=None) -> bool:
        this: CompositeCell = self
        return True if (this.tag == 0) else False

    @property
    def is_free_text(self, __unit: None=None) -> bool:
        this: CompositeCell = self
        return True if (this.tag == 1) else False

    @property
    def is_data(self, __unit: None=None) -> bool:
        this: CompositeCell = self
        return True if (this.tag == 3) else False

    def GetEmptyCell(self, __unit: None=None) -> CompositeCell:
        this: CompositeCell = self
        if this.tag == 2:
            return CompositeCell.empty_unitized()

        elif this.tag == 1:
            return CompositeCell.empty_free_text()

        elif this.tag == 3:
            return CompositeCell.empty_data()

        else: 
            return CompositeCell.empty_term()


    def GetContent(self, __unit: None=None) -> Array[str]:
        this: CompositeCell = self
        if this.tag == 0:
            oa: OntologyAnnotation = this.fields[0]
            return [oa.NameText, default_arg(oa.TermSourceREF, ""), default_arg(oa.TermAccessionNumber, "")]

        elif this.tag == 2:
            oa_1: OntologyAnnotation = this.fields[1]
            return [this.fields[0], oa_1.NameText, default_arg(oa_1.TermSourceREF, ""), default_arg(oa_1.TermAccessionNumber, "")]

        elif this.tag == 3:
            d: Data = this.fields[0]
            return [default_arg(d.Name, ""), default_arg(d.Format, ""), default_arg(d.SelectorFormat, "")]

        else: 
            return [this.fields[0]]


    def ToUnitizedCell(self, __unit: None=None) -> CompositeCell:
        this: CompositeCell = self
        if this.tag == 1:
            return CompositeCell(2, "", OntologyAnnotation.create(this.fields[0]))

        elif this.tag == 0:
            return CompositeCell(2, "", this.fields[0])

        elif this.tag == 3:
            return CompositeCell(2, "", OntologyAnnotation.create(this.fields[0].NameText))

        else: 
            return this


    def ToTermCell(self, __unit: None=None) -> CompositeCell:
        this: CompositeCell = self
        if this.tag == 2:
            return CompositeCell(0, this.fields[1])

        elif this.tag == 1:
            return CompositeCell(0, OntologyAnnotation.create(this.fields[0]))

        elif this.tag == 3:
            return CompositeCell(0, OntologyAnnotation(this.fields[0].NameText))

        else: 
            return this


    def ToFreeTextCell(self, __unit: None=None) -> CompositeCell:
        this: CompositeCell = self
        if this.tag == 0:
            return CompositeCell(1, this.fields[0].NameText)

        elif this.tag == 2:
            return CompositeCell(1, this.fields[1].NameText)

        elif this.tag == 3:
            return CompositeCell(1, this.fields[0].NameText)

        else: 
            return this


    def ToDataCell(self, __unit: None=None) -> CompositeCell:
        this: CompositeCell = self
        if this.tag == 1:
            return CompositeCell.create_data_from_string(this.fields[0])

        elif this.tag == 0:
            return CompositeCell.create_data_from_string(this.fields[0].NameText)

        elif this.tag == 3:
            return this

        else: 
            return CompositeCell.create_data_from_string(this.fields[1].NameText)


    @property
    def AsUnitized(self, __unit: None=None) -> tuple[str, OntologyAnnotation]:
        this: CompositeCell = self
        if this.tag == 2:
            return (this.fields[0], this.fields[1])

        else: 
            raise Exception("Not a Unitized cell.")


    @property
    def AsTerm(self, __unit: None=None) -> OntologyAnnotation:
        this: CompositeCell = self
        if this.tag == 0:
            return this.fields[0]

        else: 
            raise Exception("Not a Term Cell.")


    @property
    def AsFreeText(self, __unit: None=None) -> str:
        this: CompositeCell = self
        if this.tag == 1:
            return this.fields[0]

        else: 
            raise Exception("Not a FreeText Cell.")


    @property
    def AsData(self, __unit: None=None) -> Data:
        this: CompositeCell = self
        if this.tag == 3:
            return this.fields[0]

        else: 
            raise Exception("Not a Data Cell.")


    @staticmethod
    def create_term(oa: OntologyAnnotation) -> CompositeCell:
        return CompositeCell(0, oa)

    @staticmethod
    def create_term_from_string(name: str | None=None, tsr: str | None=None, tan: str | None=None) -> CompositeCell:
        return CompositeCell(0, OntologyAnnotation.create(name, tsr, tan))

    @staticmethod
    def create_unitized(value: str, oa: OntologyAnnotation | None=None) -> CompositeCell:
        return CompositeCell(2, value, default_arg(oa, OntologyAnnotation()))

    @staticmethod
    def create_unitized_from_string(value: str, name: str | None=None, tsr: str | None=None, tan: str | None=None) -> CompositeCell:
        tupled_arg: tuple[str, OntologyAnnotation] = (value, OntologyAnnotation.create(name, tsr, tan))
        return CompositeCell(2, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def create_free_text(value: str) -> CompositeCell:
        return CompositeCell(1, value)

    @staticmethod
    def create_data(d: Data) -> CompositeCell:
        return CompositeCell(3, d)

    @staticmethod
    def create_data_from_string(value: str, format: str | None=None, selector_format: str | None=None) -> CompositeCell:
        return CompositeCell(3, Data.create(None, value, None, format, selector_format))

    @staticmethod
    def empty_term() -> CompositeCell:
        return CompositeCell(0, OntologyAnnotation())

    @staticmethod
    def empty_free_text() -> CompositeCell:
        return CompositeCell(1, "")

    @staticmethod
    def empty_unitized() -> CompositeCell:
        return CompositeCell(2, "", OntologyAnnotation())

    @staticmethod
    def empty_data() -> CompositeCell:
        return CompositeCell(3, Data.create())

    def UpdateWithOA(self, oa: OntologyAnnotation) -> CompositeCell:
        this: CompositeCell = self
        if this.tag == 2:
            return CompositeCell.create_unitized(this.fields[0], oa)

        elif this.tag == 1:
            return CompositeCell.create_free_text(oa.NameText)

        elif this.tag == 3:
            d: Data = this.fields[0]
            d.Name = oa.NameText
            return CompositeCell(3, d)

        else: 
            return CompositeCell.create_term(oa)


    @staticmethod
    def update_with_oa(oa: OntologyAnnotation, cell: CompositeCell) -> CompositeCell:
        return cell.UpdateWithOA(oa)

    def __str__(self, __unit: None=None) -> str:
        this: CompositeCell = self
        if this.tag == 1:
            return this.fields[0]

        elif this.tag == 2:
            return ((("" + this.fields[0]) + " ") + this.fields[1].NameText) + ""

        elif this.tag == 3:
            return ("" + this.fields[0].NameText) + ""

        else: 
            return ("" + this.fields[0].NameText) + ""


    def Copy(self, __unit: None=None) -> CompositeCell:
        this: CompositeCell = self
        if this.tag == 1:
            return CompositeCell(1, this.fields[0])

        elif this.tag == 2:
            return CompositeCell(2, this.fields[0], this.fields[1].Copy())

        elif this.tag == 3:
            return CompositeCell(3, this.fields[0].Copy())

        else: 
            return CompositeCell(0, this.fields[0].Copy())


    def ValidateAgainstHeader(self, header: CompositeHeader, raise_exception: bool | None=None) -> bool:
        this: CompositeCell = self
        raise_exeption: bool = default_arg(raise_exception, False)
        cell: CompositeCell = this
        if (True if cell.is_data else cell.is_free_text) if header.IsDataColumn else False:
            return True

        elif header.IsDataColumn:
            if raise_exeption:
                raise Exception(((("Invalid combination of header `" + str(header)) + "` and cell `") + str(cell)) + "`, Data header should have either Data or Freetext cells")

            return False

        elif (True if cell.is_term else cell.is_unitized) if header.IsTermColumn else False:
            return True

        elif cell.is_free_text if (not header.IsTermColumn) else False:
            return True

        else: 
            if raise_exeption:
                raise Exception(((("Invalid combination of header `" + str(header)) + "` and cell `") + str(cell)) + "`")

            return False


    @staticmethod
    def term(oa: OntologyAnnotation) -> CompositeCell:
        return CompositeCell(0, oa)

    @staticmethod
    def free_text(s: str) -> CompositeCell:
        return CompositeCell(1, s)

    @staticmethod
    def unitized(v: str, oa: OntologyAnnotation) -> CompositeCell:
        return CompositeCell(2, v, oa)

    @staticmethod
    def data(d: Data) -> CompositeCell:
        return CompositeCell(3, d)


CompositeCell_reflection = _expr819

__all__ = ["CompositeCell_reflection"]

