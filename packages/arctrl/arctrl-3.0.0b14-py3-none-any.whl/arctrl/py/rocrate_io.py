from __future__ import annotations
from typing import Any
from .Core.arc_types import ArcInvestigation
from .Core.Helper.collections_ import ResizeArray_choose
from .FileSystem.file_system import FileSystem
from .Json.ROCrate.ldgraph import (encoder, decoder)
from .Json.ROCrate.ldnode import decoder as decoder_1
from .ROCrate.ldcontext import LDContext
from .ROCrate.ldobject import (LDNode, LDRef, LDGraph)
from .ROCrate.LDTypes.creative_work import LDCreativeWork
from .ROCrate.LDTypes.dataset import LDDataset
from .ROCrate.LDTypes.file import LDFile
from .ROCrate.rocrate_context import (init_v1_2, init_bioschemas_context, init_v1_1)
from .conversion import (ARCtrl_ArcInvestigation__ArcInvestigation_ToROCrateInvestigation_1695DD5C, ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateInvestigation_Static_Z6839B9E8)
from .license import License
from .fable_modules.fable_library.date import now
from .fable_modules.fable_library.option import bind
from .fable_modules.fable_library.reflection import (TypeInfo, class_type)
from .fable_modules.fable_library.seq import exactly_one
from .fable_modules.fable_library.types import Array
from .fable_modules.thoth_json_core.decode import map
from .fable_modules.thoth_json_core.types import (IEncodable, Decoder_1)

def _expr3994() -> TypeInfo:
    return class_type("ARCtrl.Json.ARC.ROCrate", None, ROCrate)


class ROCrate:
    ...

ROCrate_reflection = _expr3994

def ROCrate_get_metadataFileDescriptor(__unit: None=None) -> LDNode:
    node: LDNode = LDNode("ro-crate-metadata.json", ["http://schema.org/CreativeWork"])
    node.SetProperty("http://purl.org/dc/terms/conformsTo", LDRef("https://w3id.org/ro/crate/1.2"))
    node.SetProperty("http://schema.org/about", LDRef("./"))
    return node


def ROCrate_createLicenseNode_29619109(license: License | None=None) -> LDNode:
    if license is None:
        return LDCreativeWork.create("#LICENSE", None, None, None, None, None, None, None, None, "ALL RIGHTS RESERVED BY THE AUTHORS")

    else: 
        license_1: License = license
        text: str
        match_value: str = license_1.Type
        text = license_1.Content
        return LDCreativeWork.create(license_1.Path, None, None, None, None, None, None, None, None, text)



def ROCrate_getLicense_Z2F770004(license: LDNode, context: LDContext | None=None) -> License | None:
    text: str | None = LDCreativeWork.try_get_text_as_string(license, context)
    match_value: str = license.Id
    (pattern_matching_result, text_1, path, text_2, path_1) = (None, None, None, None, None)
    if match_value == "#LICENSE":
        if text is not None:
            if text == "ALL RIGHTS RESERVED BY THE AUTHORS":
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1
                text_1 = text


        else: 
            pattern_matching_result = 0


    elif text is None:
        pattern_matching_result = 3
        path_1 = match_value

    else: 
        pattern_matching_result = 2
        path = match_value
        text_2 = text

    if pattern_matching_result == 0:
        return None

    elif pattern_matching_result == 1:
        return License("fulltext", text_1)

    elif pattern_matching_result == 2:
        return License("fulltext", text_2, path)

    elif pattern_matching_result == 3:
        return License("fulltext", "", path_1)



def ROCrate_encoder_1E8A3F74(isa: ArcInvestigation, license: License | None=None, fs: FileSystem | None=None) -> IEncodable:
    license_1: LDNode = ROCrate_createLicenseNode_29619109(license)
    isa_1: LDNode = ARCtrl_ArcInvestigation__ArcInvestigation_ToROCrateInvestigation_1695DD5C(isa, fs)
    LDDataset.set_sddate_published_as_date_time(isa_1, now())
    LDDataset.set_license_as_creative_work(isa_1, license_1)
    graph: LDGraph = isa_1.Flatten()
    context: LDContext = LDContext(None, [init_v1_2(), init_bioschemas_context()])
    graph.SetContext(context)
    graph.AddNode(ROCrate_get_metadataFileDescriptor())
    graph.Compact_InPlace()
    return encoder(graph)


def ROCrate_get_decoder(__unit: None=None) -> Decoder_1[tuple[ArcInvestigation, Array[str], License | None]]:
    def ctor(graph: LDGraph) -> tuple[ArcInvestigation, Array[str], License | None]:
        match_value: LDNode | None = graph.TryGetNode("./")
        if match_value is None:
            raise Exception("RO-Crate graph did not contain root data Entity")

        else: 
            node: LDNode = match_value
            def f(n: LDNode, graph: Any=graph) -> str | None:
                if (not n.HasType(LDDataset.schema_type(), graph.TryGetContext())) if ((not (n.Id.find("#") >= 0)) if LDFile.validate(n, graph.TryGetContext()) else False) else False:
                    return n.Id

                else: 
                    return None


            files: Array[str] = ResizeArray_choose(f, graph.Nodes)
            def binder(n_1: LDNode, graph: Any=graph) -> License | None:
                return ROCrate_getLicense_Z2F770004(n_1, graph.TryGetContext())

            license: License | None = bind(binder, LDDataset.try_get_license_as_creative_work(node, graph, graph.TryGetContext()))
            return (ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateInvestigation_Static_Z6839B9E8(node, graph, graph.TryGetContext()), files, license)


    return map(ctor, decoder)


def ROCrate_get_decoderDeprecated(__unit: None=None) -> Decoder_1[ArcInvestigation]:
    def ctor(ldnode: LDNode) -> ArcInvestigation:
        return ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateInvestigation_Static_Z6839B9E8(exactly_one(LDDataset.get_abouts(ldnode)), None, init_v1_1())

    return map(ctor, decoder_1)


__all__ = ["ROCrate_reflection", "ROCrate_get_metadataFileDescriptor", "ROCrate_createLicenseNode_29619109", "ROCrate_getLicense_Z2F770004", "ROCrate_encoder_1E8A3F74", "ROCrate_get_decoder", "ROCrate_get_decoderDeprecated"]

