from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.option import (default_arg, value as value_4)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.seq import (to_list, delay, append, singleton, empty)
from ..fable_modules.fable_library.string_ import (join, to_text, printf)
from ..fable_modules.fable_library.system_text import (StringBuilder__ctor, StringBuilder__Append_Z721C83C5)
from ..fable_modules.fable_library.types import (Array, to_string)
from ..fable_modules.fable_library.util import (ignore, IEnumerable_1, string_hash, safe_hash)
from .comment import Comment
from .Helper.collections_ import ResizeArray_map
from .Helper.hash_codes import (merge_hashes, hash_1 as hash_1_1)
from .Helper.regex import (try_parse_term_annotation, ActivePatterns__007CRegex_007C__007C, Pattern_TermAnnotationShortPattern)
from .Helper.url import create_oauri

def _expr722() -> TypeInfo:
    return class_type("ARCtrl.OntologyAnnotation", None, OntologyAnnotation)


class OntologyAnnotation:
    def __init__(self, name: str | None=None, tsr: str | None=None, tan: str | None=None, comments: Array[Comment] | None=None) -> None:
        self._name: str | None = None if (name is None) else (None if (name == "") else name)
        self._termSourceREF: str | None = None if (tsr is None) else (None if (tsr == "") else tsr)
        self._termAccessionNumber: str | None = None if (tan is None) else (None if (tan == "") else (None if (tan == ":") else tan))
        self._comments: Array[Comment] = default_arg(comments, [])
        self._tanInfo: dict[str, Any] | None = OntologyAnnotation.compute_tan_info(self._termAccessionNumber, self._termSourceREF)

    @property
    def Name(self, __unit: None=None) -> str | None:
        this: OntologyAnnotation = self
        return this._name

    @Name.setter
    def Name(self, name: str | None=None) -> None:
        this: OntologyAnnotation = self
        this._name = name

    @property
    def TermSourceREF(self, __unit: None=None) -> str | None:
        this: OntologyAnnotation = self
        return this._termSourceREF

    @TermSourceREF.setter
    def TermSourceREF(self, tsr: str | None=None) -> None:
        this: OntologyAnnotation = self
        this._termSourceREF = tsr
        this.recompute_tan_info()

    @property
    def TermAccessionNumber(self, __unit: None=None) -> str | None:
        this: OntologyAnnotation = self
        return this._termAccessionNumber

    @TermAccessionNumber.setter
    def TermAccessionNumber(self, tan: str | None=None) -> None:
        this: OntologyAnnotation = self
        this._termAccessionNumber = tan
        this.recompute_tan_info()

    @property
    def Comments(self, __unit: None=None) -> Array[Comment]:
        this: OntologyAnnotation = self
        return this._comments

    @Comments.setter
    def Comments(self, comments: Array[Comment]) -> None:
        this: OntologyAnnotation = self
        this._comments = comments

    @staticmethod
    def make(name: str | None, tsr: str | None, tan: str | None, comments: Array[Comment]) -> OntologyAnnotation:
        return OntologyAnnotation(name, tsr, tan, comments)

    @staticmethod
    def create(name: str | None=None, tsr: str | None=None, tan: str | None=None, comments: Array[Comment] | None=None) -> OntologyAnnotation:
        comments_1: Array[Comment] = default_arg(comments, [])
        return OntologyAnnotation.make(name, tsr, tan, comments_1)

    @property
    def TANInfo(self, __unit: None=None) -> dict[str, Any] | None:
        this: OntologyAnnotation = self
        return this._tanInfo

    @property
    def NameText(self, __unit: None=None) -> str:
        this: OntologyAnnotation = self
        return default_arg(this.Name, "")

    @staticmethod
    def create_uri_annotation(term_source_ref: str, local_tan: str) -> str:
        return create_oauri(term_source_ref, local_tan)

    @staticmethod
    def from_term_annotation(tan: str, name: str | None=None) -> OntologyAnnotation:
        match_value: dict[str, Any] | None = try_parse_term_annotation(tan)
        if match_value is None:
            return OntologyAnnotation.create(name, None, tan)

        else: 
            r: dict[str, Any] = match_value
            accession: str = (r["IDSpace"] + ":") + r["LocalID"]
            return OntologyAnnotation.create(name, r["IDSpace"], accession)


    @property
    def TermAccessionShort(self, __unit: None=None) -> str:
        this: OntologyAnnotation = self
        match_value: dict[str, Any] | None = this.TANInfo
        if match_value is not None:
            id: dict[str, Any] = match_value
            return ((("" + id["IDSpace"]) + ":") + id["LocalID"]) + ""

        else: 
            return ""


    @property
    def TermAccessionOntobeeUrl(self, __unit: None=None) -> str:
        this: OntologyAnnotation = self
        match_value: dict[str, Any] | None = this.TANInfo
        if match_value is not None:
            id: dict[str, Any] = match_value
            return OntologyAnnotation.create_uri_annotation(id["IDSpace"], id["LocalID"])

        else: 
            return ""


    @property
    def TermAccessionAndOntobeeUrlIfShort(self, __unit: None=None) -> str:
        this: OntologyAnnotation = self
        match_value: str | None = this.TermAccessionNumber
        if match_value is not None:
            tan: str = match_value
            return this.TermAccessionOntobeeUrl if (ActivePatterns__007CRegex_007C__007C(Pattern_TermAnnotationShortPattern, tan) is not None) else tan

        else: 
            return ""


    @staticmethod
    def to_string_object(oa: OntologyAnnotation, as_ontobee_purl_url_if_short: bool | None=None) -> dict[str, Any]:
        as_ontobee_purl_url_if_short_1: bool = default_arg(as_ontobee_purl_url_if_short, False)
        TermName: str = default_arg(oa.Name, "")
        TermSourceREF: str = default_arg(oa.TermSourceREF, "")
        def _arrow709(__unit: None=None) -> str:
            url: str = oa.TermAccessionAndOntobeeUrlIfShort
            return default_arg(oa.TermAccessionNumber, "") if (url == "") else url

        return {
            "TermAccessionNumber": _arrow709() if as_ontobee_purl_url_if_short_1 else default_arg(oa.TermAccessionNumber, ""),
            "TermName": TermName,
            "TermSourceREF": TermSourceREF
        }

    def __str__(self, __unit: None=None) -> str:
        this: OntologyAnnotation = self
        sb: Any = StringBuilder__ctor()
        ignore(StringBuilder__Append_Z721C83C5(sb, "{"))
        def _arrow717(__unit: None=None) -> IEnumerable_1[str]:
            def _arrow710(__unit: None=None) -> str:
                arg: str = value_4(this.Name)
                return to_text(printf("Name = %A"))(arg)

            def _arrow716(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow711(__unit: None=None) -> str:
                    arg_1: str = value_4(this.TermSourceREF)
                    return to_text(printf("TSR = %A"))(arg_1)

                def _arrow715(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow712(__unit: None=None) -> str:
                        arg_2: str = value_4(this.TermAccessionNumber)
                        return to_text(printf("TAN = %A"))(arg_2)

                    def _arrow714(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow713(__unit: None=None) -> str:
                            arg_3: Array[Comment] = this.Comments
                            return to_text(printf("Comments = %A"))(arg_3)

                        return singleton(_arrow713()) if (len(this.Comments) != 0) else empty()

                    return append(singleton(_arrow712()) if (this.TermAccessionNumber is not None) else empty(), delay(_arrow714))

                return append(singleton(_arrow711()) if (this.TermSourceREF is not None) else empty(), delay(_arrow715))

            return append(singleton(_arrow710()) if (this.Name is not None) else empty(), delay(_arrow716))

        ignore(StringBuilder__Append_Z721C83C5(sb, join("; ", to_list(delay(_arrow717)))))
        ignore(StringBuilder__Append_Z721C83C5(sb, "}"))
        return to_string(sb)

    def is_empty(self, __unit: None=None) -> bool:
        this: OntologyAnnotation = self
        return (len(this.Comments) == 0) if ((this.TermAccessionNumber is None) if ((this.TermSourceREF is None) if (this.Name is None) else False) else False) else False

    def __hash__(self, __unit: None=None) -> int:
        this: OntologyAnnotation = self
        def _arrow718(__unit: None=None) -> int:
            match_value: str | None = this.Name
            return 0 if (match_value is None) else string_hash(match_value)

        def _arrow720(__unit: None=None) -> int:
            match_value: str | None = this.TermSourceREF
            match_value_1: dict[str, Any] | None = this.TANInfo
            if match_value is not None:
                if match_value_1 is None:
                    tsr_1: str = match_value
                    match_value_2: str | None = this.TermAccessionNumber
                    if match_value_2 is None:
                        return string_hash(tsr_1.lower())

                    else: 
                        tan: str = match_value_2
                        return merge_hashes(string_hash(tsr_1.lower()), string_hash(tan))


                else: 
                    taninfo_1: dict[str, Any] = match_value_1
                    tsr: str = match_value
                    return merge_hashes(string_hash(tsr.lower()), string_hash(taninfo_1["LocalID"]))


            else: 
                def _arrow719(__unit: None=None) -> int:
                    taninfo: dict[str, Any] = match_value_1
                    return merge_hashes(string_hash(taninfo["IDSpace"].lower()), string_hash(taninfo["LocalID"]))

                return 0 if (match_value_1 is None) else _arrow719()


        return merge_hashes(_arrow718(), _arrow720())

    def __eq__(self, obj: Any=None) -> bool:
        this: OntologyAnnotation = self
        return hash_1_1(this) == hash_1_1(obj)

    def Copy(self, __unit: None=None) -> OntologyAnnotation:
        this: OntologyAnnotation = self
        def f(c: Comment) -> Comment:
            return c.Copy()

        next_comments: Array[Comment] = ResizeArray_map(f, this.Comments)
        name: str | None = this.Name
        tsr: str | None = this.TermSourceREF
        tan: str | None = this.TermAccessionNumber
        return OntologyAnnotation.make(name, tsr, tan, next_comments)

    @staticmethod
    def compute_tan_info(tan: str | None=None, tsr: str | None=None) -> dict[str, Any] | None:
        if tan is None:
            return None

        else: 
            tan_1: str = tan
            match_value: dict[str, Any] | None = try_parse_term_annotation(tan_1)
            def _arrow721(__unit: None=None) -> dict[str, Any] | None:
                tsr_1: str = tsr
                return {
                    "IDSpace": tsr_1,
                    "LocalID": tan_1
                }

            return (None if (tsr is None) else (None if (tsr == "") else _arrow721())) if (match_value is None) else match_value


    def Print(self, __unit: None=None) -> str:
        this: OntologyAnnotation = self
        return to_string(this)

    def PrintCompact(self, __unit: None=None) -> str:
        this: OntologyAnnotation = self
        return "OA " + this.NameText

    def __cmp__(self, obj: Any=None) -> int:
        this: OntologyAnnotation = self
        if isinstance(obj, OntologyAnnotation):
            hash_1: int = safe_hash(this) or 0
            other_hash: int = safe_hash(obj) or 0
            return 0 if (hash_1 == other_hash) else (-1 if (hash_1 < other_hash) else 1)

        else: 
            return 1


    def recompute_tan_info(self, __unit: None=None) -> None:
        this: OntologyAnnotation = self
        new_tan_info: dict[str, Any] | None = OntologyAnnotation.compute_tan_info(this._termAccessionNumber, this._termSourceREF)
        this._tanInfo = new_tan_info


OntologyAnnotation_reflection = _expr722

def OntologyAnnotation__ctor_Z54349580(name: str | None=None, tsr: str | None=None, tan: str | None=None, comments: Array[Comment] | None=None) -> OntologyAnnotation:
    return OntologyAnnotation(name, tsr, tan, comments)


__all__ = ["OntologyAnnotation_reflection"]

