from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.array_ import equals_with
from ..fable_modules.fable_library.option import (default_arg, value)
from ..fable_modules.fable_library.seq import (to_array, delay, append, collect, singleton, empty)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..Core.arc_types import ArcWorkflow
from ..Core.Helper.identifier import (Workflow_fileNameFromIdentifier, Workflow_cwlFileNameFromIdentifier)
from ..CWL.cwlprocessing_unit import CWLProcessingUnit
from ..CWL.decode import Decode_decodeCWLProcessingUnit
from ..CWL.encode import encode_processing_unit
from ..FileSystem.file_system_tree import FileSystemTree
from ..FileSystem.path import (combine_many, get_workflow_folder_path)
from ..Spreadsheet.arc_workflow import (ARCtrl_ArcWorkflow__ArcWorkflow_toFsWorkbook_Static_Z1C75CB0E, ARCtrl_ArcWorkflow__ArcWorkflow_fromFsWorkbook_Static_32154C9D)
from .contract import (Contract, DTOType, DTO)

def _007CWorkflowPath_007C__007C(input: Array[str]) -> str | None:
    (pattern_matching_result,) = (None,)
    def _arrow3734(x: str, y: str, input: Any=input) -> bool:
        return x == y

    if (len(input) == 3) if (not equals_with(_arrow3734, input, None)) else False:
        if input[0] == "workflows":
            if input[2] == "isa.workflow.xlsx":
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        any_workflow_name: str = input[1]
        return combine_many(input)

    elif pattern_matching_result == 1:
        return None



def _007CWorkflowCWLPath_007C__007C(input: Array[str]) -> str | None:
    (pattern_matching_result,) = (None,)
    def _arrow3735(x: str, y: str, input: Any=input) -> bool:
        return x == y

    if (len(input) == 3) if (not equals_with(_arrow3735, input, None)) else False:
        if input[0] == "workflows":
            if input[2] == "workflow.cwl":
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        any_workflow_name: str = input[1]
        return combine_many(input)

    elif pattern_matching_result == 1:
        return None



def ARCtrl_ArcWorkflow__ArcWorkflow_ToCreateContract_6FCE9E49(this: ArcWorkflow, WithFolder: bool | None=None) -> Array[Contract]:
    with_folder: bool = default_arg(WithFolder, False)
    path: str = Workflow_fileNameFromIdentifier(this.Identifier)
    c: Contract = Contract.create_create(path, DTOType(2), DTO(0, ARCtrl_ArcWorkflow__ArcWorkflow_toFsWorkbook_Static_Z1C75CB0E(this)))
    def _arrow3741(__unit: None=None, this: Any=this, WithFolder: Any=WithFolder) -> IEnumerable_1[Contract]:
        def _arrow3737(__unit: None=None) -> IEnumerable_1[Contract]:
            folder_fs: FileSystemTree = FileSystemTree.create_workflows_folder([FileSystemTree.create_workflow_folder(this.Identifier)])
            def _arrow3736(p: str) -> IEnumerable_1[Contract]:
                return singleton(Contract.create_create(p, DTOType(10))) if ((p != "workflows/.gitkeep") if (p != path) else False) else empty()

            return collect(_arrow3736, folder_fs.ToFilePaths(False))

        def _arrow3740(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow3738(__unit: None=None) -> IEnumerable_1[Contract]:
                path_1: str = Workflow_cwlFileNameFromIdentifier(this.Identifier)
                dto: str = encode_processing_unit(value(this.CWLDescription))
                return singleton(Contract.create_create(path_1, DTOType(8), DTO(1, dto)))

            def _arrow3739(__unit: None=None) -> IEnumerable_1[Contract]:
                return singleton(c)

            return append(_arrow3738() if (this.CWLDescription is not None) else empty(), delay(_arrow3739))

        return append(_arrow3737() if with_folder else empty(), delay(_arrow3740))

    return to_array(delay(_arrow3741))


def ARCtrl_ArcWorkflow__ArcWorkflow_ToUpdateContract(this: ArcWorkflow) -> Contract:
    path: str = Workflow_fileNameFromIdentifier(this.Identifier)
    return Contract.create_update(path, DTOType(2), DTO(0, ARCtrl_ArcWorkflow__ArcWorkflow_toFsWorkbook_Static_Z1C75CB0E(this)))


def ARCtrl_ArcWorkflow__ArcWorkflow_ToDeleteContract(this: ArcWorkflow) -> Contract:
    path: str = get_workflow_folder_path(this.Identifier)
    return Contract.create_delete(path)


def ARCtrl_ArcWorkflow__ArcWorkflow_toDeleteContract_Static_Z1C75CB0E(workflow: ArcWorkflow) -> Contract:
    return ARCtrl_ArcWorkflow__ArcWorkflow_ToDeleteContract(workflow)


def ARCtrl_ArcWorkflow__ArcWorkflow_toCreateContract_Static_3B1E4D7B(workflow: ArcWorkflow, WithFolder: bool | None=None) -> Array[Contract]:
    return ARCtrl_ArcWorkflow__ArcWorkflow_ToCreateContract_6FCE9E49(workflow, WithFolder)


def ARCtrl_ArcWorkflow__ArcWorkflow_toUpdateContract_Static_Z1C75CB0E(workflow: ArcWorkflow) -> Contract:
    return ARCtrl_ArcWorkflow__ArcWorkflow_ToUpdateContract(workflow)


def ARCtrl_ArcWorkflow__ArcWorkflow_tryFromReadContract_Static_7570923F(c: Contract) -> ArcWorkflow | None:
    (pattern_matching_result, fsworkbook) = (None, None)
    if c.Operation == "READ":
        if c.DTOType is not None:
            if c.DTOType.tag == 2:
                if c.DTO is not None:
                    if c.DTO.tag == 0:
                        pattern_matching_result = 0
                        fsworkbook = c.DTO.fields[0]

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
        return ARCtrl_ArcWorkflow__ArcWorkflow_fromFsWorkbook_Static_32154C9D(fsworkbook)

    elif pattern_matching_result == 1:
        return None



def ARCtrl_ArcWorkflow__ArcWorkflow_tryCWLFromReadContract_Static(workflow_identifier: str, c: Contract) -> CWLProcessingUnit | None:
    p: str = Workflow_cwlFileNameFromIdentifier(workflow_identifier)
    (pattern_matching_result, cwl_1) = (None, None)
    if c.Operation == "READ":
        if c.DTOType is not None:
            if c.DTOType.tag == 8:
                if c.DTO is not None:
                    if c.DTO.tag == 1:
                        def _arrow3742(__unit: None=None, workflow_identifier: Any=workflow_identifier, c: Any=c) -> bool:
                            cwl: str = c.DTO.fields[0]
                            return c.Path == p

                        if _arrow3742():
                            pattern_matching_result = 0
                            cwl_1 = c.DTO.fields[0]

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
        return Decode_decodeCWLProcessingUnit(cwl_1)

    elif pattern_matching_result == 1:
        return None



__all__ = ["_007CWorkflowPath_007C__007C", "_007CWorkflowCWLPath_007C__007C", "ARCtrl_ArcWorkflow__ArcWorkflow_ToCreateContract_6FCE9E49", "ARCtrl_ArcWorkflow__ArcWorkflow_ToUpdateContract", "ARCtrl_ArcWorkflow__ArcWorkflow_ToDeleteContract", "ARCtrl_ArcWorkflow__ArcWorkflow_toDeleteContract_Static_Z1C75CB0E", "ARCtrl_ArcWorkflow__ArcWorkflow_toCreateContract_Static_3B1E4D7B", "ARCtrl_ArcWorkflow__ArcWorkflow_toUpdateContract_Static_Z1C75CB0E", "ARCtrl_ArcWorkflow__ArcWorkflow_tryFromReadContract_Static_7570923F", "ARCtrl_ArcWorkflow__ArcWorkflow_tryCWLFromReadContract_Static"]

