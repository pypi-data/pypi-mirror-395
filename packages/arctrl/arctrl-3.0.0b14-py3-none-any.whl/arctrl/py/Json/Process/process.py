from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, singleton, of_array, FSharpList)
from ...fable_modules.fable_library.option import map
from ...fable_modules.fable_library.seq import map as map_1
from ...fable_modules.fable_library.string_ import replace
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, list_1 as list_1_2, IGetters)
from ...fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.comment import Comment
from ...Core.Process.process import Process
from ...Core.Process.process_input import ProcessInput
from ...Core.Process.process_output import ProcessOutput
from ...Core.Process.process_parameter_value import ProcessParameterValue
from ...Core.Process.protocol import Protocol
from ...Core.uri import URIModule_toString
from ..comment import (ROCrate_encoder as ROCrate_encoder_5, ROCrate_decoder as ROCrate_decoder_5, ISAJson_encoder as ISAJson_encoder_5, ISAJson_decoder as ISAJson_decoder_5)
from ..context.rocrate.isa_process_context import context_jsonvalue
from ..decode import Decode_uri
from ..encode import (try_include, try_include_list_opt)
from ..idtable import encode
from ..person import (ROCrate_encodeAuthorListString, ROCrate_decodeAuthorListString)
from .process_input import (ROCrate_encoder as ROCrate_encoder_3, ROCrate_decoder as ROCrate_decoder_3, ISAJson_encoder as ISAJson_encoder_3, ISAJson_decoder as ISAJson_decoder_3)
from .process_output import (ROCrate_encoder as ROCrate_encoder_4, ROCrate_decoder as ROCrate_decoder_4, ISAJson_encoder as ISAJson_encoder_4, ISAJson_decoder as ISAJson_decoder_4)
from .process_parameter_value import (ROCrate_encoder as ROCrate_encoder_2, ROCrate_decoder as ROCrate_decoder_2, ISAJson_encoder as ISAJson_encoder_2, ISAJson_decoder as ISAJson_decoder_2)
from .protocol import (ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_1, ISAJson_encoder as ISAJson_encoder_1, ISAJson_decoder as ISAJson_decoder_1)

__A_ = TypeVar("__A_")

def ROCrate_genID(p: Process) -> str:
    match_value: str | None = p.ID
    if match_value is None:
        match_value_1: str | None = p.Name
        if match_value_1 is None:
            return "#EmptyProcess"

        else: 
            return "#Process_" + replace(match_value_1, " ", "_")


    else: 
        return URIModule_toString(match_value)



def ROCrate_encoder(study_name: str | None, assay_name: str | None, oa: Process) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2940(__unit: None=None, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr2939(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2939()

    class ObjectExpr2941(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> Any:
            return helpers_1.encode_string("Process")

    def _arrow2943(value_2: str, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        class ObjectExpr2942(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr2942()

    def _arrow2944(oa_1: Protocol, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_1(study_name, assay_name, oa.Name, oa_1)

    def _arrow2945(author_list: str, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        return ROCrate_encodeAuthorListString(author_list)

    def _arrow2947(value_4: str, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        class ObjectExpr2946(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_4)

        return ObjectExpr2946()

    def _arrow2948(value_6: ProcessInput, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_3(value_6)

    def _arrow2949(value_7: ProcessOutput, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_4(value_7)

    def _arrow2950(comment: Comment, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_5(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2940()), ("@type", list_1_1(singleton(ObjectExpr2941()))), try_include("name", _arrow2943, oa.Name), try_include("executesProtocol", _arrow2944, oa.ExecutesProtocol), try_include_list_opt("parameterValues", ROCrate_encoder_2, oa.ParameterValues), try_include("performer", _arrow2945, oa.Performer), try_include("date", _arrow2947, oa.Date), try_include_list_opt("inputs", _arrow2948, oa.Inputs), try_include_list_opt("outputs", _arrow2949, oa.Outputs), try_include_list_opt("comments", _arrow2950, oa.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr2951(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr2951()


def _arrow2961(get: IGetters) -> Process:
    def _arrow2952(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow2953(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow2954(__unit: None=None) -> Protocol | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("executesProtocol", ROCrate_decoder_1)

    def _arrow2955(__unit: None=None) -> FSharpList[ProcessParameterValue] | None:
        arg_7: Decoder_1[FSharpList[ProcessParameterValue]] = list_1_2(ROCrate_decoder_2)
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("parameterValues", arg_7)

    def _arrow2956(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("performer", ROCrate_decodeAuthorListString)

    def _arrow2957(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("date", string)

    def _arrow2958(__unit: None=None) -> FSharpList[ProcessInput] | None:
        arg_13: Decoder_1[FSharpList[ProcessInput]] = list_1_2(ROCrate_decoder_3)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("inputs", arg_13)

    def _arrow2959(__unit: None=None) -> FSharpList[ProcessOutput] | None:
        arg_15: Decoder_1[FSharpList[ProcessOutput]] = list_1_2(ROCrate_decoder_4)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("outputs", arg_15)

    def _arrow2960(__unit: None=None) -> FSharpList[Comment] | None:
        arg_17: Decoder_1[FSharpList[Comment]] = list_1_2(ROCrate_decoder_5)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("comments", arg_17)

    return Process(_arrow2952(), _arrow2953(), _arrow2954(), _arrow2955(), _arrow2956(), _arrow2957(), None, None, _arrow2958(), _arrow2959(), _arrow2960())


ROCrate_decoder: Decoder_1[Process] = object(_arrow2961)

def ISAJson_encoder(study_name: str | None, assay_name: str | None, id_map: Any | None, oa: Process) -> IEncodable:
    def f(oa_1: Process, study_name: Any=study_name, assay_name: Any=assay_name, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], oa_1: Any=oa_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2965(value: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2964(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2964()

        def _arrow2967(value_2: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2966(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_2)

            return ObjectExpr2966()

        def _arrow2968(oa_2: Protocol, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_1(study_name, assay_name, oa_1.Name, id_map, oa_2)

        def _arrow2969(oa_3: ProcessParameterValue, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_2(id_map, oa_3)

        def _arrow2971(value_4: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2970(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_2.encode_string(value_4)

            return ObjectExpr2970()

        def _arrow2973(value_6: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2972(IEncodable):
                def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_3.encode_string(value_6)

            return ObjectExpr2972()

        def _arrow2974(oa_4: Process, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder(study_name, assay_name, id_map, oa_4)

        def _arrow2975(oa_5: Process, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder(study_name, assay_name, id_map, oa_5)

        def _arrow2976(value_8: ProcessInput, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_3(id_map, value_8)

        def _arrow2977(value_9: ProcessOutput, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_4(id_map, value_9)

        def _arrow2978(comment: Comment, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_5(id_map, comment)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2965, ROCrate_genID(oa_1)), try_include("name", _arrow2967, oa_1.Name), try_include("executesProtocol", _arrow2968, oa_1.ExecutesProtocol), try_include_list_opt("parameterValues", _arrow2969, oa_1.ParameterValues), try_include("performer", _arrow2971, oa_1.Performer), try_include("date", _arrow2973, oa_1.Date), try_include("previousProcess", _arrow2974, oa_1.PreviousProcess), try_include("nextProcess", _arrow2975, oa_1.NextProcess), try_include_list_opt("inputs", _arrow2976, oa_1.Inputs), try_include_list_opt("outputs", _arrow2977, oa_1.Outputs), try_include_list_opt("comments", _arrow2978, oa_1.Comments)]))
        class ObjectExpr2979(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any], oa_1: Any=oa_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_4.encode_object(arg)

        return ObjectExpr2979()

    if id_map is not None:
        def _arrow2980(p: Process, study_name: Any=study_name, assay_name: Any=assay_name, id_map: Any=id_map, oa: Any=oa) -> str:
            return ROCrate_genID(p)

        return encode(_arrow2980, f, oa, id_map)

    else: 
        return f(oa)



def _arrow2993(__unit: None=None) -> Decoder_1[Process]:
    def decode(__unit: None=None) -> Decoder_1[Process]:
        def _arrow2992(get: IGetters) -> Process:
            def _arrow2981(__unit: None=None) -> str | None:
                object_arg: IOptionalGetter = get.Optional
                return object_arg.Field("@id", Decode_uri)

            def _arrow2982(__unit: None=None) -> str | None:
                object_arg_1: IOptionalGetter = get.Optional
                return object_arg_1.Field("name", string)

            def _arrow2983(__unit: None=None) -> Protocol | None:
                object_arg_2: IOptionalGetter = get.Optional
                return object_arg_2.Field("executesProtocol", ISAJson_decoder_1)

            def _arrow2984(__unit: None=None) -> FSharpList[ProcessParameterValue] | None:
                arg_7: Decoder_1[FSharpList[ProcessParameterValue]] = list_1_2(ISAJson_decoder_2)
                object_arg_3: IOptionalGetter = get.Optional
                return object_arg_3.Field("parameterValues", arg_7)

            def _arrow2985(__unit: None=None) -> str | None:
                object_arg_4: IOptionalGetter = get.Optional
                return object_arg_4.Field("performer", string)

            def _arrow2986(__unit: None=None) -> str | None:
                object_arg_5: IOptionalGetter = get.Optional
                return object_arg_5.Field("date", string)

            def _arrow2987(__unit: None=None) -> Process | None:
                arg_13: Decoder_1[Process] = decode(None)
                object_arg_6: IOptionalGetter = get.Optional
                return object_arg_6.Field("previousProcess", arg_13)

            def _arrow2988(__unit: None=None) -> Process | None:
                arg_15: Decoder_1[Process] = decode(None)
                object_arg_7: IOptionalGetter = get.Optional
                return object_arg_7.Field("nextProcess", arg_15)

            def _arrow2989(__unit: None=None) -> FSharpList[ProcessInput] | None:
                arg_17: Decoder_1[FSharpList[ProcessInput]] = list_1_2(ISAJson_decoder_3)
                object_arg_8: IOptionalGetter = get.Optional
                return object_arg_8.Field("inputs", arg_17)

            def _arrow2990(__unit: None=None) -> FSharpList[ProcessOutput] | None:
                arg_19: Decoder_1[FSharpList[ProcessOutput]] = list_1_2(ISAJson_decoder_4)
                object_arg_9: IOptionalGetter = get.Optional
                return object_arg_9.Field("outputs", arg_19)

            def _arrow2991(__unit: None=None) -> FSharpList[Comment] | None:
                arg_21: Decoder_1[FSharpList[Comment]] = list_1_2(ISAJson_decoder_5)
                object_arg_10: IOptionalGetter = get.Optional
                return object_arg_10.Field("comments", arg_21)

            return Process(_arrow2981(), _arrow2982(), _arrow2983(), _arrow2984(), _arrow2985(), _arrow2986(), _arrow2987(), _arrow2988(), _arrow2989(), _arrow2990(), _arrow2991())

        return object(_arrow2992)

    return decode(None)


ISAJson_decoder: Decoder_1[Process] = _arrow2993()

__all__ = ["ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_decoder"]

