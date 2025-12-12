from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.array_ import equals_with
from ..fable_modules.fable_library.list import contains
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import string_hash
from ..FileSystem.path import alternative_licensefile_names
from .contract import (Contract, DTOType, DTO)

def LicenseContractExtensions__007CLicensePath_007C__007C(input: Array[str]) -> str | None:
    (pattern_matching_result,) = (None,)
    def _arrow3721(x: str, y: str, input: Any=input) -> bool:
        return x == y

    if (len(input) == 1) if (not equals_with(_arrow3721, input, None)) else False:
        if input[0] == "LICENSE":
            pattern_matching_result = 0

        else: 
            class ObjectExpr3723:
                @property
                def Equals(self) -> Callable[[str, str], bool]:
                    def _arrow3722(x_1: str, y_1: str) -> bool:
                        return x_1 == y_1

                    return _arrow3722

                @property
                def GetHashCode(self) -> Callable[[str], int]:
                    return string_hash

            if contains(input[0], alternative_licensefile_names, ObjectExpr3723()):
                pattern_matching_result = 1

            else: 
                pattern_matching_result = 2



    else: 
        pattern_matching_result = 2

    if pattern_matching_result == 0:
        return "LICENSE"

    elif pattern_matching_result == 1:
        return input[0]

    elif pattern_matching_result == 2:
        return None



License_defaultLicenseContract: Contract = Contract.create_create("LICENSE", DTOType(10), DTO(1, "ALL RIGHTS RESERVED BY THE AUTHORS"))

__all__ = ["LicenseContractExtensions__007CLicensePath_007C__007C", "License_defaultLicenseContract"]

