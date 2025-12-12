from __future__ import annotations
from typing import Any
from ..Core.arc_types import ArcRun
from ..Core.comment import Comment
from ..Core.datamap import Datamap
from ..Core.Helper.collections_ import (ResizeArray_singleton, ResizeArray_map, ResizeArray_zip, ResizeArray_appendSingleton, Option_fromSeq, Option_fromValueWithDefault, ResizeArray_filter)
from ..Core.Helper.identifier import Run_cwlFileNameFromIdentifier
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from ..Core.Table.arc_tables import ArcTables
from ..CWL.cwlprocessing_unit import CWLProcessingUnit
from ..CWL.cwltypes import (CWLType, CWLType_file)
from ..CWL.inputs import (InputBinding, CWLInput)
from ..CWL.parameter_reference import CWLParameterReference
from ..FileSystem.file_system import FileSystem
from ..FileSystem.path import (combine_many, combine)
from ..ROCrate.ldcontext import LDContext
from ..ROCrate.ldobject import (LDNode, LDGraph)
from ..ROCrate.LDTypes.computational_workflow import LDComputationalWorkflow
from ..ROCrate.LDTypes.dataset import LDDataset
from ..ROCrate.LDTypes.file import LDFile
from ..ROCrate.LDTypes.formal_parameter import LDFormalParameter
from ..ROCrate.LDTypes.lab_process import LDLabProcess
from ..ROCrate.LDTypes.property_value import LDPropertyValue
from ..ROCrate.LDTypes.workflow_invocation import LDWorkflowInvocation
from ..fable_modules.fable_library.list import of_seq
from ..fable_modules.fable_library.option import (value as value_1, default_arg, bind, map)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.seq import (try_pick, find, exists)
from ..fable_modules.fable_library.string_ import (starts_with_exact, replace, trim_start, join, to_fail, printf)
from ..fable_modules.fable_library.types import (to_string, Array)
from ..fable_modules.fable_library.util import equals
from .assay import AssayConversion_getDataFilesFromProcesses_6BABD1B0
from .basic import (BaseTypes_composeDefinedTerm_ZDED3A0F, BaseTypes_composePropertyValueFromOA_ZDED3A0F, BaseTypes_composeComment_Z13201A7E, BaseTypes_decomposeDefinedTerm_Z2F770004, BaseTypes_decomposePropertyValueToOA_Z2F770004, BaseTypes_decomposeComment_Z2F770004)
from .datamap import (DatamapConversion_composeFragmentDescriptors_Z892BFC3, DatamapConversion_decomposeFragmentDescriptors_Z6E59645F)
from .person import (PersonConversion_composePerson_Z64D846DC, PersonConversion_decomposePerson_Z6839B9E8)
from .table import (ARCtrl_ArcTables__ArcTables_GetProcesses_5E660E5C, ARCtrl_ArcTables__ArcTables_fromProcesses_Static_Z27F0B586)
from .workflow import (WorkflowConversion_composeWorkflowProtocolFromProcessingUnit_Z3099C0F7, WorkflowConversion_getInputParametersFromProcessingUnit_30922B92, WorkflowConversion_decomposeWorkflowProtocolToProcessingUnit_2664C4B8)

def _expr3978() -> TypeInfo:
    return class_type("ARCtrl.Conversion.RunConversion", None, RunConversion)


class RunConversion:
    ...

RunConversion_reflection = _expr3978

def RunConversion_composeCWLInputFilePath_Z384F8060(path: str, run_name: str) -> str:
    if starts_with_exact(path, "../.."):
        return replace(replace(path, "../../", ""), "../..", "")

    else: 
        return combine_many(["runs", run_name, path])



def RunConversion_decomposeCWLInputFilePath_Z384F8060(path: str, run_name: str) -> str:
    prefix: str = combine_many(["runs", run_name])
    if starts_with_exact(path, prefix):
        return trim_start(replace(path, prefix, ""), "/")

    else: 
        return combine("../..", path)



def RunConversion_composeCWLInputValue_70DD9184(input_value: CWLParameterReference, example_of_work: LDNode, input_param: CWLInput, run_name: str) -> LDNode:
    if input_param.Type_ is None:
        raise Exception(((("Cannot convert param values \"" + str(input_value.Values)) + "\" as Input parameter \"") + input_param.Name) + "\" has no type.")

    type_: CWLType = value_1(input_param.Type_)
    if input_value.Type is not None:
        if not equals(value_1(input_value.Type), type_):
            raise Exception(((((("Type (" + to_string(value_1(input_value.Type))) + ") of yml input value \"") + input_value.Key) + "\" does not match type of workflow input parameter (") + to_string(type_)) + ").")


    (pattern_matching_result,) = (None,)
    if type_.tag == 0:
        if len(input_value.Values) == 1:
            pattern_matching_result = 0

        elif to_string(type_).lower().find("array") >= 0:
            pattern_matching_result = 1

        else: 
            pattern_matching_result = 2


    elif to_string(type_).lower().find("array") >= 0:
        pattern_matching_result = 1

    else: 
        pattern_matching_result = 2

    if pattern_matching_result == 0:
        path: str = RunConversion_composeCWLInputFilePath_Z384F8060(input_value.Values[0], run_name)
        return LDFile.create_cwlparameter(path, example_of_work)

    elif pattern_matching_result == 1:
        def binder(ib: InputBinding, input_value: Any=input_value, example_of_work: Any=example_of_work, input_param: Any=input_param, run_name: Any=run_name) -> str | None:
            return ib.ItemSeparator

        values: str = join(default_arg(bind(binder, input_param.InputBinding), ","), input_value.Values)
        return LDPropertyValue.create_cwlparameter(example_of_work, input_value.Key, ResizeArray_singleton(values))

    elif pattern_matching_result == 2:
        return LDPropertyValue.create_cwlparameter(example_of_work, input_value.Key, input_value.Values)



def RunConversion_decomposeCWLInputValue_Z1346FE9D(input_value: LDNode, run_name: str, context: LDContext | None=None, graph: LDGraph | None=None) -> CWLParameterReference:
    example_of_work: LDNode
    match_value: LDNode | None = LDFile.try_get_example_of_work_as_formal_parameter(input_value, graph, context)
    if match_value is None:
        arg: str = input_value.Id
        example_of_work = to_fail(printf("Input value %s of run %s must have an exampleOfWork property pointing to a CWL formal parameter."))(arg)(run_name)

    else: 
        example_of_work = match_value

    key: str = LDFormalParameter.get_name_as_string(example_of_work, context)
    if LDFile.validate_cwlparameter(input_value, context):
        return CWLParameterReference(key, [RunConversion_decomposeCWLInputFilePath_Z384F8060(input_value.Id, run_name)], CWLType_file())

    elif LDPropertyValue.validate_cwlparameter(input_value, context):
        return CWLParameterReference(key, LDPropertyValue.get_values_as_string(input_value, context))

    else: 
        arg_2: str = input_value.Id
        return to_fail(printf("Input value %s of run %s is neither a CWL File nor a CWL Parameter."))(arg_2)(run_name)



def RunConversion_composeWorkflowInvocationFromArcRun_Z8CC08AC(run: ArcRun, fs: FileSystem | None=None) -> Array[LDNode]:
    workflow_protocol: LDNode
    workflow_file_path: str = Run_cwlFileNameFromIdentifier(run.Identifier)
    match_value: CWLProcessingUnit | None = run.CWLDescription
    if match_value is None:
        arg: str = run.Identifier
        workflow_protocol = to_fail(printf("Run %s must have a CWL description"))(arg)

    else: 
        workflow_protocol = WorkflowConversion_composeWorkflowProtocolFromProcessingUnit_Z3099C0F7(workflow_file_path, match_value, None, run.Identifier)

    def f(tupled_arg: tuple[CWLInput, LDNode], run: Any=run, fs: Any=fs) -> LDNode:
        ld_i: LDNode = tupled_arg[1]
        name: str = LDFormalParameter.get_name_as_string(ld_i, workflow_protocol.TryGetContext())
        def chooser(i_1: CWLParameterReference, tupled_arg: Any=tupled_arg) -> CWLParameterReference | None:
            if i_1.Key == name:
                return i_1

            else: 
                return None


        param_ref: CWLParameterReference | None = try_pick(chooser, run.CWLInput)
        if param_ref is None:
            raise Exception(("Could not create workflow invocation for run \"" + run.Identifier) + "\": Workflow parameter \"name\" had no assigned value.")

        else: 
            return RunConversion_composeCWLInputValue_70DD9184(param_ref, ld_i, tupled_arg[0], run.Identifier)


    def _arrow3979(__unit: None=None, run: Any=run, fs: Any=fs) -> Array[tuple[CWLInput, LDNode]]:
        b: Array[LDNode] = LDComputationalWorkflow.get_inputs_as_formal_parameters(workflow_protocol, None, workflow_protocol.TryGetContext())
        return ResizeArray_zip(WorkflowConversion_getInputParametersFromProcessingUnit_30922B92(value_1(run.CWLDescription)), b)

    input_params: Array[LDNode] = ResizeArray_map(f, _arrow3979())
    process_sequence: Array[LDNode] = list(ARCtrl_ArcTables__ArcTables_GetProcesses_5E660E5C(ArcTables(run.Tables), None, None, fs))
    main_invocation: LDNode = LDWorkflowInvocation.create(run.Identifier, workflow_protocol, input_params, None, None, None, None, None, None, workflow_protocol)
    if len(process_sequence) == 0:
        return ResizeArray_singleton(main_invocation)

    else: 
        def f_1(p: LDNode, run: Any=run, fs: Any=fs) -> LDNode:
            id: str = replace(p.Id, "Process", ("WorkflowInvocation_" + run.Identifier) + "")
            name_1: str = LDLabProcess.get_name_as_string(p, p.TryGetContext())
            inputs: Array[LDNode] = LDLabProcess.get_objects(p)
            results: Array[LDNode] | None = Option_fromSeq(LDLabProcess.get_results(p))
            protocol: LDNode | None = LDLabProcess.try_get_executes_lab_protocol(p)
            parameter_values: Array[LDNode] | None = Option_fromSeq(LDLabProcess.get_parameter_values(p))
            def mapping(a_3: LDNode, p: Any=p) -> Array[LDNode]:
                return ResizeArray_singleton(a_3)

            agents: Array[LDNode] | None = map(mapping, LDLabProcess.try_get_agent(p))
            disambiguating_descriptions: Array[str] | None = Option_fromSeq(LDLabProcess.get_disambiguating_descriptions_as_string(p))
            return LDWorkflowInvocation.create(name_1, workflow_protocol, inputs, results, None, agents, id, None, disambiguating_descriptions, protocol, parameter_values)

        return ResizeArray_appendSingleton(main_invocation, ResizeArray_map(f_1, process_sequence))



def RunConversion_decomposeMainWorkflowInvocation_Z1346FE9D(workflow_invocation: LDNode, run_name: str, context: LDContext | None=None, graph: LDGraph | None=None) -> tuple[CWLProcessingUnit, Array[CWLParameterReference]]:
    def _arrow3980(__unit: None=None, workflow_invocation: Any=workflow_invocation, run_name: Any=run_name, context: Any=context, graph: Any=graph) -> CWLProcessingUnit:
        match_value: LDNode | None = LDLabProcess.try_get_executes_lab_protocol(workflow_invocation, graph, context)
        if match_value is None:
            raise Exception(("Could not decompose workflow invocation for run \"" + run_name) + "\": Workflow parameter \"name\" had no assigned value.")

        else: 
            return WorkflowConversion_decomposeWorkflowProtocolToProcessingUnit_2664C4B8(match_value, context, graph)


    def f(iv: LDNode, workflow_invocation: Any=workflow_invocation, run_name: Any=run_name, context: Any=context, graph: Any=graph) -> CWLParameterReference:
        return RunConversion_decomposeCWLInputValue_Z1346FE9D(iv, run_name, context, graph)

    return (_arrow3980(), ResizeArray_map(f, LDLabProcess.get_objects(workflow_invocation, graph, context)))


def RunConversion_composeRun_Z8CC08AC(run: ArcRun, fs: FileSystem | None=None) -> LDNode:
    workflow_invocations: Array[LDNode] | None = Option_fromSeq(RunConversion_composeWorkflowInvocationFromArcRun_Z8CC08AC(run, fs))
    def mapping(term: OntologyAnnotation, run: Any=run, fs: Any=fs) -> LDNode:
        return BaseTypes_composeDefinedTerm_ZDED3A0F(term)

    measurement_method: LDNode | None = map(mapping, run.TechnologyType)
    def mapping_1(term_1: OntologyAnnotation, run: Any=run, fs: Any=fs) -> LDNode:
        return BaseTypes_composeDefinedTerm_ZDED3A0F(term_1)

    measurement_technique: LDNode | None = map(mapping_1, run.TechnologyPlatform)
    def mapping_2(term_2: OntologyAnnotation, run: Any=run, fs: Any=fs) -> LDNode:
        return BaseTypes_composePropertyValueFromOA_ZDED3A0F(term_2)

    variable_measured: LDNode | None = map(mapping_2, run.MeasurementType)
    def f(c: Person, run: Any=run, fs: Any=fs) -> LDNode:
        return PersonConversion_composePerson_Z64D846DC(c)

    creators: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f, run.Performers))
    def mapping_3(datamap: Datamap, run: Any=run, fs: Any=fs) -> Array[LDNode]:
        return DatamapConversion_composeFragmentDescriptors_Z892BFC3(datamap)

    fragment_descriptors: Array[LDNode] | None = map(mapping_3, run.Datamap)
    def mapping_4(ps: Array[LDNode], run: Any=run, fs: Any=fs) -> Array[LDNode]:
        return AssayConversion_getDataFilesFromProcesses_6BABD1B0(ps, fragment_descriptors)

    data_files: Array[LDNode] | None = map(mapping_4, workflow_invocations)
    def _arrow3981(__unit: None=None, run: Any=run, fs: Any=fs) -> Array[LDNode] | None:
        fds_1: Array[LDNode] = fragment_descriptors
        return fds_1

    def _arrow3982(__unit: None=None, run: Any=run, fs: Any=fs) -> Array[LDNode] | None:
        vm_1: LDNode = variable_measured
        return ResizeArray_singleton(vm_1)

    def _arrow3983(__unit: None=None, run: Any=run, fs: Any=fs) -> Array[LDNode] | None:
        fds: Array[LDNode] = fragment_descriptors
        vm: LDNode = variable_measured
        return ResizeArray_appendSingleton(vm, fds)

    variable_measureds: Array[LDNode] | None = (None if (fragment_descriptors is None) else _arrow3981()) if (variable_measured is None) else (_arrow3982() if (fragment_descriptors is None) else _arrow3983())
    def f_1(c_1: Comment, run: Any=run, fs: Any=fs) -> LDNode:
        return BaseTypes_composeComment_Z13201A7E(c_1)

    comments: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f_1, run.Comments))
    return LDDataset.create_arcrun(run.Identifier, None, run.Title, run.Description, creators, data_files, measurement_method, measurement_technique, variable_measureds, workflow_invocations, workflow_invocations, comments)


def RunConversion_decomposeRun_Z6839B9E8(run: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcRun:
    def predicate_1(wi: LDNode, run: Any=run, graph: Any=graph, context: Any=context) -> bool:
        def predicate(i: LDNode, wi: Any=wi) -> bool:
            return LDFile.try_get_example_of_work_as_formal_parameter(i, graph, context) is not None

        return exists(predicate, LDLabProcess.get_objects(wi, graph, context))

    main_workflow_invocation: LDNode = find(predicate_1, LDDataset.get_abouts_as_workflow_invocation(run, graph, context))
    pattern_input: tuple[CWLProcessingUnit, Array[CWLParameterReference]] = RunConversion_decomposeMainWorkflowInvocation_Z1346FE9D(main_workflow_invocation, LDDataset.get_identifier_as_string(run, context), context, graph)
    def mapping(m: LDNode, run: Any=run, graph: Any=graph, context: Any=context) -> OntologyAnnotation:
        return BaseTypes_decomposeDefinedTerm_Z2F770004(m, context)

    measurement_method: OntologyAnnotation | None = map(mapping, LDDataset.try_get_measurement_method_as_defined_term(run, graph, context))
    def mapping_1(m_1: LDNode, run: Any=run, graph: Any=graph, context: Any=context) -> OntologyAnnotation:
        return BaseTypes_decomposeDefinedTerm_Z2F770004(m_1, context)

    measurement_technique: OntologyAnnotation | None = map(mapping_1, LDDataset.try_get_measurement_technique_as_defined_term(run, graph, context))
    def mapping_2(v: LDNode, run: Any=run, graph: Any=graph, context: Any=context) -> OntologyAnnotation:
        return BaseTypes_decomposePropertyValueToOA_Z2F770004(v, context)

    variable_measured: OntologyAnnotation | None = map(mapping_2, LDDataset.try_get_variable_measured_as_measurement_type(run, graph, context))
    def f(c: LDNode, run: Any=run, graph: Any=graph, context: Any=context) -> Person:
        return PersonConversion_decomposePerson_Z6839B9E8(c, graph, context)

    contacts: Array[Person] = ResizeArray_map(f, LDDataset.get_creators(run, graph, context))
    def f_1(c_1: LDNode, run: Any=run, graph: Any=graph, context: Any=context) -> Comment:
        return BaseTypes_decomposeComment_Z2F770004(c_1, context)

    comments: Array[Comment] = ResizeArray_map(f_1, LDDataset.get_comments(run, graph, context))
    datamap: Datamap | None
    v_1: Datamap = DatamapConversion_decomposeFragmentDescriptors_Z6E59645F(LDDataset.get_variable_measured_as_fragment_descriptors(run, graph, context), graph, context)
    datamap = Option_fromValueWithDefault(Datamap.init(), v_1)
    def f_2(wi_1: LDNode, run: Any=run, graph: Any=graph, context: Any=context) -> bool:
        return wi_1.Id != main_workflow_invocation.Id

    tables: ArcTables = ARCtrl_ArcTables__ArcTables_fromProcesses_Static_Z27F0B586(of_seq(ResizeArray_filter(f_2, LDDataset.get_abouts_as_lab_process(run, graph, context))), graph, context)
    return ArcRun.create(LDDataset.get_identifier_as_string(run, context), LDDataset.try_get_name_as_string(run, context), LDDataset.try_get_description_as_string(run, context), variable_measured, measurement_method, measurement_technique, None, tables.Tables, datamap, contacts, pattern_input[0], pattern_input[1], comments)


__all__ = ["RunConversion_reflection", "RunConversion_composeCWLInputFilePath_Z384F8060", "RunConversion_decomposeCWLInputFilePath_Z384F8060", "RunConversion_composeCWLInputValue_70DD9184", "RunConversion_decomposeCWLInputValue_Z1346FE9D", "RunConversion_composeWorkflowInvocationFromArcRun_Z8CC08AC", "RunConversion_decomposeMainWorkflowInvocation_Z1346FE9D", "RunConversion_composeRun_Z8CC08AC", "RunConversion_decomposeRun_Z6839B9E8"]

