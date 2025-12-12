from __future__ import annotations
from typing import Any
from .Core.comment import Comment
from .Core.comment_list import try_item
from .Core.ontology_annotation import OntologyAnnotation
from .Core.Process.component import (Component, Component_fromISAString_7C9A7CF8)
from .Core.Process.factor import Factor
from .Core.Process.factor_value import FactorValue
from .Core.Process.material_attribute import (MaterialAttribute, MaterialAttribute_fromString_5980DC03)
from .Core.Process.material_attribute_value import MaterialAttributeValue
from .Core.Process.process_parameter_value import ProcessParameterValue
from .Core.Process.protocol_parameter import ProtocolParameter
from .fable_modules.fable_library.int32 import try_parse
from .fable_modules.fable_library.option import (bind, value)
from .fable_modules.fable_library.seq import find_index
from .fable_modules.fable_library.types import (FSharpRef, Array)
from .fable_modules.fable_library.util import (int32_to_string, equals)

def try_int(str_1: str) -> int | None:
    match_value: tuple[bool, int]
    out_arg: int = 0
    def _arrow3779(__unit: None=None, str_1: Any=str_1) -> int:
        return out_arg

    def _arrow3780(v: int, str_1: Any=str_1) -> None:
        nonlocal out_arg
        out_arg = v or 0

    match_value = (try_parse(str_1, 511, False, 32, FSharpRef(_arrow3779, _arrow3780)), out_arg)
    if match_value[0]:
        return match_value[1]

    else: 
        return None



order_name: str = "ColumnIndex"

def create_order_comment(index: int) -> Comment:
    return Comment.create(order_name, int32_to_string(index))


def try_get_index(comments: Array[Comment]) -> int | None:
    match_value: str | None = try_item(order_name, comments)
    if match_value is not None:
        ci: str = match_value
        def predicate(c: Comment, comments: Any=comments) -> bool:
            return equals(c.Name, order_name)

        i: int = find_index(predicate, comments) or 0
        comments.pop(i)
        return try_int(ci)

    else: 
        return None



def set_ontology_annotation_index_inplace(i: int, oa: OntologyAnnotation) -> None:
    (oa.Comments.append(create_order_comment(i)))


def set_ontology_annotation_index(i: int, oa: OntologyAnnotation) -> OntologyAnnotation:
    oac: OntologyAnnotation = oa.Copy()
    set_ontology_annotation_index_inplace(i, oac)
    return oac


def try_get_ontology_annotation_index(oa: OntologyAnnotation) -> int | None:
    return try_get_index(oa.Comments)


def try_get_parameter_index(param: ProtocolParameter) -> int | None:
    def binder(oa: OntologyAnnotation, param: Any=param) -> int | None:
        return try_get_index(oa.Comments)

    return bind(binder, param.ParameterName)


def try_get_parameter_column_index(param_value: ProcessParameterValue) -> int | None:
    def _arrow3781(param: ProtocolParameter, param_value: Any=param_value) -> int | None:
        return try_get_parameter_index(param)

    return bind(_arrow3781, param_value.Category)


def try_get_factor_index(factor: Factor) -> int | None:
    def binder(oa: OntologyAnnotation, factor: Any=factor) -> int | None:
        return try_get_index(oa.Comments)

    return bind(binder, factor.FactorType)


def try_get_factor_column_index(factor_value: FactorValue) -> int | None:
    def _arrow3782(factor: Factor, factor_value: Any=factor_value) -> int | None:
        return try_get_factor_index(factor)

    return bind(_arrow3782, factor_value.Category)


def try_get_characteristic_index(characteristic: MaterialAttribute) -> int | None:
    def binder(oa: OntologyAnnotation, characteristic: Any=characteristic) -> int | None:
        return try_get_index(oa.Comments)

    return bind(binder, characteristic.CharacteristicType)


def try_get_characteristic_column_index(characteristic_value: MaterialAttributeValue) -> int | None:
    def _arrow3783(characteristic: MaterialAttribute, characteristic_value: Any=characteristic_value) -> int | None:
        return try_get_characteristic_index(characteristic)

    return bind(_arrow3783, characteristic_value.Category)


def try_get_component_index(comp: Component) -> int | None:
    def binder(oa: OntologyAnnotation, comp: Any=comp) -> int | None:
        return try_get_index(oa.Comments)

    return bind(binder, comp.ComponentType)


def ARCtrl_OntologyAnnotation__OntologyAnnotation_fromStringWithColumnIndex_Static(name: str, term: str, source: str, accession: str, value_index: int) -> Factor:
    return Factor.from_string(name, term, source, accession, [create_order_comment(value_index)])


def ARCtrl_OntologyAnnotation__OntologyAnnotation_getColumnIndex_Static_ZDED3A0F(f: OntologyAnnotation) -> int:
    return value(try_get_ontology_annotation_index(f))


def ARCtrl_OntologyAnnotation__OntologyAnnotation_GetColumnIndex(this: OntologyAnnotation) -> int:
    return value(try_get_ontology_annotation_index(this))


def ARCtrl_OntologyAnnotation__OntologyAnnotation_tryGetColumnIndex_Static_ZDED3A0F(f: OntologyAnnotation) -> int | None:
    return try_get_ontology_annotation_index(f)


def ARCtrl_OntologyAnnotation__OntologyAnnotation_TryGetColumnIndex(this: OntologyAnnotation) -> int | None:
    return try_get_ontology_annotation_index(this)


def ARCtrl_OntologyAnnotation__OntologyAnnotation_setColumnIndex_Static(i: int, oa: OntologyAnnotation) -> OntologyAnnotation:
    return set_ontology_annotation_index(i, oa)


def ARCtrl_OntologyAnnotation__OntologyAnnotation_SetColumnIndex_Z524259A4(this: OntologyAnnotation, i: int) -> None:
    set_ontology_annotation_index_inplace(i, this)


def ARCtrl_Process_Factor__Factor_fromStringWithColumnIndex_Static(name: str, term: str, source: str, accession: str, value_index: int) -> Factor:
    return Factor.from_string(name, term, source, accession, [create_order_comment(value_index)])


def ARCtrl_Process_Factor__Factor_getColumnIndex_Static_7206F0D9(f: Factor) -> int:
    return value(try_get_factor_index(f))


def ARCtrl_Process_Factor__Factor_GetColumnIndex(this: Factor) -> int:
    return value(try_get_factor_index(this))


def ARCtrl_Process_Factor__Factor_tryGetColumnIndex_Static_7206F0D9(f: Factor) -> int | None:
    return try_get_factor_index(f)


def ARCtrl_Process_Factor__Factor_TryGetColumnIndex(this: Factor) -> int | None:
    return try_get_factor_index(this)


def ARCtrl_Process_FactorValue__FactorValue_getColumnIndex_Static_7105C732(f: FactorValue) -> int:
    return value(try_get_factor_column_index(f))


def ARCtrl_Process_FactorValue__FactorValue_GetColumnIndex(this: FactorValue) -> int:
    return value(try_get_factor_column_index(this))


def ARCtrl_Process_FactorValue__FactorValue_tryGetColumnIndex_Static_7105C732(f: FactorValue) -> int | None:
    return try_get_factor_column_index(f)


def ARCtrl_Process_FactorValue__FactorValue_TryGetColumnIndex(this: FactorValue) -> int | None:
    return try_get_factor_column_index(this)


def ARCtrl_Process_MaterialAttribute__MaterialAttribute_fromStringWithColumnIndex_Static(term: str, source: str, accession: str, value_index: int) -> MaterialAttribute:
    return MaterialAttribute_fromString_5980DC03(term, source, accession, [create_order_comment(value_index)])


def ARCtrl_Process_MaterialAttribute__MaterialAttribute_getColumnIndex_Static_Z1E3B85DD(m: MaterialAttribute) -> int:
    return value(try_get_characteristic_index(m))


def ARCtrl_Process_MaterialAttribute__MaterialAttribute_GetColumnIndex(this: MaterialAttribute) -> int:
    return value(try_get_characteristic_index(this))


def ARCtrl_Process_MaterialAttribute__MaterialAttribute_tryGetColumnIndex_Static_Z1E3B85DD(m: MaterialAttribute) -> int | None:
    return try_get_characteristic_index(m)


def ARCtrl_Process_MaterialAttribute__MaterialAttribute_TryGetColumnIndex(this: MaterialAttribute) -> int | None:
    return try_get_characteristic_index(this)


def ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_getColumnIndex_Static_Z772273B8(m: MaterialAttributeValue) -> int:
    return value(try_get_characteristic_column_index(m))


def ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_GetColumnIndex(this: MaterialAttributeValue) -> int:
    return value(try_get_characteristic_column_index(this))


def ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_tryGetColumnIndex_Static_Z772273B8(m: MaterialAttributeValue) -> int | None:
    return try_get_characteristic_column_index(m)


def ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_TryGetColumnIndex(this: MaterialAttributeValue) -> int | None:
    return try_get_characteristic_column_index(this)


def ARCtrl_Process_ProtocolParameter__ProtocolParameter_fromStringWithColumnIndex_Static(term: str, source: str, accession: str, value_index: int) -> ProtocolParameter:
    return ProtocolParameter.from_string(term, source, accession, [create_order_comment(value_index)])


def ARCtrl_Process_ProtocolParameter__ProtocolParameter_getColumnIndex_Static_Z11F87B15(p: ProtocolParameter) -> int:
    return value(try_get_parameter_index(p))


def ARCtrl_Process_ProtocolParameter__ProtocolParameter_GetColumnIndex(this: ProtocolParameter) -> int:
    return value(try_get_parameter_index(this))


def ARCtrl_Process_ProtocolParameter__ProtocolParameter_tryGetColumnIndex_Static_Z11F87B15(p: ProtocolParameter) -> int | None:
    return try_get_parameter_index(p)


def ARCtrl_Process_ProtocolParameter__ProtocolParameter_TryGetColumnIndex(this: ProtocolParameter) -> int | None:
    return try_get_parameter_index(this)


def ARCtrl_Process_ProcessParameterValue__ProcessParameterValue_getColumnIndex_Static_Z1576263(p: ProcessParameterValue) -> int:
    return value(try_get_parameter_column_index(p))


def ARCtrl_Process_ProcessParameterValue__ProcessParameterValue_GetColumnIndex(this: ProcessParameterValue) -> int:
    return value(try_get_parameter_column_index(this))


def ARCtrl_Process_ProcessParameterValue__ProcessParameterValue_tryGetColumnIndex_Static_Z1576263(p: ProcessParameterValue) -> int | None:
    return try_get_parameter_column_index(p)


def ARCtrl_Process_ProcessParameterValue__ProcessParameterValue_TryGetColumnIndex(this: ProcessParameterValue) -> int | None:
    return try_get_parameter_column_index(this)


def ARCtrl_Process_Component__Component_fromStringWithColumnIndex_Static(name: str, term: str, source: str, accession: str, value_index: int) -> Component:
    return Component_fromISAString_7C9A7CF8(name, term, source, accession, [create_order_comment(value_index)])


def ARCtrl_Process_Component__Component_getColumnIndex_Static_Z685B8F25(f: Component) -> int:
    return value(try_get_component_index(f))


def ARCtrl_Process_Component__Component_GetColumnIndex(this: Component) -> int:
    return value(try_get_component_index(this))


def ARCtrl_Process_Component__Component_tryGetColumnIndex_Static_Z685B8F25(f: Component) -> int | None:
    return try_get_component_index(f)


def ARCtrl_Process_Component__Component_TryGetColumnIndex(this: Component) -> int | None:
    return try_get_component_index(this)


__all__ = ["try_int", "order_name", "create_order_comment", "try_get_index", "set_ontology_annotation_index_inplace", "set_ontology_annotation_index", "try_get_ontology_annotation_index", "try_get_parameter_index", "try_get_parameter_column_index", "try_get_factor_index", "try_get_factor_column_index", "try_get_characteristic_index", "try_get_characteristic_column_index", "try_get_component_index", "ARCtrl_OntologyAnnotation__OntologyAnnotation_fromStringWithColumnIndex_Static", "ARCtrl_OntologyAnnotation__OntologyAnnotation_getColumnIndex_Static_ZDED3A0F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_GetColumnIndex", "ARCtrl_OntologyAnnotation__OntologyAnnotation_tryGetColumnIndex_Static_ZDED3A0F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_TryGetColumnIndex", "ARCtrl_OntologyAnnotation__OntologyAnnotation_setColumnIndex_Static", "ARCtrl_OntologyAnnotation__OntologyAnnotation_SetColumnIndex_Z524259A4", "ARCtrl_Process_Factor__Factor_fromStringWithColumnIndex_Static", "ARCtrl_Process_Factor__Factor_getColumnIndex_Static_7206F0D9", "ARCtrl_Process_Factor__Factor_GetColumnIndex", "ARCtrl_Process_Factor__Factor_tryGetColumnIndex_Static_7206F0D9", "ARCtrl_Process_Factor__Factor_TryGetColumnIndex", "ARCtrl_Process_FactorValue__FactorValue_getColumnIndex_Static_7105C732", "ARCtrl_Process_FactorValue__FactorValue_GetColumnIndex", "ARCtrl_Process_FactorValue__FactorValue_tryGetColumnIndex_Static_7105C732", "ARCtrl_Process_FactorValue__FactorValue_TryGetColumnIndex", "ARCtrl_Process_MaterialAttribute__MaterialAttribute_fromStringWithColumnIndex_Static", "ARCtrl_Process_MaterialAttribute__MaterialAttribute_getColumnIndex_Static_Z1E3B85DD", "ARCtrl_Process_MaterialAttribute__MaterialAttribute_GetColumnIndex", "ARCtrl_Process_MaterialAttribute__MaterialAttribute_tryGetColumnIndex_Static_Z1E3B85DD", "ARCtrl_Process_MaterialAttribute__MaterialAttribute_TryGetColumnIndex", "ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_getColumnIndex_Static_Z772273B8", "ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_GetColumnIndex", "ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_tryGetColumnIndex_Static_Z772273B8", "ARCtrl_Process_MaterialAttributeValue__MaterialAttributeValue_TryGetColumnIndex", "ARCtrl_Process_ProtocolParameter__ProtocolParameter_fromStringWithColumnIndex_Static", "ARCtrl_Process_ProtocolParameter__ProtocolParameter_getColumnIndex_Static_Z11F87B15", "ARCtrl_Process_ProtocolParameter__ProtocolParameter_GetColumnIndex", "ARCtrl_Process_ProtocolParameter__ProtocolParameter_tryGetColumnIndex_Static_Z11F87B15", "ARCtrl_Process_ProtocolParameter__ProtocolParameter_TryGetColumnIndex", "ARCtrl_Process_ProcessParameterValue__ProcessParameterValue_getColumnIndex_Static_Z1576263", "ARCtrl_Process_ProcessParameterValue__ProcessParameterValue_GetColumnIndex", "ARCtrl_Process_ProcessParameterValue__ProcessParameterValue_tryGetColumnIndex_Static_Z1576263", "ARCtrl_Process_ProcessParameterValue__ProcessParameterValue_TryGetColumnIndex", "ARCtrl_Process_Component__Component_fromStringWithColumnIndex_Static", "ARCtrl_Process_Component__Component_getColumnIndex_Static_Z685B8F25", "ARCtrl_Process_Component__Component_GetColumnIndex", "ARCtrl_Process_Component__Component_tryGetColumnIndex_Static_Z685B8F25", "ARCtrl_Process_Component__Component_TryGetColumnIndex"]

