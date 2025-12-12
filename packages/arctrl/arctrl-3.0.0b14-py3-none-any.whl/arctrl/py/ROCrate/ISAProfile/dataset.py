from __future__ import annotations
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import Array
from ..ldobject import (LDNode, LDNode_reflection)

def _expr1797() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Dataset", None, Dataset, LDNode_reflection())


class Dataset(LDNode):
    def __init__(self, id: str, additional_type: Array[str] | None=None) -> None:
        super().__init__(id, ["schema.org/Dataset"], default_arg(additional_type, []))
        self.init_00408: int = 1


Dataset_reflection = _expr1797

def Dataset__ctor_Z7E7CD246(id: str, additional_type: Array[str] | None=None) -> Dataset:
    return Dataset(id, additional_type)


__all__ = ["Dataset_reflection"]

