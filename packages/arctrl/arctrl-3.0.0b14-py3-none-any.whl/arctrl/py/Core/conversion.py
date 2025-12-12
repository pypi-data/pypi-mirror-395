from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (FSharpList, choose as choose_1, singleton, is_empty, of_array, length, empty, map as map_2, item, map_indexed, collect, try_pick as try_pick_1, head, sort_by, append as append_1, zip, initialize)
from ..fable_modules.fable_library.option import (default_arg, map, value as value_10)
from ..fable_modules.fable_library.range import range_big_int
from ..fable_modules.fable_library.reg_exp import (get_item, groups)
from ..fable_modules.fable_library.seq import (choose, try_pick, indexed, to_list, filter, map as map_1, delay, append, singleton as singleton_1, empty as empty_1, fold, zip as zip_1)
from ..fable_modules.fable_library.seq2 import (List_groupBy, List_distinct)
from ..fable_modules.fable_library.string_ import (to_text, printf, starts_with_exact, ends_with_exact, to_fail)
from ..fable_modules.fable_library.types import (Array, to_string)
from ..fable_modules.fable_library.util import (IEnumerable_1, int32_to_string, string_hash, equal_arrays, array_hash, compare_primitives, get_enumerator, ignore, equals, safe_hash)
from .comment import Comment
from .data import Data
from .data_file import DataFile
from .Helper.collections_ import (ResizeArray_filter, Option_fromValueWithDefault, ResizeArray_singleton)
from .Helper.hash_codes import (box_hash_option, box_hash_seq)
from .Helper.identifier import create_missing_identifier
from .Helper.regex import ActivePatterns__007CRegex_007C__007C
from .ontology_annotation import OntologyAnnotation
from .person import Person
from .Process.column_index import (ARCtrl_OntologyAnnotation__OntologyAnnotation_SetColumnIndex_Z524259A4, ARCtrl_OntologyAnnotation__OntologyAnnotation_setColumnIndex_Static, try_get_parameter_column_index, try_get_component_index, try_get_characteristic_column_index, try_get_factor_column_index, ARCtrl_Process_ProtocolParameter__ProtocolParameter_TryGetColumnIndex, ARCtrl_Process_Component__Component_TryGetColumnIndex)
from .Process.component import (Component_create_Z2F0B38C7, Component)
from .Process.factor import Factor
from .Process.factor_value import (FactorValue_create_30BDC49, FactorValue)
from .Process.material_attribute import (MaterialAttribute_create_A220A8A, MaterialAttribute)
from .Process.material_attribute_value import (MaterialAttributeValue_create_ZE1D108D, MaterialAttributeValue)
from .Process.process import (Process_composeName, Process_make, Process, Process_decomposeName_Z721C83C5, Process_create_Z7C1F7FA9)
from .Process.process_input import (ProcessInput_createSample_Z598187B7, ProcessInput_createMaterial_4452CB4C, ProcessInput_createRawData_Z721C83C5, ProcessInput_createSource_Z5E00540E, ProcessInput, ProcessInput__isSample, ProcessInput__isSource, ProcessInput__get_Name, ProcessInput_setCharacteristicValues, ProcessInput__isData, ProcessInput__isMaterial, ProcessInput_getCharacteristicValues_5B3D5BA9)
from .Process.process_output import (ProcessOutput_createSample_Z598187B7, ProcessOutput_createMaterial_4452CB4C, ProcessOutput_createRawData_Z721C83C5, ProcessOutput, ProcessOutput__isSample, ProcessOutput__get_Name, ProcessOutput_setFactorValues, ProcessOutput__isData, ProcessOutput__isMaterial, ProcessOutput_getFactorValues_Z42C11600)
from .Process.process_parameter_value import ProcessParameterValue
from .Process.protocol import (Protocol, Protocol_make, Protocol_setProtocolType, Protocol_setVersion, Protocol_setUri, Protocol_setDescription, Protocol_setName, Protocol_addParameter, Protocol_addComponent, Protocol_create_Z414665E7)
from .Process.protocol_parameter import ProtocolParameter
from .Process.sample import Sample_create_62424AD2
from .Process.source import Source_create_Z5CA08497
from .Table.arc_table import ArcTable
from .Table.arc_table_aux import (Unchecked_tryGetCellAt, get_empty_cell_for_header, Unchecked_alignByHeaders, ArcTableValues)
from .Table.arc_tables import ArcTables
from .Table.composite_cell import CompositeCell
from .Table.composite_header import (CompositeHeader, IOType)
from .value import Value as Value_2

Person_orcidKey: str = "ORCID"

Person_AssayIdentifierPrefix: str = "performer (ARC:00000168)"

def _arrow1002(__unit: None=None) -> Callable[[str], str]:
    clo_1: Callable[[str], str] = to_text(printf("%s %s"))(Person_AssayIdentifierPrefix)
    return clo_1


Person_createAssayIdentifierKey: Callable[[str], str] = _arrow1002()

def Person_setSourceAssayComment(person: Person, assay_identifier: str) -> Person:
    person_1: Person = person.Copy()
    comment: Comment = Comment(Person_createAssayIdentifierKey(assay_identifier), assay_identifier)
    (person_1.Comments.append(comment))
    return person_1


def Person_getSourceAssayIdentifiersFromComments(person: Person) -> IEnumerable_1[str]:
    def chooser(c: Comment, person: Any=person) -> str | None:
        def mapping(n: str, c: Any=c) -> bool:
            return starts_with_exact(n, Person_AssayIdentifierPrefix)

        if default_arg(map(mapping, c.Name), False):
            return c.Value

        else: 
            return None


    return choose(chooser, person.Comments)


def Person_removeSourceAssayComments(person: Person) -> Array[Comment]:
    def f(c: Comment, person: Any=person) -> bool:
        if c.Name is not None:
            return not starts_with_exact(value_10(c.Name), Person_AssayIdentifierPrefix)

        else: 
            return False


    return ResizeArray_filter(f, person.Comments)


def Person_setOrcidFromComments(person: Person) -> Person:
    person_1: Person = person.Copy()
    def is_orcid_comment(c: Comment, person: Any=person) -> bool:
        if c.Name is not None:
            return ends_with_exact(value_10(c.Name).upper(), Person_orcidKey)

        else: 
            return False


    def chooser(c_1: Comment, person: Any=person) -> str | None:
        if is_orcid_comment(c_1):
            return c_1.Value

        else: 
            return None


    def f(arg: Comment, person: Any=person) -> bool:
        return not is_orcid_comment(arg)

    pattern_input: tuple[str | None, Array[Comment]] = (try_pick(chooser, person_1.Comments), ResizeArray_filter(f, person_1.Comments))
    person_1.ORCID = pattern_input[0]
    person_1.Comments = pattern_input[1]
    return person_1


def Person_setCommentFromORCID(person: Person) -> Person:
    person_1: Person = person.Copy()
    match_value: str | None = person_1.ORCID
    if match_value is None:
        pass

    else: 
        orcid: str = match_value
        comment: Comment = Comment.create(Person_orcidKey, orcid)
        (person_1.Comments.append(comment))

    return person_1


def JsonTypes_valueOfCell(value: CompositeCell) -> tuple[Value_2 | None, OntologyAnnotation | None]:
    if value.tag == 0:
        if value.fields[0].is_empty():
            return (None, None)

        else: 
            return (Value_2(0, value.fields[0]), None)


    elif value.tag == 2:
        return (None if (value.fields[0] == "") else Value_2.from_string(value.fields[0]), None if value.fields[1].is_empty() else value.fields[1])

    elif value.tag == 3:
        raise Exception("Data cell should not be parsed to isa value")

    elif value.fields[0] == "":
        return (None, None)

    else: 
        return (Value_2.from_string(value.fields[0]), None)



def JsonTypes_composeComponent(header: CompositeHeader, value: CompositeCell) -> Component:
    pattern_input: tuple[Value_2 | None, OntologyAnnotation | None] = JsonTypes_valueOfCell(value)
    return Component_create_Z2F0B38C7(pattern_input[0], pattern_input[1], header.ToTerm())


def JsonTypes_composeParameterValue(header: CompositeHeader, value: CompositeCell) -> ProcessParameterValue:
    pattern_input: tuple[Value_2 | None, OntologyAnnotation | None] = JsonTypes_valueOfCell(value)
    p: ProtocolParameter = ProtocolParameter.create(None, header.ToTerm())
    return ProcessParameterValue.create(p, pattern_input[0], pattern_input[1])


def JsonTypes_composeFactorValue(header: CompositeHeader, value: CompositeCell) -> FactorValue:
    pattern_input: tuple[Value_2 | None, OntologyAnnotation | None] = JsonTypes_valueOfCell(value)
    return FactorValue_create_30BDC49(None, Factor.create(to_string(header), header.ToTerm()), pattern_input[0], pattern_input[1])


def JsonTypes_composeCharacteristicValue(header: CompositeHeader, value: CompositeCell) -> MaterialAttributeValue:
    pattern_input: tuple[Value_2 | None, OntologyAnnotation | None] = JsonTypes_valueOfCell(value)
    return MaterialAttributeValue_create_ZE1D108D(None, MaterialAttribute_create_A220A8A(None, header.ToTerm()), pattern_input[0], pattern_input[1])


def JsonTypes_composeFreetextMaterialName(header_ft: str, name: str) -> str:
    return ((("" + header_ft) + "=") + name) + ""


def JsonTypes_composeProcessInput(header: CompositeHeader, value: CompositeCell) -> ProcessInput:
    if header.tag == 11:
        if header.fields[0].tag == 1:
            return ProcessInput_createSample_Z598187B7(to_string(value))

        elif header.fields[0].tag == 3:
            return ProcessInput_createMaterial_4452CB4C(to_string(value))

        elif header.fields[0].tag == 2:
            return ProcessInput_createRawData_Z721C83C5(to_string(value))

        elif header.fields[0].tag == 4:
            return ProcessInput_createMaterial_4452CB4C(JsonTypes_composeFreetextMaterialName(header.fields[0].fields[0], to_string(value)))

        else: 
            return ProcessInput_createSource_Z5E00540E(to_string(value))


    else: 
        return to_fail(printf("Could not parse input header %O"))(header)



def JsonTypes_composeProcessOutput(header: CompositeHeader, value: CompositeCell) -> ProcessOutput:
    (pattern_matching_result, ft) = (None, None)
    if header.tag == 12:
        if header.fields[0].tag == 1:
            pattern_matching_result = 0

        elif header.fields[0].tag == 3:
            pattern_matching_result = 1

        elif header.fields[0].tag == 2:
            pattern_matching_result = 2

        elif header.fields[0].tag == 4:
            pattern_matching_result = 3
            ft = header.fields[0].fields[0]

        else: 
            pattern_matching_result = 0


    else: 
        pattern_matching_result = 4

    if pattern_matching_result == 0:
        return ProcessOutput_createSample_Z598187B7(to_string(value))

    elif pattern_matching_result == 1:
        return ProcessOutput_createMaterial_4452CB4C(to_string(value))

    elif pattern_matching_result == 2:
        return ProcessOutput_createRawData_Z721C83C5(to_string(value))

    elif pattern_matching_result == 3:
        return ProcessOutput_createMaterial_4452CB4C(JsonTypes_composeFreetextMaterialName(ft, to_string(value)))

    elif pattern_matching_result == 4:
        return to_fail(printf("Could not parse output header %O"))(header)



def JsonTypes_cellOfValue(value: Value_2 | None=None, unit: OntologyAnnotation | None=None) -> CompositeCell:
    value_2: Value_2 = default_arg(value, Value_2(3, ""))
    (pattern_matching_result, oa, text, name, u, f, u_1, f_1, i, u_2, i_1) = (None, None, None, None, None, None, None, None, None, None, None)
    if value_2.tag == 3:
        if value_2.fields[0] == "":
            if unit is not None:
                pattern_matching_result = 3
                name = value_2.fields[0]
                u = unit

            else: 
                pattern_matching_result = 1


        elif unit is not None:
            pattern_matching_result = 3
            name = value_2.fields[0]
            u = unit

        else: 
            pattern_matching_result = 2
            text = value_2.fields[0]


    elif value_2.tag == 2:
        if unit is None:
            pattern_matching_result = 5
            f_1 = value_2.fields[0]

        else: 
            pattern_matching_result = 4
            f = value_2.fields[0]
            u_1 = unit


    elif value_2.tag == 1:
        if unit is None:
            pattern_matching_result = 7
            i_1 = value_2.fields[0]

        else: 
            pattern_matching_result = 6
            i = value_2.fields[0]
            u_2 = unit


    elif unit is None:
        pattern_matching_result = 0
        oa = value_2.fields[0]

    else: 
        pattern_matching_result = 8

    if pattern_matching_result == 0:
        return CompositeCell(0, oa)

    elif pattern_matching_result == 1:
        return CompositeCell(0, OntologyAnnotation())

    elif pattern_matching_result == 2:
        return CompositeCell(0, OntologyAnnotation(text))

    elif pattern_matching_result == 3:
        return CompositeCell(2, name, u)

    elif pattern_matching_result == 4:
        return CompositeCell(2, to_string(f), u_1)

    elif pattern_matching_result == 5:
        return CompositeCell(2, to_string(f_1), OntologyAnnotation())

    elif pattern_matching_result == 6:
        return CompositeCell(2, int32_to_string(i), u_2)

    elif pattern_matching_result == 7:
        return CompositeCell(2, int32_to_string(i_1), OntologyAnnotation())

    elif pattern_matching_result == 8:
        return to_fail(printf("Could not parse value %O with unit %O"))(value_2)(unit)



def JsonTypes_decomposeComponent(c: Component) -> tuple[CompositeHeader, CompositeCell]:
    return (CompositeHeader(0, value_10(c.ComponentType)), JsonTypes_cellOfValue(c.ComponentValue, c.ComponentUnit))


def JsonTypes_decomposeParameterValue(ppv: ProcessParameterValue) -> tuple[CompositeHeader, CompositeCell]:
    return (CompositeHeader(3, value_10(value_10(ppv.Category).ParameterName)), JsonTypes_cellOfValue(ppv.Value, ppv.Unit))


def JsonTypes_decomposeFactorValue(fv: FactorValue) -> tuple[CompositeHeader, CompositeCell]:
    return (CompositeHeader(2, value_10(value_10(fv.Category).FactorType)), JsonTypes_cellOfValue(fv.Value, fv.Unit))


def JsonTypes_decomposeCharacteristicValue(cv: MaterialAttributeValue) -> tuple[CompositeHeader, CompositeCell]:
    return (CompositeHeader(1, value_10(value_10(cv.Category).CharacteristicType)), JsonTypes_cellOfValue(cv.Value, cv.Unit))


def JsonTypes_decomposeProcessInput(pi: ProcessInput) -> tuple[CompositeHeader, CompositeCell]:
    if pi.tag == 1:
        return (CompositeHeader(11, IOType(1)), CompositeCell(1, default_arg(pi.fields[0].Name, "")))

    elif pi.tag == 3:
        return (CompositeHeader(11, IOType(3)), CompositeCell(1, default_arg(pi.fields[0].Name, "")))

    elif pi.tag == 2:
        d: Data = pi.fields[0]
        data_type: DataFile = value_10(d.DataType)
        if data_type.tag == 0:
            return (CompositeHeader(11, IOType(2)), CompositeCell(1, default_arg(d.Name, "")))

        elif data_type.tag == 1:
            return (CompositeHeader(11, IOType(2)), CompositeCell(1, default_arg(d.Name, "")))

        else: 
            return (CompositeHeader(11, IOType(2)), CompositeCell(1, default_arg(d.Name, "")))


    else: 
        return (CompositeHeader(11, IOType(0)), CompositeCell(1, default_arg(pi.fields[0].Name, "")))



def JsonTypes_decomposeProcessOutput(po: ProcessOutput) -> tuple[CompositeHeader, CompositeCell]:
    if po.tag == 2:
        return (CompositeHeader(12, IOType(3)), CompositeCell(1, default_arg(po.fields[0].Name, "")))

    elif po.tag == 1:
        d: Data = po.fields[0]
        data_type: DataFile = value_10(d.DataType)
        if data_type.tag == 0:
            return (CompositeHeader(12, IOType(2)), CompositeCell(1, default_arg(d.Name, "")))

        elif data_type.tag == 1:
            return (CompositeHeader(12, IOType(2)), CompositeCell(1, default_arg(d.Name, "")))

        else: 
            return (CompositeHeader(12, IOType(2)), CompositeCell(1, default_arg(d.Name, "")))


    else: 
        return (CompositeHeader(12, IOType(1)), CompositeCell(1, default_arg(po.fields[0].Name, "")))



def JsonTypes_composeTechnologyPlatform(tp: OntologyAnnotation) -> str:
    match_value: dict[str, Any] | None = tp.TANInfo
    if match_value is None:
        return ("" + tp.NameText) + ""

    else: 
        return ((("" + tp.NameText) + " (") + tp.TermAccessionShort) + ")"



def JsonTypes_decomposeTechnologyPlatform(name: str) -> OntologyAnnotation:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(?<value>.+) \\((?<ontology>[^(]*:[^)]*)\\)$", name)
    if active_pattern_result is not None:
        r: Any = active_pattern_result
        oa: OntologyAnnotation
        tan: str = get_item(groups(r), "ontology") or ""
        oa = OntologyAnnotation.from_term_annotation(tan)
        v: str = get_item(groups(r), "value") or ""
        return OntologyAnnotation.create(v, oa.TermSourceREF, oa.TermAccessionNumber)

    else: 
        return OntologyAnnotation.create(name)



def ProcessParsing_tryComponentGetter(general_i: int, value_i: int, value_header: CompositeHeader) -> Callable[[ArcTable, int], Component] | None:
    if value_header.tag == 0:
        new_oa: OntologyAnnotation = value_header.fields[0].Copy()
        ARCtrl_OntologyAnnotation__OntologyAnnotation_SetColumnIndex_Z524259A4(new_oa, value_i)
        cat: CompositeHeader = CompositeHeader(0, new_oa)
        def Value(table: ArcTable, general_i: Any=general_i, value_i: Any=value_i, value_header: Any=value_header) -> Callable[[int], Component]:
            def _arrow1004(i: int, table: Any=table) -> Component:
                def _arrow1003(__unit: None=None) -> CompositeCell:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                    return get_empty_cell_for_header(cat, None) if (match_value is None) else match_value

                return JsonTypes_composeComponent(cat, _arrow1003())

            return _arrow1004

        return Value

    else: 
        return None



def ProcessParsing_tryParameterGetter(general_i: int, value_i: int, value_header: CompositeHeader) -> Callable[[ArcTable, int], ProcessParameterValue] | None:
    if value_header.tag == 3:
        cat: CompositeHeader = CompositeHeader(3, ARCtrl_OntologyAnnotation__OntologyAnnotation_setColumnIndex_Static(value_i, value_header.fields[0]))
        def Value(table: ArcTable, general_i: Any=general_i, value_i: Any=value_i, value_header: Any=value_header) -> Callable[[int], ProcessParameterValue]:
            def _arrow1006(i_1: int, table: Any=table) -> ProcessParameterValue:
                def _arrow1005(__unit: None=None) -> CompositeCell:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i_1, table.Values)
                    return get_empty_cell_for_header(cat, None) if (match_value is None) else match_value

                return JsonTypes_composeParameterValue(cat, _arrow1005())

            return _arrow1006

        return Value

    else: 
        return None



def ProcessParsing_tryFactorGetter(general_i: int, value_i: int, value_header: CompositeHeader) -> Callable[[ArcTable, int], FactorValue] | None:
    if value_header.tag == 2:
        cat: CompositeHeader = CompositeHeader(2, ARCtrl_OntologyAnnotation__OntologyAnnotation_setColumnIndex_Static(value_i, value_header.fields[0]))
        def Value(table: ArcTable, general_i: Any=general_i, value_i: Any=value_i, value_header: Any=value_header) -> Callable[[int], FactorValue]:
            def _arrow1008(i_1: int, table: Any=table) -> FactorValue:
                def _arrow1007(__unit: None=None) -> CompositeCell:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i_1, table.Values)
                    return get_empty_cell_for_header(cat, None) if (match_value is None) else match_value

                return JsonTypes_composeFactorValue(cat, _arrow1007())

            return _arrow1008

        return Value

    else: 
        return None



def ProcessParsing_tryCharacteristicGetter(general_i: int, value_i: int, value_header: CompositeHeader) -> Callable[[ArcTable, int], MaterialAttributeValue] | None:
    if value_header.tag == 1:
        cat: CompositeHeader = CompositeHeader(1, ARCtrl_OntologyAnnotation__OntologyAnnotation_setColumnIndex_Static(value_i, value_header.fields[0]))
        def Value(table: ArcTable, general_i: Any=general_i, value_i: Any=value_i, value_header: Any=value_header) -> Callable[[int], MaterialAttributeValue]:
            def _arrow1010(i_1: int, table: Any=table) -> MaterialAttributeValue:
                def _arrow1009(__unit: None=None) -> CompositeCell:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i_1, table.Values)
                    return get_empty_cell_for_header(cat, None) if (match_value is None) else match_value

                return JsonTypes_composeCharacteristicValue(cat, _arrow1009())

            return _arrow1010

        return Value

    else: 
        return None



def ProcessParsing_tryGetProtocolTypeGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], OntologyAnnotation] | None:
    if header.tag == 4:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], OntologyAnnotation]:
            def _arrow1011(i: int, table: Any=table) -> OntologyAnnotation:
                match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                if match_value is None:
                    return OntologyAnnotation()

                else: 
                    cell: CompositeCell = match_value
                    return cell.AsTerm


            return _arrow1011

        return Value

    else: 
        return None



def ProcessParsing_tryGetProtocolREFGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], str] | None:
    if header.tag == 8:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], str]:
            def _arrow1012(i: int, table: Any=table) -> str:
                match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                if match_value is None:
                    return ""

                else: 
                    cell: CompositeCell = match_value
                    return cell.AsFreeText


            return _arrow1012

        return Value

    else: 
        return None



def ProcessParsing_tryGetProtocolDescriptionGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], str] | None:
    if header.tag == 5:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], str]:
            def _arrow1013(i: int, table: Any=table) -> str:
                match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                if match_value is None:
                    return ""

                else: 
                    cell: CompositeCell = match_value
                    return cell.AsFreeText


            return _arrow1013

        return Value

    else: 
        return None



def ProcessParsing_tryGetProtocolURIGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], str] | None:
    if header.tag == 6:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], str]:
            def _arrow1014(i: int, table: Any=table) -> str:
                match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                if match_value is None:
                    return ""

                else: 
                    cell: CompositeCell = match_value
                    return cell.AsFreeText


            return _arrow1014

        return Value

    else: 
        return None



def ProcessParsing_tryGetProtocolVersionGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], str] | None:
    if header.tag == 7:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], str]:
            def _arrow1015(i: int, table: Any=table) -> str:
                match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                if match_value is None:
                    return ""

                else: 
                    cell: CompositeCell = match_value
                    return cell.AsFreeText


            return _arrow1015

        return Value

    else: 
        return None



def ProcessParsing_tryGetInputGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], ProcessInput] | None:
    if header.tag == 11:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], ProcessInput]:
            def _arrow1017(i: int, table: Any=table) -> ProcessInput:
                def _arrow1016(__unit: None=None) -> CompositeCell:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                    return get_empty_cell_for_header(header, None) if (match_value is None) else match_value

                return JsonTypes_composeProcessInput(header, _arrow1016())

            return _arrow1017

        return Value

    else: 
        return None



def ProcessParsing_tryGetOutputGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], ProcessOutput] | None:
    if header.tag == 12:
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], ProcessOutput]:
            def _arrow1019(i: int, table: Any=table) -> ProcessOutput:
                def _arrow1018(__unit: None=None) -> CompositeCell:
                    match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                    return get_empty_cell_for_header(header, None) if (match_value is None) else match_value

                return JsonTypes_composeProcessOutput(header, _arrow1018())

            return _arrow1019

        return Value

    else: 
        return None



def ProcessParsing_tryGetCommentGetter(general_i: int, header: CompositeHeader) -> Callable[[ArcTable, int], Comment] | None:
    if header.tag == 14:
        c: str = header.fields[0]
        def Value(table: ArcTable, general_i: Any=general_i, header: Any=header) -> Callable[[int], Comment]:
            def _arrow1020(i: int, table: Any=table) -> Comment:
                match_value: CompositeCell | None = Unchecked_tryGetCellAt(general_i, i, table.Values)
                if match_value is None:
                    return Comment(c)

                else: 
                    cell: CompositeCell = match_value
                    return Comment(c, cell.AsFreeText)


            return _arrow1020

        return Value

    else: 
        return None



def ProcessParsing_getProcessGetter(process_name_root: str, headers: IEnumerable_1[CompositeHeader]) -> Callable[[ArcTable, int], Process]:
    headers_1: IEnumerable_1[tuple[int, CompositeHeader]] = indexed(headers)
    def predicate(arg: tuple[int, CompositeHeader], process_name_root: Any=process_name_root, headers: Any=headers) -> bool:
        return arg[1].IsCvParamColumn

    value_headers: FSharpList[tuple[int, tuple[int, CompositeHeader]]] = to_list(indexed(filter(predicate, headers_1)))
    def chooser(tupled_arg: tuple[int, tuple[int, CompositeHeader]], process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[ArcTable, int], MaterialAttributeValue] | None:
        _arg: tuple[int, CompositeHeader] = tupled_arg[1]
        return ProcessParsing_tryCharacteristicGetter(_arg[0], tupled_arg[0], _arg[1])

    char_getters: FSharpList[Callable[[ArcTable, int], MaterialAttributeValue]] = choose_1(chooser, value_headers)
    def chooser_1(tupled_arg_1: tuple[int, tuple[int, CompositeHeader]], process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[ArcTable, int], FactorValue] | None:
        _arg_1: tuple[int, CompositeHeader] = tupled_arg_1[1]
        return ProcessParsing_tryFactorGetter(_arg_1[0], tupled_arg_1[0], _arg_1[1])

    factor_value_getters: FSharpList[Callable[[ArcTable, int], FactorValue]] = choose_1(chooser_1, value_headers)
    def chooser_2(tupled_arg_2: tuple[int, tuple[int, CompositeHeader]], process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[ArcTable, int], ProcessParameterValue] | None:
        _arg_2: tuple[int, CompositeHeader] = tupled_arg_2[1]
        return ProcessParsing_tryParameterGetter(_arg_2[0], tupled_arg_2[0], _arg_2[1])

    parameter_value_getters: FSharpList[Callable[[ArcTable, int], ProcessParameterValue]] = choose_1(chooser_2, value_headers)
    def chooser_3(tupled_arg_3: tuple[int, tuple[int, CompositeHeader]], process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[ArcTable, int], Component] | None:
        _arg_3: tuple[int, CompositeHeader] = tupled_arg_3[1]
        return ProcessParsing_tryComponentGetter(_arg_3[0], tupled_arg_3[0], _arg_3[1])

    component_getters: FSharpList[Callable[[ArcTable, int], Component]] = choose_1(chooser_3, value_headers)
    def chooser_4(tupled_arg_4: tuple[int, CompositeHeader], process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[ArcTable, int], OntologyAnnotation] | None:
        return ProcessParsing_tryGetProtocolTypeGetter(tupled_arg_4[0], tupled_arg_4[1])

    protocol_type_getter: Callable[[ArcTable, int], OntologyAnnotation] | None = try_pick(chooser_4, headers_1)
    def chooser_5(tupled_arg_5: tuple[int, CompositeHeader], process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[ArcTable, int], str] | None:
        return ProcessParsing_tryGetProtocolREFGetter(tupled_arg_5[0], tupled_arg_5[1])

    protocol_refgetter: Callable[[ArcTable, int], str] | None = try_pick(chooser_5, headers_1)
    def chooser_6(tupled_arg_6: tuple[int, CompositeHeader], process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[ArcTable, int], str] | None:
        return ProcessParsing_tryGetProtocolDescriptionGetter(tupled_arg_6[0], tupled_arg_6[1])

    protocol_description_getter: Callable[[ArcTable, int], str] | None = try_pick(chooser_6, headers_1)
    def chooser_7(tupled_arg_7: tuple[int, CompositeHeader], process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[ArcTable, int], str] | None:
        return ProcessParsing_tryGetProtocolURIGetter(tupled_arg_7[0], tupled_arg_7[1])

    protocol_urigetter: Callable[[ArcTable, int], str] | None = try_pick(chooser_7, headers_1)
    def chooser_8(tupled_arg_8: tuple[int, CompositeHeader], process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[ArcTable, int], str] | None:
        return ProcessParsing_tryGetProtocolVersionGetter(tupled_arg_8[0], tupled_arg_8[1])

    protocol_version_getter: Callable[[ArcTable, int], str] | None = try_pick(chooser_8, headers_1)
    def chooser_9(tupled_arg_9: tuple[int, CompositeHeader], process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[ArcTable, int], Comment] | None:
        return ProcessParsing_tryGetCommentGetter(tupled_arg_9[0], tupled_arg_9[1])

    comment_getters: FSharpList[Callable[[ArcTable, int], Comment]] = to_list(choose(chooser_9, headers_1))
    input_getter_1: Callable[[ArcTable, int], FSharpList[ProcessInput]]
    def chooser_10(tupled_arg_10: tuple[int, CompositeHeader], process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[ArcTable, int], ProcessInput] | None:
        return ProcessParsing_tryGetInputGetter(tupled_arg_10[0], tupled_arg_10[1])

    match_value: Callable[[ArcTable, int], ProcessInput] | None = try_pick(chooser_10, headers_1)
    if match_value is None:
        def _arrow1022(table_1: ArcTable, process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[int], FSharpList[ProcessInput]]:
            def _arrow1021(i_1: int) -> FSharpList[ProcessInput]:
                def mapping_1(f_1: Callable[[ArcTable, int], MaterialAttributeValue]) -> MaterialAttributeValue:
                    return f_1(table_1)(i_1)

                return singleton(ProcessInput(0, Source_create_Z5CA08497(None, ((("" + process_name_root) + "_Input_") + str(i_1)) + "", to_list(map_1(mapping_1, char_getters)))))

            return _arrow1021

        input_getter_1 = _arrow1022

    else: 
        input_getter: Callable[[ArcTable, int], ProcessInput] = match_value
        def _arrow1024(table: ArcTable, process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[int], FSharpList[ProcessInput]]:
            def _arrow1023(i: int) -> FSharpList[ProcessInput]:
                def mapping(f: Callable[[ArcTable, int], MaterialAttributeValue]) -> MaterialAttributeValue:
                    return f(table)(i)

                chars: FSharpList[MaterialAttributeValue] = to_list(map_1(mapping, char_getters))
                input: ProcessInput = input_getter(table)(i)
                return of_array([input, ProcessInput_createSample_Z598187B7(ProcessInput__get_Name(input), chars)]) if ((not is_empty(chars)) if (not (True if ProcessInput__isSample(input) else ProcessInput__isSource(input))) else False) else singleton(ProcessInput_setCharacteristicValues(chars, input) if (length(chars) > 0) else input)

            return _arrow1023

        input_getter_1 = _arrow1024

    output_getter_1: Callable[[ArcTable, int], FSharpList[ProcessOutput]]
    def chooser_11(tupled_arg_11: tuple[int, CompositeHeader], process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[ArcTable, int], ProcessOutput] | None:
        return ProcessParsing_tryGetOutputGetter(tupled_arg_11[0], tupled_arg_11[1])

    match_value_1: Callable[[ArcTable, int], ProcessOutput] | None = try_pick(chooser_11, headers_1)
    if match_value_1 is None:
        def _arrow1026(table_3: ArcTable, process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[int], FSharpList[ProcessOutput]]:
            def _arrow1025(i_3: int) -> FSharpList[ProcessOutput]:
                def mapping_3(f_3: Callable[[ArcTable, int], FactorValue]) -> FactorValue:
                    return f_3(table_3)(i_3)

                return singleton(ProcessOutput(0, Sample_create_62424AD2(None, ((("" + process_name_root) + "_Output_") + str(i_3)) + "", None, to_list(map_1(mapping_3, factor_value_getters)))))

            return _arrow1025

        output_getter_1 = _arrow1026

    else: 
        output_getter: Callable[[ArcTable, int], ProcessOutput] = match_value_1
        def _arrow1028(table_2: ArcTable, process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[int], FSharpList[ProcessOutput]]:
            def _arrow1027(i_2: int) -> FSharpList[ProcessOutput]:
                def mapping_2(f_2: Callable[[ArcTable, int], FactorValue]) -> FactorValue:
                    return f_2(table_2)(i_2)

                factors: FSharpList[FactorValue] = to_list(map_1(mapping_2, factor_value_getters))
                output: ProcessOutput = output_getter(table_2)(i_2)
                return of_array([output, ProcessOutput_createSample_Z598187B7(ProcessOutput__get_Name(output), None, factors)]) if ((not is_empty(factors)) if (not ProcessOutput__isSample(output)) else False) else singleton(ProcessOutput_setFactorValues(factors, output) if (length(factors) > 0) else output)

            return _arrow1027

        output_getter_1 = _arrow1028

    def _arrow1030(table_4: ArcTable, process_name_root: Any=process_name_root, headers: Any=headers) -> Callable[[int], Process]:
        def _arrow1029(i_4: int) -> Process:
            def mapping_4(p: str) -> str:
                return Process_composeName(p, i_4)

            pn: str | None = map(mapping_4, Option_fromValueWithDefault("", process_name_root))
            def mapping_5(f_4: Callable[[ArcTable, int], ProcessParameterValue]) -> ProcessParameterValue:
                return f_4(table_4)(i_4)

            paramvalues: FSharpList[ProcessParameterValue] | None = Option_fromValueWithDefault(empty(), map_2(mapping_5, parameter_value_getters))
            def mapping_7(list_6: FSharpList[ProcessParameterValue]) -> FSharpList[ProtocolParameter]:
                def mapping_6(pv: ProcessParameterValue, list_6: Any=list_6) -> ProtocolParameter:
                    return value_10(pv.Category)

                return map_2(mapping_6, list_6)

            parameters: FSharpList[ProtocolParameter] | None = map(mapping_7, paramvalues)
            def mapping_8(f_5: Callable[[ArcTable, int], Comment]) -> Comment:
                return f_5(table_4)(i_4)

            comments: FSharpList[Comment] | None = Option_fromValueWithDefault(empty(), map_2(mapping_8, comment_getters))
            protocol: Protocol | None
            def mapping_9(f_6: Callable[[ArcTable, int], str]) -> str:
                return f_6(table_4)(i_4)

            def mapping_10(f_7: Callable[[ArcTable, int], OntologyAnnotation]) -> OntologyAnnotation:
                return f_7(table_4)(i_4)

            def mapping_11(f_8: Callable[[ArcTable, int], str]) -> str:
                return f_8(table_4)(i_4)

            def mapping_12(f_9: Callable[[ArcTable, int], str]) -> str:
                return f_9(table_4)(i_4)

            def mapping_13(f_10: Callable[[ArcTable, int], str]) -> str:
                return f_10(table_4)(i_4)

            def mapping_14(f_11: Callable[[ArcTable, int], Component]) -> Component:
                return f_11(table_4)(i_4)

            p_1: Protocol = Protocol_make(None, map(mapping_9, protocol_refgetter), map(mapping_10, protocol_type_getter), map(mapping_11, protocol_description_getter), map(mapping_12, protocol_urigetter), map(mapping_13, protocol_version_getter), parameters, Option_fromValueWithDefault(empty(), map_2(mapping_14, component_getters)), None)
            (pattern_matching_result,) = (None,)
            if p_1.Name is None:
                if p_1.ProtocolType is None:
                    if p_1.Description is None:
                        if p_1.Uri is None:
                            if p_1.Version is None:
                                if p_1.Components is None:
                                    pattern_matching_result = 0

                                else: 
                                    pattern_matching_result = 1


                            else: 
                                pattern_matching_result = 1


                        else: 
                            pattern_matching_result = 1


                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1

            if pattern_matching_result == 0:
                protocol = None

            elif pattern_matching_result == 1:
                protocol = p_1

            pattern_input: tuple[FSharpList[ProcessInput], FSharpList[ProcessOutput]]
            inputs: FSharpList[ProcessInput] = input_getter_1(table_4)(i_4)
            outputs: FSharpList[ProcessOutput] = output_getter_1(table_4)(i_4)
            pattern_input = ((of_array([item(0, inputs), item(0, inputs)]), outputs)) if ((length(outputs) == 2) if (length(inputs) == 1) else False) else (((inputs, of_array([item(0, outputs), item(0, outputs)]))) if ((length(outputs) == 1) if (length(inputs) == 2) else False) else ((inputs, outputs)))
            return Process_make(None, pn, protocol, paramvalues, None, None, None, None, pattern_input[0], pattern_input[1], comments)

        return _arrow1029

    return _arrow1030


def ProcessParsing_groupProcesses(ps: FSharpList[Process]) -> FSharpList[tuple[str, FSharpList[Process]]]:
    def projection(x: Process, ps: Any=ps) -> str:
        if (Process_decomposeName_Z721C83C5(value_10(x.Name))[1] is not None) if (x.Name is not None) else False:
            return Process_decomposeName_Z721C83C5(value_10(x.Name))[0]

        elif (value_10(x.ExecutesProtocol).Name is not None) if (x.ExecutesProtocol is not None) else False:
            return value_10(value_10(x.ExecutesProtocol).Name)

        elif x.Name is not None:
            return value_10(x.Name)

        elif (value_10(x.ExecutesProtocol).ID is not None) if (x.ExecutesProtocol is not None) else False:
            return value_10(value_10(x.ExecutesProtocol).ID)

        else: 
            return create_missing_identifier()


    class ObjectExpr1032:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1031(x_1: str, y: str) -> bool:
                return x_1 == y

            return _arrow1031

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return List_groupBy(projection, ps, ObjectExpr1032())


def ProcessParsing_mergeIdenticalProcesses(processes: FSharpList[Process]) -> FSharpList[Process]:
    def projection(x: Process, processes: Any=processes) -> tuple[str, Any, Any | None, Any | None]:
        if (Process_decomposeName_Z721C83C5(value_10(x.Name))[1] is not None) if (x.Name is not None) else False:
            def mapping(a: FSharpList[ProcessParameterValue], x: Any=x) -> Any:
                return box_hash_seq(a)

            def mapping_1(a_1: FSharpList[Comment], x: Any=x) -> Any:
                return box_hash_seq(a_1)

            return (Process_decomposeName_Z721C83C5(value_10(x.Name))[0], box_hash_option(x.ExecutesProtocol), map(mapping, x.ParameterValues), map(mapping_1, x.Comments))

        elif (value_10(x.ExecutesProtocol).Name is not None) if (x.ExecutesProtocol is not None) else False:
            def mapping_2(a_2: FSharpList[ProcessParameterValue], x: Any=x) -> Any:
                return box_hash_seq(a_2)

            def mapping_3(a_3: FSharpList[Comment], x: Any=x) -> Any:
                return box_hash_seq(a_3)

            return (value_10(value_10(x.ExecutesProtocol).Name), box_hash_option(x.ExecutesProtocol), map(mapping_2, x.ParameterValues), map(mapping_3, x.Comments))

        else: 
            def mapping_4(a_4: FSharpList[ProcessParameterValue], x: Any=x) -> Any:
                return box_hash_seq(a_4)

            def mapping_5(a_5: FSharpList[Comment], x: Any=x) -> Any:
                return box_hash_seq(a_5)

            return (create_missing_identifier(), box_hash_option(x.ExecutesProtocol), map(mapping_4, x.ParameterValues), map(mapping_5, x.Comments))


    class ObjectExpr1033:
        @property
        def Equals(self) -> Callable[[tuple[str, Any, Any | None, Any | None], tuple[str, Any, Any | None, Any | None]], bool]:
            return equal_arrays

        @property
        def GetHashCode(self) -> Callable[[tuple[str, Any, Any | None, Any | None]], int]:
            return array_hash

    l: FSharpList[tuple[tuple[str, Any, Any | None, Any | None], FSharpList[Process]]] = List_groupBy(projection, processes, ObjectExpr1033())
    def mapping_8(i: int, tupled_arg: tuple[tuple[str, Any, Any | None, Any | None], FSharpList[Process]], processes: Any=processes) -> Process:
        processes_1: FSharpList[Process] = tupled_arg[1]
        n: str = tupled_arg[0][0]
        p_vs: FSharpList[ProcessParameterValue] | None = item(0, processes_1).ParameterValues
        def mapping_6(p: Process, i: Any=i, tupled_arg: Any=tupled_arg) -> FSharpList[ProcessInput]:
            return default_arg(p.Inputs, empty())

        inputs: FSharpList[ProcessInput] | None = Option_fromValueWithDefault(empty(), collect(mapping_6, processes_1))
        def mapping_7(p_1: Process, i: Any=i, tupled_arg: Any=tupled_arg) -> FSharpList[ProcessOutput]:
            return default_arg(p_1.Outputs, empty())

        outputs: FSharpList[ProcessOutput] | None = Option_fromValueWithDefault(empty(), collect(mapping_7, processes_1))
        return Process_create_Z7C1F7FA9(None, Process_composeName(n, i) if (length(l) > 1) else n, item(0, processes_1).ExecutesProtocol, p_vs, None, None, None, None, inputs, outputs, item(0, processes_1).Comments)

    return map_indexed(mapping_8, l)


def ProcessParsing_processToRows(p: Process) -> FSharpList[FSharpList[tuple[CompositeHeader, CompositeCell]]]:
    def mapping(ppv: ProcessParameterValue, p: Any=p) -> tuple[tuple[CompositeHeader, CompositeCell], int | None]:
        return (JsonTypes_decomposeParameterValue(ppv), try_get_parameter_column_index(ppv))

    pvs: FSharpList[tuple[tuple[CompositeHeader, CompositeCell], int | None]] = map_2(mapping, default_arg(p.ParameterValues, empty()))
    components: FSharpList[tuple[tuple[CompositeHeader, CompositeCell], int | None]]
    match_value: Protocol | None = p.ExecutesProtocol
    def mapping_1(ppv_1: Component, p: Any=p) -> tuple[tuple[CompositeHeader, CompositeCell], int | None]:
        return (JsonTypes_decomposeComponent(ppv_1), try_get_component_index(ppv_1))

    components = empty() if (match_value is None) else map_2(mapping_1, default_arg(match_value.Components, empty()))
    prot_vals: FSharpList[tuple[CompositeHeader, CompositeCell]]
    match_value_1: Protocol | None = p.ExecutesProtocol
    if match_value_1 is None:
        prot_vals = empty()

    else: 
        prot_1: Protocol = match_value_1
        def _arrow1038(__unit: None=None, p: Any=p) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
            def _arrow1037(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                def _arrow1036(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                    def _arrow1035(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                        def _arrow1034(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                            return singleton_1((CompositeHeader(7), CompositeCell(1, value_10(prot_1.Version)))) if (prot_1.Version is not None) else empty_1()

                        return append(singleton_1((CompositeHeader(6), CompositeCell(1, value_10(prot_1.Uri)))) if (prot_1.Uri is not None) else empty_1(), delay(_arrow1034))

                    return append(singleton_1((CompositeHeader(5), CompositeCell(1, value_10(prot_1.Description)))) if (prot_1.Description is not None) else empty_1(), delay(_arrow1035))

                return append(singleton_1((CompositeHeader(4), CompositeCell(0, value_10(prot_1.ProtocolType)))) if (prot_1.ProtocolType is not None) else empty_1(), delay(_arrow1036))

            return append(singleton_1((CompositeHeader(8), CompositeCell(1, value_10(prot_1.Name)))) if (prot_1.Name is not None) else empty_1(), delay(_arrow1037))

        prot_vals = to_list(delay(_arrow1038))

    def mapping_2(c: Comment, p: Any=p) -> tuple[CompositeHeader, CompositeCell]:
        return (CompositeHeader(14, default_arg(c.Name, "")), CompositeCell(1, default_arg(c.Value, "")))

    comments: FSharpList[tuple[CompositeHeader, CompositeCell]] = map_2(mapping_2, default_arg(p.Comments, empty()))
    def mapping_6(tupled_arg_1: tuple[tuple[str, str], FSharpList[tuple[ProcessInput, ProcessOutput]]], p: Any=p) -> FSharpList[tuple[CompositeHeader, CompositeCell]]:
        ios: FSharpList[tuple[ProcessInput, ProcessOutput]] = tupled_arg_1[1]
        def chooser(tupled_arg_2: tuple[ProcessInput, ProcessOutput], tupled_arg_1: Any=tupled_arg_1) -> ProcessInput | None:
            i_2: ProcessInput = tupled_arg_2[0]
            if True if ProcessInput__isSource(i_2) else ProcessInput__isSample(i_2):
                return i_2

            else: 
                return None


        input_for_charas: ProcessInput = default_arg(try_pick_1(chooser, ios), head(ios)[0])
        def chooser_1(tupled_arg_3: tuple[ProcessInput, ProcessOutput], tupled_arg_1: Any=tupled_arg_1) -> ProcessInput | None:
            i_3: ProcessInput = tupled_arg_3[0]
            if True if ProcessInput__isData(i_3) else ProcessInput__isMaterial(i_3):
                return i_3

            else: 
                return None


        input_for_type: ProcessInput = default_arg(try_pick_1(chooser_1, ios), head(ios)[0])
        def mapping_3(cv: MaterialAttributeValue, tupled_arg_1: Any=tupled_arg_1) -> tuple[tuple[CompositeHeader, CompositeCell], int | None]:
            return (JsonTypes_decomposeCharacteristicValue(cv), try_get_characteristic_column_index(cv))

        chars: FSharpList[tuple[tuple[CompositeHeader, CompositeCell], int | None]] = map_2(mapping_3, ProcessInput_getCharacteristicValues_5B3D5BA9(input_for_charas))
        def chooser_2(tupled_arg_4: tuple[ProcessInput, ProcessOutput], tupled_arg_1: Any=tupled_arg_1) -> ProcessOutput | None:
            o_4: ProcessOutput = tupled_arg_4[1]
            if ProcessOutput__isSample(o_4):
                return o_4

            else: 
                return None


        output_for_factors: ProcessOutput = default_arg(try_pick_1(chooser_2, ios), head(ios)[1])
        def chooser_3(tupled_arg_5: tuple[ProcessInput, ProcessOutput], tupled_arg_1: Any=tupled_arg_1) -> ProcessOutput | None:
            o_5: ProcessOutput = tupled_arg_5[1]
            if True if ProcessOutput__isData(o_5) else ProcessOutput__isMaterial(o_5):
                return o_5

            else: 
                return None


        output_for_type: ProcessOutput = default_arg(try_pick_1(chooser_3, ios), head(ios)[1])
        def mapping_5(tuple_5: tuple[tuple[CompositeHeader, CompositeCell], int | None], tupled_arg_1: Any=tupled_arg_1) -> tuple[CompositeHeader, CompositeCell]:
            return tuple_5[0]

        def projection_1(arg: tuple[tuple[CompositeHeader, CompositeCell], int | None], tupled_arg_1: Any=tupled_arg_1) -> int:
            return default_arg(arg[1], 10000)

        def mapping_4(fv: FactorValue, tupled_arg_1: Any=tupled_arg_1) -> tuple[tuple[CompositeHeader, CompositeCell], int | None]:
            return (JsonTypes_decomposeFactorValue(fv), try_get_factor_column_index(fv))

        class ObjectExpr1039:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        vals: FSharpList[tuple[CompositeHeader, CompositeCell]] = map_2(mapping_5, sort_by(projection_1, append_1(chars, append_1(components, append_1(pvs, map_2(mapping_4, ProcessOutput_getFactorValues_Z42C11600(output_for_factors))))), ObjectExpr1039()))
        def _arrow1044(__unit: None=None, tupled_arg_1: Any=tupled_arg_1) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
            def _arrow1043(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                def _arrow1042(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                    def _arrow1041(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                        def _arrow1040(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                            return singleton_1(JsonTypes_decomposeProcessOutput(output_for_type))

                        return append(comments, delay(_arrow1040))

                    return append(vals, delay(_arrow1041))

                return append(prot_vals, delay(_arrow1042))

            return append(singleton_1(JsonTypes_decomposeProcessInput(input_for_type)), delay(_arrow1043))

        return to_list(delay(_arrow1044))

    def projection(tupled_arg: tuple[ProcessInput, ProcessOutput], p: Any=p) -> tuple[str, str]:
        return (ProcessInput__get_Name(tupled_arg[0]), ProcessOutput__get_Name(tupled_arg[1]))

    def _arrow1045(__unit: None=None, p: Any=p) -> FSharpList[tuple[ProcessInput, ProcessOutput]]:
        list_5: FSharpList[ProcessOutput] = default_arg(p.Outputs, empty())
        return zip(default_arg(p.Inputs, empty()), list_5)

    class ObjectExpr1046:
        @property
        def Equals(self) -> Callable[[tuple[str, str], tuple[str, str]], bool]:
            return equal_arrays

        @property
        def GetHashCode(self) -> Callable[[tuple[str, str]], int]:
            return array_hash

    return map_2(mapping_6, List_groupBy(projection, _arrow1045(), ObjectExpr1046()))


def ARCtrl_CompositeHeader__CompositeHeader_TryParameter(this: CompositeHeader) -> ProtocolParameter | None:
    if this.tag == 3:
        return ProtocolParameter.create(None, this.fields[0])

    else: 
        return None



def ARCtrl_CompositeHeader__CompositeHeader_TryFactor(this: CompositeHeader) -> Factor | None:
    if this.tag == 2:
        return Factor.create(None, this.fields[0])

    else: 
        return None



def ARCtrl_CompositeHeader__CompositeHeader_TryCharacteristic(this: CompositeHeader) -> MaterialAttribute | None:
    if this.tag == 1:
        return MaterialAttribute_create_A220A8A(None, this.fields[0])

    else: 
        return None



def ARCtrl_CompositeHeader__CompositeHeader_TryComponent(this: CompositeHeader) -> Component | None:
    if this.tag == 0:
        return Component_create_Z2F0B38C7(None, None, this.fields[0])

    else: 
        return None



def ARCtrl_CompositeCell__CompositeCell_fromValue_Static_Z6986DF18(value: Value_2, unit: OntologyAnnotation | None=None) -> CompositeCell:
    return JsonTypes_cellOfValue(value, unit)


def CompositeRow_toProtocol(table_name: str, row: IEnumerable_1[tuple[CompositeHeader, CompositeCell]]) -> Protocol:
    def folder(p: Protocol, hc: tuple[CompositeHeader, CompositeCell], table_name: Any=table_name, row: Any=row) -> Protocol:
        (pattern_matching_result, oa, v, v_1, v_2, v_3, oa_1, oa_2, unit, v_4, oa_3, t) = (None, None, None, None, None, None, None, None, None, None, None, None)
        if hc[0].tag == 4:
            if hc[1].tag == 0:
                pattern_matching_result = 0
                oa = hc[1].fields[0]

            else: 
                pattern_matching_result = 8


        elif hc[0].tag == 7:
            if hc[1].tag == 1:
                pattern_matching_result = 1
                v = hc[1].fields[0]

            else: 
                pattern_matching_result = 8


        elif hc[0].tag == 6:
            if hc[1].tag == 1:
                pattern_matching_result = 2
                v_1 = hc[1].fields[0]

            else: 
                pattern_matching_result = 8


        elif hc[0].tag == 5:
            if hc[1].tag == 1:
                pattern_matching_result = 3
                v_2 = hc[1].fields[0]

            else: 
                pattern_matching_result = 8


        elif hc[0].tag == 8:
            if hc[1].tag == 1:
                pattern_matching_result = 4
                v_3 = hc[1].fields[0]

            else: 
                pattern_matching_result = 8


        elif hc[0].tag == 3:
            pattern_matching_result = 5
            oa_1 = hc[0].fields[0]

        elif hc[0].tag == 0:
            if hc[1].tag == 2:
                pattern_matching_result = 6
                oa_2 = hc[0].fields[0]
                unit = hc[1].fields[1]
                v_4 = hc[1].fields[0]

            elif hc[1].tag == 0:
                pattern_matching_result = 7
                oa_3 = hc[0].fields[0]
                t = hc[1].fields[0]

            else: 
                pattern_matching_result = 8


        else: 
            pattern_matching_result = 8

        if pattern_matching_result == 0:
            return Protocol_setProtocolType(p, oa)

        elif pattern_matching_result == 1:
            return Protocol_setVersion(p, v)

        elif pattern_matching_result == 2:
            return Protocol_setUri(p, v_1)

        elif pattern_matching_result == 3:
            return Protocol_setDescription(p, v_2)

        elif pattern_matching_result == 4:
            return Protocol_setName(p, v_3)

        elif pattern_matching_result == 5:
            return Protocol_addParameter(ProtocolParameter.create(None, oa_1), p)

        elif pattern_matching_result == 6:
            return Protocol_addComponent(Component_create_Z2F0B38C7(Value_2.from_string(v_4), unit, oa_2), p)

        elif pattern_matching_result == 7:
            return Protocol_addComponent(Component_create_Z2F0B38C7(Value_2(0, t), None, oa_3), p)

        elif pattern_matching_result == 8:
            return p


    return fold(folder, Protocol_create_Z414665E7(None, table_name), row)


def ARCtrl_ArcTable__ArcTable_fromProtocol_Static_3BF20962(p: Protocol) -> ArcTable:
    t: ArcTable = ArcTable.init(default_arg(p.Name, create_missing_identifier()))
    with get_enumerator(default_arg(p.Parameters, empty())) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            pp: ProtocolParameter = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            t.AddColumn(CompositeHeader(3, value_10(pp.ParameterName)), None, ARCtrl_Process_ProtocolParameter__ProtocolParameter_TryGetColumnIndex(pp))
    with get_enumerator(default_arg(p.Components, empty())) as enumerator_1:
        while enumerator_1.System_Collections_IEnumerator_MoveNext():
            c: Component = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
            def mapping(arg: Value_2, p: Any=p) -> Array[CompositeCell]:
                return ResizeArray_singleton(ARCtrl_CompositeCell__CompositeCell_fromValue_Static_Z6986DF18(arg, c.ComponentUnit))

            v_1: Array[CompositeCell] | None = map(mapping, c.ComponentValue)
            t.AddColumn(CompositeHeader(3, value_10(c.ComponentType)), v_1, ARCtrl_Process_Component__Component_TryGetColumnIndex(c))
    def mapping_1(d: str, p: Any=p) -> None:
        t.AddProtocolDescriptionColumn(ResizeArray_singleton(d))

    ignore(map(mapping_1, p.Description))
    def mapping_2(d_1: str, p: Any=p) -> None:
        t.AddProtocolVersionColumn(ResizeArray_singleton(d_1))

    ignore(map(mapping_2, p.Version))
    def mapping_3(d_2: OntologyAnnotation, p: Any=p) -> None:
        t.AddProtocolTypeColumn(ResizeArray_singleton(d_2))

    ignore(map(mapping_3, p.ProtocolType))
    def mapping_4(d_3: str, p: Any=p) -> None:
        t.AddProtocolUriColumn(ResizeArray_singleton(d_3))

    ignore(map(mapping_4, p.Uri))
    def mapping_5(d_4: str, p: Any=p) -> None:
        t.AddProtocolNameColumn(ResizeArray_singleton(d_4))

    ignore(map(mapping_5, p.Name))
    return t


def ARCtrl_ArcTable__ArcTable_GetProtocols(this: ArcTable) -> FSharpList[Protocol]:
    if this.RowCount == 0:
        def _arrow1052(__unit: None=None, this: Any=this) -> Protocol:
            source: Array[CompositeHeader] = this.Headers
            def folder(p: Protocol, h: CompositeHeader) -> Protocol:
                if h.tag == 4:
                    return Protocol_setProtocolType(p, OntologyAnnotation())

                elif h.tag == 7:
                    return Protocol_setVersion(p, "")

                elif h.tag == 6:
                    return Protocol_setUri(p, "")

                elif h.tag == 5:
                    return Protocol_setDescription(p, "")

                elif h.tag == 8:
                    return Protocol_setName(p, "")

                elif h.tag == 3:
                    return Protocol_addParameter(ProtocolParameter.create(None, h.fields[0]), p)

                elif h.tag == 0:
                    return Protocol_addComponent(Component_create_Z2F0B38C7(None, None, h.fields[0]), p)

                else: 
                    return p


            return fold(folder, Protocol_create_Z414665E7(None, this.Name), source)

        return singleton(_arrow1052())

    else: 
        def _arrow1053(i: int, this: Any=this) -> Protocol:
            row: IEnumerable_1[tuple[CompositeHeader, CompositeCell]]
            source_2: Array[CompositeCell] = this.GetRow(i, True)
            row = zip_1(this.Headers, source_2)
            return CompositeRow_toProtocol(this.Name, row)

        class ObjectExpr1054:
            @property
            def Equals(self) -> Callable[[Protocol, Protocol], bool]:
                return equals

            @property
            def GetHashCode(self) -> Callable[[Protocol], int]:
                return safe_hash

        return List_distinct(initialize(this.RowCount, _arrow1053), ObjectExpr1054())



def ARCtrl_ArcTable__ArcTable_GetProcesses(this: ArcTable) -> FSharpList[Process]:
    if this.RowCount == 0:
        return singleton(Process_create_Z7C1F7FA9(None, this.Name))

    else: 
        getter: Callable[[ArcTable, int], Process]
        clo: Callable[[ArcTable, int], Process] = ProcessParsing_getProcessGetter(this.Name, this.Headers)
        def _arrow1056(arg: ArcTable, this: Any=this) -> Callable[[int], Process]:
            clo_1: Callable[[int], Process] = clo(arg)
            return clo_1

        getter = _arrow1056
        def _arrow1058(__unit: None=None, this: Any=this) -> IEnumerable_1[Process]:
            def _arrow1057(i: int) -> Process:
                return getter(this)(i)

            return map_1(_arrow1057, range_big_int(0, 1, this.RowCount - 1))

        return ProcessParsing_mergeIdenticalProcesses(to_list(delay(_arrow1058)))



def ARCtrl_ArcTable__ArcTable_fromProcesses_Static(name: str, ps: FSharpList[Process]) -> ArcTable:
    def mapping(p: Process, name: Any=name, ps: Any=ps) -> FSharpList[FSharpList[tuple[CompositeHeader, CompositeCell]]]:
        return ProcessParsing_processToRows(p)

    tupled_arg: tuple[Array[CompositeHeader], ArcTableValues] = Unchecked_alignByHeaders(True, collect(mapping, ps))
    return ArcTable.from_arc_table_values(name, tupled_arg[0], tupled_arg[1])


def ARCtrl_ArcTables__ArcTables_GetProcesses(this: ArcTables) -> FSharpList[Process]:
    def mapping(t: ArcTable, this: Any=this) -> FSharpList[Process]:
        return ARCtrl_ArcTable__ArcTable_GetProcesses(t)

    return collect(mapping, to_list(this.Tables))


def ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D(ps: FSharpList[Process]) -> ArcTables:
    def mapping_1(tupled_arg: tuple[str, FSharpList[Process]], ps: Any=ps) -> ArcTable:
        def mapping(p: Process, tupled_arg: Any=tupled_arg) -> FSharpList[FSharpList[tuple[CompositeHeader, CompositeCell]]]:
            return ProcessParsing_processToRows(p)

        tupled_arg_1: tuple[Array[CompositeHeader], ArcTableValues] = Unchecked_alignByHeaders(True, collect(mapping, tupled_arg[1]))
        return ArcTable.from_arc_table_values(tupled_arg[0], tupled_arg_1[0], tupled_arg_1[1])

    return ArcTables(list(map_2(mapping_1, ProcessParsing_groupProcesses(ps))))


__all__ = ["Person_orcidKey", "Person_AssayIdentifierPrefix", "Person_createAssayIdentifierKey", "Person_setSourceAssayComment", "Person_getSourceAssayIdentifiersFromComments", "Person_removeSourceAssayComments", "Person_setOrcidFromComments", "Person_setCommentFromORCID", "JsonTypes_valueOfCell", "JsonTypes_composeComponent", "JsonTypes_composeParameterValue", "JsonTypes_composeFactorValue", "JsonTypes_composeCharacteristicValue", "JsonTypes_composeFreetextMaterialName", "JsonTypes_composeProcessInput", "JsonTypes_composeProcessOutput", "JsonTypes_cellOfValue", "JsonTypes_decomposeComponent", "JsonTypes_decomposeParameterValue", "JsonTypes_decomposeFactorValue", "JsonTypes_decomposeCharacteristicValue", "JsonTypes_decomposeProcessInput", "JsonTypes_decomposeProcessOutput", "JsonTypes_composeTechnologyPlatform", "JsonTypes_decomposeTechnologyPlatform", "ProcessParsing_tryComponentGetter", "ProcessParsing_tryParameterGetter", "ProcessParsing_tryFactorGetter", "ProcessParsing_tryCharacteristicGetter", "ProcessParsing_tryGetProtocolTypeGetter", "ProcessParsing_tryGetProtocolREFGetter", "ProcessParsing_tryGetProtocolDescriptionGetter", "ProcessParsing_tryGetProtocolURIGetter", "ProcessParsing_tryGetProtocolVersionGetter", "ProcessParsing_tryGetInputGetter", "ProcessParsing_tryGetOutputGetter", "ProcessParsing_tryGetCommentGetter", "ProcessParsing_getProcessGetter", "ProcessParsing_groupProcesses", "ProcessParsing_mergeIdenticalProcesses", "ProcessParsing_processToRows", "ARCtrl_CompositeHeader__CompositeHeader_TryParameter", "ARCtrl_CompositeHeader__CompositeHeader_TryFactor", "ARCtrl_CompositeHeader__CompositeHeader_TryCharacteristic", "ARCtrl_CompositeHeader__CompositeHeader_TryComponent", "ARCtrl_CompositeCell__CompositeCell_fromValue_Static_Z6986DF18", "CompositeRow_toProtocol", "ARCtrl_ArcTable__ArcTable_fromProtocol_Static_3BF20962", "ARCtrl_ArcTable__ArcTable_GetProtocols", "ARCtrl_ArcTable__ArcTable_GetProcesses", "ARCtrl_ArcTable__ArcTable_fromProcesses_Static", "ARCtrl_ArcTables__ArcTables_GetProcesses", "ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D"]

