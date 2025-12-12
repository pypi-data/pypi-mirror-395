from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ...fable_modules.fable_library.option import (map, default_arg)
from ...fable_modules.fable_library.seq import map as map_1
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, resize_array, IGetters)
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.comment import Comment
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Process.factor import Factor
from ..comment import (ISAJson_encoder, ISAJson_decoder)
from ..encode import (try_include, try_include_seq)
from ..idtable import encode
from ..ontology_annotation import (OntologyAnnotation_ROCrate_genID, OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)

__A_ = TypeVar("__A_")

def gen_id(f: Factor) -> str:
    match_value: str | None = f.Name
    if match_value is None:
        match_value_1: OntologyAnnotation | None = f.FactorType
        if match_value_1 is None:
            return "#EmptyFactor"

        else: 
            return ("#Factor/" + OntologyAnnotation_ROCrate_genID(match_value_1)) + ""


    else: 
        return ("#Factor/" + match_value) + ""



def encoder(id_map: Any | None, value: Factor) -> IEncodable:
    def f_1(value_1: Factor, id_map: Any=id_map, value: Any=value) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], value_1: Any=value_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2552(value_2: str, value_1: Any=value_1) -> IEncodable:
            class ObjectExpr2551(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value_2)

            return ObjectExpr2551()

        def _arrow2554(value_4: str, value_1: Any=value_1) -> IEncodable:
            class ObjectExpr2553(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_4)

            return ObjectExpr2553()

        def _arrow2555(oa: OntologyAnnotation, value_1: Any=value_1) -> IEncodable:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa)

        def _arrow2556(comment: Comment, value_1: Any=value_1) -> IEncodable:
            return ISAJson_encoder(id_map, comment)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2552, gen_id(value_1)), try_include("factorName", _arrow2554, value_1.Name), try_include("factorType", _arrow2555, value_1.FactorType), try_include_seq("comments", _arrow2556, default_arg(value_1.Comments, []))]))
        class ObjectExpr2557(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], value_1: Any=value_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_2.encode_object(arg)

        return ObjectExpr2557()

    if id_map is not None:
        def _arrow2558(f_2: Factor, id_map: Any=id_map, value: Any=value) -> str:
            return gen_id(f_2)

        return encode(_arrow2558, f_1, value, id_map)

    else: 
        return f_1(value)



def _arrow2562(get: IGetters) -> Factor:
    def _arrow2559(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("factorName", string)

    def _arrow2560(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("factorType", OntologyAnnotation_ISAJson_decoder)

    def _arrow2561(__unit: None=None) -> Array[Comment] | None:
        arg_5: Decoder_1[Array[Comment]] = resize_array(ISAJson_decoder)
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("comments", arg_5)

    return Factor(_arrow2559(), _arrow2560(), _arrow2561())


decoder: Decoder_1[Factor] = object(_arrow2562)

__all__ = ["gen_id", "encoder", "decoder"]

