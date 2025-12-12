from __future__ import annotations
from typing import Any
from ..Core.arc_types import ArcWorkflow
from ..Core.comment import Comment
from ..Core.datamap import Datamap
from ..Core.Helper.collections_ import (ResizeArray_map, ResizeArray_singleton, ResizeArray_choose, Option_fromSeq, Option_fromValueWithDefault)
from ..Core.Helper.identifier import Workflow_cwlFileNameFromIdentifier
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from ..Core.Process.component import (Component, Component_create_Z2F0B38C7)
from ..Core.value import Value as Value_3
from ..CWL.cwlprocessing_unit import CWLProcessingUnit
from ..CWL.cwltypes import CWLType
from ..CWL.decode import Decode_cwlTypeStringMatcher
from ..CWL.encode import (write_yaml, encode_cwltype)
from ..CWL.inputs import (InputBinding, CWLInput, InputBinding_create_ZAC0108A)
from ..CWL.outputs import (OutputBinding, CWLOutput, OutputBinding_create_6DFDD678)
from ..CWL.tool_description import CWLToolDescription
from ..CWL.workflow_description import CWLWorkflowDescription
from ..CWL.workflow_steps import (WorkflowStep, StepOutput)
from ..FileSystem.file_system import FileSystem
from ..ROCrate.ldcontext import LDContext
from ..ROCrate.ldobject import (LDNode, LDGraph)
from ..ROCrate.LDTypes.computational_workflow import LDComputationalWorkflow
from ..ROCrate.LDTypes.computer_language import LDComputerLanguage
from ..ROCrate.LDTypes.dataset import LDDataset
from ..ROCrate.LDTypes.formal_parameter import LDFormalParameter
from ..ROCrate.LDTypes.lab_protocol import LDLabProtocol
from ..ROCrate.LDTypes.property_value import LDPropertyValue
from ..ROCrate.LDTypes.workflow_protocol import LDWorkflowProtocol
from ..fable_modules.fable_library.option import (default_arg, bind, map, value as value_2)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.seq import (try_pick, exactly_one, find)
from ..fable_modules.fable_library.string_ import (to_fail, printf)
from ..fable_modules.fable_library.types import (Array, to_string)
from ..fable_modules.fable_library.util import int32_to_string
from ..fable_modules.yamlicious.decode import (object, IGetters)
from ..fable_modules.yamlicious.yamlicious_types import YAMLElement
from .basic import (BaseTypes_decomposePropertyValue_Z2F770004, BaseTypes_composeDefinedTerm_ZDED3A0F, BaseTypes_composeComment_Z13201A7E, BaseTypes_decomposeDefinedTerm_Z2F770004, BaseTypes_decomposeComment_Z2F770004)
from .datamap import (DatamapConversion_composeFragmentDescriptors_Z892BFC3, DatamapConversion_decomposeFragmentDescriptors_Z6E59645F)
from .person import (PersonConversion_composePerson_Z64D846DC, PersonConversion_decomposePerson_Z6839B9E8)

def _expr3962() -> TypeInfo:
    return class_type("ARCtrl.Conversion.WorkflowConversion", None, WorkflowConversion)


class WorkflowConversion:
    ...

WorkflowConversion_reflection = _expr3962

def WorkflowConversion_composeAdditionalType_Z5C31A0F9(t: CWLType) -> str:
    s: str = write_yaml(encode_cwltype(t))
    return s.strip()


def WorkflowConversion_decomposeAdditionalType_Z721C83C5(t: str) -> CWLType:
    def _arrow3963(get: IGetters, t: Any=t) -> tuple[CWLType, bool]:
        return Decode_cwlTypeStringMatcher(t, get)

    return object(_arrow3963, YAMLElement(4, "dawd"))[0]


def WorkflowConversion_composeFormalParamInputIdentifiers(prefix: str | None=None, position: int | None=None) -> Array[LDNode] | None:
    if prefix is None:
        if position is None:
            return None

        else: 
            po_1: int = position or 0
            return [LDPropertyValue.create_position(po_1)]


    elif position is None:
        pr_1: str = prefix
        return [LDPropertyValue.create_prefix(pr_1)]

    else: 
        po: int = position or 0
        pr: str = prefix
        return [LDPropertyValue.create_position(po), LDPropertyValue.create_prefix(pr)]



def WorkflowConversion_composeFormalParameterFromInput_Z7A02DED7(inp: CWLInput, workflow_name: str | None=None, run_name: str | None=None) -> LDNode:
    additional_type: str
    match_value: CWLType | None = inp.Type_
    if match_value is None:
        raise Exception("Input must have a type")

    else: 
        additional_type = WorkflowConversion_composeAdditionalType_Z5C31A0F9(match_value)

    value_required: bool = not default_arg(inp.Optional, False)
    id: str = LDFormalParameter.gen_id(inp.Name, workflow_name, run_name)
    def binder(ib: InputBinding, inp: Any=inp, workflow_name: Any=workflow_name, run_name: Any=run_name) -> Array[LDNode] | None:
        return WorkflowConversion_composeFormalParamInputIdentifiers(ib.Prefix, ib.Position)

    identifiers: Array[LDNode] | None = bind(binder, inp.InputBinding)
    return LDFormalParameter.create(additional_type, id, None, inp.Name, None, None, None, None, value_required, identifiers)


def WorkflowConversion_decomposeInputBindings_1AAAE9A5(identifiers: Array[LDNode], context: LDContext | None=None) -> InputBinding | None:
    def _arrow3964(n: LDNode, identifiers: Any=identifiers, context: Any=context) -> str | None:
        return LDPropertyValue.try_get_as_prefix(n, context)

    prefix: str | None = try_pick(_arrow3964, identifiers)
    def _arrow3965(n_1: LDNode, identifiers: Any=identifiers, context: Any=context) -> int | None:
        return LDPropertyValue.try_get_as_position(n_1, context)

    position: int | None = try_pick(_arrow3965, identifiers)
    (pattern_matching_result,) = (None,)
    if prefix is None:
        if position is None:
            pattern_matching_result = 0

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        return None

    elif pattern_matching_result == 1:
        return InputBinding_create_ZAC0108A(prefix, position)



def WorkflowConversion_decomposeInputFromFormalParameter_2664C4B8(inp: LDNode, context: LDContext | None=None, graph: LDGraph | None=None) -> CWLInput:
    t_1: CWLType = WorkflowConversion_decomposeAdditionalType_Z721C83C5(exactly_one(inp.AdditionalType))
    binding: InputBinding | None = WorkflowConversion_decomposeInputBindings_1AAAE9A5(LDFormalParameter.get_identifiers(inp, graph, context), context)
    optional: bool | None
    match_value: bool | None = LDFormalParameter.try_get_value_required_as_boolean(inp, context)
    (pattern_matching_result,) = (None,)
    if match_value is not None:
        if match_value:
            pattern_matching_result = 0

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        optional = None

    elif pattern_matching_result == 1:
        optional = True

    return CWLInput(LDFormalParameter.get_name_as_string(inp, context), t_1, binding, optional)


def WorkflowConversion_composeFormalParameterOutputIdentifiers_6DFDD678(glob: str | None=None) -> Array[LDNode] | None:
    if glob is None:
        return None

    else: 
        g: str = glob
        return [LDPropertyValue.create_glob(g)]



def WorkflowConversion_composeFormalParameterFromOutput_Z25C7EC80(out: CWLOutput, workflow_name: str | None=None, run_name: str | None=None) -> LDNode:
    additional_type: str
    match_value: CWLType | None = out.Type_
    if match_value is None:
        raise Exception("Output must have a type")

    else: 
        additional_type = WorkflowConversion_composeAdditionalType_Z5C31A0F9(match_value)

    id: str = LDFormalParameter.gen_id(out.Name, workflow_name, run_name)
    def binder(ob: OutputBinding, out: Any=out, workflow_name: Any=workflow_name, run_name: Any=run_name) -> Array[LDNode] | None:
        return WorkflowConversion_composeFormalParameterOutputIdentifiers_6DFDD678(ob.Glob)

    identifiers: Array[LDNode] | None = bind(binder, out.OutputBinding)
    return LDFormalParameter.create(additional_type, id, None, out.Name, None, None, None, None, True, identifiers)


def WorkflowConversion_decomposeOutputBindings_1AAAE9A5(identifiers: Array[LDNode], context: LDContext | None=None) -> OutputBinding:
    def _arrow3966(n: LDNode, identifiers: Any=identifiers, context: Any=context) -> str | None:
        return LDPropertyValue.try_get_as_glob(n, context)

    return OutputBinding_create_6DFDD678(try_pick(_arrow3966, identifiers))


def WorkflowConversion_decomposeOutputFromFormalParameter_2664C4B8(inp: LDNode, context: LDContext | None=None, graph: LDGraph | None=None) -> CWLOutput:
    t_1: CWLType = WorkflowConversion_decomposeAdditionalType_Z721C83C5(exactly_one(inp.AdditionalType))
    binding: OutputBinding = WorkflowConversion_decomposeOutputBindings_1AAAE9A5(LDFormalParameter.get_identifiers(inp, graph, context), context)
    def _arrow3967(value: bool, inp: Any=inp, context: Any=context, graph: Any=graph) -> bool:
        return not value

    optional: bool | None = map(_arrow3967, LDFormalParameter.try_get_value_required_as_boolean(inp, context))
    return CWLOutput(LDFormalParameter.get_name_as_string(inp, context), t_1, binding)


def WorkflowConversion_composeComputationalTool_Z685B8F25(tool: Component) -> LDNode:
    pattern_input: tuple[str, str | None]
    match_value: OntologyAnnotation | None = tool.ComponentType
    (pattern_matching_result, c_1) = (None, None)
    if match_value is not None:
        def _arrow3968(__unit: None=None, tool: Any=tool) -> bool:
            c: OntologyAnnotation = match_value
            return c.Name is not None

        if _arrow3968():
            pattern_matching_result = 0
            c_1 = match_value

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        pattern_input = (value_2(c_1.Name), c_1.TermAccessionNumber)

    elif pattern_matching_result == 1:
        raise Exception("Component must have a type")

    pattern_input_1: tuple[str | None, str | None]
    match_value_1: Value_3 | None = tool.ComponentValue
    def _arrow3969(__unit: None=None, tool: Any=tool) -> tuple[str | None, str | None]:
        f: float = match_value_1.fields[0]
        return (to_string(f), None)

    def _arrow3970(__unit: None=None, tool: Any=tool) -> tuple[str | None, str | None]:
        i: int = match_value_1.fields[0] or 0
        return (int32_to_string(i), None)

    def _arrow3971(__unit: None=None, tool: Any=tool) -> tuple[str | None, str | None]:
        oa: OntologyAnnotation = match_value_1.fields[0]
        return (oa.Name, oa.TermAccessionNumber)

    def _arrow3972(__unit: None=None, tool: Any=tool) -> tuple[str | None, str | None]:
        s: str = match_value_1.fields[0]
        return (s, None)

    pattern_input_1 = ((None, None)) if (match_value_1 is None) else (_arrow3969() if (match_value_1.tag == 2) else (_arrow3970() if (match_value_1.tag == 1) else (_arrow3971() if (match_value_1.tag == 0) else _arrow3972())))
    pattern_input_2: tuple[str | None, str | None]
    match_value_2: OntologyAnnotation | None = tool.ComponentUnit
    if match_value_2 is None:
        pattern_input_2 = (None, None)

    else: 
        oa_1: OntologyAnnotation = match_value_2
        pattern_input_2 = (oa_1.Name, oa_1.TermAccessionNumber)

    return LDPropertyValue.create_component(pattern_input[0], pattern_input_1[0], None, pattern_input[1], pattern_input_2[1], pattern_input_2[0], pattern_input_1[1])


def WorkflowConversion_decomposeComputationalTool_Z6839B9E8(tool: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Component:
    pattern_input: tuple[OntologyAnnotation, Value_3 | None, OntologyAnnotation | None] = BaseTypes_decomposePropertyValue_Z2F770004(tool, context)
    return Component_create_Z2F0B38C7(pattern_input[1], pattern_input[2], pattern_input[0])


def WorkflowConversion_getInputParametersFromProcessingUnit_30922B92(pu: CWLProcessingUnit) -> Array[CWLInput]:
    if pu.tag == 1:
        def f_1(i_1: CWLInput, pu: Any=pu) -> CWLInput:
            return i_1

        return ResizeArray_map(f_1, pu.fields[0].Inputs)

    else: 
        match_value: Array[CWLInput] | None = pu.fields[0].Inputs
        if match_value is None:
            return []

        else: 
            def f(i: CWLInput, pu: Any=pu) -> CWLInput:
                return i

            return ResizeArray_map(f, match_value)




def WorkflowConversion_get_toolDescriptionTypeName(__unit: None=None) -> str:
    return "ToolDescription"


def WorkflowConversion_get_workflowDescriptionTypeName(__unit: None=None) -> str:
    return "WorkflowDescription"


def WorkflowConversion_composeWorkflowProtocolFromToolDescription_7B8357DA(file_path: str, workflow: CWLToolDescription, workflow_name: str | None=None, run_name: str | None=None) -> LDNode:
    def mapping(a: Array[CWLInput], file_path: Any=file_path, workflow: Any=workflow, workflow_name: Any=workflow_name, run_name: Any=run_name) -> Array[LDNode]:
        def f(i: CWLInput, a: Any=a) -> LDNode:
            return WorkflowConversion_composeFormalParameterFromInput_Z7A02DED7(i, workflow_name, run_name)

        return ResizeArray_map(f, a)

    inputs: Array[LDNode] | None = map(mapping, workflow.Inputs)
    def f_1(o: CWLOutput, file_path: Any=file_path, workflow: Any=workflow, workflow_name: Any=workflow_name, run_name: Any=run_name) -> LDNode:
        return WorkflowConversion_composeFormalParameterFromOutput_Z25C7EC80(o, workflow_name, run_name)

    outputs: Array[LDNode] = ResizeArray_map(f_1, workflow.Outputs)
    return LDWorkflowProtocol.create(file_path, inputs, outputs, None, None, None, None, ResizeArray_singleton(LDComputerLanguage.create_cwl()), None, None, None, None, None, None, None, None, [WorkflowConversion_get_toolDescriptionTypeName()])


def WorkflowConversion_decomposeWorkflowProtocolToToolDescription_2664C4B8(protocol: LDNode, context: LDContext | None=None, graph: LDGraph | None=None) -> CWLToolDescription:
    def f(i: LDNode, protocol: Any=protocol, context: Any=context, graph: Any=graph) -> CWLInput:
        return WorkflowConversion_decomposeInputFromFormalParameter_2664C4B8(i, context, graph)

    inputs: Array[CWLInput] = ResizeArray_map(f, LDComputationalWorkflow.get_inputs_as_formal_parameters(protocol, graph, context))
    def f_1(o: LDNode, protocol: Any=protocol, context: Any=context, graph: Any=graph) -> CWLOutput:
        return WorkflowConversion_decomposeOutputFromFormalParameter_2664C4B8(o, context, graph)

    return CWLToolDescription(ResizeArray_map(f_1, LDComputationalWorkflow.get_outputs_as_formal_parameter(protocol, graph, context)), None, None, None, None, inputs)


def WorkflowConversion_composeWorkflowStep_Z35AB9E5D(step: WorkflowStep, workflow_id: Any) -> LDNode:
    id: str = ((("WorkflowStep_" + str(workflow_id)) + "_") + step.Id) + ""
    cw: LDNode = LDComputationalWorkflow.create(id, None, None, None, None, None, step.Id)
    LDDataset.set_identifier_as_string(cw, step.Run)
    return cw


def WorkflowConversion_composeWorkflowProtocolFromWorkflow_Z6FBB852F(file_path: str, workflow: CWLWorkflowDescription, workflow_name: str | None=None, run_name: str | None=None) -> LDNode:
    def f(i: CWLInput, file_path: Any=file_path, workflow: Any=workflow, workflow_name: Any=workflow_name, run_name: Any=run_name) -> LDNode:
        return WorkflowConversion_composeFormalParameterFromInput_Z7A02DED7(i, workflow_name, run_name)

    inputs: Array[LDNode] = ResizeArray_map(f, workflow.Inputs)
    def f_1(o: CWLOutput, file_path: Any=file_path, workflow: Any=workflow, workflow_name: Any=workflow_name, run_name: Any=run_name) -> LDNode:
        return WorkflowConversion_composeFormalParameterFromOutput_Z25C7EC80(o, workflow_name, run_name)

    outputs: Array[LDNode] = ResizeArray_map(f_1, workflow.Outputs)
    def f_2(s: WorkflowStep, file_path: Any=file_path, workflow: Any=workflow, workflow_name: Any=workflow_name, run_name: Any=run_name) -> LDNode:
        return WorkflowConversion_composeWorkflowStep_Z35AB9E5D(s, file_path)

    steps: Array[LDNode] = ResizeArray_map(f_2, workflow.Steps)
    return LDWorkflowProtocol.create(file_path, inputs, outputs, None, None, None, None, ResizeArray_singleton(LDComputerLanguage.create_cwl()), None, None, None, None, steps, None, None, None, [WorkflowConversion_get_workflowDescriptionTypeName()])


def WorkflowConversion_decomposeWorkflowStep_2664C4B8(step: LDNode, context: LDContext | None=None, graph: LDGraph | None=None) -> WorkflowStep:
    name: str = LDComputationalWorkflow.get_name_as_string(step, context)
    run: str = LDDataset.get_identifier_as_string(step, context)
    return WorkflowStep(name, [], StepOutput.create([]), run)


def WorkflowConversion_decomposeWorkflowProtocolToWorkflow_2664C4B8(protocol: LDNode, context: LDContext | None=None, graph: LDGraph | None=None) -> CWLWorkflowDescription:
    def f(i: LDNode, protocol: Any=protocol, context: Any=context, graph: Any=graph) -> CWLInput:
        return WorkflowConversion_decomposeInputFromFormalParameter_2664C4B8(i, context, graph)

    inputs: Array[CWLInput] = ResizeArray_map(f, LDComputationalWorkflow.get_inputs_as_formal_parameters(protocol, graph, context))
    def f_1(o: LDNode, protocol: Any=protocol, context: Any=context, graph: Any=graph) -> CWLOutput:
        return WorkflowConversion_decomposeOutputFromFormalParameter_2664C4B8(o, context, graph)

    outputs: Array[CWLOutput] = ResizeArray_map(f_1, LDComputationalWorkflow.get_outputs_as_formal_parameter(protocol, graph, context))
    def f_2(s: LDNode, protocol: Any=protocol, context: Any=context, graph: Any=graph) -> WorkflowStep:
        return WorkflowConversion_decomposeWorkflowStep_2664C4B8(s, context, graph)

    return CWLWorkflowDescription(ResizeArray_map(f_2, LDComputationalWorkflow.get_has_part(protocol, graph, context)), inputs, outputs)


def WorkflowConversion_composeWorkflowProtocolFromProcessingUnit_Z3099C0F7(file_path: str, pu: CWLProcessingUnit, workflow_name: str | None=None, run_name: str | None=None) -> LDNode:
    if pu.tag == 1:
        return WorkflowConversion_composeWorkflowProtocolFromWorkflow_Z6FBB852F(file_path, pu.fields[0], workflow_name, run_name)

    else: 
        return WorkflowConversion_composeWorkflowProtocolFromToolDescription_7B8357DA(file_path, pu.fields[0], workflow_name, run_name)



def WorkflowConversion_decomposeWorkflowProtocolToProcessingUnit_2664C4B8(protocol: LDNode, context: LDContext | None=None, graph: LDGraph | None=None) -> CWLProcessingUnit:
    if LDComputationalWorkflow.get_additional_type_as_string(protocol, context) == WorkflowConversion_get_workflowDescriptionTypeName():
        return CWLProcessingUnit(1, WorkflowConversion_decomposeWorkflowProtocolToWorkflow_2664C4B8(protocol, context, graph))

    else: 
        return CWLProcessingUnit(0, WorkflowConversion_decomposeWorkflowProtocolToToolDescription_2664C4B8(protocol, context, graph))



def WorkflowConversion_composeWorkflow_42450E6E(workflow: ArcWorkflow, fs: FileSystem | None=None) -> LDNode:
    workflow_protocol: LDNode
    workflow_file_path: str = Workflow_cwlFileNameFromIdentifier(workflow.Identifier)
    match_value: CWLProcessingUnit | None = workflow.CWLDescription
    if match_value is None:
        arg: str = workflow.Identifier
        workflow_protocol = to_fail(printf("Workflow %s must have a CWL description"))(arg)

    else: 
        workflow_protocol = WorkflowConversion_composeWorkflowProtocolFromProcessingUnit_Z3099C0F7(workflow_file_path, match_value, workflow.Identifier)

    if workflow.Version is not None:
        LDLabProtocol.set_version_as_string(workflow_protocol, value_2(workflow.Version))

    if workflow.URI is not None:
        LDLabProtocol.set_url(workflow_protocol, value_2(workflow.URI))

    if workflow.WorkflowType is not None:
        intended_use: LDNode = BaseTypes_composeDefinedTerm_ZDED3A0F(value_2(workflow.WorkflowType))
        LDLabProtocol.set_intended_use_as_defined_term(workflow_protocol, intended_use)

    def f(df: LDNode, workflow: Any=workflow, fs: Any=fs) -> LDNode | None:
        return LDPropertyValue.try_get_subject_of(df)

    def mapping(datamap: Datamap, workflow: Any=workflow, fs: Any=fs) -> Array[LDNode]:
        return DatamapConversion_composeFragmentDescriptors_Z892BFC3(datamap)

    data_files: Array[LDNode] = ResizeArray_choose(f, default_arg(map(mapping, workflow.Datamap), []))
    if len(workflow.Components) > 0:
        def f_1(tool: Component, workflow: Any=workflow, fs: Any=fs) -> LDNode:
            return WorkflowConversion_composeComputationalTool_Z685B8F25(tool)

        software_tools: Array[LDNode] = ResizeArray_map(f_1, workflow.Components)
        LDLabProtocol.set_computational_tools(workflow_protocol, software_tools)

    def f_2(c: Person, workflow: Any=workflow, fs: Any=fs) -> LDNode:
        return PersonConversion_composePerson_Z64D846DC(c)

    creators: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f_2, workflow.Contacts))
    has_parts: Array[LDNode] | None = Option_fromSeq(data_files)
    def f_3(c_1: Comment, workflow: Any=workflow, fs: Any=fs) -> LDNode:
        return BaseTypes_composeComment_Z13201A7E(c_1)

    comments: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f_3, workflow.Comments))
    return LDDataset.create_arcworkflow(workflow.Identifier, ResizeArray_singleton(workflow_protocol), None, workflow.Title, workflow.Description, creators, has_parts, comments)


def WorkflowConversion_decomposeWorkflow_Z6839B9E8(workflow: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcWorkflow:
    def predicate(me: LDNode, workflow: Any=workflow, graph: Any=graph, context: Any=context) -> bool:
        return LDComputationalWorkflow.validate(me, context)

    workflow_protocol: LDNode = find(predicate, LDDataset.get_main_entities(workflow, graph, context))
    cwl_description: CWLProcessingUnit = WorkflowConversion_decomposeWorkflowProtocolToProcessingUnit_2664C4B8(workflow_protocol, context, graph)
    version: str | None = LDLabProtocol.try_get_version_as_string(workflow_protocol, context)
    uri: str | None = LDLabProtocol.try_get_url(workflow_protocol, context)
    def mapping(iu: LDNode, workflow: Any=workflow, graph: Any=graph, context: Any=context) -> OntologyAnnotation:
        return BaseTypes_decomposeDefinedTerm_Z2F770004(iu, context)

    workflow_type: OntologyAnnotation | None = map(mapping, LDLabProtocol.try_get_intended_use_as_defined_term(workflow_protocol, graph, context))
    def f(ct: LDNode, workflow: Any=workflow, graph: Any=graph, context: Any=context) -> Component:
        return WorkflowConversion_decomposeComputationalTool_Z6839B9E8(ct, graph, context)

    components: Array[Component] = ResizeArray_map(f, LDLabProtocol.get_computational_tools(workflow_protocol, graph, context))
    def f_1(c: LDNode, workflow: Any=workflow, graph: Any=graph, context: Any=context) -> Person:
        return PersonConversion_decomposePerson_Z6839B9E8(c, graph, context)

    contacts: Array[Person] = ResizeArray_map(f_1, LDDataset.get_creators(workflow, graph, context))
    def f_2(c_1: LDNode, workflow: Any=workflow, graph: Any=graph, context: Any=context) -> Comment:
        return BaseTypes_decomposeComment_Z2F770004(c_1, context)

    comments: Array[Comment] = ResizeArray_map(f_2, LDDataset.get_comments(workflow, graph, context))
    datamap: Datamap | None
    v: Datamap = DatamapConversion_decomposeFragmentDescriptors_Z6E59645F(LDDataset.get_variable_measured_as_fragment_descriptors(workflow, graph, context), graph, context)
    datamap = Option_fromValueWithDefault(Datamap.init(), v)
    return ArcWorkflow.create(LDDataset.get_identifier_as_string(workflow, context), LDDataset.try_get_name_as_string(workflow, context), LDDataset.try_get_description_as_string(workflow, context), workflow_type, uri, version, None, None, components, datamap, contacts, cwl_description, comments)


__all__ = ["WorkflowConversion_reflection", "WorkflowConversion_composeAdditionalType_Z5C31A0F9", "WorkflowConversion_decomposeAdditionalType_Z721C83C5", "WorkflowConversion_composeFormalParamInputIdentifiers", "WorkflowConversion_composeFormalParameterFromInput_Z7A02DED7", "WorkflowConversion_decomposeInputBindings_1AAAE9A5", "WorkflowConversion_decomposeInputFromFormalParameter_2664C4B8", "WorkflowConversion_composeFormalParameterOutputIdentifiers_6DFDD678", "WorkflowConversion_composeFormalParameterFromOutput_Z25C7EC80", "WorkflowConversion_decomposeOutputBindings_1AAAE9A5", "WorkflowConversion_decomposeOutputFromFormalParameter_2664C4B8", "WorkflowConversion_composeComputationalTool_Z685B8F25", "WorkflowConversion_decomposeComputationalTool_Z6839B9E8", "WorkflowConversion_getInputParametersFromProcessingUnit_30922B92", "WorkflowConversion_get_toolDescriptionTypeName", "WorkflowConversion_get_workflowDescriptionTypeName", "WorkflowConversion_composeWorkflowProtocolFromToolDescription_7B8357DA", "WorkflowConversion_decomposeWorkflowProtocolToToolDescription_2664C4B8", "WorkflowConversion_composeWorkflowStep_Z35AB9E5D", "WorkflowConversion_composeWorkflowProtocolFromWorkflow_Z6FBB852F", "WorkflowConversion_decomposeWorkflowStep_2664C4B8", "WorkflowConversion_decomposeWorkflowProtocolToWorkflow_2664C4B8", "WorkflowConversion_composeWorkflowProtocolFromProcessingUnit_Z3099C0F7", "WorkflowConversion_decomposeWorkflowProtocolToProcessingUnit_2664C4B8", "WorkflowConversion_composeWorkflow_42450E6E", "WorkflowConversion_decomposeWorkflow_Z6839B9E8"]

