from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import safe_hash
from .comment import Comment
from .Helper.collections_ import ResizeArray_map
from .Helper.hash_codes import (box_hash_array, box_hash_option, box_hash_seq)

def _expr741() -> TypeInfo:
    return class_type("ARCtrl.OntologySourceReference", None, OntologySourceReference)


class OntologySourceReference:
    def __init__(self, description: str | None=None, file: str | None=None, name: str | None=None, version: str | None=None, comments: Array[Comment] | None=None) -> None:
        self._description: str | None = description
        self._file: str | None = file
        self._name: str | None = name
        self._version: str | None = version
        self._comments: Array[Comment] = default_arg(comments, [])

    @property
    def Description(self, __unit: None=None) -> str | None:
        this: OntologySourceReference = self
        return this._description

    @Description.setter
    def Description(self, description: str | None=None) -> None:
        this: OntologySourceReference = self
        this._description = description

    @property
    def File(self, __unit: None=None) -> str | None:
        this: OntologySourceReference = self
        return this._file

    @File.setter
    def File(self, file: str | None=None) -> None:
        this: OntologySourceReference = self
        this._file = file

    @property
    def Name(self, __unit: None=None) -> str | None:
        this: OntologySourceReference = self
        return this._name

    @Name.setter
    def Name(self, name: str | None=None) -> None:
        this: OntologySourceReference = self
        this._name = name

    @property
    def Version(self, __unit: None=None) -> str | None:
        this: OntologySourceReference = self
        return this._version

    @Version.setter
    def Version(self, version: str | None=None) -> None:
        this: OntologySourceReference = self
        this._version = version

    @property
    def Comments(self, __unit: None=None) -> Array[Comment]:
        this: OntologySourceReference = self
        return this._comments

    @Comments.setter
    def Comments(self, comments: Array[Comment]) -> None:
        this: OntologySourceReference = self
        this._comments = comments

    @staticmethod
    def make(description: str | None, file: str | None, name: str | None, version: str | None, comments: Array[Comment]) -> OntologySourceReference:
        return OntologySourceReference(description, file, name, version, comments)

    @staticmethod
    def create(description: str | None=None, file: str | None=None, name: str | None=None, version: str | None=None, comments: Array[Comment] | None=None) -> OntologySourceReference:
        comments_1: Array[Comment] = default_arg(comments, [])
        return OntologySourceReference.make(description, file, name, version, comments_1)

    @staticmethod
    def empty() -> OntologySourceReference:
        return OntologySourceReference.create()

    def Copy(self, __unit: None=None) -> OntologySourceReference:
        this: OntologySourceReference = self
        def f(c: Comment) -> Comment:
            return c.Copy()

        next_comments: Array[Comment] = ResizeArray_map(f, this.Comments)
        description: str | None = this.Description
        file: str | None = this.File
        name: str | None = this.Name
        version: str | None = this.Version
        return OntologySourceReference.make(description, file, name, version, next_comments)

    def __hash__(self, __unit: None=None) -> Any:
        this: OntologySourceReference = self
        return box_hash_array([box_hash_option(this.Description), box_hash_option(this.File), box_hash_option(this.Name), box_hash_option(this.Version), box_hash_seq(this.Comments)])

    def __eq__(self, obj: Any=None) -> bool:
        this: OntologySourceReference = self
        return (safe_hash(this) == safe_hash(obj)) if isinstance(obj, OntologySourceReference) else False


OntologySourceReference_reflection = _expr741

def OntologySourceReference__ctor_7C9A7CF8(description: str | None=None, file: str | None=None, name: str | None=None, version: str | None=None, comments: Array[Comment] | None=None) -> OntologySourceReference:
    return OntologySourceReference(description, file, name, version, comments)


__all__ = ["OntologySourceReference_reflection"]

