from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.array_ import equals_with
from ..fable_modules.fable_library.list import FSharpList
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.seq import (to_array, delay, append, collect, singleton, empty)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..Core.arc_types import (ArcStudy, ArcAssay)
from ..Core.Helper.identifier import Study_fileNameFromIdentifier
from ..FileSystem.file_system_tree import FileSystemTree
from ..FileSystem.path import (combine_many, get_study_folder_path)
from ..Spreadsheet.arc_study import (ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522, ARCtrl_ArcStudy__ArcStudy_fromFsWorkbook_Static_32154C9D)
from .contract import (Contract, DTOType, DTO)

def _007CStudyPath_007C__007C(input: Array[str]) -> str | None:
    (pattern_matching_result,) = (None,)
    def _arrow3729(x: str, y: str, input: Any=input) -> bool:
        return x == y

    if (len(input) == 3) if (not equals_with(_arrow3729, input, None)) else False:
        if input[0] == "studies":
            if input[2] == "isa.study.xlsx":
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        any_study_name: str = input[1]
        return combine_many(input)

    elif pattern_matching_result == 1:
        return None



def ARCtrl_ArcStudy__ArcStudy_ToCreateContract_6FCE9E49(this: ArcStudy, WithFolder: bool | None=None) -> Array[Contract]:
    with_folder: bool = default_arg(WithFolder, False)
    path: str = Study_fileNameFromIdentifier(this.Identifier)
    c: Contract = Contract.create_create(path, DTOType(1), DTO(0, ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522(this)))
    def _arrow3733(__unit: None=None, this: Any=this, WithFolder: Any=WithFolder) -> IEnumerable_1[Contract]:
        def _arrow3731(__unit: None=None) -> IEnumerable_1[Contract]:
            folder_fs: FileSystemTree = FileSystemTree.create_studies_folder([FileSystemTree.create_study_folder(this.Identifier)])
            def _arrow3730(p: str) -> IEnumerable_1[Contract]:
                return singleton(Contract.create_create(p, DTOType(10))) if ((p != "studies/.gitkeep") if (p != path) else False) else empty()

            return collect(_arrow3730, folder_fs.ToFilePaths(False))

        def _arrow3732(__unit: None=None) -> IEnumerable_1[Contract]:
            return singleton(c)

        return append(_arrow3731() if with_folder else empty(), delay(_arrow3732))

    return to_array(delay(_arrow3733))


def ARCtrl_ArcStudy__ArcStudy_ToUpdateContract(this: ArcStudy) -> Contract:
    path: str = Study_fileNameFromIdentifier(this.Identifier)
    return Contract.create_update(path, DTOType(1), DTO(0, ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522(this)))


def ARCtrl_ArcStudy__ArcStudy_ToDeleteContract(this: ArcStudy) -> Contract:
    path: str = get_study_folder_path(this.Identifier)
    return Contract.create_delete(path)


def ARCtrl_ArcStudy__ArcStudy_toDeleteContract_Static_1680536E(study: ArcStudy) -> Contract:
    return ARCtrl_ArcStudy__ArcStudy_ToDeleteContract(study)


def ARCtrl_ArcStudy__ArcStudy_toCreateContract_Static_Z76BBA099(study: ArcStudy, WithFolder: bool | None=None) -> Array[Contract]:
    return ARCtrl_ArcStudy__ArcStudy_ToCreateContract_6FCE9E49(study, WithFolder)


def ARCtrl_ArcStudy__ArcStudy_toUpdateContract_Static_1680536E(study: ArcStudy) -> Contract:
    return ARCtrl_ArcStudy__ArcStudy_ToUpdateContract(study)


def ARCtrl_ArcStudy__ArcStudy_tryFromReadContract_Static_7570923F(c: Contract) -> tuple[ArcStudy, FSharpList[ArcAssay]] | None:
    (pattern_matching_result, fsworkbook) = (None, None)
    if c.Operation == "READ":
        if c.DTOType is not None:
            if c.DTOType.tag == 1:
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
        return ARCtrl_ArcStudy__ArcStudy_fromFsWorkbook_Static_32154C9D(fsworkbook)

    elif pattern_matching_result == 1:
        return None



__all__ = ["_007CStudyPath_007C__007C", "ARCtrl_ArcStudy__ArcStudy_ToCreateContract_6FCE9E49", "ARCtrl_ArcStudy__ArcStudy_ToUpdateContract", "ARCtrl_ArcStudy__ArcStudy_ToDeleteContract", "ARCtrl_ArcStudy__ArcStudy_toDeleteContract_Static_1680536E", "ARCtrl_ArcStudy__ArcStudy_toCreateContract_Static_Z76BBA099", "ARCtrl_ArcStudy__ArcStudy_toUpdateContract_Static_1680536E", "ARCtrl_ArcStudy__ArcStudy_tryFromReadContract_Static_7570923F"]

