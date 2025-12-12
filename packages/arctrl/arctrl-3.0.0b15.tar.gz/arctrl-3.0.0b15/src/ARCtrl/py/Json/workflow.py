from __future__ import annotations
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.seq import map as map_1
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, IOptionalGetter, resize_array, IGetters)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.arc_types import ArcWorkflow
from ..Core.comment import Comment
from ..Core.datamap import Datamap
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from ..Core.Process.component import Component
from ..Core.Table.composite_cell import CompositeCell
from .comment import (encoder as encoder_4, decoder as decoder_4)
from .Datamap.datamap import (encoder as encoder_1, decoder as decoder_2, encoder_compressed as encoder_compressed_1, decoder_compressed as decoder_compressed_1)
from .encode import (try_include, try_include_seq)
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder)
from .person import (encoder as encoder_3, decoder as decoder_3)
from .Process.component import (encoder as encoder_2, decoder as decoder_1)

__A_ = TypeVar("__A_")

def encoder(workflow: ArcWorkflow) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], workflow: Any=workflow) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3252(__unit: None=None, workflow: Any=workflow) -> IEncodable:
        value: str = workflow.Identifier
        class ObjectExpr3251(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3251()

    def _arrow3253(oa: OntologyAnnotation, workflow: Any=workflow) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def _arrow3255(value_1: str, workflow: Any=workflow) -> IEncodable:
        class ObjectExpr3254(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr3254()

    def _arrow3257(value_3: str, workflow: Any=workflow) -> IEncodable:
        class ObjectExpr3256(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_3)

        return ObjectExpr3256()

    def _arrow3259(value_5: str, workflow: Any=workflow) -> IEncodable:
        class ObjectExpr3258(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr3258()

    def _arrow3261(value_7: str, workflow: Any=workflow) -> IEncodable:
        class ObjectExpr3260(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_7)

        return ObjectExpr3260()

    def _arrow3262(dm: Datamap, workflow: Any=workflow) -> IEncodable:
        return encoder_1(dm)

    def _arrow3264(value_9: str, workflow: Any=workflow) -> IEncodable:
        class ObjectExpr3263(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_9)

        return ObjectExpr3263()

    def _arrow3265(oa_1: OntologyAnnotation, workflow: Any=workflow) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow3266(value_11: Component, workflow: Any=workflow) -> IEncodable:
        return encoder_2(value_11)

    def _arrow3267(person: Person, workflow: Any=workflow) -> IEncodable:
        return encoder_3(person)

    def _arrow3268(comment: Comment, workflow: Any=workflow) -> IEncodable:
        return encoder_4(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow3252()), try_include("WorkflowType", _arrow3253, workflow.WorkflowType), try_include("Title", _arrow3255, workflow.Title), try_include("URI", _arrow3257, workflow.URI), try_include("Description", _arrow3259, workflow.Description), try_include("Version", _arrow3261, workflow.Version), try_include("Datamap", _arrow3262, workflow.Datamap), try_include_seq("SubWorkflowIdentifiers", _arrow3264, workflow.SubWorkflowIdentifiers), try_include_seq("Parameters", _arrow3265, workflow.Parameters), try_include_seq("Components", _arrow3266, workflow.Components), try_include_seq("Contacts", _arrow3267, workflow.Contacts), try_include_seq("Comments", _arrow3268, workflow.Comments)]))
    class ObjectExpr3269(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], workflow: Any=workflow) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr3269()


def _arrow3282(get: IGetters) -> ArcWorkflow:
    def _arrow3270(__unit: None=None) -> str:
        object_arg: IRequiredGetter = get.Required
        return object_arg.Field("Identifier", string)

    def _arrow3271(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("Title", string)

    def _arrow3272(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("Description", string)

    def _arrow3273(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("WorkflowType", OntologyAnnotation_decoder)

    def _arrow3274(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("URI", string)

    def _arrow3275(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("Version", string)

    def _arrow3276(__unit: None=None) -> Array[str] | None:
        arg_13: Decoder_1[Array[str]] = resize_array(string)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("SubWorkflowIdentifiers", arg_13)

    def _arrow3277(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_15: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("Parameters", arg_15)

    def _arrow3278(__unit: None=None) -> Array[Component] | None:
        arg_17: Decoder_1[Array[Component]] = resize_array(decoder_1)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("Components", arg_17)

    def _arrow3279(__unit: None=None) -> Datamap | None:
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("Datamap", decoder_2)

    def _arrow3280(__unit: None=None) -> Array[Person] | None:
        arg_21: Decoder_1[Array[Person]] = resize_array(decoder_3)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("Contacts", arg_21)

    def _arrow3281(__unit: None=None) -> Array[Comment] | None:
        arg_23: Decoder_1[Array[Comment]] = resize_array(decoder_4)
        object_arg_11: IOptionalGetter = get.Optional
        return object_arg_11.Field("Comments", arg_23)

    return ArcWorkflow.create(_arrow3270(), _arrow3271(), _arrow3272(), _arrow3273(), _arrow3274(), _arrow3275(), _arrow3276(), _arrow3277(), _arrow3278(), _arrow3279(), _arrow3280(), None, _arrow3281())


decoder: Decoder_1[ArcWorkflow] = object(_arrow3282)

def encoder_compressed(string_table: Any, oa_table: Any, cell_table: Any, workflow: ArcWorkflow) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3286(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> IEncodable:
        value: str = workflow.Identifier
        class ObjectExpr3285(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3285()

    def _arrow3287(oa: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def _arrow3289(value_1: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> IEncodable:
        class ObjectExpr3288(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr3288()

    def _arrow3291(value_3: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> IEncodable:
        class ObjectExpr3290(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_3)

        return ObjectExpr3290()

    def _arrow3293(value_5: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> IEncodable:
        class ObjectExpr3292(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr3292()

    def _arrow3295(value_7: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> IEncodable:
        class ObjectExpr3294(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_7)

        return ObjectExpr3294()

    def _arrow3296(dm: Datamap, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> IEncodable:
        return encoder_compressed_1(string_table, oa_table, cell_table, dm)

    def _arrow3298(value_9: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> IEncodable:
        class ObjectExpr3297(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_9)

        return ObjectExpr3297()

    def _arrow3299(oa_1: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow3300(value_11: Component, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> IEncodable:
        return encoder_2(value_11)

    def _arrow3301(person: Person, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> IEncodable:
        return encoder_3(person)

    def _arrow3302(comment: Comment, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> IEncodable:
        return encoder_4(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow3286()), try_include("WorkflowType", _arrow3287, workflow.WorkflowType), try_include("Title", _arrow3289, workflow.Title), try_include("URI", _arrow3291, workflow.URI), try_include("Description", _arrow3293, workflow.Description), try_include("Version", _arrow3295, workflow.Version), try_include("Datamap", _arrow3296, workflow.Datamap), try_include_seq("SubWorkflowIdentifiers", _arrow3298, workflow.SubWorkflowIdentifiers), try_include_seq("Parameters", _arrow3299, workflow.Parameters), try_include_seq("Components", _arrow3300, workflow.Components), try_include_seq("Contacts", _arrow3301, workflow.Contacts), try_include_seq("Comments", _arrow3302, workflow.Comments)]))
    class ObjectExpr3303(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, workflow: Any=workflow) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr3303()


def decoder_compressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[ArcWorkflow]:
    def _arrow3316(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> ArcWorkflow:
        def _arrow3304(__unit: None=None) -> str:
            object_arg: IRequiredGetter = get.Required
            return object_arg.Field("Identifier", string)

        def _arrow3305(__unit: None=None) -> str | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("Title", string)

        def _arrow3306(__unit: None=None) -> str | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("Description", string)

        def _arrow3307(__unit: None=None) -> OntologyAnnotation | None:
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("WorkflowType", OntologyAnnotation_decoder)

        def _arrow3308(__unit: None=None) -> str | None:
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("URI", string)

        def _arrow3309(__unit: None=None) -> str | None:
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("Version", string)

        def _arrow3310(__unit: None=None) -> Array[str] | None:
            arg_13: Decoder_1[Array[str]] = resize_array(string)
            object_arg_6: IOptionalGetter = get.Optional
            return object_arg_6.Field("SubWorkflowIdentifiers", arg_13)

        def _arrow3311(__unit: None=None) -> Array[OntologyAnnotation] | None:
            arg_15: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
            object_arg_7: IOptionalGetter = get.Optional
            return object_arg_7.Field("Parameters", arg_15)

        def _arrow3312(__unit: None=None) -> Array[Component] | None:
            arg_17: Decoder_1[Array[Component]] = resize_array(decoder_1)
            object_arg_8: IOptionalGetter = get.Optional
            return object_arg_8.Field("Components", arg_17)

        def _arrow3313(__unit: None=None) -> Datamap | None:
            arg_19: Decoder_1[Datamap] = decoder_compressed_1(string_table, oa_table, cell_table)
            object_arg_9: IOptionalGetter = get.Optional
            return object_arg_9.Field("Datamap", arg_19)

        def _arrow3314(__unit: None=None) -> Array[Person] | None:
            arg_21: Decoder_1[Array[Person]] = resize_array(decoder_3)
            object_arg_10: IOptionalGetter = get.Optional
            return object_arg_10.Field("Contacts", arg_21)

        def _arrow3315(__unit: None=None) -> Array[Comment] | None:
            arg_23: Decoder_1[Array[Comment]] = resize_array(decoder_4)
            object_arg_11: IOptionalGetter = get.Optional
            return object_arg_11.Field("Comments", arg_23)

        return ArcWorkflow.create(_arrow3304(), _arrow3305(), _arrow3306(), _arrow3307(), _arrow3308(), _arrow3309(), _arrow3310(), _arrow3311(), _arrow3312(), _arrow3313(), _arrow3314(), None, _arrow3315())

    return object(_arrow3316)


__all__ = ["encoder", "decoder", "encoder_compressed", "decoder_compressed"]

