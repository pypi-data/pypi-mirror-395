from __future__ import annotations
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (FSharpList, is_empty, length, head)
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.seq import (map, append, to_list, delay, singleton, empty)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (IEnumerable_1, get_enumerator)
from ...fable_modules.thoth_json_core.decode import (Getters_2__ctor_Z4BE6C149, Getters_2, IRequiredGetter, string, Getters_2__get_Errors, resize_array)
from ...fable_modules.thoth_json_core.encode import seq
from ...fable_modules.thoth_json_core.types import (Decoder_1, ErrorReason_1, IDecoderHelpers_1, IEncodable, IEncoderHelpers_1)
from ...ROCrate.ldcontext import LDContext
from ...ROCrate.rocrate_context import (init_v1_2, init_v1_1)

__A_ = TypeVar("__A_")

class ObjectExpr2157(Decoder_1[LDContext]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value: Any) -> FSharpResult_2[LDContext, tuple[str, ErrorReason_1[__A_]]]:
        this: Decoder_1[LDContext] = self
        if helpers.is_object(value):
            getters: Getters_2[__A_, Any] = Getters_2__ctor_Z4BE6C149(helpers, value)
            properties: IEnumerable_1[str] = helpers.get_properties(value)
            result: LDContext
            o: LDContext = LDContext()
            with get_enumerator(properties) as enumerator:
                while enumerator.System_Collections_IEnumerator_MoveNext():
                    property: str = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                    if (property != "@type") if (property != "@id") else False:
                        def _arrow2156(__unit: None=None) -> str:
                            object_arg: IRequiredGetter = getters.Required
                            return object_arg.Field(property, string)

                        o.AddMapping(property, _arrow2156())

            result = o
            match_value: FSharpList[tuple[str, ErrorReason_1[__A_]]] = Getters_2__get_Errors(getters)
            if not is_empty(match_value):
                errors: FSharpList[tuple[str, ErrorReason_1[__A_]]] = match_value
                return FSharpResult_2(1, ("", ErrorReason_1(7, errors))) if (length(errors) > 1) else FSharpResult_2(1, head(match_value))

            else: 
                return FSharpResult_2(0, result)


        elif helpers.is_string(value):
            s: str = helpers.as_string(value)
            return FSharpResult_2(0, init_v1_2()) if (True if (s == "https://w3id.org/ro/crate/1.2-DRAFT/context") else (s == "https://w3id.org/ro/crate/1.2/context")) else (FSharpResult_2(0, init_v1_1()) if (s == "https://w3id.org/ro/crate/1.1/context") else FSharpResult_2(1, ("", ErrorReason_1(0, "an object", value))))

        elif helpers.is_array(value):
            match_value_1: FSharpResult_2[Array[LDContext], tuple[str, ErrorReason_1[__A_]]] = resize_array(this).Decode(helpers, value)
            return FSharpResult_2(1, match_value_1.fields[0]) if (match_value_1.tag == 1) else FSharpResult_2(0, LDContext(None, match_value_1.fields[0]))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "an object", value)))



decoder: Decoder_1[LDContext] = ObjectExpr2157()

def encoder(ctx_mut: LDContext) -> IEncodable:
    while True:
        (ctx,) = (ctx_mut,)
        match_value: str | None = ctx.Name
        (pattern_matching_result,) = (None,)
        if match_value is not None:
            if match_value == "https://w3id.org/ro/crate/1.2-DRAFT/context":
                pattern_matching_result = 0

            elif match_value == "https://w3id.org/ro/crate/1.2/context":
                pattern_matching_result = 1

            elif match_value == "https://w3id.org/ro/crate/1.1/context":
                pattern_matching_result = 2

            else: 
                pattern_matching_result = 3


        else: 
            pattern_matching_result = 3

        if pattern_matching_result == 0:
            class ObjectExpr2158(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any], ctx: Any=ctx) -> Any:
                    return helpers.encode_string("https://w3id.org/ro/crate/1.2-DRAFT/context")

            return ObjectExpr2158()

        elif pattern_matching_result == 1:
            class ObjectExpr2159(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any], ctx: Any=ctx) -> Any:
                    return helpers_1.encode_string("https://w3id.org/ro/crate/1.2/context")

            return ObjectExpr2159()

        elif pattern_matching_result == 2:
            class ObjectExpr2160(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any], ctx: Any=ctx) -> Any:
                    return helpers_2.encode_string("https://w3id.org/ro/crate/1.1/context")

            return ObjectExpr2160()

        elif pattern_matching_result == 3:
            mappings: IEncodable
            def mapping(kv: Any, ctx: Any=ctx) -> tuple[str, IEncodable]:
                class ObjectExpr2161(IEncodable):
                    def Encode(self, helpers_3: IEncoderHelpers_1[Any], kv: Any=kv) -> Any:
                        return helpers_3.encode_string(kv[1])

                return (kv[0], ObjectExpr2161())

            values: IEnumerable_1[tuple[str, IEncodable]] = map(mapping, ctx.Mappings)
            class ObjectExpr2162(IEncodable):
                def Encode(self, helpers_4: IEncoderHelpers_1[Any], ctx: Any=ctx) -> Any:
                    def mapping_1(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                        return (tupled_arg[0], tupled_arg[1].Encode(helpers_4))

                    arg: IEnumerable_1[tuple[str, __A_]] = map(mapping_1, values)
                    return helpers_4.encode_object(arg)

            mappings = ObjectExpr2162()
            if len(ctx.BaseContexts) == 0:
                return mappings

            elif (len(ctx.Mappings) == 0) if (len(ctx.BaseContexts) == 1) else False:
                ctx_mut = ctx.BaseContexts[0]
                continue

            else: 
                def _arrow2164(__unit: None=None, ctx: Any=ctx) -> IEnumerable_1[IEncodable]:
                    source_4: IEnumerable_1[IEncodable] = map(encoder, ctx.BaseContexts)
                    def _arrow2163(__unit: None=None) -> IEnumerable_1[IEncodable]:
                        return singleton(mappings) if (len(ctx.Mappings) != 0) else empty()

                    return append(to_list(delay(_arrow2163)), source_4)

                return seq(_arrow2164())


        break


__all__ = ["decoder", "encoder"]

