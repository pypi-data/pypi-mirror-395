from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.array_ import equals_with
from ..fable_modules.fable_library.types import Array
from ..Core.arc_types import ArcInvestigation
from ..FileSystem.path import combine_many
from ..Spreadsheet.arc_investigation import (ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF, ARCtrl_ArcInvestigation__ArcInvestigation_fromFsWorkbook_Static_32154C9D)
from .contract import (Contract, DTOType, DTO)

def _007CInvestigationPath_007C__007C(input: Array[str]) -> str | None:
    (pattern_matching_result,) = (None,)
    def _arrow3754(x: str, y: str, input: Any=input) -> bool:
        return x == y

    if (len(input) == 1) if (not equals_with(_arrow3754, input, None)) else False:
        if input[0] == "isa.investigation.xlsx":
            pattern_matching_result = 0

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        return combine_many(input)

    elif pattern_matching_result == 1:
        return None



def ARCtrl_ArcInvestigation__ArcInvestigation_ToCreateContract(this: ArcInvestigation) -> Contract:
    return Contract.create_create("isa.investigation.xlsx", DTOType(4), DTO(0, ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF(this)))


def ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract(this: ArcInvestigation) -> Contract:
    return Contract.create_update("isa.investigation.xlsx", DTOType(4), DTO(0, ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF(this)))


def ARCtrl_ArcInvestigation__ArcInvestigation_toCreateContract_Static_Z720BD3FF(inv: ArcInvestigation) -> Contract:
    return ARCtrl_ArcInvestigation__ArcInvestigation_ToCreateContract(inv)


def ARCtrl_ArcInvestigation__ArcInvestigation_toUpdateContract_Static_Z720BD3FF(inv: ArcInvestigation) -> Contract:
    return ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract(inv)


def ARCtrl_ArcInvestigation__ArcInvestigation_tryFromReadContract_Static_7570923F(c: Contract) -> ArcInvestigation | None:
    (pattern_matching_result, fsworkbook) = (None, None)
    if c.Operation == "READ":
        if c.DTOType is not None:
            if c.DTOType.tag == 4:
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
        return ARCtrl_ArcInvestigation__ArcInvestigation_fromFsWorkbook_Static_32154C9D(fsworkbook)

    elif pattern_matching_result == 1:
        return None



__all__ = ["_007CInvestigationPath_007C__007C", "ARCtrl_ArcInvestigation__ArcInvestigation_ToCreateContract", "ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract", "ARCtrl_ArcInvestigation__ArcInvestigation_toCreateContract_Static_Z720BD3FF", "ARCtrl_ArcInvestigation__ArcInvestigation_toUpdateContract_Static_Z720BD3FF", "ARCtrl_ArcInvestigation__ArcInvestigation_tryFromReadContract_Static_7570923F"]

