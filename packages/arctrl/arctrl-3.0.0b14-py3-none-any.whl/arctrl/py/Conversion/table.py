from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Core.Helper.collections_ import (ResizeArray_appendSingleton, ResizeArray_singleton)
from ..Core.Helper.identifier import create_missing_identifier
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.Table.arc_table import ArcTable
from ..Core.Table.arc_table_aux import (Unchecked_alignByHeaders, ArcTableValues)
from ..Core.Table.arc_tables import ArcTables
from ..Core.Table.composite_cell import CompositeCell
from ..Core.Table.composite_header import CompositeHeader
from ..FileSystem.file_system import FileSystem
from ..ROCrate.ldcontext import LDContext
from ..ROCrate.ldobject import (LDNode, LDGraph)
from ..ROCrate.LDTypes.lab_process import LDLabProcess
from ..ROCrate.LDTypes.lab_protocol import LDLabProtocol
from ..ROCrate.LDTypes.property_value import LDPropertyValue
from ..fable_modules.fable_library.list import (singleton, initialize, FSharpList, collect, of_seq, map as map_2)
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.range import range_big_int
from ..fable_modules.fable_library.seq import (fold, zip, to_list, delay, map as map_1)
from ..fable_modules.fable_library.seq2 import List_distinct
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (IEnumerable_1, get_enumerator, dispose, ignore, equals, safe_hash)
from .basic import (BaseTypes_composeDefinedTerm_ZDED3A0F, BaseTypes_composeComponent, BaseTypes_decomposeComponent_Z2F770004)
from .column_index import ARCtrl_ROCrate_LDNode__LDNode_TryGetColumnIndex
from .process import (ProcessConversion_tryGetProtocolType_Z6839B9E8, ProcessConversion_getProcessGetter, ProcessConversion_processToRows_Z6839B9E8, ProcessConversion_groupProcesses_Z27F0B586)

def CompositeRow_toProtocol(table_name: str, row: IEnumerable_1[tuple[CompositeHeader, CompositeCell]]) -> LDNode:
    def folder(p: LDNode, hc: tuple[CompositeHeader, CompositeCell], table_name: Any=table_name, row: Any=row) -> LDNode:
        (pattern_matching_result, oa, v, v_1, v_2, v_3) = (None, None, None, None, None, None)
        if hc[0].tag == 4:
            if hc[1].tag == 0:
                pattern_matching_result = 0
                oa = hc[1].fields[0]

            else: 
                pattern_matching_result = 6


        elif hc[0].tag == 7:
            if hc[1].tag == 1:
                pattern_matching_result = 1
                v = hc[1].fields[0]

            else: 
                pattern_matching_result = 6


        elif hc[0].tag == 6:
            if hc[1].tag == 1:
                pattern_matching_result = 2
                v_1 = hc[1].fields[0]

            else: 
                pattern_matching_result = 6


        elif hc[0].tag == 5:
            if hc[1].tag == 1:
                pattern_matching_result = 3
                v_2 = hc[1].fields[0]

            else: 
                pattern_matching_result = 6


        elif hc[0].tag == 8:
            if hc[1].tag == 1:
                pattern_matching_result = 4
                v_3 = hc[1].fields[0]

            else: 
                pattern_matching_result = 6


        elif hc[0].tag == 0:
            if hc[1].tag == 0:
                pattern_matching_result = 5

            elif hc[1].tag == 2:
                pattern_matching_result = 5

            else: 
                pattern_matching_result = 6


        else: 
            pattern_matching_result = 6

        if pattern_matching_result == 0:
            LDLabProtocol.set_intended_use_as_defined_term(p, BaseTypes_composeDefinedTerm_ZDED3A0F(oa))

        elif pattern_matching_result == 1:
            LDLabProtocol.set_version_as_string(p, v)

        elif pattern_matching_result == 2:
            LDLabProtocol.set_url(p, v_1)

        elif pattern_matching_result == 3:
            LDLabProtocol.set_description_as_string(p, v_2)

        elif pattern_matching_result == 4:
            LDLabProtocol.set_name_as_string(p, v_3)

        elif pattern_matching_result == 5:
            new_c: Array[LDNode] = ResizeArray_appendSingleton(BaseTypes_composeComponent(hc[0], hc[1]), LDLabProtocol.get_lab_equipments(p))
            LDLabProtocol.set_lab_equipments(p, new_c)

        return p

    return fold(folder, LDLabProtocol.create(table_name, table_name), row)


def ARCtrl_ArcTable__ArcTable_fromProtocol_Static_Z6839B9E8(p: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcTable:
    name: str = LDLabProtocol.get_name_as_string(p, context)
    t: ArcTable = ArcTable.init(name)
    enumerator: Any = get_enumerator(LDLabProtocol.get_components(p, graph, context))
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            c: LDNode = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            pattern_input: tuple[CompositeHeader, CompositeCell] = BaseTypes_decomposeComponent_Z2F770004(c, context)
            t.AddColumn(pattern_input[0], ResizeArray_singleton(pattern_input[1]), ARCtrl_ROCrate_LDNode__LDNode_TryGetColumnIndex(c))

    finally: 
        dispose(enumerator)

    def mapping(d: str, p: Any=p, graph: Any=graph, context: Any=context) -> None:
        t.AddProtocolDescriptionColumn(ResizeArray_singleton(d))

    ignore(map(mapping, LDLabProtocol.try_get_description_as_string(p, context)))
    def mapping_1(d_1: str, p: Any=p, graph: Any=graph, context: Any=context) -> None:
        t.AddProtocolVersionColumn(ResizeArray_singleton(d_1))

    ignore(map(mapping_1, LDLabProtocol.try_get_version_as_string(p, context)))
    def mapping_2(d_2: OntologyAnnotation, p: Any=p, graph: Any=graph, context: Any=context) -> None:
        t.AddProtocolTypeColumn(ResizeArray_singleton(d_2))

    ignore(map(mapping_2, ProcessConversion_tryGetProtocolType_Z6839B9E8(p, None, context)))
    def mapping_3(d_3: str, p: Any=p, graph: Any=graph, context: Any=context) -> None:
        t.AddProtocolUriColumn(ResizeArray_singleton(d_3))

    ignore(map(mapping_3, LDLabProtocol.try_get_url(p, context)))
    t.AddProtocolNameColumn(ResizeArray_singleton(name))
    return t


def ARCtrl_ArcTable__ArcTable_GetProtocols(this: ArcTable) -> FSharpList[LDNode]:
    if this.RowCount == 0:
        def _arrow3879(__unit: None=None, this: Any=this) -> LDNode:
            source: Array[CompositeHeader] = this.Headers
            def folder(p: LDNode, h: CompositeHeader) -> LDNode:
                if h.tag == 0:
                    oa: OntologyAnnotation = h.fields[0]
                    match_value: str = oa.NameText
                    match_value_1: str = oa.TermAccessionOntobeeUrl
                    new_c: Array[LDNode] = ResizeArray_appendSingleton(LDPropertyValue.create_component(match_value, "Empty Component Value", None, match_value_1), LDLabProtocol.get_lab_equipments(p))
                    LDLabProtocol.set_lab_equipments(p, new_c)

                return p

            return fold(folder, LDLabProtocol.create(create_missing_identifier(), this.Name), source)

        return singleton(_arrow3879())

    else: 
        def _arrow3880(i: int, this: Any=this) -> LDNode:
            row: IEnumerable_1[tuple[CompositeHeader, CompositeCell]]
            source_2: Array[CompositeCell] = this.GetRow(i, True)
            row = zip(this.Headers, source_2)
            return CompositeRow_toProtocol(this.Name, row)

        class ObjectExpr3881:
            @property
            def Equals(self) -> Callable[[LDNode, LDNode], bool]:
                return equals

            @property
            def GetHashCode(self) -> Callable[[LDNode], int]:
                return safe_hash

        return List_distinct(initialize(this.RowCount, _arrow3880), ObjectExpr3881())



def ARCtrl_ArcTable__ArcTable_GetProcesses_5E660E5C(this: ArcTable, assay_name: str | None=None, study_name: str | None=None, fs: FileSystem | None=None) -> FSharpList[LDNode]:
    if this.RowCount == 0:
        return singleton(LDLabProcess.create(this.Name))

    else: 
        getter: Callable[[ArcTable, int], LDNode] = ProcessConversion_getProcessGetter(assay_name, study_name, this.Name, this.Headers, fs)
        def _arrow3883(__unit: None=None, this: Any=this, assay_name: Any=assay_name, study_name: Any=study_name, fs: Any=fs) -> IEnumerable_1[LDNode]:
            def _arrow3882(i: int) -> LDNode:
                return getter(this)(i)

            return map_1(_arrow3882, range_big_int(0, 1, this.RowCount - 1))

        return to_list(delay(_arrow3883))



def ARCtrl_ArcTable__ArcTable_fromProcesses_Static_Z3575FB5F(name: str, ps: FSharpList[LDNode], graph: LDGraph | None=None, context: LDContext | None=None) -> ArcTable:
    def mapping(p: LDNode, name: Any=name, ps: Any=ps, graph: Any=graph, context: Any=context) -> FSharpList[FSharpList[tuple[CompositeHeader, CompositeCell]]]:
        return of_seq(ProcessConversion_processToRows_Z6839B9E8(p, graph, context))

    tupled_arg: tuple[Array[CompositeHeader], ArcTableValues] = Unchecked_alignByHeaders(True, collect(mapping, ps))
    return ArcTable.from_arc_table_values(name, tupled_arg[0], tupled_arg[1])


def ARCtrl_ArcTables__ArcTables_GetProcesses_5E660E5C(this: ArcTables, assay_name: str | None=None, study_name: str | None=None, fs: FileSystem | None=None) -> FSharpList[LDNode]:
    def mapping(t: ArcTable, this: Any=this, assay_name: Any=assay_name, study_name: Any=study_name, fs: Any=fs) -> FSharpList[LDNode]:
        return ARCtrl_ArcTable__ArcTable_GetProcesses_5E660E5C(t, assay_name, study_name, fs)

    return collect(mapping, to_list(this.Tables))


def ARCtrl_ArcTables__ArcTables_fromProcesses_Static_Z27F0B586(ps: FSharpList[LDNode], graph: LDGraph | None=None, context: LDContext | None=None) -> ArcTables:
    def mapping_1(tupled_arg: tuple[str, FSharpList[LDNode]], ps: Any=ps, graph: Any=graph, context: Any=context) -> ArcTable:
        def mapping(p: LDNode, tupled_arg: Any=tupled_arg) -> FSharpList[FSharpList[tuple[CompositeHeader, CompositeCell]]]:
            return of_seq(ProcessConversion_processToRows_Z6839B9E8(p, graph, context))

        tupled_arg_1: tuple[Array[CompositeHeader], ArcTableValues] = Unchecked_alignByHeaders(True, collect(mapping, tupled_arg[1]))
        return ArcTable.from_arc_table_values(tupled_arg[0], tupled_arg_1[0], tupled_arg_1[1])

    return ArcTables(list(map_2(mapping_1, ProcessConversion_groupProcesses_Z27F0B586(ps, graph, context))))


__all__ = ["CompositeRow_toProtocol", "ARCtrl_ArcTable__ArcTable_fromProtocol_Static_Z6839B9E8", "ARCtrl_ArcTable__ArcTable_GetProtocols", "ARCtrl_ArcTable__ArcTable_GetProcesses_5E660E5C", "ARCtrl_ArcTable__ArcTable_fromProcesses_Static_Z3575FB5F", "ARCtrl_ArcTables__ArcTables_GetProcesses_5E660E5C", "ARCtrl_ArcTables__ArcTables_fromProcesses_Static_Z27F0B586"]

