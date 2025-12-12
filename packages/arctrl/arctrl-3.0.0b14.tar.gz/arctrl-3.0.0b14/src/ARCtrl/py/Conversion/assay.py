from __future__ import annotations
from typing import Any
from ..Core.arc_types import ArcAssay
from ..Core.comment import Comment
from ..Core.data import DataAux_pathAndSelectorFromName
from ..Core.datamap import Datamap
from ..Core.Helper.collections_ import (ResizeArray_distinct, ResizeArray_append, ResizeArray_choose, ResizeArray_collect, ResizeArray_filter, ResizeArray_map, ResizeArray_tryFind, Option_fromSeq, ResizeArray_groupBy, ResizeArray_singleton, ResizeArray_appendSingleton, Option_fromValueWithDefault)
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from ..Core.Table.arc_tables import ArcTables
from ..FileSystem.file_system import FileSystem
from ..ROCrate.ldcontext import LDContext
from ..ROCrate.ldobject import (LDNode, LDGraph)
from ..ROCrate.LDTypes.dataset import LDDataset
from ..ROCrate.LDTypes.file import LDFile
from ..ROCrate.LDTypes.lab_process import LDLabProcess
from ..ROCrate.LDTypes.property_value import LDPropertyValue
from ..fable_modules.fable_library.list import of_seq
from ..fable_modules.fable_library.option import (default_arg, map)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.types import Array
from .basic import (BaseTypes_composeDefinedTerm_ZDED3A0F, BaseTypes_composePropertyValueFromOA_ZDED3A0F, BaseTypes_composeComment_Z13201A7E, BaseTypes_decomposeDefinedTerm_Z2F770004, BaseTypes_decomposePropertyValueToOA_Z2F770004, BaseTypes_decomposeComment_Z2F770004)
from .datamap import (DatamapConversion_composeFragmentDescriptors_Z892BFC3, DatamapConversion_decomposeFragmentDescriptors_Z6E59645F)
from .person import (PersonConversion_composePerson_Z64D846DC, PersonConversion_decomposePerson_Z6839B9E8)
from .table import (ARCtrl_ArcTables__ArcTables_GetProcesses_5E660E5C, ARCtrl_ArcTables__ArcTables_fromProcesses_Static_Z27F0B586)

def _expr3958() -> TypeInfo:
    return class_type("ARCtrl.Conversion.AssayConversion", None, AssayConversion)


class AssayConversion:
    ...

AssayConversion_reflection = _expr3958

def AssayConversion_getDataFilesFromProcesses_6BABD1B0(processes: Array[LDNode], fragment_descriptors: Array[LDNode] | None=None, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
    def f(df: LDNode, processes: Any=processes, fragment_descriptors: Any=fragment_descriptors, graph: Any=graph, context: Any=context) -> LDNode | None:
        return LDPropertyValue.try_get_subject_of(df, graph, context)

    def f_1(p: LDNode, processes: Any=processes, fragment_descriptors: Any=fragment_descriptors, graph: Any=graph, context: Any=context) -> Array[LDNode]:
        return ResizeArray_append(LDLabProcess.get_objects_as_data(p, graph, context), LDLabProcess.get_results_as_data(p, graph, context))

    data: Array[LDNode] = ResizeArray_distinct(ResizeArray_append(ResizeArray_choose(f, default_arg(fragment_descriptors, [])), ResizeArray_collect(f_1, processes)))
    def f_2(d: LDNode, processes: Any=processes, fragment_descriptors: Any=fragment_descriptors, graph: Any=graph, context: Any=context) -> bool:
        return DataAux_pathAndSelectorFromName(d.Id)[1] is None

    files: Array[LDNode] = ResizeArray_filter(f_2, data)
    def f_7(tupled_arg: tuple[str, Array[LDNode]], processes: Any=processes, fragment_descriptors: Any=fragment_descriptors, graph: Any=graph, context: Any=context) -> LDNode:
        path: str = tupled_arg[0]
        fragments: Array[LDNode] = tupled_arg[1]
        file: LDNode
        def f_5(d_3: LDNode, tupled_arg: Any=tupled_arg) -> bool:
            return d_3.Id == path

        match_value: LDNode | None = ResizeArray_tryFind(f_5, files)
        if match_value is None:
            comments: Array[LDNode] | None = Option_fromSeq(LDFile.get_comments(fragments[0], graph, context))
            file = LDFile.create(path, path, comments, LDFile.try_get_disambiguating_description_as_string(fragments[0], context), LDFile.try_get_encoding_format_as_string(fragments[0], context), None, fragments[0].TryGetContext())

        else: 
            file = match_value

        LDDataset.set_has_parts(file, fragments, context)
        return file

    def f_4(d_2: LDNode, processes: Any=processes, fragment_descriptors: Any=fragment_descriptors, graph: Any=graph, context: Any=context) -> str:
        return DataAux_pathAndSelectorFromName(d_2.Id)[0]

    def f_3(d_1: LDNode, processes: Any=processes, fragment_descriptors: Any=fragment_descriptors, graph: Any=graph, context: Any=context) -> bool:
        return DataAux_pathAndSelectorFromName(d_1.Id)[1] is not None

    return ResizeArray_append(files, ResizeArray_map(f_7, ResizeArray_groupBy(f_4, ResizeArray_filter(f_3, data))))


def AssayConversion_composeAssay_Z5C53FD5C(assay: ArcAssay, fs: FileSystem | None=None) -> LDNode:
    def mapping(term: OntologyAnnotation, assay: Any=assay, fs: Any=fs) -> LDNode:
        return BaseTypes_composeDefinedTerm_ZDED3A0F(term)

    measurement_method: LDNode | None = map(mapping, assay.TechnologyType)
    def mapping_1(term_1: OntologyAnnotation, assay: Any=assay, fs: Any=fs) -> LDNode:
        return BaseTypes_composeDefinedTerm_ZDED3A0F(term_1)

    measurement_technique: LDNode | None = map(mapping_1, assay.TechnologyPlatform)
    def mapping_2(term_2: OntologyAnnotation, assay: Any=assay, fs: Any=fs) -> LDNode:
        return BaseTypes_composePropertyValueFromOA_ZDED3A0F(term_2)

    variable_measured: LDNode | None = map(mapping_2, assay.MeasurementType)
    def f(c: Person, assay: Any=assay, fs: Any=fs) -> LDNode:
        return PersonConversion_composePerson_Z64D846DC(c)

    creators: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f, assay.Performers))
    process_sequence: Array[LDNode] | None = Option_fromSeq(list(ARCtrl_ArcTables__ArcTables_GetProcesses_5E660E5C(ArcTables(assay.Tables), assay.Identifier, None, fs)))
    def mapping_3(datamap: Datamap, assay: Any=assay, fs: Any=fs) -> Array[LDNode]:
        return DatamapConversion_composeFragmentDescriptors_Z892BFC3(datamap)

    fragment_descriptors: Array[LDNode] | None = map(mapping_3, assay.Datamap)
    def mapping_4(ps: Array[LDNode], assay: Any=assay, fs: Any=fs) -> Array[LDNode]:
        return AssayConversion_getDataFilesFromProcesses_6BABD1B0(ps, fragment_descriptors)

    data_files: Array[LDNode] | None = map(mapping_4, process_sequence)
    def _arrow3959(__unit: None=None, assay: Any=assay, fs: Any=fs) -> Array[LDNode] | None:
        fds_1: Array[LDNode] = fragment_descriptors
        return fds_1

    def _arrow3960(__unit: None=None, assay: Any=assay, fs: Any=fs) -> Array[LDNode] | None:
        vm_1: LDNode = variable_measured
        return ResizeArray_singleton(vm_1)

    def _arrow3961(__unit: None=None, assay: Any=assay, fs: Any=fs) -> Array[LDNode] | None:
        fds: Array[LDNode] = fragment_descriptors
        vm: LDNode = variable_measured
        return ResizeArray_appendSingleton(vm, fds)

    variable_measureds: Array[LDNode] | None = (None if (fragment_descriptors is None) else _arrow3959()) if (variable_measured is None) else (_arrow3960() if (fragment_descriptors is None) else _arrow3961())
    def f_1(c_1: Comment, assay: Any=assay, fs: Any=fs) -> LDNode:
        return BaseTypes_composeComment_Z13201A7E(c_1)

    comments: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f_1, assay.Comments))
    return LDDataset.create_assay(assay.Identifier, None, assay.Title, assay.Description, creators, data_files, measurement_method, measurement_technique, variable_measureds, process_sequence, comments)


def AssayConversion_decomposeAssay_Z6839B9E8(assay: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcAssay:
    def mapping(m: LDNode, assay: Any=assay, graph: Any=graph, context: Any=context) -> OntologyAnnotation:
        return BaseTypes_decomposeDefinedTerm_Z2F770004(m, context)

    measurement_method: OntologyAnnotation | None = map(mapping, LDDataset.try_get_measurement_method_as_defined_term(assay, graph, context))
    def mapping_1(m_1: LDNode, assay: Any=assay, graph: Any=graph, context: Any=context) -> OntologyAnnotation:
        return BaseTypes_decomposeDefinedTerm_Z2F770004(m_1, context)

    measurement_technique: OntologyAnnotation | None = map(mapping_1, LDDataset.try_get_measurement_technique_as_defined_term(assay, graph, context))
    def mapping_2(v: LDNode, assay: Any=assay, graph: Any=graph, context: Any=context) -> OntologyAnnotation:
        return BaseTypes_decomposePropertyValueToOA_Z2F770004(v, context)

    variable_measured: OntologyAnnotation | None = map(mapping_2, LDDataset.try_get_variable_measured_as_measurement_type(assay, graph, context))
    def f(c: LDNode, assay: Any=assay, graph: Any=graph, context: Any=context) -> Person:
        return PersonConversion_decomposePerson_Z6839B9E8(c, graph, context)

    perfomers: Array[Person] = ResizeArray_map(f, LDDataset.get_creators(assay, graph, context))
    datamap: Datamap | None
    v_1: Datamap = DatamapConversion_decomposeFragmentDescriptors_Z6E59645F(LDDataset.get_variable_measured_as_fragment_descriptors(assay, graph, context), graph, context)
    datamap = Option_fromValueWithDefault(Datamap.init(), v_1)
    tables: ArcTables = ARCtrl_ArcTables__ArcTables_fromProcesses_Static_Z27F0B586(of_seq(LDDataset.get_abouts_as_lab_process(assay, graph, context)), graph, context)
    def f_1(c_1: LDNode, assay: Any=assay, graph: Any=graph, context: Any=context) -> Comment:
        return BaseTypes_decomposeComment_Z2F770004(c_1, context)

    comments: Array[Comment] = ResizeArray_map(f_1, LDDataset.get_comments(assay, graph, context))
    return ArcAssay.create(LDDataset.get_identifier_as_string(assay, context), LDDataset.try_get_name_as_string(assay, context), LDDataset.try_get_description_as_string(assay, context), variable_measured, measurement_method, measurement_technique, tables.Tables, datamap, perfomers, comments)


__all__ = ["AssayConversion_reflection", "AssayConversion_getDataFilesFromProcesses_6BABD1B0", "AssayConversion_composeAssay_Z5C53FD5C", "AssayConversion_decomposeAssay_Z6839B9E8"]

