from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from ..fable_modules.fable_library.array_ import (append, map)
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.reflection import (TypeInfo, array_type, record_type)
from ..fable_modules.fable_library.types import (Array, Record)
from .commit import (Commit, Commit_reflection)
from .file_system_tree import (FileSystemTree, FileSystemTree_reflection)

def _expr441() -> TypeInfo:
    return record_type("ARCtrl.FileSystem.FileSystem", [], FileSystem, lambda: [("Tree", FileSystemTree_reflection()), ("History", array_type(Commit_reflection()))])


@dataclass(eq = False, repr = False, slots = True)
class FileSystem(Record):
    Tree: FileSystemTree
    History: Array[Commit]
    @staticmethod
    def create(tree: FileSystemTree, history: Array[Commit] | None=None) -> FileSystem:
        return FileSystem(tree, default_arg(history, []))

    def AddFile(self, path: str) -> FileSystem:
        this: FileSystem = self
        return FileSystem(this.Tree.AddFile(path), this.History)

    @staticmethod
    def add_file(path: str) -> Callable[[FileSystem], FileSystem]:
        def _arrow440(fs: FileSystem) -> FileSystem:
            return fs.AddFile(path)

        return _arrow440

    @staticmethod
    def from_file_paths(paths: Array[str]) -> FileSystem:
        tree: FileSystemTree = FileSystemTree.from_file_paths(paths)
        return FileSystem.create(tree = tree)

    def Union(self, other: FileSystem) -> FileSystem:
        this: FileSystem = self
        tree: FileSystemTree = this.Tree.Union(other.Tree)
        history: Array[Commit] = append(this.History, other.History, None)
        return FileSystem.create(tree = tree, history = history)

    def Copy(self, __unit: None=None) -> FileSystem:
        this: FileSystem = self
        fst_copy: FileSystemTree = this.Tree.Copy()
        def mapping(x: Commit) -> Commit:
            return x

        history_copy: Array[Commit] = map(mapping, this.History, None)
        return FileSystem.create(tree = fst_copy, history = history_copy)


FileSystem_reflection = _expr441

__all__ = ["FileSystem_reflection"]

