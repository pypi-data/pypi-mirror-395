from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (singleton, FSharpList)
from ..fable_modules.fable_library.map_util import add_to_dict
from ..fable_modules.fable_library.seq import map
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

_VALUE = TypeVar("_VALUE")

def encode_id(id: str) -> IEncodable:
    class ObjectExpr2204(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], id: Any=id) -> Any:
            return helpers.encode_string(id)

    values: FSharpList[tuple[str, IEncodable]] = singleton(("@id", ObjectExpr2204()))
    class ObjectExpr2205(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], id: Any=id) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_1))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_1.encode_object(arg)

    return ObjectExpr2205()


def encode(gen_id: Callable[[_VALUE], str], encoder: Callable[[_VALUE], IEncodable], value: Any, table: Any) -> IEncodable:
    id: str = gen_id(value)
    if id in table:
        return encode_id(id)

    else: 
        v: IEncodable = encoder(value)
        add_to_dict(table, gen_id(value), v)
        return v



__all__ = ["encode_id", "encode"]

