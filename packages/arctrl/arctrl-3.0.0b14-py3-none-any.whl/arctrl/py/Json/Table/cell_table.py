from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.array_ import map as map_1
from ...fable_modules.fable_library.map_util import add_to_dict
from ...fable_modules.fable_library.seq import (to_array, map, sort_by)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import compare_primitives
from ...fable_modules.thoth_json_core.decode import (array as array_2, object, int_1, IGetters)
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.Helper.collections_ import (Dictionary_items, Dictionary_tryFind)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Table.composite_cell import CompositeCell
from .composite_cell import (encoder_compressed, decoder_compressed)

__A_ = TypeVar("__A_")

def array_from_map(otm: Any) -> Array[CompositeCell]:
    def mapping(kv_1: Any, otm: Any=otm) -> CompositeCell:
        return kv_1[0]

    def projection(kv: Any, otm: Any=otm) -> int:
        return kv[1]

    class ObjectExpr3018:
        @property
        def Compare(self) -> Callable[[int, int], int]:
            return compare_primitives

    return to_array(map(mapping, sort_by(projection, Dictionary_items(otm), ObjectExpr3018())))


def encoder(string_table: Any, oa_table: Any, ot: Array[CompositeCell]) -> IEncodable:
    def mapping(cc: CompositeCell, string_table: Any=string_table, oa_table: Any=oa_table, ot: Any=ot) -> IEncodable:
        return encoder_compressed(string_table, oa_table, cc)

    values: Array[IEncodable] = map_1(mapping, ot, None)
    class ObjectExpr3019(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], string_table: Any=string_table, oa_table: Any=oa_table, ot: Any=ot) -> Any:
            def mapping_1(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_1(mapping_1, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr3019()


def decoder(string_table: Array[str], oa_table: Array[OntologyAnnotation]) -> Decoder_1[Array[CompositeCell]]:
    return array_2(decoder_compressed(string_table, oa_table))


def encode_cell(otm: Any, cc: CompositeCell) -> IEncodable:
    match_value: int | None = Dictionary_tryFind(cc, otm)
    if match_value is None:
        i_1: int = len(otm) or 0
        add_to_dict(otm, cc, i_1)
        class ObjectExpr3020(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], otm: Any=otm, cc: Any=cc) -> Any:
                return helpers_1.encode_signed_integral_number(i_1)

        return ObjectExpr3020()

    else: 
        i: int = match_value or 0
        class ObjectExpr3021(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], otm: Any=otm, cc: Any=cc) -> Any:
                return helpers.encode_signed_integral_number(i)

        return ObjectExpr3021()



def decode_cell(ot: Array[CompositeCell]) -> Decoder_1[CompositeCell]:
    def _arrow3022(get: IGetters, ot: Any=ot) -> CompositeCell:
        i: int = get.Required.Raw(int_1) or 0
        return ot[i].Copy()

    return object(_arrow3022)


__all__ = ["array_from_map", "encoder", "decoder", "encode_cell", "decode_cell"]

