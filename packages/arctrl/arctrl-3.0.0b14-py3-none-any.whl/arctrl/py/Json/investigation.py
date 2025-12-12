from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.date import (today, to_string)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList, unzip, empty)
from ..fable_modules.fable_library.option import (map, default_arg)
from ..fable_modules.fable_library.seq import (map as map_1, concat)
from ..fable_modules.fable_library.seq2 import distinct_by
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (IEnumerable_1, string_hash)
from ..fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, IOptionalGetter, resize_array, IGetters, list_1 as list_1_1)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.arc_types import (ArcAssay, ArcStudy, ArcInvestigation)
from ..Core.comment import Comment
from ..Core.Helper.identifier import create_missing_identifier
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.ontology_source_reference import OntologySourceReference
from ..Core.person import Person
from ..Core.publication import Publication
from ..Core.Table.composite_cell import CompositeCell
from .assay import (encoder as encoder_4, decoder as decoder_6, encoder_compressed as encoder_compressed_1, decoder_compressed as decoder_compressed_1)
from .comment import (encoder as encoder_6, decoder as decoder_8, ROCrate_encoder as ROCrate_encoder_5, ROCrate_decoder as ROCrate_decoder_5, ISAJson_encoder as ISAJson_encoder_5, ISAJson_decoder as ISAJson_decoder_5)
from .context.rocrate.isa_investigation_context import context_jsonvalue
from .context.rocrate.rocrate_context import (conforms_to_jsonvalue, context_jsonvalue as context_jsonvalue_1)
from .decode import Decode_objectNoAdditionalProperties
from .encode import (try_include, try_include_seq)
from .ontology_source_reference import (encoder as encoder_1, decoder as decoder_3, ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_2, ISAJson_encoder as ISAJson_encoder_1, ISAJson_decoder as ISAJson_decoder_2)
from .person import (encoder as encoder_3, decoder as decoder_5, ROCrate_encoder as ROCrate_encoder_3, ROCrate_decoder as ROCrate_decoder_4, ISAJson_encoder as ISAJson_encoder_3, ISAJson_decoder as ISAJson_decoder_4)
from .publication import (encoder as encoder_2, decoder as decoder_4, ROCrate_encoder as ROCrate_encoder_2, ROCrate_decoder as ROCrate_decoder_3, ISAJson_encoder as ISAJson_encoder_2, ISAJson_decoder as ISAJson_decoder_3)
from .study import (encoder as encoder_5, decoder as decoder_7, encoder_compressed as encoder_compressed_2, decoder_compressed as decoder_compressed_2, ROCrate_encoder as ROCrate_encoder_4, ROCrate_decoder as ROCrate_decoder_1, ISAJson_encoder as ISAJson_encoder_4, ISAJson_decoder as ISAJson_decoder_1)

__A_ = TypeVar("__A_")

def encoder(inv: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], inv: Any=inv) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3558(__unit: None=None, inv: Any=inv) -> IEncodable:
        value: str = inv.Identifier
        class ObjectExpr3557(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3557()

    def _arrow3560(value_1: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr3559(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr3559()

    def _arrow3562(value_3: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr3561(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_3)

        return ObjectExpr3561()

    def _arrow3564(value_5: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr3563(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr3563()

    def _arrow3566(value_7: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr3565(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_7)

        return ObjectExpr3565()

    def _arrow3567(osr: OntologySourceReference, inv: Any=inv) -> IEncodable:
        return encoder_1(osr)

    def _arrow3568(oa: Publication, inv: Any=inv) -> IEncodable:
        return encoder_2(oa)

    def _arrow3569(person: Person, inv: Any=inv) -> IEncodable:
        return encoder_3(person)

    def _arrow3570(assay: ArcAssay, inv: Any=inv) -> IEncodable:
        return encoder_4(assay)

    def _arrow3571(study: ArcStudy, inv: Any=inv) -> IEncodable:
        return encoder_5(study)

    def _arrow3573(value_9: str, inv: Any=inv) -> IEncodable:
        class ObjectExpr3572(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_9)

        return ObjectExpr3572()

    def _arrow3574(comment: Comment, inv: Any=inv) -> IEncodable:
        return encoder_6(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow3558()), try_include("Title", _arrow3560, inv.Title), try_include("Description", _arrow3562, inv.Description), try_include("SubmissionDate", _arrow3564, inv.SubmissionDate), try_include("PublicReleaseDate", _arrow3566, inv.PublicReleaseDate), try_include_seq("OntologySourceReferences", _arrow3567, inv.OntologySourceReferences), try_include_seq("Publications", _arrow3568, inv.Publications), try_include_seq("Contacts", _arrow3569, inv.Contacts), try_include_seq("Assays", _arrow3570, inv.Assays), try_include_seq("Studies", _arrow3571, inv.Studies), try_include_seq("RegisteredStudyIdentifiers", _arrow3573, inv.RegisteredStudyIdentifiers), try_include_seq("Comments", _arrow3574, inv.Comments)]))
    class ObjectExpr3575(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], inv: Any=inv) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr3575()


def _arrow3588(get: IGetters) -> ArcInvestigation:
    def _arrow3576(__unit: None=None) -> str:
        object_arg: IRequiredGetter = get.Required
        return object_arg.Field("Identifier", string)

    def _arrow3577(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("Title", string)

    def _arrow3578(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("Description", string)

    def _arrow3579(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("SubmissionDate", string)

    def _arrow3580(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("PublicReleaseDate", string)

    def _arrow3581(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_11: Decoder_1[Array[OntologySourceReference]] = resize_array(decoder_3)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("OntologySourceReferences", arg_11)

    def _arrow3582(__unit: None=None) -> Array[Publication] | None:
        arg_13: Decoder_1[Array[Publication]] = resize_array(decoder_4)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("Publications", arg_13)

    def _arrow3583(__unit: None=None) -> Array[Person] | None:
        arg_15: Decoder_1[Array[Person]] = resize_array(decoder_5)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("Contacts", arg_15)

    def _arrow3584(__unit: None=None) -> Array[ArcAssay] | None:
        arg_17: Decoder_1[Array[ArcAssay]] = resize_array(decoder_6)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("Assays", arg_17)

    def _arrow3585(__unit: None=None) -> Array[ArcStudy] | None:
        arg_19: Decoder_1[Array[ArcStudy]] = resize_array(decoder_7)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("Studies", arg_19)

    def _arrow3586(__unit: None=None) -> Array[str] | None:
        arg_21: Decoder_1[Array[str]] = resize_array(string)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("RegisteredStudyIdentifiers", arg_21)

    def _arrow3587(__unit: None=None) -> Array[Comment] | None:
        arg_23: Decoder_1[Array[Comment]] = resize_array(decoder_8)
        object_arg_11: IOptionalGetter = get.Optional
        return object_arg_11.Field("Comments", arg_23)

    return ArcInvestigation(_arrow3576(), _arrow3577(), _arrow3578(), _arrow3579(), _arrow3580(), _arrow3581(), _arrow3582(), _arrow3583(), _arrow3584(), _arrow3585(), None, None, _arrow3586(), _arrow3587())


decoder: Decoder_1[ArcInvestigation] = object(_arrow3588)

def encoder_compressed(string_table: Any, oa_table: Any, cell_table: Any, inv: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3592(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        value: str = inv.Identifier
        class ObjectExpr3591(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3591()

    def _arrow3594(value_1: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr3593(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr3593()

    def _arrow3596(value_3: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr3595(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_3)

        return ObjectExpr3595()

    def _arrow3598(value_5: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr3597(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr3597()

    def _arrow3600(value_7: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr3599(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_7)

        return ObjectExpr3599()

    def _arrow3601(osr: OntologySourceReference, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_1(osr)

    def _arrow3602(oa: Publication, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_2(oa)

    def _arrow3603(person: Person, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_3(person)

    def _arrow3604(assay: ArcAssay, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_compressed_1(string_table, oa_table, cell_table, assay)

    def _arrow3605(study: ArcStudy, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_compressed_2(string_table, oa_table, cell_table, study)

    def _arrow3607(value_9: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        class ObjectExpr3606(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_9)

        return ObjectExpr3606()

    def _arrow3608(comment: Comment, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> IEncodable:
        return encoder_6(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow3592()), try_include("Title", _arrow3594, inv.Title), try_include("Description", _arrow3596, inv.Description), try_include("SubmissionDate", _arrow3598, inv.SubmissionDate), try_include("PublicReleaseDate", _arrow3600, inv.PublicReleaseDate), try_include_seq("OntologySourceReferences", _arrow3601, inv.OntologySourceReferences), try_include_seq("Publications", _arrow3602, inv.Publications), try_include_seq("Contacts", _arrow3603, inv.Contacts), try_include_seq("Assays", _arrow3604, inv.Assays), try_include_seq("Studies", _arrow3605, inv.Studies), try_include_seq("RegisteredStudyIdentifiers", _arrow3607, inv.RegisteredStudyIdentifiers), try_include_seq("Comments", _arrow3608, inv.Comments)]))
    class ObjectExpr3609(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr3609()


def decoder_compressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[ArcInvestigation]:
    def _arrow3622(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> ArcInvestigation:
        def _arrow3610(__unit: None=None) -> str:
            object_arg: IRequiredGetter = get.Required
            return object_arg.Field("Identifier", string)

        def _arrow3611(__unit: None=None) -> str | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("Title", string)

        def _arrow3612(__unit: None=None) -> str | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("Description", string)

        def _arrow3613(__unit: None=None) -> str | None:
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("SubmissionDate", string)

        def _arrow3614(__unit: None=None) -> str | None:
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("PublicReleaseDate", string)

        def _arrow3615(__unit: None=None) -> Array[OntologySourceReference] | None:
            arg_11: Decoder_1[Array[OntologySourceReference]] = resize_array(decoder_3)
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("OntologySourceReferences", arg_11)

        def _arrow3616(__unit: None=None) -> Array[Publication] | None:
            arg_13: Decoder_1[Array[Publication]] = resize_array(decoder_4)
            object_arg_6: IOptionalGetter = get.Optional
            return object_arg_6.Field("Publications", arg_13)

        def _arrow3617(__unit: None=None) -> Array[Person] | None:
            arg_15: Decoder_1[Array[Person]] = resize_array(decoder_5)
            object_arg_7: IOptionalGetter = get.Optional
            return object_arg_7.Field("Contacts", arg_15)

        def _arrow3618(__unit: None=None) -> Array[ArcAssay] | None:
            arg_17: Decoder_1[Array[ArcAssay]] = resize_array(decoder_compressed_1(string_table, oa_table, cell_table))
            object_arg_8: IOptionalGetter = get.Optional
            return object_arg_8.Field("Assays", arg_17)

        def _arrow3619(__unit: None=None) -> Array[ArcStudy] | None:
            arg_19: Decoder_1[Array[ArcStudy]] = resize_array(decoder_compressed_2(string_table, oa_table, cell_table))
            object_arg_9: IOptionalGetter = get.Optional
            return object_arg_9.Field("Studies", arg_19)

        def _arrow3620(__unit: None=None) -> Array[str] | None:
            arg_21: Decoder_1[Array[str]] = resize_array(string)
            object_arg_10: IOptionalGetter = get.Optional
            return object_arg_10.Field("RegisteredStudyIdentifiers", arg_21)

        def _arrow3621(__unit: None=None) -> Array[Comment] | None:
            arg_23: Decoder_1[Array[Comment]] = resize_array(decoder_8)
            object_arg_11: IOptionalGetter = get.Optional
            return object_arg_11.Field("Comments", arg_23)

        return ArcInvestigation(_arrow3610(), _arrow3611(), _arrow3612(), _arrow3613(), _arrow3614(), _arrow3615(), _arrow3616(), _arrow3617(), _arrow3618(), _arrow3619(), None, None, _arrow3620(), _arrow3621())

    return object(_arrow3622)


def ROCrate_genID(i: ArcInvestigation) -> str:
    return "./"


def ROCrate_encoder(oa: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3626(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr3625(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3625()

    class ObjectExpr3627(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Investigation")

    class ObjectExpr3628(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_2.encode_string("Investigation")

    def _arrow3630(__unit: None=None, oa: Any=oa) -> IEncodable:
        value_3: str = oa.Identifier
        class ObjectExpr3629(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_3)

        return ObjectExpr3629()

    def _arrow3632(__unit: None=None, oa: Any=oa) -> IEncodable:
        value_4: str = ArcInvestigation.FileName()
        class ObjectExpr3631(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_4)

        return ObjectExpr3631()

    def _arrow3634(value_5: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3633(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_5)

        return ObjectExpr3633()

    def _arrow3636(value_7: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3635(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_7)

        return ObjectExpr3635()

    def _arrow3638(value_9: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3637(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                return helpers_7.encode_string(value_9)

        return ObjectExpr3637()

    def _arrow3641(__unit: None=None, oa: Any=oa) -> IEncodable:
        def _arrow3639(__unit: None=None) -> str:
            copy_of_struct: Any = today()
            return to_string(copy_of_struct, "yyyy-MM-dd")

        value_12: str = default_arg(oa.PublicReleaseDate, _arrow3639())
        class ObjectExpr3640(IEncodable):
            def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                return helpers_8.encode_string(value_12)

        return ObjectExpr3640()

    def _arrow3642(osr: OntologySourceReference, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_1(osr)

    def _arrow3643(oa_1: Publication, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_2(oa_1)

    def _arrow3644(oa_2: Person, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_3(oa_2)

    def _arrow3645(s: ArcStudy, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_4(None, s)

    def _arrow3646(comment: Comment, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_5(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow3626()), ("@type", ObjectExpr3627()), ("additionalType", ObjectExpr3628()), ("identifier", _arrow3630()), ("filename", _arrow3632()), try_include("title", _arrow3634, oa.Title), try_include("description", _arrow3636, oa.Description), try_include("submissionDate", _arrow3638, oa.SubmissionDate), ("publicReleaseDate", _arrow3641()), try_include_seq("ontologySourceReferences", _arrow3642, oa.OntologySourceReferences), try_include_seq("publications", _arrow3643, oa.Publications), try_include_seq("people", _arrow3644, oa.Contacts), try_include_seq("studies", _arrow3645, oa.Studies), try_include_seq("comments", _arrow3646, oa.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr3647(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_9))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_9.encode_object(arg)

    return ObjectExpr3647()


def _arrow3659(get: IGetters) -> ArcInvestigation:
    identifier: str
    match_value: str | None
    object_arg: IOptionalGetter = get.Optional
    match_value = object_arg.Field("identifier", string)
    identifier = create_missing_identifier() if (match_value is None) else match_value
    def _arrow3648(__unit: None=None) -> FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]] | None:
        arg_3: Decoder_1[FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]]] = list_1_1(ROCrate_decoder_1)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("studies", arg_3)

    pattern_input: tuple[FSharpList[ArcStudy], FSharpList[FSharpList[ArcAssay]]] = unzip(default_arg(_arrow3648(), empty()))
    studies_raw: FSharpList[ArcStudy] = pattern_input[0]
    def projection(a: ArcAssay) -> str:
        return a.Identifier

    class ObjectExpr3650:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow3649(x: str, y: str) -> bool:
                return x == y

            return _arrow3649

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    assays: Array[ArcAssay] = list(distinct_by(projection, concat(pattern_input[1]), ObjectExpr3650()))
    studies: Array[ArcStudy] = list(studies_raw)
    def mapping(a_1: ArcStudy) -> str:
        return a_1.Identifier

    study_identifiers: Array[str] = list(map_1(mapping, studies_raw))
    def _arrow3651(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("title", string)

    def _arrow3652(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("description", string)

    def _arrow3653(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("submissionDate", string)

    def _arrow3654(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("publicReleaseDate", string)

    def _arrow3655(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_13: Decoder_1[Array[OntologySourceReference]] = resize_array(ROCrate_decoder_2)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("ontologySourceReferences", arg_13)

    def _arrow3656(__unit: None=None) -> Array[Publication] | None:
        arg_15: Decoder_1[Array[Publication]] = resize_array(ROCrate_decoder_3)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("publications", arg_15)

    def _arrow3657(__unit: None=None) -> Array[Person] | None:
        arg_17: Decoder_1[Array[Person]] = resize_array(ROCrate_decoder_4)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("people", arg_17)

    def _arrow3658(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = resize_array(ROCrate_decoder_5)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return ArcInvestigation(identifier, _arrow3651(), _arrow3652(), _arrow3653(), _arrow3654(), _arrow3655(), _arrow3656(), _arrow3657(), assays, studies, None, None, study_identifiers, _arrow3658())


ROCrate_decoder: Decoder_1[ArcInvestigation] = object(_arrow3659)

def ROCrate_encodeRoCrate(oa: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3663(value: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3662(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3662()

    def _arrow3665(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr3664(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr3664()

    def _arrow3667(oa_1: ArcInvestigation, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder(oa_1)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@type", _arrow3663, "CreativeWork"), try_include("@id", _arrow3665, "ro-crate-metadata.json"), try_include("about", _arrow3667, oa), ("conformsTo", conforms_to_jsonvalue), ("@context", context_jsonvalue_1)]))
    class ObjectExpr3668(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_2.encode_object(arg)

    return ObjectExpr3668()


ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "filename", "identifier", "title", "description", "submissionDate", "publicReleaseDate", "ontologySourceReferences", "publications", "people", "studies", "comments", "@type", "@context"])

def ISAJson_encoder(id_map: Any | None, inv: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], id_map: Any=id_map, inv: Any=inv) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3674(__unit: None=None, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        value: str = ROCrate_genID(inv)
        class ObjectExpr3673(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3673()

    def _arrow3676(__unit: None=None, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        value_1: str = ArcInvestigation.FileName()
        class ObjectExpr3675(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr3675()

    def _arrow3678(__unit: None=None, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        value_2: str = inv.Identifier
        class ObjectExpr3677(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr3677()

    def _arrow3680(value_3: str, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        class ObjectExpr3679(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_3)

        return ObjectExpr3679()

    def _arrow3682(value_5: str, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        class ObjectExpr3681(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_5)

        return ObjectExpr3681()

    def _arrow3684(value_7: str, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        class ObjectExpr3683(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_7)

        return ObjectExpr3683()

    def _arrow3686(value_9: str, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        class ObjectExpr3685(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_9)

        return ObjectExpr3685()

    def _arrow3687(osr: OntologySourceReference, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_1(id_map, osr)

    def _arrow3688(oa: Publication, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_2(id_map, oa)

    def _arrow3689(person: Person, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_3(id_map, person)

    def _arrow3690(s: ArcStudy, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_4(id_map, None, s)

    def _arrow3691(comment: Comment, id_map: Any=id_map, inv: Any=inv) -> IEncodable:
        return ISAJson_encoder_5(id_map, comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow3674()), ("filename", _arrow3676()), ("identifier", _arrow3678()), try_include("title", _arrow3680, inv.Title), try_include("description", _arrow3682, inv.Description), try_include("submissionDate", _arrow3684, inv.SubmissionDate), try_include("publicReleaseDate", _arrow3686, inv.PublicReleaseDate), try_include_seq("ontologySourceReferences", _arrow3687, inv.OntologySourceReferences), try_include_seq("publications", _arrow3688, inv.Publications), try_include_seq("people", _arrow3689, inv.Contacts), try_include_seq("studies", _arrow3690, inv.Studies), try_include_seq("comments", _arrow3691, inv.Comments)]))
    class ObjectExpr3693(IEncodable):
        def Encode(self, helpers_7: IEncoderHelpers_1[Any], id_map: Any=id_map, inv: Any=inv) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_7))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_7.encode_object(arg)

    return ObjectExpr3693()


def _arrow3705(get: IGetters) -> ArcInvestigation:
    identifer: str
    match_value: str | None
    object_arg: IOptionalGetter = get.Optional
    match_value = object_arg.Field("identifier", string)
    identifer = create_missing_identifier() if (match_value is None) else match_value
    def _arrow3694(__unit: None=None) -> FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]] | None:
        arg_3: Decoder_1[FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]]] = list_1_1(ISAJson_decoder_1)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("studies", arg_3)

    pattern_input: tuple[FSharpList[ArcStudy], FSharpList[FSharpList[ArcAssay]]] = unzip(default_arg(_arrow3694(), empty()))
    studies_raw: FSharpList[ArcStudy] = pattern_input[0]
    def projection(a: ArcAssay) -> str:
        return a.Identifier

    class ObjectExpr3696:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow3695(x: str, y: str) -> bool:
                return x == y

            return _arrow3695

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    assays: Array[ArcAssay] = list(distinct_by(projection, concat(pattern_input[1]), ObjectExpr3696()))
    studies: Array[ArcStudy] = list(studies_raw)
    def mapping(a_1: ArcStudy) -> str:
        return a_1.Identifier

    study_identifiers: Array[str] = list(map_1(mapping, studies_raw))
    def _arrow3697(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("title", string)

    def _arrow3698(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("description", string)

    def _arrow3699(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("submissionDate", string)

    def _arrow3700(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("publicReleaseDate", string)

    def _arrow3701(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_13: Decoder_1[Array[OntologySourceReference]] = resize_array(ISAJson_decoder_2)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("ontologySourceReferences", arg_13)

    def _arrow3702(__unit: None=None) -> Array[Publication] | None:
        arg_15: Decoder_1[Array[Publication]] = resize_array(ISAJson_decoder_3)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("publications", arg_15)

    def _arrow3703(__unit: None=None) -> Array[Person] | None:
        arg_17: Decoder_1[Array[Person]] = resize_array(ISAJson_decoder_4)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("people", arg_17)

    def _arrow3704(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = resize_array(ISAJson_decoder_5)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return ArcInvestigation(identifer, _arrow3697(), _arrow3698(), _arrow3699(), _arrow3700(), _arrow3701(), _arrow3702(), _arrow3703(), assays, studies, None, None, study_identifiers, _arrow3704())


ISAJson_decoder: Decoder_1[ArcInvestigation] = Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow3705)

__all__ = ["encoder", "decoder", "encoder_compressed", "decoder_compressed", "ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ROCrate_encodeRoCrate", "ISAJson_allowedFields", "ISAJson_encoder", "ISAJson_decoder"]

