from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (map, FSharpList, of_array, singleton, transpose)
from ...fable_modules.fable_library.option import (default_arg, bind)
from ...fable_modules.fable_library.seq import (to_list, collect, map as map_1, delay, append, singleton as singleton_1, try_find)
from ...fable_modules.fable_library.seq2 import distinct
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (ignore, IEnumerable_1, string_hash)
from ...fable_modules.fs_spreadsheet.Cells.fs_cell import FsCell
from ...fable_modules.fs_spreadsheet.fs_column import FsColumn
from ...Core.comment import Comment
from ...Core.data_context import (DataContext, DataContext__get_Explication, DataContext__get_Unit, DataContext__get_ObjectType, DataContext__get_Description, DataContext__get_GeneratedBy, DataContext__get_Label)
from ...Core.ontology_annotation import OntologyAnnotation
from .datamap_header import (from_fs_cells, to_fs_cells)

def set_from_fs_columns(dc: Array[DataContext], columns: FSharpList[FsColumn]) -> Array[DataContext]:
    def mapping(c: FsColumn, dc: Any=dc, columns: Any=columns) -> FsCell:
        return c.Item(1)

    cell_parser: Callable[[DataContext, FSharpList[FsCell]], DataContext] = from_fs_cells(map(mapping, columns))
    for i in range(0, (len(dc) - 1) + 1, 1):
        def mapping_1(c_1: FsColumn, dc: Any=dc, columns: Any=columns) -> FsCell:
            return c_1.Item(i + 2)

        ignore(cell_parser(dc[i])(map(mapping_1, columns)))
    return dc


def to_fs_columns(dc: Array[DataContext]) -> FSharpList[FSharpList[FsCell]]:
    def mapping_1(dc_1: DataContext, dc: Any=dc) -> IEnumerable_1[str]:
        def mapping(c: Comment, dc_1: Any=dc_1) -> str:
            return default_arg(c.Name, "")

        return map_1(mapping, dc_1.Comments)

    class ObjectExpr1547:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1546(x: str, y: str) -> bool:
                return x == y

            return _arrow1546

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    comment_keys: FSharpList[str] = to_list(distinct(collect(mapping_1, dc), ObjectExpr1547()))
    headers: FSharpList[FsCell] = to_fs_cells(comment_keys)
    def create_term(oa: OntologyAnnotation | None=None, dc: Any=dc) -> FSharpList[FsCell]:
        if oa is None:
            return of_array([FsCell(""), FsCell(""), FsCell("")])

        else: 
            oa_1: OntologyAnnotation = oa
            return of_array([FsCell(default_arg(oa_1.Name, "")), FsCell(default_arg(oa_1.TermSourceREF, "")), FsCell(default_arg(oa_1.TermAccessionNumber, ""))])


    def create_text(s: str | None=None, dc: Any=dc) -> FSharpList[FsCell]:
        return singleton(FsCell(default_arg(s, "")))

    def _arrow1559(__unit: None=None, dc: Any=dc) -> IEnumerable_1[FSharpList[FsCell]]:
        def _arrow1558(__unit: None=None) -> IEnumerable_1[FSharpList[FsCell]]:
            def _arrow1557(dc_4: DataContext) -> FSharpList[FsCell]:
                dc_3: DataContext = dc_4
                def _arrow1556(__unit: None=None) -> IEnumerable_1[FsCell]:
                    def _arrow1548(__unit: None=None) -> FSharpList[FsCell]:
                        dc_2: DataContext = dc_3
                        return of_array([FsCell(default_arg(dc_2.Name, "")), FsCell(default_arg(dc_2.Format, "")), FsCell(default_arg(dc_2.SelectorFormat, ""))])

                    def _arrow1555(__unit: None=None) -> IEnumerable_1[FsCell]:
                        def _arrow1554(__unit: None=None) -> IEnumerable_1[FsCell]:
                            def _arrow1553(__unit: None=None) -> IEnumerable_1[FsCell]:
                                def _arrow1552(__unit: None=None) -> IEnumerable_1[FsCell]:
                                    def _arrow1551(__unit: None=None) -> IEnumerable_1[FsCell]:
                                        def _arrow1550(__unit: None=None) -> IEnumerable_1[FsCell]:
                                            def _arrow1549(__unit: None=None) -> IEnumerable_1[FsCell]:
                                                def mapping_2(key: str) -> FsCell:
                                                    def binder(c_2: Comment, key: Any=key) -> str | None:
                                                        return c_2.Value

                                                    def predicate(c_1: Comment, key: Any=key) -> bool:
                                                        return default_arg(c_1.Name, "") == key

                                                    return FsCell(default_arg(bind(binder, try_find(predicate, dc_3.Comments)), ""))

                                                return map(mapping_2, comment_keys)

                                            return append(create_text(DataContext__get_Label(dc_3)), delay(_arrow1549))

                                        return append(create_text(DataContext__get_GeneratedBy(dc_3)), delay(_arrow1550))

                                    return append(create_text(DataContext__get_Description(dc_3)), delay(_arrow1551))

                                return append(create_term(DataContext__get_ObjectType(dc_3)), delay(_arrow1552))

                            return append(create_term(DataContext__get_Unit(dc_3)), delay(_arrow1553))

                        return append(create_term(DataContext__get_Explication(dc_3)), delay(_arrow1554))

                    return append(_arrow1548(), delay(_arrow1555))

                return to_list(delay(_arrow1556))

            return map_1(_arrow1557, dc)

        return append(singleton_1(headers), delay(_arrow1558))

    return transpose(to_list(delay(_arrow1559)))


__all__ = ["set_from_fs_columns", "to_fs_columns"]

