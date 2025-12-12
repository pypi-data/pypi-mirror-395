from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.array_ import map as map_2
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import (map, default_arg)
from ..fable_modules.fable_library.seq import (map as map_1, try_pick)
from ..fable_modules.fable_library.string_ import (replace, split, join)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, resize_array, IGetters, IRequiredGetter, map as map_3, array as array_3)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.comment import Comment
from ..Core.conversion import (Person_setCommentFromORCID, Person_setOrcidFromComments)
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from .comment import (encoder as encoder_1, decoder as decoder_1, ROCrate_encoderDisambiguatingDescription, ROCrate_decoderDisambiguatingDescription)
from .context.rocrate.isa_organization_context import context_jsonvalue
from .context.rocrate.isa_person_context import (context_jsonvalue as context_jsonvalue_1, context_minimal_json_value)
from .decode import Decode_objectNoAdditionalProperties
from .encode import (try_include, try_include_seq)
from .idtable import encode
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderDefinedTerm)

__A_ = TypeVar("__A_")

def encoder(person: Person) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], person: Any=person) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2566(value: str, person: Any=person) -> IEncodable:
        class ObjectExpr2565(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2565()

    def _arrow2568(value_2: str, person: Any=person) -> IEncodable:
        class ObjectExpr2567(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr2567()

    def _arrow2570(value_4: str, person: Any=person) -> IEncodable:
        class ObjectExpr2569(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr2569()

    def _arrow2572(value_6: str, person: Any=person) -> IEncodable:
        class ObjectExpr2571(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr2571()

    def _arrow2574(value_8: str, person: Any=person) -> IEncodable:
        class ObjectExpr2573(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_8)

        return ObjectExpr2573()

    def _arrow2576(value_10: str, person: Any=person) -> IEncodable:
        class ObjectExpr2575(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_10)

        return ObjectExpr2575()

    def _arrow2578(value_12: str, person: Any=person) -> IEncodable:
        class ObjectExpr2577(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_12)

        return ObjectExpr2577()

    def _arrow2580(value_14: str, person: Any=person) -> IEncodable:
        class ObjectExpr2579(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                return helpers_7.encode_string(value_14)

        return ObjectExpr2579()

    def _arrow2582(value_16: str, person: Any=person) -> IEncodable:
        class ObjectExpr2581(IEncodable):
            def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                return helpers_8.encode_string(value_16)

        return ObjectExpr2581()

    def _arrow2583(oa: OntologyAnnotation, person: Any=person) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def _arrow2584(comment: Comment, person: Any=person) -> IEncodable:
        return encoder_1(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("firstName", _arrow2566, person.FirstName), try_include("lastName", _arrow2568, person.LastName), try_include("midInitials", _arrow2570, person.MidInitials), try_include("orcid", _arrow2572, person.ORCID), try_include("email", _arrow2574, person.EMail), try_include("phone", _arrow2576, person.Phone), try_include("fax", _arrow2578, person.Fax), try_include("address", _arrow2580, person.Address), try_include("affiliation", _arrow2582, person.Affiliation), try_include_seq("roles", _arrow2583, person.Roles), try_include_seq("comments", _arrow2584, person.Comments)]))
    class ObjectExpr2585(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any], person: Any=person) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_9))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_9.encode_object(arg)

    return ObjectExpr2585()


def _arrow2597(get: IGetters) -> Person:
    def _arrow2586(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("orcid", string)

    def _arrow2587(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("lastName", string)

    def _arrow2588(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("firstName", string)

    def _arrow2589(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("midInitials", string)

    def _arrow2590(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("email", string)

    def _arrow2591(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("phone", string)

    def _arrow2592(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("fax", string)

    def _arrow2593(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("address", string)

    def _arrow2594(__unit: None=None) -> str | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("affiliation", string)

    def _arrow2595(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_19: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("roles", arg_19)

    def _arrow2596(__unit: None=None) -> Array[Comment] | None:
        arg_21: Decoder_1[Array[Comment]] = resize_array(decoder_1)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("comments", arg_21)

    return Person(_arrow2586(), _arrow2587(), _arrow2588(), _arrow2589(), _arrow2590(), _arrow2591(), _arrow2592(), _arrow2593(), _arrow2594(), _arrow2595(), _arrow2596())


decoder: Decoder_1[Person] = object(_arrow2597)

def ROCrate_genID(p: Person) -> str:
    def chooser(c: Comment, p: Any=p) -> str | None:
        match_value: str | None = c.Name
        match_value_1: str | None = c.Value
        (pattern_matching_result, n, v) = (None, None, None)
        if match_value is not None:
            if match_value_1 is not None:
                pattern_matching_result = 0
                n = match_value
                v = match_value_1

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            if True if (True if (n == "orcid") else (n == "Orcid")) else (n == "ORCID"):
                return v

            else: 
                return None


        elif pattern_matching_result == 1:
            return None


    orcid: str | None = try_pick(chooser, p.Comments)
    if orcid is None:
        match_value_1: str | None = p.EMail
        if match_value_1 is None:
            match_value_2: str | None = p.FirstName
            match_value_3: str | None = p.MidInitials
            match_value_4: str | None = p.LastName
            (pattern_matching_result_1, fn, ln, mn, fn_1, ln_1, ln_2, fn_2) = (None, None, None, None, None, None, None, None)
            if match_value_2 is None:
                if match_value_3 is None:
                    if match_value_4 is not None:
                        pattern_matching_result_1 = 2
                        ln_2 = match_value_4

                    else: 
                        pattern_matching_result_1 = 4


                else: 
                    pattern_matching_result_1 = 4


            elif match_value_3 is None:
                if match_value_4 is None:
                    pattern_matching_result_1 = 3
                    fn_2 = match_value_2

                else: 
                    pattern_matching_result_1 = 1
                    fn_1 = match_value_2
                    ln_1 = match_value_4


            elif match_value_4 is not None:
                pattern_matching_result_1 = 0
                fn = match_value_2
                ln = match_value_4
                mn = match_value_3

            else: 
                pattern_matching_result_1 = 4

            if pattern_matching_result_1 == 0:
                return (((("#" + replace(fn, " ", "_")) + "_") + replace(mn, " ", "_")) + "_") + replace(ln, " ", "_")

            elif pattern_matching_result_1 == 1:
                return (("#" + replace(fn_1, " ", "_")) + "_") + replace(ln_1, " ", "_")

            elif pattern_matching_result_1 == 2:
                return "#" + replace(ln_2, " ", "_")

            elif pattern_matching_result_1 == 3:
                return "#" + replace(fn_2, " ", "_")

            elif pattern_matching_result_1 == 4:
                return "#EmptyPerson"


        else: 
            return match_value_1


    else: 
        return orcid



def ROCrate_Affiliation_encoder(affiliation: str) -> IEncodable:
    class ObjectExpr2599(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], affiliation: Any=affiliation) -> Any:
            return helpers.encode_string("Organization")

    def _arrow2601(__unit: None=None, affiliation: Any=affiliation) -> IEncodable:
        value_1: str = replace(("#Organization_" + affiliation) + "", " ", "_")
        class ObjectExpr2600(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr2600()

    class ObjectExpr2602(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], affiliation: Any=affiliation) -> Any:
            return helpers_2.encode_string(affiliation)

    values: FSharpList[tuple[str, IEncodable]] = of_array([("@type", ObjectExpr2599()), ("@id", _arrow2601()), ("name", ObjectExpr2602()), ("@context", context_jsonvalue)])
    class ObjectExpr2603(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any], affiliation: Any=affiliation) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_3))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping, values)
            return helpers_3.encode_object(arg)

    return ObjectExpr2603()


def _arrow2604(get: IGetters) -> str:
    object_arg: IRequiredGetter = get.Required
    return object_arg.Field("name", string)


ROCrate_Affiliation_decoder: Decoder_1[str] = object(_arrow2604)

def ROCrate_encoder(oa: Person) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2608(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr2607(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2607()

    class ObjectExpr2609(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Person")

    def _arrow2611(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2610(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr2610()

    def _arrow2613(value_4: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2612(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_4)

        return ObjectExpr2612()

    def _arrow2615(value_6: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2614(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_6)

        return ObjectExpr2614()

    def _arrow2617(value_8: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2616(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_8)

        return ObjectExpr2616()

    def _arrow2619(value_10: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2618(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_10)

        return ObjectExpr2618()

    def _arrow2626(value_12: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2625(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                return helpers_7.encode_string(value_12)

        return ObjectExpr2625()

    def _arrow2630(value_14: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2629(IEncodable):
            def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                return helpers_8.encode_string(value_14)

        return ObjectExpr2629()

    def _arrow2633(value_16: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2632(IEncodable):
            def Encode(self, helpers_9: IEncoderHelpers_1[Any]) -> Any:
                return helpers_9.encode_string(value_16)

        return ObjectExpr2632()

    def _arrow2634(affiliation: str, oa: Any=oa) -> IEncodable:
        return ROCrate_Affiliation_encoder(affiliation)

    def _arrow2636(oa_1: OntologyAnnotation, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_1)

    def _arrow2637(comment: Comment, oa: Any=oa) -> IEncodable:
        return ROCrate_encoderDisambiguatingDescription(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2608()), ("@type", ObjectExpr2609()), try_include("orcid", _arrow2611, oa.ORCID), try_include("firstName", _arrow2613, oa.FirstName), try_include("lastName", _arrow2615, oa.LastName), try_include("midInitials", _arrow2617, oa.MidInitials), try_include("email", _arrow2619, oa.EMail), try_include("phone", _arrow2626, oa.Phone), try_include("fax", _arrow2630, oa.Fax), try_include("address", _arrow2633, oa.Address), try_include("affiliation", _arrow2634, oa.Affiliation), try_include_seq("roles", _arrow2636, oa.Roles), try_include_seq("comments", _arrow2637, oa.Comments), ("@context", context_jsonvalue_1)]))
    class ObjectExpr2642(IEncodable):
        def Encode(self, helpers_10: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_10))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_10.encode_object(arg)

    return ObjectExpr2642()


def _arrow2655(get: IGetters) -> Person:
    def _arrow2644(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("orcid", string)

    def _arrow2645(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("lastName", string)

    def _arrow2646(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("firstName", string)

    def _arrow2647(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("midInitials", string)

    def _arrow2648(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("email", string)

    def _arrow2649(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("phone", string)

    def _arrow2650(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("fax", string)

    def _arrow2651(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("address", string)

    def _arrow2652(__unit: None=None) -> str | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("affiliation", ROCrate_Affiliation_decoder)

    def _arrow2653(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_19: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_ROCrate_decoderDefinedTerm)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("roles", arg_19)

    def _arrow2654(__unit: None=None) -> Array[Comment] | None:
        arg_21: Decoder_1[Array[Comment]] = resize_array(ROCrate_decoderDisambiguatingDescription)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("comments", arg_21)

    return Person(_arrow2644(), _arrow2645(), _arrow2646(), _arrow2647(), _arrow2648(), _arrow2649(), _arrow2650(), _arrow2651(), _arrow2652(), _arrow2653(), _arrow2654())


ROCrate_decoder: Decoder_1[Person] = object(_arrow2655)

def ROCrate_encodeAuthorListString(author_list: str) -> IEncodable:
    def encode_single(name: str, author_list: Any=author_list) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], name: Any=name) -> tuple[str, IEncodable] | None:
            def mapping_1(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping_1, tupled_arg[1])

        class ObjectExpr2657(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], name: Any=name) -> Any:
                return helpers.encode_string("Person")

        def _arrow2659(value_1: str, name: Any=name) -> IEncodable:
            class ObjectExpr2658(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_1)

            return ObjectExpr2658()

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@type", ObjectExpr2657()), try_include("name", _arrow2659, name), ("@context", context_minimal_json_value)]))
        class ObjectExpr2660(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], name: Any=name) -> Any:
                def mapping_2(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_2, values)
                return helpers_2.encode_object(arg)

        return ObjectExpr2660()

    def mapping(s: str, author_list: Any=author_list) -> str:
        return s.strip()

    values_2: Array[IEncodable] = map_2(encode_single, map_2(mapping, split(author_list, ["\t" if (author_list.find("\t") >= 0) else (";" if (author_list.find(";") >= 0) else ",")], None, 0), None), None)
    class ObjectExpr2661(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any], author_list: Any=author_list) -> Any:
            def mapping_3(v_3: IEncodable) -> __A_:
                return v_3.Encode(helpers_3)

            arg_1: Array[__A_] = map_2(mapping_3, values_2, None)
            return helpers_3.encode_array(arg_1)

    return ObjectExpr2661()


def ctor(v: Array[str]) -> str:
    return join(", ", v)


def _arrow2663(get: IGetters) -> str:
    def _arrow2662(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("name", string)

    return default_arg(_arrow2662(), "")


ROCrate_decodeAuthorListString: Decoder_1[str] = map_3(ctor, array_3(object(_arrow2663)))

ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "firstName", "lastName", "midInitials", "email", "phone", "fax", "address", "affiliation", "roles", "comments", "@type", "@context"])

def ISAJson_encoder(id_map: Any | None, person: Person) -> IEncodable:
    def f(person_1: Person, id_map: Any=id_map, person: Any=person) -> IEncodable:
        person_2: Person = Person_setCommentFromORCID(person_1)
        def chooser(tupled_arg: tuple[str, IEncodable | None], person_1: Any=person_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2667(value: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2666(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2666()

        def _arrow2669(value_2: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2668(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_2)

            return ObjectExpr2668()

        def _arrow2671(value_4: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2670(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_2.encode_string(value_4)

            return ObjectExpr2670()

        def _arrow2673(value_6: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2672(IEncodable):
                def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_3.encode_string(value_6)

            return ObjectExpr2672()

        def _arrow2675(value_8: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2674(IEncodable):
                def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_4.encode_string(value_8)

            return ObjectExpr2674()

        def _arrow2677(value_10: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2676(IEncodable):
                def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_5.encode_string(value_10)

            return ObjectExpr2676()

        def _arrow2679(value_12: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2678(IEncodable):
                def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_6.encode_string(value_12)

            return ObjectExpr2678()

        def _arrow2681(value_14: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2680(IEncodable):
                def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_7.encode_string(value_14)

            return ObjectExpr2680()

        def _arrow2683(value_16: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2682(IEncodable):
                def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_8.encode_string(value_16)

            return ObjectExpr2682()

        def _arrow2684(oa: OntologyAnnotation, person_1: Any=person_1) -> IEncodable:
            return OntologyAnnotation_encoder(oa)

        def _arrow2685(comment: Comment, person_1: Any=person_1) -> IEncodable:
            return encoder_1(comment)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2667, ROCrate_genID(person_2)), try_include("firstName", _arrow2669, person_2.FirstName), try_include("lastName", _arrow2671, person_2.LastName), try_include("midInitials", _arrow2673, person_2.MidInitials), try_include("email", _arrow2675, person_2.EMail), try_include("phone", _arrow2677, person_2.Phone), try_include("fax", _arrow2679, person_2.Fax), try_include("address", _arrow2681, person_2.Address), try_include("affiliation", _arrow2683, person_2.Affiliation), try_include_seq("roles", _arrow2684, person_2.Roles), try_include_seq("comments", _arrow2685, person_2.Comments)]))
        class ObjectExpr2686(IEncodable):
            def Encode(self, helpers_9: IEncoderHelpers_1[Any], person_1: Any=person_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_9))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_9.encode_object(arg)

        return ObjectExpr2686()

    if id_map is not None:
        def _arrow2687(p_1: Person, id_map: Any=id_map, person: Any=person) -> str:
            return ROCrate_genID(p_1)

        return encode(_arrow2687, f, person, id_map)

    else: 
        return f(person)



def _arrow2698(get: IGetters) -> Person:
    def _arrow2688(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("lastName", string)

    def _arrow2689(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("firstName", string)

    def _arrow2690(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("midInitials", string)

    def _arrow2691(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("email", string)

    def _arrow2692(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("phone", string)

    def _arrow2693(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("fax", string)

    def _arrow2694(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("address", string)

    def _arrow2695(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("affiliation", string)

    def _arrow2696(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_17: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("roles", arg_17)

    def _arrow2697(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = resize_array(decoder_1)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return Person_setOrcidFromComments(Person(None, _arrow2688(), _arrow2689(), _arrow2690(), _arrow2691(), _arrow2692(), _arrow2693(), _arrow2694(), _arrow2695(), _arrow2696(), _arrow2697()))


ISAJson_decoder: Decoder_1[Person] = Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow2698)

__all__ = ["encoder", "decoder", "ROCrate_genID", "ROCrate_Affiliation_encoder", "ROCrate_Affiliation_decoder", "ROCrate_encoder", "ROCrate_decoder", "ROCrate_encodeAuthorListString", "ROCrate_decodeAuthorListString", "ISAJson_allowedFields", "ISAJson_encoder", "ISAJson_decoder"]

