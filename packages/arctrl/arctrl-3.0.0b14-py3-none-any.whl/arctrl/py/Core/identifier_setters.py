from __future__ import annotations
from .arc_types import (ArcAssay, ArcStudy, ArcWorkflow, ArcRun, ArcInvestigation)
from .Helper.identifier import check_valid_characters
from .Table.arc_table import ArcTable

def set_arc_table_name(new_name: str, table: ArcTable) -> ArcTable:
    check_valid_characters(new_name)
    table.Name = new_name
    return table


def set_assay_identifier(new_identifier: str, assay: ArcAssay) -> ArcAssay:
    check_valid_characters(new_identifier)
    assay.Identifier = new_identifier
    return assay


def set_study_identifier(new_identifier: str, study: ArcStudy) -> ArcStudy:
    check_valid_characters(new_identifier)
    study.Identifier = new_identifier
    return study


def set_workflow_identifier(new_identifier: str, workflow: ArcWorkflow) -> ArcWorkflow:
    check_valid_characters(new_identifier)
    workflow.Identifier = new_identifier
    return workflow


def set_run_identifier(new_identifier: str, run: ArcRun) -> ArcRun:
    check_valid_characters(new_identifier)
    run.Identifier = new_identifier
    return run


def set_investigation_identifier(new_identifier: str, investigation: ArcInvestigation) -> ArcInvestigation:
    check_valid_characters(new_identifier)
    investigation.Identifier = new_identifier
    return investigation


__all__ = ["set_arc_table_name", "set_assay_identifier", "set_study_identifier", "set_workflow_identifier", "set_run_identifier", "set_investigation_identifier"]

