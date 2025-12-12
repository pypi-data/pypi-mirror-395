from typing import Any
from ...fable_modules.fable_library.reg_exp import (create, match)
from .regex import ActivePatterns__007CRegex_007C__007C

orcid_regex: Any = create("[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]")

def try_get_orcid_number(orcid: str) -> str | None:
    m: Any = match(orcid_regex, orcid)
    if m is not None:
        return m[0]

    else: 
        return None



orcid_prefix: str = "http://orcid.org/"

def _007CORCID_007C__007C(input: str) -> str | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]", input)
    if active_pattern_result is not None:
        r: Any = active_pattern_result
        return r[0]

    else: 
        return None



def try_get_orcid_url(orcid: str) -> str | None:
    active_pattern_result: str | None = _007CORCID_007C__007C(orcid)
    if active_pattern_result is not None:
        orcid_1: str = active_pattern_result
        return ((("" + orcid_prefix) + "") + orcid_1) + ""

    else: 
        return None



__all__ = ["orcid_regex", "try_get_orcid_number", "orcid_prefix", "_007CORCID_007C__007C", "try_get_orcid_url"]

