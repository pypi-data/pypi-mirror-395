from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.types import Array
from .comment import Comment
from .data import (Data, Data_reflection)
from .data_file import DataFile
from .Helper.hash_codes import (box_hash_array, box_hash_option, box_hash_seq, hash_1)
from .ontology_annotation import OntologyAnnotation
from .value import Value as Value_1

def _expr729() -> TypeInfo:
    return class_type("ARCtrl.DataContext", None, DataContext, Data_reflection())


class DataContext(Data):
    def __init__(self, id: str | None=None, name: str | None=None, data_type: DataFile | None=None, format: str | None=None, selector_format: str | None=None, explication: OntologyAnnotation | None=None, unit: OntologyAnnotation | None=None, object_type: OntologyAnnotation | None=None, label: str | None=None, description: str | None=None, generated_by: str | None=None, comments: Array[Comment] | None=None) -> None:
        super().__init__(id, name, data_type, format, selector_format, comments)
        self._explication: OntologyAnnotation | None = explication
        self._unit: OntologyAnnotation | None = unit
        self._objectType: OntologyAnnotation | None = object_type
        self._label: str | None = label
        self._description: str | None = description
        self._generatedBy: str | None = generated_by

    def __hash__(self, __unit: None=None) -> Any:
        this: DataContext = self
        return box_hash_array([box_hash_option(this.ID), box_hash_option(this.Name), box_hash_option(this.DataType), box_hash_option(this.Format), box_hash_option(this.SelectorFormat), box_hash_seq(this.Comments), box_hash_option(DataContext__get_Explication(this)), box_hash_option(DataContext__get_Unit(this)), box_hash_option(DataContext__get_ObjectType(this)), box_hash_option(DataContext__get_Label(this)), box_hash_option(DataContext__get_Description(this)), box_hash_option(DataContext__get_GeneratedBy(this))])

    def __eq__(self, obj: Any=None) -> bool:
        this: DataContext = self
        return hash_1(this) == hash_1(obj)

    def AlternateName(self, __unit: None=None) -> str | None:
        this: DataContext = self
        return DataContext__get_Label(this)

    def MeasurementMethod(self, __unit: None=None) -> str | None:
        this: DataContext = self
        return DataContext__get_GeneratedBy(this)

    def GetCategory(self, __unit: None=None) -> OntologyAnnotation | None:
        this: DataContext = self
        return DataContext__get_Explication(this)

    def GetValue(self, __unit: None=None) -> Value_1 | None:
        this: DataContext = self
        def mapping(Item: OntologyAnnotation) -> Value_1:
            return Value_1(0, Item)

        return map(mapping, DataContext__get_ObjectType(this))

    def GetUnit(self, __unit: None=None) -> OntologyAnnotation | None:
        this: DataContext = self
        return DataContext__get_Unit(this)

    def GetAdditionalType(self, __unit: None=None) -> str:
        return "DataContext"

    def Description(self, __unit: None=None) -> str | None:
        this: DataContext = self
        return DataContext__get_Description(this)


DataContext_reflection = _expr729

def DataContext__ctor_Z780A8A2A(id: str | None=None, name: str | None=None, data_type: DataFile | None=None, format: str | None=None, selector_format: str | None=None, explication: OntologyAnnotation | None=None, unit: OntologyAnnotation | None=None, object_type: OntologyAnnotation | None=None, label: str | None=None, description: str | None=None, generated_by: str | None=None, comments: Array[Comment] | None=None) -> DataContext:
    return DataContext(id, name, data_type, format, selector_format, explication, unit, object_type, label, description, generated_by, comments)


def DataContext__get_Explication(this: DataContext) -> OntologyAnnotation | None:
    return this._explication


def DataContext__set_Explication_279AAFF2(this: DataContext, explication: OntologyAnnotation | None=None) -> None:
    this._explication = explication


def DataContext__get_Unit(this: DataContext) -> OntologyAnnotation | None:
    return this._unit


def DataContext__set_Unit_279AAFF2(this: DataContext, unit: OntologyAnnotation | None=None) -> None:
    this._unit = unit


def DataContext__get_ObjectType(this: DataContext) -> OntologyAnnotation | None:
    return this._objectType


def DataContext__set_ObjectType_279AAFF2(this: DataContext, object_type: OntologyAnnotation | None=None) -> None:
    this._objectType = object_type


def DataContext__get_Label(this: DataContext) -> str | None:
    return this._label


def DataContext__set_Label_6DFDD678(this: DataContext, label: str | None=None) -> None:
    this._label = label


def DataContext__get_Description(this: DataContext) -> str | None:
    return this._description


def DataContext__set_Description_6DFDD678(this: DataContext, description: str | None=None) -> None:
    this._description = description


def DataContext__get_GeneratedBy(this: DataContext) -> str | None:
    return this._generatedBy


def DataContext__set_GeneratedBy_6DFDD678(this: DataContext, generated_by: str | None=None) -> None:
    this._generatedBy = generated_by


def DataContext__AsData(this: DataContext) -> Data:
    return Data(this.ID, this.Name, this.DataType, this.Format, this.SelectorFormat, this.Comments)


def DataContext_fromData_Z7B4D7BF5(data: Data, explication: OntologyAnnotation | None=None, unit: OntologyAnnotation | None=None, object_type: OntologyAnnotation | None=None, label: str | None=None, description: str | None=None, generated_by: str | None=None) -> DataContext:
    return DataContext__ctor_Z780A8A2A(data.ID, data.Name, data.DataType, data.Format, data.SelectorFormat, explication, unit, object_type, label, description, generated_by, data.Comments)


def DataContext_createAsPV(alternate_name: str | None=None, measurement_method: str | None=None, description: str | None=None, category: OntologyAnnotation | None=None, value: Value_1 | None=None, unit: OntologyAnnotation | None=None) -> DataContext:
    def _arrow730(__unit: None=None, alternate_name: Any=alternate_name, measurement_method: Any=measurement_method, description: Any=description, category: Any=category, value: Any=value, unit: Any=unit) -> OntologyAnnotation | None:
        oa: OntologyAnnotation = value.fields[0]
        return oa

    def _arrow731(__unit: None=None, alternate_name: Any=alternate_name, measurement_method: Any=measurement_method, description: Any=description, category: Any=category, value: Any=value, unit: Any=unit) -> OntologyAnnotation | None:
        v: Value_1 = value
        return OntologyAnnotation(v.Text)

    return DataContext__ctor_Z780A8A2A(None, None, None, None, None, category, unit, None if (value is None) else (_arrow730() if (value.tag == 0) else _arrow731()), alternate_name, description, measurement_method)


def DataContext__Copy(this: DataContext) -> DataContext:
    copy: DataContext = DataContext__ctor_Z780A8A2A()
    copy.ID = this.ID
    copy.Name = this.Name
    copy.DataType = this.DataType
    copy.Format = this.Format
    copy.SelectorFormat = this.SelectorFormat
    DataContext__set_Explication_279AAFF2(copy, DataContext__get_Explication(this))
    DataContext__set_Unit_279AAFF2(copy, DataContext__get_Unit(this))
    DataContext__set_ObjectType_279AAFF2(copy, DataContext__get_ObjectType(this))
    DataContext__set_Description_6DFDD678(copy, DataContext__get_Description(this))
    DataContext__set_GeneratedBy_6DFDD678(copy, DataContext__get_GeneratedBy(this))
    copy.Comments = this.Comments
    return copy


__all__ = ["DataContext_reflection", "DataContext__get_Explication", "DataContext__set_Explication_279AAFF2", "DataContext__get_Unit", "DataContext__set_Unit_279AAFF2", "DataContext__get_ObjectType", "DataContext__set_ObjectType_279AAFF2", "DataContext__get_Label", "DataContext__set_Label_6DFDD678", "DataContext__get_Description", "DataContext__set_Description_6DFDD678", "DataContext__get_GeneratedBy", "DataContext__set_GeneratedBy_6DFDD678", "DataContext__AsData", "DataContext_fromData_Z7B4D7BF5", "DataContext_createAsPV", "DataContext__Copy"]

