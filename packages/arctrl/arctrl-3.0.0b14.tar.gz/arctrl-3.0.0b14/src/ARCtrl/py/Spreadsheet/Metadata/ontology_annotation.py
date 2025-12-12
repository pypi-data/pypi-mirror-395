from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (length, singleton, initialize, map, FSharpList, of_array, empty, iterate_indexed, cons, reverse)
from ...fable_modules.fable_library.map_util import add_to_dict
from ...fable_modules.fable_library.seq2 import List_distinct
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (string_hash, IEnumerable_1, IEnumerator)
from ...Core.comment import (Comment, Remark)
from ...Core.Helper.collections_ import ResizeArray_iter
from ...Core.ontology_annotation import OntologyAnnotation
from .comment import (Comment_fromString, Comment_toString)
from .sparse_table import (SparseTable_GetEmptyComments_3ECCA699, SparseTable__TryGetValueDefault_5BAE6133, SparseTable__TryGetValue_11FD62A8, SparseTable, SparseTable_Create_Z2192E64B, SparseTable_FromRows_Z5579EC29, SparseTable_ToRows_759CAFC1)

def from_sparse_table(label: str, label_tsr: str, label_tan: str, matrix: SparseTable) -> FSharpList[OntologyAnnotation]:
    if (length(matrix.CommentKeys) != 0) if (matrix.ColumnCount == 0) else False:
        comments: Array[Comment] = SparseTable_GetEmptyComments_3ECCA699(matrix)
        def _arrow1055(__unit: None=None, label: Any=label, label_tsr: Any=label_tsr, label_tan: Any=label_tan, matrix: Any=matrix) -> OntologyAnnotation:
            return_val: OntologyAnnotation = OntologyAnnotation.create()
            return_val.Comments = comments
            return return_val

        return singleton(_arrow1055())

    else: 
        def _arrow1059(i: int, label: Any=label, label_tsr: Any=label_tsr, label_tan: Any=label_tan, matrix: Any=matrix) -> OntologyAnnotation:
            def mapping(k: str) -> Comment:
                return Comment_fromString(k, SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (k, i)))

            comments_1: Array[Comment] = list(map(mapping, matrix.CommentKeys))
            return OntologyAnnotation(SparseTable__TryGetValue_11FD62A8(matrix, (label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (label_tsr, i)), SparseTable__TryGetValue_11FD62A8(matrix, (label_tan, i)), comments_1)

        return initialize(matrix.ColumnCount, _arrow1059)



def to_sparse_table(label: str, label_tsr: str, label_tan: str, designs: FSharpList[OntologyAnnotation]) -> SparseTable:
    matrix: SparseTable = SparseTable_Create_Z2192E64B(None, of_array([label, label_tan, label_tsr]), None, length(designs) + 1)
    comment_keys: FSharpList[str] = empty()
    def action(i: int, d: OntologyAnnotation, label: Any=label, label_tsr: Any=label_tsr, label_tan: Any=label_tan, designs: Any=designs) -> None:
        i_1: int = (i + 1) or 0
        oa: dict[str, Any] = OntologyAnnotation.to_string_object(d, True)
        add_to_dict(matrix.Matrix, (label, i_1), oa["TermName"])
        add_to_dict(matrix.Matrix, (label_tan, i_1), oa["TermAccessionNumber"])
        add_to_dict(matrix.Matrix, (label_tsr, i_1), oa["TermSourceREF"])
        def f(comment: Comment, i: Any=i, d: Any=d) -> None:
            nonlocal comment_keys
            pattern_input: tuple[str, str] = Comment_toString(comment)
            n: str = pattern_input[0]
            comment_keys = cons(n, comment_keys)
            add_to_dict(matrix.Matrix, (n, i_1), pattern_input[1])

        ResizeArray_iter(f, d.Comments)

    iterate_indexed(action, designs)
    class ObjectExpr1065:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1064(x: str, y: str) -> bool:
                return x == y

            return _arrow1064

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return SparseTable(matrix.Matrix, matrix.Keys, reverse(List_distinct(comment_keys, ObjectExpr1065())), matrix.ColumnCount)


def from_rows(prefix: str | None, label: str, label_tsr: str, label_tan: str, line_number: int, rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, int, FSharpList[Remark], FSharpList[OntologyAnnotation]]:
    labels: FSharpList[str] = of_array([label, label_tan, label_tsr])
    tupled_arg: tuple[str | None, int, FSharpList[Remark], SparseTable] = SparseTable_FromRows_Z5579EC29(rows, labels, line_number) if (prefix is None) else SparseTable_FromRows_Z5579EC29(rows, labels, line_number, prefix)
    return (tupled_arg[0], tupled_arg[1], tupled_arg[2], from_sparse_table(label, label_tsr, label_tan, tupled_arg[3]))


def to_rows(prefix: str | None, label: str, label_tsr: str, label_tan: str, designs: FSharpList[OntologyAnnotation]) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    m: SparseTable = to_sparse_table(label, label_tsr, label_tan, designs)
    if prefix is None:
        return SparseTable_ToRows_759CAFC1(m)

    else: 
        return SparseTable_ToRows_759CAFC1(m, prefix)



__all__ = ["from_sparse_table", "to_sparse_table", "from_rows", "to_rows"]

