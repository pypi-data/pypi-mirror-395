from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (choose, FSharpList, filter, concat, collect, empty, map, zip, singleton)
from ...fable_modules.fable_library.map import (of_list as of_list_1, FSharpMap__TryFind)
from ...fable_modules.fable_library.option import (bind, default_arg, value as value_4)
from ...fable_modules.fable_library.seq2 import (List_distinct, List_groupBy)
from ...fable_modules.fable_library.set import (of_list, FSharpSet__Contains)
from ...fable_modules.fable_library.util import (string_hash, equals, safe_hash, compare_primitives, equal_arrays, array_hash)
from ..data import Data
from ..ontology_annotation import OntologyAnnotation
from .factor import Factor
from .factor_value import FactorValue
from .material import Material
from .material_attribute import MaterialAttribute
from .material_attribute_value import MaterialAttributeValue
from .process import (Process, Process_tryGetInputsWithParameterBy, Process_tryGetOutputsWithParameterBy, Process_getParameters_763471FF, Process_getCharacteristics_763471FF, Process_tryGetInputsWithCharacteristicBy, Process_tryGetOutputsWithCharacteristicBy, Process_tryGetOutputsWithFactorBy, Process_getFactors_763471FF, Process_getUnits_763471FF, Process_getData_763471FF, Process_getSources_763471FF, Process_getSamples_763471FF, Process_getMaterials_763471FF)
from .process_input import (ProcessInput, ProcessInput_getName_5B3D5BA9, ProcessInput__get_Name)
from .process_output import (ProcessOutput, ProcessOutput_getName_Z42C11600, ProcessOutput__get_Name)
from .process_parameter_value import ProcessParameterValue
from .protocol import Protocol
from .protocol_parameter import ProtocolParameter
from .sample import Sample
from .source import Source

def get_protocol_names(process_sequence: FSharpList[Process]) -> FSharpList[str]:
    def chooser(p: Process, process_sequence: Any=process_sequence) -> str | None:
        def binder(protocol: Protocol, p: Any=p) -> str | None:
            return protocol.Name

        return bind(binder, p.ExecutesProtocol)

    class ObjectExpr786:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow785(x: str, y: str) -> bool:
                return x == y

            return _arrow785

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return List_distinct(choose(chooser, process_sequence), ObjectExpr786())


def get_protocols(process_sequence: FSharpList[Process]) -> FSharpList[Protocol]:
    def chooser(p: Process, process_sequence: Any=process_sequence) -> Protocol | None:
        return p.ExecutesProtocol

    class ObjectExpr787:
        @property
        def Equals(self) -> Callable[[Protocol, Protocol], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[Protocol], int]:
            return safe_hash

    return List_distinct(choose(chooser, process_sequence), ObjectExpr787())


def filter_by_protocol_by(predicate: Callable[[Protocol], bool], process_sequence: FSharpList[Process]) -> FSharpList[Process]:
    def predicate_1(p: Process, predicate: Any=predicate, process_sequence: Any=process_sequence) -> bool:
        match_value: Protocol | None = p.ExecutesProtocol
        (pattern_matching_result,) = (None,)
        if match_value is not None:
            if predicate(match_value):
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return True

        elif pattern_matching_result == 1:
            return False


    return filter(predicate_1, process_sequence)


def filter_by_protocol_name(protocol_name: str, process_sequence: FSharpList[Process]) -> FSharpList[Process]:
    def _arrow788(p: Protocol, protocol_name: Any=protocol_name, process_sequence: Any=process_sequence) -> bool:
        return equals(p.Name, protocol_name)

    return filter_by_protocol_by(_arrow788, process_sequence)


def get_inputs_with_parameter_by(predicate: Callable[[ProtocolParameter], bool], process_sequence: FSharpList[Process]) -> FSharpList[tuple[ProcessInput, ProcessParameterValue]]:
    def chooser(p: Process, predicate: Any=predicate, process_sequence: Any=process_sequence) -> FSharpList[tuple[ProcessInput, ProcessParameterValue]] | None:
        return Process_tryGetInputsWithParameterBy(predicate, p)

    return concat(choose(chooser, process_sequence))


def get_outputs_with_parameter_by(predicate: Callable[[ProtocolParameter], bool], process_sequence: FSharpList[Process]) -> FSharpList[tuple[ProcessOutput, ProcessParameterValue]]:
    def chooser(p: Process, predicate: Any=predicate, process_sequence: Any=process_sequence) -> FSharpList[tuple[ProcessOutput, ProcessParameterValue]] | None:
        return Process_tryGetOutputsWithParameterBy(predicate, p)

    return concat(choose(chooser, process_sequence))


def get_parameters(process_sequence: FSharpList[Process]) -> FSharpList[ProtocolParameter]:
    def mapping(p: Process, process_sequence: Any=process_sequence) -> FSharpList[ProtocolParameter]:
        return Process_getParameters_763471FF(p)

    class ObjectExpr789:
        @property
        def Equals(self) -> Callable[[ProtocolParameter, ProtocolParameter], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[ProtocolParameter], int]:
            return safe_hash

    return List_distinct(collect(mapping, process_sequence), ObjectExpr789())


def get_characteristics(process_sequence: FSharpList[Process]) -> FSharpList[MaterialAttribute]:
    def mapping(p: Process, process_sequence: Any=process_sequence) -> FSharpList[MaterialAttribute]:
        return Process_getCharacteristics_763471FF(p)

    class ObjectExpr790:
        @property
        def Equals(self) -> Callable[[MaterialAttribute, MaterialAttribute], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[MaterialAttribute], int]:
            return safe_hash

    return List_distinct(collect(mapping, process_sequence), ObjectExpr790())


def get_inputs_with_characteristic_by(predicate: Callable[[MaterialAttribute], bool], process_sequence: FSharpList[Process]) -> FSharpList[tuple[ProcessInput, MaterialAttributeValue]]:
    def chooser(p: Process, predicate: Any=predicate, process_sequence: Any=process_sequence) -> FSharpList[tuple[ProcessInput, MaterialAttributeValue]] | None:
        return Process_tryGetInputsWithCharacteristicBy(predicate, p)

    return concat(choose(chooser, process_sequence))


def get_outputs_with_characteristic_by(predicate: Callable[[MaterialAttribute], bool], process_sequence: FSharpList[Process]) -> FSharpList[tuple[ProcessOutput, MaterialAttributeValue]]:
    def chooser(p: Process, predicate: Any=predicate, process_sequence: Any=process_sequence) -> FSharpList[tuple[ProcessOutput, MaterialAttributeValue]] | None:
        return Process_tryGetOutputsWithCharacteristicBy(predicate, p)

    return concat(choose(chooser, process_sequence))


def get_outputs_with_factor_by(predicate: Callable[[Factor], bool], process_sequence: FSharpList[Process]) -> FSharpList[tuple[ProcessOutput, FactorValue]]:
    def chooser(p: Process, predicate: Any=predicate, process_sequence: Any=process_sequence) -> FSharpList[tuple[ProcessOutput, FactorValue]] | None:
        return Process_tryGetOutputsWithFactorBy(predicate, p)

    return concat(choose(chooser, process_sequence))


def get_factors(process_sequence: FSharpList[Process]) -> FSharpList[Factor]:
    def mapping(p: Process, process_sequence: Any=process_sequence) -> FSharpList[Factor]:
        return Process_getFactors_763471FF(p)

    class ObjectExpr791:
        @property
        def Equals(self) -> Callable[[Factor, Factor], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[Factor], int]:
            return safe_hash

    return List_distinct(collect(mapping, process_sequence), ObjectExpr791())


def get_root_inputs(process_sequence: FSharpList[Process]) -> FSharpList[ProcessInput]:
    def mapping(p: Process, process_sequence: Any=process_sequence) -> FSharpList[ProcessInput]:
        return default_arg(p.Inputs, empty())

    inputs: FSharpList[ProcessInput] = collect(mapping, process_sequence)
    def mapping_2(p_1: Process, process_sequence: Any=process_sequence) -> FSharpList[str]:
        def mapping_1(po: ProcessOutput, p_1: Any=p_1) -> str:
            return ProcessOutput_getName_Z42C11600(po)

        return map(mapping_1, default_arg(p_1.Outputs, empty()))

    class ObjectExpr792:
        @property
        def Compare(self) -> Callable[[str, str], int]:
            return compare_primitives

    outputs: Any = of_list(collect(mapping_2, process_sequence), ObjectExpr792())
    def predicate(i: ProcessInput, process_sequence: Any=process_sequence) -> bool:
        return not FSharpSet__Contains(outputs, ProcessInput_getName_5B3D5BA9(i))

    return filter(predicate, inputs)


def get_final_outputs(process_sequence: FSharpList[Process]) -> FSharpList[ProcessOutput]:
    def mapping_1(p: Process, process_sequence: Any=process_sequence) -> FSharpList[str]:
        def mapping(pi: ProcessInput, p: Any=p) -> str:
            return ProcessInput_getName_5B3D5BA9(pi)

        return map(mapping, default_arg(p.Inputs, empty()))

    class ObjectExpr793:
        @property
        def Compare(self) -> Callable[[str, str], int]:
            return compare_primitives

    inputs: Any = of_list(collect(mapping_1, process_sequence), ObjectExpr793())
    def predicate(o: ProcessOutput, process_sequence: Any=process_sequence) -> bool:
        return not FSharpSet__Contains(inputs, ProcessOutput_getName_Z42C11600(o))

    def mapping_2(p_1: Process, process_sequence: Any=process_sequence) -> FSharpList[ProcessOutput]:
        return default_arg(p_1.Outputs, empty())

    return filter(predicate, collect(mapping_2, process_sequence))


def get_root_input_of(process_sequence: FSharpList[Process], sample: str) -> FSharpList[str]:
    def mapping_4(tupled_arg: tuple[str, FSharpList[tuple[str, str]]], process_sequence: Any=process_sequence, sample: Any=sample) -> tuple[str, FSharpList[str]]:
        def mapping_3(tuple_1: tuple[str, str], tupled_arg: Any=tupled_arg) -> str:
            return tuple_1[1]

        return (tupled_arg[0], map(mapping_3, tupled_arg[1]))

    def projection(tuple: tuple[str, str], process_sequence: Any=process_sequence, sample: Any=sample) -> str:
        return tuple[0]

    def mapping_2(p: Process, process_sequence: Any=process_sequence, sample: Any=sample) -> FSharpList[tuple[str, str]]:
        def mapping(o: ProcessOutput, p: Any=p) -> str:
            return ProcessOutput__get_Name(o)

        def mapping_1(i: ProcessInput, p: Any=p) -> str:
            return ProcessInput__get_Name(i)

        class ObjectExpr794:
            @property
            def Equals(self) -> Callable[[tuple[str, str], tuple[str, str]], bool]:
                return equal_arrays

            @property
            def GetHashCode(self) -> Callable[[tuple[str, str]], int]:
                return array_hash

        return List_distinct(zip(map(mapping, value_4(p.Outputs)), map(mapping_1, value_4(p.Inputs))), ObjectExpr794())

    class ObjectExpr796:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow795(x_1: str, y_1: str) -> bool:
                return x_1 == y_1

            return _arrow795

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    class ObjectExpr797:
        @property
        def Compare(self) -> Callable[[str, str], int]:
            return compare_primitives

    mappings: Any = of_list_1(map(mapping_4, List_groupBy(projection, collect(mapping_2, process_sequence), ObjectExpr796())), ObjectExpr797())
    def loop(last_state_mut: FSharpList[str], state_mut: FSharpList[str], process_sequence: Any=process_sequence, sample: Any=sample) -> FSharpList[str]:
        while True:
            (last_state, state) = (last_state_mut, state_mut)
            if equals(last_state, state):
                return state

            else: 
                last_state_mut = state
                def mapping_5(s: str, last_state: Any=last_state, state: Any=state) -> FSharpList[str]:
                    return default_arg(FSharpMap__TryFind(mappings, s), singleton(s))

                state_mut = collect(mapping_5, state)
                continue

            break

    return loop(empty(), singleton(sample))


def get_final_outputs_of(process_sequence: FSharpList[Process], sample: str) -> FSharpList[str]:
    def mapping_4(tupled_arg: tuple[str, FSharpList[tuple[str, str]]], process_sequence: Any=process_sequence, sample: Any=sample) -> tuple[str, FSharpList[str]]:
        def mapping_3(tuple_1: tuple[str, str], tupled_arg: Any=tupled_arg) -> str:
            return tuple_1[1]

        return (tupled_arg[0], map(mapping_3, tupled_arg[1]))

    def projection(tuple: tuple[str, str], process_sequence: Any=process_sequence, sample: Any=sample) -> str:
        return tuple[0]

    def mapping_2(p: Process, process_sequence: Any=process_sequence, sample: Any=sample) -> FSharpList[tuple[str, str]]:
        def mapping(i: ProcessInput, p: Any=p) -> str:
            return ProcessInput__get_Name(i)

        def mapping_1(o: ProcessOutput, p: Any=p) -> str:
            return ProcessOutput__get_Name(o)

        class ObjectExpr798:
            @property
            def Equals(self) -> Callable[[tuple[str, str], tuple[str, str]], bool]:
                return equal_arrays

            @property
            def GetHashCode(self) -> Callable[[tuple[str, str]], int]:
                return array_hash

        return List_distinct(zip(map(mapping, value_4(p.Inputs)), map(mapping_1, value_4(p.Outputs))), ObjectExpr798())

    class ObjectExpr800:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow799(x_1: str, y_1: str) -> bool:
                return x_1 == y_1

            return _arrow799

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    class ObjectExpr801:
        @property
        def Compare(self) -> Callable[[str, str], int]:
            return compare_primitives

    mappings: Any = of_list_1(map(mapping_4, List_groupBy(projection, collect(mapping_2, process_sequence), ObjectExpr800())), ObjectExpr801())
    def loop(last_state_mut: FSharpList[str], state_mut: FSharpList[str], process_sequence: Any=process_sequence, sample: Any=sample) -> FSharpList[str]:
        while True:
            (last_state, state) = (last_state_mut, state_mut)
            if equals(last_state, state):
                return state

            else: 
                last_state_mut = state
                def mapping_5(s: str, last_state: Any=last_state, state: Any=state) -> FSharpList[str]:
                    return default_arg(FSharpMap__TryFind(mappings, s), singleton(s))

                state_mut = collect(mapping_5, state)
                continue

            break

    return loop(empty(), singleton(sample))


def get_units(process_sequence: FSharpList[Process]) -> FSharpList[OntologyAnnotation]:
    def _arrow802(p: Process, process_sequence: Any=process_sequence) -> FSharpList[OntologyAnnotation]:
        return Process_getUnits_763471FF(p)

    class ObjectExpr803:
        @property
        def Equals(self) -> Callable[[OntologyAnnotation, OntologyAnnotation], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[OntologyAnnotation], int]:
            return safe_hash

    return List_distinct(collect(_arrow802, process_sequence), ObjectExpr803())


def get_data(process_sequence: FSharpList[Process]) -> FSharpList[Data]:
    def mapping(p: Process, process_sequence: Any=process_sequence) -> FSharpList[Data]:
        return Process_getData_763471FF(p)

    class ObjectExpr804:
        @property
        def Equals(self) -> Callable[[Data, Data], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[Data], int]:
            return safe_hash

    return List_distinct(collect(mapping, process_sequence), ObjectExpr804())


def get_sources(process_sequence: FSharpList[Process]) -> FSharpList[Source]:
    def mapping(p: Process, process_sequence: Any=process_sequence) -> FSharpList[Source]:
        return Process_getSources_763471FF(p)

    class ObjectExpr805:
        @property
        def Equals(self) -> Callable[[Source, Source], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[Source], int]:
            return safe_hash

    return List_distinct(collect(mapping, process_sequence), ObjectExpr805())


def get_samples(process_sequence: FSharpList[Process]) -> FSharpList[Sample]:
    def mapping(p: Process, process_sequence: Any=process_sequence) -> FSharpList[Sample]:
        return Process_getSamples_763471FF(p)

    class ObjectExpr806:
        @property
        def Equals(self) -> Callable[[Sample, Sample], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[Sample], int]:
            return safe_hash

    return List_distinct(collect(mapping, process_sequence), ObjectExpr806())


def get_materials(process_sequence: FSharpList[Process]) -> FSharpList[Material]:
    def mapping(p: Process, process_sequence: Any=process_sequence) -> FSharpList[Material]:
        return Process_getMaterials_763471FF(p)

    class ObjectExpr807:
        @property
        def Equals(self) -> Callable[[Material, Material], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[Material], int]:
            return safe_hash

    return List_distinct(collect(mapping, process_sequence), ObjectExpr807())


__all__ = ["get_protocol_names", "get_protocols", "filter_by_protocol_by", "filter_by_protocol_name", "get_inputs_with_parameter_by", "get_outputs_with_parameter_by", "get_parameters", "get_characteristics", "get_inputs_with_characteristic_by", "get_outputs_with_characteristic_by", "get_outputs_with_factor_by", "get_factors", "get_root_inputs", "get_final_outputs", "get_root_input_of", "get_final_outputs_of", "get_units", "get_data", "get_sources", "get_samples", "get_materials"]

