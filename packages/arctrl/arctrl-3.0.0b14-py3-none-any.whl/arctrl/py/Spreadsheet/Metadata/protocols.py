from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (of_array, FSharpList, of_seq, empty, length, singleton, initialize, map as map_1, iterate_indexed, iterate, cons, reverse)
from ...fable_modules.fable_library.map_util import add_to_dict
from ...fable_modules.fable_library.option import (map, default_arg)
from ...fable_modules.fable_library.seq2 import List_distinct
from ...fable_modules.fable_library.util import (string_hash, IEnumerable_1, IEnumerator)
from ...Core.comment import (Comment, Remark)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Process.component import Component
from ...Core.Process.protocol import (Protocol_make, Protocol, Protocol_create_Z414665E7)
from ...Core.Process.protocol_parameter import ProtocolParameter
from ...Core.uri import URIModule_fromString
from .comment import (Comment_fromString, Comment_toString)
from .conversions import (ProtocolParameter_fromAggregatedStrings, Component_fromAggregatedStrings, Option_fromValueWithDefault, ProtocolParameter_toAggregatedStrings, Component_toAggregatedStrings)
from .sparse_table import (SparseTable_GetEmptyComments_3ECCA699, SparseTable__TryGetValueDefault_5BAE6133, SparseTable__TryGetValue_11FD62A8, SparseTable, SparseTable_Create_Z2192E64B, SparseTable_FromRows_Z5579EC29, SparseTable_ToRows_759CAFC1)

name_label: str = "Name"

protocol_type_label: str = "Type"

type_term_accession_number_label: str = "Type Term Accession Number"

type_term_source_reflabel: str = "Type Term Source REF"

description_label: str = "Description"

uri_label: str = "URI"

version_label: str = "Version"

parameters_name_label: str = "Parameters Name"

parameters_term_accession_number_label: str = "Parameters Term Accession Number"

parameters_term_source_reflabel: str = "Parameters Term Source REF"

components_name_label: str = "Components Name"

components_type_label: str = "Components Type"

components_type_term_accession_number_label: str = "Components Type Term Accession Number"

components_type_term_source_reflabel: str = "Components Type Term Source REF"

labels: FSharpList[str] = of_array([name_label, protocol_type_label, type_term_accession_number_label, type_term_source_reflabel, description_label, uri_label, version_label, parameters_name_label, parameters_term_accession_number_label, parameters_term_source_reflabel, components_name_label, components_type_label, components_type_term_accession_number_label, components_type_term_source_reflabel])

def from_string(name: str | None, protocol_type: str | None, type_term_accession_number: str | None, type_term_source_ref: str | None, description: str | None, uri: str | None, version: str | None, parameters_name: str, parameters_term_accession_number: str, parameters_term_source_ref: str, components_name: str, components_type: str, components_type_term_accession_number: str, components_type_term_source_ref: str, comments: FSharpList[Comment]) -> Protocol:
    protocol_type_1: OntologyAnnotation = OntologyAnnotation.create(protocol_type, type_term_source_ref, type_term_accession_number)
    parameters: FSharpList[ProtocolParameter] = of_seq(ProtocolParameter_fromAggregatedStrings(";", parameters_name, parameters_term_source_ref, parameters_term_accession_number))
    components: FSharpList[Component] = Component_fromAggregatedStrings(";", components_name, components_type, components_type_term_source_ref, components_type_term_accession_number)
    def _arrow1091(s: str, name: Any=name, protocol_type: Any=protocol_type, type_term_accession_number: Any=type_term_accession_number, type_term_source_ref: Any=type_term_source_ref, description: Any=description, uri: Any=uri, version: Any=version, parameters_name: Any=parameters_name, parameters_term_accession_number: Any=parameters_term_accession_number, parameters_term_source_ref: Any=parameters_term_source_ref, components_name: Any=components_name, components_type: Any=components_type, components_type_term_accession_number: Any=components_type_term_accession_number, components_type_term_source_ref: Any=components_type_term_source_ref, comments: Any=comments) -> str:
        return URIModule_fromString(s)

    def _arrow1093(s_1: str, name: Any=name, protocol_type: Any=protocol_type, type_term_accession_number: Any=type_term_accession_number, type_term_source_ref: Any=type_term_source_ref, description: Any=description, uri: Any=uri, version: Any=version, parameters_name: Any=parameters_name, parameters_term_accession_number: Any=parameters_term_accession_number, parameters_term_source_ref: Any=parameters_term_source_ref, components_name: Any=components_name, components_type: Any=components_type, components_type_term_accession_number: Any=components_type_term_accession_number, components_type_term_source_ref: Any=components_type_term_source_ref, comments: Any=comments) -> str:
        return URIModule_fromString(s_1)

    return Protocol_make(None, map(_arrow1091, name), Option_fromValueWithDefault(OntologyAnnotation(), protocol_type_1), description, map(_arrow1093, uri), version, Option_fromValueWithDefault(empty(), parameters), Option_fromValueWithDefault(empty(), components), Option_fromValueWithDefault(empty(), comments))


def from_sparse_table(matrix: SparseTable) -> FSharpList[Protocol]:
    if (length(matrix.CommentKeys) != 0) if (matrix.ColumnCount == 0) else False:
        return singleton(Protocol_create_Z414665E7(None, None, None, None, None, None, None, None, of_seq(SparseTable_GetEmptyComments_3ECCA699(matrix))))

    else: 
        def _arrow1098(i: int, matrix: Any=matrix) -> Protocol:
            def mapping(k: str) -> Comment:
                return Comment_fromString(k, SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (k, i)))

            comments_1: FSharpList[Comment] = map_1(mapping, matrix.CommentKeys)
            return from_string(SparseTable__TryGetValue_11FD62A8(matrix, (name_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (protocol_type_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (type_term_accession_number_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (type_term_source_reflabel, i)), SparseTable__TryGetValue_11FD62A8(matrix, (description_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (uri_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (version_label, i)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (parameters_name_label, i)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (parameters_term_accession_number_label, i)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (parameters_term_source_reflabel, i)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (components_name_label, i)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (components_type_label, i)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (components_type_term_accession_number_label, i)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (components_type_term_source_reflabel, i)), comments_1)

        return initialize(matrix.ColumnCount, _arrow1098)



def to_sparse_table(protocols: FSharpList[Protocol]) -> SparseTable:
    matrix: SparseTable = SparseTable_Create_Z2192E64B(None, labels, None, length(protocols) + 1)
    comment_keys: FSharpList[str] = empty()
    def action_1(i: int, p: Protocol, protocols: Any=protocols) -> None:
        i_1: int = (i + 1) or 0
        pt_1: dict[str, Any]
        pt: OntologyAnnotation = default_arg(p.ProtocolType, OntologyAnnotation())
        pt_1 = OntologyAnnotation.to_string_object(pt, True)
        p_agg: dict[str, Any] = ProtocolParameter_toAggregatedStrings(";", default_arg(p.Parameters, empty()))
        c_agg: dict[str, Any] = Component_toAggregatedStrings(";", default_arg(p.Components, empty()))
        add_to_dict(matrix.Matrix, (name_label, i_1), default_arg(p.Name, ""))
        add_to_dict(matrix.Matrix, (protocol_type_label, i_1), pt_1["TermName"])
        add_to_dict(matrix.Matrix, (type_term_accession_number_label, i_1), pt_1["TermAccessionNumber"])
        add_to_dict(matrix.Matrix, (type_term_source_reflabel, i_1), pt_1["TermSourceREF"])
        add_to_dict(matrix.Matrix, (description_label, i_1), default_arg(p.Description, ""))
        add_to_dict(matrix.Matrix, (uri_label, i_1), default_arg(p.Uri, ""))
        add_to_dict(matrix.Matrix, (version_label, i_1), default_arg(p.Version, ""))
        add_to_dict(matrix.Matrix, (parameters_name_label, i_1), p_agg["TermNameAgg"])
        add_to_dict(matrix.Matrix, (parameters_term_accession_number_label, i_1), p_agg["TermAccessionNumberAgg"])
        add_to_dict(matrix.Matrix, (parameters_term_source_reflabel, i_1), p_agg["TermSourceREFAgg"])
        add_to_dict(matrix.Matrix, (components_name_label, i_1), c_agg["NameAgg"])
        add_to_dict(matrix.Matrix, (components_type_label, i_1), c_agg["TermNameAgg"])
        add_to_dict(matrix.Matrix, (components_type_term_accession_number_label, i_1), c_agg["TermAccessionNumberAgg"])
        add_to_dict(matrix.Matrix, (components_type_term_source_reflabel, i_1), c_agg["TermSourceREFAgg"])
        match_value: FSharpList[Comment] | None = p.Comments
        if match_value is not None:
            def action(comment: Comment, i: Any=i, p: Any=p) -> None:
                nonlocal comment_keys
                pattern_input: tuple[str, str] = Comment_toString(comment)
                n: str = pattern_input[0]
                comment_keys = cons(n, comment_keys)
                add_to_dict(matrix.Matrix, (n, i_1), pattern_input[1])

            iterate(action, match_value)


    iterate_indexed(action_1, protocols)
    class ObjectExpr1103:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1102(x: str, y: str) -> bool:
                return x == y

            return _arrow1102

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return SparseTable(matrix.Matrix, matrix.Keys, reverse(List_distinct(comment_keys, ObjectExpr1103())), matrix.ColumnCount)


def from_rows(prefix: str | None, line_number: int, rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, int, FSharpList[Remark], FSharpList[Protocol]]:
    tupled_arg: tuple[str | None, int, FSharpList[Remark], SparseTable] = SparseTable_FromRows_Z5579EC29(rows, labels, line_number) if (prefix is None) else SparseTable_FromRows_Z5579EC29(rows, labels, line_number, prefix)
    return (tupled_arg[0], tupled_arg[1], tupled_arg[2], from_sparse_table(tupled_arg[3]))


def to_rows(prefix: str | None, protocols: FSharpList[Protocol]) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    m: SparseTable = to_sparse_table(protocols)
    if prefix is None:
        return SparseTable_ToRows_759CAFC1(m)

    else: 
        return SparseTable_ToRows_759CAFC1(m, prefix)



__all__ = ["name_label", "protocol_type_label", "type_term_accession_number_label", "type_term_source_reflabel", "description_label", "uri_label", "version_label", "parameters_name_label", "parameters_term_accession_number_label", "parameters_term_source_reflabel", "components_name_label", "components_type_label", "components_type_term_accession_number_label", "components_type_term_source_reflabel", "labels", "from_string", "from_sparse_table", "to_sparse_table", "from_rows", "to_rows"]

