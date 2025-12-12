from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Core.comment import Comment
from ..Core.Helper.collections_ import (ResizeArray_singleton, Option_fromValueWithDefault, ResizeArray_map, ResizeArray_create, ResizeArray_zip)
from ..Core.Helper.identifier import create_missing_identifier
from ..Core.Helper.regex import ActivePatterns__007CRegex_007C__007C
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.Table.arc_table import ArcTable
from ..Core.Table.arc_table_aux import (Unchecked_tryGetCellAt, get_empty_cell_for_header)
from ..Core.Table.composite_cell import CompositeCell
from ..Core.Table.composite_header import CompositeHeader
from ..FileSystem.file_system import FileSystem
from ..ROCrate.ldcontext import LDContext
from ..ROCrate.ldobject import (LDNode, LDGraph)
from ..ROCrate.LDTypes.lab_process import LDLabProcess
from ..ROCrate.LDTypes.lab_protocol import LDLabProtocol
from ..ROCrate.LDTypes.person import LDPerson
from ..ROCrate.LDTypes.sample import LDSample
from ..fable_modules.fable_library.int32 import parse
from ..fable_modules.fable_library.list import (FSharpList, choose, length, empty, map as map_2, sort_by)
from ..fable_modules.fable_library.option import (map as map_1, default_arg, value as value_2)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.reg_exp import (get_item, groups)
from ..fable_modules.fable_library.seq import (indexed, to_list, filter, try_pick, choose as choose_1, map, delay, append, empty as empty_1, singleton)
from ..fable_modules.fable_library.seq2 import List_groupBy
from ..fable_modules.fable_library.types import (to_string, Array)
from ..fable_modules.fable_library.util import (IEnumerable_1, string_hash, compare_primitives)
from .basic import (BaseTypes_decomposeDefinedTerm_Z2F770004, BaseTypes_composeComponent, BaseTypes_composeParameterValue, BaseTypes_composeFactorValue, BaseTypes_composeCharacteristicValue, BaseTypes_composeDefinedTerm_ZDED3A0F, BaseTypes_composeProcessInput, BaseTypes_composeProcessOutput, BaseTypes_decomposeParameterValue_Z2F770004, BaseTypes_decomposeComponent_Z2F770004, BaseTypes_decomposeCharacteristicValue_Z2F770004, BaseTypes_decomposeFactorValue_Z2F770004, BaseTypes_decomposeProcessInput_Z2F770004, BaseTypes_decomposeProcessOutput_Z2F770004)
from .column_index import (ARCtrl_ROCrate_LDNode__LDNode_SetColumnIndex_Z524259A4, try_get_index)

def _expr3886() -> TypeInfo:
    return class_type("ARCtrl.Conversion.ProcessConversion", None, ProcessConversion)


class ProcessConversion:
    ...

ProcessConversion_reflection = _expr3886

def ProcessConversion_tryGetProtocolType_Z6839B9E8(pv: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> OntologyAnnotation | None:
    match_value: LDNode | None = LDLabProtocol.try_get_intended_use_as_defined_term(pv, graph, context)
    if match_value is None:
        match_value_1: str | None = LDLabProtocol.try_get_intended_use_as_string(pv, context)
        if match_value_1 is None:
            return None

        else: 
            s: str = match_value_1
            return OntologyAnnotation.create(s)


    else: 
        return BaseTypes_decomposeDefinedTerm_Z2F770004(match_value, context)



def ProcessConversion_composeProcessName(process_name_root: str, i: int) -> str:
    return ((("" + process_name_root) + "_") + str(i)) + ""


def ProcessConversion_decomposeProcessName_Z721C83C5(name: str) -> tuple[str, int | None]:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("(?<name>.+)_(?<num>\\d+)", name)
    if active_pattern_result is not None:
        r: Any = active_pattern_result
        return (get_item(groups(r), "name") or "", parse(get_item(groups(r), "num") or "", 511, False, 32))

    else: 
        return (name, None)



def ProcessConversion_tryComponentGetter(general_i: int, value_i: int, value_header: CompositeHeader) -> Callable[[ArcTable, int], LDNode] | None:
    if value_header.tag == 0:
        def Value(table: ArcTable, general_i: Any=general_i, value_i: Any=value_i, value_header: Any=value_header) -> Callable[[int], LDNode]:
            def _arrow3888(i: int, table: Any=table) -> LDNode:
                def _arrow3887(__unit: None=None) -> CompositeCell:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                    return get_empty_cell_for_header(value_header, None) if (match_value is None) else match_value

                c: LDNode = BaseTypes_composeComponent(value_header, _arrow3887())
                ARCtrl_ROCrate_LDNode__LDNode_SetColumnIndex_Z524259A4(c, value_i)
                return c

            return _arrow3888

        return Value

    else: 
        return None



def ProcessConversion_tryParameterGetter(general_i: int, value_i: int, value_header: CompositeHeader) -> Callable[[ArcTable, int], LDNode] | None:
    if value_header.tag == 3:
        def Value(table: ArcTable, general_i: Any=general_i, value_i: Any=value_i, value_header: Any=value_header) -> Callable[[int], LDNode]:
            def _arrow3890(i: int, table: Any=table) -> LDNode:
                def _arrow3889(__unit: None=None) -> CompositeCell:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                    return get_empty_cell_for_header(value_header, None) if (match_value is None) else match_value

                p: LDNode = BaseTypes_composeParameterValue(value_header, _arrow3889())
                ARCtrl_ROCrate_LDNode__LDNode_SetColumnIndex_Z524259A4(p, value_i)
                return p

            return _arrow3890

        return Value

    else: 
        return None



def ProcessConversion_tryFactorGetter(general_i: int, value_i: int, value_header: CompositeHeader) -> Callable[[ArcTable, int], LDNode] | None:
    if value_header.tag == 2:
        def Value(table: ArcTable, general_i: Any=general_i, value_i: Any=value_i, value_header: Any=value_header) -> Callable[[int], LDNode]:
            def _arrow3892(i: int, table: Any=table) -> LDNode:
                def _arrow3891(__unit: None=None) -> CompositeCell:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                    return get_empty_cell_for_header(value_header, None) if (match_value is None) else match_value

                f: LDNode = BaseTypes_composeFactorValue(value_header, _arrow3891())
                ARCtrl_ROCrate_LDNode__LDNode_SetColumnIndex_Z524259A4(f, value_i)
                return f

            return _arrow3892

        return Value

    else: 
        return None



def ProcessConversion_tryCharacteristicGetter(general_i: int, value_i: int, value_header: CompositeHeader) -> Callable[[ArcTable, int], LDNode] | None:
    if value_header.tag == 1:
        def Value(table: ArcTable, general_i: Any=general_i, value_i: Any=value_i, value_header: Any=value_header) -> Callable[[int], LDNode]:
            def _arrow3894(i: int, table: Any=table) -> LDNode:
                def _arrow3893(__unit: None=None) -> CompositeCell:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                    return get_empty_cell_for_header(value_header, None) if (match_value is None) else match_value

                c: LDNode = BaseTypes_composeCharacteristicValue(value_header, _arrow3893())
                ARCtrl_ROCrate_LDNode__LDNode_SetColumnIndex_Z524259A4(c, value_i)
                return c

            return _arrow3894

        return Value

    else: 
        return None



def ProcessConversion_tryGetProtocolTypeGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], LDNode] | None:
    if header.tag == 4:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], LDNode]:
            def _arrow3896(i: int, table: Any=table) -> LDNode:
                def _arrow3895(__unit: None=None) -> OntologyAnnotation:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                    if match_value is None:
                        return OntologyAnnotation()

                    else: 
                        cell: CompositeCell = match_value
                        return cell.AsTerm


                return BaseTypes_composeDefinedTerm_ZDED3A0F(_arrow3895())

            return _arrow3896

        return Value

    else: 
        return None



def ProcessConversion_tryGetProtocolREFGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], str] | None:
    if header.tag == 8:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], str]:
            def _arrow3897(i: int, table: Any=table) -> str:
                match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                if match_value is None:
                    return ""

                else: 
                    cell: CompositeCell = match_value
                    return cell.AsFreeText


            return _arrow3897

        return Value

    else: 
        return None



def ProcessConversion_tryGetProtocolDescriptionGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], str] | None:
    if header.tag == 5:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], str]:
            def _arrow3898(i: int, table: Any=table) -> str:
                match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                if match_value is None:
                    return ""

                else: 
                    cell: CompositeCell = match_value
                    return cell.AsFreeText


            return _arrow3898

        return Value

    else: 
        return None



def ProcessConversion_tryGetProtocolURIGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], str] | None:
    if header.tag == 6:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], str]:
            def _arrow3899(i: int, table: Any=table) -> str:
                match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                if match_value is None:
                    return ""

                else: 
                    cell: CompositeCell = match_value
                    return cell.AsFreeText


            return _arrow3899

        return Value

    else: 
        return None



def ProcessConversion_tryGetProtocolVersionGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], str] | None:
    if header.tag == 7:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], str]:
            def _arrow3900(i: int, table: Any=table) -> str:
                match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                if match_value is None:
                    return ""

                else: 
                    cell: CompositeCell = match_value
                    return cell.AsFreeText


            return _arrow3900

        return Value

    else: 
        return None



def ProcessConversion_tryGetInputGetter(general_i: int, header: CompositeHeader, fs: FileSystem | None=None) -> Callable[[ArcTable, int], LDNode] | None:
    if header.tag == 11:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header, fs: Any=fs) -> Callable[[int], LDNode]:
            def _arrow3902(i: int, table: Any=table) -> LDNode:
                def _arrow3901(__unit: None=None) -> CompositeCell:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                    return get_empty_cell_for_header(header, None) if (match_value is None) else match_value

                return BaseTypes_composeProcessInput(header, _arrow3901(), fs)

            return _arrow3902

        return Value

    else: 
        return None



def ProcessConversion_tryGetOutputGetter(general_i: int, header: CompositeHeader, fs: FileSystem | None=None) -> Callable[[ArcTable, int], LDNode] | None:
    if header.tag == 12:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header, fs: Any=fs) -> Callable[[int], LDNode]:
            def _arrow3904(i: int, table: Any=table) -> LDNode:
                def _arrow3903(__unit: None=None) -> CompositeCell:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                    return get_empty_cell_for_header(header, None) if (match_value is None) else match_value

                return BaseTypes_composeProcessOutput(header, _arrow3903(), fs)

            return _arrow3904

        return Value

    else: 
        return None



def ProcessConversion_tryGetCommentGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], str] | None:
    if header.tag == 14:
        c: str = header.fields[0]
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], str]:
            def _arrow3906(i: int, table: Any=table) -> str:
                def _arrow3905(__unit: None=None) -> Comment:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                    if match_value is None:
                        return Comment(c)

                    else: 
                        cell: CompositeCell = match_value
                        return Comment(c, cell.AsFreeText)


                return to_string(_arrow3905())

            return _arrow3906

        return Value

    else: 
        return None



def ProcessConversion_tryGetPerformerGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], LDNode] | None:
    if header.tag == 9:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], LDNode]:
            def _arrow3907(i: int, table: Any=table) -> LDNode:
                performer: str
                match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                if match_value is None:
                    performer = ""

                else: 
                    cell: CompositeCell = match_value
                    performer = cell.AsFreeText

                return LDPerson.create(performer)

            return _arrow3907

        return Value

    else: 
        return None



def ProcessConversion_getProcessGetter(assay_name: str | None, study_name: str | None, process_name_root: str, headers: IEnumerable_1[CompositeHeader], fs: FileSystem | None=None) -> Callable[[ArcTable, int], LDNode]:
    headers_1: IEnumerable_1[tuple[int, CompositeHeader]] = indexed(headers)
    def predicate(arg: tuple[int, CompositeHeader], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> bool:
        return arg[1].IsCvParamColumn

    value_headers: FSharpList[tuple[int, tuple[int, CompositeHeader]]] = to_list(indexed(filter(predicate, headers_1)))
    def chooser(tupled_arg: tuple[int, tuple[int, CompositeHeader]], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[ArcTable, int], LDNode] | None:
        _arg: tuple[int, CompositeHeader] = tupled_arg[1]
        return ProcessConversion_tryCharacteristicGetter(_arg[0], tupled_arg[0], _arg[1])

    char_getters: FSharpList[Callable[[ArcTable, int], LDNode]] = choose(chooser, value_headers)
    def chooser_1(tupled_arg_1: tuple[int, tuple[int, CompositeHeader]], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[ArcTable, int], LDNode] | None:
        _arg_1: tuple[int, CompositeHeader] = tupled_arg_1[1]
        return ProcessConversion_tryFactorGetter(_arg_1[0], tupled_arg_1[0], _arg_1[1])

    factor_value_getters: FSharpList[Callable[[ArcTable, int], LDNode]] = choose(chooser_1, value_headers)
    def chooser_2(tupled_arg_2: tuple[int, tuple[int, CompositeHeader]], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[ArcTable, int], LDNode] | None:
        _arg_2: tuple[int, CompositeHeader] = tupled_arg_2[1]
        return ProcessConversion_tryParameterGetter(_arg_2[0], tupled_arg_2[0], _arg_2[1])

    parameter_value_getters: FSharpList[Callable[[ArcTable, int], LDNode]] = choose(chooser_2, value_headers)
    def chooser_3(tupled_arg_3: tuple[int, tuple[int, CompositeHeader]], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[ArcTable, int], LDNode] | None:
        _arg_3: tuple[int, CompositeHeader] = tupled_arg_3[1]
        return ProcessConversion_tryComponentGetter(_arg_3[0], tupled_arg_3[0], _arg_3[1])

    component_getters: FSharpList[Callable[[ArcTable, int], LDNode]] = choose(chooser_3, value_headers)
    def chooser_4(tupled_arg_4: tuple[int, CompositeHeader], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[ArcTable, int], LDNode] | None:
        return ProcessConversion_tryGetProtocolTypeGetter(tupled_arg_4[0], tupled_arg_4[1])

    protocol_type_getter: Callable[[ArcTable, int], LDNode] | None = try_pick(chooser_4, headers_1)
    def chooser_5(tupled_arg_5: tuple[int, CompositeHeader], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[ArcTable, int], str] | None:
        return ProcessConversion_tryGetProtocolREFGetter(tupled_arg_5[0], tupled_arg_5[1])

    protocol_refgetter: Callable[[ArcTable, int], str] | None = try_pick(chooser_5, headers_1)
    def chooser_6(tupled_arg_6: tuple[int, CompositeHeader], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[ArcTable, int], str] | None:
        return ProcessConversion_tryGetProtocolDescriptionGetter(tupled_arg_6[0], tupled_arg_6[1])

    protocol_description_getter: Callable[[ArcTable, int], str] | None = try_pick(chooser_6, headers_1)
    def chooser_7(tupled_arg_7: tuple[int, CompositeHeader], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[ArcTable, int], str] | None:
        return ProcessConversion_tryGetProtocolURIGetter(tupled_arg_7[0], tupled_arg_7[1])

    protocol_urigetter: Callable[[ArcTable, int], str] | None = try_pick(chooser_7, headers_1)
    def chooser_8(tupled_arg_8: tuple[int, CompositeHeader], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[ArcTable, int], str] | None:
        return ProcessConversion_tryGetProtocolVersionGetter(tupled_arg_8[0], tupled_arg_8[1])

    protocol_version_getter: Callable[[ArcTable, int], str] | None = try_pick(chooser_8, headers_1)
    def chooser_9(tupled_arg_9: tuple[int, CompositeHeader], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[ArcTable, int], LDNode] | None:
        return ProcessConversion_tryGetPerformerGetter(tupled_arg_9[0], tupled_arg_9[1])

    performer_getter: Callable[[ArcTable, int], LDNode] | None = try_pick(chooser_9, headers_1)
    def chooser_10(tupled_arg_10: tuple[int, CompositeHeader], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[ArcTable, int], str] | None:
        return ProcessConversion_tryGetCommentGetter(tupled_arg_10[0], tupled_arg_10[1])

    comment_getters: FSharpList[Callable[[ArcTable, int], str]] = to_list(choose_1(chooser_10, headers_1))
    input_getter_1: Callable[[ArcTable, int], Array[LDNode]]
    def chooser_11(tupled_arg_11: tuple[int, CompositeHeader], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[ArcTable, int], LDNode] | None:
        return ProcessConversion_tryGetInputGetter(tupled_arg_11[0], tupled_arg_11[1], fs)

    match_value: Callable[[ArcTable, int], LDNode] | None = try_pick(chooser_11, headers_1)
    if match_value is None:
        def _arrow3909(table_1: ArcTable, assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[int], Array[LDNode]]:
            def _arrow3908(i_1: int) -> Array[LDNode]:
                def mapping_1(f_1: Callable[[ArcTable, int], LDNode]) -> LDNode:
                    return f_1(table_1)(i_1)

                chars_1: Array[LDNode] = list(map(mapping_1, char_getters))
                return ResizeArray_singleton(LDSample.create_sample(((("" + process_name_root) + "_Input_") + str(i_1)) + "", None, chars_1))

            return _arrow3908

        def _arrow3911(table_2: ArcTable, assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[int], Array[LDNode]]:
            def _arrow3910(i_2: int) -> Array[LDNode]:
                return []

            return _arrow3910

        input_getter_1 = _arrow3909 if (length(char_getters) != 0) else _arrow3911

    else: 
        input_getter: Callable[[ArcTable, int], LDNode] = match_value
        def _arrow3913(table: ArcTable, assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[int], Array[LDNode]]:
            def _arrow3912(i: int) -> Array[LDNode]:
                def mapping(f: Callable[[ArcTable, int], LDNode]) -> LDNode:
                    return f(table)(i)

                chars: Array[LDNode] = list(map(mapping, char_getters))
                input: LDNode = input_getter(table)(i)
                if len(chars) > 0:
                    LDSample.set_additional_properties(input, chars)

                return ResizeArray_singleton(input)

            return _arrow3912

        input_getter_1 = _arrow3913

    output_getter_1: Callable[[ArcTable, int], Array[LDNode]]
    def chooser_12(tupled_arg_12: tuple[int, CompositeHeader], assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[ArcTable, int], LDNode] | None:
        return ProcessConversion_tryGetOutputGetter(tupled_arg_12[0], tupled_arg_12[1], fs)

    match_value_1: Callable[[ArcTable, int], LDNode] | None = try_pick(chooser_12, headers_1)
    if match_value_1 is None:
        def _arrow3915(table_4: ArcTable, assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[int], Array[LDNode]]:
            def _arrow3914(i_4: int) -> Array[LDNode]:
                def mapping_3(f_3: Callable[[ArcTable, int], LDNode]) -> LDNode:
                    return f_3(table_4)(i_4)

                factors_1: Array[LDNode] = list(map(mapping_3, factor_value_getters))
                return ResizeArray_singleton(LDSample.create_sample(((("" + process_name_root) + "_Output_") + str(i_4)) + "", None, factors_1))

            return _arrow3914

        def _arrow3917(table_5: ArcTable, assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[int], Array[LDNode]]:
            def _arrow3916(i_5: int) -> Array[LDNode]:
                return []

            return _arrow3916

        output_getter_1 = _arrow3915 if (length(factor_value_getters) != 0) else _arrow3917

    else: 
        output_getter: Callable[[ArcTable, int], LDNode] = match_value_1
        def _arrow3919(table_3: ArcTable, assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[int], Array[LDNode]]:
            def _arrow3918(i_3: int) -> Array[LDNode]:
                def mapping_2(f_2: Callable[[ArcTable, int], LDNode]) -> LDNode:
                    return f_2(table_3)(i_3)

                factors: Array[LDNode] = list(map(mapping_2, factor_value_getters))
                output: LDNode = output_getter(table_3)(i_3)
                if len(factors) > 0:
                    LDSample.set_additional_properties(output, factors)

                return ResizeArray_singleton(output)

            return _arrow3918

        output_getter_1 = _arrow3919

    def _arrow3921(table_6: ArcTable, assay_name: Any=assay_name, study_name: Any=study_name, process_name_root: Any=process_name_root, headers: Any=headers, fs: Any=fs) -> Callable[[int], LDNode]:
        def _arrow3920(i_6: int) -> LDNode:
            pn: str = process_name_root if (table_6.RowCount == 1) else ProcessConversion_composeProcessName(process_name_root, i_6)
            def mapping_4(f_4: Callable[[ArcTable, int], LDNode]) -> LDNode:
                return f_4(table_6)(i_6)

            paramvalues: Array[LDNode] | None = map_1(list, Option_fromValueWithDefault(empty(), map_2(mapping_4, parameter_value_getters)))
            def mapping_6(f_5: Callable[[ArcTable, int], str]) -> str:
                return f_5(table_6)(i_6)

            comments: Array[str] | None = map_1(list, Option_fromValueWithDefault(empty(), map_2(mapping_6, comment_getters)))
            def mapping_8(f_6: Callable[[ArcTable, int], LDNode]) -> LDNode:
                return f_6(table_6)(i_6)

            components: Array[LDNode] | None = map_1(list, Option_fromValueWithDefault(empty(), map_2(mapping_8, component_getters)))
            id: str = LDLabProcess.gen_id(process_name_root, assay_name, study_name) + (("_" + str(i_6)) + "")
            protocol: LDNode | None
            def mapping_10(f_7: Callable[[ArcTable, int], str]) -> str:
                return f_7(table_6)(i_6)

            name: str | None = map_1(mapping_10, protocol_refgetter)
            protocol_id: str = LDLabProtocol.gen_id(name, process_name_root)
            def mapping_11(f_8: Callable[[ArcTable, int], str]) -> str:
                return f_8(table_6)(i_6)

            def mapping_12(f_9: Callable[[ArcTable, int], LDNode]) -> LDNode:
                return f_9(table_6)(i_6)

            def mapping_13(f_10: Callable[[ArcTable, int], str]) -> str:
                return f_10(table_6)(i_6)

            def mapping_14(f_11: Callable[[ArcTable, int], str]) -> str:
                return f_11(table_6)(i_6)

            protocol = LDLabProtocol.create(protocol_id, name, map_1(mapping_11, protocol_description_getter), map_1(mapping_12, protocol_type_getter), None, None, components, None, map_1(mapping_13, protocol_urigetter), map_1(mapping_14, protocol_version_getter))
            match_value: Array[LDNode] = input_getter_1(table_6)(i_6)
            match_value_1: Array[LDNode] = output_getter_1(table_6)(i_6)
            def mapping_15(f_12: Callable[[ArcTable, int], LDNode]) -> LDNode:
                return f_12(table_6)(i_6)

            agent: LDNode | None = map_1(mapping_15, performer_getter)
            return LDLabProcess.create(pn, match_value, match_value_1, id, agent, protocol, paramvalues, None, comments)

        return _arrow3920

    return _arrow3921


def ProcessConversion_groupProcesses_Z27F0B586(processes: FSharpList[LDNode], graph: LDGraph | None=None, context: LDContext | None=None) -> FSharpList[tuple[str, FSharpList[LDNode]]]:
    def projection(p: LDNode, processes: Any=processes, graph: Any=graph, context: Any=context) -> str:
        match_value: str | None = LDLabProcess.try_get_name_as_string(p, context)
        match_value_1: LDNode | None = LDLabProcess.try_get_executes_lab_protocol(p, graph, context)
        (pattern_matching_result, name_1, protocol_2, name_2, protocol_3) = (None, None, None, None, None)
        if match_value is not None:
            if ProcessConversion_decomposeProcessName_Z721C83C5(match_value)[1] is not None:
                pattern_matching_result = 0
                name_1 = match_value

            elif match_value_1 is not None:
                def _arrow3922(__unit: None=None, p: Any=p) -> bool:
                    protocol: LDNode = match_value_1
                    return LDLabProtocol.try_get_name_as_string(protocol, context) is not None

                if _arrow3922():
                    pattern_matching_result = 1
                    protocol_2 = match_value_1

                else: 
                    pattern_matching_result = 2
                    name_2 = match_value


            else: 
                pattern_matching_result = 2
                name_2 = match_value


        elif match_value_1 is not None:
            def _arrow3923(__unit: None=None, p: Any=p) -> bool:
                protocol_1: LDNode = match_value_1
                return LDLabProtocol.try_get_name_as_string(protocol_1, context) is not None

            if _arrow3923():
                pattern_matching_result = 1
                protocol_2 = match_value_1

            else: 
                pattern_matching_result = 3
                protocol_3 = match_value_1


        else: 
            pattern_matching_result = 4

        if pattern_matching_result == 0:
            return ProcessConversion_decomposeProcessName_Z721C83C5(name_1)[0]

        elif pattern_matching_result == 1:
            return default_arg(LDLabProtocol.try_get_name_as_string(protocol_2, context), "")

        elif pattern_matching_result == 2:
            return name_2

        elif pattern_matching_result == 3:
            return protocol_3.Id

        elif pattern_matching_result == 4:
            return create_missing_identifier()


    class ObjectExpr3925:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow3924(x: str, y: str) -> bool:
                return x == y

            return _arrow3924

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return List_groupBy(projection, processes, ObjectExpr3925())


def ProcessConversion_processToRows_Z6839B9E8(p: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[FSharpList[tuple[CompositeHeader, CompositeCell]]]:
    def f(ppv: LDNode, p: Any=p, graph: Any=graph, context: Any=context) -> tuple[tuple[CompositeHeader, CompositeCell], int | None]:
        return (BaseTypes_decomposeParameterValue_Z2F770004(ppv, context), try_get_index(ppv))

    pvs: Array[tuple[tuple[CompositeHeader, CompositeCell], int | None]] = ResizeArray_map(f, LDLabProcess.get_parameter_values(p, graph, context))
    components: Array[tuple[tuple[CompositeHeader, CompositeCell], int | None]]
    match_value: LDNode | None = LDLabProcess.try_get_executes_lab_protocol(p, graph, context)
    if match_value is None:
        components = []

    else: 
        prot: LDNode = match_value
        def f_1(ppv_1: LDNode, p: Any=p, graph: Any=graph, context: Any=context) -> tuple[tuple[CompositeHeader, CompositeCell], int | None]:
            return (BaseTypes_decomposeComponent_Z2F770004(ppv_1, context), try_get_index(ppv_1))

        components = ResizeArray_map(f_1, LDLabProtocol.get_components(prot, graph, context))

    prot_vals: FSharpList[tuple[CompositeHeader, CompositeCell]]
    match_value_1: LDNode | None = LDLabProcess.try_get_executes_lab_protocol(p, graph, context)
    if match_value_1 is None:
        prot_vals = empty()

    else: 
        prot_1: LDNode = match_value_1
        def _arrow3934(__unit: None=None, p: Any=p, graph: Any=graph, context: Any=context) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
            def _arrow3926(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                match_value_2: str | None = LDLabProtocol.try_get_name_as_string(prot_1, context)
                if match_value_2 is None:
                    return empty_1()

                else: 
                    return singleton((CompositeHeader(8), CompositeCell(1, match_value_2)))


            def _arrow3933(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                def _arrow3927(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                    match_value_3: str | None = LDLabProtocol.try_get_description_as_string(prot_1, context)
                    if match_value_3 is None:
                        return empty_1()

                    else: 
                        return singleton((CompositeHeader(5), CompositeCell(1, match_value_3)))


                def _arrow3932(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                    def _arrow3928(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                        match_value_4: str | None = LDLabProtocol.try_get_url(prot_1, context)
                        if match_value_4 is None:
                            return empty_1()

                        else: 
                            return singleton((CompositeHeader(6), CompositeCell(1, match_value_4)))


                    def _arrow3931(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                        def _arrow3929(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                            match_value_5: str | None = LDLabProtocol.try_get_version_as_string(prot_1, context)
                            if match_value_5 is None:
                                return empty_1()

                            else: 
                                return singleton((CompositeHeader(7), CompositeCell(1, match_value_5)))


                        def _arrow3930(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                            match_value_6: OntologyAnnotation | None = ProcessConversion_tryGetProtocolType_Z6839B9E8(prot_1, graph, context)
                            if match_value_6 is None:
                                return empty_1()

                            else: 
                                return singleton((CompositeHeader(4), CompositeCell(0, match_value_6)))


                        return append(_arrow3929(), delay(_arrow3930))

                    return append(_arrow3928(), delay(_arrow3931))

                return append(_arrow3927(), delay(_arrow3932))

            return append(_arrow3926(), delay(_arrow3933))

        prot_vals = to_list(delay(_arrow3934))

    def f_2(c: str, p: Any=p, graph: Any=graph, context: Any=context) -> tuple[CompositeHeader, CompositeCell]:
        c_1: Comment = Comment.from_string(c)
        return (CompositeHeader(14, default_arg(c_1.Name, "")), CompositeCell(1, default_arg(c_1.Value, "")))

    comments: Array[tuple[CompositeHeader, CompositeCell]] = ResizeArray_map(f_2, LDLabProcess.get_disambiguating_descriptions_as_string(p, context))
    inputs: Array[LDNode] = LDLabProcess.get_objects(p, graph, context)
    outputs: Array[LDNode] = LDLabProcess.get_results(p, graph, context)
    def _arrow3935(Value: LDNode, p: Any=p, graph: Any=graph, context: Any=context) -> LDNode | None:
        return Value

    def _arrow3936(Value_1: LDNode, p: Any=p, graph: Any=graph, context: Any=context) -> LDNode | None:
        return Value_1

    def _arrow3937(Value_2: LDNode, p: Any=p, graph: Any=graph, context: Any=context) -> LDNode | None:
        return Value_2

    def _arrow3938(Value_3: LDNode, p: Any=p, graph: Any=graph, context: Any=context) -> LDNode | None:
        return Value_3

    pattern_input: tuple[Array[LDNode | None], Array[LDNode | None]] = ((ResizeArray_create(len(outputs), None), ResizeArray_map(_arrow3935, outputs))) if ((len(outputs) != 0) if (len(inputs) == 0) else False) else (((ResizeArray_map(_arrow3936, inputs), ResizeArray_create(len(inputs), None))) if ((len(outputs) == 0) if (len(inputs) != 0) else False) else ((ResizeArray_map(_arrow3937, inputs), ResizeArray_map(_arrow3938, outputs))))
    outputs_1: Array[LDNode | None] = pattern_input[1]
    inputs_1: Array[LDNode | None] = pattern_input[0]
    if (len(outputs_1) == 0) if (len(inputs_1) == 0) else False:
        def mapping(tuple_1: tuple[tuple[CompositeHeader, CompositeCell], int | None], p: Any=p, graph: Any=graph, context: Any=context) -> tuple[CompositeHeader, CompositeCell]:
            return tuple_1[0]

        def projection(arg: tuple[tuple[CompositeHeader, CompositeCell], int | None], p: Any=p, graph: Any=graph, context: Any=context) -> int:
            return default_arg(arg[1], 10000)

        def _arrow3940(__unit: None=None, p: Any=p, graph: Any=graph, context: Any=context) -> IEnumerable_1[tuple[tuple[CompositeHeader, CompositeCell], int | None]]:
            def _arrow3939(__unit: None=None) -> IEnumerable_1[tuple[tuple[CompositeHeader, CompositeCell], int | None]]:
                return pvs

            return append(components, delay(_arrow3939))

        class ObjectExpr3941:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        vals: FSharpList[tuple[CompositeHeader, CompositeCell]] = map_2(mapping, sort_by(projection, to_list(delay(_arrow3940)), ObjectExpr3941()))
        def _arrow3944(__unit: None=None, p: Any=p, graph: Any=graph, context: Any=context) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
            def _arrow3943(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                def _arrow3942(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                    return comments

                return append(vals, delay(_arrow3942))

            return append(prot_vals, delay(_arrow3943))

        return ResizeArray_singleton(to_list(delay(_arrow3944)))

    else: 
        def f_5(tupled_arg: tuple[LDNode | None, LDNode | None], p: Any=p, graph: Any=graph, context: Any=context) -> FSharpList[tuple[CompositeHeader, CompositeCell]]:
            i: LDNode | None = tupled_arg[0]
            o: LDNode | None = tupled_arg[1]
            chars: Array[tuple[tuple[CompositeHeader, CompositeCell], int | None]]
            if i is None:
                chars = []

            else: 
                i_1: LDNode = i
                def f_3(cv: LDNode, tupled_arg: Any=tupled_arg) -> tuple[tuple[CompositeHeader, CompositeCell], int | None]:
                    return (BaseTypes_decomposeCharacteristicValue_Z2F770004(cv, context), try_get_index(cv))

                chars = ResizeArray_map(f_3, LDSample.get_characteristics(i_1, graph, context))

            factors: Array[tuple[tuple[CompositeHeader, CompositeCell], int | None]]
            if o is None:
                factors = []

            else: 
                o_1: LDNode = o
                def f_4(fv: LDNode, tupled_arg: Any=tupled_arg) -> tuple[tuple[CompositeHeader, CompositeCell], int | None]:
                    return (BaseTypes_decomposeFactorValue_Z2F770004(fv, context), try_get_index(fv))

                factors = ResizeArray_map(f_4, LDSample.get_factors(o_1, graph, context))

            def mapping_1(tuple_3: tuple[tuple[CompositeHeader, CompositeCell], int | None], tupled_arg: Any=tupled_arg) -> tuple[CompositeHeader, CompositeCell]:
                return tuple_3[0]

            def projection_1(arg_1: tuple[tuple[CompositeHeader, CompositeCell], int | None], tupled_arg: Any=tupled_arg) -> int:
                return default_arg(arg_1[1], 10000)

            def _arrow3948(__unit: None=None, tupled_arg: Any=tupled_arg) -> IEnumerable_1[tuple[tuple[CompositeHeader, CompositeCell], int | None]]:
                def _arrow3947(__unit: None=None) -> IEnumerable_1[tuple[tuple[CompositeHeader, CompositeCell], int | None]]:
                    def _arrow3946(__unit: None=None) -> IEnumerable_1[tuple[tuple[CompositeHeader, CompositeCell], int | None]]:
                        def _arrow3945(__unit: None=None) -> IEnumerable_1[tuple[tuple[CompositeHeader, CompositeCell], int | None]]:
                            return factors

                        return append(pvs, delay(_arrow3945))

                    return append(components, delay(_arrow3946))

                return append(chars, delay(_arrow3947))

            class ObjectExpr3949:
                @property
                def Compare(self) -> Callable[[int, int], int]:
                    return compare_primitives

            vals_1: FSharpList[tuple[CompositeHeader, CompositeCell]] = map_2(mapping_1, sort_by(projection_1, to_list(delay(_arrow3948)), ObjectExpr3949()))
            def _arrow3954(__unit: None=None, tupled_arg: Any=tupled_arg) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                def _arrow3953(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                    def _arrow3952(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                        def _arrow3951(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                            def _arrow3950(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                                return singleton(BaseTypes_decomposeProcessOutput_Z2F770004(value_2(o), context)) if (o is not None) else empty_1()

                            return append(comments, delay(_arrow3950))

                        return append(vals_1, delay(_arrow3951))

                    return append(prot_vals, delay(_arrow3952))

                return append(singleton(BaseTypes_decomposeProcessInput_Z2F770004(value_2(i), context)) if (i is not None) else empty_1(), delay(_arrow3953))

            return to_list(delay(_arrow3954))

        return ResizeArray_map(f_5, ResizeArray_zip(inputs_1, outputs_1))



__all__ = ["ProcessConversion_reflection", "ProcessConversion_tryGetProtocolType_Z6839B9E8", "ProcessConversion_composeProcessName", "ProcessConversion_decomposeProcessName_Z721C83C5", "ProcessConversion_tryComponentGetter", "ProcessConversion_tryParameterGetter", "ProcessConversion_tryFactorGetter", "ProcessConversion_tryCharacteristicGetter", "ProcessConversion_tryGetProtocolTypeGetter", "ProcessConversion_tryGetProtocolREFGetter", "ProcessConversion_tryGetProtocolDescriptionGetter", "ProcessConversion_tryGetProtocolURIGetter", "ProcessConversion_tryGetProtocolVersionGetter", "ProcessConversion_tryGetInputGetter", "ProcessConversion_tryGetOutputGetter", "ProcessConversion_tryGetCommentGetter", "ProcessConversion_tryGetPerformerGetter", "ProcessConversion_getProcessGetter", "ProcessConversion_groupProcesses_Z27F0B586", "ProcessConversion_processToRows_Z6839B9E8"]

