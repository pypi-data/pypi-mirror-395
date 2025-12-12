from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.option import value
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import Array
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import (LDNode, LDGraph)
from .comment import LDComment
from .defined_term import LDDefinedTerm
from .person import LDPerson
from .property_value import LDPropertyValue

def _expr1763() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDScholarlyArticle", None, LDScholarlyArticle)


class LDScholarlyArticle:
    @staticmethod
    def schema_type() -> str:
        return "http://schema.org/ScholarlyArticle"

    @staticmethod
    def headline() -> str:
        return "http://schema.org/headline"

    @staticmethod
    def identifier() -> str:
        return "http://schema.org/identifier"

    @staticmethod
    def author() -> str:
        return "http://schema.org/author"

    @staticmethod
    def url() -> str:
        return "http://schema.org/url"

    @staticmethod
    def same_as() -> str:
        return "http://schema.org/sameAs"

    @staticmethod
    def creative_work_status() -> str:
        return "http://schema.org/creativeWorkStatus"

    @staticmethod
    def comment() -> str:
        return "http://schema.org/comment"

    @staticmethod
    def try_get_headline_as_string(s: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = s.TryGetPropertyAsSingleton(LDScholarlyArticle.headline(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_headline_as_string(s: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = s.TryGetPropertyAsSingleton(LDScholarlyArticle.headline(), context)
        if match_value is None:
            raise Exception(("Could not access property `headline` of object with @id `" + s.Id) + "`")

        elif str(type(value(match_value))) == "<class \'str\'>":
            n: str = value(match_value)
            return n

        else: 
            raise Exception(("Value of property `headline` of object with @id `" + s.Id) + "` should have been a string")


    @staticmethod
    def set_headline_as_string(s: LDNode, n: str) -> None:
        s.SetProperty(LDScholarlyArticle.headline(), n)

    @staticmethod
    def get_identifiers(s: LDNode, context: LDContext | None=None) -> Array[Any]:
        return s.GetPropertyValues(LDScholarlyArticle.identifier(), None, context)

    @staticmethod
    def get_identifiers_as_property_value(s: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDPropertyValue.validate(ld_object, context_1)

        return s.GetPropertyNodes(LDScholarlyArticle.identifier(), filter, graph, context)

    @staticmethod
    def set_identifiers(s: LDNode, identifiers: Array[Any]) -> None:
        s.SetProperty(LDScholarlyArticle.identifier(), identifiers)

    @staticmethod
    def get_authors(s: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDPerson.validate(ld_object, context_1)

        return s.GetPropertyNodes(LDScholarlyArticle.author(), filter, graph, context)

    @staticmethod
    def set_authors(s: LDNode, authors: Array[LDNode], context: LDContext | None=None) -> Any:
        return s.SetProperty(LDScholarlyArticle.author(), authors, context)

    @staticmethod
    def try_get_url_as_string(s: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = s.TryGetPropertyAsSingleton(LDScholarlyArticle.url(), context)
        (pattern_matching_result, u) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                u = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return u

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def try_get_same_as_as_string(s: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = s.TryGetPropertyAsSingleton(LDScholarlyArticle.same_as(), context)
        (pattern_matching_result, sa) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                sa = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return sa

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def try_get_creative_work_status(s: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = s.TryGetPropertyAsSingleNode(LDScholarlyArticle.creative_work_status(), graph, context)
        (pattern_matching_result, cws_1) = (None, None)
        if match_value is not None:
            def _arrow1762(__unit: None=None) -> bool:
                cws: LDNode = match_value
                return LDDefinedTerm.validate(cws, context)

            if _arrow1762():
                pattern_matching_result = 0
                cws_1 = match_value

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return cws_1

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_creative_work_status(s: LDNode, cws: LDNode, context: LDContext | None=None) -> Any:
        return s.SetProperty(LDScholarlyArticle.creative_work_status(), cws, context)

    @staticmethod
    def get_comments(s: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDComment.validate(ld_object, context_1)

        return s.GetPropertyNodes(LDScholarlyArticle.comment(), filter, graph, context)

    @staticmethod
    def setcomments(s: LDNode, comments: Array[LDNode], context: LDContext | None=None) -> Any:
        return s.SetProperty(LDScholarlyArticle.comment(), comments, context)

    @staticmethod
    def gen_id(headline: str, url: str | None=None) -> str:
        return clean((("#" + headline) + "") if (url is None) else url)

    @staticmethod
    def validate(s: LDNode, context: LDContext | None=None) -> bool:
        return s.HasProperty(LDScholarlyArticle.headline(), context) if s.HasType(LDScholarlyArticle.schema_type(), context) else False

    @staticmethod
    def create(headline: str, identifiers: Array[Any], id: str | None=None, authors: Array[LDNode] | None=None, url: str | None=None, creative_work_status: LDNode | None=None, comments: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        s: LDNode = LDNode(LDScholarlyArticle.gen_id(headline, url) if (id is None) else id, [LDScholarlyArticle.schema_type()], None, context)
        s.SetProperty(LDScholarlyArticle.headline(), headline, context)
        s.SetProperty(LDScholarlyArticle.identifier(), identifiers, context)
        s.SetOptionalProperty(LDScholarlyArticle.author(), authors, context)
        s.SetOptionalProperty(LDScholarlyArticle.url(), url, context)
        s.SetOptionalProperty(LDScholarlyArticle.creative_work_status(), creative_work_status, context)
        s.SetOptionalProperty(LDScholarlyArticle.comment(), comments, context)
        return s


LDScholarlyArticle_reflection = _expr1763

__all__ = ["LDScholarlyArticle_reflection"]

