from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (of_array, FSharpList, length, singleton, initialize, map as map_1, empty, iterate_indexed, cons, reverse)
from ...fable_modules.fable_library.map_util import add_to_dict
from ...fable_modules.fable_library.option import (map, default_arg)
from ...fable_modules.fable_library.seq2 import List_distinct
from ...fable_modules.fable_library.string_ import starts_with_exact
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (string_hash, IEnumerable_1, IEnumerator)
from ...Core.arc_types import ArcAssay
from ...Core.comment import (Comment, Remark)
from ...Core.conversion import (JsonTypes_decomposeTechnologyPlatform, JsonTypes_composeTechnologyPlatform)
from ...Core.Helper.collections_ import (Option_fromValueWithDefault, ResizeArray_iter)
from ...Core.Helper.identifier import (create_missing_identifier, Assay_tryIdentifierFromFileName, remove_missing_identifier, Assay_fileNameFromIdentifier)
from ...Core.ontology_annotation import OntologyAnnotation
from .comment import (Comment_fromString, Comment_toString)
from .sparse_table import (SparseTable_GetEmptyComments_3ECCA699, SparseTable__TryGetValueDefault_5BAE6133, SparseTable__TryGetValue_11FD62A8, SparseTable, SparseTable_Create_Z2192E64B, SparseTable_FromRows_Z5579EC29, SparseTable_ToRows_759CAFC1)

labels: FSharpList[str] = of_array(["Identifier", "Title", "Description", "Measurement Type", "Measurement Type Term Accession Number", "Measurement Type Term Source REF", "Technology Type", "Technology Type Term Accession Number", "Technology Type Term Source REF", "Technology Platform", "File Name"])

def from_string(identifier: str | None, title: str | None, description: str | None, measurement_type: str | None, measurement_type_term_source_ref: str | None, measurement_type_term_accession_number: str | None, technology_type: str | None, technology_type_term_source_ref: str | None, technology_type_term_accession_number: str | None, technology_platform: str | None, file_name: str | None, comments: Array[Comment]) -> ArcAssay:
    measurement_type_1: OntologyAnnotation = OntologyAnnotation.create(measurement_type, measurement_type_term_source_ref, measurement_type_term_accession_number)
    technology_type_1: OntologyAnnotation = OntologyAnnotation.create(technology_type, technology_type_term_source_ref, technology_type_term_accession_number)
    identifier_4: str
    if identifier is None:
        if file_name is None:
            identifier_4 = create_missing_identifier()

        else: 
            match_value: str | None = Assay_tryIdentifierFromFileName(file_name)
            identifier_4 = match_value if (match_value is not None) else create_missing_identifier()


    else: 
        identifier_4 = identifier

    measurement_type_2: OntologyAnnotation | None = Option_fromValueWithDefault(OntologyAnnotation(), measurement_type_1)
    technology_type_2: OntologyAnnotation | None = Option_fromValueWithDefault(OntologyAnnotation(), technology_type_1)
    def _arrow1183(name: str, identifier: Any=identifier, title: Any=title, description: Any=description, measurement_type: Any=measurement_type, measurement_type_term_source_ref: Any=measurement_type_term_source_ref, measurement_type_term_accession_number: Any=measurement_type_term_accession_number, technology_type: Any=technology_type, technology_type_term_source_ref: Any=technology_type_term_source_ref, technology_type_term_accession_number: Any=technology_type_term_accession_number, technology_platform: Any=technology_platform, file_name: Any=file_name, comments: Any=comments) -> OntologyAnnotation:
        return JsonTypes_decomposeTechnologyPlatform(name)

    technology_platform_1: OntologyAnnotation | None = map(_arrow1183, technology_platform)
    return ArcAssay.make(identifier_4, title, description, measurement_type_2, technology_type_2, technology_platform_1, [], None, [], comments)


def from_sparse_table(matrix: SparseTable) -> FSharpList[ArcAssay]:
    if (length(matrix.CommentKeys) != 0) if (matrix.ColumnCount == 0) else False:
        comments: Array[Comment] = SparseTable_GetEmptyComments_3ECCA699(matrix)
        return singleton(ArcAssay.create(create_missing_identifier(), None, None, None, None, None, None, None, None, comments))

    else: 
        def _arrow1188(i: int, matrix: Any=matrix) -> ArcAssay:
            def mapping(k: str) -> Comment:
                return Comment_fromString(k, SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (k, i)))

            comments_1: Array[Comment] = list(map_1(mapping, matrix.CommentKeys))
            return from_string(SparseTable__TryGetValue_11FD62A8(matrix, ("Identifier", i)), SparseTable__TryGetValue_11FD62A8(matrix, ("Title", i)), SparseTable__TryGetValue_11FD62A8(matrix, ("Description", i)), SparseTable__TryGetValue_11FD62A8(matrix, ("Measurement Type", i)), SparseTable__TryGetValue_11FD62A8(matrix, ("Measurement Type Term Source REF", i)), SparseTable__TryGetValue_11FD62A8(matrix, ("Measurement Type Term Accession Number", i)), SparseTable__TryGetValue_11FD62A8(matrix, ("Technology Type", i)), SparseTable__TryGetValue_11FD62A8(matrix, ("Technology Type Term Source REF", i)), SparseTable__TryGetValue_11FD62A8(matrix, ("Technology Type Term Accession Number", i)), SparseTable__TryGetValue_11FD62A8(matrix, ("Technology Platform", i)), SparseTable__TryGetValue_11FD62A8(matrix, ("File Name", i)), comments_1)

        return initialize(matrix.ColumnCount, _arrow1188)



def to_sparse_table(assays: FSharpList[ArcAssay]) -> SparseTable:
    matrix: SparseTable = SparseTable_Create_Z2192E64B(None, labels, None, length(assays) + 1)
    comment_keys: FSharpList[str] = empty()
    def action(i: int, a: ArcAssay, assays: Any=assays) -> None:
        processed_file_name: str = remove_missing_identifier(a.Identifier) if starts_with_exact(a.Identifier, "MISSING_IDENTIFIER_") else Assay_fileNameFromIdentifier(a.Identifier)
        i_1: int = (i + 1) or 0
        mt_1: dict[str, Any]
        mt: OntologyAnnotation = default_arg(a.MeasurementType, OntologyAnnotation())
        mt_1 = OntologyAnnotation.to_string_object(mt, True)
        tt_1: dict[str, Any]
        tt: OntologyAnnotation = default_arg(a.TechnologyType, OntologyAnnotation())
        tt_1 = OntologyAnnotation.to_string_object(tt, True)
        add_to_dict(matrix.Matrix, ("Identifier", i_1), remove_missing_identifier(a.Identifier))
        add_to_dict(matrix.Matrix, ("Title", i_1), default_arg(a.Title, ""))
        add_to_dict(matrix.Matrix, ("Description", i_1), default_arg(a.Description, ""))
        add_to_dict(matrix.Matrix, ("Measurement Type", i_1), mt_1["TermName"])
        add_to_dict(matrix.Matrix, ("Measurement Type Term Accession Number", i_1), mt_1["TermAccessionNumber"])
        add_to_dict(matrix.Matrix, ("Measurement Type Term Source REF", i_1), mt_1["TermSourceREF"])
        add_to_dict(matrix.Matrix, ("Technology Type", i_1), tt_1["TermName"])
        add_to_dict(matrix.Matrix, ("Technology Type Term Accession Number", i_1), tt_1["TermAccessionNumber"])
        add_to_dict(matrix.Matrix, ("Technology Type Term Source REF", i_1), tt_1["TermSourceREF"])
        def mapping(tp: OntologyAnnotation, i: Any=i, a: Any=a) -> str:
            return JsonTypes_composeTechnologyPlatform(tp)

        add_to_dict(matrix.Matrix, ("Technology Platform", i_1), default_arg(map(mapping, a.TechnologyPlatform), ""))
        add_to_dict(matrix.Matrix, ("File Name", i_1), processed_file_name)
        def f(comment: Comment, i: Any=i, a: Any=a) -> None:
            nonlocal comment_keys
            pattern_input: tuple[str, str] = Comment_toString(comment)
            n: str = pattern_input[0]
            comment_keys = cons(n, comment_keys)
            add_to_dict(matrix.Matrix, (n, i_1), pattern_input[1])

        ResizeArray_iter(f, a.Comments)

    iterate_indexed(action, assays)
    class ObjectExpr1192:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1191(x: str, y: str) -> bool:
                return x == y

            return _arrow1191

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return SparseTable(matrix.Matrix, matrix.Keys, reverse(List_distinct(comment_keys, ObjectExpr1192())), matrix.ColumnCount)


def from_rows(prefix: str | None, line_number: int, rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, int, FSharpList[Remark], FSharpList[ArcAssay]]:
    tupled_arg: tuple[str | None, int, FSharpList[Remark], SparseTable] = SparseTable_FromRows_Z5579EC29(rows, labels, line_number, prefix)
    return (tupled_arg[0], tupled_arg[1], tupled_arg[2], from_sparse_table(tupled_arg[3]))


def to_rows(prefix: str | None, assays: FSharpList[ArcAssay]) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    return SparseTable_ToRows_759CAFC1(to_sparse_table(assays), prefix)


__all__ = ["labels", "from_string", "from_sparse_table", "to_sparse_table", "from_rows", "to_rows"]

