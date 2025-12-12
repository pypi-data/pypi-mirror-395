from __future__ import annotations
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, FSharpList, is_empty, length, head)
from ...fable_modules.fable_library.option import map
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.seq import (to_list, delay, append, singleton, collect, empty, map as map_1)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (IEnumerable_1, get_enumerator, dispose)
from ...fable_modules.thoth_json_core.decode import (Getters_2__ctor_Z4BE6C149, Getters_2, IGetters, IOptionalGetter, string, resize_array, IRequiredGetter, Getters_2__get_Errors)
from ...fable_modules.thoth_json_core.encode import seq
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1, ErrorReason_1, IDecoderHelpers_1)
from ...ROCrate.ldcontext import LDContext
from ...ROCrate.ldobject import (LDNode, LDGraph)
from ..encode import try_include
from .ldcontext import (encoder as encoder_1, decoder as decoder_1)
from .ldnode import (generic_encoder, encoder as encoder_2, decoder as decoder_2, generic_decoder)

__A_ = TypeVar("__A_")

def encoder(obj: LDGraph) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], obj: Any=obj) -> tuple[str, IEncodable] | None:
        def mapping_1(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping_1, tupled_arg[1])

    def _arrow2212(__unit: None=None, obj: Any=obj) -> IEnumerable_1[tuple[str, IEncodable | None]]:
        def _arrow2207(value: str) -> IEncodable:
            class ObjectExpr2206(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2206()

        def _arrow2211(__unit: None=None) -> IEnumerable_1[tuple[str, IEncodable | None]]:
            def _arrow2210(__unit: None=None) -> IEnumerable_1[tuple[str, IEncodable | None]]:
                def _arrow2208(kv: Any) -> IEnumerable_1[tuple[str, IEncodable | None]]:
                    l: str = kv[0].lower()
                    return singleton((kv[0], generic_encoder(kv[1]))) if ((l != "mappings") if ((l != "nodes") if ((l != "@context") if (l != "id") else False) else False) else False) else empty()

                def _arrow2209(__unit: None=None) -> IEnumerable_1[tuple[str, IEncodable | None]]:
                    return singleton(("@graph", seq(map_1(encoder_2, obj.Nodes))))

                return append(collect(_arrow2208, obj.GetProperties(True)), delay(_arrow2209))

            return append(singleton(try_include("@context", encoder_1, obj.TryGetContext())), delay(_arrow2210))

        return append(singleton(try_include("@id", _arrow2207, obj.Id)), delay(_arrow2211))

    values_1: FSharpList[tuple[str, IEncodable]] = choose(chooser, to_list(delay(_arrow2212)))
    class ObjectExpr2213(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], obj: Any=obj) -> Any:
            def mapping_2(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_1))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_2, values_1)
            return helpers_1.encode_object(arg)

    return ObjectExpr2213()


class ObjectExpr2215(Decoder_1[LDGraph]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value: Any) -> FSharpResult_2[LDGraph, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_object(value):
            getters: Getters_2[__A_, Any] = Getters_2__ctor_Z4BE6C149(helpers, value)
            properties: IEnumerable_1[str] = helpers.get_properties(value)
            result: LDGraph
            get: IGetters = getters
            id: str | None
            object_arg: IOptionalGetter = get.Optional
            id = object_arg.Field("@id", string)
            context: LDContext | None
            object_arg_1: IOptionalGetter = get.Optional
            context = object_arg_1.Field("@context", decoder_1)
            nodes: Array[LDNode]
            arg_5: Decoder_1[Array[LDNode]] = resize_array(decoder_2)
            object_arg_2: IRequiredGetter = get.Required
            nodes = object_arg_2.Field("@graph", arg_5)
            o: LDGraph = LDGraph(id, None, context)
            with get_enumerator(properties) as enumerator:
                while enumerator.System_Collections_IEnumerator_MoveNext():
                    property: str = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                    if (property != "@context") if ((property != "@graph") if (property != "@id") else False) else False:
                        def _arrow2214(__unit: None=None) -> Any:
                            object_arg_3: IRequiredGetter = get.Required
                            return object_arg_3.Field(property, generic_decoder)

                        o.SetProperty(property, _arrow2214())

            enumerator_1: Any = get_enumerator(nodes)
            try: 
                while enumerator_1.System_Collections_IEnumerator_MoveNext():
                    node: LDNode = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                    o.AddNode(node)

            finally: 
                dispose(enumerator_1)

            result = o
            match_value: FSharpList[tuple[str, ErrorReason_1[__A_]]] = Getters_2__get_Errors(getters)
            if not is_empty(match_value):
                errors: FSharpList[tuple[str, ErrorReason_1[__A_]]] = match_value
                return FSharpResult_2(1, ("", ErrorReason_1(7, errors))) if (length(errors) > 1) else FSharpResult_2(1, head(match_value))

            else: 
                return FSharpResult_2(0, result)


        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "an object", value)))



decoder: Decoder_1[LDGraph] = ObjectExpr2215()

__all__ = ["encoder", "decoder"]

