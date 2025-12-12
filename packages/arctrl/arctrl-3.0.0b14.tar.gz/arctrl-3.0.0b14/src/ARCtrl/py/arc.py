from __future__ import annotations
from collections.abc import Callable
from typing import Any
from .Contract.arc import try_isaread_contract_from_path
from .Contract.arc_assay import (ARCtrl_ArcAssay__ArcAssay_ToDeleteContract, ARCtrl_ArcAssay__ArcAssay_ToCreateContract_6FCE9E49, ARCtrl_ArcAssay__ArcAssay_ToUpdateContract, ARCtrl_ArcAssay__ArcAssay_tryFromReadContract_Static_7570923F)
from .Contract.arc_investigation import (ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract, ARCtrl_ArcInvestigation__ArcInvestigation_tryFromReadContract_Static_7570923F)
from .Contract.arc_run import (ARCtrl_ArcRun__ArcRun_ToDeleteContract, ARCtrl_ArcRun__ArcRun_ToCreateContract_6FCE9E49, ARCtrl_ArcRun__ArcRun_ToUpdateContract, ARCtrl_ArcRun__ArcRun_tryFromReadContract_Static_7570923F, ARCtrl_ArcRun__ArcRun_tryCWLFromReadContract_Static, ARCtrl_ArcRun__ArcRun_tryYMLFromReadContract_Static)
from .Contract.arc_study import (ARCtrl_ArcStudy__ArcStudy_ToCreateContract_6FCE9E49, ARCtrl_ArcStudy__ArcStudy_ToUpdateContract, ARCtrl_ArcStudy__ArcStudy_tryFromReadContract_Static_7570923F)
from .Contract.arc_workflow import (ARCtrl_ArcWorkflow__ArcWorkflow_ToDeleteContract, ARCtrl_ArcWorkflow__ArcWorkflow_ToCreateContract_6FCE9E49, ARCtrl_ArcWorkflow__ArcWorkflow_ToUpdateContract, ARCtrl_ArcWorkflow__ArcWorkflow_tryFromReadContract_Static_7570923F, ARCtrl_ArcWorkflow__ArcWorkflow_tryCWLFromReadContract_Static)
from .Contract.contract import (Contract, DTOType, DTO)
from .Contract.datamap import (ARCtrl_Datamap__Datamap_ToCreateContractForStudy_Z721C83C5, ARCtrl_Datamap__Datamap_ToUpdateContractForStudy_Z721C83C5, ARCtrl_Datamap__Datamap_ToCreateContractForAssay_Z721C83C5, ARCtrl_Datamap__Datamap_ToUpdateContractForAssay_Z721C83C5, ARCtrl_Datamap__Datamap_ToCreateContractForWorkflow_Z721C83C5, ARCtrl_Datamap__Datamap_ToUpdateContractForWorkflow_Z721C83C5, ARCtrl_Datamap__Datamap_ToCreateContractForRun_Z721C83C5, ARCtrl_Datamap__Datamap_ToUpdateContractForRun_Z721C83C5, ARCtrl_Datamap__Datamap_tryFromReadContractForAssay_Static, ARCtrl_Datamap__Datamap_tryFromReadContractForStudy_Static, ARCtrl_Datamap__Datamap_tryFromReadContractForWorkflow_Static, ARCtrl_Datamap__Datamap_tryFromReadContractForRun_Static)
from .Contract.git import (Init_createInitContract_6DFDD678, gitignore_contract, gitattributes_contract, Init_createAddRemoteContract_Z721C83C5, Clone_createCloneContract_5000466F)
from .Contract.validation_packages_config import (ValidationPackagesConfigHelper_ConfigFilePath, ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toCreateContract_Static_724DAE55, ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toDeleteContract_Static_724DAE55, ValidationPackagesConfigHelper_ReadContract, ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_tryFromReadContract_Static_7570923F)
from .Core.arc_types import (ArcInvestigation, ArcAssay, ArcStudy, ArcRun, ArcWorkflow, ArcInvestigation_reflection)
from .Core.comment import (Comment, Remark)
from .Core.data import Data
from .Core.data_context import DataContext
from .Core.datamap import Datamap
from .Core.Helper.collections_ import (ResizeArray_iter, ResizeArray_map)
from .Core.Helper.identifier import (create_missing_identifier, Study_fileNameFromIdentifier, Study_datamapFileNameFromIdentifier, Assay_fileNameFromIdentifier, Assay_datamapFileNameFromIdentifier, Workflow_fileNameFromIdentifier, Workflow_datamapFileNameFromIdentifier, Run_fileNameFromIdentifier, Run_datamapFileNameFromIdentifier)
from .Core.identifier_setters import set_investigation_identifier
from .Core.ontology_source_reference import OntologySourceReference
from .Core.person import Person
from .Core.publication import Publication
from .Core.Table.arc_table import ArcTable
from .Core.Table.arc_tables import ArcTables
from .Core.Table.composite_cell import CompositeCell
from .Core.Table.composite_column import CompositeColumn
from .CWL.cwlprocessing_unit import CWLProcessingUnit
from .CWL.parameter_reference import CWLParameterReference
from .FileSystem.file_system import FileSystem
from .FileSystem.file_system_tree import FileSystemTree
from .FileSystem.path import (get_assay_folder_path, get_run_folder_path, get_workflow_folder_path, get_study_folder_path)
from .Json.encode import default_spaces
from .Spreadsheet.arc_assay import ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F
from .Spreadsheet.arc_investigation import ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF
from .Spreadsheet.arc_run import ARCtrl_ArcRun__ArcRun_toFsWorkbook_Static_Z3EFAF6F8
from .Spreadsheet.arc_study import ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522
from .Spreadsheet.arc_workflow import ARCtrl_ArcWorkflow__ArcWorkflow_toFsWorkbook_Static_Z1C75CB0E
from .Spreadsheet.datamap import to_fs_workbook
from .ValidationPackages.validation_packages_config import ValidationPackagesConfig
from .ContractIO.contract_io import full_fill_contract_batch_async
from .ContractIO.file_system_helper import get_all_file_paths_async
from .fable_modules.thoth_json_python.decode import Decode_fromString
from .fable_modules.thoth_json_python.encode import to_string
from .license import License
from .fable_modules.fable_library.array_ import (filter, map, choose, iterate as iterate_1, exists, fold, concat, contains as contains_2, append as append_1, try_pick, equals_with)
from .fable_modules.fable_library.async_ import run_synchronously
from .fable_modules.fable_library.async_builder import (Async, singleton)
from .fable_modules.fable_library.list import FSharpList
from .fable_modules.fable_library.map import of_seq as of_seq_1
from .fable_modules.fable_library.map_util import add_to_dict
from .fable_modules.fable_library.option import (value as value_9, default_arg, map as map_1, bind, default_arg_with)
from .fable_modules.fable_library.reflection import (TypeInfo, class_type)
from .fable_modules.fable_library.result import FSharpResult_2
from .fable_modules.fable_library.seq import (to_array, contains, delay, append, singleton as singleton_1, iterate, try_find, find, empty, collect, to_list)
from .fable_modules.fable_library.set import (of_seq, contains as contains_1, union_many, FSharpSet__Contains)
from .fable_modules.fable_library.string_ import (starts_with_exact, join, to_fail, printf, replace, to_text)
from .fable_modules.fable_library.types import (Array, FSharpRef)
from .fable_modules.fable_library.util import (string_hash, IEnumerable_1, compare_primitives, curry2, ignore, safe_hash, get_enumerator, dispose, to_enumerable, equals)
from .fable_modules.fs_spreadsheet.Cells.fs_cells_collection import Dictionary_tryGet
from .fable_modules.thoth_json_core.types import IEncodable
from .rocrate_io import (ROCrate_get_decoderDeprecated, ROCrate_get_decoder, ROCrate_encoder_1E8A3F74)

def _expr4228() -> TypeInfo:
    return class_type("ARCtrl.ARC", None, ARC, ArcInvestigation_reflection())


class ARC(ArcInvestigation):
    def __init__(self, identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, ontology_source_references: Array[OntologySourceReference] | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, assays: Array[ArcAssay] | None=None, studies: Array[ArcStudy] | None=None, workflows: Array[ArcWorkflow] | None=None, runs: Array[ArcRun] | None=None, registered_study_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None, remarks: Array[Remark] | None=None, fs: FileSystem | None=None, license: License | None=None) -> None:
        super().__init__(identifier, title, description, submission_date, public_release_date, ontology_source_references, publications, contacts, assays, studies, workflows, runs, registered_study_identifiers, comments, remarks)
        this: FSharpRef[ARC] = FSharpRef(None)
        this.contents = self
        self._license: License | None = license
        def _arrow4227(__unit: None=None) -> FileSystem:
            fs_1: FileSystem = default_arg(fs, FileSystem.create(tree = FileSystemTree(1, "", [])))
            return ARCAux_updateFSByARC(this.contents, license, fs_1)

        self._fs: FileSystem = _arrow4227()
        self.init_0040114: int = 1

    @property
    def FileSystem(self, __unit: None=None) -> FileSystem:
        this: ARC = self
        return this._fs

    @FileSystem.setter
    def FileSystem(self, fs: FileSystem) -> None:
        this: ARC = self
        this._fs = fs

    @property
    def License(self, __unit: None=None) -> License | None:
        this: ARC = self
        return this._license

    @License.setter
    def License(self, license: License | None=None) -> None:
        this: ARC = self
        this._license = license

    @staticmethod
    def from_arc_investigation(isa: ArcInvestigation, fs: FileSystem | None=None, license: License | None=None) -> ARC:
        return ARC(isa.Identifier, isa.Title, isa.Description, isa.SubmissionDate, isa.PublicReleaseDate, isa.OntologySourceReferences, isa.Publications, isa.Contacts, isa.Assays, isa.Studies, isa.Workflows, isa.Runs, isa.RegisteredStudyIdentifiers, isa.Comments, isa.Remarks, fs, license)

    def TryWriteAsync(self, arc_path: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetWriteContracts())

    def TryUpdateAsync(self, arc_path: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetUpdateContracts())

    def SetLicenseFulltext(self, fulltext: str, path: str | None=None) -> None:
        this: ARC = self
        match_value: License | None = this.License
        if match_value is None:
            license_1: License = License("fulltext", fulltext)
            this.License = license_1
            if path is not None:
                license_1.Path = value_9(path)


        else: 
            license: License = match_value
            license.Type = "fulltext"
            license.Content = fulltext
            if path is not None:
                license.Path = value_9(path)



    @staticmethod
    def try_load_async(arc_path: str) -> Async[FSharpResult_2[ARC, Array[str]]]:
        def _arrow4103(__unit: None=None) -> Async[FSharpResult_2[ARC, Array[str]]]:
            def _arrow4102(_arg: Array[str]) -> Async[FSharpResult_2[ARC, Array[str]]]:
                arc: ARC = ARC.from_file_paths(to_array(_arg))
                contracts: Array[Contract] = arc.GetReadContracts()
                def _arrow4101(_arg_1: FSharpResult_2[Array[Contract], Array[str]]) -> Async[FSharpResult_2[ARC, Array[str]]]:
                    ful_filled_contracts: FSharpResult_2[Array[Contract], Array[str]] = _arg_1
                    if ful_filled_contracts.tag == 1:
                        return singleton.Return(FSharpResult_2(1, ful_filled_contracts.fields[0]))

                    else: 
                        arc.SetISAFromContracts(ful_filled_contracts.fields[0])
                        return singleton.Return(FSharpResult_2(0, arc))


                return singleton.Bind(full_fill_contract_batch_async(arc_path, contracts), _arrow4101)

            return singleton.Bind(get_all_file_paths_async(arc_path), _arrow4102)

        return singleton.Delay(_arrow4103)

    def GetAssayRemoveContracts(self, assay_identifier: str) -> Array[Contract]:
        this: ARC = self
        class ObjectExpr4105:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow4104(x: str, y: str) -> bool:
                    return x == y

                return _arrow4104

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if not contains(assay_identifier, this.AssayIdentifiers, ObjectExpr4105()):
            raise Exception("ARC does not contain assay with given name")

        assay: ArcAssay = this.GetAssay(assay_identifier)
        studies: Array[ArcStudy] = assay.StudiesRegisteredIn
        super().RemoveAssay(assay_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        assay_folder_path: str = get_assay_folder_path(assay_identifier)
        def predicate(p: str) -> bool:
            return not starts_with_exact(p, assay_folder_path)

        filtered_paths: Array[str] = filter(predicate, paths)
        this.SetFilePaths(filtered_paths)
        def _arrow4107(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow4106(__unit: None=None) -> IEnumerable_1[Contract]:
                return this.GetUpdateContracts()

            return append(singleton_1(ARCtrl_ArcAssay__ArcAssay_ToDeleteContract(assay)), delay(_arrow4106))

        return to_array(delay(_arrow4107))

    def GetRunRemoveContracts(self, run_identifier: str) -> Array[Contract]:
        this: ARC = self
        class ObjectExpr4109:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow4108(x: str, y: str) -> bool:
                    return x == y

                return _arrow4108

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if not contains(run_identifier, this.RunIdentifiers, ObjectExpr4109()):
            raise Exception("ARC does not contain run with given name")

        run: ArcRun = this.GetRun(run_identifier)
        this.DeleteRun(run_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        run_folder_path: str = get_run_folder_path(run_identifier)
        def predicate(p: str) -> bool:
            return not starts_with_exact(p, run_folder_path)

        filtered_paths: Array[str] = filter(predicate, paths)
        this.SetFilePaths(filtered_paths)
        def _arrow4111(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow4110(__unit: None=None) -> IEnumerable_1[Contract]:
                return this.GetUpdateContracts()

            return append(singleton_1(ARCtrl_ArcRun__ArcRun_ToDeleteContract(run)), delay(_arrow4110))

        return to_array(delay(_arrow4111))

    def GetWorkflowRemoveContracts(self, workflow_identifier: str) -> Array[Contract]:
        this: ARC = self
        class ObjectExpr4113:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow4112(x: str, y: str) -> bool:
                    return x == y

                return _arrow4112

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if not contains(workflow_identifier, this.WorkflowIdentifiers, ObjectExpr4113()):
            raise Exception("ARC does not contain workflow with given name")

        workflow: ArcWorkflow = this.GetWorkflow(workflow_identifier)
        this.DeleteWorkflow(workflow_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        workflow_folder_path: str = get_workflow_folder_path(workflow_identifier)
        def predicate(p: str) -> bool:
            return not starts_with_exact(p, workflow_folder_path)

        filtered_paths: Array[str] = filter(predicate, paths)
        this.SetFilePaths(filtered_paths)
        def _arrow4115(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow4114(__unit: None=None) -> IEnumerable_1[Contract]:
                return this.GetUpdateContracts()

            return append(singleton_1(ARCtrl_ArcWorkflow__ArcWorkflow_ToDeleteContract(workflow)), delay(_arrow4114))

        return to_array(delay(_arrow4115))

    def TryRemoveAssayAsync(self, arc_path: str, assay_identifier: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetAssayRemoveContracts(assay_identifier))

    def TryRemoveRunAsync(self, arc_path: str, run_identifier: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetRunRemoveContracts(run_identifier))

    def TryRemoveWorkflowAsync(self, arc_path: str, workflow_identifier: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetWorkflowRemoveContracts(workflow_identifier))

    def RemoveRunAsync(self, arc_path: str, run_identifier: str) -> Async[None]:
        this: ARC = self
        def _arrow4117(__unit: None=None) -> Async[None]:
            def _arrow4116(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not remove run, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryRemoveRunAsync(arc_path, run_identifier), _arrow4116)

        return singleton.Delay(_arrow4117)

    def RemoveWorkflowAsync(self, arc_path: str, workflow_identifier: str) -> Async[None]:
        this: ARC = self
        def _arrow4119(__unit: None=None) -> Async[None]:
            def _arrow4118(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not remove workflow, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryRemoveWorkflowAsync(arc_path, workflow_identifier), _arrow4118)

        return singleton.Delay(_arrow4119)

    def TryRenameRunAsync(self, arc_path: str, old_run_identifier: str, new_run_identifier: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetRunRenameContracts(old_run_identifier, new_run_identifier))

    def TryRenameWorkflowAsync(self, arc_path: str, old_workflow_identifier: str, new_workflow_identifier: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetWorkflowRenameContracts(old_workflow_identifier, new_workflow_identifier))

    def RenameRunAsync(self, arc_path: str, old_run_identifier: str, new_run_identifier: str) -> Async[None]:
        this: ARC = self
        def _arrow4121(__unit: None=None) -> Async[None]:
            def _arrow4120(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not rename run, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryRenameRunAsync(arc_path, old_run_identifier, new_run_identifier), _arrow4120)

        return singleton.Delay(_arrow4121)

    def RenameWorkflowAsync(self, arc_path: str, old_workflow_identifier: str, new_workflow_identifier: str) -> Async[None]:
        this: ARC = self
        def _arrow4123(__unit: None=None) -> Async[None]:
            def _arrow4122(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not rename workflow, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryRenameWorkflowAsync(arc_path, old_workflow_identifier, new_workflow_identifier), _arrow4122)

        return singleton.Delay(_arrow4123)

    def GetAssayRenameContracts(self, old_assay_identifier: str, new_assay_identifier: str) -> Array[Contract]:
        this: ARC = self
        class ObjectExpr4125:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow4124(x: str, y: str) -> bool:
                    return x == y

                return _arrow4124

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if not contains(old_assay_identifier, this.AssayIdentifiers, ObjectExpr4125()):
            raise Exception("ARC does not contain assay with given name")

        super().RenameAssay(old_assay_identifier, new_assay_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        old_assay_folder_path: str = get_assay_folder_path(old_assay_identifier)
        new_assay_folder_path: str = get_assay_folder_path(new_assay_identifier)
        def mapping(p: str) -> str:
            return replace(p, old_assay_folder_path, new_assay_folder_path)

        renamed_paths: Array[str] = map(mapping, paths, None)
        this.SetFilePaths(renamed_paths)
        def _arrow4127(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow4126(__unit: None=None) -> IEnumerable_1[Contract]:
                return this.GetUpdateContracts()

            return append(singleton_1(Contract.create_rename(old_assay_folder_path, new_assay_folder_path)), delay(_arrow4126))

        return to_array(delay(_arrow4127))

    def GetRunRenameContracts(self, old_run_identifier: str, new_run_identifier: str) -> Array[Contract]:
        this: ARC = self
        class ObjectExpr4129:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow4128(x: str, y: str) -> bool:
                    return x == y

                return _arrow4128

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if not contains(old_run_identifier, this.RunIdentifiers, ObjectExpr4129()):
            raise Exception("ARC does not contain run with given name")

        super().RenameRun(old_run_identifier, new_run_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        old_path: str = get_run_folder_path(old_run_identifier)
        new_path: str = get_run_folder_path(new_run_identifier)
        def mapping(p: str) -> str:
            return replace(p, old_path, new_path)

        renamed_paths: Array[str] = map(mapping, paths, None)
        this.SetFilePaths(renamed_paths)
        def _arrow4131(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow4130(__unit: None=None) -> IEnumerable_1[Contract]:
                return this.GetUpdateContracts()

            return append(singleton_1(Contract.create_rename(old_path, new_path)), delay(_arrow4130))

        return to_array(delay(_arrow4131))

    def GetWorkflowRenameContracts(self, old_workflow_identifier: str, new_workflow_identifier: str) -> Array[Contract]:
        this: ARC = self
        class ObjectExpr4133:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow4132(x: str, y: str) -> bool:
                    return x == y

                return _arrow4132

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if not contains(old_workflow_identifier, this.WorkflowIdentifiers, ObjectExpr4133()):
            raise Exception("ARC does not contain workflow with given name")

        super().RenameWorkflow(old_workflow_identifier, new_workflow_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        old_path: str = get_workflow_folder_path(old_workflow_identifier)
        new_path: str = get_workflow_folder_path(new_workflow_identifier)
        def mapping(p: str) -> str:
            return replace(p, old_path, new_path)

        renamed_paths: Array[str] = map(mapping, paths, None)
        this.SetFilePaths(renamed_paths)
        def _arrow4135(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow4134(__unit: None=None) -> IEnumerable_1[Contract]:
                return this.GetUpdateContracts()

            return append(singleton_1(Contract.create_rename(old_path, new_path)), delay(_arrow4134))

        return to_array(delay(_arrow4135))

    def TryRenameAssayAsync(self, arc_path: str, old_assay_identifier: str, new_assay_identifier: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetAssayRenameContracts(old_assay_identifier, new_assay_identifier))

    def GetStudyRemoveContracts(self, study_identifier: str) -> Array[Contract]:
        this: ARC = self
        super().RemoveStudy(study_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        study_folder_path: str = get_study_folder_path(study_identifier)
        def predicate(p: str) -> bool:
            return not starts_with_exact(p, study_folder_path)

        filtered_paths: Array[str] = filter(predicate, paths)
        this.SetFilePaths(filtered_paths)
        return [Contract.create_delete(study_folder_path), ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract(this)]

    def TryRemoveStudyAsync(self, arc_path: str, study_identifier: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetStudyRemoveContracts(study_identifier))

    def GetStudyRenameContracts(self, old_study_identifier: str, new_study_identifier: str) -> Array[Contract]:
        this: ARC = self
        class ObjectExpr4137:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow4136(x: str, y: str) -> bool:
                    return x == y

                return _arrow4136

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if not contains(old_study_identifier, this.StudyIdentifiers, ObjectExpr4137()):
            raise Exception("ARC does not contain study with given name")

        super().RenameStudy(old_study_identifier, new_study_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        old_study_folder_path: str = get_study_folder_path(old_study_identifier)
        new_study_folder_path: str = get_study_folder_path(new_study_identifier)
        def mapping(p: str) -> str:
            return replace(p, old_study_folder_path, new_study_folder_path)

        renamed_paths: Array[str] = map(mapping, paths, None)
        this.SetFilePaths(renamed_paths)
        def _arrow4139(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow4138(__unit: None=None) -> IEnumerable_1[Contract]:
                return this.GetUpdateContracts()

            return append(singleton_1(Contract.create_rename(old_study_folder_path, new_study_folder_path)), delay(_arrow4138))

        return to_array(delay(_arrow4139))

    def TryRenameStudyAsync(self, arc_path: str, old_study_identifier: str, new_study_identifier: str) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        this: ARC = self
        return full_fill_contract_batch_async(arc_path, this.GetStudyRenameContracts(old_study_identifier, new_study_identifier))

    def WriteAsync(self, arc_path: str) -> Async[None]:
        this: ARC = self
        def _arrow4141(__unit: None=None) -> Async[None]:
            def _arrow4140(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not write ARC, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryWriteAsync(arc_path), _arrow4140)

        return singleton.Delay(_arrow4141)

    def UpdateAsync(self, arc_path: str) -> Async[None]:
        this: ARC = self
        def _arrow4143(__unit: None=None) -> Async[None]:
            def _arrow4142(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not update ARC, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryUpdateAsync(arc_path), _arrow4142)

        return singleton.Delay(_arrow4143)

    def RemoveAssayAsync(self, arc_path: str, assay_identifier: str) -> Async[None]:
        this: ARC = self
        def _arrow4145(__unit: None=None) -> Async[None]:
            def _arrow4144(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not remove assay, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryRemoveAssayAsync(arc_path, assay_identifier), _arrow4144)

        return singleton.Delay(_arrow4145)

    def RenameAssayAsync(self, arc_path: str, old_assay_identifier: str, new_assay_identifier: str) -> Async[None]:
        this: ARC = self
        def _arrow4147(__unit: None=None) -> Async[None]:
            def _arrow4146(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not rename assay, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryRenameAssayAsync(arc_path, old_assay_identifier, new_assay_identifier), _arrow4146)

        return singleton.Delay(_arrow4147)

    def RemoveStudyAsync(self, arc_path: str, study_identifier: str) -> Async[None]:
        this: ARC = self
        def _arrow4149(__unit: None=None) -> Async[None]:
            def _arrow4148(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not remove study, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryRemoveStudyAsync(arc_path, study_identifier), _arrow4148)

        return singleton.Delay(_arrow4149)

    def RenameStudyAsync(self, arc_path: str, old_study_identifier: str, new_study_identifier: str) -> Async[None]:
        this: ARC = self
        def _arrow4151(__unit: None=None) -> Async[None]:
            def _arrow4150(_arg: FSharpResult_2[Array[Contract], Array[str]]) -> Async[None]:
                result: FSharpResult_2[Array[Contract], Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not rename study, failed with the following errors %s"))(appended)
                    return singleton.Zero()

                else: 
                    return singleton.Zero()


            return singleton.Bind(this.TryRenameStudyAsync(arc_path, old_study_identifier, new_study_identifier), _arrow4150)

        return singleton.Delay(_arrow4151)

    @staticmethod
    def load_async(arc_path: str) -> Async[ARC]:
        def _arrow4153(__unit: None=None) -> Async[ARC]:
            def _arrow4152(_arg: FSharpResult_2[ARC, Array[str]]) -> Async[ARC]:
                result: FSharpResult_2[ARC, Array[str]] = _arg
                if result.tag == 1:
                    def mapping(e: str) -> str:
                        return e

                    appended: str = join("\n", map(mapping, result.fields[0], None))
                    to_fail(printf("Could not load ARC, failed with the following errors %s"))(appended)
                    return singleton.Return(ARC(create_missing_identifier()))

                else: 
                    return singleton.Return(result.fields[0])


            return singleton.Bind(ARC.try_load_async(arc_path), _arrow4152)

        return singleton.Delay(_arrow4153)

    def Write(self, arc_path: str) -> None:
        this: ARC = self
        run_synchronously(this.WriteAsync(arc_path))

    def Update(self, arc_path: str) -> None:
        this: ARC = self
        run_synchronously(this.UpdateAsync(arc_path))

    def RemoveAssay(self, arc_path: str, assay_identifier: str) -> None:
        this: ARC = self
        run_synchronously(this.RemoveAssayAsync(arc_path, assay_identifier))

    def RenameAssay(self, arc_path: str, old_assay_identifier: str, new_assay_identifier: str) -> None:
        this: ARC = self
        run_synchronously(this.RenameAssayAsync(arc_path, old_assay_identifier, new_assay_identifier))

    def RemoveStudy(self, arc_path: str, study_identifier: str) -> None:
        this: ARC = self
        run_synchronously(this.RemoveStudyAsync(arc_path, study_identifier))

    def RenameStudy(self, arc_path: str, old_study_identifier: str, new_study_identifier: str) -> None:
        this: ARC = self
        run_synchronously(this.RenameStudyAsync(arc_path, old_study_identifier, new_study_identifier))

    def RemoveRun(self, arc_path: str, run_identifier: str) -> None:
        this: ARC = self
        run_synchronously(this.RemoveRunAsync(arc_path, run_identifier))

    def RenameRun(self, arc_path: str, old_run_identifier: str, new_run_identifier: str) -> None:
        this: ARC = self
        run_synchronously(this.RenameRunAsync(arc_path, old_run_identifier, new_run_identifier))

    def RemoveWorkflow(self, arc_path: str, workflow_identifier: str) -> None:
        this: ARC = self
        run_synchronously(this.RemoveWorkflowAsync(arc_path, workflow_identifier))

    def RenameWorkflow(self, arc_path: str, old_workflow_identifier: str, new_workflow_identifier: str) -> None:
        this: ARC = self
        run_synchronously(this.RenameWorkflowAsync(arc_path, old_workflow_identifier, new_workflow_identifier))

    @staticmethod
    def load(arc_path: str) -> ARC:
        return run_synchronously(ARC.load_async(arc_path))

    def MakeDataFilesAbsolute(self, __unit: None=None) -> None:
        this: ARC = self
        class ObjectExpr4154:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        files_paths: Any = of_seq(this.FileSystem.Tree.ToFilePaths(), ObjectExpr4154())
        def check_existence_from_root(p: str) -> bool:
            return contains_1(p, files_paths)

        def update_column_option(data_name_function: Callable[[Data], str], col: CompositeColumn | None=None) -> None:
            (pattern_matching_result, col_2) = (None, None)
            if col is not None:
                def _arrow4155(__unit: None=None, data_name_function: Any=data_name_function, col: Any=col) -> bool:
                    col_1: CompositeColumn = col
                    return col_1.Header.IsDataColumn

                if _arrow4155():
                    pattern_matching_result = 0
                    col_2 = col

                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1

            if pattern_matching_result == 0:
                def f(c: CompositeCell, data_name_function: Any=data_name_function, col: Any=col) -> None:
                    if c.AsData.FilePath is not None:
                        new_file_path: str = data_name_function(c.AsData)
                        c.AsData.FilePath = new_file_path


                ResizeArray_iter(f, col_2.Cells)

            elif pattern_matching_result == 1:
                pass


        def update_table(data_name_function_1: Callable[[Data], str], t: ArcTable) -> None:
            update_column_option(data_name_function_1, t.TryGetInputColumn())
            update_column_option(data_name_function_1, t.TryGetOutputColumn())

        def update_datamap(data_name_function_2: Callable[[Data], str], dm: Datamap) -> None:
            def action(c_1: DataContext, data_name_function_2: Any=data_name_function_2, dm: Any=dm) -> None:
                if c_1.FilePath is not None:
                    new_file_path_1: str = data_name_function_2(c_1)
                    c_1.FilePath = new_file_path_1


            iterate(action, dm.DataContexts)

        def action_2(s: ArcStudy) -> None:
            def f_1(d: Data, s: Any=s) -> str:
                return d.GetAbsolutePathForStudy(s.Identifier, check_existence_from_root)

            source_1: Array[ArcTable] = s.Tables
            iterate(curry2(update_table)(f_1), source_1)
            if s.Datamap is not None:
                update_datamap(f_1, value_9(s.Datamap))


        iterate(action_2, this.Studies)
        def action_4(a_1: ArcAssay) -> None:
            def f_2(d_1: Data, a_1: Any=a_1) -> str:
                return d_1.GetAbsolutePathForAssay(a_1.Identifier, check_existence_from_root)

            source_3: Array[ArcTable] = a_1.Tables
            iterate(curry2(update_table)(f_2), source_3)
            if a_1.Datamap is not None:
                update_datamap(f_2, value_9(a_1.Datamap))


        iterate(action_4, this.Assays)

    @staticmethod
    def from_file_paths(file_paths: Array[str]) -> ARC:
        fs: FileSystem = FileSystem.from_file_paths(file_paths)
        return ARC(create_missing_identifier(), None, None, None, None, None, None, None, None, None, None, None, None, None, None, fs)

    def SetFilePaths(self, file_paths: Array[str]) -> None:
        this: ARC = self
        tree: FileSystemTree = FileSystemTree.from_file_paths(file_paths)
        this._fs = FileSystem(tree, this._fs.History)

    def GetReadContracts(self, __unit: None=None) -> Array[Contract]:
        this: ARC = self
        return choose(try_isaread_contract_from_path, this._fs.Tree.ToFilePaths(), None)

    def SetISAFromContracts(self, contracts: Array[Contract]) -> None:
        this: ARC = self
        investigation: ArcInvestigation = ARCAux_getArcInvestigationFromContracts(contracts)
        ignore(set_investigation_identifier(investigation.Identifier, this))
        this.Title = investigation.Title
        this.Description = investigation.Description
        this.SubmissionDate = investigation.SubmissionDate
        this.PublicReleaseDate = investigation.PublicReleaseDate
        this.OntologySourceReferences = investigation.OntologySourceReferences
        this.Publications = investigation.Publications
        this.Contacts = investigation.Contacts
        this.Comments = investigation.Comments
        this.Remarks = investigation.Remarks
        this.RegisteredStudyIdentifiers = investigation.RegisteredStudyIdentifiers
        def mapping(tuple: tuple[ArcStudy, FSharpList[ArcAssay]]) -> ArcStudy:
            return tuple[0]

        studies: Array[ArcStudy] = map(mapping, ARCAux_getArcStudiesFromContracts(contracts), None)
        assays: Array[ArcAssay] = ARCAux_getArcAssaysFromContracts(contracts)
        workflows: Array[ArcWorkflow] = ARCAux_getArcWorkflowsFromContracts(contracts)
        runs: Array[ArcRun] = ARCAux_getArcRunsFromContracts(contracts)
        license: License | None = ARCAux_getLicenseFromContracts(contracts)
        def action(ai: str) -> None:
            def predicate(a: ArcAssay, ai: Any=ai) -> bool:
                return a.Identifier == ai

            if not exists(predicate, assays):
                this.DeleteAssay(ai)


        iterate_1(action, this.AssayIdentifiers)
        def action_1(si: str) -> None:
            def predicate_1(s: ArcStudy, si: Any=si) -> bool:
                return s.Identifier == si

            if not exists(predicate_1, studies):
                this.DeleteStudy(si)


        iterate_1(action_1, this.StudyIdentifiers)
        def action_2(study: ArcStudy) -> None:
            def predicate_2(s_1: ArcStudy, study: Any=study) -> bool:
                return s_1.Identifier == study.Identifier

            registered_study_opt: ArcStudy | None = try_find(predicate_2, this.Studies)
            if registered_study_opt is None:
                this.AddStudy(study)

            else: 
                registered_study: ArcStudy = registered_study_opt
                registered_study.UpdateReferenceByStudyFile(study, True)

            datamap: Datamap | None = ARCAux_getStudyDatamapFromContracts(study.Identifier, contracts)
            if study.Datamap is None:
                study.Datamap = datamap

            study.StaticHash = study.GetLightHashCode() or 0

        iterate_1(action_2, studies)
        def action_3(assay: ArcAssay) -> None:
            def predicate_3(a_1: ArcAssay, assay: Any=assay) -> bool:
                return a_1.Identifier == assay.Identifier

            registered_assay_opt: ArcAssay | None = try_find(predicate_3, this.Assays)
            if registered_assay_opt is None:
                this.AddAssay(assay)

            else: 
                registered_assay: ArcAssay = registered_assay_opt
                registered_assay.UpdateReferenceByAssayFile(assay, True)

            def predicate_4(a_2: ArcAssay, assay: Any=assay) -> bool:
                return a_2.Identifier == assay.Identifier

            assay_1: ArcAssay = find(predicate_4, this.Assays)
            updated_tables: ArcTables
            array_6: Array[ArcStudy] = assay_1.StudiesRegisteredIn
            def folder(tables: ArcTables, study_1: ArcStudy, assay: Any=assay) -> ArcTables:
                return ArcTables.update_reference_tables_by_sheets(ArcTables(study_1.Tables), tables, False)

            updated_tables = fold(folder, ArcTables(assay_1.Tables), array_6)
            datamap_1: Datamap | None = ARCAux_getAssayDatamapFromContracts(assay_1.Identifier, contracts)
            if assay_1.Datamap is None:
                assay_1.Datamap = datamap_1

            assay_1.Tables = updated_tables.Tables

        iterate_1(action_3, assays)
        def action_4(workflow: ArcWorkflow) -> None:
            datamap_2: Datamap | None = ARCAux_getWorkflowDatamapFromContracts(workflow.Identifier, contracts)
            cwl: CWLProcessingUnit | None = ARCAux_getWorkflowCWLFromContracts(workflow.Identifier, contracts)
            if workflow.Datamap is None:
                workflow.Datamap = datamap_2

            workflow.CWLDescription = cwl
            this.AddWorkflow(workflow)
            workflow.StaticHash = workflow.GetLightHashCode() or 0

        iterate_1(action_4, workflows)
        def action_5(run: ArcRun) -> None:
            datamap_3: Datamap | None = ARCAux_getRunDatamapFromContracts(run.Identifier, contracts)
            cwl_1: CWLProcessingUnit | None = ARCAux_getRunCWLFromContracts(run.Identifier, contracts)
            yml: Array[CWLParameterReference] | None = ARCAux_getRunYMLFromContracts(run.Identifier, contracts)
            if run.Datamap is None:
                run.Datamap = datamap_3

            run.CWLInput = default_arg(yml, [])
            run.CWLDescription = cwl_1
            this.AddRun(run)
            run.StaticHash = run.GetLightHashCode() or 0

        iterate_1(action_5, runs)
        def action_6(a_3: ArcAssay) -> None:
            a_3.StaticHash = a_3.GetLightHashCode() or 0

        iterate(action_6, this.Assays)
        def action_7(s_2: ArcStudy) -> None:
            s_2.StaticHash = s_2.GetLightHashCode() or 0

        iterate(action_7, this.Studies)
        this.License = license
        this.StaticHash = this.GetLightHashCode() or 0

    def UpdateFileSystem(self, __unit: None=None) -> None:
        this: ARC = self
        new_fs: FileSystem = ARCAux_updateFSByARC(this, this._license, this._fs)
        this._fs = new_fs

    def GetWriteContracts(self, skip_update_fs: bool | None=None) -> Array[Contract]:
        this: ARC = self
        if not default_arg(skip_update_fs, False):
            this.UpdateFileSystem()

        filemap: Any = dict([])
        add_to_dict(filemap, "isa.investigation.xlsx", (DTOType(4), DTO(0, ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF(this))))
        this.StaticHash = this.GetLightHashCode() or 0
        def action(s: ArcStudy) -> None:
            s.StaticHash = s.GetLightHashCode() or 0
            add_to_dict(filemap, Study_fileNameFromIdentifier(s.Identifier), (DTOType(1), DTO(0, ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522(s))))
            if s.Datamap is not None:
                dm: Datamap = value_9(s.Datamap)
                dm.StaticHash = safe_hash(dm) or 0
                add_to_dict(filemap, Study_datamapFileNameFromIdentifier(s.Identifier), (DTOType(5), DTO(0, to_fs_workbook(dm))))


        iterate(action, this.Studies)
        def action_1(a: ArcAssay) -> None:
            a.StaticHash = a.GetLightHashCode() or 0
            add_to_dict(filemap, Assay_fileNameFromIdentifier(a.Identifier), (DTOType(0), DTO(0, ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F(a))))
            if a.Datamap is not None:
                dm_1: Datamap = value_9(a.Datamap)
                dm_1.StaticHash = safe_hash(dm_1) or 0
                add_to_dict(filemap, Assay_datamapFileNameFromIdentifier(a.Identifier), (DTOType(5), DTO(0, to_fs_workbook(dm_1))))


        iterate(action_1, this.Assays)
        def action_2(w: ArcWorkflow) -> None:
            w.StaticHash = w.GetLightHashCode() or 0
            add_to_dict(filemap, Workflow_fileNameFromIdentifier(w.Identifier), (DTOType(2), DTO(0, ARCtrl_ArcWorkflow__ArcWorkflow_toFsWorkbook_Static_Z1C75CB0E(w))))
            if w.CWLDescription is not None:
                raise Exception("Not implemented yet: CWL description in ARC.GetWriteContracts")

            if w.Datamap is not None:
                dm_2: Datamap = value_9(w.Datamap)
                dm_2.StaticHash = safe_hash(dm_2) or 0
                add_to_dict(filemap, Workflow_datamapFileNameFromIdentifier(w.Identifier), (DTOType(5), DTO(0, to_fs_workbook(dm_2))))


        iterate(action_2, this.Workflows)
        def action_3(r: ArcRun) -> None:
            r.StaticHash = r.GetLightHashCode() or 0
            add_to_dict(filemap, Run_fileNameFromIdentifier(r.Identifier), (DTOType(3), DTO(0, ARCtrl_ArcRun__ArcRun_toFsWorkbook_Static_Z3EFAF6F8(r))))
            if r.CWLDescription is not None:
                raise Exception("Not implemented yet: CWL description in ARC.GetWriteContracts")

            if len(r.CWLInput) > 0:
                raise Exception("Not implemented yet: CWL YAML input in ARC.GetWriteContracts")

            if r.Datamap is not None:
                dm_3: Datamap = value_9(r.Datamap)
                dm_3.StaticHash = safe_hash(dm_3) or 0
                add_to_dict(filemap, Run_datamapFileNameFromIdentifier(r.Identifier), (DTOType(5), DTO(0, to_fs_workbook(dm_3))))


        iterate(action_3, this.Runs)
        match_value: License | None = this.License
        if match_value is None:
            pass

        else: 
            l: License = match_value
            match_value_1: str = l.Type
            l.StaticHash = safe_hash(l) or 0
            add_to_dict(filemap, l.Path, (DTOType(10), DTO(1, l.Content)))

        def mapping(fp: str) -> Contract:
            match_value_2: tuple[DTOType, DTO] | None = Dictionary_tryGet(fp, filemap)
            if match_value_2 is None:
                return Contract.create_create(fp, DTOType(10))

            else: 
                wb: DTO = match_value_2[1]
                dto: DTOType = match_value_2[0]
                return Contract.create_create(fp, dto, wb)


        return map(mapping, this._fs.Tree.ToFilePaths(True), None)

    def GetUpdateContracts(self, skip_update_fs: bool | None=None) -> Array[Contract]:
        this: ARC = self
        if this.StaticHash == 0:
            this.StaticHash = this.GetLightHashCode() or 0
            return this.GetWriteContracts(skip_update_fs)

        else: 
            def _arrow4186(__unit: None=None) -> IEnumerable_1[Contract]:
                hash_1: int = this.GetLightHashCode() or 0
                def _arrow4185(__unit: None=None) -> IEnumerable_1[Contract]:
                    this.StaticHash = hash_1 or 0
                    def _arrow4161(s: ArcStudy) -> IEnumerable_1[Contract]:
                        hash_2: int = s.GetLightHashCode() or 0
                        def _arrow4160(__unit: None=None) -> IEnumerable_1[Contract]:
                            s.StaticHash = hash_2 or 0
                            match_value: Datamap | None = s.Datamap
                            (pattern_matching_result, dm_2, dm_3) = (None, None, None)
                            if match_value is not None:
                                def _arrow4158(__unit: None=None) -> bool:
                                    dm: Datamap = match_value
                                    return dm.StaticHash == 0

                                if _arrow4158():
                                    pattern_matching_result = 0
                                    dm_2 = match_value

                                else: 
                                    def _arrow4159(__unit: None=None) -> bool:
                                        dm_1: Datamap = match_value
                                        return dm_1.StaticHash != safe_hash(dm_1)

                                    if _arrow4159():
                                        pattern_matching_result = 1
                                        dm_3 = match_value

                                    else: 
                                        pattern_matching_result = 2



                            else: 
                                pattern_matching_result = 2

                            if pattern_matching_result == 0:
                                def _arrow4156(__unit: None=None) -> IEnumerable_1[Contract]:
                                    dm_2.StaticHash = safe_hash(dm_2) or 0
                                    return empty()

                                return append(singleton_1(ARCtrl_Datamap__Datamap_ToCreateContractForStudy_Z721C83C5(dm_2, s.Identifier)), delay(_arrow4156))

                            elif pattern_matching_result == 1:
                                def _arrow4157(__unit: None=None) -> IEnumerable_1[Contract]:
                                    dm_3.StaticHash = safe_hash(dm_3) or 0
                                    return empty()

                                return append(singleton_1(ARCtrl_Datamap__Datamap_ToUpdateContractForStudy_Z721C83C5(dm_3, s.Identifier)), delay(_arrow4157))

                            elif pattern_matching_result == 2:
                                return empty()


                        return append(ARCtrl_ArcStudy__ArcStudy_ToCreateContract_6FCE9E49(s, True) if (s.StaticHash == 0) else (singleton_1(ARCtrl_ArcStudy__ArcStudy_ToUpdateContract(s)) if (s.StaticHash != hash_2) else empty()), delay(_arrow4160))

                    def _arrow4184(__unit: None=None) -> IEnumerable_1[Contract]:
                        def _arrow4167(a: ArcAssay) -> IEnumerable_1[Contract]:
                            hash_3: int = a.GetLightHashCode() or 0
                            def _arrow4166(__unit: None=None) -> IEnumerable_1[Contract]:
                                a.StaticHash = hash_3 or 0
                                match_value_1: Datamap | None = a.Datamap
                                (pattern_matching_result_1, dm_6, dm_7) = (None, None, None)
                                if match_value_1 is not None:
                                    def _arrow4164(__unit: None=None) -> bool:
                                        dm_4: Datamap = match_value_1
                                        return dm_4.StaticHash == 0

                                    if _arrow4164():
                                        pattern_matching_result_1 = 0
                                        dm_6 = match_value_1

                                    else: 
                                        def _arrow4165(__unit: None=None) -> bool:
                                            dm_5: Datamap = match_value_1
                                            return dm_5.StaticHash != safe_hash(dm_5)

                                        if _arrow4165():
                                            pattern_matching_result_1 = 1
                                            dm_7 = match_value_1

                                        else: 
                                            pattern_matching_result_1 = 2



                                else: 
                                    pattern_matching_result_1 = 2

                                if pattern_matching_result_1 == 0:
                                    def _arrow4162(__unit: None=None) -> IEnumerable_1[Contract]:
                                        dm_6.StaticHash = safe_hash(dm_6) or 0
                                        return empty()

                                    return append(singleton_1(ARCtrl_Datamap__Datamap_ToCreateContractForAssay_Z721C83C5(dm_6, a.Identifier)), delay(_arrow4162))

                                elif pattern_matching_result_1 == 1:
                                    def _arrow4163(__unit: None=None) -> IEnumerable_1[Contract]:
                                        dm_7.StaticHash = safe_hash(dm_7) or 0
                                        return empty()

                                    return append(singleton_1(ARCtrl_Datamap__Datamap_ToUpdateContractForAssay_Z721C83C5(dm_7, a.Identifier)), delay(_arrow4163))

                                elif pattern_matching_result_1 == 2:
                                    return empty()


                            return append(ARCtrl_ArcAssay__ArcAssay_ToCreateContract_6FCE9E49(a, True) if (a.StaticHash == 0) else (singleton_1(ARCtrl_ArcAssay__ArcAssay_ToUpdateContract(a)) if (a.StaticHash != hash_3) else empty()), delay(_arrow4166))

                        def _arrow4183(__unit: None=None) -> IEnumerable_1[Contract]:
                            def _arrow4173(w: ArcWorkflow) -> IEnumerable_1[Contract]:
                                hash_4: int = w.GetLightHashCode() or 0
                                def _arrow4172(__unit: None=None) -> IEnumerable_1[Contract]:
                                    w.StaticHash = hash_4 or 0
                                    match_value_2: Datamap | None = w.Datamap
                                    (pattern_matching_result_2, dm_10, dm_11) = (None, None, None)
                                    if match_value_2 is not None:
                                        def _arrow4170(__unit: None=None) -> bool:
                                            dm_8: Datamap = match_value_2
                                            return dm_8.StaticHash == 0

                                        if _arrow4170():
                                            pattern_matching_result_2 = 0
                                            dm_10 = match_value_2

                                        else: 
                                            def _arrow4171(__unit: None=None) -> bool:
                                                dm_9: Datamap = match_value_2
                                                return dm_9.StaticHash != safe_hash(dm_9)

                                            if _arrow4171():
                                                pattern_matching_result_2 = 1
                                                dm_11 = match_value_2

                                            else: 
                                                pattern_matching_result_2 = 2



                                    else: 
                                        pattern_matching_result_2 = 2

                                    if pattern_matching_result_2 == 0:
                                        def _arrow4168(__unit: None=None) -> IEnumerable_1[Contract]:
                                            dm_10.StaticHash = safe_hash(dm_10) or 0
                                            return empty()

                                        return append(singleton_1(ARCtrl_Datamap__Datamap_ToCreateContractForWorkflow_Z721C83C5(dm_10, w.Identifier)), delay(_arrow4168))

                                    elif pattern_matching_result_2 == 1:
                                        def _arrow4169(__unit: None=None) -> IEnumerable_1[Contract]:
                                            dm_11.StaticHash = safe_hash(dm_11) or 0
                                            return empty()

                                        return append(singleton_1(ARCtrl_Datamap__Datamap_ToUpdateContractForWorkflow_Z721C83C5(dm_11, w.Identifier)), delay(_arrow4169))

                                    elif pattern_matching_result_2 == 2:
                                        return empty()


                                return append(ARCtrl_ArcWorkflow__ArcWorkflow_ToCreateContract_6FCE9E49(w, True) if (w.StaticHash == 0) else (singleton_1(ARCtrl_ArcWorkflow__ArcWorkflow_ToUpdateContract(w)) if (w.StaticHash != hash_4) else empty()), delay(_arrow4172))

                            def _arrow4182(__unit: None=None) -> IEnumerable_1[Contract]:
                                def _arrow4179(r: ArcRun) -> IEnumerable_1[Contract]:
                                    hash_5: int = r.GetLightHashCode() or 0
                                    def _arrow4178(__unit: None=None) -> IEnumerable_1[Contract]:
                                        r.StaticHash = hash_5 or 0
                                        match_value_3: Datamap | None = r.Datamap
                                        (pattern_matching_result_3, dm_14, dm_15) = (None, None, None)
                                        if match_value_3 is not None:
                                            def _arrow4176(__unit: None=None) -> bool:
                                                dm_12: Datamap = match_value_3
                                                return dm_12.StaticHash == 0

                                            if _arrow4176():
                                                pattern_matching_result_3 = 0
                                                dm_14 = match_value_3

                                            else: 
                                                def _arrow4177(__unit: None=None) -> bool:
                                                    dm_13: Datamap = match_value_3
                                                    return dm_13.StaticHash != safe_hash(dm_13)

                                                if _arrow4177():
                                                    pattern_matching_result_3 = 1
                                                    dm_15 = match_value_3

                                                else: 
                                                    pattern_matching_result_3 = 2



                                        else: 
                                            pattern_matching_result_3 = 2

                                        if pattern_matching_result_3 == 0:
                                            def _arrow4174(__unit: None=None) -> IEnumerable_1[Contract]:
                                                dm_14.StaticHash = safe_hash(dm_14) or 0
                                                return empty()

                                            return append(singleton_1(ARCtrl_Datamap__Datamap_ToCreateContractForRun_Z721C83C5(dm_14, r.Identifier)), delay(_arrow4174))

                                        elif pattern_matching_result_3 == 1:
                                            def _arrow4175(__unit: None=None) -> IEnumerable_1[Contract]:
                                                dm_15.StaticHash = safe_hash(dm_15) or 0
                                                return empty()

                                            return append(singleton_1(ARCtrl_Datamap__Datamap_ToUpdateContractForRun_Z721C83C5(dm_15, r.Identifier)), delay(_arrow4175))

                                        elif pattern_matching_result_3 == 2:
                                            return empty()


                                    return append(ARCtrl_ArcRun__ArcRun_ToCreateContract_6FCE9E49(r, True) if (r.StaticHash == 0) else (singleton_1(ARCtrl_ArcRun__ArcRun_ToUpdateContract(r)) if (r.StaticHash != hash_5) else empty()), delay(_arrow4178))

                                def _arrow4181(__unit: None=None) -> IEnumerable_1[Contract]:
                                    match_value_4: License | None = this.License
                                    if match_value_4 is None:
                                        return empty()

                                    else: 
                                        l: License = match_value_4
                                        hash_6: int = safe_hash(l) or 0
                                        def _arrow4180(__unit: None=None) -> IEnumerable_1[Contract]:
                                            l.StaticHash = hash_6 or 0
                                            return empty()

                                        return append(singleton_1(l.ToCreateContract()) if (l.StaticHash == 0) else (singleton_1(l.ToUpdateContract()) if (l.StaticHash != hash_6) else empty()), delay(_arrow4180))


                                return append(collect(_arrow4179, this.Runs), delay(_arrow4181))

                            return append(collect(_arrow4173, this.Workflows), delay(_arrow4182))

                        return append(collect(_arrow4167, this.Assays), delay(_arrow4183))

                    return append(collect(_arrow4161, this.Studies), delay(_arrow4184))

                return append(singleton_1(ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract(this)) if (this.StaticHash != hash_1) else empty(), delay(_arrow4185))

            return to_array(delay(_arrow4186))


    def GetGitInitContracts(self, branch: str | None=None, repository_address: str | None=None, default_gitignore: bool | None=None, default_gitattributes: bool | None=None) -> Array[Contract]:
        default_gitignore_1: bool = default_arg(default_gitignore, False)
        default_gitattributes_1: bool = default_arg(default_gitattributes, False)
        def _arrow4190(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow4189(__unit: None=None) -> IEnumerable_1[Contract]:
                def _arrow4188(__unit: None=None) -> IEnumerable_1[Contract]:
                    def _arrow4187(__unit: None=None) -> IEnumerable_1[Contract]:
                        return singleton_1(Init_createAddRemoteContract_Z721C83C5(value_9(repository_address))) if (repository_address is not None) else empty()

                    return append(singleton_1(gitattributes_contract) if default_gitattributes_1 else empty(), delay(_arrow4187))

                return append(singleton_1(gitignore_contract) if default_gitignore_1 else empty(), delay(_arrow4188))

            return append(singleton_1(Init_createInitContract_6DFDD678(branch)), delay(_arrow4189))

        return to_array(delay(_arrow4190))

    @staticmethod
    def get_clone_contract(remote_url: str, merge: bool | None=None, branch: str | None=None, token: tuple[str, str] | None=None, nolfs: bool | None=None) -> Contract:
        return Clone_createCloneContract_5000466F(remote_url, merge, branch, token, nolfs)

    def Copy(self, __unit: None=None) -> ARC:
        this: ARC = self
        next_assays: Array[ArcAssay] = []
        next_studies: Array[ArcStudy] = []
        next_workflows: Array[ArcWorkflow] = []
        next_runs: Array[ArcRun] = []
        enumerator: Any = get_enumerator(this.Assays)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                assay: ArcAssay = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                copy: ArcAssay = assay.Copy()
                (next_assays.append(copy))

        finally: 
            dispose(enumerator)

        enumerator_1: Any = get_enumerator(this.Studies)
        try: 
            while enumerator_1.System_Collections_IEnumerator_MoveNext():
                study: ArcStudy = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                copy_1: ArcStudy = study.Copy()
                (next_studies.append(copy_1))

        finally: 
            dispose(enumerator_1)

        enumerator_2: Any = get_enumerator(this.Workflows)
        try: 
            while enumerator_2.System_Collections_IEnumerator_MoveNext():
                workflow: ArcWorkflow = enumerator_2.System_Collections_Generic_IEnumerator_1_get_Current()
                copy_2: ArcWorkflow = workflow.Copy()
                (next_workflows.append(copy_2))

        finally: 
            dispose(enumerator_2)

        enumerator_3: Any = get_enumerator(this.Runs)
        try: 
            while enumerator_3.System_Collections_IEnumerator_MoveNext():
                run: ArcRun = enumerator_3.System_Collections_Generic_IEnumerator_1_get_Current()
                copy_3: ArcRun = run.Copy()
                (next_runs.append(copy_3))

        finally: 
            dispose(enumerator_3)

        def f(c: Comment) -> Comment:
            return c.Copy()

        next_comments: Array[Comment] = ResizeArray_map(f, this.Comments)
        def f_1(c_1: Remark) -> Remark:
            return c_1.Copy()

        next_remarks: Array[Remark] = ResizeArray_map(f_1, this.Remarks)
        def f_2(c_2: Person) -> Person:
            return c_2.Copy()

        next_contacts: Array[Person] = ResizeArray_map(f_2, this.Contacts)
        def f_3(c_3: Publication) -> Publication:
            return c_3.Copy()

        next_publications: Array[Publication] = ResizeArray_map(f_3, this.Publications)
        def f_4(c_4: OntologySourceReference) -> OntologySourceReference:
            return c_4.Copy()

        next_ontology_source_references: Array[OntologySourceReference] = ResizeArray_map(f_4, this.OntologySourceReferences)
        next_study_identifiers: Array[str] = list(this.RegisteredStudyIdentifiers)
        def mapping(_arg: License) -> License:
            return _arg.Copy()

        next_license: License | None = map_1(mapping, this.License)
        fs_copy: FileSystem = this._fs.Copy()
        return ARC(this.Identifier, this.Title, this.Description, this.SubmissionDate, this.PublicReleaseDate, next_ontology_source_references, next_publications, next_contacts, next_assays, next_studies, next_workflows, next_runs, next_study_identifiers, next_comments, next_remarks, fs_copy, next_license)

    def GetRegisteredPayload(self, IgnoreHidden: bool | None=None) -> FileSystemTree:
        this: ARC = self
        copy: ARC = this.Copy()
        registered_studies: Array[ArcStudy] = copy.Studies[:]
        def mapping(s: ArcStudy) -> Array[ArcAssay]:
            return s.RegisteredAssays[:]

        registered_assays: Array[ArcAssay] = concat(map(mapping, registered_studies, None), None)
        def _arrow4193(__unit: None=None) -> IEnumerable_1[str]:
            def _arrow4192(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow4191(__unit: None=None) -> IEnumerable_1[str]:
                    return singleton_1(value_9(this.License).Path) if (this.License is not None) else empty()

                return append(singleton_1("README.md"), delay(_arrow4191))

            return append(singleton_1("isa.investigation.xlsx"), delay(_arrow4192))

        class ObjectExpr4194:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        def mapping_1(s_1: ArcStudy) -> Any:
            study_foldername: str = ((("" + "studies") + "/") + s_1.Identifier) + ""
            def _arrow4201(__unit: None=None, s_1: Any=s_1) -> IEnumerable_1[str]:
                def _arrow4200(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow4199(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow4198(table: ArcTable) -> IEnumerable_1[str]:
                            def _arrow4197(kv: Any) -> IEnumerable_1[str]:
                                text_value: str = kv[1].ToFreeTextCell().AsFreeText
                                def _arrow4196(__unit: None=None) -> IEnumerable_1[str]:
                                    def _arrow4195(__unit: None=None) -> IEnumerable_1[str]:
                                        return singleton_1(((((("" + study_foldername) + "/") + "protocols") + "/") + text_value) + "")

                                    return append(singleton_1(((((("" + study_foldername) + "/") + "resources") + "/") + text_value) + ""), delay(_arrow4195))

                                return append(singleton_1(text_value), delay(_arrow4196))

                            return collect(_arrow4197, table.Values)

                        return collect(_arrow4198, s_1.Tables)

                    return append(singleton_1(((("" + study_foldername) + "/") + "README.md") + ""), delay(_arrow4199))

                return append(singleton_1(((("" + study_foldername) + "/") + "isa.study.xlsx") + ""), delay(_arrow4200))

            class ObjectExpr4202:
                @property
                def Compare(self) -> Callable[[str, str], int]:
                    return compare_primitives

            return of_seq(to_list(delay(_arrow4201)), ObjectExpr4202())

        class ObjectExpr4203:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        def mapping_2(a: ArcAssay) -> Any:
            assay_foldername: str = ((("" + "assays") + "/") + a.Identifier) + ""
            def _arrow4210(__unit: None=None, a: Any=a) -> IEnumerable_1[str]:
                def _arrow4209(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow4208(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow4207(table_1: ArcTable) -> IEnumerable_1[str]:
                            def _arrow4206(kv_1: Any) -> IEnumerable_1[str]:
                                text_value_1: str = kv_1[1].ToFreeTextCell().AsFreeText
                                def _arrow4205(__unit: None=None) -> IEnumerable_1[str]:
                                    def _arrow4204(__unit: None=None) -> IEnumerable_1[str]:
                                        return singleton_1(((((("" + assay_foldername) + "/") + "protocols") + "/") + text_value_1) + "")

                                    return append(singleton_1(((((("" + assay_foldername) + "/") + "dataset") + "/") + text_value_1) + ""), delay(_arrow4204))

                                return append(singleton_1(text_value_1), delay(_arrow4205))

                            return collect(_arrow4206, table_1.Values)

                        return collect(_arrow4207, a.Tables)

                    return append(singleton_1(((("" + assay_foldername) + "/") + "README.md") + ""), delay(_arrow4208))

                return append(singleton_1(((("" + assay_foldername) + "/") + "isa.assay.xlsx") + ""), delay(_arrow4209))

            class ObjectExpr4211:
                @property
                def Compare(self) -> Callable[[str, str], int]:
                    return compare_primitives

            return of_seq(to_list(delay(_arrow4210)), ObjectExpr4211())

        class ObjectExpr4212:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        class ObjectExpr4213:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        include_files: Any = union_many(to_enumerable([of_seq(to_list(delay(_arrow4193)), ObjectExpr4194()), union_many(map(mapping_1, registered_studies, None), ObjectExpr4203()), union_many(map(mapping_2, registered_assays, None), ObjectExpr4212())]), ObjectExpr4213())
        ignore_hidden: bool = default_arg(IgnoreHidden, True)
        fs_copy: FileSystem = this._fs.Copy()
        def binder(tree_1: FileSystemTree) -> FileSystemTree | None:
            if ignore_hidden:
                def _arrow4214(n_1: str, tree_1: Any=tree_1) -> bool:
                    return not starts_with_exact(n_1, ".")

                return FileSystemTree.filter_folders(_arrow4214)(tree_1)

            else: 
                return tree_1


        def _arrow4216(__unit: None=None) -> FileSystemTree | None:
            tree: FileSystemTree
            def predicate(p: str) -> bool:
                if True if starts_with_exact(p, "workflows") else starts_with_exact(p, "runs"):
                    return True

                else: 
                    return FSharpSet__Contains(include_files, p)


            paths: Array[str] = filter(predicate, FileSystemTree.to_file_paths()(fs_copy.Tree))
            tree = FileSystemTree.from_file_paths(paths)
            def _arrow4215(n: str) -> bool:
                return not starts_with_exact(n, ".")

            return FileSystemTree.filter_files(_arrow4215)(tree) if ignore_hidden else tree

        return default_arg(bind(binder, _arrow4216()), FileSystemTree.from_file_paths([]))

    def GetAdditionalPayload(self, IgnoreHidden: bool | None=None) -> FileSystemTree:
        this: ARC = self
        ignore_hidden: bool = default_arg(IgnoreHidden, True)
        class ObjectExpr4217:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        registered_payload: Any = of_seq(FileSystemTree.to_file_paths()(this.GetRegisteredPayload()), ObjectExpr4217())
        def binder(tree_1: FileSystemTree) -> FileSystemTree | None:
            if ignore_hidden:
                def _arrow4218(n_1: str, tree_1: Any=tree_1) -> bool:
                    return not starts_with_exact(n_1, ".")

                return FileSystemTree.filter_folders(_arrow4218)(tree_1)

            else: 
                return tree_1


        def _arrow4220(__unit: None=None) -> FileSystemTree | None:
            tree: FileSystemTree
            def predicate(p: str) -> bool:
                return not FSharpSet__Contains(registered_payload, p)

            paths: Array[str] = filter(predicate, FileSystemTree.to_file_paths()(this._fs.Copy().Tree))
            tree = FileSystemTree.from_file_paths(paths)
            def _arrow4219(n: str) -> bool:
                return not starts_with_exact(n, ".")

            return FileSystemTree.filter_files(_arrow4219)(tree) if ignore_hidden else tree

        return default_arg(bind(binder, _arrow4220()), FileSystemTree.from_file_paths([]))

    @staticmethod
    def DefaultContracts() -> Any:
        class ObjectExpr4221:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        return of_seq_1(to_enumerable([(".gitignore", gitignore_contract), (".gitattributes", gitattributes_contract)]), ObjectExpr4221())

    @staticmethod
    def from_deprecated_rocrate_json_string(s: str) -> ARC:
        try: 
            s_1: str = replace(s, "bio:additionalProperty", "sdo:additionalProperty")
            isa: ArcInvestigation
            match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(ROCrate_get_decoderDeprecated(), s_1)
            if match_value.tag == 1:
                raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

            else: 
                isa = match_value.fields[0]

            return ARC.from_arc_investigation(isa)

        except Exception as ex:
            arg_1: str = str(ex)
            return to_fail(printf("Could not parse deprecated ARC-RO-Crate metadata: \n%s"))(arg_1)


    @staticmethod
    def from_rocrate_json_string(s: str) -> ARC:
        try: 
            pattern_input: tuple[ArcInvestigation, Array[str], License | None]
            match_value: FSharpResult_2[tuple[ArcInvestigation, Array[str], License | None], str] = Decode_fromString(ROCrate_get_decoder(), s)
            if match_value.tag == 1:
                raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

            else: 
                pattern_input = match_value.fields[0]

            file_system: FileSystem
            paths: Array[str] = list(pattern_input[1])
            file_system = FileSystem.from_file_paths(paths)
            return ARC.from_arc_investigation(pattern_input[0], file_system, pattern_input[2])

        except Exception as ex:
            arg_1: str = str(ex)
            return to_fail(printf("Could not parse ARC-RO-Crate metadata: \n%s"))(arg_1)


    def ToROCrateJsonString(self, spaces: int | None=None) -> str:
        this: ARC = self
        this.MakeDataFilesAbsolute()
        value: IEncodable = ROCrate_encoder_1E8A3F74(this, this._license, this._fs)
        return to_string(default_spaces(spaces), value)

    @staticmethod
    def to_rocrate_json_string(spaces: int | None=None) -> Callable[[ARC], str]:
        def _arrow4222(obj: ARC) -> str:
            return obj.ToROCrateJsonString(spaces)

        return _arrow4222

    def GetLicenseWriteContract(self, __unit: None=None) -> Contract:
        this: ARC = self
        def def_thunk(__unit: None=None) -> License:
            return License.GetDefaultLicense()

        _arg: License = default_arg_with(this.License, def_thunk)
        return _arg.ToCreateContract()

    def GetValidationPackagesConfigWriteContract(self, vpc: ValidationPackagesConfig) -> Contract:
        this: ARC = self
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        class ObjectExpr4224:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow4223(x: str, y: str) -> bool:
                    return x == y

                return _arrow4223

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if not contains_2(ValidationPackagesConfigHelper_ConfigFilePath, paths, ObjectExpr4224()):
            file_paths: Array[str] = append_1([ValidationPackagesConfigHelper_ConfigFilePath], paths, None)
            this.SetFilePaths(file_paths)

        return ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toCreateContract_Static_724DAE55(vpc)

    def GetValidationPackagesConfigDeleteContract(self, vpc: ValidationPackagesConfig) -> Contract:
        this: ARC = self
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        class ObjectExpr4226:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow4225(x: str, y: str) -> bool:
                    return x == y

                return _arrow4225

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if contains_2(ValidationPackagesConfigHelper_ConfigFilePath, paths, ObjectExpr4226()):
            def predicate(p: str) -> bool:
                return not (p == ValidationPackagesConfigHelper_ConfigFilePath)

            file_paths: Array[str] = filter(predicate, paths)
            this.SetFilePaths(file_paths)

        return ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_toDeleteContract_Static_724DAE55(vpc)

    def GetValidationPackagesConfigReadContract(self, __unit: None=None) -> Contract:
        return ValidationPackagesConfigHelper_ReadContract

    def GetValidationPackagesConfigFromReadContract(self, contract: Contract) -> ValidationPackagesConfig | None:
        return ARCtrl_ValidationPackages_ValidationPackagesConfig__ValidationPackagesConfig_tryFromReadContract_Static_7570923F(contract)

    def ToFilePaths(self, remove_root: bool | None=None, skip_update_fs: bool | None=None) -> Array[str]:
        this: ARC = self
        if not default_arg(skip_update_fs, False):
            this.UpdateFileSystem()

        return this.FileSystem.Tree.ToFilePaths(remove_root)


ARC_reflection = _expr4228

def ARC__ctor_Z443FB9BF(identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, ontology_source_references: Array[OntologySourceReference] | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, assays: Array[ArcAssay] | None=None, studies: Array[ArcStudy] | None=None, workflows: Array[ArcWorkflow] | None=None, runs: Array[ArcRun] | None=None, registered_study_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None, remarks: Array[Remark] | None=None, fs: FileSystem | None=None, license: License | None=None) -> ARC:
    return ARC(identifier, title, description, submission_date, public_release_date, ontology_source_references, publications, contacts, assays, studies, workflows, runs, registered_study_identifiers, comments, remarks, fs, license)


def ARCAux_getArcAssaysFromContracts(contracts: Array[Contract]) -> Array[ArcAssay]:
    def chooser(c: Contract, contracts: Any=contracts) -> ArcAssay | None:
        return ARCtrl_ArcAssay__ArcAssay_tryFromReadContract_Static_7570923F(c)

    return choose(chooser, contracts, None)


def ARCAux_getArcStudiesFromContracts(contracts: Array[Contract]) -> Array[tuple[ArcStudy, FSharpList[ArcAssay]]]:
    def chooser(c: Contract, contracts: Any=contracts) -> tuple[ArcStudy, FSharpList[ArcAssay]] | None:
        return ARCtrl_ArcStudy__ArcStudy_tryFromReadContract_Static_7570923F(c)

    return choose(chooser, contracts, None)


def ARCAux_getArcWorkflowsFromContracts(contracts: Array[Contract]) -> Array[ArcWorkflow]:
    def chooser(c: Contract, contracts: Any=contracts) -> ArcWorkflow | None:
        return ARCtrl_ArcWorkflow__ArcWorkflow_tryFromReadContract_Static_7570923F(c)

    return choose(chooser, contracts, None)


def ARCAux_getArcRunsFromContracts(contracts: Array[Contract]) -> Array[ArcRun]:
    def chooser(c: Contract, contracts: Any=contracts) -> ArcRun | None:
        return ARCtrl_ArcRun__ArcRun_tryFromReadContract_Static_7570923F(c)

    return choose(chooser, contracts, None)


def ARCAux_getAssayDatamapFromContracts(assay_identifier: str, contracts: Array[Contract]) -> Datamap | None:
    def chooser(c: Contract, assay_identifier: Any=assay_identifier, contracts: Any=contracts) -> Datamap | None:
        return ARCtrl_Datamap__Datamap_tryFromReadContractForAssay_Static(assay_identifier, c)

    return try_pick(chooser, contracts)


def ARCAux_getStudyDatamapFromContracts(study_identifier: str, contracts: Array[Contract]) -> Datamap | None:
    def chooser(c: Contract, study_identifier: Any=study_identifier, contracts: Any=contracts) -> Datamap | None:
        return ARCtrl_Datamap__Datamap_tryFromReadContractForStudy_Static(study_identifier, c)

    return try_pick(chooser, contracts)


def ARCAux_getWorkflowDatamapFromContracts(workflow_identifier: str, contracts: Array[Contract]) -> Datamap | None:
    def chooser(c: Contract, workflow_identifier: Any=workflow_identifier, contracts: Any=contracts) -> Datamap | None:
        return ARCtrl_Datamap__Datamap_tryFromReadContractForWorkflow_Static(workflow_identifier, c)

    return try_pick(chooser, contracts)


def ARCAux_getRunDatamapFromContracts(run_identifier: str, contracts: Array[Contract]) -> Datamap | None:
    def chooser(c: Contract, run_identifier: Any=run_identifier, contracts: Any=contracts) -> Datamap | None:
        return ARCtrl_Datamap__Datamap_tryFromReadContractForRun_Static(run_identifier, c)

    return try_pick(chooser, contracts)


def ARCAux_getWorkflowCWLFromContracts(workflow_identifier: str, contracts: Array[Contract]) -> CWLProcessingUnit | None:
    def chooser(c: Contract, workflow_identifier: Any=workflow_identifier, contracts: Any=contracts) -> CWLProcessingUnit | None:
        return ARCtrl_ArcWorkflow__ArcWorkflow_tryCWLFromReadContract_Static(workflow_identifier, c)

    return try_pick(chooser, contracts)


def ARCAux_getRunCWLFromContracts(run_identifier: str, contracts: Array[Contract]) -> CWLProcessingUnit | None:
    def chooser(c: Contract, run_identifier: Any=run_identifier, contracts: Any=contracts) -> CWLProcessingUnit | None:
        return ARCtrl_ArcRun__ArcRun_tryCWLFromReadContract_Static(run_identifier, c)

    return try_pick(chooser, contracts)


def ARCAux_getRunYMLFromContracts(run_identifier: str, contracts: Array[Contract]) -> Array[CWLParameterReference] | None:
    def chooser(c: Contract, run_identifier: Any=run_identifier, contracts: Any=contracts) -> Array[CWLParameterReference] | None:
        return ARCtrl_ArcRun__ArcRun_tryYMLFromReadContract_Static(run_identifier, c)

    return try_pick(chooser, contracts)


def ARCAux_getArcInvestigationFromContracts(contracts: Array[Contract]) -> ArcInvestigation:
    def chooser(c: Contract, contracts: Any=contracts) -> ArcInvestigation | None:
        return ARCtrl_ArcInvestigation__ArcInvestigation_tryFromReadContract_Static_7570923F(c)

    match_value: Array[ArcInvestigation] = choose(chooser, contracts, None)
    def _arrow4229(x: ArcInvestigation, y: ArcInvestigation, contracts: Any=contracts) -> bool:
        return equals(x, y)

    if (len(match_value) == 1) if (not equals_with(_arrow4229, match_value, None)) else False:
        return match_value[0]

    else: 
        arg: int = len(match_value) or 0
        return to_fail(printf("Could not find investigation in contracts. Expected exactly one investigation, but found %d."))(arg)



def ARCAux_getLicenseFromContracts(contracts: Array[Contract]) -> License | None:
    def chooser(c: Contract, contracts: Any=contracts) -> License | None:
        return License.try_from_read_contract(c)

    return try_pick(chooser, contracts)


def ARCAux_updateFSByARC(isa: ArcInvestigation, license: License | None, fs: FileSystem) -> FileSystem:
    assays_folder: FileSystemTree
    def mapping(a: ArcAssay, isa: Any=isa, license: Any=license, fs: Any=fs) -> FileSystemTree:
        return FileSystemTree.create_assay_folder(a.Identifier, a.Datamap is not None)

    assays: Array[FileSystemTree] = map(mapping, to_array(isa.Assays), None)
    assays_folder = FileSystemTree.create_assays_folder(assays)
    studies_folder: FileSystemTree
    def mapping_1(s: ArcStudy, isa: Any=isa, license: Any=license, fs: Any=fs) -> FileSystemTree:
        return FileSystemTree.create_study_folder(s.Identifier, s.Datamap is not None)

    studies: Array[FileSystemTree] = map(mapping_1, to_array(isa.Studies), None)
    studies_folder = FileSystemTree.create_studies_folder(studies)
    workflows_folder: FileSystemTree
    def mapping_2(w: ArcWorkflow, isa: Any=isa, license: Any=license, fs: Any=fs) -> FileSystemTree:
        return FileSystemTree.create_workflow_folder(w.Identifier, w.CWLDescription is not None, w.Datamap is not None)

    workflows: Array[FileSystemTree] = map(mapping_2, to_array(isa.Workflows), None)
    workflows_folder = FileSystemTree.create_workflows_folder(workflows)
    runs_folder: FileSystemTree
    def mapping_3(r: ArcRun, isa: Any=isa, license: Any=license, fs: Any=fs) -> FileSystemTree:
        return FileSystemTree.create_run_folder(r.Identifier, r.CWLDescription is not None, len(r.CWLInput) > 0, r.Datamap is not None)

    runs: Array[FileSystemTree] = map(mapping_3, to_array(isa.Runs), None)
    runs_folder = FileSystemTree.create_runs_folder(runs)
    investigation: FileSystemTree = FileSystemTree.create_investigation_file()
    tree_1: FileSystem
    def _arrow4235(__unit: None=None, isa: Any=isa, license: Any=license, fs: Any=fs) -> IEnumerable_1[FileSystemTree]:
        def _arrow4234(__unit: None=None) -> IEnumerable_1[FileSystemTree]:
            def _arrow4233(__unit: None=None) -> IEnumerable_1[FileSystemTree]:
                def _arrow4232(__unit: None=None) -> IEnumerable_1[FileSystemTree]:
                    def _arrow4231(__unit: None=None) -> IEnumerable_1[FileSystemTree]:
                        def _arrow4230(__unit: None=None) -> IEnumerable_1[FileSystemTree]:
                            return singleton_1(FileSystemTree(0, value_9(license).Path)) if (license is not None) else empty()

                        return append(singleton_1(runs_folder), delay(_arrow4230))

                    return append(singleton_1(workflows_folder), delay(_arrow4231))

                return append(singleton_1(studies_folder), delay(_arrow4232))

            return append(singleton_1(assays_folder), delay(_arrow4233))

        return append(singleton_1(investigation), delay(_arrow4234))

    tree: FileSystemTree = FileSystemTree.create_root_folder(to_array(delay(_arrow4235)))
    tree_1 = FileSystem.create(tree = tree)
    return fs.Union(tree_1)


__all__ = ["ARC_reflection", "ARCAux_getArcAssaysFromContracts", "ARCAux_getArcStudiesFromContracts", "ARCAux_getArcWorkflowsFromContracts", "ARCAux_getArcRunsFromContracts", "ARCAux_getAssayDatamapFromContracts", "ARCAux_getStudyDatamapFromContracts", "ARCAux_getWorkflowDatamapFromContracts", "ARCAux_getRunDatamapFromContracts", "ARCAux_getWorkflowCWLFromContracts", "ARCAux_getRunCWLFromContracts", "ARCAux_getRunYMLFromContracts", "ARCAux_getArcInvestigationFromContracts", "ARCAux_getLicenseFromContracts", "ARCAux_updateFSByARC"]

