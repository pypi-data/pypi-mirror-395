from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (of_array, FSharpList, map as map_1, empty, cons, reverse)
from ...fable_modules.fable_library.map_util import add_to_dict
from ...fable_modules.fable_library.option import (map, default_arg)
from ...fable_modules.fable_library.seq2 import List_distinct
from ...fable_modules.fable_library.string_ import (starts_with_exact, join)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (string_hash, IEnumerable_1, IEnumerator)
from ...Core.arc_types import ArcRun
from ...Core.comment import (Comment, Remark)
from ...Core.conversion import (JsonTypes_decomposeTechnologyPlatform, JsonTypes_composeTechnologyPlatform)
from ...Core.Helper.collections_ import (Option_fromValueWithDefault, ResizeArray_iter)
from ...Core.Helper.identifier import (create_missing_identifier, Assay_tryIdentifierFromFileName, Run_fileNameFromIdentifier)
from ...Core.ontology_annotation import OntologyAnnotation
from .comment import (Comment_fromString, Comment_toString)
from .sparse_table import (SparseTable__TryGetValueDefault_5BAE6133, SparseTable__TryGetValue_11FD62A8, SparseTable, SparseTable_Create_Z2192E64B, SparseTable_FromRows_Z5579EC29, SparseTable_ToRows_759CAFC1)

labels: FSharpList[str] = of_array(["Identifier", "Title", "Description", "Workflow Identifiers", "Measurement Type", "Measurement Type Term Accession Number", "Measurement Type Term Source REF", "Technology Type", "Technology Type Term Accession Number", "Technology Type Term Source REF", "Technology Platform", "File Name"])

def from_string(identifier: str | None, title: str | None, description: str | None, workflow_identifiers: str | None, measurement_type: str | None, measurement_type_term_source_ref: str | None, measurement_type_term_accession_number: str | None, technology_type: str | None, technology_type_term_source_ref: str | None, technology_type_term_accession_number: str | None, technology_platform: str | None, file_name: str | None, comments: Array[Comment]) -> ArcRun:
    workflow_identifiers_1: Array[str]
    if workflow_identifiers is None:
        workflow_identifiers_1 = []

    else: 
        wi: str = workflow_identifiers
        workflow_identifiers_1 = list(wi.split(";"))

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
    def _arrow1439(name: str, identifier: Any=identifier, title: Any=title, description: Any=description, workflow_identifiers: Any=workflow_identifiers, measurement_type: Any=measurement_type, measurement_type_term_source_ref: Any=measurement_type_term_source_ref, measurement_type_term_accession_number: Any=measurement_type_term_accession_number, technology_type: Any=technology_type, technology_type_term_source_ref: Any=technology_type_term_source_ref, technology_type_term_accession_number: Any=technology_type_term_accession_number, technology_platform: Any=technology_platform, file_name: Any=file_name, comments: Any=comments) -> OntologyAnnotation:
        return JsonTypes_decomposeTechnologyPlatform(name)

    technology_platform_1: OntologyAnnotation | None = map(_arrow1439, technology_platform)
    return ArcRun.make(identifier_4, title, description, measurement_type_2, technology_type_2, technology_platform_1, workflow_identifiers_1, [], None, [], None, [], comments)


def from_sparse_table(matrix: SparseTable) -> ArcRun:
    def mapping(k: str, matrix: Any=matrix) -> Comment:
        return Comment_fromString(k, SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (k, 0)))

    comments: Array[Comment] = list(map_1(mapping, matrix.CommentKeys))
    return from_string(SparseTable__TryGetValue_11FD62A8(matrix, ("Identifier", 0)), SparseTable__TryGetValue_11FD62A8(matrix, ("Title", 0)), SparseTable__TryGetValue_11FD62A8(matrix, ("Description", 0)), SparseTable__TryGetValue_11FD62A8(matrix, ("Workflow Identifiers", 0)), SparseTable__TryGetValue_11FD62A8(matrix, ("Measurement Type", 0)), SparseTable__TryGetValue_11FD62A8(matrix, ("Measurement Type Term Source REF", 0)), SparseTable__TryGetValue_11FD62A8(matrix, ("Measurement Type Term Accession Number", 0)), SparseTable__TryGetValue_11FD62A8(matrix, ("Technology Type", 0)), SparseTable__TryGetValue_11FD62A8(matrix, ("Technology Type Term Source REF", 0)), SparseTable__TryGetValue_11FD62A8(matrix, ("Technology Type Term Accession Number", 0)), SparseTable__TryGetValue_11FD62A8(matrix, ("Technology Platform", 0)), SparseTable__TryGetValue_11FD62A8(matrix, ("File Name", 0)), comments)


def to_sparse_table(run: ArcRun) -> SparseTable:
    matrix: SparseTable = SparseTable_Create_Z2192E64B(None, labels, None, 2)
    comment_keys: FSharpList[str] = empty()
    pattern_input: tuple[str, str] = (("", "")) if starts_with_exact(run.Identifier, "MISSING_IDENTIFIER_") else ((run.Identifier, Run_fileNameFromIdentifier(run.Identifier)))
    workflow_identifiers: str = join(";", run.WorkflowIdentifiers)
    mt_1: dict[str, Any]
    mt: OntologyAnnotation = default_arg(run.MeasurementType, OntologyAnnotation())
    mt_1 = OntologyAnnotation.to_string_object(mt, True)
    tt_1: dict[str, Any]
    tt: OntologyAnnotation = default_arg(run.TechnologyType, OntologyAnnotation())
    tt_1 = OntologyAnnotation.to_string_object(tt, True)
    add_to_dict(matrix.Matrix, ("Identifier", 1), pattern_input[0])
    add_to_dict(matrix.Matrix, ("Title", 1), default_arg(run.Title, ""))
    add_to_dict(matrix.Matrix, ("Description", 1), default_arg(run.Description, ""))
    add_to_dict(matrix.Matrix, ("Workflow Identifiers", 1), workflow_identifiers)
    add_to_dict(matrix.Matrix, ("Measurement Type", 1), mt_1["TermName"])
    add_to_dict(matrix.Matrix, ("Measurement Type Term Accession Number", 1), mt_1["TermAccessionNumber"])
    add_to_dict(matrix.Matrix, ("Measurement Type Term Source REF", 1), mt_1["TermSourceREF"])
    add_to_dict(matrix.Matrix, ("Technology Type", 1), tt_1["TermName"])
    add_to_dict(matrix.Matrix, ("Technology Type Term Accession Number", 1), tt_1["TermAccessionNumber"])
    add_to_dict(matrix.Matrix, ("Technology Type Term Source REF", 1), tt_1["TermSourceREF"])
    def mapping(tp: OntologyAnnotation, run: Any=run) -> str:
        return JsonTypes_composeTechnologyPlatform(tp)

    add_to_dict(matrix.Matrix, ("Technology Platform", 1), default_arg(map(mapping, run.TechnologyPlatform), ""))
    add_to_dict(matrix.Matrix, ("File Name", 1), pattern_input[1])
    def f(comment: Comment, run: Any=run) -> None:
        nonlocal comment_keys
        pattern_input_1: tuple[str, str] = Comment_toString(comment)
        n: str = pattern_input_1[0]
        comment_keys = cons(n, comment_keys)
        add_to_dict(matrix.Matrix, (n, 1), pattern_input_1[1])

    ResizeArray_iter(f, run.Comments)
    class ObjectExpr1441:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1440(x: str, y: str) -> bool:
                return x == y

            return _arrow1440

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return SparseTable(matrix.Matrix, matrix.Keys, reverse(List_distinct(comment_keys, ObjectExpr1441())), matrix.ColumnCount)


def from_rows(line_number: int, rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, int, FSharpList[Remark], ArcRun]:
    tupled_arg: tuple[str | None, int, FSharpList[Remark], SparseTable] = SparseTable_FromRows_Z5579EC29(rows, labels, line_number, "Run")
    return (tupled_arg[0], tupled_arg[1], tupled_arg[2], from_sparse_table(tupled_arg[3]))


def to_rows(run: ArcRun) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    return SparseTable_ToRows_759CAFC1(to_sparse_table(run), "Run")


__all__ = ["labels", "from_string", "from_sparse_table", "to_sparse_table", "from_rows", "to_rows"]

