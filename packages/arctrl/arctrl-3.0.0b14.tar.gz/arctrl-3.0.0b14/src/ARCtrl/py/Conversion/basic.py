from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Core.comment import Comment
from ..Core.data import Data
from ..Core.data_context import (DataContext__get_Explication, DataContext__get_Unit, DataContext__get_ObjectType, DataContext__get_GeneratedBy, DataContext__get_Description, DataContext__get_Label, DataContext, DataContext__ctor_Z780A8A2A)
from ..Core.data_file import (DataFile__get_AsString, DataFile, DataFile_fromString_Z721C83C5)
from ..Core.Helper.collections_ import (Option_fromValueWithDefault, Option_fromSeq, ResizeArray_map)
from ..Core.Helper.regex import ActivePatterns__007CRegex_007C__007C
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.Table.composite_cell import CompositeCell
from ..Core.Table.composite_header import (CompositeHeader, IOType)
from ..Core.value import Value as Value_1
from ..FileSystem.file_system import FileSystem
from ..FileSystem.file_system_tree import FileSystemTree
from ..FileSystem.path import combine
from ..ROCrate.ldcontext import LDContext
from ..ROCrate.ldobject import (LDNode, LDRef, LDGraph)
from ..ROCrate.LDTypes.comment import LDComment
from ..ROCrate.LDTypes.dataset import LDDataset
from ..ROCrate.LDTypes.defined_term import LDDefinedTerm
from ..ROCrate.LDTypes.file import LDFile
from ..ROCrate.LDTypes.property_value import LDPropertyValue
from ..ROCrate.LDTypes.sample import LDSample
from ..fable_modules.fable_library.array_ import map as map_1
from ..fable_modules.fable_library.option import (map, default_arg, bind)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.reg_exp import (get_item, groups)
from ..fable_modules.fable_library.string_ import (to_fail, printf)
from ..fable_modules.fable_library.types import (Array, to_string)

def _expr3875() -> TypeInfo:
    return class_type("ARCtrl.Conversion.BaseTypes", None, BaseTypes)


class BaseTypes:
    ...

BaseTypes_reflection = _expr3875

def BaseTypes_composeComment_Z13201A7E(comment: Comment) -> LDNode:
    name: str
    match_value: str | None = comment.Name
    if match_value is None:
        raise Exception("Comment must have a name")

    else: 
        name = match_value

    return LDComment.create(name, None, comment.Value)


def BaseTypes_decomposeComment_Z2F770004(comment: LDNode, context: LDContext | None=None) -> Comment:
    return Comment(LDComment.get_name_as_string(comment, context), LDComment.try_get_text_as_string(comment, context))


def BaseTypes_ontologyTermFromNameAndID_40457300(name: str | None=None, id: str | None=None) -> OntologyAnnotation:
    if id is None:
        return OntologyAnnotation.create(name)

    else: 
        t: str = id
        return OntologyAnnotation.from_term_annotation(t, name)



def BaseTypes_tryOntologyTermFromNameAndID_40457300(name: str | None=None, id: str | None=None) -> OntologyAnnotation | None:
    if (id is None) if (name is None) else False:
        return None

    else: 
        return BaseTypes_ontologyTermFromNameAndID_40457300(name, id)



def BaseTypes_composeDefinedTerm_ZDED3A0F(term: OntologyAnnotation) -> LDNode:
    tan: str | None = Option_fromValueWithDefault("", term.TermAccessionAndOntobeeUrlIfShort)
    return LDDefinedTerm.create(term.NameText, None, tan)


def BaseTypes_decomposeDefinedTerm_Z2F770004(term: LDNode, context: LDContext | None=None) -> OntologyAnnotation:
    return BaseTypes_ontologyTermFromNameAndID_40457300(LDDefinedTerm.get_name_as_string(term, context), LDDefinedTerm.try_get_term_code_as_string(term, context))


def BaseTypes_composePropertyValueFromOA_ZDED3A0F(term: OntologyAnnotation) -> LDNode:
    tan: str | None = Option_fromValueWithDefault("", term.TermAccessionAndOntobeeUrlIfShort)
    return LDPropertyValue.create(term.NameText, None, None, tan)


def BaseTypes_decomposePropertyValueToOA_Z2F770004(term: LDNode, context: LDContext | None=None) -> OntologyAnnotation:
    return BaseTypes_ontologyTermFromNameAndID_40457300(LDPropertyValue.get_name_as_string(term, context), LDPropertyValue.try_get_property_idas_string(term, context))


def BaseTypes_valuesOfCell_Z436420FE(value: CompositeCell) -> tuple[str | None, str | None, str | None, str | None]:
    if value.tag == 0:
        if value.fields[0].is_empty():
            return (None, None, None, None)

        elif value.fields[0].TANInfo is not None:
            return (value.fields[0].Name, value.fields[0].TermAccessionAndOntobeeUrlIfShort, None, None)

        else: 
            return (value.fields[0].Name, None, None, None)


    elif value.tag == 2:
        pattern_input: tuple[str | None, str | None] = ((None, None)) if value.fields[1].is_empty() else ((value.fields[1].Name, Option_fromValueWithDefault("", value.fields[1].TermAccessionAndOntobeeUrlIfShort)))
        return (Option_fromValueWithDefault("", value.fields[0]), None, pattern_input[0], pattern_input[1])

    elif value.tag == 3:
        raise Exception("Data cell should not be parsed to isa value")

    elif value.fields[0] == "":
        return (None, None, None, None)

    else: 
        return (value.fields[0], None, None, None)



def BaseTypes_termOfHeader_6CAF647B(header: CompositeHeader) -> tuple[str, str | None]:
    (pattern_matching_result, oa) = (None, None)
    if header.tag == 0:
        pattern_matching_result = 0
        oa = header.fields[0]

    elif header.tag == 3:
        pattern_matching_result = 0
        oa = header.fields[0]

    elif header.tag == 2:
        pattern_matching_result = 0
        oa = header.fields[0]

    elif header.tag == 1:
        pattern_matching_result = 0
        oa = header.fields[0]

    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        return (oa.NameText, oa.TermAccessionAndOntobeeUrlIfShort if (oa.TANInfo is not None) else None)

    elif pattern_matching_result == 1:
        return to_fail(printf("header %O should not be parsed to isa value"))(header)



def BaseTypes_composeComponent(header: CompositeHeader, value: CompositeCell) -> LDNode:
    pattern_input: tuple[str | None, str | None, str | None, str | None] = BaseTypes_valuesOfCell_Z436420FE(value)
    pattern_input_1: tuple[str, str | None] = BaseTypes_termOfHeader_6CAF647B(header)
    return LDPropertyValue.create_component(pattern_input_1[0], pattern_input[0], None, pattern_input_1[1], pattern_input[3], pattern_input[2], pattern_input[1])


def BaseTypes_composeParameterValue(header: CompositeHeader, value: CompositeCell) -> LDNode:
    pattern_input: tuple[str | None, str | None, str | None, str | None] = BaseTypes_valuesOfCell_Z436420FE(value)
    pattern_input_1: tuple[str, str | None] = BaseTypes_termOfHeader_6CAF647B(header)
    return LDPropertyValue.create_parameter_value(pattern_input_1[0], pattern_input[0], None, pattern_input_1[1], pattern_input[3], pattern_input[2], pattern_input[1])


def BaseTypes_composeFactorValue(header: CompositeHeader, value: CompositeCell) -> LDNode:
    pattern_input: tuple[str | None, str | None, str | None, str | None] = BaseTypes_valuesOfCell_Z436420FE(value)
    pattern_input_1: tuple[str, str | None] = BaseTypes_termOfHeader_6CAF647B(header)
    return LDPropertyValue.create_factor_value(pattern_input_1[0], pattern_input[0], None, pattern_input_1[1], pattern_input[3], pattern_input[2], pattern_input[1])


def BaseTypes_composeCharacteristicValue(header: CompositeHeader, value: CompositeCell) -> LDNode:
    pattern_input: tuple[str | None, str | None, str | None, str | None] = BaseTypes_valuesOfCell_Z436420FE(value)
    pattern_input_1: tuple[str, str | None] = BaseTypes_termOfHeader_6CAF647B(header)
    return LDPropertyValue.create_characteristic_value(pattern_input_1[0], pattern_input[0], None, pattern_input_1[1], pattern_input[3], pattern_input[2], pattern_input[1])


def BaseTypes_composeFreetextMaterialName(header_ft: str, name: str) -> str:
    return ((("" + header_ft) + "=") + name) + ""


def BaseTypes_composeFile_6CE21C7D(d: Data, fs: FileSystem | None=None) -> LDNode:
    def create_file(__unit: None=None, d: Any=d, fs: Any=fs) -> LDNode:
        data_type: str | None = map(DataFile__get_AsString, d.DataType)
        return LDFile.create(d.NameText, d.NameText, None, data_type, d.Format, d.SelectorFormat)

    if fs is None:
        return create_file(None)

    else: 
        fs_1: FileSystem = fs
        match_value: FileSystemTree | None = fs_1.Tree.TryGetPath(d.NameText)
        if match_value is not None:
            if match_value.tag == 1:
                fs_2: FileSystemTree = match_value
                file: LDNode = create_file(None)
                file.SchemaType = [LDFile.schema_type(), LDDataset.schema_type()]
                def mapping_1(fp: str, d: Any=d, fs: Any=fs) -> LDNode:
                    full_path: str = combine(d.NameText, fp)
                    return LDFile.create(full_path, full_path)

                sub_files: Array[LDNode] = list(map_1(mapping_1, fs_2.ToFilePaths(True), None))
                LDDataset.set_has_parts(file, sub_files)
                return file

            else: 
                return create_file(None)


        else: 
            return create_file(None)




def BaseTypes_decomposeFile_Z2F770004(f: LDNode, context: LDContext | None=None) -> Data:
    def mapping(dt: str, f: Any=f, context: Any=context) -> DataFile:
        return DataFile_fromString_Z721C83C5(dt)

    data_type: DataFile | None = map(mapping, LDFile.try_get_disambiguating_description_as_string(f, context))
    format: str | None = LDFile.try_get_encoding_format_as_string(f, context)
    selector_format: str | None = LDFile.try_get_usage_info_as_string(f, context)
    return Data(None, LDFile.get_name_as_string(f, context), data_type, format, selector_format)


def BaseTypes_composeFragmentDescriptor_Z4C0BEF62(dc: DataContext) -> LDNode:
    if dc.Name is None:
        raise Exception("RO-Crate parsing of DataContext failed: Cannot create a fragment descriptor without a name.")

    id: str = LDPropertyValue.gen_id_fragment_descriptor(dc.NameText)
    def mapping(e: OntologyAnnotation, dc: Any=dc) -> tuple[str | None, str | None]:
        return (e.Name, Option_fromValueWithDefault("", e.TermAccessionAndOntobeeUrlIfShort))

    pattern_input: tuple[str | None, str | None] = default_arg(map(mapping, DataContext__get_Explication(dc)), (None, None))
    def mapping_1(u: OntologyAnnotation, dc: Any=dc) -> tuple[str | None, str | None]:
        return (u.Name, Option_fromValueWithDefault("", u.TermAccessionAndOntobeeUrlIfShort))

    pattern_input_1: tuple[str | None, str | None] = default_arg(map(mapping_1, DataContext__get_Unit(dc)), (None, None))
    def f(c: Comment, dc: Any=dc) -> str:
        return to_string(c)

    disambiguating_descriptions: Array[str] | None = Option_fromSeq(ResizeArray_map(f, dc.Comments))
    data_fragment: LDNode = BaseTypes_composeFile_6CE21C7D(dc)
    def mapping_2(term: OntologyAnnotation, dc: Any=dc) -> LDNode:
        return BaseTypes_composeDefinedTerm_ZDED3A0F(term)

    pattern: LDNode | None = map(mapping_2, DataContext__get_ObjectType(dc))
    data_fragment.SetProperty(LDFile.about(), LDRef(id))
    data_fragment.SetOptionalProperty(LDFile.pattern(), pattern)
    return LDPropertyValue.create_fragment_descriptor(dc.NameText, pattern_input[0], None, pattern_input_1[1], pattern_input_1[0], pattern_input[1], DataContext__get_GeneratedBy(dc), DataContext__get_Description(dc), DataContext__get_Label(dc), disambiguating_descriptions, data_fragment)


def BaseTypes_decomposeFragmentDescriptor_Z6839B9E8(fd: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> DataContext:
    file: LDNode | None = LDPropertyValue.try_get_subject_of(fd, graph, context)
    name: str
    if file is None:
        raise Exception("RO-Crate parsing of DataContext failed: Cannot decompose a fragment descriptor without a name.")

    else: 
        f: LDNode = file
        name = LDFile.get_name_as_string(f, context)

    def mapping(pa: LDNode, fd: Any=fd, graph: Any=graph, context: Any=context) -> OntologyAnnotation:
        return BaseTypes_decomposeDefinedTerm_Z2F770004(pa, context)

    def binder(f_1: LDNode, fd: Any=fd, graph: Any=graph, context: Any=context) -> LDNode | None:
        return LDFile.try_get_pattern_as_defined_term(f_1, graph, context)

    object_type: OntologyAnnotation | None = map(mapping, bind(binder, file))
    def binder_1(f_2: LDNode, fd: Any=fd, graph: Any=graph, context: Any=context) -> str | None:
        return LDFile.try_get_encoding_format_as_string(f_2, context)

    format: str | None = bind(binder_1, file)
    def binder_2(f_3: LDNode, fd: Any=fd, graph: Any=graph, context: Any=context) -> str | None:
        return LDFile.try_get_usage_info_as_string(f_3, context)

    selector_format: str | None = bind(binder_2, file)
    explication: OntologyAnnotation | None = BaseTypes_tryOntologyTermFromNameAndID_40457300(LDPropertyValue.try_get_value_as_string(fd), LDPropertyValue.try_get_value_reference_as_string(fd))
    unit: OntologyAnnotation | None = BaseTypes_tryOntologyTermFromNameAndID_40457300(LDPropertyValue.try_get_unit_text_as_string(fd), LDPropertyValue.try_get_unit_code_as_string(fd))
    generated_by: str | None = LDPropertyValue.try_get_measurement_method_as_string(fd)
    description: str | None = LDPropertyValue.try_get_description_as_string(fd)
    def f_4(s: str, fd: Any=fd, graph: Any=graph, context: Any=context) -> Comment:
        return Comment.from_string(s)

    return DataContext__ctor_Z780A8A2A(None, name, None, format, selector_format, explication, unit, object_type, LDPropertyValue.try_get_alternate_name_as_string(fd), description, generated_by, ResizeArray_map(f_4, LDPropertyValue.get_disambiguating_descriptions_as_string(fd)))


def BaseTypes_composeProcessInput(header: CompositeHeader, value: CompositeCell, fs: FileSystem | None=None) -> LDNode:
    if header.tag == 11:
        if header.fields[0].tag == 1:
            return LDSample.create_sample(value.AsFreeText)

        elif header.fields[0].tag == 3:
            return LDSample.create_material(value.AsFreeText)

        elif header.fields[0].tag == 2:
            if value.tag == 1:
                ft: str = value.fields[0]
                return LDFile.create(ft, ft)

            elif value.tag == 3:
                return BaseTypes_composeFile_6CE21C7D(value.fields[0], fs)

            else: 
                return to_fail(printf("Could not parse input data %O"))(value)


        elif header.fields[0].tag == 4:
            n: LDNode = LDNode(BaseTypes_composeFreetextMaterialName(header.fields[0].fields[0], value.AsFreeText), [header.fields[0].fields[0]])
            n.SetProperty(LDSample.name(), value.AsFreeText)
            return n

        else: 
            return LDSample.create_source(value.AsFreeText)


    else: 
        return to_fail(printf("Could not parse input header %O"))(header)



def BaseTypes_composeProcessOutput(header: CompositeHeader, value: CompositeCell, fs: FileSystem | None=None) -> LDNode:
    (pattern_matching_result, ft_1) = (None, None)
    if header.tag == 12:
        if header.fields[0].tag == 1:
            pattern_matching_result = 0

        elif header.fields[0].tag == 3:
            pattern_matching_result = 1

        elif header.fields[0].tag == 2:
            pattern_matching_result = 2

        elif header.fields[0].tag == 4:
            pattern_matching_result = 3
            ft_1 = header.fields[0].fields[0]

        else: 
            pattern_matching_result = 0


    else: 
        pattern_matching_result = 4

    if pattern_matching_result == 0:
        return LDSample.create_sample(value.AsFreeText)

    elif pattern_matching_result == 1:
        return LDSample.create_material(value.AsFreeText)

    elif pattern_matching_result == 2:
        if value.tag == 1:
            ft: str = value.fields[0]
            return LDFile.create(ft, ft)

        elif value.tag == 3:
            return BaseTypes_composeFile_6CE21C7D(value.fields[0], fs)

        else: 
            return to_fail(printf("Could not parse output data %O"))(value)


    elif pattern_matching_result == 3:
        n: LDNode = LDNode(BaseTypes_composeFreetextMaterialName(ft_1, value.AsFreeText), [ft_1])
        n.SetProperty(LDSample.name(), value.AsFreeText)
        return n

    elif pattern_matching_result == 4:
        return to_fail(printf("Could not parse output header %O"))(header)



def BaseTypes_headerOntologyOfPropertyValue_Z2F770004(pv: LDNode, context: LDContext | None=None) -> OntologyAnnotation:
    n: str = LDPropertyValue.get_name_as_string(pv, context)
    match_value: str | None = LDPropertyValue.try_get_property_idas_string(pv, context)
    if match_value is None:
        return OntologyAnnotation(n)

    else: 
        n_ref: str = match_value
        return OntologyAnnotation.from_term_annotation(n_ref, n)



def BaseTypes_cellOfPropertyValue_Z2F770004(pv: LDNode, context: LDContext | None=None) -> CompositeCell:
    v: str | None = LDPropertyValue.try_get_value_as_string(pv, context)
    v_ref: str | None = LDPropertyValue.try_get_value_reference_as_string(pv, context)
    u: str | None = LDPropertyValue.try_get_unit_text_as_string(pv, context)
    u_ref: str | None = LDPropertyValue.try_get_unit_code_as_string(pv, context)
    (pattern_matching_result, vr, u_1, u_ref_1) = (None, None, None, None)
    if v_ref is None:
        if u is None:
            if u_ref is None:
                pattern_matching_result = 3

            else: 
                pattern_matching_result = 2
                u_ref_1 = u_ref


        elif u_ref is not None:
            pattern_matching_result = 2
            u_ref_1 = u_ref

        else: 
            pattern_matching_result = 1
            u_1 = u


    elif u is None:
        if u_ref is None:
            pattern_matching_result = 0
            vr = v_ref

        else: 
            pattern_matching_result = 4


    else: 
        pattern_matching_result = 4

    if pattern_matching_result == 0:
        return CompositeCell(0, OntologyAnnotation.from_term_annotation(vr, v))

    elif pattern_matching_result == 1:
        return CompositeCell(2, default_arg(v, ""), OntologyAnnotation(u_1))

    elif pattern_matching_result == 2:
        return CompositeCell(2, default_arg(v, ""), OntologyAnnotation.from_term_annotation(u_ref_1, u))

    elif pattern_matching_result == 3:
        return CompositeCell(0, OntologyAnnotation(v))

    elif pattern_matching_result == 4:
        arg: str = default_arg(v, "")
        return to_fail(printf("Could not parse value %s with unit %O and unit reference %O"))(arg)(u)(u_ref)



def BaseTypes_decomposePropertyValue_Z2F770004(pv: LDNode, context: LDContext | None=None) -> tuple[OntologyAnnotation, Value_1 | None, OntologyAnnotation | None]:
    def _arrow3876(__unit: None=None, pv: Any=pv, context: Any=context) -> Value_1 | None:
        v: str | None = LDPropertyValue.try_get_value_as_string(pv, context)
        v_ref: str | None = LDPropertyValue.try_get_value_reference_as_string(pv, context)
        if v_ref is None:
            return None if (v is None) else Value_1(3, v)

        else: 
            vr: str = v_ref
            return Value_1(0, OntologyAnnotation.from_term_annotation(vr, v))


    def _arrow3877(__unit: None=None, pv: Any=pv, context: Any=context) -> OntologyAnnotation | None:
        u: str | None = LDPropertyValue.try_get_unit_text_as_string(pv, context)
        u_ref: str | None = LDPropertyValue.try_get_unit_code_as_string(pv, context)
        (pattern_matching_result, u_1, u_ref_1) = (None, None, None)
        if u is None:
            if u_ref is None:
                pattern_matching_result = 2

            else: 
                pattern_matching_result = 1
                u_ref_1 = u_ref


        elif u_ref is not None:
            pattern_matching_result = 1
            u_ref_1 = u_ref

        else: 
            pattern_matching_result = 0
            u_1 = u

        if pattern_matching_result == 0:
            return OntologyAnnotation(u_1)

        elif pattern_matching_result == 1:
            return OntologyAnnotation.from_term_annotation(u_ref_1, u)

        elif pattern_matching_result == 2:
            return None


    return (BaseTypes_headerOntologyOfPropertyValue_Z2F770004(pv, context), _arrow3876(), _arrow3877())


def BaseTypes_decomposeComponent_Z2F770004(c: LDNode, context: LDContext | None=None) -> tuple[CompositeHeader, CompositeCell]:
    return (CompositeHeader(0, BaseTypes_headerOntologyOfPropertyValue_Z2F770004(c, context)), BaseTypes_cellOfPropertyValue_Z2F770004(c, context))


def BaseTypes_decomposeParameterValue_Z2F770004(c: LDNode, context: LDContext | None=None) -> tuple[CompositeHeader, CompositeCell]:
    return (CompositeHeader(3, BaseTypes_headerOntologyOfPropertyValue_Z2F770004(c, context)), BaseTypes_cellOfPropertyValue_Z2F770004(c, context))


def BaseTypes_decomposeFactorValue_Z2F770004(c: LDNode, context: LDContext | None=None) -> tuple[CompositeHeader, CompositeCell]:
    return (CompositeHeader(2, BaseTypes_headerOntologyOfPropertyValue_Z2F770004(c, context)), BaseTypes_cellOfPropertyValue_Z2F770004(c, context))


def BaseTypes_decomposeCharacteristicValue_Z2F770004(c: LDNode, context: LDContext | None=None) -> tuple[CompositeHeader, CompositeCell]:
    return (CompositeHeader(1, BaseTypes_headerOntologyOfPropertyValue_Z2F770004(c, context)), BaseTypes_cellOfPropertyValue_Z2F770004(c, context))


def BaseTypes_decomposeProcessInput_Z2F770004(pn: LDNode, context: LDContext | None=None) -> tuple[CompositeHeader, CompositeCell]:
    if LDSample.validate_source(pn, context):
        return (CompositeHeader(11, IOType(0)), CompositeCell(1, LDSample.get_name_as_string(pn, context)))

    elif LDSample.validate_material(pn, context):
        return (CompositeHeader(11, IOType(3)), CompositeCell(1, LDSample.get_name_as_string(pn, context)))

    elif LDSample.validate(pn, context):
        return (CompositeHeader(11, IOType(1)), CompositeCell(1, LDSample.get_name_as_string(pn, context)))

    elif LDFile.validate(pn, context):
        return (CompositeHeader(11, IOType(2)), CompositeCell(3, BaseTypes_decomposeFile_Z2F770004(pn, context)))

    else: 
        n: LDNode = pn
        return (CompositeHeader(11, IOType(4, n.SchemaType[0])), CompositeCell(1, LDSample.get_name_as_string(n, context)))



def BaseTypes_decomposeProcessOutput_Z2F770004(pn: LDNode, context: LDContext | None=None) -> tuple[CompositeHeader, CompositeCell]:
    if LDSample.validate_material(pn, context):
        return (CompositeHeader(12, IOType(3)), CompositeCell(1, LDSample.get_name_as_string(pn, context)))

    elif LDSample.validate(pn, context):
        return (CompositeHeader(12, IOType(1)), CompositeCell(1, LDSample.get_name_as_string(pn, context)))

    elif LDFile.validate(pn, context):
        return (CompositeHeader(12, IOType(2)), CompositeCell(3, BaseTypes_decomposeFile_Z2F770004(pn, context)))

    else: 
        n: LDNode = pn
        return (CompositeHeader(12, IOType(4, n.SchemaType[0])), CompositeCell(1, LDSample.get_name_as_string(n, context)))



def BaseTypes_composeTechnologyPlatform_ZDED3A0F(tp: OntologyAnnotation) -> str:
    match_value: dict[str, Any] | None = tp.TANInfo
    if match_value is None:
        return ("" + tp.NameText) + ""

    else: 
        return ((("" + tp.NameText) + " (") + tp.TermAccessionShort) + ")"



def BaseTypes_decomposeTechnologyPlatform_Z721C83C5(name: str) -> OntologyAnnotation:
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



__all__ = ["BaseTypes_reflection", "BaseTypes_composeComment_Z13201A7E", "BaseTypes_decomposeComment_Z2F770004", "BaseTypes_ontologyTermFromNameAndID_40457300", "BaseTypes_tryOntologyTermFromNameAndID_40457300", "BaseTypes_composeDefinedTerm_ZDED3A0F", "BaseTypes_decomposeDefinedTerm_Z2F770004", "BaseTypes_composePropertyValueFromOA_ZDED3A0F", "BaseTypes_decomposePropertyValueToOA_Z2F770004", "BaseTypes_valuesOfCell_Z436420FE", "BaseTypes_termOfHeader_6CAF647B", "BaseTypes_composeComponent", "BaseTypes_composeParameterValue", "BaseTypes_composeFactorValue", "BaseTypes_composeCharacteristicValue", "BaseTypes_composeFreetextMaterialName", "BaseTypes_composeFile_6CE21C7D", "BaseTypes_decomposeFile_Z2F770004", "BaseTypes_composeFragmentDescriptor_Z4C0BEF62", "BaseTypes_decomposeFragmentDescriptor_Z6839B9E8", "BaseTypes_composeProcessInput", "BaseTypes_composeProcessOutput", "BaseTypes_headerOntologyOfPropertyValue_Z2F770004", "BaseTypes_cellOfPropertyValue_Z2F770004", "BaseTypes_decomposePropertyValue_Z2F770004", "BaseTypes_decomposeComponent_Z2F770004", "BaseTypes_decomposeParameterValue_Z2F770004", "BaseTypes_decomposeFactorValue_Z2F770004", "BaseTypes_decomposeCharacteristicValue_Z2F770004", "BaseTypes_decomposeProcessInput_Z2F770004", "BaseTypes_decomposeProcessOutput_Z2F770004", "BaseTypes_composeTechnologyPlatform_ZDED3A0F", "BaseTypes_decomposeTechnologyPlatform_Z721C83C5"]

