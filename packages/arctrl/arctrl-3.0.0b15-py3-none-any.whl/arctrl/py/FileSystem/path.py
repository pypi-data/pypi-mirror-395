from typing import Any
from ..fable_modules.fable_library.array_ import (filter, map_indexed, last)
from ..fable_modules.fable_library.list import (of_array, FSharpList)
from ..fable_modules.fable_library.string_ import (split as split_1, trim_end, trim_start, join, trim)
from ..fable_modules.fable_library.types import Array

seperators: Array[str] = ["/", "\\"]

alternative_licensefile_names: FSharpList[str] = of_array(["LICENSE.txt", "LICENSE.md", "LICENSE.rst"])

def split(path: str) -> Array[str]:
    def predicate(p: str, path: Any=path) -> bool:
        if p != "":
            return p != "."

        else: 
            return False


    return filter(predicate, split_1(path, seperators, None, 3))


def combine(path1: str, path2: str) -> str:
    return (trim_end(path1, *seperators) + "/") + trim_start(path2, *seperators)


def combine_many(paths: Array[str]) -> str:
    def mapping(i: int, p: str, paths: Any=paths) -> str:
        if i == 0:
            return trim_end(p, *seperators)

        elif i == (len(paths) - 1):
            return trim_start(p, *seperators)

        else: 
            return trim(p, *seperators)


    return join("/", map_indexed(mapping, paths, None))


def get_file_name(path: str) -> str:
    return last(split(path))


def is_file(file_name: str, path: str) -> bool:
    return get_file_name(path) == file_name


def get_assay_folder_path(assay_identifier: str) -> str:
    return combine("assays", assay_identifier)


def get_study_folder_path(study_identifier: str) -> str:
    return combine("studies", study_identifier)


def get_workflow_folder_path(workflow_identifier: str) -> str:
    return combine("workflows", workflow_identifier)


def get_run_folder_path(run_identifier: str) -> str:
    return combine("runs", run_identifier)


__all__ = ["seperators", "alternative_licensefile_names", "split", "combine", "combine_many", "get_file_name", "is_file", "get_assay_folder_path", "get_study_folder_path", "get_workflow_folder_path", "get_run_folder_path"]

