from __future__ import annotations
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (FSharpList, choose, of_array)
from ...fable_modules.fable_library.option import map
from ...fable_modules.fable_library.seq import map as map_1
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)
from ...Core.Process.material import Material
from ...Core.Process.process import Process
from ...Core.Process.process_sequence import (get_samples, get_materials)
from ...Core.Process.sample import Sample
from ..encode import try_include_list
from .material import ISAJson_encoder as ISAJson_encoder_1
from .sample import ISAJson_encoder

__A_ = TypeVar("__A_")

def encoder(id_map: Any | None, ps: FSharpList[Process]) -> IEncodable:
    samples: FSharpList[Sample] = get_samples(ps)
    materials: FSharpList[Material] = get_materials(ps)
    def chooser(tupled_arg: tuple[str, IEncodable | None], id_map: Any=id_map, ps: Any=ps) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2929(oa: Sample, id_map: Any=id_map, ps: Any=ps) -> IEncodable:
        return ISAJson_encoder(id_map, oa)

    def _arrow2930(c: Material, id_map: Any=id_map, ps: Any=ps) -> IEncodable:
        return ISAJson_encoder_1(id_map, c)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include_list("samples", _arrow2929, samples), try_include_list("otherMaterials", _arrow2930, materials)]))
    class ObjectExpr2931(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], id_map: Any=id_map, ps: Any=ps) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers.encode_object(arg)

    return ObjectExpr2931()


__all__ = ["encoder"]

