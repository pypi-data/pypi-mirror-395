from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.array_ import map as map_1
from ...fable_modules.fable_library.date import to_string as to_string_1
from ...fable_modules.fable_library.seq import map
from ...fable_modules.fable_library.types import (to_string, Array)
from ...fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ...fable_modules.thoth_json_core.decode import (and_then, succeed, string, object, IRequiredGetter, guid, resize_array, IOptionalGetter, IGetters, datetime_local, array as array_2)
from ...fable_modules.thoth_json_core.encode import seq
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.person import Person
from ...Core.Table.arc_table import ArcTable
from ...Core.Table.composite_cell import CompositeCell
from ...Core.template import (Organisation, Template)
from ..decode import Decode_datetime
from ..encode import date_time
from ..ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder)
from ..person import (encoder as encoder_1, decoder as decoder_2)
from .arc_table import (encoder, decoder as decoder_1, encoder_compressed, decoder_compressed)

__A_ = TypeVar("__A_")

def _arrow3030(arg: Organisation) -> IEncodable:
    value: str = to_string(arg)
    class ObjectExpr3029(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string(value)

    return ObjectExpr3029()


Template_Organisation_encoder: Callable[[Organisation], IEncodable] = _arrow3030

def cb(text_value: str) -> Decoder_1[Organisation]:
    return succeed(Organisation.of_string(text_value))


Template_Organisation_decoder: Decoder_1[Organisation] = and_then(cb, string)

def Template_encoder(template: Template) -> IEncodable:
    def _arrow3032(__unit: None=None, template: Any=template) -> IEncodable:
        value_1: str
        copy_of_struct: str = template.Id
        value_1 = str(copy_of_struct)
        class ObjectExpr3031(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value_1)

        return ObjectExpr3031()

    def _arrow3037(__unit: None=None, template: Any=template) -> IEncodable:
        value_3: str = template.Name
        class ObjectExpr3036(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_3)

        return ObjectExpr3036()

    def _arrow3041(__unit: None=None, template: Any=template) -> IEncodable:
        value_4: str = template.Description
        class ObjectExpr3040(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr3040()

    def _arrow3044(__unit: None=None, template: Any=template) -> IEncodable:
        value_5: str = template.Version
        class ObjectExpr3043(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr3043()

    def mapping(person: Person, template: Any=template) -> IEncodable:
        return encoder_1(person)

    def mapping_1(oa: OntologyAnnotation, template: Any=template) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def mapping_2(oa_1: OntologyAnnotation, template: Any=template) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    values_3: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("id", _arrow3032()), ("table", encoder(template.Table)), ("name", _arrow3037()), ("description", _arrow3041()), ("organisation", Template_Organisation_encoder(template.Organisation)), ("version", _arrow3044()), ("authors", seq(map(mapping, template.Authors))), ("endpoint_repositories", seq(map(mapping_1, template.EndpointRepositories))), ("tags", seq(map(mapping_2, template.Tags))), ("last_updated", date_time(template.LastUpdated))])
    class ObjectExpr3057(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], template: Any=template) -> Any:
            def mapping_3(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping_3, values_3)
            return helpers_4.encode_object(arg)

    return ObjectExpr3057()


def _arrow3084(get: IGetters) -> Template:
    def _arrow3061(__unit: None=None) -> str:
        object_arg: IRequiredGetter = get.Required
        return object_arg.Field("id", guid)

    def _arrow3063(__unit: None=None) -> ArcTable:
        object_arg_1: IRequiredGetter = get.Required
        return object_arg_1.Field("table", decoder_1)

    def _arrow3066(__unit: None=None) -> str:
        object_arg_2: IRequiredGetter = get.Required
        return object_arg_2.Field("name", string)

    def _arrow3067(__unit: None=None) -> str:
        object_arg_3: IRequiredGetter = get.Required
        return object_arg_3.Field("description", string)

    def _arrow3069(__unit: None=None) -> Organisation:
        object_arg_4: IRequiredGetter = get.Required
        return object_arg_4.Field("organisation", Template_Organisation_decoder)

    def _arrow3070(__unit: None=None) -> str:
        object_arg_5: IRequiredGetter = get.Required
        return object_arg_5.Field("version", string)

    def _arrow3072(__unit: None=None) -> Array[Person] | None:
        arg_13: Decoder_1[Array[Person]] = resize_array(decoder_2)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("authors", arg_13)

    def _arrow3077(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_15: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("endpoint_repositories", arg_15)

    def _arrow3080(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_17: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("tags", arg_17)

    def _arrow3083(__unit: None=None) -> Any:
        object_arg_9: IRequiredGetter = get.Required
        return object_arg_9.Field("last_updated", Decode_datetime)

    return Template.create(_arrow3061(), _arrow3063(), _arrow3066(), _arrow3067(), _arrow3069(), _arrow3070(), _arrow3072(), _arrow3077(), _arrow3080(), _arrow3083())


Template_decoder: Decoder_1[Template] = object(_arrow3084)

def Template_encoderCompressed(string_table: Any, oa_table: Any, cell_table: Any, template: Template) -> IEncodable:
    def _arrow3088(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, template: Any=template) -> IEncodable:
        value_1: str
        copy_of_struct: str = template.Id
        value_1 = str(copy_of_struct)
        class ObjectExpr3087(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value_1)

        return ObjectExpr3087()

    def _arrow3091(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, template: Any=template) -> IEncodable:
        value_3: str = template.Name
        class ObjectExpr3090(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_3)

        return ObjectExpr3090()

    def _arrow3093(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, template: Any=template) -> IEncodable:
        value_4: str = template.Description
        class ObjectExpr3092(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr3092()

    def _arrow3097(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, template: Any=template) -> IEncodable:
        value_5: str = template.Version
        class ObjectExpr3096(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr3096()

    def mapping(person: Person, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, template: Any=template) -> IEncodable:
        return encoder_1(person)

    def mapping_1(oa: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, template: Any=template) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def mapping_2(oa_1: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, template: Any=template) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow3101(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, template: Any=template) -> IEncodable:
        value_1_1: str = to_string_1(template.LastUpdated, "O", {})
        class ObjectExpr3100(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_1_1)

        return ObjectExpr3100()

    values_3: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("id", _arrow3088()), ("table", encoder_compressed(string_table, oa_table, cell_table, template.Table)), ("name", _arrow3091()), ("description", _arrow3093()), ("organisation", Template_Organisation_encoder(template.Organisation)), ("version", _arrow3097()), ("authors", seq(map(mapping, template.Authors))), ("endpoint_repositories", seq(map(mapping_1, template.EndpointRepositories))), ("tags", seq(map(mapping_2, template.Tags))), ("last_updated", _arrow3101())])
    class ObjectExpr3102(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, template: Any=template) -> Any:
            def mapping_3(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_5))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping_3, values_3)
            return helpers_5.encode_object(arg)

    return ObjectExpr3102()


def Template_decoderCompressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[Template]:
    def _arrow3115(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> Template:
        def _arrow3103(__unit: None=None) -> str:
            object_arg: IRequiredGetter = get.Required
            return object_arg.Field("id", guid)

        def _arrow3104(__unit: None=None) -> ArcTable:
            arg_3: Decoder_1[ArcTable] = decoder_compressed(string_table, oa_table, cell_table)
            object_arg_1: IRequiredGetter = get.Required
            return object_arg_1.Field("table", arg_3)

        def _arrow3106(__unit: None=None) -> str:
            object_arg_2: IRequiredGetter = get.Required
            return object_arg_2.Field("name", string)

        def _arrow3108(__unit: None=None) -> str:
            object_arg_3: IRequiredGetter = get.Required
            return object_arg_3.Field("description", string)

        def _arrow3109(__unit: None=None) -> Organisation:
            object_arg_4: IRequiredGetter = get.Required
            return object_arg_4.Field("organisation", Template_Organisation_decoder)

        def _arrow3110(__unit: None=None) -> str:
            object_arg_5: IRequiredGetter = get.Required
            return object_arg_5.Field("version", string)

        def _arrow3111(__unit: None=None) -> Array[Person] | None:
            arg_13: Decoder_1[Array[Person]] = resize_array(decoder_2)
            object_arg_6: IOptionalGetter = get.Optional
            return object_arg_6.Field("authors", arg_13)

        def _arrow3112(__unit: None=None) -> Array[OntologyAnnotation] | None:
            arg_15: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
            object_arg_7: IOptionalGetter = get.Optional
            return object_arg_7.Field("endpoint_repositories", arg_15)

        def _arrow3113(__unit: None=None) -> Array[OntologyAnnotation] | None:
            arg_17: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
            object_arg_8: IOptionalGetter = get.Optional
            return object_arg_8.Field("tags", arg_17)

        def _arrow3114(__unit: None=None) -> Any:
            object_arg_9: IRequiredGetter = get.Required
            return object_arg_9.Field("last_updated", datetime_local)

        return Template.create(_arrow3103(), _arrow3104(), _arrow3106(), _arrow3108(), _arrow3109(), _arrow3110(), _arrow3111(), _arrow3112(), _arrow3113(), _arrow3114())

    return object(_arrow3115)


def Templates_encoder(templates: Array[Template]) -> IEncodable:
    def mapping(template: Template, templates: Any=templates) -> IEncodable:
        return Template_encoder(template)

    values: Array[IEncodable] = map_1(mapping, templates, None)
    class ObjectExpr3117(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], templates: Any=templates) -> Any:
            def mapping_1(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_1(mapping_1, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr3117()


Templates_decoder: Decoder_1[Array[Template]] = array_2(Template_decoder)

__all__ = ["Template_Organisation_encoder", "Template_Organisation_decoder", "Template_encoder", "Template_decoder", "Template_encoderCompressed", "Template_decoderCompressed", "Templates_encoder", "Templates_decoder"]

