from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.array_ import (try_find, exists, filter)
from ..fable_modules.fable_library.list import (append, singleton, FSharpList, map, choose, of_array)
from ..fable_modules.fable_library.option import (default_arg, map as map_1)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.seq import length
from ..fable_modules.fable_library.string_ import (join, to_text, printf)
from ..fable_modules.fable_library.system_text import (StringBuilder__ctor, StringBuilder__Append_Z721C83C5)
from ..fable_modules.fable_library.types import (Array, to_string)
from ..fable_modules.fable_library.util import (equals, ignore)
from .comment import Comment
from .Helper.collections_ import ResizeArray_map
from .Helper.hash_codes import (box_hash_array, box_hash_option, box_hash_seq, hash_1)
from .ontology_annotation import OntologyAnnotation

def _expr736() -> TypeInfo:
    return class_type("ARCtrl.Person", None, Person)


class Person:
    def __init__(self, orcid: str | None=None, last_name: str | None=None, first_name: str | None=None, mid_initials: str | None=None, email: str | None=None, phone: str | None=None, fax: str | None=None, address: str | None=None, affiliation: str | None=None, roles: Array[OntologyAnnotation] | None=None, comments: Array[Comment] | None=None) -> None:
        self._orcid: str | None = orcid
        self._lastName: str | None = last_name
        self._firstName: str | None = first_name
        self._midInitials: str | None = mid_initials
        self._email: str | None = email
        self._phone: str | None = phone
        self._fax: str | None = fax
        self._address: str | None = address
        self._affiliation: str | None = affiliation
        self._roles: Array[OntologyAnnotation] = default_arg(roles, [])
        self._comments: Array[Comment] = default_arg(comments, [])

    @property
    def ORCID(self, __unit: None=None) -> str | None:
        this: Person = self
        return this._orcid

    @ORCID.setter
    def ORCID(self, orcid: str | None=None) -> None:
        this: Person = self
        this._orcid = orcid

    @property
    def FirstName(self, __unit: None=None) -> str | None:
        this: Person = self
        return this._firstName

    @FirstName.setter
    def FirstName(self, first_name: str | None=None) -> None:
        this: Person = self
        this._firstName = first_name

    @property
    def LastName(self, __unit: None=None) -> str | None:
        this: Person = self
        return this._lastName

    @LastName.setter
    def LastName(self, last_name: str | None=None) -> None:
        this: Person = self
        this._lastName = last_name

    @property
    def MidInitials(self, __unit: None=None) -> str | None:
        this: Person = self
        return this._midInitials

    @MidInitials.setter
    def MidInitials(self, mid_initials: str | None=None) -> None:
        this: Person = self
        this._midInitials = mid_initials

    @property
    def Address(self, __unit: None=None) -> str | None:
        this: Person = self
        return this._address

    @Address.setter
    def Address(self, address: str | None=None) -> None:
        this: Person = self
        this._address = address

    @property
    def Affiliation(self, __unit: None=None) -> str | None:
        this: Person = self
        return this._affiliation

    @Affiliation.setter
    def Affiliation(self, affiliation: str | None=None) -> None:
        this: Person = self
        this._affiliation = affiliation

    @property
    def EMail(self, __unit: None=None) -> str | None:
        this: Person = self
        return this._email

    @EMail.setter
    def EMail(self, email: str | None=None) -> None:
        this: Person = self
        this._email = email

    @property
    def Phone(self, __unit: None=None) -> str | None:
        this: Person = self
        return this._phone

    @Phone.setter
    def Phone(self, phone: str | None=None) -> None:
        this: Person = self
        this._phone = phone

    @property
    def Fax(self, __unit: None=None) -> str | None:
        this: Person = self
        return this._fax

    @Fax.setter
    def Fax(self, fax: str | None=None) -> None:
        this: Person = self
        this._fax = fax

    @property
    def Roles(self, __unit: None=None) -> Array[OntologyAnnotation]:
        this: Person = self
        return this._roles

    @Roles.setter
    def Roles(self, roles: Array[OntologyAnnotation]) -> None:
        this: Person = self
        this._roles = roles

    @property
    def Comments(self, __unit: None=None) -> Array[Comment]:
        this: Person = self
        return this._comments

    @Comments.setter
    def Comments(self, comments: Array[Comment]) -> None:
        this: Person = self
        this._comments = comments

    @staticmethod
    def make(orcid: str | None, last_name: str | None, first_name: str | None, mid_initials: str | None, email: str | None, phone: str | None, fax: str | None, address: str | None, affiliation: str | None, roles: Array[OntologyAnnotation], comments: Array[Comment]) -> Person:
        return Person(orcid, last_name, first_name, mid_initials, email, phone, fax, address, affiliation, roles, comments)

    @staticmethod
    def create(orcid: str | None=None, last_name: str | None=None, first_name: str | None=None, mid_initials: str | None=None, email: str | None=None, phone: str | None=None, fax: str | None=None, address: str | None=None, affiliation: str | None=None, roles: Array[OntologyAnnotation] | None=None, comments: Array[Comment] | None=None) -> Person:
        roles_1: Array[OntologyAnnotation] = default_arg(roles, [])
        comments_1: Array[Comment] = default_arg(comments, [])
        return Person.make(orcid, last_name, first_name, mid_initials, email, phone, fax, address, affiliation, roles_1, comments_1)

    @staticmethod
    def empty() -> Person:
        return Person.create()

    @staticmethod
    def try_get_by_full_name(first_name: str, mid_initials: str, last_name: str, persons: Array[Person]) -> Person | None:
        def predicate(p: Person) -> bool:
            if mid_initials == "":
                if equals(p.FirstName, first_name):
                    return equals(p.LastName, last_name)

                else: 
                    return False


            elif equals(p.MidInitials, mid_initials) if equals(p.FirstName, first_name) else False:
                return equals(p.LastName, last_name)

            else: 
                return False


        return try_find(predicate, persons)

    @staticmethod
    def exists_by_full_name(first_name: str, mid_initials: str, last_name: str, persons: Array[Person]) -> bool:
        def _arrow732(p: Person) -> bool:
            return (equals(p.LastName, last_name) if equals(p.FirstName, first_name) else False) if (mid_initials == "") else (equals(p.LastName, last_name) if (equals(p.MidInitials, mid_initials) if equals(p.FirstName, first_name) else False) else False)

        return exists(_arrow732, persons)

    @staticmethod
    def add(persons: FSharpList[Person], person: Person) -> FSharpList[Person]:
        return append(persons, singleton(person))

    @staticmethod
    def remove_by_full_name(first_name: str, mid_initials: str, last_name: str, persons: Array[Person]) -> Array[Person]:
        def _arrow733(p: Person) -> bool:
            return (not (equals(p.LastName, last_name) if equals(p.FirstName, first_name) else False)) if (mid_initials == "") else (not (equals(p.LastName, last_name) if (equals(p.MidInitials, mid_initials) if equals(p.FirstName, first_name) else False) else False))

        return filter(_arrow733, persons)

    def Copy(self, __unit: None=None) -> Person:
        this: Person = self
        def f(c: Comment) -> Comment:
            return c.Copy()

        next_comments: Array[Comment] = ResizeArray_map(f, this.Comments)
        def f_1(c_1: OntologyAnnotation) -> OntologyAnnotation:
            return c_1.Copy()

        next_roles: Array[OntologyAnnotation] = ResizeArray_map(f_1, this.Roles)
        orcid: str | None = this.ORCID
        last_name: str | None = this.LastName
        first_name: str | None = this.FirstName
        mid_initials: str | None = this.MidInitials
        email: str | None = this.EMail
        phone: str | None = this.Phone
        fax: str | None = this.Fax
        address: str | None = this.Address
        affiliation: str | None = this.Affiliation
        return Person.make(orcid, last_name, first_name, mid_initials, email, phone, fax, address, affiliation, next_roles, next_comments)

    def __hash__(self, __unit: None=None) -> Any:
        this: Person = self
        return box_hash_array([box_hash_option(this.ORCID), box_hash_option(this.LastName), box_hash_option(this.FirstName), box_hash_option(this.MidInitials), box_hash_option(this.EMail), box_hash_option(this.Phone), box_hash_option(this.Fax), box_hash_option(this.Address), box_hash_option(this.Affiliation), box_hash_seq(this.Roles), box_hash_seq(this.Comments)])

    def __eq__(self, obj: Any=None) -> bool:
        this: Person = self
        return hash_1(this) == hash_1(obj)

    def __str__(self, __unit: None=None) -> str:
        this: Person = self
        sb: Any = StringBuilder__ctor()
        ignore(StringBuilder__Append_Z721C83C5(sb, "Person {\n\t"))
        def mapping_1(tupled_arg_1: tuple[str, str]) -> str:
            return to_text(printf("%s = %A"))(tupled_arg_1[0])(tupled_arg_1[1])

        def chooser(tupled_arg: tuple[str, str | None]) -> tuple[str, str] | None:
            def mapping(o: str, tupled_arg: Any=tupled_arg) -> tuple[str, str]:
                return (tupled_arg[0], o)

            return map_1(mapping, tupled_arg[1])

        def _arrow734(__unit: None=None) -> str:
            arg: Array[OntologyAnnotation] = this.Roles
            return to_text(printf("%A"))(arg)

        def _arrow735(__unit: None=None) -> str:
            arg_1: Array[Comment] = this.Comments
            return to_text(printf("%A"))(arg_1)

        ignore(StringBuilder__Append_Z721C83C5(sb, join(",\n\t", map(mapping_1, choose(chooser, of_array([("FirstName", this.FirstName), ("LastName", this.LastName), ("MidInitials", this.MidInitials), ("EMail", this.EMail), ("Phone", this.Phone), ("Address", this.Address), ("Affiliation", this.Affiliation), ("Fax", this.Fax), ("ORCID", this.ORCID), ("Roles", _arrow734() if (length(this.Roles) > 0) else None), ("Comments", _arrow735() if (length(this.Comments) > 0) else None)]))))))
        ignore(StringBuilder__Append_Z721C83C5(sb, "\n}"))
        return to_string(sb)


Person_reflection = _expr736

def Person__ctor_Z2F6491B5(orcid: str | None=None, last_name: str | None=None, first_name: str | None=None, mid_initials: str | None=None, email: str | None=None, phone: str | None=None, fax: str | None=None, address: str | None=None, affiliation: str | None=None, roles: Array[OntologyAnnotation] | None=None, comments: Array[Comment] | None=None) -> Person:
    return Person(orcid, last_name, first_name, mid_initials, email, phone, fax, address, affiliation, roles, comments)


__all__ = ["Person_reflection"]

