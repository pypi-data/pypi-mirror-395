from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (of_array, FSharpList, length, singleton, initialize, map as map_1, empty, iterate_indexed, cons, reverse)
from ...fable_modules.fable_library.map_util import add_to_dict
from ...fable_modules.fable_library.option import (map, default_arg)
from ...fable_modules.fable_library.seq2 import List_distinct
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (string_hash, IEnumerable_1, IEnumerator)
from ...Core.comment import (Comment, Remark)
from ...Core.Helper.collections_ import (Option_fromValueWithDefault, ResizeArray_iter)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.publication import Publication
from ...Core.uri import URIModule_fromString
from .comment import (Comment_fromString, Comment_toString)
from .sparse_table import (SparseTable_GetEmptyComments_3ECCA699, SparseTable__TryGetValueDefault_5BAE6133, SparseTable__TryGetValue_11FD62A8, SparseTable, SparseTable_Create_Z2192E64B, SparseTable_FromRows_Z5579EC29, SparseTable_ToRows_759CAFC1)

pub_med_idlabel: str = "PubMed ID"

doi_label: str = "DOI"

author_list_label: str = "Author List"

title_label: str = "Title"

status_label: str = "Status"

status_term_accession_number_label: str = "Status Term Accession Number"

status_term_source_reflabel: str = "Status Term Source REF"

labels: FSharpList[str] = of_array([pub_med_idlabel, doi_label, author_list_label, title_label, status_label, status_term_accession_number_label, status_term_source_reflabel])

def from_string(pub_med_id: str | None, doi: str | None, author: str | None, title: str | None, status: str | None, status_term_source_ref: str | None, status_term_accession_number: str | None, comments: Array[Comment]) -> Publication:
    status_1: OntologyAnnotation = OntologyAnnotation(status, status_term_source_ref, status_term_accession_number)
    def _arrow1083(s: str, pub_med_id: Any=pub_med_id, doi: Any=doi, author: Any=author, title: Any=title, status: Any=status, status_term_source_ref: Any=status_term_source_ref, status_term_accession_number: Any=status_term_accession_number, comments: Any=comments) -> str:
        return URIModule_fromString(s)

    pub_med_id_1: str | None = map(_arrow1083, pub_med_id)
    status_2: OntologyAnnotation | None = Option_fromValueWithDefault(OntologyAnnotation(), status_1)
    return Publication.make(pub_med_id_1, doi, author, title, status_2, comments)


def from_sparse_table(matrix: SparseTable) -> FSharpList[Publication]:
    if (length(matrix.CommentKeys) != 0) if (matrix.ColumnCount == 0) else False:
        comments: Array[Comment] = SparseTable_GetEmptyComments_3ECCA699(matrix)
        def _arrow1084(__unit: None=None, matrix: Any=matrix) -> Publication:
            return_val: Publication = Publication.create()
            return_val.Comments = comments
            return return_val

        return singleton(_arrow1084())

    else: 
        def _arrow1085(i: int, matrix: Any=matrix) -> Publication:
            def mapping(k: str) -> Comment:
                return Comment_fromString(k, SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (k, i)))

            comments_1: Array[Comment] = list(map_1(mapping, matrix.CommentKeys))
            return from_string(SparseTable__TryGetValue_11FD62A8(matrix, (pub_med_idlabel, i)), SparseTable__TryGetValue_11FD62A8(matrix, (doi_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (author_list_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (title_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (status_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (status_term_source_reflabel, i)), SparseTable__TryGetValue_11FD62A8(matrix, (status_term_accession_number_label, i)), comments_1)

        return initialize(matrix.ColumnCount, _arrow1085)



def to_sparse_table(publications: FSharpList[Publication]) -> SparseTable:
    matrix: SparseTable = SparseTable_Create_Z2192E64B(None, labels, None, length(publications) + 1)
    comment_keys: FSharpList[str] = empty()
    def action(i: int, p: Publication, publications: Any=publications) -> None:
        i_1: int = (i + 1) or 0
        s_1: dict[str, Any]
        s: OntologyAnnotation = default_arg(p.Status, OntologyAnnotation())
        s_1 = OntologyAnnotation.to_string_object(s, True)
        add_to_dict(matrix.Matrix, (pub_med_idlabel, i_1), default_arg(p.PubMedID, ""))
        add_to_dict(matrix.Matrix, (doi_label, i_1), default_arg(p.DOI, ""))
        add_to_dict(matrix.Matrix, (author_list_label, i_1), default_arg(p.Authors, ""))
        add_to_dict(matrix.Matrix, (title_label, i_1), default_arg(p.Title, ""))
        add_to_dict(matrix.Matrix, (status_label, i_1), s_1["TermName"])
        add_to_dict(matrix.Matrix, (status_term_accession_number_label, i_1), s_1["TermAccessionNumber"])
        add_to_dict(matrix.Matrix, (status_term_source_reflabel, i_1), s_1["TermSourceREF"])
        def f(comment: Comment, i: Any=i, p: Any=p) -> None:
            nonlocal comment_keys
            pattern_input: tuple[str, str] = Comment_toString(comment)
            n: str = pattern_input[0]
            comment_keys = cons(n, comment_keys)
            add_to_dict(matrix.Matrix, (n, i_1), pattern_input[1])

        ResizeArray_iter(f, p.Comments)

    iterate_indexed(action, publications)
    class ObjectExpr1090:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1088(x: str, y: str) -> bool:
                return x == y

            return _arrow1088

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return SparseTable(matrix.Matrix, matrix.Keys, reverse(List_distinct(comment_keys, ObjectExpr1090())), matrix.ColumnCount)


def from_rows(prefix: str | None, line_number: int, rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, int, FSharpList[Remark], FSharpList[Publication]]:
    tupled_arg: tuple[str | None, int, FSharpList[Remark], SparseTable] = SparseTable_FromRows_Z5579EC29(rows, labels, line_number) if (prefix is None) else SparseTable_FromRows_Z5579EC29(rows, labels, line_number, prefix)
    return (tupled_arg[0], tupled_arg[1], tupled_arg[2], from_sparse_table(tupled_arg[3]))


def to_rows(prefix: str | None, publications: FSharpList[Publication]) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    m: SparseTable = to_sparse_table(publications)
    if prefix is None:
        return SparseTable_ToRows_759CAFC1(m)

    else: 
        return SparseTable_ToRows_759CAFC1(m, prefix)



__all__ = ["pub_med_idlabel", "doi_label", "author_list_label", "title_label", "status_label", "status_term_accession_number_label", "status_term_source_reflabel", "labels", "from_string", "from_sparse_table", "to_sparse_table", "from_rows", "to_rows"]

