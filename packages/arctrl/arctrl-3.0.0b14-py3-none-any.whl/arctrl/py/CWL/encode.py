from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.dynamic_obj.dynamic_obj import DynamicObj
from ..fable_modules.fable_library.list import (map, is_empty, tail, head, FSharpList, singleton, append, of_array, choose, empty, of_seq, cons, reverse, length)
from ..fable_modules.fable_library.map import to_list as to_list_1
from ..fable_modules.fable_library.option import map as map_1
from ..fable_modules.fable_library.seq import (to_list, choose as choose_1, map as map_2, delay, append as append_1, singleton as singleton_1, empty as empty_1)
from ..fable_modules.fable_library.string_ import (split, trim_end, replace, trim_start, join)
from ..fable_modules.fable_library.types import (Array, to_string)
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.yamlicious.encode import (string, int_1, float_1)
from ..fable_modules.yamlicious.writer import write
from ..fable_modules.yamlicious.yamlicious_types import (YAMLContent, YAMLElement, Config)
from .cwlprocessing_unit import CWLProcessingUnit
from .cwltypes import (DirentInstance, CWLType, SchemaDefRequirementType, SoftwarePackage)
from .inputs import (InputBinding, CWLInput)
from .outputs import (OutputBinding, CWLOutput)
from .requirements import (DockerRequirement, EnvironmentDef, Requirement)
from .tool_description import CWLToolDescription
from .workflow_description import CWLWorkflowDescription
from .workflow_steps import (StepInput, StepOutput, WorkflowStep)

def y_bool(b: bool) -> YAMLElement:
    return YAMLElement(1, YAMLContent("true" if b else "false", None))


def y_map(pairs: FSharpList[tuple[str, YAMLElement]]) -> YAMLElement:
    def mapping(tupled_arg: tuple[str, YAMLElement], pairs: Any=pairs) -> YAMLElement:
        def _arrow646(__unit: None=None, tupled_arg: Any=tupled_arg) -> YAMLElement:
            _arg: YAMLElement = tupled_arg[1]
            (pattern_matching_result, single, other) = (None, None, None)
            if _arg.tag == 3:
                if not is_empty(_arg.fields[0]):
                    if is_empty(tail(_arg.fields[0])):
                        pattern_matching_result = 0
                        single = head(_arg.fields[0])

                    else: 
                        pattern_matching_result = 1
                        other = _arg


                else: 
                    pattern_matching_result = 1
                    other = _arg


            else: 
                pattern_matching_result = 1
                other = _arg

            if pattern_matching_result == 0:
                return single

            elif pattern_matching_result == 1:
                return other


        return YAMLElement(0, YAMLContent(tupled_arg[0], None), _arrow646())

    return YAMLElement(3, map(mapping, pairs))


def encode_cwltype(t: CWLType) -> YAMLElement:
    if t.tag == 1:
        return string("Directory")

    elif t.tag == 2:
        d: DirentInstance = t.fields[0]
        def _arrow647(__unit: None=None, t: Any=t) -> FSharpList[tuple[str, YAMLElement]]:
            value_4: bool | None = d.Writable
            acc_3: FSharpList[tuple[str, YAMLElement]]
            value_2: str | None = d.Entryname
            acc_1: FSharpList[tuple[str, YAMLElement]] = singleton(("entry", string(d.Entry)))
            acc_3 = acc_1 if (value_2 is None) else append(acc_1, singleton(("entryname", string(value_2))))
            return acc_3 if (value_4 is None) else append(acc_3, singleton(("writable", y_bool(value_4))))

        return y_map(_arrow647())

    elif t.tag == 3:
        return string("string")

    elif t.tag == 4:
        return string("int")

    elif t.tag == 5:
        return string("long")

    elif t.tag == 6:
        return string("float")

    elif t.tag == 7:
        return string("double")

    elif t.tag == 8:
        return string("boolean")

    elif t.tag == 9:
        return string("stdout")

    elif t.tag == 10:
        return string("null")

    elif t.tag == 11:
        inner: CWLType = t.fields[0]
        short_form: str | None = "File[]" if (inner.tag == 0) else ("Directory[]" if (inner.tag == 1) else ("Dirent[]" if (inner.tag == 2) else ("string[]" if (inner.tag == 3) else ("int[]" if (inner.tag == 4) else ("long[]" if (inner.tag == 5) else ("float[]" if (inner.tag == 6) else ("double[]" if (inner.tag == 7) else ("boolean[]" if (inner.tag == 8) else None))))))))
        if short_form is None:
            return y_map(of_array([("type", string("array")), ("items", encode_cwltype(inner))]))

        else: 
            return string(short_form)


    else: 
        return string("File")



def encode_output_binding(ob: OutputBinding) -> YAMLElement:
    def chooser(x: tuple[str, YAMLElement] | None=None, ob: Any=ob) -> tuple[str, YAMLElement] | None:
        return x

    def mapping(g: str, ob: Any=ob) -> tuple[str, YAMLElement]:
        return ("glob", string(g))

    return y_map(choose(chooser, singleton(map_1(mapping, ob.Glob))))


def encode_cwloutput(o: CWLOutput) -> tuple[str, YAMLElement]:
    pairs: FSharpList[tuple[str, YAMLElement]]
    acc_4: FSharpList[tuple[str, YAMLElement]]
    acc_2: FSharpList[tuple[str, YAMLElement]]
    value_1: CWLType | None = o.Type_
    acc_1: FSharpList[tuple[str, YAMLElement]] = empty()
    acc_2 = acc_1 if (value_1 is None) else append(acc_1, singleton(("type", encode_cwltype(value_1))))
    value_3: OutputBinding | None = o.OutputBinding
    acc_3: FSharpList[tuple[str, YAMLElement]] = acc_2
    acc_4 = acc_3 if (value_3 is None) else append(acc_3, singleton(("outputBinding", encode_output_binding(value_3))))
    value_6: str | None = o.OutputSource
    acc_5: FSharpList[tuple[str, YAMLElement]] = acc_4
    pairs = acc_5 if (value_6 is None) else append(acc_5, singleton(("outputSource", string(value_6))))
    (pattern_matching_result, t_1) = (None, None)
    if not is_empty(pairs):
        if head(pairs)[0] == "type":
            if is_empty(tail(pairs)):
                pattern_matching_result = 0
                t_1 = head(pairs)[1]

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        return (o.Name, t_1)

    elif pattern_matching_result == 1:
        return (o.Name, y_map(pairs))



def encode_input_binding(ib: InputBinding) -> YAMLElement:
    def _arrow648(__unit: None=None, ib: Any=ib) -> FSharpList[tuple[str, YAMLElement]]:
        value_9: bool | None = ib.Separate
        acc_7: FSharpList[tuple[str, YAMLElement]]
        value_7: str | None = ib.ItemSeparator
        acc_5: FSharpList[tuple[str, YAMLElement]]
        value_4: int | None = ib.Position
        acc_3: FSharpList[tuple[str, YAMLElement]]
        value_2: str | None = ib.Prefix
        acc_1: FSharpList[tuple[str, YAMLElement]] = empty()
        acc_3 = acc_1 if (value_2 is None) else append(acc_1, singleton(("prefix", string(value_2))))
        acc_5 = acc_3 if (value_4 is None) else append(acc_3, singleton(("position", int_1(value_4))))
        acc_7 = acc_5 if (value_7 is None) else append(acc_5, singleton(("itemSeparator", string(value_7))))
        return acc_7 if (value_9 is None) else append(acc_7, singleton(("separate", y_bool(value_9))))

    return y_map(_arrow648())


def encode_cwlinput(i: CWLInput) -> tuple[str, YAMLElement]:
    pairs: FSharpList[tuple[str, YAMLElement]]
    acc_4: FSharpList[tuple[str, YAMLElement]]
    acc_2: FSharpList[tuple[str, YAMLElement]]
    value_1: CWLType | None = i.Type_
    acc_1: FSharpList[tuple[str, YAMLElement]] = empty()
    acc_2 = acc_1 if (value_1 is None) else append(acc_1, singleton(("type", encode_cwltype(value_1))))
    value_3: InputBinding | None = i.InputBinding
    acc_3: FSharpList[tuple[str, YAMLElement]] = acc_2
    acc_4 = acc_3 if (value_3 is None) else append(acc_3, singleton(("inputBinding", encode_input_binding(value_3))))
    value_5: bool | None = i.Optional
    acc_5: FSharpList[tuple[str, YAMLElement]] = acc_4
    pairs = acc_5 if (value_5 is None) else append(acc_5, singleton(("optional", y_bool(value_5))))
    (pattern_matching_result, t_1) = (None, None)
    if not is_empty(pairs):
        if head(pairs)[0] == "type":
            if is_empty(tail(pairs)):
                pattern_matching_result = 0
                t_1 = head(pairs)[1]

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        return (i.Name, t_1)

    elif pattern_matching_result == 1:
        return (i.Name, y_map(pairs))



def encode_schema_def_requirement_type(s: SchemaDefRequirementType) -> YAMLElement:
    def chooser(kvp: Any, s: Any=s) -> tuple[str, YAMLElement] | None:
        match_value: Any = kvp[1]
        if str(type(match_value)) == "<class \'str\'>":
            return (kvp[0], string(match_value))

        else: 
            return None


    return y_map(to_list(choose_1(chooser, s.GetProperties(False))))


def encode_requirement(r: Requirement) -> YAMLElement:
    if r.tag == 1:
        def mapping(s: SchemaDefRequirementType, r: Any=r) -> YAMLElement:
            return encode_schema_def_requirement_type(s)

        return y_map(of_array([("class", string("SchemaDefRequirement")), ("types", YAMLElement(2, of_seq(map_2(mapping, r.fields[0]))))]))

    elif r.tag == 2:
        dr: DockerRequirement = r.fields[0]
        def _arrow649(__unit: None=None, r: Any=r) -> FSharpList[tuple[str, YAMLElement]]:
            value_7: str | None = dr.DockerImageId
            acc_5: FSharpList[tuple[str, YAMLElement]]
            value_4: Any | None = dr.DockerFile
            acc_3: FSharpList[tuple[str, YAMLElement]]
            value_2: str | None = dr.DockerPull
            acc_1: FSharpList[tuple[str, YAMLElement]] = singleton(("class", string("DockerRequirement")))
            acc_3 = acc_1 if (value_2 is None) else append(acc_1, singleton(("dockerPull", string(value_2))))
            def mapping_1(tupled_arg: tuple[str, str]) -> tuple[str, YAMLElement]:
                return (tupled_arg[0], string(tupled_arg[1]))

            acc_5 = acc_3 if (value_4 is None) else append(acc_3, singleton(("dockerFile", y_map(map(mapping_1, to_list_1(value_4))))))
            return acc_5 if (value_7 is None) else append(acc_5, singleton(("dockerImageId", string(value_7))))

        return y_map(_arrow649())

    elif r.tag == 3:
        def encode_pkg(p: SoftwarePackage, r: Any=r) -> YAMLElement:
            def _arrow650(__unit: None=None, p: Any=p) -> FSharpList[tuple[str, YAMLElement]]:
                value_13: Array[str] | None = p.Specs
                acc_10: FSharpList[tuple[str, YAMLElement]]
                value_10: Array[str] | None = p.Version
                acc_8: FSharpList[tuple[str, YAMLElement]] = append(empty(), singleton(("package", string(p.Package))))
                acc_10 = acc_8 if (value_10 is None) else append(acc_8, singleton(("version", YAMLElement(2, of_seq(map_2(string, value_10))))))
                return acc_10 if (value_13 is None) else append(acc_10, singleton(("specs", YAMLElement(2, of_seq(map_2(string, value_13))))))

            return y_map(_arrow650())

        return y_map(of_array([("class", string("SoftwareRequirement")), ("packages", YAMLElement(2, of_seq(map_2(encode_pkg, r.fields[0]))))]))

    elif r.tag == 4:
        def encode_dirent(_arg: CWLType, r: Any=r) -> YAMLElement:
            if _arg.tag == 2:
                d: DirentInstance = _arg.fields[0]
                entry_element: YAMLElement
                if d.Entry.find(": ") >= 0:
                    parts: Array[str] = split(d.Entry, [": "], 2, 0)
                    entry_element = y_map(singleton((parts[0], string(parts[1])))) if (len(parts) == 2) else string(d.Entry)

                else: 
                    entry_element = string(d.Entry)

                def _arrow652(__unit: None=None, _arg: Any=_arg) -> FSharpList[tuple[str, YAMLElement]]:
                    value_18: bool | None = d.Writable
                    def _arrow651(__unit: None=None) -> FSharpList[tuple[str, YAMLElement]]:
                        value_16: str | None = d.Entryname
                        acc_12: FSharpList[tuple[str, YAMLElement]] = empty()
                        return acc_12 if (value_16 is None) else append(acc_12, singleton(("entryname", string(value_16))))

                    acc_15: FSharpList[tuple[str, YAMLElement]] = append(_arrow651(), singleton(("entry", entry_element)))
                    return acc_15 if (value_18 is None) else append(acc_15, singleton(("writable", y_bool(value_18))))

                return y_map(_arrow652())

            else: 
                return encode_cwltype(_arg)


        return y_map(of_array([("class", string("InitialWorkDirRequirement")), ("listing", YAMLElement(2, of_seq(map_2(encode_dirent, r.fields[0]))))]))

    elif r.tag == 5:
        def encode_env(e: EnvironmentDef, r: Any=r) -> YAMLElement:
            v_8: str = (("\"" + e.EnvValue) + "\"") if (True if (e.EnvValue == "true") else (e.EnvValue == "false")) else e.EnvValue
            return y_map(of_array([("envName", string(e.EnvName)), ("envValue", string(v_8))]))

        return y_map(of_array([("class", string("EnvVarRequirement")), ("envDef", YAMLElement(2, of_seq(map_2(encode_env, r.fields[0]))))]))

    elif r.tag == 6:
        return y_map(singleton(("class", string("ShellCommandRequirement"))))

    elif r.tag == 7:
        def chooser(kvp: Any, r: Any=r) -> tuple[str, YAMLElement] | None:
            match_value: Any = kvp[1]
            if str(type(match_value)) == "<class \'int\'>":
                return (kvp[0], int_1(match_value))

            elif str(type(match_value)) == "<class \'float\'>":
                return (kvp[0], float_1(match_value))

            elif str(type(match_value)) == "<class \'str\'>":
                return (kvp[0], string(match_value))

            elif str(type(match_value)) == "<class \'bool\'>":
                return (kvp[0], y_bool(match_value))

            else: 
                return None


        dynamic_pairs: FSharpList[tuple[str, YAMLElement]] = to_list(choose_1(chooser, r.fields[0].GetProperties(False)))
        return y_map(append(singleton(("class", string("ResourceRequirement"))), dynamic_pairs))

    elif r.tag == 8:
        return y_map(singleton(("class", string("WorkReuse"))))

    elif r.tag == 9:
        return y_map(of_array([("class", string("NetworkAccess")), ("networkAccess", y_bool(True))]))

    elif r.tag == 10:
        return y_map(singleton(("class", string("InplaceUpdateRequirement"))))

    elif r.tag == 11:
        return y_map(of_array([("class", string("ToolTimeLimit")), ("timelimit", float_1(r.fields[0]))]))

    elif r.tag == 12:
        return y_map(singleton(("class", string("SubworkflowFeatureRequirement"))))

    elif r.tag == 13:
        return y_map(singleton(("class", string("ScatterFeatureRequirement"))))

    elif r.tag == 14:
        return y_map(singleton(("class", string("MultipleInputFeatureRequirement"))))

    elif r.tag == 15:
        return y_map(singleton(("class", string("StepInputExpressionRequirement"))))

    else: 
        return y_map(singleton(("class", string("InlineJavascriptRequirement"))))



def encode_step_input(si: StepInput) -> tuple[str, YAMLElement]:
    pairs: FSharpList[tuple[str, YAMLElement]]
    value_8: str | None = si.ValueFrom
    acc_5: FSharpList[tuple[str, YAMLElement]]
    value_5: str | None = si.DefaultValue
    acc_3: FSharpList[tuple[str, YAMLElement]]
    value_2: str | None = si.Source
    acc_1: FSharpList[tuple[str, YAMLElement]] = empty()
    acc_3 = acc_1 if (value_2 is None) else append(acc_1, singleton(("source", string(value_2))))
    acc_5 = acc_3 if (value_5 is None) else append(acc_3, singleton(("default", string(value_5))))
    pairs = acc_5 if (value_8 is None) else append(acc_5, singleton(("valueFrom", string(value_8))))
    (pattern_matching_result, s_1) = (None, None)
    if not is_empty(pairs):
        if head(pairs)[0] == "source":
            if is_empty(tail(pairs)):
                if (si.ValueFrom is None) if (si.DefaultValue is None) else False:
                    pattern_matching_result = 0
                    s_1 = head(pairs)[1]

                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        return (si.Id, s_1)

    elif pattern_matching_result == 1:
        return (si.Id, y_map(pairs))



def encode_step_inputs(inputs: Array[StepInput]) -> YAMLElement:
    def _arrow653(si: StepInput, inputs: Any=inputs) -> tuple[str, YAMLElement]:
        return encode_step_input(si)

    return y_map(to_list(map_2(_arrow653, inputs)))


def encode_step_output(so: StepOutput) -> YAMLElement:
    def _arrow654(value: str, so: Any=so) -> YAMLElement:
        return string(value)

    return YAMLElement(2, of_seq(map_2(_arrow654, so.Id)))


def encode_workflow_step(ws: WorkflowStep) -> tuple[str, YAMLElement]:
    base_pairs: FSharpList[tuple[str, YAMLElement]] = of_array([("run", string(ws.Run)), ("in", encode_step_inputs(ws.In)), ("out", encode_step_output(ws.Out))])
    with_req: FSharpList[tuple[str, YAMLElement]]
    match_value: Array[Requirement] | None = ws.Requirements
    (pattern_matching_result, r_1) = (None, None)
    if match_value is not None:
        if len(match_value) > 0:
            pattern_matching_result = 0
            r_1 = match_value

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def _arrow655(r_2: Requirement, ws: Any=ws) -> YAMLElement:
            return encode_requirement(r_2)

        with_req = append(base_pairs, singleton(("requirements", YAMLElement(2, of_seq(map_2(_arrow655, r_1))))))

    elif pattern_matching_result == 1:
        with_req = base_pairs

    with_hints: FSharpList[tuple[str, YAMLElement]]
    match_value_1: Array[Requirement] | None = ws.Hints
    (pattern_matching_result_1, h_1) = (None, None)
    if match_value_1 is not None:
        if len(match_value_1) > 0:
            pattern_matching_result_1 = 0
            h_1 = match_value_1

        else: 
            pattern_matching_result_1 = 1


    else: 
        pattern_matching_result_1 = 1

    if pattern_matching_result_1 == 0:
        def _arrow656(r_3: Requirement, ws: Any=ws) -> YAMLElement:
            return encode_requirement(r_3)

        with_hints = append(with_req, singleton(("hints", YAMLElement(2, of_seq(map_2(_arrow656, h_1))))))

    elif pattern_matching_result_1 == 1:
        with_hints = with_req

    return (ws.Id, y_map(with_hints))


def write_yaml(element: YAMLElement) -> str:
    def _arrow657(c: Config, element: Any=element) -> Config:
        return Config(2, c.Level)

    return write(element, _arrow657)


def encode_tool_description(td: CWLToolDescription) -> str:
    def section(pairs: FSharpList[tuple[str, YAMLElement]], td: Any=td) -> FSharpList[str]:
        s: str = write_yaml(y_map(pairs))
        return of_array(trim_end(replace(s, "\r\n", "\n"), "\n").split("\n"))

    base_lines: FSharpList[str] = section(of_array([("cwlVersion", string(td.CWLVersion)), ("class", string("CommandLineTool"))]))
    def mapping(h: Array[Requirement], td: Any=td) -> FSharpList[str]:
        def _arrow658(r: Requirement, h: Any=h) -> YAMLElement:
            return encode_requirement(r)

        return section(singleton(("hints", YAMLElement(2, of_seq(map_2(_arrow658, h))))))

    hints_lines: FSharpList[str] | None = map_1(mapping, td.Hints)
    def mapping_1(r_1: Array[Requirement], td: Any=td) -> FSharpList[str]:
        def _arrow659(r_2: Requirement, r_1: Any=r_1) -> YAMLElement:
            return encode_requirement(r_2)

        return section(singleton(("requirements", YAMLElement(2, of_seq(map_2(_arrow659, r_1))))))

    req_lines: FSharpList[str] | None = map_1(mapping_1, td.Requirements)
    def mapping_2(bc: Array[str], td: Any=td) -> FSharpList[str]:
        def _arrow660(value: str, bc: Any=bc) -> YAMLElement:
            return string(value)

        return section(singleton(("baseCommand", YAMLElement(2, of_seq(map_2(_arrow660, bc))))))

    base_command_lines: FSharpList[str] | None = map_1(mapping_2, td.BaseCommand)
    def mapping_4(i: Array[CWLInput], td: Any=td) -> FSharpList[str]:
        def mapping_3(i_1: CWLInput, i: Any=i) -> tuple[str, YAMLElement]:
            return encode_cwlinput(i_1)

        return section(singleton(("inputs", y_map(to_list(map_2(mapping_3, i))))))

    inputs_lines: FSharpList[str] | None = map_1(mapping_4, td.Inputs)
    def mapping_5(o: CWLOutput, td: Any=td) -> tuple[str, YAMLElement]:
        return encode_cwloutput(o)

    outputs_lines: FSharpList[str] = section(singleton(("outputs", y_map(to_list(map_2(mapping_5, td.Outputs))))))
    def mapping_7(md: DynamicObj, td: Any=td) -> FSharpList[str]:
        def mapping_6(kvp: Any, md: Any=md) -> tuple[str, YAMLElement]:
            def _arrow661(__unit: None=None, kvp: Any=kvp) -> YAMLElement:
                match_value: Any = kvp[1]
                return string(match_value) if (str(type(match_value)) == "<class \'str\'>") else string(to_string(kvp[1]))

            return (kvp[0], _arrow661())

        s_2: str = write_yaml(y_map(to_list(map_2(mapping_6, md.GetProperties(False)))))
        return of_array(trim_end(replace(s_2, "\r\n", "\n"), "\n").split("\n"))

    metadata_lines: FSharpList[str] | None = map_1(mapping_7, td.Metadata)
    def merge(acc_mut: FSharpList[str], remaining_mut: FSharpList[str], td: Any=td) -> FSharpList[str]:
        while True:
            (acc, remaining) = (acc_mut, remaining_mut)
            (pattern_matching_result, a_1, b_1, rest_1, l_6, rest_2) = (None, None, None, None, None, None)
            if is_empty(remaining):
                pattern_matching_result = 2

            elif not is_empty(tail(remaining)):
                if (trim_start(head(tail(remaining))).find(":") >= 0) if (head(remaining).strip() == "-") else False:
                    pattern_matching_result = 0
                    a_1 = head(remaining)
                    b_1 = head(tail(remaining))
                    rest_1 = tail(tail(remaining))

                else: 
                    pattern_matching_result = 1
                    l_6 = head(remaining)
                    rest_2 = tail(remaining)


            else: 
                pattern_matching_result = 1
                l_6 = head(remaining)
                rest_2 = tail(remaining)

            if pattern_matching_result == 0:
                acc_mut = cons((a_1 + " ") + b_1.strip(), acc)
                remaining_mut = rest_1
                continue

            elif pattern_matching_result == 1:
                acc_mut = cons(l_6, acc)
                remaining_mut = rest_2
                continue

            elif pattern_matching_result == 2:
                return reverse(acc)

            break

    def _arrow678(__unit: None=None, td: Any=td) -> IEnumerable_1[str]:
        def _arrow677(__unit: None=None) -> IEnumerable_1[str]:
            def _arrow676(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow663(__unit: None=None) -> IEnumerable_1[str]:
                    match_value_1: FSharpList[str] | None = hints_lines
                    if match_value_1 is None:
                        return empty_1()

                    else: 
                        def _arrow662(__unit: None=None) -> IEnumerable_1[str]:
                            return singleton_1("")

                        return append_1(match_value_1, delay(_arrow662))


                def _arrow675(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow665(__unit: None=None) -> IEnumerable_1[str]:
                        match_value_2: FSharpList[str] | None = req_lines
                        if match_value_2 is None:
                            return empty_1()

                        else: 
                            def _arrow664(__unit: None=None) -> IEnumerable_1[str]:
                                return singleton_1("")

                            return append_1(match_value_2, delay(_arrow664))


                    def _arrow674(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow667(__unit: None=None) -> IEnumerable_1[str]:
                            match_value_3: FSharpList[str] | None = base_command_lines
                            if match_value_3 is None:
                                return empty_1()

                            else: 
                                def _arrow666(__unit: None=None) -> IEnumerable_1[str]:
                                    return singleton_1("")

                                return append_1(match_value_3, delay(_arrow666))


                        def _arrow673(__unit: None=None) -> IEnumerable_1[str]:
                            def _arrow669(__unit: None=None) -> IEnumerable_1[str]:
                                match_value_4: FSharpList[str] | None = inputs_lines
                                if match_value_4 is None:
                                    return empty_1()

                                else: 
                                    def _arrow668(__unit: None=None) -> IEnumerable_1[str]:
                                        return singleton_1("")

                                    return append_1(match_value_4, delay(_arrow668))


                            def _arrow672(__unit: None=None) -> IEnumerable_1[str]:
                                def _arrow671(__unit: None=None) -> IEnumerable_1[str]:
                                    match_value_5: FSharpList[str] | None = metadata_lines
                                    (pattern_matching_result_1, l_5) = (None, None)
                                    if match_value_5 is not None:
                                        if length(match_value_5) > 0:
                                            pattern_matching_result_1 = 0
                                            l_5 = match_value_5

                                        else: 
                                            pattern_matching_result_1 = 1


                                    else: 
                                        pattern_matching_result_1 = 1

                                    if pattern_matching_result_1 == 0:
                                        def _arrow670(__unit: None=None) -> IEnumerable_1[str]:
                                            return l_5

                                        return append_1(singleton_1(""), delay(_arrow670))

                                    elif pattern_matching_result_1 == 1:
                                        return empty_1()


                                return append_1(outputs_lines, delay(_arrow671))

                            return append_1(_arrow669(), delay(_arrow672))

                        return append_1(_arrow667(), delay(_arrow673))

                    return append_1(_arrow665(), delay(_arrow674))

                return append_1(_arrow663(), delay(_arrow675))

            return append_1(singleton_1(""), delay(_arrow676))

        return append_1(base_lines, delay(_arrow677))

    return join("\r\n", merge(empty(), of_array(split(join("\r\n", to_list(delay(_arrow678))), ["\r\n"], None, 0))))


def encode_workflow_description(wd: CWLWorkflowDescription) -> str:
    def section(pairs: FSharpList[tuple[str, YAMLElement]], wd: Any=wd) -> FSharpList[str]:
        s: str = write_yaml(y_map(pairs))
        return of_array(trim_end(replace(s, "\r\n", "\n"), "\n").split("\n"))

    base_lines: FSharpList[str] = section(of_array([("cwlVersion", string(wd.CWLVersion)), ("class", string("Workflow"))]))
    def mapping(r: Array[Requirement], wd: Any=wd) -> FSharpList[str]:
        def _arrow679(r_1: Requirement, r: Any=r) -> YAMLElement:
            return encode_requirement(r_1)

        return section(singleton(("requirements", YAMLElement(2, of_seq(map_2(_arrow679, r))))))

    req_lines: FSharpList[str] | None = map_1(mapping, wd.Requirements)
    def mapping_1(i: CWLInput, wd: Any=wd) -> tuple[str, YAMLElement]:
        return encode_cwlinput(i)

    inputs_lines: FSharpList[str] = section(singleton(("inputs", y_map(to_list(map_2(mapping_1, wd.Inputs))))))
    def mapping_2(ws: WorkflowStep, wd: Any=wd) -> tuple[str, YAMLElement]:
        return encode_workflow_step(ws)

    steps_lines: FSharpList[str] = section(singleton(("steps", y_map(to_list(map_2(mapping_2, wd.Steps))))))
    def mapping_3(o: CWLOutput, wd: Any=wd) -> tuple[str, YAMLElement]:
        return encode_cwloutput(o)

    outputs_lines: FSharpList[str] = section(singleton(("outputs", y_map(to_list(map_2(mapping_3, wd.Outputs))))))
    def mapping_5(md: DynamicObj, wd: Any=wd) -> FSharpList[str]:
        def mapping_4(kvp: Any, md: Any=md) -> tuple[str, YAMLElement]:
            def _arrow680(__unit: None=None, kvp: Any=kvp) -> YAMLElement:
                match_value: Any = kvp[1]
                return string(match_value) if (str(type(match_value)) == "<class \'str\'>") else string(to_string(kvp[1]))

            return (kvp[0], _arrow680())

        s_2: str = write_yaml(y_map(to_list(map_2(mapping_4, md.GetProperties(False)))))
        return of_array(trim_end(replace(s_2, "\r\n", "\n"), "\n").split("\n"))

    metadata_lines: FSharpList[str] | None = map_1(mapping_5, wd.Metadata)
    def merge(acc_mut: FSharpList[str], remaining_mut: FSharpList[str], wd: Any=wd) -> FSharpList[str]:
        while True:
            (acc, remaining) = (acc_mut, remaining_mut)
            (pattern_matching_result, a_1, b_1, rest_1, l_3, rest_2) = (None, None, None, None, None, None)
            if is_empty(remaining):
                pattern_matching_result = 2

            elif not is_empty(tail(remaining)):
                if (trim_start(head(tail(remaining))).find(":") >= 0) if (head(remaining).strip() == "-") else False:
                    pattern_matching_result = 0
                    a_1 = head(remaining)
                    b_1 = head(tail(remaining))
                    rest_1 = tail(tail(remaining))

                else: 
                    pattern_matching_result = 1
                    l_3 = head(remaining)
                    rest_2 = tail(remaining)


            else: 
                pattern_matching_result = 1
                l_3 = head(remaining)
                rest_2 = tail(remaining)

            if pattern_matching_result == 0:
                acc_mut = cons((a_1 + " ") + b_1.strip(), acc)
                remaining_mut = rest_1
                continue

            elif pattern_matching_result == 1:
                acc_mut = cons(l_3, acc)
                remaining_mut = rest_2
                continue

            elif pattern_matching_result == 2:
                return reverse(acc)

            break

    def _arrow692(__unit: None=None, wd: Any=wd) -> IEnumerable_1[str]:
        def _arrow691(__unit: None=None) -> IEnumerable_1[str]:
            def _arrow690(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow682(__unit: None=None) -> IEnumerable_1[str]:
                    match_value_1: FSharpList[str] | None = req_lines
                    if match_value_1 is None:
                        return empty_1()

                    else: 
                        def _arrow681(__unit: None=None) -> IEnumerable_1[str]:
                            return singleton_1("")

                        return append_1(match_value_1, delay(_arrow681))


                def _arrow689(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow688(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow687(__unit: None=None) -> IEnumerable_1[str]:
                            def _arrow686(__unit: None=None) -> IEnumerable_1[str]:
                                def _arrow685(__unit: None=None) -> IEnumerable_1[str]:
                                    def _arrow684(__unit: None=None) -> IEnumerable_1[str]:
                                        match_value_2: FSharpList[str] | None = metadata_lines
                                        (pattern_matching_result_1, l_2) = (None, None)
                                        if match_value_2 is not None:
                                            if length(match_value_2) > 0:
                                                pattern_matching_result_1 = 0
                                                l_2 = match_value_2

                                            else: 
                                                pattern_matching_result_1 = 1


                                        else: 
                                            pattern_matching_result_1 = 1

                                        if pattern_matching_result_1 == 0:
                                            def _arrow683(__unit: None=None) -> IEnumerable_1[str]:
                                                return l_2

                                            return append_1(singleton_1(""), delay(_arrow683))

                                        elif pattern_matching_result_1 == 1:
                                            return empty_1()


                                    return append_1(outputs_lines, delay(_arrow684))

                                return append_1(singleton_1(""), delay(_arrow685))

                            return append_1(steps_lines, delay(_arrow686))

                        return append_1(singleton_1(""), delay(_arrow687))

                    return append_1(inputs_lines, delay(_arrow688))

                return append_1(_arrow682(), delay(_arrow689))

            return append_1(singleton_1(""), delay(_arrow690))

        return append_1(base_lines, delay(_arrow691))

    return join("\r\n", merge(empty(), of_array(split(join("\r\n", to_list(delay(_arrow692))), ["\r\n"], None, 0))))


def encode_processing_unit(pu: CWLProcessingUnit) -> str:
    if pu.tag == 1:
        return encode_workflow_description(pu.fields[0])

    else: 
        return encode_tool_description(pu.fields[0])



__all__ = ["y_bool", "y_map", "encode_cwltype", "encode_output_binding", "encode_cwloutput", "encode_input_binding", "encode_cwlinput", "encode_schema_def_requirement_type", "encode_requirement", "encode_step_input", "encode_step_inputs", "encode_step_output", "encode_workflow_step", "write_yaml", "encode_tool_description", "encode_workflow_description", "encode_processing_unit"]

