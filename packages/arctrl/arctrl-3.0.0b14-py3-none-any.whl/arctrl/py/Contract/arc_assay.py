from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.array_ import equals_with
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.seq import (to_array, delay, append, collect, singleton, empty)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..Core.arc_types import ArcAssay
from ..Core.Helper.identifier import Assay_fileNameFromIdentifier
from ..FileSystem.file_system_tree import FileSystemTree
from ..FileSystem.path import (combine_many, get_assay_folder_path)
from ..Spreadsheet.arc_assay import (ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F, ARCtrl_ArcAssay__ArcAssay_fromFsWorkbook_Static_32154C9D)
from .contract import (Contract, DTOType, DTO)

def _007CAssayPath_007C__007C(input: Array[str]) -> str | None:
    (pattern_matching_result,) = (None,)
    def _arrow3724(x: str, y: str, input: Any=input) -> bool:
        return x == y

    if (len(input) == 3) if (not equals_with(_arrow3724, input, None)) else False:
        if input[0] == "assays":
            if input[2] == "isa.assay.xlsx":
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        any_assay_name: str = input[1]
        return combine_many(input)

    elif pattern_matching_result == 1:
        return None



def ARCtrl_ArcAssay__ArcAssay_ToCreateContract_6FCE9E49(this: ArcAssay, WithFolder: bool | None=None) -> Array[Contract]:
    with_folder: bool = default_arg(WithFolder, False)
    path: str = Assay_fileNameFromIdentifier(this.Identifier)
    c: Contract = Contract.create_create(path, DTOType(0), DTO(0, ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F(this)))
    def _arrow3728(__unit: None=None, this: Any=this, WithFolder: Any=WithFolder) -> IEnumerable_1[Contract]:
        def _arrow3726(__unit: None=None) -> IEnumerable_1[Contract]:
            folder_fs: FileSystemTree = FileSystemTree.create_assays_folder([FileSystemTree.create_assay_folder(this.Identifier)])
            def _arrow3725(p: str) -> IEnumerable_1[Contract]:
                return singleton(Contract.create_create(p, DTOType(10))) if ((p != "assays/.gitkeep") if (p != path) else False) else empty()

            return collect(_arrow3725, folder_fs.ToFilePaths(False))

        def _arrow3727(__unit: None=None) -> IEnumerable_1[Contract]:
            return singleton(c)

        return append(_arrow3726() if with_folder else empty(), delay(_arrow3727))

    return to_array(delay(_arrow3728))


def ARCtrl_ArcAssay__ArcAssay_ToUpdateContract(this: ArcAssay) -> Contract:
    path: str = Assay_fileNameFromIdentifier(this.Identifier)
    return Contract.create_update(path, DTOType(0), DTO(0, ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F(this)))


def ARCtrl_ArcAssay__ArcAssay_ToDeleteContract(this: ArcAssay) -> Contract:
    path: str = get_assay_folder_path(this.Identifier)
    return Contract.create_delete(path)


def ARCtrl_ArcAssay__ArcAssay_toDeleteContract_Static_1501C0F8(assay: ArcAssay) -> Contract:
    return ARCtrl_ArcAssay__ArcAssay_ToDeleteContract(assay)


def ARCtrl_ArcAssay__ArcAssay_toCreateContract_Static_Z2508BE4F(assay: ArcAssay, WithFolder: bool | None=None) -> Array[Contract]:
    return ARCtrl_ArcAssay__ArcAssay_ToCreateContract_6FCE9E49(assay, WithFolder)


def ARCtrl_ArcAssay__ArcAssay_toUpdateContract_Static_1501C0F8(assay: ArcAssay) -> Contract:
    return ARCtrl_ArcAssay__ArcAssay_ToUpdateContract(assay)


def ARCtrl_ArcAssay__ArcAssay_tryFromReadContract_Static_7570923F(c: Contract) -> ArcAssay | None:
    (pattern_matching_result, fsworkbook) = (None, None)
    if c.Operation == "READ":
        if c.DTOType is not None:
            if c.DTOType.tag == 0:
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
        return ARCtrl_ArcAssay__ArcAssay_fromFsWorkbook_Static_32154C9D(fsworkbook)

    elif pattern_matching_result == 1:
        return None



__all__ = ["_007CAssayPath_007C__007C", "ARCtrl_ArcAssay__ArcAssay_ToCreateContract_6FCE9E49", "ARCtrl_ArcAssay__ArcAssay_ToUpdateContract", "ARCtrl_ArcAssay__ArcAssay_ToDeleteContract", "ARCtrl_ArcAssay__ArcAssay_toDeleteContract_Static_1501C0F8", "ARCtrl_ArcAssay__ArcAssay_toCreateContract_Static_Z2508BE4F", "ARCtrl_ArcAssay__ArcAssay_toUpdateContract_Static_1501C0F8", "ARCtrl_ArcAssay__ArcAssay_tryFromReadContract_Static_7570923F"]

