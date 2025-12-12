from __future__ import annotations
from datetime import datetime
from typing import Any
from ...fable_modules.fable_library.option import value
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import Array
from ..ldcontext import LDContext
from ..ldobject import (LDNode, LDGraph)
from .comment import LDComment
from .file import LDFile
from .lab_process import LDLabProcess
from .person import LDPerson
from .scholarly_article import LDScholarlyArticle

def _expr1787() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDCreativeWork", None, LDCreativeWork)


class LDCreativeWork:
    @staticmethod
    def schema_type() -> str:
        return "http://schema.org/CreativeWork"

    @staticmethod
    def identifier() -> str:
        return "http://schema.org/identifier"

    @staticmethod
    def creator() -> str:
        return "http://schema.org/creator"

    @staticmethod
    def date_created() -> str:
        return "http://schema.org/dateCreated"

    @staticmethod
    def date_published() -> str:
        return "http://schema.org/datePublished"

    @staticmethod
    def sd_date_published() -> str:
        return "http://schema.org/datePublished"

    @staticmethod
    def license() -> str:
        return "http://schema.org/license"

    @staticmethod
    def date_modified() -> str:
        return "http://schema.org/dateModified"

    @staticmethod
    def description() -> str:
        return "http://schema.org/description"

    @staticmethod
    def has_part() -> str:
        return "http://schema.org/hasPart"

    @staticmethod
    def headline() -> str:
        return "http://schema.org/headline"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def text() -> str:
        return "http://schema.org/text"

    @staticmethod
    def citation() -> str:
        return "http://schema.org/citation"

    @staticmethod
    def comment() -> str:
        return "http://schema.org/comment"

    @staticmethod
    def mentions() -> str:
        return "http://schema.org/mentions"

    @staticmethod
    def url() -> str:
        return "http://schema.org/url"

    @staticmethod
    def about() -> str:
        return "http://schema.org/about"

    @staticmethod
    def try_get_identifier_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.identifier(), context)
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
    def get_identifier_as_string(lp: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.identifier(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                n: str = value(match_value)
                return n

            else: 
                raise Exception(("property `identifier` of object with @id `" + lp.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `identifier` of object with @id `" + lp.Id) + "`")


    @staticmethod
    def set_identifier_as_string(lp: LDNode, identifier: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.identifier(), identifier, context)

    @staticmethod
    def get_creators(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(p: LDNode, ctx: LDContext | None=None) -> bool:
            return LDPerson.validate(p, ctx)

        return lp.GetPropertyNodes(LDCreativeWork.creator(), filter, graph, context)

    @staticmethod
    def set_creators(lp: LDNode, creators: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.creator(), creators, context)

    @staticmethod
    def try_get_date_created_as_date_time(lp: LDNode, context: LDContext | None=None) -> Any | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.date_created(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if isinstance(value(match_value), datetime):
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
    def set_date_created_as_date_time(lp: LDNode, date_created: Any, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.date_created(), date_created, context)

    @staticmethod
    def try_get_date_published_as_date_time(lp: LDNode, context: LDContext | None=None) -> Any | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.date_published(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if isinstance(value(match_value), datetime):
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
    def set_date_published_as_date_time(lp: LDNode, date_published: Any, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.date_published(), date_published, context)

    @staticmethod
    def try_get_sddate_published_as_date_time(lp: LDNode, context: LDContext | None=None) -> Any | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.sd_date_published(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if isinstance(value(match_value), datetime):
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
    def set_sddate_published_as_date_time(lp: LDNode, sd_date_published: Any, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.sd_date_published(), sd_date_published, context)

    @staticmethod
    def try_get_license_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.license(), context)
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
    def set_license_as_string(lp: LDNode, license: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.license(), license, context)

    @staticmethod
    def set_license_as_creative_work(lp: LDNode, license: Any=None, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.license(), license, context)

    @staticmethod
    def try_get_date_modified_as_date_time(lp: LDNode, context: LDContext | None=None) -> Any | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.date_modified(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if isinstance(value(match_value), datetime):
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
    def set_date_modified_as_date_time(lp: LDNode, date_modified: Any, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.date_modified(), date_modified, context)

    @staticmethod
    def try_get_description_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.description(), context)
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
    def get_description_as_string(lp: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.description(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                n: str = value(match_value)
                return n

            else: 
                raise Exception(("property `description` of object with @id `" + lp.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `description` of object with @id `" + lp.Id) + "`")


    @staticmethod
    def set_description_as_string(lp: LDNode, description: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.description(), description, context)

    @staticmethod
    def get_has_parts(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return lp.GetPropertyNodes(LDCreativeWork.has_part(), None, graph, context)

    @staticmethod
    def get_has_parts_as_dataset(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ldnode: LDNode, context_1: LDContext | None=None) -> bool:
            return LDCreativeWork.validate(ldnode, context_1)

        return lp.GetPropertyNodes(LDCreativeWork.has_part(), filter, graph, context)

    @staticmethod
    def get_has_parts_as_file(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ldnode: LDNode, context_1: LDContext | None=None) -> bool:
            return LDFile.validate(ldnode, context_1)

        return lp.GetPropertyNodes(LDCreativeWork.has_part(), filter, graph, context)

    @staticmethod
    def set_has_parts(lp: LDNode, has_parts: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.has_part(), has_parts, context)

    @staticmethod
    def try_get_headline_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.headline(), context)
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
    def try_get_name_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.name(), context)
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
    def get_name_as_string(lp: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.name(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                n: str = value(match_value)
                return n

            else: 
                raise Exception(("property `name` of object with @id `" + lp.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `name` of object with @id `" + lp.Id) + "`")


    @staticmethod
    def set_name_as_string(lp: LDNode, name: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.name(), name, context)

    @staticmethod
    def try_get_text_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.text(), context)
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
    def get_text_as_string(lp: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.text(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                n: str = value(match_value)
                return n

            else: 
                raise Exception(("property `text` of object with @id `" + lp.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `text` of object with @id `" + lp.Id) + "`")


    @staticmethod
    def set_text_as_string(lp: LDNode, text: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.text(), text, context)

    @staticmethod
    def get_citations(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ldnode: LDNode, context_1: LDContext | None=None) -> bool:
            return LDScholarlyArticle.validate(ldnode, context_1)

        return lp.GetPropertyNodes(LDCreativeWork.citation(), filter, graph, context)

    @staticmethod
    def set_citations(lp: LDNode, citations: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.citation(), citations, context)

    @staticmethod
    def get_comments(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ldnode: LDNode, context_1: LDContext | None=None) -> bool:
            return LDComment.validate(ldnode, context_1)

        return lp.GetPropertyNodes(LDCreativeWork.comment(), filter, graph, context)

    @staticmethod
    def set_comments(lp: LDNode, comments: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.comment(), comments, context)

    @staticmethod
    def try_get_url_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.url(), context)
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
    def get_url_as_string(lp: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDCreativeWork.url(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                n: str = value(match_value)
                return n

            else: 
                raise Exception(("property `url` of object with @id `" + lp.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `url` of object with @id `" + lp.Id) + "`")


    @staticmethod
    def set_url_as_string(lp: LDNode, url: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.url(), url, context)

    @staticmethod
    def get_abouts(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return lp.GetPropertyNodes(LDCreativeWork.about(), None, graph, context)

    @staticmethod
    def get_abouts_as_lab_process(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ldnode: LDNode, context_1: LDContext | None=None) -> bool:
            return LDLabProcess.validate(ldnode, context_1)

        return lp.GetPropertyNodes(LDCreativeWork.about(), filter, graph, context)

    @staticmethod
    def set_abouts(lp: LDNode, abouts: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDCreativeWork.about(), abouts, context)

    @staticmethod
    def validate(lp: LDNode, context: LDContext | None=None) -> bool:
        return lp.HasType(LDCreativeWork.schema_type(), context)

    @staticmethod
    def create(id: str, identifier: str | None=None, creators: Array[LDNode] | None=None, date_created: Any | None=None, date_published: Any | None=None, date_modified: Any | None=None, description: str | None=None, has_parts: Array[LDNode] | None=None, name: str | None=None, text: str | None=None, citations: Array[LDNode] | None=None, comments: Array[LDNode] | None=None, mentions: Array[LDNode] | None=None, url: str | None=None, abouts: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        s: LDNode = LDNode(id, [LDCreativeWork.schema_type()], None, context)
        s.SetOptionalProperty(LDCreativeWork.identifier(), identifier, context)
        s.SetOptionalProperty(LDCreativeWork.creator(), creators, context)
        s.SetOptionalProperty(LDCreativeWork.date_created(), date_created, context)
        s.SetOptionalProperty(LDCreativeWork.date_published(), date_published, context)
        s.SetOptionalProperty(LDCreativeWork.date_modified(), date_modified, context)
        s.SetOptionalProperty(LDCreativeWork.description(), description, context)
        s.SetOptionalProperty(LDCreativeWork.has_part(), has_parts, context)
        s.SetOptionalProperty(LDCreativeWork.name(), name, context)
        s.SetOptionalProperty(LDCreativeWork.text(), text, context)
        s.SetOptionalProperty(LDCreativeWork.citation(), citations, context)
        s.SetOptionalProperty(LDCreativeWork.comment(), comments, context)
        s.SetOptionalProperty(LDCreativeWork.mentions(), mentions, context)
        s.SetOptionalProperty(LDCreativeWork.url(), url, context)
        s.SetOptionalProperty(LDCreativeWork.about(), abouts, context)
        return s


LDCreativeWork_reflection = _expr1787

__all__ = ["LDCreativeWork_reflection"]

