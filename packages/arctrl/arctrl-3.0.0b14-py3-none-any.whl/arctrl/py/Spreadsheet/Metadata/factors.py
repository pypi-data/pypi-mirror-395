from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (of_array, FSharpList, length, singleton, initialize, map, empty, iterate_indexed, cons, reverse)
from ...fable_modules.fable_library.map_util import add_to_dict
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.seq2 import List_distinct
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (string_hash, IEnumerable_1, IEnumerator)
from ...Core.comment import (Comment, Remark)
from ...Core.Helper.collections_ import (Option_fromValueWithDefault, ResizeArray_iter)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Process.factor import Factor
from .comment import (Comment_fromString, Comment_toString)
from .sparse_table import (SparseTable_GetEmptyComments_3ECCA699, SparseTable__TryGetValueDefault_5BAE6133, SparseTable__TryGetValue_11FD62A8, SparseTable, SparseTable_Create_Z2192E64B, SparseTable_FromRows_Z5579EC29, SparseTable_ToRows_759CAFC1)

name_label: str = "Name"

factor_type_label: str = "Type"

type_term_accession_number_label: str = "Type Term Accession Number"

type_term_source_reflabel: str = "Type Term Source REF"

labels: FSharpList[str] = of_array([name_label, factor_type_label, type_term_accession_number_label, type_term_source_reflabel])

def from_string(name: str | None, design_type: str | None, type_term_source_ref: str | None, type_term_accession_number: str | None, comments: Array[Comment]) -> Factor:
    factor_type: OntologyAnnotation = OntologyAnnotation.create(design_type, type_term_source_ref, type_term_accession_number)
    factor_type_1: OntologyAnnotation | None = Option_fromValueWithDefault(OntologyAnnotation(), factor_type)
    comments_1: Array[Comment] | None = Option_fromValueWithDefault([], comments)
    return Factor.make(name, factor_type_1, comments_1)


def from_sparse_table(matrix: SparseTable) -> FSharpList[Factor]:
    if (length(matrix.CommentKeys) != 0) if (matrix.ColumnCount == 0) else False:
        comments: Array[Comment] = SparseTable_GetEmptyComments_3ECCA699(matrix)
        return singleton(Factor.create(None, None, comments))

    else: 
        def _arrow1080(i: int, matrix: Any=matrix) -> Factor:
            def mapping(k: str) -> Comment:
                return Comment_fromString(k, SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (k, i)))

            comments_1: Array[Comment] = list(map(mapping, matrix.CommentKeys))
            return from_string(SparseTable__TryGetValue_11FD62A8(matrix, (name_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (factor_type_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (type_term_source_reflabel, i)), SparseTable__TryGetValue_11FD62A8(matrix, (type_term_accession_number_label, i)), comments_1)

        return initialize(matrix.ColumnCount, _arrow1080)



def to_sparse_table(factors: FSharpList[Factor]) -> SparseTable:
    matrix: SparseTable = SparseTable_Create_Z2192E64B(None, labels, None, length(factors) + 1)
    comment_keys: FSharpList[str] = empty()
    def action(i: int, f: Factor, factors: Any=factors) -> None:
        i_1: int = (i + 1) or 0
        ft: dict[str, Any]
        f_1: OntologyAnnotation = default_arg(f.FactorType, OntologyAnnotation())
        ft = OntologyAnnotation.to_string_object(f_1, True)
        add_to_dict(matrix.Matrix, (name_label, i_1), default_arg(f.Name, ""))
        add_to_dict(matrix.Matrix, (factor_type_label, i_1), ft["TermName"])
        add_to_dict(matrix.Matrix, (type_term_accession_number_label, i_1), ft["TermAccessionNumber"])
        add_to_dict(matrix.Matrix, (type_term_source_reflabel, i_1), ft["TermSourceREF"])
        match_value: Array[Comment] | None = f.Comments
        if match_value is not None:
            def f_2(comment: Comment, i: Any=i, f: Any=f) -> None:
                nonlocal comment_keys
                pattern_input: tuple[str, str] = Comment_toString(comment)
                n: str = pattern_input[0]
                comment_keys = cons(n, comment_keys)
                add_to_dict(matrix.Matrix, (n, i_1), pattern_input[1])

            ResizeArray_iter(f_2, match_value)


    iterate_indexed(action, factors)
    class ObjectExpr1082:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1081(x: str, y: str) -> bool:
                return x == y

            return _arrow1081

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return SparseTable(matrix.Matrix, matrix.Keys, reverse(List_distinct(comment_keys, ObjectExpr1082())), matrix.ColumnCount)


def from_rows(prefix: str | None, line_number: int, rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, int, FSharpList[Remark], FSharpList[Factor]]:
    tupled_arg: tuple[str | None, int, FSharpList[Remark], SparseTable] = SparseTable_FromRows_Z5579EC29(rows, labels, line_number) if (prefix is None) else SparseTable_FromRows_Z5579EC29(rows, labels, line_number, prefix)
    return (tupled_arg[0], tupled_arg[1], tupled_arg[2], from_sparse_table(tupled_arg[3]))


def to_rows(prefix: str | None, factors: FSharpList[Factor]) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    m: SparseTable = to_sparse_table(factors)
    if prefix is None:
        return SparseTable_ToRows_759CAFC1(m)

    else: 
        return SparseTable_ToRows_759CAFC1(m, prefix)



__all__ = ["name_label", "factor_type_label", "type_term_accession_number_label", "type_term_source_reflabel", "labels", "from_string", "from_sparse_table", "to_sparse_table", "from_rows", "to_rows"]

