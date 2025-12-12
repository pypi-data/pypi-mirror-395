from typing import Any
from ...fable_modules.fable_library.guid import new_guid
from ...fable_modules.fable_library.reg_exp import (get_item, groups)
from ...fable_modules.fable_library.string_ import starts_with_exact
from ...FileSystem.path import combine_many
from .regex import ActivePatterns__007CRegex_007C__007C

def try_check_valid_characters(identifier: str) -> bool:
    if ActivePatterns__007CRegex_007C__007C("^[a-zA-Z0-9_\\- ]+$", identifier) is not None:
        return True

    else: 
        return False



def check_valid_characters(identifier: str) -> None:
    if try_check_valid_characters(identifier):
        pass

    else: 
        raise Exception(("New identifier \"" + identifier) + "\" contains forbidden characters! Allowed characters are: letters, digits, underscore (_), dash (-) and whitespace ( ).")



def create_missing_identifier(__unit: None=None) -> str:
    def _arrow695(__unit: None=None) -> str:
        copy_of_struct: str = new_guid()
        return str(copy_of_struct)

    return "MISSING_IDENTIFIER_" + _arrow695()


def is_missing_identifier(str_1: str) -> bool:
    return starts_with_exact(str_1, "MISSING_IDENTIFIER_")


def remove_missing_identifier(str_1: str) -> str:
    if starts_with_exact(str_1, "MISSING_IDENTIFIER_"):
        return ""

    else: 
        return str_1



def Assay_identifierFromFileName(file_name: str) -> str:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(assays(\\/|\\\\))?(?<identifier>[a-zA-Z0-9_\\- ]+)((\\/|\\\\)isa.assay.xlsx)?$", file_name)
    if active_pattern_result is not None:
        m: Any = active_pattern_result
        return get_item(groups(m), "identifier") or ""

    else: 
        raise Exception(("Cannot parse assay identifier from FileName `" + file_name) + "`")



def Assay_tryIdentifierFromFileName(file_name: str) -> str | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(assays(\\/|\\\\))?(?<identifier>[a-zA-Z0-9_\\- ]+)((\\/|\\\\)isa.assay.xlsx)?$", file_name)
    if active_pattern_result is not None:
        m: Any = active_pattern_result
        return get_item(groups(m), "identifier") or ""

    else: 
        return None



def Assay_fileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["assays", identifier, "isa.assay.xlsx"])


def Assay_tryFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["assays", identifier, "isa.assay.xlsx"])

    else: 
        return None



def Assay_datamapFileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["assays", identifier, "isa.datamap.xlsx"])


def Assay_tryDatamapFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["assays", identifier, "isa.datamap.xlsx"])

    else: 
        return None



def Study_identifierFromFileName(file_name: str) -> str:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(studies(\\/|\\\\))?(?<identifier>[a-zA-Z0-9_\\- ]+)((\\/|\\\\)isa.study.xlsx)?$", file_name)
    if active_pattern_result is not None:
        m: Any = active_pattern_result
        return get_item(groups(m), "identifier") or ""

    else: 
        raise Exception(("Cannot parse study identifier from FileName `" + file_name) + "`")



def Study_tryIdentifierFromFileName(file_name: str) -> str | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(studies(\\/|\\\\))?(?<identifier>[a-zA-Z0-9_\\- ]+)((\\/|\\\\)isa.study.xlsx)?$", file_name)
    if active_pattern_result is not None:
        m: Any = active_pattern_result
        return get_item(groups(m), "identifier") or ""

    else: 
        return None



def Study_fileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["studies", identifier, "isa.study.xlsx"])


def Study_tryFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["studies", identifier, "isa.study.xlsx"])

    else: 
        return None



def Study_datamapFileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["studies", identifier, "isa.datamap.xlsx"])


def Study_tryDatamapFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["studies", identifier, "isa.datamap.xlsx"])

    else: 
        return None



def Workflow_identifierFromFileName(file_name: str) -> str:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(workflows(\\/|\\\\))?(?<identifier>[a-zA-Z0-9_\\- ]+)((\\/|\\\\)isa.workflow.xlsx)?$", file_name)
    if active_pattern_result is not None:
        m: Any = active_pattern_result
        return get_item(groups(m), "identifier") or ""

    else: 
        raise Exception(("Cannot parse workflow identifier from FileName `" + file_name) + "`")



def Workflow_tryIdentifierFromFileName(file_name: str) -> str | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(workflows(\\/|\\\\))?(?<identifier>[a-zA-Z0-9_\\- ]+)((\\/|\\\\)isa.workflow.xlsx)?$", file_name)
    if active_pattern_result is not None:
        m: Any = active_pattern_result
        return get_item(groups(m), "identifier") or ""

    else: 
        return None



def Workflow_fileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["workflows", identifier, "isa.workflow.xlsx"])


def Workflow_tryFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["workflows", identifier, "isa.workflow.xlsx"])

    else: 
        return None



def Workflow_cwlFileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["workflows", identifier, "workflow.cwl"])


def Workflow_tryCwlFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["workflows", identifier, "workflow.cwl"])

    else: 
        return None



def Workflow_datamapFileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["workflows", identifier, "isa.datamap.xlsx"])


def Workflow_tryDatamapFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["workflows", identifier, "isa.datamap.xlsx"])

    else: 
        return None



def Run_identifierFromFileName(file_name: str) -> str:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(runs(\\/|\\\\))?(?<identifier>[a-zA-Z0-9_\\- ]+)((\\/|\\\\)isa.run.xlsx)?$", file_name)
    if active_pattern_result is not None:
        m: Any = active_pattern_result
        return get_item(groups(m), "identifier") or ""

    else: 
        raise Exception(("Cannot parse run identifier from FileName `" + file_name) + "`")



def Run_tryIdentifierFromFileName(file_name: str) -> str | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(runs(\\/|\\\\))?(?<identifier>[a-zA-Z0-9_\\- ]+)((\\/|\\\\)isa.run.xlsx)?$", file_name)
    if active_pattern_result is not None:
        m: Any = active_pattern_result
        return get_item(groups(m), "identifier") or ""

    else: 
        return None



def Run_fileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["runs", identifier, "isa.run.xlsx"])


def Run_tryFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["runs", identifier, "isa.run.xlsx"])

    else: 
        return None



def Run_cwlFileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["runs", identifier, "run.cwl"])


def Run_tryCwlFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["runs", identifier, "run.cwl"])

    else: 
        return None



def Run_ymlFileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["runs", identifier, "run.yml"])


def Run_tryYmlFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["runs", identifier, "run.yml"])

    else: 
        return None



def Run_datamapFileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["runs", identifier, "isa.datamap.xlsx"])


def Run_tryDatamapFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["runs", identifier, "isa.datamap.xlsx"])

    else: 
        return None



__all__ = ["try_check_valid_characters", "check_valid_characters", "create_missing_identifier", "is_missing_identifier", "remove_missing_identifier", "Assay_identifierFromFileName", "Assay_tryIdentifierFromFileName", "Assay_fileNameFromIdentifier", "Assay_tryFileNameFromIdentifier", "Assay_datamapFileNameFromIdentifier", "Assay_tryDatamapFileNameFromIdentifier", "Study_identifierFromFileName", "Study_tryIdentifierFromFileName", "Study_fileNameFromIdentifier", "Study_tryFileNameFromIdentifier", "Study_datamapFileNameFromIdentifier", "Study_tryDatamapFileNameFromIdentifier", "Workflow_identifierFromFileName", "Workflow_tryIdentifierFromFileName", "Workflow_fileNameFromIdentifier", "Workflow_tryFileNameFromIdentifier", "Workflow_cwlFileNameFromIdentifier", "Workflow_tryCwlFileNameFromIdentifier", "Workflow_datamapFileNameFromIdentifier", "Workflow_tryDatamapFileNameFromIdentifier", "Run_identifierFromFileName", "Run_tryIdentifierFromFileName", "Run_fileNameFromIdentifier", "Run_tryFileNameFromIdentifier", "Run_cwlFileNameFromIdentifier", "Run_tryCwlFileNameFromIdentifier", "Run_ymlFileNameFromIdentifier", "Run_tryYmlFileNameFromIdentifier", "Run_datamapFileNameFromIdentifier", "Run_tryDatamapFileNameFromIdentifier"]

