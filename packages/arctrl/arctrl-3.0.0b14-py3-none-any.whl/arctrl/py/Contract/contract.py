from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.reflection import (TypeInfo, union_type, string_type, array_type, record_type, obj_type, option_type)
from ..fable_modules.fable_library.types import (Array, Union, Record)

def _expr3666() -> TypeInfo:
    return union_type("ARCtrl.Contract.DTOType", [], DTOType, lambda: [[], [], [], [], [], [], [], [], [], [], [], []])


class DTOType(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["ISA_Assay", "ISA_Study", "ISA_Workflow", "ISA_Run", "ISA_Investigation", "ISA_Datamap", "JSON", "Markdown", "CWL", "YAML", "PlainText", "Cli"]


DTOType_reflection = _expr3666

def _expr3669() -> TypeInfo:
    return record_type("ARCtrl.Contract.CLITool", [], CLITool, lambda: [("Name", string_type), ("Arguments", array_type(string_type))])


@dataclass(eq = False, repr = False, slots = True)
class CLITool(Record):
    Name: str
    Arguments: Array[str]
    @staticmethod
    def create(name: str, arguments: Array[str]) -> CLITool:
        return CLITool(name, arguments)


CLITool_reflection = _expr3669

def _expr3672() -> TypeInfo:
    return union_type("ARCtrl.Contract.DTO", [], DTO, lambda: [[("Item", obj_type)], [("Item", string_type)], [("Item", CLITool_reflection())]])


class DTO(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Spreadsheet", "Text", "CLITool"]


DTO_reflection = _expr3672

def DTO__get_isSpreadsheet(this: DTO) -> bool:
    if this.tag == 0:
        return True

    else: 
        return False



def DTO__get_isText(this: DTO) -> bool:
    if this.tag == 1:
        return True

    else: 
        return False



def DTO__get_isCLITool(this: DTO) -> bool:
    if this.tag == 2:
        return True

    else: 
        return False



def DTO__AsSpreadsheet(this: DTO) -> Any:
    if this.tag == 0:
        return this.fields[0]

    else: 
        raise Exception("Not a spreadsheet")



def DTO__AsText(this: DTO) -> str:
    if this.tag == 1:
        return this.fields[0]

    else: 
        raise Exception("Not text")



def DTO__AsCLITool(this: DTO) -> CLITool:
    if this.tag == 2:
        return this.fields[0]

    else: 
        raise Exception("Not a CLI tool")



def _expr3692() -> TypeInfo:
    return record_type("ARCtrl.Contract.Contract", [], Contract, lambda: [("Operation", string_type), ("Path", string_type), ("DTOType", option_type(DTOType_reflection())), ("DTO", option_type(DTO_reflection()))])


@dataclass(eq = False, repr = False, slots = True)
class Contract(Record):
    Operation: str
    Path: str
    DTOType: DTOType | None
    DTO: DTO | None
    @staticmethod
    def create(op: str, path: str, dto_type: DTOType | None=None, dto: DTO | None=None) -> Contract:
        return Contract(op, path, dto_type, dto)

    @staticmethod
    def create_create(path: str, dto_type: DTOType, dto: DTO | None=None) -> Contract:
        return Contract("CREATE", path, dto_type, dto)

    @staticmethod
    def create_update(path: str, dto_type: DTOType, dto: DTO) -> Contract:
        return Contract("UPDATE", path, dto_type, dto)

    @staticmethod
    def create_delete(path: str) -> Contract:
        return Contract("DELETE", path, None, None)

    @staticmethod
    def create_read(path: str, dto_type: DTOType) -> Contract:
        return Contract("READ", path, dto_type, None)

    @staticmethod
    def create_execute(dto: CLITool, path: str | None=None) -> Contract:
        return Contract("EXECUTE", default_arg(path, ""), DTOType(11), DTO(2, dto))

    @staticmethod
    def create_rename(old_path: str, new_path: str) -> Contract:
        return Contract("RENAME", old_path, None, DTO(1, new_path))


Contract_reflection = _expr3692

__all__ = ["DTOType_reflection", "CLITool_reflection", "DTO_reflection", "DTO__get_isSpreadsheet", "DTO__get_isText", "DTO__get_isCLITool", "DTO__AsSpreadsheet", "DTO__AsText", "DTO__AsCLITool", "Contract_reflection"]

