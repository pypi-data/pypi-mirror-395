from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.array_ import contains
from ...fable_modules.fable_library.int32 import try_parse
from ...fable_modules.fable_library.option import (value as value_3, default_arg, to_array)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.seq import iterate
from ...fable_modules.fable_library.string_ import (join, replace)
from ...fable_modules.fable_library.types import (Array, FSharpRef)
from ...fable_modules.fable_library.util import (string_hash, int32_to_string)
from ...Core.Helper.collections_ import ResizeArray_map
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import (LDNode, LDGraph)
from .formal_parameter import LDFormalParameter

def _expr1756() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDPropertyValue", None, LDPropertyValue)


class LDPropertyValue:
    @staticmethod
    def schema_type() -> str:
        return "http://schema.org/PropertyValue"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def value() -> str:
        return "http://schema.org/value"

    @staticmethod
    def property_id() -> str:
        return "http://schema.org/propertyID"

    @staticmethod
    def unit_code() -> str:
        return "http://schema.org/unitCode"

    @staticmethod
    def unit_text() -> str:
        return "http://schema.org/unitText"

    @staticmethod
    def value_reference() -> str:
        return "http://schema.org/valueReference"

    @staticmethod
    def measurement_method() -> str:
        return "http://schema.org/measurementMethod"

    @staticmethod
    def description() -> str:
        return "http://schema.org/description"

    @staticmethod
    def alternate_name() -> str:
        return "http://schema.org/alternateName"

    @staticmethod
    def subject_of() -> str:
        return "http://schema.org/subjectOf"

    @staticmethod
    def disambiguating_description() -> str:
        return "http://schema.org/disambiguatingDescription"

    @staticmethod
    def doi_key() -> str:
        return "DOI"

    @staticmethod
    def doi_url() -> str:
        return "http://purl.obolibrary.org/obo/OBI_0002110"

    @staticmethod
    def pubmed_idkey() -> str:
        return "PubMedID"

    @staticmethod
    def pubmed_idurl() -> str:
        return "http://purl.obolibrary.org/obo/OBI_0001617"

    @staticmethod
    def prefix_key() -> str:
        return "Prefix"

    @staticmethod
    def position_key() -> str:
        return "Position"

    @staticmethod
    def glob_key() -> str:
        return "Glob"

    @staticmethod
    def example_of_work() -> str:
        return "http://schema.org/exampleOfWork"

    @staticmethod
    def try_get_name_as_string(pv: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = pv.TryGetPropertyAsSingleton(LDPropertyValue.name(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value_3(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value_3(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_name_as_string(pv: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = pv.TryGetPropertyAsSingleton(LDPropertyValue.name(), context)
        if match_value is not None:
            if str(type(value_3(match_value))) == "<class \'str\'>":
                n: str = value_3(match_value)
                return n

            else: 
                raise Exception(("Property of `name` of object with @id `" + pv.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `name` of object with @id `" + pv.Id) + "`")


    @staticmethod
    def set_name_as_string(pv: LDNode, name: str, context: LDContext | None=None) -> Any:
        return pv.SetProperty(LDPropertyValue.name(), name, context)

    @staticmethod
    def get_values_as_string(pv: LDNode, context: LDContext | None=None) -> Array[str]:
        def f(o_1: Any=None) -> Any:
            return o_1

        def filter(o: Any=None, context_1: LDContext | None=None) -> bool:
            return str(type(o)) == "<class \'str\'>"

        return ResizeArray_map(f, pv.GetPropertyValues(LDPropertyValue.value(), filter, context))

    @staticmethod
    def try_get_value_as_string(pv: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = pv.TryGetPropertyAsSingleton(LDPropertyValue.value(), context)
        (pattern_matching_result, v) = (None, None)
        if match_value is not None:
            if str(type(value_3(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                v = value_3(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return v

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_value_as_string(pv: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = pv.TryGetPropertyAsSingleton(LDPropertyValue.value(), context)
        if match_value is not None:
            if str(type(value_3(match_value))) == "<class \'str\'>":
                v: str = value_3(match_value)
                return v

            else: 
                raise Exception(("Property of `value` of object with @id `" + pv.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `value` of object with @id `" + pv.Id) + "`")


    @staticmethod
    def set_value_as_string(pv: LDNode, value: str, context: LDContext | None=None) -> Any:
        return pv.SetProperty(LDPropertyValue.value(), value, context)

    @staticmethod
    def try_get_property_idas_string(pv: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = pv.TryGetPropertyAsSingleton(LDPropertyValue.property_id(), context)
        (pattern_matching_result, pid) = (None, None)
        if match_value is not None:
            if str(type(value_3(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                pid = value_3(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return pid

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_property_idas_string(pv: LDNode, property_id: str, context: LDContext | None=None) -> Any:
        return pv.SetProperty(LDPropertyValue.property_id(), property_id, context)

    @staticmethod
    def try_get_unit_code_as_string(pv: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = pv.TryGetPropertyAsSingleton(LDPropertyValue.unit_code(), context)
        (pattern_matching_result, uc) = (None, None)
        if match_value is not None:
            if str(type(value_3(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                uc = value_3(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return uc

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_unit_code_as_string(pv: LDNode, unit_code: str, context: LDContext | None=None) -> Any:
        return pv.SetProperty(LDPropertyValue.unit_code(), unit_code, context)

    @staticmethod
    def try_get_unit_text_as_string(pv: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = pv.TryGetPropertyAsSingleton(LDPropertyValue.unit_text(), context)
        (pattern_matching_result, ut) = (None, None)
        if match_value is not None:
            if str(type(value_3(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                ut = value_3(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return ut

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_unit_text_as_string(pv: LDNode, unit_text: str, context: LDContext | None=None) -> Any:
        return pv.SetProperty(LDPropertyValue.unit_text(), unit_text, context)

    @staticmethod
    def try_get_value_reference_as_string(pv: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = pv.TryGetPropertyAsSingleton(LDPropertyValue.value_reference(), context)
        (pattern_matching_result, vr) = (None, None)
        if match_value is not None:
            if str(type(value_3(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                vr = value_3(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return vr

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_value_reference_as_string(pv: LDNode, value_reference: str, context: LDContext | None=None) -> Any:
        return pv.SetProperty(LDPropertyValue.value_reference(), value_reference, context)

    @staticmethod
    def try_get_measurement_method_as_string(pv: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = pv.TryGetPropertyAsSingleton(LDPropertyValue.measurement_method(), context)
        (pattern_matching_result, vr) = (None, None)
        if match_value is not None:
            if str(type(value_3(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                vr = value_3(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return vr

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_measurement_method_as_string(pv: LDNode, measurement_method: str, context: LDContext | None=None) -> Any:
        return pv.SetProperty(LDPropertyValue.measurement_method(), measurement_method, context)

    @staticmethod
    def try_get_description_as_string(pv: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = pv.TryGetPropertyAsSingleton(LDPropertyValue.description(), context)
        (pattern_matching_result, vr) = (None, None)
        if match_value is not None:
            if str(type(value_3(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                vr = value_3(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return vr

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_description_as_string(pv: LDNode, description: str, context: LDContext | None=None) -> Any:
        return pv.SetProperty(LDPropertyValue.description(), description, context)

    @staticmethod
    def try_get_alternate_name_as_string(pv: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = pv.TryGetPropertyAsSingleton(LDPropertyValue.alternate_name(), context)
        (pattern_matching_result, vr) = (None, None)
        if match_value is not None:
            if str(type(value_3(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                vr = value_3(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return vr

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_alternate_name_as_string(pv: LDNode, alternate_name: str, context: LDContext | None=None) -> Any:
        return pv.SetProperty(LDPropertyValue.alternate_name(), alternate_name, context)

    @staticmethod
    def get_disambiguating_descriptions_as_string(pv: LDNode, context: LDContext | None=None) -> Array[str]:
        def f(o_1: Any=None) -> Any:
            return o_1

        def filter(o: Any=None, context_1: LDContext | None=None) -> bool:
            return str(type(o)) == "<class \'str\'>"

        return ResizeArray_map(f, pv.GetPropertyValues(LDPropertyValue.disambiguating_description(), filter, context))

    @staticmethod
    def set_disambiguating_descriptions_as_string(lp: LDNode, disambiguating_descriptions: Array[str], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDPropertyValue.disambiguating_description(), disambiguating_descriptions, context)

    @staticmethod
    def try_get_subject_of(pv: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = pv.TryGetPropertyAsSingleNode(LDPropertyValue.subject_of(), graph, context)
        return match_value if (match_value is not None) else None

    @staticmethod
    def set_subject_of(pv: LDNode, subject_of: LDNode, context: LDContext | None=None) -> Any:
        return pv.SetProperty(LDPropertyValue.subject_of(), subject_of, context)

    @staticmethod
    def try_get_example_of_work(dt: LDNode, context: LDContext | None=None) -> Any | None:
        return dt.TryGetPropertyAsSingleton(LDPropertyValue.example_of_work(), context)

    @staticmethod
    def try_get_example_of_work_as_formal_parameter(dt: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = dt.TryGetPropertyAsSingleNode(LDPropertyValue.example_of_work(), graph, context)
        if match_value is not None:
            def _arrow1731(__unit: None=None) -> bool:
                fp: LDNode = match_value
                return LDFormalParameter.validate(fp, context)

            if _arrow1731():
                fp_1: LDNode = match_value
                return fp_1

            else: 
                raise Exception(("Property of `exampleOfWork` of object with @id `" + dt.Id) + "` was not a FormalParameter")


        else: 
            return None


    @staticmethod
    def set_example_of_work(pv: LDNode, example_of_work: LDNode, context: LDContext | None=None) -> Any:
        return pv.SetProperty(LDPropertyValue.example_of_work(), example_of_work, context)

    @staticmethod
    def validate(pv: LDNode, context: LDContext | None=None) -> bool:
        return pv.HasProperty(LDPropertyValue.name(), context) if pv.HasType(LDPropertyValue.schema_type(), context) else False

    @staticmethod
    def validate_component(pv: LDNode, context: LDContext | None=None) -> bool:
        class ObjectExpr1733:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1732(x: str, y: str) -> bool:
                    return x == y

                return _arrow1732

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        return contains("Component", pv.AdditionalType, ObjectExpr1733()) if LDPropertyValue.validate(pv, context) else False

    @staticmethod
    def validate_parameter_value(pv: LDNode, context: LDContext | None=None) -> bool:
        class ObjectExpr1735:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1734(x: str, y: str) -> bool:
                    return x == y

                return _arrow1734

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        class ObjectExpr1737:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1736(x_1: str, y_1: str) -> bool:
                    return x_1 == y_1

                return _arrow1736

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        return (True if contains("ParameterValue", pv.AdditionalType, ObjectExpr1735()) else contains("ProcessParameterValue", pv.AdditionalType, ObjectExpr1737())) if LDPropertyValue.validate(pv, context) else False

    @staticmethod
    def validate_characteristic_value(pv: LDNode, context: LDContext | None=None) -> bool:
        class ObjectExpr1739:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1738(x: str, y: str) -> bool:
                    return x == y

                return _arrow1738

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        class ObjectExpr1741:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1740(x_1: str, y_1: str) -> bool:
                    return x_1 == y_1

                return _arrow1740

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        return (True if contains("CharacteristicValue", pv.AdditionalType, ObjectExpr1739()) else contains("MaterialAttributeValue", pv.AdditionalType, ObjectExpr1741())) if LDPropertyValue.validate(pv, context) else False

    @staticmethod
    def validate_factor_value(pv: LDNode, context: LDContext | None=None) -> bool:
        class ObjectExpr1743:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1742(x: str, y: str) -> bool:
                    return x == y

                return _arrow1742

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        return contains("FactorValue", pv.AdditionalType, ObjectExpr1743()) if LDPropertyValue.validate(pv, context) else False

    @staticmethod
    def validate_fragment_descriptor(pv: LDNode, context: LDContext | None=None) -> bool:
        return (LDPropertyValue.get_name_as_string(pv, context) == "FragmentDescriptor") if LDPropertyValue.validate(pv, context) else False

    @staticmethod
    def validate_cwlparameter(pv: LDNode, context: LDContext | None=None) -> bool:
        class ObjectExpr1745:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1744(x: str, y: str) -> bool:
                    return x == y

                return _arrow1744

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        return contains("WorkflowInput", pv.AdditionalType, ObjectExpr1745()) if (pv.HasProperty(LDPropertyValue.value(), context) if (pv.HasProperty(LDPropertyValue.example_of_work(), context) if LDPropertyValue.validate(pv, context) else False) else False) else False

    @staticmethod
    def validate_doi(pv: LDNode, context: LDContext | None=None) -> bool:
        if LDPropertyValue.validate(pv, context):
            match_value: str | None = LDPropertyValue.try_get_name_as_string(pv, context)
            match_value_1: str | None = LDPropertyValue.try_get_value_as_string(pv, context)
            match_value_2: str | None = LDPropertyValue.try_get_property_idas_string(pv, context)
            (pattern_matching_result,) = (None,)
            if match_value is not None:
                if match_value_1 is not None:
                    if match_value_2 is not None:
                        def _arrow1746(__unit: None=None) -> bool:
                            value: str = match_value_1
                            id: str = match_value_2
                            return (id == LDPropertyValue.doi_url()) if (match_value == LDPropertyValue.doi_key()) else False

                        if _arrow1746():
                            pattern_matching_result = 0

                        else: 
                            pattern_matching_result = 1


                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1

            if pattern_matching_result == 0:
                return True

            elif pattern_matching_result == 1:
                return False


        else: 
            return False


    @staticmethod
    def validate_pub_med_id(pv: LDNode, context: LDContext | None=None) -> bool:
        if LDPropertyValue.validate(pv, context):
            match_value: str | None = LDPropertyValue.try_get_name_as_string(pv, context)
            match_value_1: str | None = LDPropertyValue.try_get_value_as_string(pv, context)
            match_value_2: str | None = LDPropertyValue.try_get_property_idas_string(pv, context)
            (pattern_matching_result,) = (None,)
            if match_value is not None:
                if match_value_1 is not None:
                    if match_value_2 is not None:
                        def _arrow1747(__unit: None=None) -> bool:
                            value: str = match_value_1
                            id: str = match_value_2
                            return (id == LDPropertyValue.pubmed_idurl()) if (match_value == LDPropertyValue.pubmed_idkey()) else False

                        if _arrow1747():
                            pattern_matching_result = 0

                        else: 
                            pattern_matching_result = 1


                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1

            if pattern_matching_result == 0:
                return True

            elif pattern_matching_result == 1:
                return False


        else: 
            return False


    @staticmethod
    def validate_prefix(pv: LDNode, context: LDContext | None=None) -> bool:
        if LDPropertyValue.validate(pv, context):
            match_value: str | None = LDPropertyValue.try_get_name_as_string(pv, context)
            match_value_1: str | None = LDPropertyValue.try_get_value_as_string(pv, context)
            (pattern_matching_result,) = (None,)
            if match_value is not None:
                if match_value_1 is not None:
                    def _arrow1748(__unit: None=None) -> bool:
                        value: str = match_value_1
                        return match_value == LDPropertyValue.prefix_key()

                    if _arrow1748():
                        pattern_matching_result = 0

                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1

            if pattern_matching_result == 0:
                return True

            elif pattern_matching_result == 1:
                return False


        else: 
            return False


    @staticmethod
    def validate_position(pv: LDNode, context: LDContext | None=None) -> bool:
        if LDPropertyValue.validate(pv, context):
            match_value: str | None = LDPropertyValue.try_get_name_as_string(pv, context)
            match_value_1: str | None = LDPropertyValue.try_get_value_as_string(pv, context)
            (pattern_matching_result,) = (None,)
            if match_value is not None:
                if match_value_1 is not None:
                    def _arrow1749(__unit: None=None) -> bool:
                        value: str = match_value_1
                        return match_value == LDPropertyValue.position_key()

                    if _arrow1749():
                        pattern_matching_result = 0

                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1

            if pattern_matching_result == 0:
                return True

            elif pattern_matching_result == 1:
                return False


        else: 
            return False


    @staticmethod
    def validate_glob(pv: LDNode, context: LDContext | None=None) -> bool:
        if LDPropertyValue.validate(pv, context):
            match_value: str | None = LDPropertyValue.try_get_name_as_string(pv, context)
            match_value_1: str | None = LDPropertyValue.try_get_value_as_string(pv, context)
            (pattern_matching_result,) = (None,)
            if match_value is not None:
                if match_value_1 is not None:
                    def _arrow1750(__unit: None=None) -> bool:
                        value: str = match_value_1
                        return match_value == LDPropertyValue.glob_key()

                    if _arrow1750():
                        pattern_matching_result = 0

                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1

            if pattern_matching_result == 0:
                return True

            elif pattern_matching_result == 1:
                return False


        else: 
            return False


    @staticmethod
    def gen_id(name: str, value: str | None=None, property_id: str | None=None, prefix: str | None=None) -> str:
        prefix_1: str = default_arg(prefix, "PV")
        def _arrow1751(__unit: None=None) -> str:
            pid_1: str = property_id
            return ((("#" + prefix_1) + "_") + name) + ""

        def _arrow1752(__unit: None=None) -> str:
            value_2: str = value
            return ((((("#" + prefix_1) + "_") + name) + "_") + value_2) + ""

        def _arrow1753(__unit: None=None) -> str:
            pid: str = property_id
            value_1: str = value
            return ((((("#" + prefix_1) + "_") + name) + "_") + value_1) + ""

        return clean((_arrow1751() if (property_id is not None) else (((("#" + prefix_1) + "_") + name) + "")) if (value is None) else (_arrow1752() if (property_id is None) else _arrow1753()))

    @staticmethod
    def gen_id_component(name: str, value: str | None=None, property_id: str | None=None) -> str:
        return LDPropertyValue.gen_id(name, value, property_id, "Component")

    @staticmethod
    def gen_id_parameter_value(name: str, value: str | None=None, property_id: str | None=None) -> str:
        return LDPropertyValue.gen_id(name, value, property_id, "ParameterValue")

    @staticmethod
    def gen_id_characteristic_value(name: str, value: str | None=None, property_id: str | None=None) -> str:
        return LDPropertyValue.gen_id(name, value, property_id, "CharacteristicValue")

    @staticmethod
    def gen_id_factor_value(name: str, value: str | None=None, property_id: str | None=None) -> str:
        return LDPropertyValue.gen_id(name, value, property_id, "FactorValue")

    @staticmethod
    def gen_id_fragment_descriptor(file_name: str) -> str:
        return ("#Descriptor_" + file_name) + ""

    @staticmethod
    def gen_id_cwlparameter(name: str, values: Array[str]) -> str:
        def f(v: str) -> str:
            return replace(v, " ", "_")

        return ((("#WorkflowParameter_" + name) + "_") + (join("_", ResizeArray_map(f, values)) if (len(values) > 0) else "")) + ""

    @staticmethod
    def gen_id_prefix(prefix: str) -> str:
        return ("#Prefix_" + prefix) + ""

    @staticmethod
    def gen_id_position(position: int) -> str:
        return ("#Position_" + str(position)) + ""

    @staticmethod
    def gen_id_glob(glob: str) -> str:
        return ("#Glob_" + glob) + ""

    @staticmethod
    def create(name: str, value: str | None=None, id: str | None=None, property_id: str | None=None, unit_code: str | None=None, unit_text: str | None=None, value_reference: str | None=None, context: LDContext | None=None) -> LDNode:
        pv: LDNode = LDNode(LDPropertyValue.gen_id(name, value, property_id) if (id is None) else id, [LDPropertyValue.schema_type()], None, context)
        LDPropertyValue.set_name_as_string(pv, name, context)
        pv.SetOptionalProperty(LDPropertyValue.value(), value, context)
        def action(pid: str) -> None:
            LDPropertyValue.set_property_idas_string(pv, pid, context)

        iterate(action, to_array(property_id))
        def action_1(uc: str) -> None:
            LDPropertyValue.set_unit_code_as_string(pv, uc, context)

        iterate(action_1, to_array(unit_code))
        def action_2(ut: str) -> None:
            LDPropertyValue.set_unit_text_as_string(pv, ut, context)

        iterate(action_2, to_array(unit_text))
        def action_3(vr: str) -> None:
            LDPropertyValue.set_value_reference_as_string(pv, vr, context)

        iterate(action_3, to_array(value_reference))
        return pv

    @staticmethod
    def create_component(name: str, value: str | None=None, id: str | None=None, property_id: str | None=None, unit_code: str | None=None, unit_text: str | None=None, value_reference: str | None=None, context: LDContext | None=None) -> LDNode:
        id_1: str = LDPropertyValue.gen_id_component(name, value, property_id) if (id is None) else id
        c: LDNode = LDPropertyValue.create(name, value, id_1, property_id, unit_code, unit_text, value_reference, context)
        c.AdditionalType = ["Component"]
        return c

    @staticmethod
    def create_parameter_value(name: str, value: str | None=None, id: str | None=None, property_id: str | None=None, unit_code: str | None=None, unit_text: str | None=None, value_reference: str | None=None, context: LDContext | None=None) -> LDNode:
        id_1: str = LDPropertyValue.gen_id_parameter_value(name, value, property_id) if (id is None) else id
        pv: LDNode = LDPropertyValue.create(name, value, id_1, property_id, unit_code, unit_text, value_reference, context)
        pv.AdditionalType = ["ParameterValue"]
        return pv

    @staticmethod
    def create_characteristic_value(name: str, value: str | None=None, id: str | None=None, property_id: str | None=None, unit_code: str | None=None, unit_text: str | None=None, value_reference: str | None=None, context: LDContext | None=None) -> LDNode:
        id_1: str = LDPropertyValue.gen_id_characteristic_value(name, value, property_id) if (id is None) else id
        cv: LDNode = LDPropertyValue.create(name, value, id_1, property_id, unit_code, unit_text, value_reference, context)
        cv.AdditionalType = ["CharacteristicValue"]
        return cv

    @staticmethod
    def create_factor_value(name: str, value: str | None=None, id: str | None=None, property_id: str | None=None, unit_code: str | None=None, unit_text: str | None=None, value_reference: str | None=None, context: LDContext | None=None) -> LDNode:
        id_1: str = LDPropertyValue.gen_id_factor_value(name, value, property_id) if (id is None) else id
        fv: LDNode = LDPropertyValue.create(name, value, id_1, property_id, unit_code, unit_text, value_reference, context)
        fv.AdditionalType = ["FactorValue"]
        return fv

    @staticmethod
    def create_fragment_descriptor(file_name: str, value: str | None=None, id: str | None=None, unit_code: str | None=None, unit_text: str | None=None, value_reference: str | None=None, measurement_method: str | None=None, description: str | None=None, alternate_name: str | None=None, disambiguating_descriptions: Any | None=None, subject_of: Any | None=None, context: LDContext | None=None) -> LDNode:
        id_1: str = LDPropertyValue.gen_id_fragment_descriptor(file_name) if (id is None) else id
        fd: LDNode = LDPropertyValue.create("FragmentDescriptor", value, id_1, "https://github.com/nfdi4plants/ARC-specification/blob/dev/ISA-XLSX.md#datamap-table-sheets", unit_code, unit_text, value_reference, context)
        if measurement_method is not None:
            LDPropertyValue.set_measurement_method_as_string(fd, value_3(measurement_method), context)

        if description is not None:
            LDPropertyValue.set_description_as_string(fd, value_3(description), context)

        if alternate_name is not None:
            LDPropertyValue.set_alternate_name_as_string(fd, value_3(alternate_name), context)

        if disambiguating_descriptions is not None:
            LDPropertyValue.set_disambiguating_descriptions_as_string(fd, value_3(disambiguating_descriptions), context)

        if subject_of is not None:
            LDPropertyValue.set_subject_of(fd, value_3(subject_of), context)

        return fd

    @staticmethod
    def create_cwlparameter(example_of_work: LDNode, name: str, values: Array[str], context: LDContext | None=None) -> LDNode:
        id: str = LDPropertyValue.gen_id_cwlparameter(name, values)
        pv: LDNode = LDPropertyValue.create(name, None, id, None, None, None, None, context)
        if len(values) > 0:
            pv.SetProperty(LDPropertyValue.value(), values, context)

        pv.SetProperty(LDPropertyValue.example_of_work(), example_of_work, context)
        pv.AdditionalType = ["WorkflowInput"]
        return pv

    @staticmethod
    def create_doi(value: str, context: LDContext | None=None) -> LDNode:
        return LDPropertyValue.create(LDPropertyValue.doi_key(), value, value, LDPropertyValue.doi_url(), None, None, None, context)

    @staticmethod
    def create_pub_med_id(value: str, context: LDContext | None=None) -> LDNode:
        return LDPropertyValue.create(LDPropertyValue.pubmed_idkey(), value, value, LDPropertyValue.pubmed_idurl(), None, None, None, context)

    @staticmethod
    def create_prefix(value: str, context: LDContext | None=None) -> LDNode:
        id: str = LDPropertyValue.gen_id_prefix(value)
        return LDPropertyValue.create(LDPropertyValue.prefix_key(), value, id, None, None, None, None, context)

    @staticmethod
    def create_position(value: int, context: LDContext | None=None) -> LDNode:
        id: str = LDPropertyValue.gen_id_position(value)
        return LDPropertyValue.create(LDPropertyValue.position_key(), int32_to_string(value), id, None, None, None, None, context)

    @staticmethod
    def create_glob(value: str, context: LDContext | None=None) -> LDNode:
        id: str = LDPropertyValue.gen_id_glob(value)
        return LDPropertyValue.create(LDPropertyValue.glob_key(), value, id, None, None, None, None, context)

    @staticmethod
    def try_get_as_doi(pv: LDNode, context: LDContext | None=None) -> str | None:
        return LDPropertyValue.get_value_as_string(pv, context) if LDPropertyValue.validate_doi(pv, context) else None

    @staticmethod
    def try_get_as_pub_med_id(pv: LDNode, context: LDContext | None=None) -> str | None:
        return LDPropertyValue.get_value_as_string(pv, context) if LDPropertyValue.validate_pub_med_id(pv, context) else None

    @staticmethod
    def try_get_as_prefix(pv: LDNode, context: LDContext | None=None) -> str | None:
        return LDPropertyValue.get_value_as_string(pv, context) if LDPropertyValue.validate_prefix(pv, context) else None

    @staticmethod
    def try_get_as_position(pv: LDNode, context: LDContext | None=None) -> int | None:
        if LDPropertyValue.validate_position(pv, context):
            match_value: tuple[bool, int]
            out_arg: int = 0
            def _arrow1754(__unit: None=None) -> int:
                return out_arg

            def _arrow1755(v: int) -> None:
                nonlocal out_arg
                out_arg = v or 0

            match_value = (try_parse(LDPropertyValue.get_value_as_string(pv, context), 511, False, 32, FSharpRef(_arrow1754, _arrow1755)), out_arg)
            return match_value[1] if match_value[0] else None

        else: 
            return None


    @staticmethod
    def try_get_as_glob(pv: LDNode, context: LDContext | None=None) -> str | None:
        return LDPropertyValue.get_value_as_string(pv, context) if LDPropertyValue.validate_glob(pv, context) else None


LDPropertyValue_reflection = _expr1756

__all__ = ["LDPropertyValue_reflection"]

