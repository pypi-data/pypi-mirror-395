from __future__ import annotations
from ..fable_modules.dynamic_obj.dynamic_obj import DynamicObj
from ..fable_modules.dynamic_obj.dyn_obj import set_optional_property
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.types import FSharpRef
from .ldcontext import LDContext
from .ldobject import (LDNode, LDNode_reflection)

def _expr1838() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.ArcROCrateMetadata", None, ArcROCrateMetadata, LDNode_reflection())


class ArcROCrateMetadata(LDNode):
    def __init__(self, about: LDNode | None=None) -> None:
        super().__init__("ro-crate-metadata", ["CreativeWork"])
        this: FSharpRef[ArcROCrateMetadata] = FSharpRef(None)
        this.contents = self
        self.init_00405: int = 1
        set_optional_property("about", about, this.contents)
        conforms_to: DynamicObj = DynamicObj()
        conforms_to.SetProperty("@id", "https://w3id.org/ro/crate/1.1")
        this.contents.SetProperty("conformsTo", conforms_to)
        context: LDContext = LDContext()
        context.AddMapping("sdo", "http://schema.org/")
        context.AddMapping("arc", "http://purl.org/nfdi4plants/ontology/")
        context.AddMapping("CreativeWork", "sdo:CreativeWork")
        context.AddMapping("about", "sdo:about")
        context.AddMapping("conformsTo", "sdo:conformsTo")
        this.contents.SetProperty("@context", context)


ArcROCrateMetadata_reflection = _expr1838

def ArcROCrateMetadata__ctor_Z7020538(about: LDNode | None=None) -> ArcROCrateMetadata:
    return ArcROCrateMetadata(about)


__all__ = ["ArcROCrateMetadata_reflection"]

