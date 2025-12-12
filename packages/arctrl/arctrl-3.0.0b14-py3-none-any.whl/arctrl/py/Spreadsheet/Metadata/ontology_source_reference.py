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
from ...Core.Helper.collections_ import ResizeArray_iter
from ...Core.ontology_source_reference import OntologySourceReference
from .comment import (Comment_fromString, Comment_toString)
from .sparse_table import (SparseTable_GetEmptyComments_3ECCA699, SparseTable__TryGetValueDefault_5BAE6133, SparseTable__TryGetValue_11FD62A8, SparseTable, SparseTable_Create_Z2192E64B, SparseTable_FromRows_Z5579EC29, SparseTable_ToRows_759CAFC1)

name_label: str = "Term Source Name"

file_label: str = "Term Source File"

version_label: str = "Term Source Version"

description_label: str = "Term Source Description"

labels: FSharpList[str] = of_array([name_label, file_label, version_label, description_label])

def from_string(description: str | None, file: str | None, name: str | None, version: str | None, comments: Array[Comment]) -> OntologySourceReference:
    return OntologySourceReference.make(description, file, name, version, comments)


def from_sparse_table(matrix: SparseTable) -> FSharpList[OntologySourceReference]:
    if (length(matrix.CommentKeys) != 0) if (matrix.ColumnCount == 0) else False:
        comments: Array[Comment] = SparseTable_GetEmptyComments_3ECCA699(matrix)
        def _arrow1442(__unit: None=None, matrix: Any=matrix) -> OntologySourceReference:
            return_val: OntologySourceReference = OntologySourceReference.create()
            return_val.Comments = comments
            return return_val

        return singleton(_arrow1442())

    else: 
        def _arrow1443(i: int, matrix: Any=matrix) -> OntologySourceReference:
            def mapping(k: str) -> Comment:
                return Comment_fromString(k, SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (k, i)))

            comments_1: Array[Comment] = list(map(mapping, matrix.CommentKeys))
            return from_string(SparseTable__TryGetValue_11FD62A8(matrix, (description_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (file_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (name_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (version_label, i)), comments_1)

        return initialize(matrix.ColumnCount, _arrow1443)



def to_sparse_table(ontology_sources: FSharpList[OntologySourceReference]) -> SparseTable:
    matrix: SparseTable = SparseTable_Create_Z2192E64B(None, labels, None, length(ontology_sources) + 1)
    comment_keys: FSharpList[str] = empty()
    def action(i: int, o: OntologySourceReference, ontology_sources: Any=ontology_sources) -> None:
        i_1: int = (i + 1) or 0
        add_to_dict(matrix.Matrix, (name_label, i_1), default_arg(o.Name, ""))
        add_to_dict(matrix.Matrix, (file_label, i_1), default_arg(o.File, ""))
        add_to_dict(matrix.Matrix, (version_label, i_1), default_arg(o.Version, ""))
        add_to_dict(matrix.Matrix, (description_label, i_1), default_arg(o.Description, ""))
        def f(comment: Comment, i: Any=i, o: Any=o) -> None:
            nonlocal comment_keys
            pattern_input: tuple[str, str] = Comment_toString(comment)
            n: str = pattern_input[0]
            comment_keys = cons(n, comment_keys)
            add_to_dict(matrix.Matrix, (n, i_1), pattern_input[1])

        ResizeArray_iter(f, o.Comments)

    iterate_indexed(action, ontology_sources)
    class ObjectExpr1445:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1444(x: str, y: str) -> bool:
                return x == y

            return _arrow1444

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return SparseTable(matrix.Matrix, matrix.Keys, reverse(List_distinct(comment_keys, ObjectExpr1445())), matrix.ColumnCount)


def from_rows(line_number: int, rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, int, FSharpList[Remark], FSharpList[OntologySourceReference]]:
    tupled_arg: tuple[str | None, int, FSharpList[Remark], SparseTable] = SparseTable_FromRows_Z5579EC29(rows, labels, line_number)
    return (tupled_arg[0], tupled_arg[1], tupled_arg[2], from_sparse_table(tupled_arg[3]))


def to_rows(term_sources: FSharpList[OntologySourceReference]) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    return SparseTable_ToRows_759CAFC1(to_sparse_table(term_sources))


__all__ = ["name_label", "file_label", "version_label", "description_label", "labels", "from_string", "from_sparse_table", "to_sparse_table", "from_rows", "to_rows"]

