from __future__ import annotations
from ...fable_modules.fable_library.list import (of_array, FSharpList)
from ...fable_modules.fable_library.util import (IEnumerable_1, IEnumerator)
from ...Core.comment import Remark
from ...Core.ontology_annotation import OntologyAnnotation
from .ontology_annotation import (from_sparse_table as from_sparse_table_1, to_sparse_table as to_sparse_table_1, from_rows as from_rows_1, to_rows as to_rows_1)
from .sparse_table import SparseTable

design_type_label: str = "Type"

design_type_term_accession_number_label: str = "Type Term Accession Number"

design_type_term_source_reflabel: str = "Type Term Source REF"

labels: FSharpList[str] = of_array([design_type_label, design_type_term_accession_number_label, design_type_term_source_reflabel])

def from_sparse_table(matrix: SparseTable) -> FSharpList[OntologyAnnotation]:
    return from_sparse_table_1(design_type_label, design_type_term_source_reflabel, design_type_term_accession_number_label, matrix)


def to_sparse_table(designs: FSharpList[OntologyAnnotation]) -> SparseTable:
    return to_sparse_table_1(design_type_label, design_type_term_source_reflabel, design_type_term_accession_number_label, designs)


def from_rows(prefix: str | None, line_number: int, rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, int, FSharpList[Remark], FSharpList[OntologyAnnotation]]:
    return from_rows_1(prefix, design_type_label, design_type_term_source_reflabel, design_type_term_accession_number_label, line_number, rows)


def to_rows(prefix: str | None, designs: FSharpList[OntologyAnnotation]) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    return to_rows_1(prefix, design_type_label, design_type_term_source_reflabel, design_type_term_accession_number_label, designs)


__all__ = ["design_type_label", "design_type_term_accession_number_label", "design_type_term_source_reflabel", "labels", "from_sparse_table", "to_sparse_table", "from_rows", "to_rows"]

