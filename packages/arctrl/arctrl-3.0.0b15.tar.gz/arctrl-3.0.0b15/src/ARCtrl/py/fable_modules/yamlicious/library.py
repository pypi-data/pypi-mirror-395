from __future__ import annotations
from ..fable_library.list import of_array
from .yamlicious_types import PreprocessorElement

SequenceMappingsAST: PreprocessorElement = PreprocessorElement(0, of_array([PreprocessorElement(2, "-"), PreprocessorElement(1, of_array([PreprocessorElement(2, "My Key1: My Value1"), PreprocessorElement(2, "My Key2: My Value2"), PreprocessorElement(2, "My Key3: My Value3")])), PreprocessorElement(2, "-"), PreprocessorElement(1, of_array([PreprocessorElement(2, "My Key4: My Value4"), PreprocessorElement(2, "My Key5: My Value5"), PreprocessorElement(2, "My Key6: My Value6")]))]))

StringReplaceClean: str = "\r\nMy Key: </1>\r\n"

__all__ = ["SequenceMappingsAST", "StringReplaceClean"]

