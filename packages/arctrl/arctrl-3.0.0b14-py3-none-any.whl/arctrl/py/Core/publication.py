from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (map, choose, of_array)
from ..fable_modules.fable_library.option import (default_arg, map as map_1)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.seq import length
from ..fable_modules.fable_library.string_ import (join, to_text, printf)
from ..fable_modules.fable_library.system_text import (StringBuilder__ctor, StringBuilder__Append_Z721C83C5)
from ..fable_modules.fable_library.types import (Array, to_string)
from ..fable_modules.fable_library.util import (safe_hash, ignore)
from .comment import Comment
from .Helper.collections_ import ResizeArray_map
from .Helper.hash_codes import (box_hash_array, box_hash_option, box_hash_seq)
from .ontology_annotation import OntologyAnnotation

def _expr740() -> TypeInfo:
    return class_type("ARCtrl.Publication", None, Publication)


class Publication:
    def __init__(self, pub_med_id: str | None=None, doi: str | None=None, authors: str | None=None, title: str | None=None, status: OntologyAnnotation | None=None, comments: Array[Comment] | None=None) -> None:
        self._pubMedID: str | None = pub_med_id
        self._doi: str | None = doi
        self._authors: str | None = authors
        self._title: str | None = title
        self._status: OntologyAnnotation | None = status
        self._comments: Array[Comment] = default_arg(comments, [])

    @property
    def PubMedID(self, __unit: None=None) -> str | None:
        this: Publication = self
        return this._pubMedID

    @PubMedID.setter
    def PubMedID(self, pub_med_id: str | None=None) -> None:
        this: Publication = self
        this._pubMedID = pub_med_id

    @property
    def DOI(self, __unit: None=None) -> str | None:
        this: Publication = self
        return this._doi

    @DOI.setter
    def DOI(self, doi: str | None=None) -> None:
        this: Publication = self
        this._doi = doi

    @property
    def Authors(self, __unit: None=None) -> str | None:
        this: Publication = self
        return this._authors

    @Authors.setter
    def Authors(self, authors: str | None=None) -> None:
        this: Publication = self
        this._authors = authors

    @property
    def Title(self, __unit: None=None) -> str | None:
        this: Publication = self
        return this._title

    @Title.setter
    def Title(self, title: str | None=None) -> None:
        this: Publication = self
        this._title = title

    @property
    def Status(self, __unit: None=None) -> OntologyAnnotation | None:
        this: Publication = self
        return this._status

    @Status.setter
    def Status(self, status: OntologyAnnotation | None=None) -> None:
        this: Publication = self
        this._status = status

    @property
    def Comments(self, __unit: None=None) -> Array[Comment]:
        this: Publication = self
        return this._comments

    @Comments.setter
    def Comments(self, comments: Array[Comment]) -> None:
        this: Publication = self
        this._comments = comments

    @staticmethod
    def make(pub_med_id: str | None, doi: str | None, authors: str | None, title: str | None, status: OntologyAnnotation | None, comments: Array[Comment]) -> Publication:
        return Publication(pub_med_id, doi, authors, title, status, comments)

    @staticmethod
    def create(pub_med_id: str | None=None, doi: str | None=None, authors: str | None=None, title: str | None=None, status: OntologyAnnotation | None=None, comments: Array[Comment] | None=None) -> Publication:
        comments_1: Array[Comment] = default_arg(comments, [])
        return Publication.make(pub_med_id, doi, authors, title, status, comments_1)

    @staticmethod
    def empty(__unit: None=None) -> Publication:
        return Publication.create()

    def Copy(self, __unit: None=None) -> Publication:
        this: Publication = self
        def f(c: Comment) -> Comment:
            return c.Copy()

        next_comments: Array[Comment] = ResizeArray_map(f, this.Comments)
        pub_med_id: str | None = this.PubMedID
        doi: str | None = this.DOI
        authors: str | None = this.Authors
        title: str | None = this.Title
        status: OntologyAnnotation | None = this.Status
        return Publication.make(pub_med_id, doi, authors, title, status, next_comments)

    def __hash__(self, __unit: None=None) -> Any:
        this: Publication = self
        return box_hash_array([box_hash_option(this.DOI), box_hash_option(this.Title), box_hash_option(this.Authors), box_hash_option(this.PubMedID), box_hash_option(this.Status), box_hash_seq(this.Comments)])

    def __eq__(self, obj: Any=None) -> bool:
        this: Publication = self
        return (safe_hash(this) == safe_hash(obj)) if isinstance(obj, Publication) else False

    def __str__(self, __unit: None=None) -> str:
        this: Publication = self
        sb: Any = StringBuilder__ctor()
        ignore(StringBuilder__Append_Z721C83C5(sb, "Publication {\n\t"))
        def mapping_2(tupled_arg_1: tuple[str, str]) -> str:
            return to_text(printf("%s = %A"))(tupled_arg_1[0])(tupled_arg_1[1])

        def chooser(tupled_arg: tuple[str, str | None]) -> tuple[str, str] | None:
            def mapping_1(o: str, tupled_arg: Any=tupled_arg) -> tuple[str, str]:
                return (tupled_arg[0], o)

            return map_1(mapping_1, tupled_arg[1])

        def _arrow738(__unit: None=None) -> str | None:
            option: OntologyAnnotation | None = this.Status
            def _arrow737(__unit: None=None) -> Callable[[OntologyAnnotation], str]:
                clo: Callable[[OntologyAnnotation], str] = to_text(printf("%A"))
                return clo

            return map_1(_arrow737(), option)

        def _arrow739(__unit: None=None) -> str:
            arg_1: Array[Comment] = this.Comments
            return to_text(printf("%A"))(arg_1)

        ignore(StringBuilder__Append_Z721C83C5(sb, join(",\n\t", map(mapping_2, choose(chooser, of_array([("PubMedID", this.PubMedID), ("DOI", this.DOI), ("Authors", this.Authors), ("Title", this.Title), ("Status", _arrow738()), ("Comments", _arrow739() if (length(this.Comments) > 0) else None)]))))))
        ignore(StringBuilder__Append_Z721C83C5(sb, "\n}"))
        return to_string(sb)


Publication_reflection = _expr740

def Publication__ctor_Z645CED36(pub_med_id: str | None=None, doi: str | None=None, authors: str | None=None, title: str | None=None, status: OntologyAnnotation | None=None, comments: Array[Comment] | None=None) -> Publication:
    return Publication(pub_med_id, doi, authors, title, status, comments)


__all__ = ["Publication_reflection"]

