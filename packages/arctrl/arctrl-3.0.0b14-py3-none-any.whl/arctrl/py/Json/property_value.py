from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.seq import map as map_1
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, IGetters)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.iproperty_value import IPropertyValue
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.value import Value as Value_4
from .context.rocrate.property_value_context import context_jsonvalue
from .encode import try_include
from .ontology_annotation import AnnotationValue_decoder

__A_ = TypeVar("__A_")

_T = TypeVar("_T")

def gen_id(p: IPropertyValue) -> str:
    match_value: OntologyAnnotation | None = p.GetCategory()
    match_value_1: Value_4 | None = p.GetValue()
    match_value_2: OntologyAnnotation | None = p.GetUnit()
    (pattern_matching_result, t, u, v, t_1, v_1) = (None, None, None, None, None, None)
    if match_value is not None:
        if match_value_1 is not None:
            if match_value_2 is None:
                pattern_matching_result = 1
                t_1 = match_value
                v_1 = match_value_1

            else: 
                pattern_matching_result = 0
                t = match_value
                u = match_value_2
                v = match_value_1


        else: 
            pattern_matching_result = 2


    else: 
        pattern_matching_result = 2

    if pattern_matching_result == 0:
        return ((((((("#" + p.GetAdditionalType()) + "/") + t.NameText) + "=") + v.Text) + "") + u.NameText) + ""

    elif pattern_matching_result == 1:
        return ((((("#" + p.GetAdditionalType()) + "/") + t_1.NameText) + "=") + v_1.Text) + ""

    elif pattern_matching_result == 2:
        return ("#Empty" + p.GetAdditionalType()) + ""



def encoder(pv: IPropertyValue) -> IEncodable:
    pattern_input: tuple[str | None, str | None]
    match_value: OntologyAnnotation | None = pv.GetCategory()
    if match_value is None:
        pattern_input = (None, None)

    else: 
        oa: OntologyAnnotation = match_value
        pattern_input = (oa.Name, oa.TermAccessionNumber)

    pattern_input_1: tuple[IEncodable | None, IEncodable | None]
    match_value_1: Value_4 | None = pv.GetValue()
    if match_value_1 is None:
        pattern_input_1 = (None, None)

    else: 
        v: Value_4 = match_value_1
        if v.tag == 1:
            class ObjectExpr2330(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any], pv: Any=pv) -> Any:
                    return helpers_1.encode_signed_integral_number(v.fields[0])

            pattern_input_1 = (ObjectExpr2330(), None)

        elif v.tag == 2:
            class ObjectExpr2331(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any], pv: Any=pv) -> Any:
                    return helpers_2.encode_decimal_number(v.fields[0])

            pattern_input_1 = (ObjectExpr2331(), None)

        elif v.tag == 0:
            oa_1: OntologyAnnotation = v.fields[0]
            def _arrow2333(value_3: str, pv: Any=pv) -> IEncodable:
                class ObjectExpr2332(IEncodable):
                    def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                        return helpers_3.encode_string(value_3)

                return ObjectExpr2332()

            def _arrow2335(value_5: str, pv: Any=pv) -> IEncodable:
                class ObjectExpr2334(IEncodable):
                    def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                        return helpers_4.encode_string(value_5)

                return ObjectExpr2334()

            pattern_input_1 = (map(_arrow2333, oa_1.Name), map(_arrow2335, oa_1.TermAccessionNumber))

        else: 
            class ObjectExpr2336(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any], pv: Any=pv) -> Any:
                    return helpers.encode_string(v.fields[0])

            pattern_input_1 = (ObjectExpr2336(), None)


    pattern_input_2: tuple[str | None, str | None]
    match_value_2: OntologyAnnotation | None = pv.GetUnit()
    if match_value_2 is None:
        pattern_input_2 = (None, None)

    else: 
        oa_2: OntologyAnnotation = match_value_2
        pattern_input_2 = (oa_2.Name, oa_2.TermAccessionNumber)

    def chooser(tupled_arg: tuple[str, IEncodable | None], pv: Any=pv) -> tuple[str, IEncodable] | None:
        def mapping(v_1_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1_1)

        return map(mapping, tupled_arg[1])

    def _arrow2340(__unit: None=None, pv: Any=pv) -> IEncodable:
        value_8: str = gen_id(pv)
        class ObjectExpr2339(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_8)

        return ObjectExpr2339()

    class ObjectExpr2341(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], pv: Any=pv) -> Any:
            return helpers_6.encode_string("PropertyValue")

    def _arrow2343(__unit: None=None, pv: Any=pv) -> IEncodable:
        value_10: str = pv.GetAdditionalType()
        class ObjectExpr2342(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                return helpers_7.encode_string(value_10)

        return ObjectExpr2342()

    def _arrow2345(value_11: str, pv: Any=pv) -> IEncodable:
        class ObjectExpr2344(IEncodable):
            def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                return helpers_8.encode_string(value_11)

        return ObjectExpr2344()

    def _arrow2347(value_13: str, pv: Any=pv) -> IEncodable:
        class ObjectExpr2346(IEncodable):
            def Encode(self, helpers_9: IEncoderHelpers_1[Any]) -> Any:
                return helpers_9.encode_string(value_13)

        return ObjectExpr2346()

    def _arrow2349(value_15: str, pv: Any=pv) -> IEncodable:
        class ObjectExpr2348(IEncodable):
            def Encode(self, helpers_10: IEncoderHelpers_1[Any]) -> Any:
                return helpers_10.encode_string(value_15)

        return ObjectExpr2348()

    def _arrow2351(value_17: str, pv: Any=pv) -> IEncodable:
        class ObjectExpr2350(IEncodable):
            def Encode(self, helpers_11: IEncoderHelpers_1[Any]) -> Any:
                return helpers_11.encode_string(value_17)

        return ObjectExpr2350()

    def _arrow2353(value_19: str, pv: Any=pv) -> IEncodable:
        class ObjectExpr2352(IEncodable):
            def Encode(self, helpers_12: IEncoderHelpers_1[Any]) -> Any:
                return helpers_12.encode_string(value_19)

        return ObjectExpr2352()

    def _arrow2354(x: IEncodable, pv: Any=pv) -> IEncodable:
        return x

    def _arrow2355(x_1: IEncodable, pv: Any=pv) -> IEncodable:
        return x_1

    def _arrow2357(value_21: str, pv: Any=pv) -> IEncodable:
        class ObjectExpr2356(IEncodable):
            def Encode(self, helpers_13: IEncoderHelpers_1[Any]) -> Any:
                return helpers_13.encode_string(value_21)

        return ObjectExpr2356()

    def _arrow2359(value_23: str, pv: Any=pv) -> IEncodable:
        class ObjectExpr2358(IEncodable):
            def Encode(self, helpers_14: IEncoderHelpers_1[Any]) -> Any:
                return helpers_14.encode_string(value_23)

        return ObjectExpr2358()

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2340()), ("@type", ObjectExpr2341()), ("additionalType", _arrow2343()), try_include("alternateName", _arrow2345, pv.AlternateName()), try_include("measurementMethod", _arrow2347, pv.MeasurementMethod()), try_include("description", _arrow2349, pv.Description()), try_include("category", _arrow2351, pattern_input[0]), try_include("categoryCode", _arrow2353, pattern_input[1]), try_include("value", _arrow2354, pattern_input_1[0]), try_include("valueCode", _arrow2355, pattern_input_1[1]), try_include("unit", _arrow2357, pattern_input_2[0]), try_include("unitCode", _arrow2359, pattern_input_2[1]), ("@context", context_jsonvalue)]))
    class ObjectExpr2360(IEncodable):
        def Encode(self, helpers_15: IEncoderHelpers_1[Any], pv: Any=pv) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_15))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_15.encode_object(arg)

    return ObjectExpr2360()


def decoder(create: Callable[[str | None, str | None, str | None, OntologyAnnotation | None, Value_4 | None, OntologyAnnotation | None], _T]) -> Decoder_1[Any]:
    def _arrow2362(get: IGetters, create: Any=create) -> _T:
        alternate_name: str | None
        object_arg: IOptionalGetter = get.Optional
        alternate_name = object_arg.Field("alternateName", string)
        measurement_method: str | None
        object_arg_1: IOptionalGetter = get.Optional
        measurement_method = object_arg_1.Field("measurementMethod", string)
        description: str | None
        object_arg_2: IOptionalGetter = get.Optional
        description = object_arg_2.Field("description", string)
        category: OntologyAnnotation | None
        name: str | None
        object_arg_3: IOptionalGetter = get.Optional
        name = object_arg_3.Field("category", string)
        code: str | None
        object_arg_4: IOptionalGetter = get.Optional
        code = object_arg_4.Field("categoryCode", string)
        (pattern_matching_result, code_1) = (None, None)
        if name is None:
            if code is not None:
                if code == "":
                    pattern_matching_result = 0

                else: 
                    pattern_matching_result = 2
                    code_1 = code


            else: 
                pattern_matching_result = 0


        elif code is not None:
            if code == "":
                pattern_matching_result = 1

            else: 
                pattern_matching_result = 2
                code_1 = code


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            category = None

        elif pattern_matching_result == 1:
            try: 
                category = OntologyAnnotation.create(name)

            except Exception as err:
                raise Exception(((("Error while decoding category (name:" + str(name)) + "): ") + str(err)) + "")


        elif pattern_matching_result == 2:
            try: 
                category = OntologyAnnotation.from_term_annotation(code_1, name)

            except Exception as err_1:
                raise Exception(((((("Error while decoding category (name:" + str(name)) + ", code:") + code_1) + "): ") + str(err_1)) + "")


        unit: OntologyAnnotation | None
        name_1: str | None
        object_arg_5: IOptionalGetter = get.Optional
        name_1 = object_arg_5.Field("unit", string)
        code_2: str | None
        object_arg_6: IOptionalGetter = get.Optional
        code_2 = object_arg_6.Field("unitCode", string)
        (pattern_matching_result_1, code_3) = (None, None)
        if name_1 is None:
            if code_2 is not None:
                if code_2 == "":
                    pattern_matching_result_1 = 0

                else: 
                    pattern_matching_result_1 = 2
                    code_3 = code_2


            else: 
                pattern_matching_result_1 = 0


        elif code_2 is not None:
            if code_2 == "":
                pattern_matching_result_1 = 1

            else: 
                pattern_matching_result_1 = 2
                code_3 = code_2


        else: 
            pattern_matching_result_1 = 1

        if pattern_matching_result_1 == 0:
            unit = None

        elif pattern_matching_result_1 == 1:
            try: 
                unit = OntologyAnnotation.create(name_1)

            except Exception as err_2:
                raise Exception(((("Error while decoding unit (name:" + str(name_1)) + "): ") + str(err_2)) + "")


        elif pattern_matching_result_1 == 2:
            try: 
                unit = OntologyAnnotation.from_term_annotation(code_3, name_1)

            except Exception as err_3:
                raise Exception(((((("Error while decoding unit (name:" + str(name_1)) + ", code:") + code_3) + "): ") + str(err_3)) + "")


        def _arrow2361(__unit: None=None) -> Value_4 | None:
            value: str | None
            object_arg_7: IOptionalGetter = get.Optional
            value = object_arg_7.Field("value", AnnotationValue_decoder)
            code_4: str | None
            object_arg_8: IOptionalGetter = get.Optional
            code_4 = object_arg_8.Field("valueCode", string)
            if (code_4 is None) if (value is None) else False:
                return None

            else: 
                try: 
                    return Value_4.from_options(value, None, code_4)

                except Exception as err_4:
                    raise Exception(((((("Error while decoding value " + str(value)) + ",") + str(code_4)) + ": ") + str(err_4)) + "")



        return create(alternate_name, measurement_method, description, category, _arrow2361(), unit)

    return object(_arrow2362)


__all__ = ["gen_id", "encoder", "decoder"]

