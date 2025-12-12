from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.string_ import (to_text, printf, trim, trim_start as trim_start_1, starts_with_exact, substring)
from ..fable_modules.fable_library.types import (Array, to_string)
from .comment import Comment
from .data_file import (DataFile, DataFile__get_AsString)
from .Helper.collections_ import ResizeArray_map
from .Helper.hash_codes import (box_hash_array, box_hash_option, box_hash_seq, hash_1)

def DataAux_nameFromPathAndSelector(path: str, selector: str) -> str:
    return to_text(printf("%s#%s"))(path)(selector)


def DataAux_pathAndSelectorFromName(name: str) -> tuple[str, str | None]:
    name_1: str = trim(name, "#")
    parts: Array[str] = name_1.split("#")
    if len(parts) == 2:
        return (parts[0], parts[1])

    else: 
        return (name_1, None)



def _expr728() -> TypeInfo:
    return class_type("ARCtrl.Data", None, Data)


class Data:
    def __init__(self, id: str | None=None, name: str | None=None, data_type: DataFile | None=None, format: str | None=None, selector_format: str | None=None, comments: Array[Comment] | None=None) -> None:
        self._id: str | None = id
        pattern_input_1: tuple[str | None, str | None]
        if name is None:
            pattern_input_1 = (None, None)

        else: 
            pattern_input: tuple[str, str | None] = DataAux_pathAndSelectorFromName(name)
            pattern_input_1 = (pattern_input[0], pattern_input[1])

        self._selector: str | None = pattern_input_1[1]
        self._filePath: str | None = pattern_input_1[0]
        self._dataType: DataFile | None = data_type
        self._format: str | None = format
        self._selectorFormat: str | None = selector_format
        self._comments: Array[Comment] = default_arg(comments, [])

    @property
    def ID(self, __unit: None=None) -> str | None:
        this: Data = self
        return this._id

    @ID.setter
    def ID(self, id: str | None=None) -> None:
        this: Data = self
        this._id = id

    @property
    def Name(self, __unit: None=None) -> str | None:
        this: Data = self
        match_value: str | None = this._filePath
        match_value_1: str | None = this._selector
        def _arrow723(__unit: None=None) -> str | None:
            p_1: str = match_value
            return p_1

        def _arrow724(__unit: None=None) -> str | None:
            p: str = match_value
            s: str = match_value_1
            return DataAux_nameFromPathAndSelector(p, s)

        return None if (match_value is None) else (_arrow723() if (match_value_1 is None) else _arrow724())

    @Name.setter
    def Name(self, name: str | None=None) -> None:
        this: Data = self
        if name is None:
            this._filePath = None
            this._selector = None

        else: 
            pattern_input: tuple[str, str | None] = DataAux_pathAndSelectorFromName(name)
            this._filePath = pattern_input[0]
            this._selector = pattern_input[1]


    @property
    def FilePath(self, __unit: None=None) -> str | None:
        this: Data = self
        return this._filePath

    @FilePath.setter
    def FilePath(self, file_path: str | None=None) -> None:
        this: Data = self
        this._filePath = file_path

    @property
    def Selector(self, __unit: None=None) -> str | None:
        this: Data = self
        return this._selector

    @Selector.setter
    def Selector(self, selector: str | None=None) -> None:
        this: Data = self
        this._selector = selector

    @property
    def DataType(self, __unit: None=None) -> DataFile | None:
        this: Data = self
        return this._dataType

    @DataType.setter
    def DataType(self, data_type: DataFile | None=None) -> None:
        this: Data = self
        this._dataType = data_type

    @property
    def Format(self, __unit: None=None) -> str | None:
        this: Data = self
        return this._format

    @Format.setter
    def Format(self, format: str | None=None) -> None:
        this: Data = self
        this._format = format

    @property
    def SelectorFormat(self, __unit: None=None) -> str | None:
        this: Data = self
        return this._selectorFormat

    @SelectorFormat.setter
    def SelectorFormat(self, selector_format: str | None=None) -> None:
        this: Data = self
        this._selectorFormat = selector_format

    @property
    def Comments(self, __unit: None=None) -> Array[Comment]:
        this: Data = self
        return this._comments

    @Comments.setter
    def Comments(self, comments: Array[Comment]) -> None:
        this: Data = self
        this._comments = comments

    @staticmethod
    def make(id: str | None=None, name: str | None=None, data_type: DataFile | None=None, format: str | None=None, selector_format: str | None=None, comments: Array[Comment] | None=None) -> Data:
        return Data(id, name, data_type, format, selector_format, comments)

    @staticmethod
    def create(Id: str | None=None, Name: str | None=None, DataType: DataFile | None=None, Format: str | None=None, SelectorFormat: str | None=None, Comments: Array[Comment] | None=None) -> Data:
        return Data.make(Id, Name, DataType, Format, SelectorFormat, Comments)

    @staticmethod
    def empty() -> Data:
        return Data.create()

    @property
    def NameText(self, __unit: None=None) -> str:
        this: Data = self
        return default_arg(this.Name, "")

    def GetAbsolutePathBy(self, f: Callable[[str], str], check_existence_from_root: Callable[[str], bool] | None=None) -> str:
        this: Data = self
        def _arrow725(_arg: str) -> bool:
            return False

        check_existence_from_root_1: Callable[[str], bool] = default_arg(check_existence_from_root, _arrow725)
        match_value: str | None = this.FilePath
        if match_value is None:
            raise Exception("Data does not have a file path")

        else: 
            p_3: str
            s: str = trim_start_1(match_value, "/")
            p_3 = substring(s, len("./")) if starts_with_exact(s, "./") else s
            def _arrow726(__unit: None=None) -> bool:
                p: str = p_3
                return True if (True if (True if starts_with_exact(p, "assays/") else starts_with_exact(p, "studies/")) else starts_with_exact(p, "workflows/")) else starts_with_exact(p, "runs/")

            def _arrow727(__unit: None=None) -> bool:
                p_1: str = p_3
                return True if starts_with_exact(p_1, "http:") else starts_with_exact(p_1, "https:")

            return p_3 if (True if (True if check_existence_from_root_1(p_3) else _arrow726()) else _arrow727()) else f(p_3)


    def GetAbsolutePathForAssay(self, assay_identifier: str, check_existence_from_root: Callable[[str], bool] | None=None) -> str:
        this: Data = self
        def f(p: str) -> str:
            return (("assays/" + assay_identifier) + "/dataset/") + trim_start_1(p, "/")

        return this.GetAbsolutePathBy(f, check_existence_from_root)

    def GetAbsolutePathForStudy(self, study_identifier: str, check_existence_from_root: Callable[[str], bool] | None=None) -> str:
        this: Data = self
        def f(p: str) -> str:
            return (("studies/" + study_identifier) + "/resources/") + trim_start_1(p, "/")

        return this.GetAbsolutePathBy(f, check_existence_from_root)

    def Copy(self, __unit: None=None) -> Data:
        this: Data = self
        def f(c: Comment) -> Comment:
            return c.Copy()

        next_comments: Array[Comment] = ResizeArray_map(f, this.Comments)
        return Data(this.ID, this.Name, this.DataType, this.Format, this.SelectorFormat, next_comments)

    def __hash__(self, __unit: None=None) -> Any:
        this: Data = self
        return box_hash_array([box_hash_option(this.ID), box_hash_option(this.Name), box_hash_option(this.DataType), box_hash_option(this.Format), box_hash_option(this.SelectorFormat), box_hash_seq(this.Comments)])

    def __eq__(self, obj: Any=None) -> bool:
        this: Data = self
        return hash_1(this) == hash_1(obj)

    def Print(self, __unit: None=None) -> str:
        this: Data = self
        return to_string(this)

    def PrintCompact(self, __unit: None=None) -> str:
        this: Data = self
        match_value: DataFile | None = this.DataType
        if match_value is None:
            arg_2: str = this.NameText
            return to_text(printf("%s"))(arg_2)

        else: 
            t: DataFile = match_value
            arg: str = this.NameText
            arg_1: str = DataFile__get_AsString(t)
            return to_text(printf("%s [%s]"))(arg)(arg_1)



Data_reflection = _expr728

def Data__ctor_5909441C(id: str | None=None, name: str | None=None, data_type: DataFile | None=None, format: str | None=None, selector_format: str | None=None, comments: Array[Comment] | None=None) -> Data:
    return Data(id, name, data_type, format, selector_format, comments)


__all__ = ["DataAux_nameFromPathAndSelector", "DataAux_pathAndSelectorFromName", "Data_reflection"]

