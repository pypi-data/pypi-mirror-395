from typing import Any
from ..Json.decode import Decode_datetime
from ..Json.encode import date_time
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string as to_string_1
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf)

def try_from_string(s: str) -> Any | None:
    try: 
        def _arrow3874(__unit: None=None) -> Any:
            match_value: FSharpResult_2[Any, str] = Decode_fromString(Decode_datetime, s)
            if match_value.tag == 1:
                raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

            else: 
                return match_value.fields[0]


        return _arrow3874()

    except Exception as match_value_1:
        return None



def to_string(d: Any) -> str:
    return to_string_1(0, date_time(d))


__all__ = ["try_from_string", "to_string"]

