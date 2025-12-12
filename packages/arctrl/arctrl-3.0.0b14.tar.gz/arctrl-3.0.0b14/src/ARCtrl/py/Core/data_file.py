from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.reflection import (TypeInfo, union_type)
from ..fable_modules.fable_library.types import (Array, Union)

def _expr702() -> TypeInfo:
    return union_type("ARCtrl.DataFile", [], DataFile, lambda: [[], [], []])


class DataFile(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["RawDataFile", "DerivedDataFile", "ImageFile"]


DataFile_reflection = _expr702

def DataFile_get_RawDataFileJson(__unit: None=None) -> str:
    return "Raw Data File"


def DataFile_get_DerivedDataFileJson(__unit: None=None) -> str:
    return "Derived Data File"


def DataFile_get_ImageFileJson(__unit: None=None) -> str:
    return "Image File"


def DataFile__get_AsString(this: DataFile) -> str:
    if this.tag == 1:
        return "Derived Data File"

    elif this.tag == 2:
        return "Image File"

    else: 
        return "Raw Data File"



def DataFile_fromString_Z721C83C5(dt: str) -> DataFile:
    (pattern_matching_result,) = (None,)
    if dt == "RawDataFileJson":
        pattern_matching_result = 0

    elif dt == "Raw Data File":
        pattern_matching_result = 0

    elif dt == "DerivedDataFileJson":
        pattern_matching_result = 1

    elif dt == "Derived Data File":
        pattern_matching_result = 1

    elif dt == "ImageFileJson":
        pattern_matching_result = 2

    elif dt == "Image File":
        pattern_matching_result = 2

    else: 
        pattern_matching_result = 3

    if pattern_matching_result == 0:
        return DataFile(0)

    elif pattern_matching_result == 1:
        return DataFile(1)

    elif pattern_matching_result == 2:
        return DataFile(2)

    elif pattern_matching_result == 3:
        raise Exception(("Invalid DataFile type: " + dt) + "")



def DataFile__get_IsDerivedData(this: DataFile) -> bool:
    if this.tag == 1:
        return True

    else: 
        return False



def DataFile__get_IsRawData(this: DataFile) -> bool:
    if this.tag == 0:
        return True

    else: 
        return False



def DataFile__get_IsImage(this: DataFile) -> bool:
    if this.tag == 2:
        return True

    else: 
        return False



__all__ = ["DataFile_reflection", "DataFile_get_RawDataFileJson", "DataFile_get_DerivedDataFileJson", "DataFile_get_ImageFileJson", "DataFile__get_AsString", "DataFile_fromString_Z721C83C5", "DataFile__get_IsDerivedData", "DataFile__get_IsRawData", "DataFile__get_IsImage"]

