from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Table.composite_cell import CompositeCell
from ...Core.template import Template
from ...Json.encode import default_spaces
from ...Json.Table.templates import (Template_encoder, Template_decoder, Template_decoderCompressed, Template_encoderCompressed)
from ...fable_modules.fable_library.array_ import map
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (to_fail, printf, to_text)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.thoth_json_core.decode import array as array_2
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string
from .compression import (decode, encode)

__A_ = TypeVar("__A_")

def Templates_encoder(templates: Array[Template]) -> IEncodable:
    def mapping(template: Template, templates: Any=templates) -> IEncodable:
        return Template_encoder(template)

    values: Array[IEncodable] = map(mapping, templates, None)
    class ObjectExpr3849(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], templates: Any=templates) -> Any:
            def mapping_1(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map(mapping_1, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr3849()


Templates_decoder: Decoder_1[Array[Template]] = array_2(Template_decoder)

def Templates_fromJsonString(json_string: str) -> Array[Template]:
    try: 
        match_value: FSharpResult_2[Array[Template], str] = Decode_fromString(Templates_decoder, json_string)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as exn:
        return to_fail(printf("Error. Given json string cannot be parsed to Templates map: %A"))(exn)



def Templates_toJsonString(spaces: int, templates: Array[Template]) -> str:
    return to_string(spaces, Templates_encoder(templates))


def ARCtrl_Template__Template_fromJsonString_Static_Z721C83C5(json_string: str) -> Template:
    try: 
        match_value: FSharpResult_2[Template, str] = Decode_fromString(Template_decoder, json_string)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as exn:
        return to_fail(printf("Error. Given json string cannot be parsed to Template: %A"))(exn)



def ARCtrl_Template__Template_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Template], str]:
    def _arrow3850(template: Template, spaces: Any=spaces) -> str:
        return to_string(default_spaces(spaces), Template_encoder(template))

    return _arrow3850


def ARCtrl_Template__Template_toJsonString_71136F3F(this: Template, spaces: int | None=None) -> str:
    return ARCtrl_Template__Template_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_Template__Template_fromCompressedJsonString_Static_Z721C83C5(s: str) -> Template:
    try: 
        match_value: FSharpResult_2[Template, str] = Decode_fromString(decode(Template_decoderCompressed), s)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as e_1:
        arg_1: str = str(e_1)
        return to_fail(printf("Error. Unable to parse json string to ArcStudy: %s"))(arg_1)



def ARCtrl_Template__Template_toCompressedJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Template], str]:
    def _arrow3851(obj: Template, spaces: Any=spaces) -> str:
        return to_string(default_arg(spaces, 0), encode(Template_encoderCompressed, obj))

    return _arrow3851


def ARCtrl_Template__Template_toCompressedJsonString_71136F3F(this: Template, spaces: int | None=None) -> str:
    return ARCtrl_Template__Template_toCompressedJsonString_Static_71136F3F(spaces)(this)


__all__ = ["Templates_encoder", "Templates_decoder", "Templates_fromJsonString", "Templates_toJsonString", "ARCtrl_Template__Template_fromJsonString_Static_Z721C83C5", "ARCtrl_Template__Template_toJsonString_Static_71136F3F", "ARCtrl_Template__Template_toJsonString_71136F3F", "ARCtrl_Template__Template_fromCompressedJsonString_Static_Z721C83C5", "ARCtrl_Template__Template_toCompressedJsonString_Static_71136F3F", "ARCtrl_Template__Template_toCompressedJsonString_71136F3F"]

