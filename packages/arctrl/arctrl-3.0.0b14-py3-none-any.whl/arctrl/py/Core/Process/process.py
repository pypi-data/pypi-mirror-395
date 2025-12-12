from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from ...fable_modules.fable_library.int32 import parse
from ...fable_modules.fable_library.list import (length, empty, FSharpList, choose, collect, append, try_find, map as map_1, try_pick, zip)
from ...fable_modules.fable_library.option import (default_arg, bind, value as value_4, map)
from ...fable_modules.fable_library.reflection import (TypeInfo, string_type, option_type, list_type, record_type)
from ...fable_modules.fable_library.reg_exp import (get_item, groups)
from ...fable_modules.fable_library.seq2 import List_distinct
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.fable_library.types import (to_string, Record)
from ...fable_modules.fable_library.util import (equals, safe_hash)
from ..comment import (Comment, Comment_reflection)
from ..data import Data
from ..Helper.collections_ import Option_fromValueWithDefault
from ..Helper.regex import ActivePatterns__007CRegex_007C__007C
from ..ontology_annotation import OntologyAnnotation
from .factor import Factor
from .factor_value import FactorValue
from .material import Material
from .material_attribute import MaterialAttribute
from .material_attribute_value import MaterialAttributeValue
from .process_input import (ProcessInput, ProcessInput_reflection, ProcessInput_tryGetCharacteristicValues_5B3D5BA9, ProcessInput_trySource_5B3D5BA9, ProcessInput_tryData_5B3D5BA9, ProcessInput_trySample_5B3D5BA9, ProcessInput_tryMaterial_5B3D5BA9)
from .process_output import (ProcessOutput, ProcessOutput_reflection, ProcessOutput_tryGetCharacteristicValues_Z42C11600, ProcessOutput_tryGetFactorValues_Z42C11600, ProcessOutput_tryData_Z42C11600, ProcessOutput_trySample_Z42C11600, ProcessOutput_tryMaterial_Z42C11600)
from .process_parameter_value import (ProcessParameterValue, ProcessParameterValue_reflection)
from .protocol import (Protocol, Protocol_reflection)
from .protocol_parameter import ProtocolParameter
from .sample import Sample
from .source import Source

def _expr774() -> TypeInfo:
    return record_type("ARCtrl.Process.Process", [], Process, lambda: [("ID", option_type(string_type)), ("Name", option_type(string_type)), ("ExecutesProtocol", option_type(Protocol_reflection())), ("ParameterValues", option_type(list_type(ProcessParameterValue_reflection()))), ("Performer", option_type(string_type)), ("Date", option_type(string_type)), ("PreviousProcess", option_type(Process_reflection())), ("NextProcess", option_type(Process_reflection())), ("Inputs", option_type(list_type(ProcessInput_reflection()))), ("Outputs", option_type(list_type(ProcessOutput_reflection()))), ("Comments", option_type(list_type(Comment_reflection())))])


@dataclass(eq = False, repr = False, slots = True)
class Process(Record):
    ID: str | None
    Name: str | None
    ExecutesProtocol: Protocol | None
    ParameterValues: FSharpList[ProcessParameterValue] | None
    Performer: str | None
    Date: str | None
    PreviousProcess: Process | None
    NextProcess: Process | None
    Inputs: FSharpList[ProcessInput] | None
    Outputs: FSharpList[ProcessOutput] | None
    Comments: FSharpList[Comment] | None
    def Print(self, __unit: None=None) -> str:
        this: Process = self
        return to_string(this)

    def PrintCompact(self, __unit: None=None) -> str:
        this: Process = self
        input_count: int = length(default_arg(this.Inputs, empty())) or 0
        output_count: int = length(default_arg(this.Outputs, empty())) or 0
        param_count: int = length(default_arg(this.ParameterValues, empty())) or 0
        name: str = default_arg(this.Name, "Unnamed Process")
        return to_text(printf("%s [%i Inputs -> %i Params -> %i Outputs]"))(name)(input_count)(param_count)(output_count)


Process_reflection = _expr774

def Process_make(id: str | None=None, name: str | None=None, executes_protocol: Protocol | None=None, parameter_values: FSharpList[ProcessParameterValue] | None=None, performer: str | None=None, date: str | None=None, previous_process: Process | None=None, next_process: Process | None=None, inputs: FSharpList[ProcessInput] | None=None, outputs: FSharpList[ProcessOutput] | None=None, comments: FSharpList[Comment] | None=None) -> Process:
    return Process(id, name, executes_protocol, parameter_values, performer, date, previous_process, next_process, inputs, outputs, comments)


def Process_create_Z7C1F7FA9(Id: str | None=None, Name: str | None=None, ExecutesProtocol: Protocol | None=None, ParameterValues: FSharpList[ProcessParameterValue] | None=None, Performer: str | None=None, Date: str | None=None, PreviousProcess: Process | None=None, NextProcess: Process | None=None, Inputs: FSharpList[ProcessInput] | None=None, Outputs: FSharpList[ProcessOutput] | None=None, Comments: FSharpList[Comment] | None=None) -> Process:
    return Process_make(Id, Name, ExecutesProtocol, ParameterValues, Performer, Date, PreviousProcess, NextProcess, Inputs, Outputs, Comments)


def Process_get_empty(__unit: None=None) -> Process:
    return Process_create_Z7C1F7FA9()


def Process_composeName(process_name_root: str, i: int) -> str:
    return ((("" + process_name_root) + "_") + str(i)) + ""


def Process_decomposeName_Z721C83C5(name: str) -> tuple[str, int | None]:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("(?<name>.+)_(?<num>\\d+)", name)
    if active_pattern_result is not None:
        r: Any = active_pattern_result
        return (get_item(groups(r), "name") or "", parse(get_item(groups(r), "num") or "", 511, False, 32))

    else: 
        return (name, None)



def Process_tryGetProtocolName_763471FF(p: Process) -> str | None:
    def binder(p_1: Protocol, p: Any=p) -> str | None:
        return p_1.Name

    return bind(binder, p.ExecutesProtocol)


def Process_getProtocolName_763471FF(p: Process) -> str:
    def binder(p_1: Protocol, p: Any=p) -> str | None:
        return p_1.Name

    return value_4(bind(binder, p.ExecutesProtocol))


def Process_getParameterValues_763471FF(p: Process) -> FSharpList[ProcessParameterValue]:
    return default_arg(p.ParameterValues, empty())


def Process_getParameters_763471FF(p: Process) -> FSharpList[ProtocolParameter]:
    def chooser(pv: ProcessParameterValue, p: Any=p) -> ProtocolParameter | None:
        return pv.Category

    return choose(chooser, Process_getParameterValues_763471FF(p))


def Process_getInputCharacteristicValues_763471FF(p: Process) -> FSharpList[MaterialAttributeValue]:
    match_value: FSharpList[ProcessInput] | None = p.Inputs
    if match_value is None:
        return empty()

    else: 
        def mapping(inp: ProcessInput, p: Any=p) -> FSharpList[MaterialAttributeValue]:
            return default_arg(ProcessInput_tryGetCharacteristicValues_5B3D5BA9(inp), empty())

        class ObjectExpr775:
            @property
            def Equals(self) -> Callable[[MaterialAttributeValue, MaterialAttributeValue], bool]:
                return equals

            @property
            def GetHashCode(self) -> Callable[[MaterialAttributeValue], int]:
                return safe_hash

        return List_distinct(collect(mapping, match_value), ObjectExpr775())



def Process_getOutputCharacteristicValues_763471FF(p: Process) -> FSharpList[MaterialAttributeValue]:
    match_value: FSharpList[ProcessOutput] | None = p.Outputs
    if match_value is None:
        return empty()

    else: 
        def mapping(out: ProcessOutput, p: Any=p) -> FSharpList[MaterialAttributeValue]:
            return default_arg(ProcessOutput_tryGetCharacteristicValues_Z42C11600(out), empty())

        class ObjectExpr776:
            @property
            def Equals(self) -> Callable[[MaterialAttributeValue, MaterialAttributeValue], bool]:
                return equals

            @property
            def GetHashCode(self) -> Callable[[MaterialAttributeValue], int]:
                return safe_hash

        return List_distinct(collect(mapping, match_value), ObjectExpr776())



def Process_getCharacteristicValues_763471FF(p: Process) -> FSharpList[MaterialAttributeValue]:
    class ObjectExpr777:
        @property
        def Equals(self) -> Callable[[MaterialAttributeValue, MaterialAttributeValue], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[MaterialAttributeValue], int]:
            return safe_hash

    return List_distinct(append(Process_getInputCharacteristicValues_763471FF(p), Process_getOutputCharacteristicValues_763471FF(p)), ObjectExpr777())


def Process_getCharacteristics_763471FF(p: Process) -> FSharpList[MaterialAttribute]:
    def chooser(cv: MaterialAttributeValue, p: Any=p) -> MaterialAttribute | None:
        return cv.Category

    class ObjectExpr778:
        @property
        def Equals(self) -> Callable[[MaterialAttribute, MaterialAttribute], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[MaterialAttribute], int]:
            return safe_hash

    return List_distinct(choose(chooser, Process_getCharacteristicValues_763471FF(p)), ObjectExpr778())


def Process_getFactorValues_763471FF(p: Process) -> FSharpList[FactorValue]:
    def mapping(arg: ProcessOutput, p: Any=p) -> FSharpList[FactorValue]:
        return default_arg(ProcessOutput_tryGetFactorValues_Z42C11600(arg), empty())

    class ObjectExpr779:
        @property
        def Equals(self) -> Callable[[FactorValue, FactorValue], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[FactorValue], int]:
            return safe_hash

    return List_distinct(collect(mapping, default_arg(p.Outputs, empty())), ObjectExpr779())


def Process_getFactors_763471FF(p: Process) -> FSharpList[Factor]:
    def chooser(fv: FactorValue, p: Any=p) -> Factor | None:
        return fv.Category

    class ObjectExpr780:
        @property
        def Equals(self) -> Callable[[Factor, Factor], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[Factor], int]:
            return safe_hash

    return List_distinct(choose(chooser, Process_getFactorValues_763471FF(p)), ObjectExpr780())


def Process_getUnits_763471FF(p: Process) -> FSharpList[OntologyAnnotation]:
    def chooser(cv: MaterialAttributeValue, p: Any=p) -> OntologyAnnotation | None:
        return cv.Unit

    def chooser_1(pv: ProcessParameterValue, p: Any=p) -> OntologyAnnotation | None:
        return pv.Unit

    def chooser_2(fv: FactorValue, p: Any=p) -> OntologyAnnotation | None:
        return fv.Unit

    return append(choose(chooser, Process_getCharacteristicValues_763471FF(p)), append(choose(chooser_1, Process_getParameterValues_763471FF(p)), choose(chooser_2, Process_getFactorValues_763471FF(p))))


def Process_tryGetInputsWithParameterBy(predicate: Callable[[ProtocolParameter], bool], p: Process) -> FSharpList[tuple[ProcessInput, ProcessParameterValue]] | None:
    match_value: FSharpList[ProcessParameterValue] | None = p.ParameterValues
    if match_value is None:
        return None

    else: 
        def predicate_1(pv: ProcessParameterValue, predicate: Any=predicate, p: Any=p) -> bool:
            return predicate(default_arg(pv.Category, ProtocolParameter.empty()))

        match_value_1: ProcessParameterValue | None = try_find(predicate_1, match_value)
        if match_value_1 is None:
            return None

        else: 
            param_value: ProcessParameterValue = match_value_1
            def mapping_1(list_2: FSharpList[ProcessInput], predicate: Any=predicate, p: Any=p) -> FSharpList[tuple[ProcessInput, ProcessParameterValue]]:
                def mapping(i: ProcessInput, list_2: Any=list_2) -> tuple[ProcessInput, ProcessParameterValue]:
                    return (i, param_value)

                return map_1(mapping, list_2)

            return map(mapping_1, p.Inputs)




def Process_tryGetOutputsWithParameterBy(predicate: Callable[[ProtocolParameter], bool], p: Process) -> FSharpList[tuple[ProcessOutput, ProcessParameterValue]] | None:
    match_value: FSharpList[ProcessParameterValue] | None = p.ParameterValues
    if match_value is None:
        return None

    else: 
        def predicate_1(pv: ProcessParameterValue, predicate: Any=predicate, p: Any=p) -> bool:
            return predicate(default_arg(pv.Category, ProtocolParameter.empty()))

        match_value_1: ProcessParameterValue | None = try_find(predicate_1, match_value)
        if match_value_1 is None:
            return None

        else: 
            param_value: ProcessParameterValue = match_value_1
            def mapping_1(list_2: FSharpList[ProcessOutput], predicate: Any=predicate, p: Any=p) -> FSharpList[tuple[ProcessOutput, ProcessParameterValue]]:
                def mapping(i: ProcessOutput, list_2: Any=list_2) -> tuple[ProcessOutput, ProcessParameterValue]:
                    return (i, param_value)

                return map_1(mapping, list_2)

            return map(mapping_1, p.Outputs)




def Process_tryGetInputsWithCharacteristicBy(predicate: Callable[[MaterialAttribute], bool], p: Process) -> FSharpList[tuple[ProcessInput, MaterialAttributeValue]] | None:
    match_value: FSharpList[ProcessInput] | None = p.Inputs
    if match_value is None:
        return None

    else: 
        def chooser_1(i: ProcessInput, predicate: Any=predicate, p: Any=p) -> tuple[ProcessInput, MaterialAttributeValue] | None:
            def chooser(mv: MaterialAttributeValue, i: Any=i) -> tuple[ProcessInput, MaterialAttributeValue] | None:
                match_value_1: MaterialAttribute | None = mv.Category
                (pattern_matching_result,) = (None,)
                if match_value_1 is not None:
                    if predicate(match_value_1):
                        pattern_matching_result = 0

                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1

                if pattern_matching_result == 0:
                    return (i, mv)

                elif pattern_matching_result == 1:
                    return None


            return try_pick(chooser, default_arg(ProcessInput_tryGetCharacteristicValues_5B3D5BA9(i), empty()))

        return Option_fromValueWithDefault(empty(), choose(chooser_1, match_value))



def Process_tryGetOutputsWithCharacteristicBy(predicate: Callable[[MaterialAttribute], bool], p: Process) -> FSharpList[tuple[ProcessOutput, MaterialAttributeValue]] | None:
    match_value: FSharpList[ProcessInput] | None = p.Inputs
    match_value_1: FSharpList[ProcessOutput] | None = p.Outputs
    (pattern_matching_result, is_, os) = (None, None, None)
    if match_value is not None:
        if match_value_1 is not None:
            pattern_matching_result = 0
            is_ = match_value
            os = match_value_1

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def chooser_1(tupled_arg: tuple[ProcessInput, ProcessOutput], predicate: Any=predicate, p: Any=p) -> tuple[ProcessOutput, MaterialAttributeValue] | None:
            def chooser(mv: MaterialAttributeValue, tupled_arg: Any=tupled_arg) -> tuple[ProcessOutput, MaterialAttributeValue] | None:
                match_value_1: MaterialAttribute | None = mv.Category
                (pattern_matching_result_1,) = (None,)
                if match_value_1 is not None:
                    if predicate(match_value_1):
                        pattern_matching_result_1 = 0

                    else: 
                        pattern_matching_result_1 = 1


                else: 
                    pattern_matching_result_1 = 1

                if pattern_matching_result_1 == 0:
                    return (tupled_arg[1], mv)

                elif pattern_matching_result_1 == 1:
                    return None


            return try_pick(chooser, default_arg(ProcessInput_tryGetCharacteristicValues_5B3D5BA9(tupled_arg[0]), empty()))

        return Option_fromValueWithDefault(empty(), choose(chooser_1, zip(is_, os)))

    elif pattern_matching_result == 1:
        return None



def Process_tryGetOutputsWithFactorBy(predicate: Callable[[Factor], bool], p: Process) -> FSharpList[tuple[ProcessOutput, FactorValue]] | None:
    match_value: FSharpList[ProcessOutput] | None = p.Outputs
    if match_value is None:
        return None

    else: 
        def chooser_1(o: ProcessOutput, predicate: Any=predicate, p: Any=p) -> tuple[ProcessOutput, FactorValue] | None:
            def chooser(mv: FactorValue, o: Any=o) -> tuple[ProcessOutput, FactorValue] | None:
                match_value_1: Factor | None = mv.Category
                (pattern_matching_result,) = (None,)
                if match_value_1 is not None:
                    if predicate(match_value_1):
                        pattern_matching_result = 0

                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1

                if pattern_matching_result == 0:
                    return (o, mv)

                elif pattern_matching_result == 1:
                    return None


            return try_pick(chooser, default_arg(ProcessOutput_tryGetFactorValues_Z42C11600(o), empty()))

        return Option_fromValueWithDefault(empty(), choose(chooser_1, match_value))



def Process_getSources_763471FF(p: Process) -> FSharpList[Source]:
    def chooser(pi: ProcessInput, p: Any=p) -> Source | None:
        return ProcessInput_trySource_5B3D5BA9(pi)

    class ObjectExpr781:
        @property
        def Equals(self) -> Callable[[Source, Source], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[Source], int]:
            return safe_hash

    return List_distinct(choose(chooser, default_arg(p.Inputs, empty())), ObjectExpr781())


def Process_getData_763471FF(p: Process) -> FSharpList[Data]:
    def chooser(pi: ProcessInput, p: Any=p) -> Data | None:
        return ProcessInput_tryData_5B3D5BA9(pi)

    def chooser_1(po: ProcessOutput, p: Any=p) -> Data | None:
        return ProcessOutput_tryData_Z42C11600(po)

    class ObjectExpr782:
        @property
        def Equals(self) -> Callable[[Data, Data], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[Data], int]:
            return safe_hash

    return List_distinct(append(choose(chooser, default_arg(p.Inputs, empty())), choose(chooser_1, default_arg(p.Outputs, empty()))), ObjectExpr782())


def Process_getSamples_763471FF(p: Process) -> FSharpList[Sample]:
    def chooser(pi: ProcessInput, p: Any=p) -> Sample | None:
        return ProcessInput_trySample_5B3D5BA9(pi)

    def chooser_1(po: ProcessOutput, p: Any=p) -> Sample | None:
        return ProcessOutput_trySample_Z42C11600(po)

    class ObjectExpr783:
        @property
        def Equals(self) -> Callable[[Sample, Sample], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[Sample], int]:
            return safe_hash

    return List_distinct(append(choose(chooser, default_arg(p.Inputs, empty())), choose(chooser_1, default_arg(p.Outputs, empty()))), ObjectExpr783())


def Process_getMaterials_763471FF(p: Process) -> FSharpList[Material]:
    def chooser(pi: ProcessInput, p: Any=p) -> Material | None:
        return ProcessInput_tryMaterial_5B3D5BA9(pi)

    def chooser_1(po: ProcessOutput, p: Any=p) -> Material | None:
        return ProcessOutput_tryMaterial_Z42C11600(po)

    class ObjectExpr784:
        @property
        def Equals(self) -> Callable[[Material, Material], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[Material], int]:
            return safe_hash

    return List_distinct(append(choose(chooser, default_arg(p.Inputs, empty())), choose(chooser_1, default_arg(p.Outputs, empty()))), ObjectExpr784())


__all__ = ["Process_reflection", "Process_make", "Process_create_Z7C1F7FA9", "Process_get_empty", "Process_composeName", "Process_decomposeName_Z721C83C5", "Process_tryGetProtocolName_763471FF", "Process_getProtocolName_763471FF", "Process_getParameterValues_763471FF", "Process_getParameters_763471FF", "Process_getInputCharacteristicValues_763471FF", "Process_getOutputCharacteristicValues_763471FF", "Process_getCharacteristicValues_763471FF", "Process_getCharacteristics_763471FF", "Process_getFactorValues_763471FF", "Process_getFactors_763471FF", "Process_getUnits_763471FF", "Process_tryGetInputsWithParameterBy", "Process_tryGetOutputsWithParameterBy", "Process_tryGetInputsWithCharacteristicBy", "Process_tryGetOutputsWithCharacteristicBy", "Process_tryGetOutputsWithFactorBy", "Process_getSources_763471FF", "Process_getData_763471FF", "Process_getSamples_763471FF", "Process_getMaterials_763471FF"]

