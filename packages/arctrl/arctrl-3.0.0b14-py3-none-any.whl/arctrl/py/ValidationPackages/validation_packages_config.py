from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.array_ import sort_by
from ..fable_modules.fable_library.option import value
from ..fable_modules.fable_library.range import range_big_int
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.seq import (to_list, delay, append, singleton, empty, map, length, fold, item)
from ..fable_modules.fable_library.string_ import join
from ..fable_modules.fable_library.types import (Array, to_string)
from ..fable_modules.fable_library.util import (IEnumerable_1, compare_arrays, equals)
from ..Core.Helper.hash_codes import (box_hash_array, box_hash_option, box_hash_seq)
from .validation_package import ValidationPackage

def _expr3536() -> TypeInfo:
    return class_type("ARCtrl.ValidationPackages.ValidationPackagesConfig", None, ValidationPackagesConfig)


class ValidationPackagesConfig:
    def __init__(self, validation_packages: Array[ValidationPackage], arc_specification: str | None=None) -> None:
        self._arc_specification: str | None = arc_specification
        self._validation_packages: Array[ValidationPackage] = validation_packages

    @property
    def ValidationPackages(self, __unit: None=None) -> Array[ValidationPackage]:
        this: ValidationPackagesConfig = self
        return this._validation_packages

    @ValidationPackages.setter
    def ValidationPackages(self, validation_packages: Array[ValidationPackage]) -> None:
        this: ValidationPackagesConfig = self
        this._validation_packages = validation_packages

    @property
    def ARCSpecification(self, __unit: None=None) -> str | None:
        this: ValidationPackagesConfig = self
        return this._arc_specification

    @ARCSpecification.setter
    def ARCSpecification(self, arc_specification: str | None=None) -> None:
        this: ValidationPackagesConfig = self
        this._arc_specification = arc_specification

    @staticmethod
    def make(validation_packages: Array[ValidationPackage], arc_specification: str | None=None) -> ValidationPackagesConfig:
        return ValidationPackagesConfig(validation_packages, arc_specification)

    def Copy(self, __unit: None=None) -> ValidationPackagesConfig:
        this: ValidationPackagesConfig = self
        validation_packages: Array[ValidationPackage] = this.ValidationPackages
        arc_specification: str | None = this.ARCSpecification
        return ValidationPackagesConfig.make(validation_packages, arc_specification)

    def __str__(self, __unit: None=None) -> str:
        this: ValidationPackagesConfig = self
        def _arrow3532(__unit: None=None) -> IEnumerable_1[str]:
            def _arrow3531(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow3530(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow3529(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow3528(__unit: None=None) -> IEnumerable_1[str]:
                            def _arrow3527(__unit: None=None) -> IEnumerable_1[str]:
                                return singleton("}")

                            return append(singleton("]"), delay(_arrow3527))

                        return append(singleton(join((";" + "\n") + "", map(to_string, this.ValidationPackages))), delay(_arrow3528))

                    return append(singleton(" ValidationPackages = ["), delay(_arrow3529))

                return append(singleton((" ARCSpecification = " + value(this.ARCSpecification)) + "") if (this.ARCSpecification is not None) else empty(), delay(_arrow3530))

            return append(singleton("{"), delay(_arrow3531))

        return join("\n", to_list(delay(_arrow3532)))

    def StructurallyEquals(self, other: ValidationPackagesConfig) -> bool:
        this: ValidationPackagesConfig = self
        def sort(arg: Array[ValidationPackage]) -> Array[ValidationPackage]:
            def projection(vp: ValidationPackage, arg: Any=arg) -> tuple[str, str | None]:
                return (vp.Name, vp.Version)

            class ObjectExpr3533:
                @property
                def Compare(self) -> Callable[[tuple[str, str | None], tuple[str, str | None]], int]:
                    return compare_arrays

            return sort_by(projection, list(arg), ObjectExpr3533())

        if equals(this.ARCSpecification, other.ARCSpecification):
            a: IEnumerable_1[ValidationPackage] = sort(this.ValidationPackages)
            b: IEnumerable_1[ValidationPackage] = sort(other.ValidationPackages)
            def folder(acc: bool, e: bool) -> bool:
                if acc:
                    return e

                else: 
                    return False


            def _arrow3535(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow3534(i: int) -> bool:
                    return equals(item(i, a), item(i, b))

                return map(_arrow3534, range_big_int(0, 1, length(a) - 1))

            return fold(folder, True, to_list(delay(_arrow3535))) if (length(a) == length(b)) else False

        else: 
            return False


    def ReferenceEquals(self, other: ValidationPackagesConfig) -> bool:
        this: ValidationPackagesConfig = self
        return this is other

    def __eq__(self, other: Any=None) -> bool:
        this: ValidationPackagesConfig = self
        return this.StructurallyEquals(other) if isinstance(other, ValidationPackagesConfig) else False

    def __hash__(self, __unit: None=None) -> Any:
        this: ValidationPackagesConfig = self
        return box_hash_array([box_hash_option(this.ARCSpecification), box_hash_seq(this.ValidationPackages)])


ValidationPackagesConfig_reflection = _expr3536

def ValidationPackagesConfig__ctor_376974AD(validation_packages: Array[ValidationPackage], arc_specification: str | None=None) -> ValidationPackagesConfig:
    return ValidationPackagesConfig(validation_packages, arc_specification)


__all__ = ["ValidationPackagesConfig_reflection"]

