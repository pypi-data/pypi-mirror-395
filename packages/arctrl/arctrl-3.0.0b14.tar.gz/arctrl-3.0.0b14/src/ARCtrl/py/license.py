from __future__ import annotations
from collections.abc import Callable
from typing import Any
from .Contract.contract import (Contract, DTOType, DTO)
from .Core.Helper.hash_codes import box_hash_array
from .FileSystem.path import alternative_licensefile_names
from .fable_modules.fable_library.reflection import (TypeInfo, class_type)
from .fable_modules.fable_library.seq import (contains, for_all)
from .fable_modules.fable_library.types import Array
from .fable_modules.fable_library.util import (string_hash, to_enumerable)

def _expr3769() -> TypeInfo:
    return class_type("ARCtrl.License", None, License)


class License:
    def __init__(self, content_type: str, content: str, path: str | None=None) -> None:
        self._type: str = content_type
        self._content: str = content
        self._staticHash: int = 0
        self._path: str = "LICENSE" if (path is None) else path

    @property
    def Type(self, __unit: None=None) -> str:
        this: License = self
        return this._type

    @Type.setter
    def Type(self, h: str) -> None:
        this: License = self
        this._type = h

    @property
    def Content(self, __unit: None=None) -> str:
        this: License = self
        return this._content

    @Content.setter
    def Content(self, h: str) -> None:
        this: License = self
        this._content = h

    @property
    def StaticHash(self, __unit: None=None) -> int:
        this: License = self
        return this._staticHash

    @StaticHash.setter
    def StaticHash(self, h: int) -> None:
        this: License = self
        this._staticHash = h or 0

    @property
    def Path(self, __unit: None=None) -> str:
        this: License = self
        return this._path

    @Path.setter
    def Path(self, p: str) -> None:
        this: License = self
        this._path = p

    @staticmethod
    def init_fulltext(content: str, path: str | None=None) -> License:
        return License("fulltext", content, path)

    def ToCreateContract(self, __unit: None=None) -> Contract:
        this: License = self
        match_value: str = this.Type
        return Contract.create_create(this._path, DTOType(10), DTO(1, this.Content))

    def ToUpdateContract(self, __unit: None=None) -> Contract:
        this: License = self
        match_value: str = this.Type
        return Contract.create_update(this._path, DTOType(10), DTO(1, this.Content))

    def ToDeleteContract(self, __unit: None=None) -> Contract:
        this: License = self
        return Contract.create_delete(this._path)

    def GetRenameContracts(self, new_path: str) -> Array[Contract]:
        this: License = self
        delete_contract: Contract = this.ToDeleteContract()
        this.Path = new_path
        def _arrow3763(__unit: None=None) -> Contract:
            match_value: str = this.Type
            return Contract.create_create(new_path, DTOType(10), DTO(1, this.Content))

        return [delete_contract, _arrow3763()]

    @staticmethod
    def to_delete_contract(license: License) -> Contract:
        return license.ToDeleteContract()

    @staticmethod
    def to_create_contract(license: License) -> Contract:
        return license.ToCreateContract()

    @staticmethod
    def to_update_contract(license: License) -> Contract:
        return license.ToUpdateContract()

    @staticmethod
    def get_rename_contracts(new_path: str) -> Callable[[License], Array[Contract]]:
        def _arrow3764(license: License) -> Array[Contract]:
            return license.GetRenameContracts(new_path)

        return _arrow3764

    @staticmethod
    def try_from_read_contract(c: Contract) -> License | None:
        def _arrow3767(__unit: None=None) -> bool:
            txt: str = c.DTO.fields[0]
            class ObjectExpr3766:
                @property
                def Equals(self) -> Callable[[str, str], bool]:
                    def _arrow3765(x: str, y: str) -> bool:
                        return x == y

                    return _arrow3765

                @property
                def GetHashCode(self) -> Callable[[str], int]:
                    return string_hash

            return True if (c.Path == "LICENSE") else contains(c.Path, alternative_licensefile_names, ObjectExpr3766())

        def _arrow3768(__unit: None=None) -> License | None:
            txt_1: str = c.DTO.fields[0]
            return License.init_fulltext(txt_1, c.Path)

        return (((((_arrow3768() if _arrow3767() else None) if (c.DTO.tag == 1) else None) if (c.DTO is not None) else None) if (c.DTOType.tag == 10) else None) if (c.DTOType is not None) else None) if (c.Operation == "READ") else None

    @staticmethod
    def GetDefaultLicense(__unit: None=None) -> License:
        return License.init_fulltext("ALL RIGHTS RESERVED BY THE AUTHORS")

    def Copy(self, __unit: None=None) -> License:
        this: License = self
        return License(this.Type, this.Content)

    def __eq__(self, other: Any=None) -> bool:
        this: License = self
        return this.StructurallyEquals(other) if isinstance(other, License) else False

    def __hash__(self, __unit: None=None) -> Any:
        this: License = self
        return box_hash_array([this.Type, this.Content, this.Path])

    def StructurallyEquals(self, other: License) -> bool:
        this: License = self
        def predicate(x: bool) -> bool:
            return x == True

        return for_all(predicate, to_enumerable([this.Type == other.Type, this.Content == other.Content, this.Path == other.Path]))

    def ReferenceEquals(self, other: License) -> bool:
        this: License = self
        return this is other


License_reflection = _expr3769

def License__ctor_Z2FC25A28(content_type: str, content: str, path: str | None=None) -> License:
    return License(content_type, content, path)


__all__ = ["License_reflection"]

