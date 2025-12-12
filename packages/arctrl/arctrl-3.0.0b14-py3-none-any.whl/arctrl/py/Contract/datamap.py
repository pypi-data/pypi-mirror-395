from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.array_ import equals_with
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import safe_hash
from ..Core.datamap import Datamap
from ..Core.Helper.identifier import (Assay_datamapFileNameFromIdentifier, Study_datamapFileNameFromIdentifier, Workflow_datamapFileNameFromIdentifier, Run_datamapFileNameFromIdentifier)
from ..FileSystem.path import combine_many
from ..Spreadsheet.datamap import (to_fs_workbook, from_fs_workbook)
from .contract import (Contract, DTOType, DTO)

def _007CDatamapPath_007C__007C(input: Array[str]) -> str | None:
    (pattern_matching_result,) = (None,)
    def _arrow3708(x: str, y: str, input: Any=input) -> bool:
        return x == y

    if (len(input) == 3) if (not equals_with(_arrow3708, input, None)) else False:
        if input[0] == "assays":
            if input[2] == "isa.datamap.xlsx":
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 4


        elif input[0] == "studies":
            if input[2] == "isa.datamap.xlsx":
                pattern_matching_result = 1

            else: 
                pattern_matching_result = 4


        elif input[0] == "workflows":
            if input[2] == "isa.datamap.xlsx":
                pattern_matching_result = 2

            else: 
                pattern_matching_result = 4


        elif input[0] == "runs":
            if input[2] == "isa.datamap.xlsx":
                pattern_matching_result = 3

            else: 
                pattern_matching_result = 4


        else: 
            pattern_matching_result = 4


    else: 
        pattern_matching_result = 4

    if pattern_matching_result == 0:
        any_assay_name: str = input[1]
        return combine_many(input)

    elif pattern_matching_result == 1:
        any_study_name: str = input[1]
        return combine_many(input)

    elif pattern_matching_result == 2:
        any_workflow_name: str = input[1]
        return combine_many(input)

    elif pattern_matching_result == 3:
        any_run_name: str = input[1]
        return combine_many(input)

    elif pattern_matching_result == 4:
        return None



def ARCtrl_Datamap__Datamap_ToCreateContractForAssay_Z721C83C5(this: Datamap, assay_identifier: str) -> Contract:
    path: str = Assay_datamapFileNameFromIdentifier(assay_identifier)
    return Contract.create_create(path, DTOType(5), DTO(0, to_fs_workbook(this)))


def ARCtrl_Datamap__Datamap_ToUpdateContractForAssay_Z721C83C5(this: Datamap, assay_identifier: str) -> Contract:
    path: str = Assay_datamapFileNameFromIdentifier(assay_identifier)
    return Contract.create_update(path, DTOType(5), DTO(0, to_fs_workbook(this)))


def ARCtrl_Datamap__Datamap_ToDeleteContractForAssay_Z721C83C5(this: Datamap, assay_identifier: str) -> Contract:
    path: str = Assay_datamapFileNameFromIdentifier(assay_identifier)
    return Contract.create_delete(path)


def ARCtrl_Datamap__Datamap_toDeleteContractForAssay_Static_Z721C83C5(assay_identifier: str) -> Callable[[Datamap], Contract]:
    def _arrow3709(datamap: Datamap, assay_identifier: Any=assay_identifier) -> Contract:
        return ARCtrl_Datamap__Datamap_ToDeleteContractForAssay_Z721C83C5(datamap, assay_identifier)

    return _arrow3709


def ARCtrl_Datamap__Datamap_toUpdateContractForAssay_Static_Z721C83C5(assay_identifier: str) -> Callable[[Datamap], Contract]:
    def _arrow3710(datamap: Datamap, assay_identifier: Any=assay_identifier) -> Contract:
        return ARCtrl_Datamap__Datamap_ToUpdateContractForAssay_Z721C83C5(datamap, assay_identifier)

    return _arrow3710


def ARCtrl_Datamap__Datamap_tryFromReadContractForAssay_Static(assay_identifier: str, c: Contract) -> Datamap | None:
    path: str = Assay_datamapFileNameFromIdentifier(assay_identifier)
    (pattern_matching_result, fsworkbook_1, p_1) = (None, None, None)
    if c.Operation == "READ":
        if c.DTOType is not None:
            if c.DTOType.tag == 5:
                if c.DTO is not None:
                    if c.DTO.tag == 0:
                        def _arrow3711(__unit: None=None, assay_identifier: Any=assay_identifier, c: Any=c) -> bool:
                            fsworkbook: Any = c.DTO.fields[0]
                            return c.Path == path

                        if _arrow3711():
                            pattern_matching_result = 0
                            fsworkbook_1 = c.DTO.fields[0]
                            p_1 = c.Path

                        else: 
                            pattern_matching_result = 1


                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        dm: Datamap = from_fs_workbook(fsworkbook_1)
        dm.StaticHash = safe_hash(dm) or 0
        return dm

    elif pattern_matching_result == 1:
        return None



def ARCtrl_Datamap__Datamap_ToCreateContractForStudy_Z721C83C5(this: Datamap, study_identifier: str) -> Contract:
    path: str = Study_datamapFileNameFromIdentifier(study_identifier)
    return Contract.create_create(path, DTOType(5), DTO(0, to_fs_workbook(this)))


def ARCtrl_Datamap__Datamap_ToUpdateContractForStudy_Z721C83C5(this: Datamap, study_identifier: str) -> Contract:
    path: str = Study_datamapFileNameFromIdentifier(study_identifier)
    return Contract.create_update(path, DTOType(5), DTO(0, to_fs_workbook(this)))


def ARCtrl_Datamap__Datamap_ToDeleteContractForStudy_Z721C83C5(this: Datamap, study_identifier: str) -> Contract:
    path: str = Study_datamapFileNameFromIdentifier(study_identifier)
    return Contract.create_delete(path)


def ARCtrl_Datamap__Datamap_toDeleteContractForStudy_Static_Z721C83C5(study_identifier: str) -> Callable[[Datamap], Contract]:
    def _arrow3712(datamap: Datamap, study_identifier: Any=study_identifier) -> Contract:
        return ARCtrl_Datamap__Datamap_ToDeleteContractForStudy_Z721C83C5(datamap, study_identifier)

    return _arrow3712


def ARCtrl_Datamap__Datamap_toUpdateContractForStudy_Static_Z721C83C5(study_identifier: str) -> Callable[[Datamap], Contract]:
    def _arrow3713(datamap: Datamap, study_identifier: Any=study_identifier) -> Contract:
        return ARCtrl_Datamap__Datamap_ToUpdateContractForStudy_Z721C83C5(datamap, study_identifier)

    return _arrow3713


def ARCtrl_Datamap__Datamap_tryFromReadContractForStudy_Static(study_identifier: str, c: Contract) -> Datamap | None:
    path: str = Study_datamapFileNameFromIdentifier(study_identifier)
    (pattern_matching_result, fsworkbook_1, p_1) = (None, None, None)
    if c.Operation == "READ":
        if c.DTOType is not None:
            if c.DTOType.tag == 5:
                if c.DTO is not None:
                    if c.DTO.tag == 0:
                        def _arrow3714(__unit: None=None, study_identifier: Any=study_identifier, c: Any=c) -> bool:
                            fsworkbook: Any = c.DTO.fields[0]
                            return c.Path == path

                        if _arrow3714():
                            pattern_matching_result = 0
                            fsworkbook_1 = c.DTO.fields[0]
                            p_1 = c.Path

                        else: 
                            pattern_matching_result = 1


                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        dm: Datamap = from_fs_workbook(fsworkbook_1)
        dm.StaticHash = safe_hash(dm) or 0
        return dm

    elif pattern_matching_result == 1:
        return None



def ARCtrl_Datamap__Datamap_ToCreateContractForWorkflow_Z721C83C5(this: Datamap, workflow_identifier: str) -> Contract:
    path: str = Workflow_datamapFileNameFromIdentifier(workflow_identifier)
    return Contract.create_create(path, DTOType(5), DTO(0, to_fs_workbook(this)))


def ARCtrl_Datamap__Datamap_ToUpdateContractForWorkflow_Z721C83C5(this: Datamap, workflow_identifier: str) -> Contract:
    path: str = Workflow_datamapFileNameFromIdentifier(workflow_identifier)
    return Contract.create_update(path, DTOType(5), DTO(0, to_fs_workbook(this)))


def ARCtrl_Datamap__Datamap_ToDeleteContractForWorkflow_Z721C83C5(this: Datamap, workflow_identifier: str) -> Contract:
    path: str = Workflow_datamapFileNameFromIdentifier(workflow_identifier)
    return Contract.create_delete(path)


def ARCtrl_Datamap__Datamap_toDeleteContractForWorkflow_Static_Z721C83C5(workflow_identifier: str) -> Callable[[Datamap], Contract]:
    def _arrow3715(datamap: Datamap, workflow_identifier: Any=workflow_identifier) -> Contract:
        return ARCtrl_Datamap__Datamap_ToDeleteContractForWorkflow_Z721C83C5(datamap, workflow_identifier)

    return _arrow3715


def ARCtrl_Datamap__Datamap_toUpdateContractForWorkflow_Static_Z721C83C5(workflow_identifier: str) -> Callable[[Datamap], Contract]:
    def _arrow3716(datamap: Datamap, workflow_identifier: Any=workflow_identifier) -> Contract:
        return ARCtrl_Datamap__Datamap_ToUpdateContractForWorkflow_Z721C83C5(datamap, workflow_identifier)

    return _arrow3716


def ARCtrl_Datamap__Datamap_tryFromReadContractForWorkflow_Static(workflow_identifier: str, c: Contract) -> Datamap | None:
    path: str = Workflow_datamapFileNameFromIdentifier(workflow_identifier)
    (pattern_matching_result, fsworkbook_1, p_1) = (None, None, None)
    if c.Operation == "READ":
        if c.DTOType is not None:
            if c.DTOType.tag == 5:
                if c.DTO is not None:
                    if c.DTO.tag == 0:
                        def _arrow3717(__unit: None=None, workflow_identifier: Any=workflow_identifier, c: Any=c) -> bool:
                            fsworkbook: Any = c.DTO.fields[0]
                            return c.Path == path

                        if _arrow3717():
                            pattern_matching_result = 0
                            fsworkbook_1 = c.DTO.fields[0]
                            p_1 = c.Path

                        else: 
                            pattern_matching_result = 1


                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        dm: Datamap = from_fs_workbook(fsworkbook_1)
        dm.StaticHash = safe_hash(dm) or 0
        return dm

    elif pattern_matching_result == 1:
        return None



def ARCtrl_Datamap__Datamap_ToCreateContractForRun_Z721C83C5(this: Datamap, run_identifier: str) -> Contract:
    path: str = Run_datamapFileNameFromIdentifier(run_identifier)
    return Contract.create_create(path, DTOType(5), DTO(0, to_fs_workbook(this)))


def ARCtrl_Datamap__Datamap_ToUpdateContractForRun_Z721C83C5(this: Datamap, run_identifier: str) -> Contract:
    path: str = Run_datamapFileNameFromIdentifier(run_identifier)
    return Contract.create_update(path, DTOType(5), DTO(0, to_fs_workbook(this)))


def ARCtrl_Datamap__Datamap_ToDeleteContractForRun_Z721C83C5(this: Datamap, run_identifier: str) -> Contract:
    path: str = Run_datamapFileNameFromIdentifier(run_identifier)
    return Contract.create_delete(path)


def ARCtrl_Datamap__Datamap_toDeleteContractForRun_Static_Z721C83C5(run_identifier: str) -> Callable[[Datamap], Contract]:
    def _arrow3718(datamap: Datamap, run_identifier: Any=run_identifier) -> Contract:
        return ARCtrl_Datamap__Datamap_ToDeleteContractForRun_Z721C83C5(datamap, run_identifier)

    return _arrow3718


def ARCtrl_Datamap__Datamap_toUpdateContractForRun_Static_Z721C83C5(run_identifier: str) -> Callable[[Datamap], Contract]:
    def _arrow3719(datamap: Datamap, run_identifier: Any=run_identifier) -> Contract:
        return ARCtrl_Datamap__Datamap_ToUpdateContractForRun_Z721C83C5(datamap, run_identifier)

    return _arrow3719


def ARCtrl_Datamap__Datamap_tryFromReadContractForRun_Static(run_identifier: str, c: Contract) -> Datamap | None:
    path: str = Run_datamapFileNameFromIdentifier(run_identifier)
    (pattern_matching_result, fsworkbook_1, p_1) = (None, None, None)
    if c.Operation == "READ":
        if c.DTOType is not None:
            if c.DTOType.tag == 5:
                if c.DTO is not None:
                    if c.DTO.tag == 0:
                        def _arrow3720(__unit: None=None, run_identifier: Any=run_identifier, c: Any=c) -> bool:
                            fsworkbook: Any = c.DTO.fields[0]
                            return c.Path == path

                        if _arrow3720():
                            pattern_matching_result = 0
                            fsworkbook_1 = c.DTO.fields[0]
                            p_1 = c.Path

                        else: 
                            pattern_matching_result = 1


                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        dm: Datamap = from_fs_workbook(fsworkbook_1)
        dm.StaticHash = safe_hash(dm) or 0
        return dm

    elif pattern_matching_result == 1:
        return None



__all__ = ["_007CDatamapPath_007C__007C", "ARCtrl_Datamap__Datamap_ToCreateContractForAssay_Z721C83C5", "ARCtrl_Datamap__Datamap_ToUpdateContractForAssay_Z721C83C5", "ARCtrl_Datamap__Datamap_ToDeleteContractForAssay_Z721C83C5", "ARCtrl_Datamap__Datamap_toDeleteContractForAssay_Static_Z721C83C5", "ARCtrl_Datamap__Datamap_toUpdateContractForAssay_Static_Z721C83C5", "ARCtrl_Datamap__Datamap_tryFromReadContractForAssay_Static", "ARCtrl_Datamap__Datamap_ToCreateContractForStudy_Z721C83C5", "ARCtrl_Datamap__Datamap_ToUpdateContractForStudy_Z721C83C5", "ARCtrl_Datamap__Datamap_ToDeleteContractForStudy_Z721C83C5", "ARCtrl_Datamap__Datamap_toDeleteContractForStudy_Static_Z721C83C5", "ARCtrl_Datamap__Datamap_toUpdateContractForStudy_Static_Z721C83C5", "ARCtrl_Datamap__Datamap_tryFromReadContractForStudy_Static", "ARCtrl_Datamap__Datamap_ToCreateContractForWorkflow_Z721C83C5", "ARCtrl_Datamap__Datamap_ToUpdateContractForWorkflow_Z721C83C5", "ARCtrl_Datamap__Datamap_ToDeleteContractForWorkflow_Z721C83C5", "ARCtrl_Datamap__Datamap_toDeleteContractForWorkflow_Static_Z721C83C5", "ARCtrl_Datamap__Datamap_toUpdateContractForWorkflow_Static_Z721C83C5", "ARCtrl_Datamap__Datamap_tryFromReadContractForWorkflow_Static", "ARCtrl_Datamap__Datamap_ToCreateContractForRun_Z721C83C5", "ARCtrl_Datamap__Datamap_ToUpdateContractForRun_Z721C83C5", "ARCtrl_Datamap__Datamap_ToDeleteContractForRun_Z721C83C5", "ARCtrl_Datamap__Datamap_toDeleteContractForRun_Static_Z721C83C5", "ARCtrl_Datamap__Datamap_toUpdateContractForRun_Static_Z721C83C5", "ARCtrl_Datamap__Datamap_tryFromReadContractForRun_Static"]

