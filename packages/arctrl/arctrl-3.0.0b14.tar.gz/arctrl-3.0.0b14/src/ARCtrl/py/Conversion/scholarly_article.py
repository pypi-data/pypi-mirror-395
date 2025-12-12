from __future__ import annotations
from typing import Any
from ..Core.comment import Comment
from ..Core.Helper.collections_ import (ResizeArray_map, Option_fromSeq, ResizeArray_tryPick)
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.publication import Publication
from ..Json.ROCrate.ldnode import (decoder as decoder_1, encoder)
from ..ROCrate.ldcontext import LDContext
from ..ROCrate.ldobject import (LDNode, LDGraph)
from ..ROCrate.LDTypes.person import LDPerson
from ..ROCrate.LDTypes.property_value import LDPropertyValue
from ..ROCrate.LDTypes.scholarly_article import LDScholarlyArticle
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string as to_string_1
from ..fable_modules.fable_library.option import (map as map_1, value as value_4)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.seq import (map, is_empty, filter, to_list, delay, append, singleton, empty)
from ..fable_modules.fable_library.string_ import (to_text, printf, join)
from ..fable_modules.fable_library.system_text import (StringBuilder__ctor, StringBuilder__Append_244C7CD6, StringBuilder__Clear)
from ..fable_modules.fable_library.types import (Array, to_string)
from ..fable_modules.fable_library.util import (ignore, get_enumerator, IEnumerable_1)
from .basic import (BaseTypes_composeComment_Z13201A7E, BaseTypes_composeDefinedTerm_ZDED3A0F, BaseTypes_decomposeComment_Z2F770004, BaseTypes_decomposeDefinedTerm_Z2F770004)

def _expr3955() -> TypeInfo:
    return class_type("ARCtrl.Conversion.ScholarlyArticleConversion", None, ScholarlyArticleConversion)


class ScholarlyArticleConversion:
    ...

ScholarlyArticleConversion_reflection = _expr3955

def ScholarlyArticleConversion_composeAuthor_Z721C83C5(author: str) -> LDNode:
    try: 
        match_value: FSharpResult_2[LDNode, str] = Decode_fromString(decoder_1, author)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as match_value_1:
        return LDPerson.create(author)



def ScholarlyArticleConversion_splitAuthors_Z721C83C5(a: str) -> Array[str]:
    bracket_count: int = 0
    authors: Array[str] = []
    sb: Any = StringBuilder__ctor()
    with get_enumerator(list(a)) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            c: str = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            if c == "{":
                bracket_count = (bracket_count + 1) or 0
                ignore(StringBuilder__Append_244C7CD6(sb, c))

            elif c == "}":
                bracket_count = (bracket_count - 1) or 0
                ignore(StringBuilder__Append_244C7CD6(sb, c))

            elif (bracket_count == 0) if (c == ",") else False:
                (authors.append(to_string(sb)))
                ignore(StringBuilder__Clear(sb))

            else: 
                ignore(StringBuilder__Append_244C7CD6(sb, c))

    (authors.append(to_string(sb)))
    return authors


def ScholarlyArticleConversion_composeAuthors_Z721C83C5(authors: str) -> Array[LDNode]:
    def mapping(author: str, authors: Any=authors) -> LDNode:
        return ScholarlyArticleConversion_composeAuthor_Z721C83C5(author)

    return list(map(mapping, ScholarlyArticleConversion_splitAuthors_Z721C83C5(authors)))


def ScholarlyArticleConversion_decomposeAuthor_Z2F770004(author: LDNode, context: LDContext | None=None) -> str:
    def predicate(n: str, author: Any=author, context: Any=context) -> bool:
        return n != LDPerson.given_name()

    if is_empty(filter(predicate, author.GetPropertyNames(context))):
        return LDPerson.get_given_name_as_string(author, context)

    else: 
        return to_string_1(0, encoder(author))



def ScholarlyArticleConversion_decomposeAuthors_1AAAE9A5(authors: Array[LDNode], context: LDContext | None=None) -> str:
    def f(a: LDNode, authors: Any=authors, context: Any=context) -> str:
        return ScholarlyArticleConversion_decomposeAuthor_Z2F770004(a, context)

    return join(",", ResizeArray_map(f, authors))


def ScholarlyArticleConversion_composeScholarlyArticle_D324A6D(publication: Publication) -> LDNode:
    title: str
    match_value: str | None = publication.Title
    if match_value is None:
        raise Exception("Publication must have a title")

    else: 
        title = match_value

    def mapping(authors: str, publication: Any=publication) -> Array[LDNode]:
        return ScholarlyArticleConversion_composeAuthors_Z721C83C5(authors)

    authors_1: Array[LDNode] | None = map_1(mapping, publication.Authors)
    def f(comment: Comment, publication: Any=publication) -> LDNode:
        return BaseTypes_composeComment_Z13201A7E(comment)

    comments: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f, publication.Comments))
    def _arrow3957(__unit: None=None, publication: Any=publication) -> IEnumerable_1[LDNode]:
        def _arrow3956(__unit: None=None) -> IEnumerable_1[LDNode]:
            return singleton(LDPropertyValue.create_pub_med_id(value_4(publication.PubMedID))) if ((value_4(publication.PubMedID) != "") if (publication.PubMedID is not None) else False) else empty()

        return append(singleton(LDPropertyValue.create_doi(value_4(publication.DOI))) if ((value_4(publication.DOI) != "") if (publication.DOI is not None) else False) else empty(), delay(_arrow3956))

    identifiers: Array[LDNode] = list(to_list(delay(_arrow3957)))
    def mapping_1(term: OntologyAnnotation, publication: Any=publication) -> LDNode:
        return BaseTypes_composeDefinedTerm_ZDED3A0F(term)

    status: LDNode | None = map_1(mapping_1, publication.Status)
    return LDScholarlyArticle.create(title, identifiers, None, authors_1, None, status, comments)


def ScholarlyArticleConversion_decomposeScholarlyArticle_Z6839B9E8(sa: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Publication:
    title: str = LDScholarlyArticle.get_headline_as_string(sa, context)
    def mapping(a: Array[LDNode], sa: Any=sa, graph: Any=graph, context: Any=context) -> str:
        return ScholarlyArticleConversion_decomposeAuthors_1AAAE9A5(a, context)

    authors: str | None = map_1(mapping, Option_fromSeq(LDScholarlyArticle.get_authors(sa, graph, context)))
    def f(c: LDNode, sa: Any=sa, graph: Any=graph, context: Any=context) -> Comment:
        return BaseTypes_decomposeComment_Z2F770004(c, context)

    comments: Array[Comment] = ResizeArray_map(f, LDScholarlyArticle.get_comments(sa, graph, context))
    def mapping_1(s: LDNode, sa: Any=sa, graph: Any=graph, context: Any=context) -> OntologyAnnotation:
        return BaseTypes_decomposeDefinedTerm_Z2F770004(s, context)

    status: OntologyAnnotation | None = map_1(mapping_1, LDScholarlyArticle.try_get_creative_work_status(sa, graph, context))
    identifiers: Array[LDNode] = LDScholarlyArticle.get_identifiers_as_property_value(sa, graph, context)
    doi: str | None
    def f_1(i: LDNode, sa: Any=sa, graph: Any=graph, context: Any=context) -> str | None:
        return LDPropertyValue.try_get_as_doi(i, context)

    _arg: str | None = ResizeArray_tryPick(f_1, identifiers)
    doi = LDScholarlyArticle.try_get_same_as_as_string(sa, context) if (_arg is None) else _arg
    pub_med_id: str | None
    def f_2(i_1: LDNode, sa: Any=sa, graph: Any=graph, context: Any=context) -> str | None:
        return LDPropertyValue.try_get_as_pub_med_id(i_1, context)

    _arg_1: str | None = ResizeArray_tryPick(f_2, identifiers)
    pub_med_id = LDScholarlyArticle.try_get_url_as_string(sa, context) if (_arg_1 is None) else _arg_1
    return Publication.create(pub_med_id, doi, authors, title, status, comments)


__all__ = ["ScholarlyArticleConversion_reflection", "ScholarlyArticleConversion_composeAuthor_Z721C83C5", "ScholarlyArticleConversion_splitAuthors_Z721C83C5", "ScholarlyArticleConversion_composeAuthors_Z721C83C5", "ScholarlyArticleConversion_decomposeAuthor_Z2F770004", "ScholarlyArticleConversion_decomposeAuthors_1AAAE9A5", "ScholarlyArticleConversion_composeScholarlyArticle_D324A6D", "ScholarlyArticleConversion_decomposeScholarlyArticle_Z6839B9E8"]

