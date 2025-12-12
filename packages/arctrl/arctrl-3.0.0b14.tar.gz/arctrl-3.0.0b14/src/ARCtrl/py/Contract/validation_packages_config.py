from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.array_ import equals_with
from ..fable_modules.fable_library.types import Array
from ..FileSystem.path import combine_many
from ..ValidationPackages.validation_packages_config import ValidationPackagesConfig
from ..Yaml.validation_packages_config import (ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toYamlString_Static_71136F3F, ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_fromYamlString_Static_Z721C83C5)
from .contract import (DTOType as DTOType_1, Contract, DTO)

ValidationPackagesConfigHelper_ConfigFilePath: str = combine_many([".arc", "validation_packages.yml"])

ValidationPackagesConfigHelper_ReadContract: Contract = Contract("READ", ValidationPackagesConfigHelper_ConfigFilePath, DTOType_1(9), None)

def ValidationPackagesConfigExtensions__007CValidationPackagesYamlPath_007C__007C(input: Array[str]) -> str | None:
    (pattern_matching_result,) = (None,)
    def _arrow3706(x: str, y: str, input: Any=input) -> bool:
        return x == y

    if (len(input) == 2) if (not equals_with(_arrow3706, input, None)) else False:
        if input[0] == ".arc":
            if input[1] == "validation_packages.yml":
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        return combine_many(input)

    elif pattern_matching_result == 1:
        return None



def ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_ToCreateContract(this: ValidationPackagesConfig) -> Contract:
    return Contract.create_create(ValidationPackagesConfigHelper_ConfigFilePath, DTOType_1(9), DTO(1, ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toYamlString_Static_71136F3F()(this)))


def ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_ToDeleteContract(this: ValidationPackagesConfig) -> Contract:
    return Contract.create_delete(ValidationPackagesConfigHelper_ConfigFilePath)


def ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toDeleteContract_Static_724DAE55(config: ValidationPackagesConfig) -> Contract:
    return ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_ToDeleteContract(config)


def ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toCreateContract_Static_724DAE55(config: ValidationPackagesConfig) -> Contract:
    return ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_ToCreateContract(config)


def ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_tryFromReadContract_Static_7570923F(c: Contract) -> ValidationPackagesConfig | None:
    (pattern_matching_result, p_1, yaml_1) = (None, None, None)
    if c.Operation == "READ":
        if c.DTOType is not None:
            if c.DTOType.tag == 9:
                if c.DTO is not None:
                    if c.DTO.tag == 1:
                        def _arrow3707(__unit: None=None, c: Any=c) -> bool:
                            yaml: str = c.DTO.fields[0]
                            return c.Path == ValidationPackagesConfigHelper_ConfigFilePath

                        if _arrow3707():
                            pattern_matching_result = 0
                            p_1 = c.Path
                            yaml_1 = c.DTO.fields[0]

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
        return ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_fromYamlString_Static_Z721C83C5(yaml_1)

    elif pattern_matching_result == 1:
        return None



__all__ = ["ValidationPackagesConfigHelper_ConfigFilePath", "ValidationPackagesConfigHelper_ReadContract", "ValidationPackagesConfigExtensions__007CValidationPackagesYamlPath_007C__007C", "ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_ToCreateContract", "ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_ToDeleteContract", "ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toDeleteContract_Static_724DAE55", "ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toCreateContract_Static_724DAE55", "ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_tryFromReadContract_Static_7570923F"]

