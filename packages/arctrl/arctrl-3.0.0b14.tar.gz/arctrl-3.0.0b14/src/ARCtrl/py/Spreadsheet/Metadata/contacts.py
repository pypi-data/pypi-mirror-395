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
from ...Core.conversion import (Person_setOrcidFromComments, Person_setCommentFromORCID)
from ...Core.Helper.collections_ import ResizeArray_iter
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.person import Person
from .comment import (Comment_fromString, Comment_toString)
from .conversions import (OntologyAnnotation_fromAggregatedStrings, OntologyAnnotation_toAggregatedStrings)
from .sparse_table import (SparseTable_GetEmptyComments_3ECCA699, SparseTable__TryGetValueDefault_5BAE6133, SparseTable__TryGetValue_11FD62A8, SparseTable, SparseTable_Create_Z2192E64B, SparseTable_FromRows_Z5579EC29, SparseTable_ToRows_759CAFC1)

last_name_label: str = "Last Name"

first_name_label: str = "First Name"

mid_initials_label: str = "Mid Initials"

email_label: str = "Email"

phone_label: str = "Phone"

fax_label: str = "Fax"

address_label: str = "Address"

affiliation_label: str = "Affiliation"

roles_label: str = "Roles"

roles_term_accession_number_label: str = "Roles Term Accession Number"

roles_term_source_reflabel: str = "Roles Term Source REF"

labels: FSharpList[str] = of_array([last_name_label, first_name_label, mid_initials_label, email_label, phone_label, fax_label, address_label, affiliation_label, roles_label, roles_term_accession_number_label, roles_term_source_reflabel])

def from_string(last_name: str | None, first_name: str | None, mid_initials: str | None, email: str | None, phone: str | None, fax: str | None, address: str | None, affiliation: str | None, role: str, roles_term_accession_number: str, roles_term_source_ref: str, comments: Array[Comment]) -> Person:
    def _arrow1047(__unit: None=None, last_name: Any=last_name, first_name: Any=first_name, mid_initials: Any=mid_initials, email: Any=email, phone: Any=phone, fax: Any=fax, address: Any=address, affiliation: Any=affiliation, role: Any=role, roles_term_accession_number: Any=roles_term_accession_number, roles_term_source_ref: Any=roles_term_source_ref, comments: Any=comments) -> Person:
        roles_1: Array[OntologyAnnotation] = OntologyAnnotation_fromAggregatedStrings(";", role, roles_term_source_ref, roles_term_accession_number)
        return Person.make(None, last_name, first_name, mid_initials, email, phone, fax, address, affiliation, roles_1, comments)

    return Person_setOrcidFromComments(_arrow1047())


def from_sparse_table(matrix: SparseTable) -> FSharpList[Person]:
    if (length(matrix.CommentKeys) != 0) if (matrix.ColumnCount == 0) else False:
        comments: Array[Comment] = SparseTable_GetEmptyComments_3ECCA699(matrix)
        def _arrow1048(__unit: None=None, matrix: Any=matrix) -> Person:
            return_val: Person = Person.create()
            return_val.Comments = comments
            return return_val

        return singleton(_arrow1048())

    else: 
        def _arrow1049(i: int, matrix: Any=matrix) -> Person:
            def mapping(k: str) -> Comment:
                return Comment_fromString(k, SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (k, i)))

            comments_1: Array[Comment] = list(map(mapping, matrix.CommentKeys))
            return from_string(SparseTable__TryGetValue_11FD62A8(matrix, (last_name_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (first_name_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (mid_initials_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (email_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (phone_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (fax_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (address_label, i)), SparseTable__TryGetValue_11FD62A8(matrix, (affiliation_label, i)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (roles_label, i)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (roles_term_accession_number_label, i)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (roles_term_source_reflabel, i)), comments_1)

        return initialize(matrix.ColumnCount, _arrow1049)



def to_sparse_table(persons: FSharpList[Person]) -> SparseTable:
    matrix: SparseTable = SparseTable_Create_Z2192E64B(None, labels, None, length(persons) + 1)
    comment_keys: FSharpList[str] = empty()
    def action(i: int, p: Person, persons: Any=persons) -> None:
        i_1: int = (i + 1) or 0
        r_agg: dict[str, Any] = OntologyAnnotation_toAggregatedStrings(";", list(p.Roles))
        add_to_dict(matrix.Matrix, (last_name_label, i_1), default_arg(p.LastName, ""))
        add_to_dict(matrix.Matrix, (first_name_label, i_1), default_arg(p.FirstName, ""))
        add_to_dict(matrix.Matrix, (mid_initials_label, i_1), default_arg(p.MidInitials, ""))
        add_to_dict(matrix.Matrix, (email_label, i_1), default_arg(p.EMail, ""))
        add_to_dict(matrix.Matrix, (phone_label, i_1), default_arg(p.Phone, ""))
        add_to_dict(matrix.Matrix, (fax_label, i_1), default_arg(p.Fax, ""))
        add_to_dict(matrix.Matrix, (address_label, i_1), default_arg(p.Address, ""))
        add_to_dict(matrix.Matrix, (affiliation_label, i_1), default_arg(p.Affiliation, ""))
        add_to_dict(matrix.Matrix, (roles_label, i_1), r_agg["TermNameAgg"])
        add_to_dict(matrix.Matrix, (roles_term_accession_number_label, i_1), r_agg["TermAccessionNumberAgg"])
        add_to_dict(matrix.Matrix, (roles_term_source_reflabel, i_1), r_agg["TermSourceREFAgg"])
        def f(comment: Comment, i: Any=i, p: Any=p) -> None:
            nonlocal comment_keys
            pattern_input: tuple[str, str] = Comment_toString(comment)
            n: str = pattern_input[0]
            comment_keys = cons(n, comment_keys)
            add_to_dict(matrix.Matrix, (n, i_1), pattern_input[1])

        ResizeArray_iter(f, p.Comments)

    def mapping(person: Person, persons: Any=persons) -> Person:
        return Person_setCommentFromORCID(person)

    iterate_indexed(action, map(mapping, persons))
    class ObjectExpr1051:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1050(x: str, y: str) -> bool:
                return x == y

            return _arrow1050

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return SparseTable(matrix.Matrix, matrix.Keys, reverse(List_distinct(comment_keys, ObjectExpr1051())), matrix.ColumnCount)


def from_rows(prefix: str | None, line_number: int, rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, int, FSharpList[Remark], FSharpList[Person]]:
    tupled_arg: tuple[str | None, int, FSharpList[Remark], SparseTable] = SparseTable_FromRows_Z5579EC29(rows, labels, line_number, prefix)
    return (tupled_arg[0], tupled_arg[1], tupled_arg[2], from_sparse_table(tupled_arg[3]))


def to_rows(prefix: str | None, persons: FSharpList[Person]) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    m: SparseTable = to_sparse_table(persons)
    if prefix is None:
        return SparseTable_ToRows_759CAFC1(m)

    else: 
        return SparseTable_ToRows_759CAFC1(m, prefix)



__all__ = ["last_name_label", "first_name_label", "mid_initials_label", "email_label", "phone_label", "fax_label", "address_label", "affiliation_label", "roles_label", "roles_term_accession_number_label", "roles_term_source_reflabel", "labels", "from_string", "from_sparse_table", "to_sparse_table", "from_rows", "to_rows"]

