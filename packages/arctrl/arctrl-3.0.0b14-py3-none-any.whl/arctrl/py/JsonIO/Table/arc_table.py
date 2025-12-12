from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...Core.Helper.collections_ import Dictionary_init
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Table.arc_table import ArcTable
from ...Core.Table.composite_cell import CompositeCell
from ...Json.encode import default_spaces
from ...Json.string_table import (decoder as decoder_3, encoder as encoder_3, array_from_map as array_from_map_2)
from ...Json.Table.arc_table import (decoder as decoder_2, encoder, decoder_compressed, encoder_compressed)
from ...Json.Table.cell_table import (decoder as decoder_5, encoder as encoder_1, array_from_map)
from ...Json.Table.oatable import (decoder as decoder_4, encoder as encoder_2, array_from_map as array_from_map_1)
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.seq import map
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ...fable_modules.thoth_json_core.decode import (object, IRequiredGetter, IGetters)
from ...fable_modules.thoth_json_core.types import (IEncodable, Decoder_1, IEncoderHelpers_1)
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string

__A_ = TypeVar("__A_")

def ARCtrl_ArcTable__ArcTable_fromJsonString_Static_Z721C83C5(s: str) -> ArcTable:
    match_value: FSharpResult_2[ArcTable, str] = Decode_fromString(decoder_2, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcTable__ArcTable_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcTable], str]:
    def _arrow3843(obj: ArcTable, spaces: Any=spaces) -> str:
        value: IEncodable = encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3843


def ARCtrl_ArcTable__ArcTable_ToJsonString_71136F3F(this: ArcTable, spaces: int | None=None) -> str:
    return ARCtrl_ArcTable__ArcTable_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcTable__ArcTable_fromCompressedJsonString_Static_Z721C83C5(json_string: str) -> ArcTable:
    def _arrow3845(get: IGetters, json_string: Any=json_string) -> ArcTable:
        string_table: Array[str]
        object_arg: IRequiredGetter = get.Required
        string_table = object_arg.Field("stringTable", decoder_3)
        oa_table: Array[OntologyAnnotation]
        arg_3: Decoder_1[Array[OntologyAnnotation]] = decoder_4(string_table)
        object_arg_1: IRequiredGetter = get.Required
        oa_table = object_arg_1.Field("oaTable", arg_3)
        def _arrow3844(__unit: None=None) -> Array[CompositeCell]:
            arg_5: Decoder_1[Array[CompositeCell]] = decoder_5(string_table, oa_table)
            object_arg_2: IRequiredGetter = get.Required
            return object_arg_2.Field("cellTable", arg_5)

        arg_7: Decoder_1[ArcTable] = decoder_compressed(string_table, oa_table, _arrow3844())
        object_arg_3: IRequiredGetter = get.Required
        return object_arg_3.Field("table", arg_7)

    match_value: FSharpResult_2[ArcTable, str] = Decode_fromString(object(_arrow3845), json_string)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcTable__ArcTable_ToCompressedJsonString_71136F3F(this: ArcTable, spaces: int | None=None) -> str:
    spaces_1: int = default_spaces(spaces) or 0
    string_table: Any = Dictionary_init()
    oa_table: Any = Dictionary_init()
    cell_table: Any = Dictionary_init()
    arc_table: IEncodable = encoder_compressed(string_table, oa_table, cell_table, this)
    def _arrow3847(__unit: None=None, this: Any=this, spaces: Any=spaces) -> IEncodable:
        values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("cellTable", encoder_1(string_table, oa_table, array_from_map(cell_table))), ("oaTable", encoder_2(string_table, array_from_map_1(oa_table))), ("stringTable", encoder_3(array_from_map_2(string_table))), ("table", arc_table)])
        class ObjectExpr3846(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg[0], tupled_arg[1].Encode(helpers))

                arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
                return helpers.encode_object(arg)

        return ObjectExpr3846()

    return to_string(spaces_1, _arrow3847())


def ARCtrl_ArcTable__ArcTable_toCompressedJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcTable], str]:
    def _arrow3848(obj: ArcTable, spaces: Any=spaces) -> str:
        return ARCtrl_ArcTable__ArcTable_ToCompressedJsonString_71136F3F(obj, spaces)

    return _arrow3848


__all__ = ["ARCtrl_ArcTable__ArcTable_fromJsonString_Static_Z721C83C5", "ARCtrl_ArcTable__ArcTable_toJsonString_Static_71136F3F", "ARCtrl_ArcTable__ArcTable_ToJsonString_71136F3F", "ARCtrl_ArcTable__ArcTable_fromCompressedJsonString_Static_Z721C83C5", "ARCtrl_ArcTable__ArcTable_ToCompressedJsonString_71136F3F", "ARCtrl_ArcTable__ArcTable_toCompressedJsonString_Static_71136F3F"]

