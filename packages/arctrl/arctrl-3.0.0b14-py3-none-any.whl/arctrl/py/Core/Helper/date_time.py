from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.date import (min_value, try_parse as try_parse_1)
from ...fable_modules.fable_library.types import FSharpRef

def try_parse(s: str) -> Any | None:
    match_value: tuple[bool, Any]
    out_arg: Any = min_value()
    def _arrow601(__unit: None=None, s: Any=s) -> Any:
        return out_arg

    def _arrow602(v: Any, s: Any=s) -> None:
        nonlocal out_arg
        out_arg = v

    match_value = (try_parse_1(s, FSharpRef(_arrow601, _arrow602)), out_arg)
    if match_value[0]:
        return match_value[1]

    else: 
        return None



__all__ = ["try_parse"]

