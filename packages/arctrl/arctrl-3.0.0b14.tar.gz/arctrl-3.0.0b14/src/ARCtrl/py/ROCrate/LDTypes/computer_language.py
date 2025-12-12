from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.option import (value, map)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..ldcontext import LDContext
from ..ldobject import (LDNode, LDRef)
from .formal_parameter import LDFormalParameter

def _expr1724() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDComputerLanguage", None, LDComputerLanguage)


class LDComputerLanguage:
    @staticmethod
    def schema_type() -> str:
        return "http://schema.org/ComputerLanguage"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def alternate_name() -> str:
        return "http://schema.org/alternateName"

    @staticmethod
    def identifier() -> str:
        return "http://schema.org/identifier"

    @staticmethod
    def url() -> str:
        return "http://schema.org/url"

    @staticmethod
    def same_as() -> str:
        return "http://schema.org/sameAs"

    @staticmethod
    def try_get_name_as_string(cl: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = cl.TryGetPropertyAsSingleton(LDFormalParameter.name(), context)
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
    def get_name_as_string(cl: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = cl.TryGetPropertyAsSingleton(LDComputerLanguage.name(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                n: str = value(match_value)
                return n

            else: 
                raise Exception(("Property of `name` of object with @id `" + cl.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `name` of object with @id `" + cl.Id) + "`")


    @staticmethod
    def set_name_as_string(cl: LDNode, name: str, context: LDContext | None=None) -> Any:
        return cl.SetProperty(LDComputerLanguage.name(), name, context)

    @staticmethod
    def try_get_alternate_name_as_string(cl: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = cl.TryGetPropertyAsSingleton(LDComputerLanguage.alternate_name(), context)
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
    def get_alternate_name_as_string(cl: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = cl.TryGetPropertyAsSingleton(LDComputerLanguage.alternate_name(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                n: str = value(match_value)
                return n

            else: 
                raise Exception(("Property of `alternateName` of object with @id `" + cl.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `alternateName` of object with @id `" + cl.Id) + "`")


    @staticmethod
    def set_alternate_name_as_string(cl: LDNode, alternate_name: str, context: LDContext | None=None) -> Any:
        return cl.SetProperty(LDComputerLanguage.alternate_name(), alternate_name, context)

    @staticmethod
    def try_get_identifier_as_ldref(cl: LDNode, context: LDContext | None=None) -> LDRef | None:
        match_value: Any | None = cl.TryGetPropertyAsSingleton(LDComputerLanguage.identifier(), context)
        (pattern_matching_result, id) = (None, None)
        if match_value is not None:
            if isinstance(value(match_value), LDRef):
                pattern_matching_result = 0
                id = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return id

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_identifier_as_ldref(cl: LDNode, context: LDContext | None=None) -> LDRef:
        match_value: Any | None = cl.TryGetPropertyAsSingleton(LDComputerLanguage.identifier(), context)
        if match_value is not None:
            if isinstance(value(match_value), LDRef):
                id: LDRef = value(match_value)
                return id

            else: 
                raise Exception(("Property of `identifier` of object with @id `" + cl.Id) + "` was not a LDRef")


        else: 
            raise Exception(("Could not access property `identifier` of object with @id `" + cl.Id) + "`")


    @staticmethod
    def set_identifier_as_ldref(cl: LDNode, identifier: LDRef, context: LDContext | None=None) -> Any:
        return cl.SetProperty(LDComputerLanguage.identifier(), identifier, context)

    @staticmethod
    def try_get_url_as_ldref(cl: LDNode, context: LDContext | None=None) -> LDRef | None:
        match_value: Any | None = cl.TryGetPropertyAsSingleton(LDComputerLanguage.url(), context)
        (pattern_matching_result, url) = (None, None)
        if match_value is not None:
            if isinstance(value(match_value), LDRef):
                pattern_matching_result = 0
                url = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return url

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_url_as_ldref(cl: LDNode, context: LDContext | None=None) -> LDRef:
        match_value: Any | None = cl.TryGetPropertyAsSingleton(LDComputerLanguage.url(), context)
        if match_value is not None:
            if isinstance(value(match_value), LDRef):
                url: LDRef = value(match_value)
                return url

            else: 
                raise Exception(("Property of `url` of object with @id `" + cl.Id) + "` was not a LDRef")


        else: 
            raise Exception(("Could not access property `url` of object with @id `" + cl.Id) + "`")


    @staticmethod
    def set_url_as_ldref(cl: LDNode, url: LDRef, context: LDContext | None=None) -> Any:
        return cl.SetProperty(LDComputerLanguage.url(), url, context)

    @staticmethod
    def validate(cl: LDNode, context: LDContext | None=None) -> bool:
        return cl.HasType(LDComputerLanguage.schema_type(), context)

    @staticmethod
    def validate_cwl(cl: LDNode, context: LDContext | None=None) -> bool:
        return (cl.Id == "https://w3id.org/workflowhub/workflow-ro-crate#cwl") if LDComputerLanguage.validate(cl, context) else False

    @staticmethod
    def validate_galaxy(cl: LDNode, context: LDContext | None=None) -> bool:
        return (cl.Id == "https://w3id.org/workflowhub/workflow-ro-crate#galaxy") if LDComputerLanguage.validate(cl, context) else False

    @staticmethod
    def validate_knime(cl: LDNode, context: LDContext | None=None) -> bool:
        return (cl.Id == "https://w3id.org/workflowhub/workflow-ro-crate#knime") if LDComputerLanguage.validate(cl, context) else False

    @staticmethod
    def validate_nextflow(cl: LDNode, context: LDContext | None=None) -> bool:
        return (cl.Id == "https://w3id.org/workflowhub/workflow-ro-crate#nextflow") if LDComputerLanguage.validate(cl, context) else False

    @staticmethod
    def validate_snakemake(cl: LDNode, context: LDContext | None=None) -> bool:
        return (cl.Id == "https://w3id.org/workflowhub/workflow-ro-crate#snakemake") if LDComputerLanguage.validate(cl, context) else False

    @staticmethod
    def create(id: str, name: str | None=None, alternate_name: str | None=None, identifier: str | None=None, url: str | None=None, context: LDContext | None=None) -> LDNode:
        cl: LDNode = LDNode(id, [LDComputerLanguage.schema_type()], None, context)
        identifier_1: LDRef | None = map(LDRef, identifier)
        url_1: LDRef | None = map(LDRef, url)
        cl.SetOptionalProperty(LDComputerLanguage.name(), name, context)
        cl.SetOptionalProperty(LDComputerLanguage.alternate_name(), alternate_name, context)
        cl.SetOptionalProperty(LDComputerLanguage.identifier(), identifier_1, context)
        cl.SetOptionalProperty(LDComputerLanguage.url(), url_1, context)
        return cl

    @staticmethod
    def create_cwl(context: LDContext | None=None) -> LDNode:
        return LDComputerLanguage.create("https://w3id.org/workflowhub/workflow-ro-crate#cwl", "Common Workflow Language", "CWL", "https://w3id.org/cwl/v1.2/", "https://www.commonwl.org/", context)

    @staticmethod
    def create_galaxy(context: LDContext | None=None) -> LDNode:
        return LDComputerLanguage.create("https://w3id.org/workflowhub/workflow-ro-crate#galaxy", "Galaxy", None, "https://galaxyproject.org/", "https://galaxyproject.org/", context)

    @staticmethod
    def create_knime(context: LDContext | None=None) -> LDNode:
        return LDComputerLanguage.create("https://w3id.org/workflowhub/workflow-ro-crate#knime", "KNIME", None, "https://www.knime.com/", "https://www.knime.com/", context)

    @staticmethod
    def create_nextflow(context: LDContext | None=None) -> LDNode:
        return LDComputerLanguage.create("https://w3id.org/workflowhub/workflow-ro-crate#nextflow", "Nextflow", None, "https://www.nextflow.io/", "https://www.nextflow.io/", context)

    @staticmethod
    def create_snakemake(context: LDContext | None=None) -> LDNode:
        return LDComputerLanguage.create("https://w3id.org/workflowhub/workflow-ro-crate#snakemake", "Snakemake", None, "https://doi.org/10.1093/bioinformatics/bts480", "https://snakemake.readthedocs.io", context)


LDComputerLanguage_reflection = _expr1724

__all__ = ["LDComputerLanguage_reflection"]

