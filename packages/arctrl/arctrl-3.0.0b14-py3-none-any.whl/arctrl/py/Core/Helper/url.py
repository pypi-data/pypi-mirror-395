from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.util import to_enumerable
from .collections_ import (Dictionary_ofSeq, Dictionary_tryFind)

def OntobeeParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "http://purl.obolibrary.org/obo/") + "") + tsr) + "_") + local_tan) + ""


def BioregistryParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://bioregistry.io/") + "") + tsr) + ":") + local_tan) + ""


def OntobeeDPBOParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "http://purl.org/nfdi4plants/ontology/dpbo/") + "") + tsr) + "_") + local_tan) + ""


def MSParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://www.ebi.ac.uk/ols4/ontologies/ms/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F") + "") + tsr) + "_") + local_tan) + ""


def POParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://www.ebi.ac.uk/ols4/ontologies/po/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F") + "") + tsr) + "_") + local_tan) + ""


def ROParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://www.ebi.ac.uk/ols4/ontologies/ro/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F") + "") + tsr) + "_") + local_tan) + ""


def _arrow608(tsr: str) -> Callable[[str], str]:
    def _arrow607(local_tan: str) -> str:
        return OntobeeDPBOParser(tsr, local_tan)

    return _arrow607


def _arrow610(tsr_1: str) -> Callable[[str], str]:
    def _arrow609(local_tan_1: str) -> str:
        return MSParser(tsr_1, local_tan_1)

    return _arrow609


def _arrow612(tsr_2: str) -> Callable[[str], str]:
    def _arrow611(local_tan_2: str) -> str:
        return POParser(tsr_2, local_tan_2)

    return _arrow611


def _arrow614(tsr_3: str) -> Callable[[str], str]:
    def _arrow613(local_tan_3: str) -> str:
        return ROParser(tsr_3, local_tan_3)

    return _arrow613


def _arrow616(tsr_4: str) -> Callable[[str], str]:
    def _arrow615(local_tan_4: str) -> str:
        return BioregistryParser(tsr_4, local_tan_4)

    return _arrow615


def _arrow618(tsr_5: str) -> Callable[[str], str]:
    def _arrow617(local_tan_5: str) -> str:
        return BioregistryParser(tsr_5, local_tan_5)

    return _arrow617


def _arrow620(tsr_6: str) -> Callable[[str], str]:
    def _arrow619(local_tan_6: str) -> str:
        return BioregistryParser(tsr_6, local_tan_6)

    return _arrow619


def _arrow622(tsr_7: str) -> Callable[[str], str]:
    def _arrow621(local_tan_7: str) -> str:
        return BioregistryParser(tsr_7, local_tan_7)

    return _arrow621


def _arrow624(tsr_8: str) -> Callable[[str], str]:
    def _arrow623(local_tan_8: str) -> str:
        return BioregistryParser(tsr_8, local_tan_8)

    return _arrow623


def _arrow626(tsr_9: str) -> Callable[[str], str]:
    def _arrow625(local_tan_9: str) -> str:
        return BioregistryParser(tsr_9, local_tan_9)

    return _arrow625


def _arrow628(tsr_10: str) -> Callable[[str], str]:
    def _arrow627(local_tan_10: str) -> str:
        return BioregistryParser(tsr_10, local_tan_10)

    return _arrow627


def _arrow630(tsr_11: str) -> Callable[[str], str]:
    def _arrow629(local_tan_11: str) -> str:
        return BioregistryParser(tsr_11, local_tan_11)

    return _arrow629


def _arrow632(tsr_12: str) -> Callable[[str], str]:
    def _arrow631(local_tan_12: str) -> str:
        return BioregistryParser(tsr_12, local_tan_12)

    return _arrow631


def _arrow634(tsr_13: str) -> Callable[[str], str]:
    def _arrow633(local_tan_13: str) -> str:
        return BioregistryParser(tsr_13, local_tan_13)

    return _arrow633


def _arrow636(tsr_14: str) -> Callable[[str], str]:
    def _arrow635(local_tan_14: str) -> str:
        return BioregistryParser(tsr_14, local_tan_14)

    return _arrow635


uri_parser_collection: Any = Dictionary_ofSeq(to_enumerable([("DPBO", _arrow608), ("MS", _arrow610), ("PO", _arrow612), ("RO", _arrow614), ("ENVO", _arrow616), ("CHEBI", _arrow618), ("GO", _arrow620), ("OBI", _arrow622), ("PATO", _arrow624), ("PECO", _arrow626), ("TO", _arrow628), ("UO", _arrow630), ("EFO", _arrow632), ("NCIT", _arrow634), ("OMP", _arrow636)]))

def create_oauri(tsr: str, local_tan: str) -> str:
    match_value: Callable[[str, str], str] | None = Dictionary_tryFind(tsr, uri_parser_collection)
    if match_value is None:
        return OntobeeParser(tsr, local_tan)

    else: 
        return match_value(tsr)(local_tan)



__all__ = ["OntobeeParser", "BioregistryParser", "OntobeeDPBOParser", "MSParser", "POParser", "ROParser", "uri_parser_collection", "create_oauri"]

