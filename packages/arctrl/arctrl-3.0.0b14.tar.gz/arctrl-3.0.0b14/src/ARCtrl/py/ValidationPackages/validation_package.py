from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.option import value as value_1
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.seq import (to_list, delay, append, singleton, empty)
from ..fable_modules.fable_library.string_ import join
from ..fable_modules.fable_library.util import (IEnumerable_1, equals, string_hash)
from ..Core.Helper.hash_codes import (box_hash_array, box_hash_option)

def _expr3526() -> TypeInfo:
    return class_type("ARCtrl.ValidationPackages.ValidationPackage", None, ValidationPackage)


class ValidationPackage:
    def __init__(self, name: str, version: str | None=None) -> None:
        self.version: str | None = version
        self._name: str = name
        self._version: str | None = self.version

    @property
    def Name(self, __unit: None=None) -> str:
        this: ValidationPackage = self
        return this._name

    @Name.setter
    def Name(self, name: str) -> None:
        this: ValidationPackage = self
        this._name = name

    @property
    def Version(self, __unit: None=None) -> str | None:
        this: ValidationPackage = self
        return this._version

    @Version.setter
    def Version(self, version: str | None=None) -> None:
        this: ValidationPackage = self
        this._version = version

    @staticmethod
    def make(name: str, version: str | None=None) -> ValidationPackage:
        return ValidationPackage(name, version)

    def Copy(self, __unit: None=None) -> ValidationPackage:
        this: ValidationPackage = self
        name: str = this.Name
        version: str | None = this.Version
        return ValidationPackage.make(name, version)

    def __str__(self, __unit: None=None) -> str:
        this: ValidationPackage = self
        def _arrow3525(__unit: None=None) -> IEnumerable_1[str]:
            def _arrow3524(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow3523(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow3522(__unit: None=None) -> IEnumerable_1[str]:
                        return singleton("}")

                    return append(singleton((" Version = " + value_1(this.Version)) + "") if (this.version is not None) else empty(), delay(_arrow3522))

                return append(singleton((" Name = " + this.Name) + ""), delay(_arrow3523))

            return append(singleton("{"), delay(_arrow3524))

        return join("\n", to_list(delay(_arrow3525)))

    def __eq__(self, obj: Any=None) -> bool:
        this: ValidationPackage = self
        return (equals(obj.Version, this.Version) if (obj.Name == this.Name) else False) if isinstance(obj, ValidationPackage) else False

    def __hash__(self, __unit: None=None) -> Any:
        this: ValidationPackage = self
        return box_hash_array([string_hash(this.Name), box_hash_option(this.Version)])


ValidationPackage_reflection = _expr3526

def ValidationPackage__ctor_27AED5E3(name: str, version: str | None=None) -> ValidationPackage:
    return ValidationPackage(name, version)


__all__ = ["ValidationPackage_reflection"]

