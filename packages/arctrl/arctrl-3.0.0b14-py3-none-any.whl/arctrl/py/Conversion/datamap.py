from __future__ import annotations
from typing import Any
from ..Core.data_context import DataContext
from ..Core.datamap import Datamap
from ..Core.Helper.collections_ import ResizeArray_map
from ..ROCrate.ldcontext import LDContext
from ..ROCrate.ldobject import (LDNode, LDGraph)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.types import Array
from .basic import (BaseTypes_composeFragmentDescriptor_Z4C0BEF62, BaseTypes_decomposeFragmentDescriptor_Z6839B9E8)

def _expr3878() -> TypeInfo:
    return class_type("ARCtrl.Conversion.DatamapConversion", None, DatamapConversion)


class DatamapConversion:
    ...

DatamapConversion_reflection = _expr3878

def DatamapConversion_composeFragmentDescriptors_Z892BFC3(datamap: Datamap) -> Array[LDNode]:
    def f(dc: DataContext, datamap: Any=datamap) -> LDNode:
        return BaseTypes_composeFragmentDescriptor_Z4C0BEF62(dc)

    return ResizeArray_map(f, datamap.DataContexts)


def DatamapConversion_decomposeFragmentDescriptors_Z6E59645F(fragment_descriptors: Array[LDNode], graph: LDGraph | None=None, context: LDContext | None=None) -> Datamap:
    def f(fd: LDNode, fragment_descriptors: Any=fragment_descriptors, graph: Any=graph, context: Any=context) -> DataContext:
        return BaseTypes_decomposeFragmentDescriptor_Z6839B9E8(fd, graph, context)

    return Datamap(ResizeArray_map(f, fragment_descriptors))


__all__ = ["DatamapConversion_reflection", "DatamapConversion_composeFragmentDescriptors_Z892BFC3", "DatamapConversion_decomposeFragmentDescriptors_Z6E59645F"]

