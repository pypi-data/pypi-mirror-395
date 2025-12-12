from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.double import try_parse as try_parse_1
from ..fable_modules.fable_library.int32 import try_parse
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.reflection import (TypeInfo, int32_type, float64_type, string_type, union_type)
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.fable_library.types import (FSharpRef, to_string, Array, Union)
from ..fable_modules.fable_library.util import int32_to_string
from .ontology_annotation import (OntologyAnnotation, OntologyAnnotation_reflection)

def _expr708() -> TypeInfo:
    return union_type("ARCtrl.Value", [], Value, lambda: [[("Item", OntologyAnnotation_reflection())], [("Item", int32_type)], [("Item", float64_type)], [("Item", string_type)]])


class Value(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Ontology", "Int", "Float", "Name"]

    @staticmethod
    def from_string(value: str) -> Value:
        match_value: tuple[bool, int]
        out_arg: int = 0
        def _arrow703(__unit: None=None) -> int:
            return out_arg

        def _arrow704(v: int) -> None:
            nonlocal out_arg
            out_arg = v or 0

        match_value = (try_parse(value, 511, False, 32, FSharpRef(_arrow703, _arrow704)), out_arg)
        if match_value[0]:
            return Value(1, match_value[1])

        else: 
            match_value_1: tuple[bool, float]
            out_arg_1: float = 0.0
            def _arrow705(__unit: None=None) -> float:
                return out_arg_1

            def _arrow706(v_2: float) -> None:
                nonlocal out_arg_1
                out_arg_1 = v_2

            match_value_1 = (try_parse_1(value, FSharpRef(_arrow705, _arrow706)), out_arg_1)
            return Value(2, match_value_1[1]) if match_value_1[0] else Value(3, value)


    @staticmethod
    def from_options(value: str | None=None, term_source: str | None=None, term_accesssion: str | None=None) -> Value | None:
        def _arrow707(__unit: None=None) -> Value | None:
            value_1: str = value
            return Value.from_string(value_1)

        return ((None if (term_accesssion is None) else Value(0, OntologyAnnotation.create(default_arg(value, ""), term_source, term_accesssion))) if (term_source is None) else Value(0, OntologyAnnotation.create(default_arg(value, ""), term_source, term_accesssion))) if (value is None) else ((_arrow707() if (term_accesssion is None) else Value(0, OntologyAnnotation.create(default_arg(value, ""), term_source, term_accesssion))) if (term_source is None) else Value(0, OntologyAnnotation.create(default_arg(value, ""), term_source, term_accesssion)))

    @staticmethod
    def to_options(value: Value) -> tuple[str | None, str | None, str | None]:
        if value.tag == 1:
            return (int32_to_string(value.fields[0]), None, None)

        elif value.tag == 2:
            return (to_string(value.fields[0]), None, None)

        elif value.tag == 3:
            return (value.fields[0], None, None)

        else: 
            oa: OntologyAnnotation = value.fields[0]
            return (oa.Name, oa.TermAccessionNumber, oa.TermSourceREF)


    @property
    def Text(self, __unit: None=None) -> str:
        this: Value = self
        if this.tag == 2:
            return to_string(this.fields[0])

        elif this.tag == 1:
            return int32_to_string(this.fields[0])

        elif this.tag == 3:
            return this.fields[0]

        else: 
            return this.fields[0].NameText


    def AsName(self, __unit: None=None) -> str:
        this: Value = self
        if this.tag == 3:
            return this.fields[0]

        else: 
            raise Exception(("Value " + str(this)) + " is not of case name")


    def AsInt(self, __unit: None=None) -> int:
        this: Value = self
        if this.tag == 1:
            return this.fields[0]

        else: 
            raise Exception(("Value " + str(this)) + " is not of case int")


    def AsFloat(self, __unit: None=None) -> float:
        this: Value = self
        if this.tag == 2:
            return this.fields[0]

        else: 
            raise Exception(("Value " + str(this)) + " is not of case float")


    def AsOntology(self, __unit: None=None) -> OntologyAnnotation:
        this: Value = self
        if this.tag == 0:
            return this.fields[0]

        else: 
            raise Exception(("Value " + str(this)) + " is not of case ontology")


    @property
    def IsAnOntology(self, __unit: None=None) -> bool:
        this: Value = self
        return True if (this.tag == 0) else False

    @property
    def IsNumerical(self, __unit: None=None) -> bool:
        this: Value = self
        if (this.tag == 1) or (this.tag == 2):
            return True

        else: 
            return False


    @property
    def IsAnInt(self, __unit: None=None) -> bool:
        this: Value = self
        return True if (this.tag == 1) else False

    @property
    def IsAFloat(self, __unit: None=None) -> bool:
        this: Value = self
        return True if (this.tag == 2) else False

    @property
    def IsAText(self, __unit: None=None) -> bool:
        this: Value = self
        return True if (this.tag == 3) else False

    @staticmethod
    def get_text(v: Value) -> str:
        return v.Text

    def Print(self, __unit: None=None) -> str:
        this: Value = self
        return to_string(this)

    def PrintCompact(self, __unit: None=None) -> str:
        this: Value = self
        if this.tag == 1:
            return to_text(printf("%i"))(this.fields[0])

        elif this.tag == 2:
            return to_text(printf("%f"))(this.fields[0])

        elif this.tag == 3:
            return this.fields[0]

        else: 
            return this.fields[0].NameText



Value_reflection = _expr708

__all__ = ["Value_reflection"]

