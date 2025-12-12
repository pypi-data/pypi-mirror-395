from __future__ import annotations
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.seq import map as map_1
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, IOptionalGetter, resize_array, IGetters)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.arc_types import ArcRun
from ..Core.comment import Comment
from ..Core.datamap import Datamap
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from ..Core.Table.arc_table import ArcTable
from ..Core.Table.composite_cell import CompositeCell
from .comment import (encoder as encoder_4, decoder as decoder_4)
from .Datamap.datamap import (encoder as encoder_1, decoder as decoder_2, encoder_compressed as encoder_compressed_1, decoder_compressed as decoder_compressed_2)
from .encode import (try_include, try_include_seq)
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder)
from .person import (encoder as encoder_3, decoder as decoder_3)
from .Table.arc_table import (encoder as encoder_2, decoder as decoder_1, encoder_compressed as encoder_compressed_2, decoder_compressed as decoder_compressed_1)

__A_ = TypeVar("__A_")

def encoder(run: ArcRun) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], run: Any=run) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3339(__unit: None=None, run: Any=run) -> IEncodable:
        value: str = run.Identifier
        class ObjectExpr3338(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3338()

    def _arrow3341(value_1: str, run: Any=run) -> IEncodable:
        class ObjectExpr3340(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr3340()

    def _arrow3344(value_3: str, run: Any=run) -> IEncodable:
        class ObjectExpr3343(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_3)

        return ObjectExpr3343()

    def _arrow3345(oa: OntologyAnnotation, run: Any=run) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def _arrow3346(oa_1: OntologyAnnotation, run: Any=run) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow3347(oa_2: OntologyAnnotation, run: Any=run) -> IEncodable:
        return OntologyAnnotation_encoder(oa_2)

    def _arrow3348(dm: Datamap, run: Any=run) -> IEncodable:
        return encoder_1(dm)

    def _arrow3350(value_5: str, run: Any=run) -> IEncodable:
        class ObjectExpr3349(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr3349()

    def _arrow3351(table: ArcTable, run: Any=run) -> IEncodable:
        return encoder_2(table)

    def _arrow3353(person: Person, run: Any=run) -> IEncodable:
        return encoder_3(person)

    def _arrow3355(comment: Comment, run: Any=run) -> IEncodable:
        return encoder_4(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow3339()), try_include("Title", _arrow3341, run.Title), try_include("Description", _arrow3344, run.Description), try_include("MeasurementType", _arrow3345, run.MeasurementType), try_include("TechnologyType", _arrow3346, run.TechnologyType), try_include("TechnologyPlatform", _arrow3347, run.TechnologyPlatform), try_include("Datamap", _arrow3348, run.Datamap), try_include_seq("WorkflowIdentifiers", _arrow3350, run.WorkflowIdentifiers), try_include_seq("Tables", _arrow3351, run.Tables), try_include_seq("Performers", _arrow3353, run.Performers), try_include_seq("Comments", _arrow3355, run.Comments)]))
    class ObjectExpr3360(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], run: Any=run) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr3360()


def _arrow3387(get: IGetters) -> ArcRun:
    def _arrow3368(__unit: None=None) -> str:
        object_arg: IRequiredGetter = get.Required
        return object_arg.Field("Identifier", string)

    def _arrow3369(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("Title", string)

    def _arrow3370(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("Description", string)

    def _arrow3371(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("MeasurementType", OntologyAnnotation_decoder)

    def _arrow3372(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("TechnologyType", OntologyAnnotation_decoder)

    def _arrow3373(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("TechnologyPlatform", OntologyAnnotation_decoder)

    def _arrow3376(__unit: None=None) -> Array[str] | None:
        arg_13: Decoder_1[Array[str]] = resize_array(string)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("WorkflowIdentifiers", arg_13)

    def _arrow3379(__unit: None=None) -> Array[ArcTable] | None:
        arg_15: Decoder_1[Array[ArcTable]] = resize_array(decoder_1)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("Tables", arg_15)

    def _arrow3380(__unit: None=None) -> Datamap | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("Datamap", decoder_2)

    def _arrow3383(__unit: None=None) -> Array[Person] | None:
        arg_19: Decoder_1[Array[Person]] = resize_array(decoder_3)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("Performers", arg_19)

    def _arrow3384(__unit: None=None) -> Array[Comment] | None:
        arg_21: Decoder_1[Array[Comment]] = resize_array(decoder_4)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("Comments", arg_21)

    return ArcRun.create(_arrow3368(), _arrow3369(), _arrow3370(), _arrow3371(), _arrow3372(), _arrow3373(), _arrow3376(), _arrow3379(), _arrow3380(), _arrow3383(), None, None, _arrow3384())


decoder: Decoder_1[ArcRun] = object(_arrow3387)

def encoder_compressed(string_table: Any, oa_table: Any, cell_table: Any, run: ArcRun) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, run: Any=run) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3398(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, run: Any=run) -> IEncodable:
        value: str = run.Identifier
        class ObjectExpr3397(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3397()

    def _arrow3402(value_1: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, run: Any=run) -> IEncodable:
        class ObjectExpr3401(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr3401()

    def _arrow3406(value_3: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, run: Any=run) -> IEncodable:
        class ObjectExpr3405(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_3)

        return ObjectExpr3405()

    def _arrow3408(oa: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, run: Any=run) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def _arrow3409(oa_1: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, run: Any=run) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow3410(oa_2: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, run: Any=run) -> IEncodable:
        return OntologyAnnotation_encoder(oa_2)

    def _arrow3411(dm: Datamap, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, run: Any=run) -> IEncodable:
        return encoder_compressed_1(string_table, oa_table, cell_table, dm)

    def _arrow3414(value_5: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, run: Any=run) -> IEncodable:
        class ObjectExpr3413(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr3413()

    def _arrow3415(table: ArcTable, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, run: Any=run) -> IEncodable:
        return encoder_compressed_2(string_table, oa_table, cell_table, table)

    def _arrow3416(person: Person, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, run: Any=run) -> IEncodable:
        return encoder_3(person)

    def _arrow3417(comment: Comment, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, run: Any=run) -> IEncodable:
        return encoder_4(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow3398()), try_include("Title", _arrow3402, run.Title), try_include("Description", _arrow3406, run.Description), try_include("MeasurementType", _arrow3408, run.MeasurementType), try_include("TechnologyType", _arrow3409, run.TechnologyType), try_include("TechnologyPlatform", _arrow3410, run.TechnologyPlatform), try_include("Datamap", _arrow3411, run.Datamap), try_include_seq("WorkflowIdentifiers", _arrow3414, run.WorkflowIdentifiers), try_include_seq("Tables", _arrow3415, run.Tables), try_include_seq("Performers", _arrow3416, run.Performers), try_include_seq("Comments", _arrow3417, run.Comments)]))
    class ObjectExpr3418(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, run: Any=run) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr3418()


def decoder_compressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[ArcRun]:
    def _arrow3443(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> ArcRun:
        def _arrow3426(__unit: None=None) -> str:
            object_arg: IRequiredGetter = get.Required
            return object_arg.Field("Identifier", string)

        def _arrow3428(__unit: None=None) -> str | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("Title", string)

        def _arrow3429(__unit: None=None) -> str | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("Description", string)

        def _arrow3431(__unit: None=None) -> OntologyAnnotation | None:
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("MeasurementType", OntologyAnnotation_decoder)

        def _arrow3432(__unit: None=None) -> OntologyAnnotation | None:
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("TechnologyType", OntologyAnnotation_decoder)

        def _arrow3434(__unit: None=None) -> OntologyAnnotation | None:
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("TechnologyPlatform", OntologyAnnotation_decoder)

        def _arrow3436(__unit: None=None) -> Array[str] | None:
            arg_13: Decoder_1[Array[str]] = resize_array(string)
            object_arg_6: IOptionalGetter = get.Optional
            return object_arg_6.Field("WorkflowIdentifiers", arg_13)

        def _arrow3439(__unit: None=None) -> Array[ArcTable] | None:
            arg_15: Decoder_1[Array[ArcTable]] = resize_array(decoder_compressed_1(string_table, oa_table, cell_table))
            object_arg_7: IOptionalGetter = get.Optional
            return object_arg_7.Field("Tables", arg_15)

        def _arrow3440(__unit: None=None) -> Datamap | None:
            arg_17: Decoder_1[Datamap] = decoder_compressed_2(string_table, oa_table, cell_table)
            object_arg_8: IOptionalGetter = get.Optional
            return object_arg_8.Field("Datamap", arg_17)

        def _arrow3441(__unit: None=None) -> Array[Person] | None:
            arg_19: Decoder_1[Array[Person]] = resize_array(decoder_3)
            object_arg_9: IOptionalGetter = get.Optional
            return object_arg_9.Field("Performers", arg_19)

        def _arrow3442(__unit: None=None) -> Array[Comment] | None:
            arg_21: Decoder_1[Array[Comment]] = resize_array(decoder_4)
            object_arg_10: IOptionalGetter = get.Optional
            return object_arg_10.Field("Comments", arg_21)

        return ArcRun.create(_arrow3426(), _arrow3428(), _arrow3429(), _arrow3431(), _arrow3432(), _arrow3434(), _arrow3436(), _arrow3439(), _arrow3440(), _arrow3441(), None, None, _arrow3442())

    return object(_arrow3443)


__all__ = ["encoder", "decoder", "encoder_compressed", "decoder_compressed"]

