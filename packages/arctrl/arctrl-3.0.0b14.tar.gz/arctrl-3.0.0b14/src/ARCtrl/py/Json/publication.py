from __future__ import annotations
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.seq import map as map_1
from ..fable_modules.fable_library.string_ import replace
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, resize_array, IGetters)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.comment import Comment
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.publication import Publication
from .comment import (encoder as encoder_1, decoder as decoder_2, ROCrate_encoderDisambiguatingDescription, ROCrate_decoderDisambiguatingDescription, ISAJson_encoder as ISAJson_encoder_1)
from .context.rocrate.isa_publication_context import context_jsonvalue
from .decode import (Decode_uri, Decode_noAdditionalProperties)
from .encode import (try_include, try_include_seq)
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderDefinedTerm)
from .person import (ROCrate_encodeAuthorListString, ROCrate_decodeAuthorListString)

__A_ = TypeVar("__A_")

def encoder(oa: Publication) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2497(value: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2496(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2496()

    def _arrow2499(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2498(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr2498()

    def _arrow2501(value_4: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2500(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr2500()

    def _arrow2503(value_6: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2502(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr2502()

    def _arrow2504(oa_1: OntologyAnnotation, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow2505(comment: Comment, oa: Any=oa) -> IEncodable:
        return encoder_1(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("pubMedID", _arrow2497, oa.PubMedID), try_include("doi", _arrow2499, oa.DOI), try_include("authorList", _arrow2501, oa.Authors), try_include("title", _arrow2503, oa.Title), try_include("status", _arrow2504, oa.Status), try_include_seq("comments", _arrow2505, oa.Comments)]))
    class ObjectExpr2506(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr2506()


def _arrow2513(get: IGetters) -> Publication:
    def _arrow2507(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("pubMedID", Decode_uri)

    def _arrow2508(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("doi", string)

    def _arrow2509(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("authorList", string)

    def _arrow2510(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("title", string)

    def _arrow2511(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("status", OntologyAnnotation_decoder)

    def _arrow2512(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = resize_array(decoder_2)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Publication(_arrow2507(), _arrow2508(), _arrow2509(), _arrow2510(), _arrow2511(), _arrow2512())


decoder: Decoder_1[Publication] = object(_arrow2513)

def ROCrate_genID(p: Publication) -> str:
    match_value: str | None = p.DOI
    if match_value is None:
        match_value_1: str | None = p.PubMedID
        if match_value_1 is None:
            match_value_2: str | None = p.Title
            if match_value_2 is None:
                return "#EmptyPublication"

            else: 
                return "#Pub_" + replace(match_value_2, " ", "_")


        else: 
            return match_value_1


    else: 
        return match_value



def ROCrate_encoder(oa: Publication) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2517(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr2516(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2516()

    class ObjectExpr2518(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Publication")

    def _arrow2520(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2519(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr2519()

    def _arrow2522(value_4: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2521(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_4)

        return ObjectExpr2521()

    def _arrow2523(author_list: str, oa: Any=oa) -> IEncodable:
        return ROCrate_encodeAuthorListString(author_list)

    def _arrow2525(value_6: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2524(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_6)

        return ObjectExpr2524()

    def _arrow2526(oa_1: OntologyAnnotation, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_1)

    def _arrow2527(comment: Comment, oa: Any=oa) -> IEncodable:
        return ROCrate_encoderDisambiguatingDescription(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2517()), ("@type", ObjectExpr2518()), try_include("pubMedID", _arrow2520, oa.PubMedID), try_include("doi", _arrow2522, oa.DOI), try_include("authorList", _arrow2523, oa.Authors), try_include("title", _arrow2525, oa.Title), try_include("status", _arrow2526, oa.Status), try_include_seq("comments", _arrow2527, oa.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr2528(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_5))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_5.encode_object(arg)

    return ObjectExpr2528()


def _arrow2535(get: IGetters) -> Publication:
    def _arrow2529(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("pubMedID", Decode_uri)

    def _arrow2530(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("doi", string)

    def _arrow2531(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("authorList", ROCrate_decodeAuthorListString)

    def _arrow2532(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("title", string)

    def _arrow2533(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("status", OntologyAnnotation_ROCrate_decoderDefinedTerm)

    def _arrow2534(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = resize_array(ROCrate_decoderDisambiguatingDescription)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Publication(_arrow2529(), _arrow2530(), _arrow2531(), _arrow2532(), _arrow2533(), _arrow2534())


ROCrate_decoder: Decoder_1[Publication] = object(_arrow2535)

def ISAJson_encoder(id_map: Any | None, oa: Publication) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], id_map: Any=id_map, oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2539(value: str, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        class ObjectExpr2538(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2538()

    def _arrow2541(value_2: str, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        class ObjectExpr2540(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr2540()

    def _arrow2543(value_4: str, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        class ObjectExpr2542(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr2542()

    def _arrow2545(value_6: str, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        class ObjectExpr2544(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr2544()

    def _arrow2546(oa_1: OntologyAnnotation, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow2547(comment: Comment, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        return ISAJson_encoder_1(id_map, comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("pubMedID", _arrow2539, oa.PubMedID), try_include("doi", _arrow2541, oa.DOI), try_include("authorList", _arrow2543, oa.Authors), try_include("title", _arrow2545, oa.Title), try_include("status", _arrow2546, oa.Status), try_include_seq("comments", _arrow2547, oa.Comments)]))
    class ObjectExpr2548(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], id_map: Any=id_map, oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr2548()


ISAJson_allowedFields: FSharpList[str] = of_array(["pubMedID", "doi", "authorList", "title", "status", "comments"])

ISAJson_decoder: Decoder_1[Publication] = Decode_noAdditionalProperties(ISAJson_allowedFields, decoder)

__all__ = ["encoder", "decoder", "ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_allowedFields", "ISAJson_decoder"]

