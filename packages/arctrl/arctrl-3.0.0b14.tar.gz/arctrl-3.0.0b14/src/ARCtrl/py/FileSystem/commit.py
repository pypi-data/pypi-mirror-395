from dataclasses import dataclass
from typing import Any
from ..fable_modules.fable_library.reflection import (TypeInfo, string_type, class_type, record_type)
from ..fable_modules.fable_library.types import Record

def _expr439() -> TypeInfo:
    return record_type("ARCtrl.FileSystem.Commit", [], Commit, lambda: [("Hash", string_type), ("UserName", string_type), ("UserEmail", string_type), ("Date", class_type("System.DateTime")), ("Message", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class Commit(Record):
    Hash: str
    UserName: str
    UserEmail: str
    Date: Any
    Message: str

Commit_reflection = _expr439

__all__ = ["Commit_reflection"]

