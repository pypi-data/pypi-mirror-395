from __future__ import annotations
from ..fable_modules.fable_library.types import Array
from ..FileSystem.path import split as split_1
from .arc_assay import _007CAssayPath_007C__007C
from .arc_investigation import _007CInvestigationPath_007C__007C
from .arc_run import (_007CRunPath_007C__007C, _007CRunCWLPath_007C__007C, _007CRunYMLPath_007C__007C)
from .arc_study import _007CStudyPath_007C__007C
from .arc_workflow import (_007CWorkflowPath_007C__007C, _007CWorkflowCWLPath_007C__007C)
from .contract import (Contract, DTOType)
from .datamap import _007CDatamapPath_007C__007C
from .license import LicenseContractExtensions__007CLicensePath_007C__007C

def try_isaread_contract_from_path(path: str) -> Contract | None:
    split: Array[str] = split_1(path)
    active_pattern_result: str | None = _007CInvestigationPath_007C__007C(split)
    if active_pattern_result is not None:
        p: str = active_pattern_result
        return Contract.create_read(p, DTOType(4))

    else: 
        active_pattern_result_1: str | None = _007CAssayPath_007C__007C(split)
        if active_pattern_result_1 is not None:
            p_1: str = active_pattern_result_1
            return Contract.create_read(p_1, DTOType(0))

        else: 
            active_pattern_result_2: str | None = _007CStudyPath_007C__007C(split)
            if active_pattern_result_2 is not None:
                p_2: str = active_pattern_result_2
                return Contract.create_read(p_2, DTOType(1))

            else: 
                active_pattern_result_3: str | None = _007CWorkflowPath_007C__007C(split)
                if active_pattern_result_3 is not None:
                    p_3: str = active_pattern_result_3
                    return Contract.create_read(p_3, DTOType(2))

                else: 
                    active_pattern_result_4: str | None = _007CWorkflowCWLPath_007C__007C(split)
                    if active_pattern_result_4 is not None:
                        p_4: str = active_pattern_result_4
                        return Contract.create_read(p_4, DTOType(8))

                    else: 
                        active_pattern_result_5: str | None = _007CRunPath_007C__007C(split)
                        if active_pattern_result_5 is not None:
                            p_5: str = active_pattern_result_5
                            return Contract.create_read(p_5, DTOType(3))

                        else: 
                            active_pattern_result_6: str | None = _007CRunCWLPath_007C__007C(split)
                            if active_pattern_result_6 is not None:
                                p_6: str = active_pattern_result_6
                                return Contract.create_read(p_6, DTOType(8))

                            else: 
                                active_pattern_result_7: str | None = _007CRunYMLPath_007C__007C(split)
                                if active_pattern_result_7 is not None:
                                    p_7: str = active_pattern_result_7
                                    return Contract.create_read(p_7, DTOType(9))

                                else: 
                                    active_pattern_result_8: str | None = _007CDatamapPath_007C__007C(split)
                                    if active_pattern_result_8 is not None:
                                        p_8: str = active_pattern_result_8
                                        return Contract.create_read(p_8, DTOType(5))

                                    else: 
                                        active_pattern_result_9: str | None = LicenseContractExtensions__007CLicensePath_007C__007C(split)
                                        if active_pattern_result_9 is not None:
                                            p_9: str = active_pattern_result_9
                                            return Contract.create_read(p_9, DTOType(10))

                                        else: 
                                            return None












__all__ = ["try_isaread_contract_from_path"]

