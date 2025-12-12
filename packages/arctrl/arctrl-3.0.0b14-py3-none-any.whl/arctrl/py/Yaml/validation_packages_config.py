from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.seq import (to_list, delay, collect, singleton)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (equals, IEnumerable_1)
from ..fable_modules.yamlicious.yamlicious_types import YAMLContent_create_27AED5E3
from ..fable_modules.yamlicious.decode import (object, IRequiredGetter, resizearray as resizearray_1, IOptionalGetter, string as string_1, IGetters)
from ..fable_modules.yamlicious.encode import (try_include, string, resizearray)
from ..fable_modules.yamlicious.reader import read
from ..fable_modules.yamlicious.writer import write
from ..fable_modules.yamlicious.yamlicious_types import (YAMLElement, Config)
from ..ValidationPackages.validation_package import ValidationPackage
from ..ValidationPackages.validation_packages_config import ValidationPackagesConfig
from .encode import default_whitespace
from .validation_package import (ValidationPackage_encoder, ValidationPackage_decoder)

def ValidationPackagesConfig_encoder(validationpackage: ValidationPackagesConfig) -> YAMLElement:
    def chooser(tupled_arg: tuple[str, YAMLElement], validationpackage: Any=validationpackage) -> tuple[str, YAMLElement] | None:
        v: YAMLElement = tupled_arg[1]
        if equals(v, YAMLElement(5)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow3546(value: str, validationpackage: Any=validationpackage) -> YAMLElement:
        return string(value)

    def _arrow3547(validationpackage_1: ValidationPackage, validationpackage: Any=validationpackage) -> YAMLElement:
        return ValidationPackage_encoder(validationpackage_1)

    obj_seq: FSharpList[tuple[str, YAMLElement]] = choose(chooser, of_array([try_include("arc_specification", _arrow3546, validationpackage.ARCSpecification), ("validation_packages", resizearray(_arrow3547, validationpackage.ValidationPackages))]))
    def _arrow3549(__unit: None=None, validationpackage: Any=validationpackage) -> IEnumerable_1[YAMLElement]:
        def _arrow3548(match_value: tuple[str, YAMLElement]) -> IEnumerable_1[YAMLElement]:
            return singleton(YAMLElement(0, YAMLContent_create_27AED5E3(match_value[0]), match_value[1]))

        return collect(_arrow3548, obj_seq)

    return YAMLElement(3, to_list(delay(_arrow3549)))


def _arrow3552(value_2: YAMLElement) -> ValidationPackagesConfig:
    def getter(get: IGetters) -> ValidationPackagesConfig:
        def _arrow3550(__unit: None=None, get: Any=get) -> Array[ValidationPackage]:
            object_arg: IRequiredGetter = get.Required
            def arg_1(value: YAMLElement) -> Array[ValidationPackage]:
                return resizearray_1(ValidationPackage_decoder, value)

            return object_arg.Field("validation_packages", arg_1)

        def _arrow3551(__unit: None=None, get: Any=get) -> str | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("arc_specification", string_1)

        return ValidationPackagesConfig(_arrow3550(), _arrow3551())

    return object(getter, value_2)


ValidationPackagesConfig_decoder: Callable[[YAMLElement], ValidationPackagesConfig] = _arrow3552

def ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_fromYamlString_Static_Z721C83C5(s: str) -> ValidationPackagesConfig:
    return ValidationPackagesConfig_decoder(read(s))


def ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toYamlString_Static_71136F3F(whitespace: int | None=None) -> Callable[[ValidationPackagesConfig], str]:
    def _arrow3554(vp: ValidationPackagesConfig, whitespace: Any=whitespace) -> str:
        element: YAMLElement = ValidationPackagesConfig_encoder(vp)
        whitespace_1: int = default_whitespace(whitespace) or 0
        def _arrow3553(c: Config) -> Config:
            return Config(whitespace_1, c.Level)

        return write(element, _arrow3553)

    return _arrow3554


def ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toYamlString_71136F3F(this: ValidationPackagesConfig, whitespace: int | None=None) -> str:
    return ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toYamlString_Static_71136F3F(whitespace)(this)


__all__ = ["ValidationPackagesConfig_encoder", "ValidationPackagesConfig_decoder", "ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_fromYamlString_Static_Z721C83C5", "ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toYamlString_Static_71136F3F", "ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toYamlString_71136F3F"]

