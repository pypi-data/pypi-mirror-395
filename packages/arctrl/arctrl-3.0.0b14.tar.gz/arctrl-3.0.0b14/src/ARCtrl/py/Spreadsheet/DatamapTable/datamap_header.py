from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (map, FSharpList, item, is_empty, head, tail, try_find_index)
from ...fable_modules.fable_library.option import map as map_1
from ...fable_modules.fable_library.seq import (to_list, delay, append, map as map_2)
from ...fable_modules.fable_library.string_ import (starts_with_exact, join, to_fail, printf)
from ...fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ...fable_modules.fs_spreadsheet.Cells.fs_cell import FsCell
from ...Core.comment import Comment
from ...Core.data import Data
from ...Core.data_context import (DataContext__set_Explication_279AAFF2, DataContext, DataContext__set_Unit_279AAFF2, DataContext__set_ObjectType_279AAFF2, DataContext__set_Description_6DFDD678, DataContext__set_GeneratedBy_6DFDD678, DataContext__set_Label_6DFDD678)
from ...Core.Helper.collections_ import Option_fromValueWithDefault
from ...Core.Helper.regex import ActivePatterns__007CComment_007C__007C
from ...Core.ontology_annotation import OntologyAnnotation

def ActivePattern_ontologyAnnotationFromFsCells(tsr_col: int | None, tan_col: int | None, cells: FSharpList[FsCell]) -> OntologyAnnotation:
    def mapping(c: FsCell, tsr_col: Any=tsr_col, tan_col: Any=tan_col, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    def _arrow1560(i: int, tsr_col: Any=tsr_col, tan_col: Any=tan_col, cells: Any=cells) -> str:
        return item(i, cell_values)

    tsr: str | None = map_1(_arrow1560, tsr_col)
    def _arrow1561(i_1: int, tsr_col: Any=tsr_col, tan_col: Any=tan_col, cells: Any=cells) -> str:
        return item(i_1, cell_values)

    tan: str | None = map_1(_arrow1561, tan_col)
    return OntologyAnnotation(item(0, cell_values), tsr, tan)


def ActivePattern_freeTextFromFsCells(cells: FSharpList[FsCell]) -> str:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    return item(0, map(mapping, cells))


def ActivePattern_dataFromFsCells(format: int | None, selector_format: int | None, cells: FSharpList[FsCell]) -> Data:
    def mapping(c: FsCell, format: Any=format, selector_format: Any=selector_format, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    def _arrow1562(i: int, format: Any=format, selector_format: Any=selector_format, cells: Any=cells) -> str:
        return item(i, cell_values)

    format_1: str | None = map_1(_arrow1562, format)
    def _arrow1563(i_1: int, format: Any=format, selector_format: Any=selector_format, cells: Any=cells) -> str:
        return item(i_1, cell_values)

    selector_format_1: str | None = map_1(_arrow1563, selector_format)
    return Data(None, item(0, cell_values), None, format_1, selector_format_1)


def ActivePattern__007CTerm_007C__007C(category_string: str, cells: FSharpList[FsCell]) -> Callable[[FSharpList[FsCell]], OntologyAnnotation] | None:
    def _007CAC_007C__007C(s: str, category_string: Any=category_string, cells: Any=cells) -> int | None:
        if s == category_string:
            return 1

        else: 
            return None


    def _007CTSRColumnHeaderRaw_007C__007C(s_1: str, category_string: Any=category_string, cells: Any=cells) -> str | None:
        if starts_with_exact(s_1, "Term Source REF"):
            return s_1

        else: 
            return None


    def _007CTANColumnHeaderRaw_007C__007C(s_2: str, category_string: Any=category_string, cells: Any=cells) -> str | None:
        if starts_with_exact(s_2, "Term Accession Number"):
            return s_2

        else: 
            return None


    def mapping(c: FsCell, category_string: Any=category_string, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result,) = (None,)
    if not is_empty(cell_values):
        active_pattern_result: int | None = _007CAC_007C__007C(head(cell_values))
        if active_pattern_result is not None:
            if is_empty(tail(cell_values)):
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def Value(cells_1: FSharpList[FsCell], category_string: Any=category_string, cells: Any=cells) -> OntologyAnnotation:
            return ActivePattern_ontologyAnnotationFromFsCells(None, None, cells_1)

        return Value

    elif pattern_matching_result == 1:
        (pattern_matching_result_1,) = (None,)
        if not is_empty(cell_values):
            active_pattern_result_1: int | None = _007CAC_007C__007C(head(cell_values))
            if active_pattern_result_1 is not None:
                if not is_empty(tail(cell_values)):
                    if _007CTSRColumnHeaderRaw_007C__007C(head(tail(cell_values))) is not None:
                        if not is_empty(tail(tail(cell_values))):
                            if _007CTANColumnHeaderRaw_007C__007C(head(tail(tail(cell_values)))) is not None:
                                if is_empty(tail(tail(tail(cell_values)))):
                                    pattern_matching_result_1 = 0

                                else: 
                                    pattern_matching_result_1 = 1


                            else: 
                                pattern_matching_result_1 = 1


                        else: 
                            pattern_matching_result_1 = 1


                    else: 
                        pattern_matching_result_1 = 1


                else: 
                    pattern_matching_result_1 = 1


            else: 
                pattern_matching_result_1 = 1


        else: 
            pattern_matching_result_1 = 1

        if pattern_matching_result_1 == 0:
            def Value_1(cells_2: FSharpList[FsCell], category_string: Any=category_string, cells: Any=cells) -> OntologyAnnotation:
                return ActivePattern_ontologyAnnotationFromFsCells(1, 2, cells_2)

            return Value_1

        elif pattern_matching_result_1 == 1:
            (pattern_matching_result_2,) = (None,)
            if not is_empty(cell_values):
                active_pattern_result_4: int | None = _007CAC_007C__007C(head(cell_values))
                if active_pattern_result_4 is not None:
                    if not is_empty(tail(cell_values)):
                        if _007CTANColumnHeaderRaw_007C__007C(head(tail(cell_values))) is not None:
                            if not is_empty(tail(tail(cell_values))):
                                if _007CTSRColumnHeaderRaw_007C__007C(head(tail(tail(cell_values)))) is not None:
                                    if is_empty(tail(tail(tail(cell_values)))):
                                        pattern_matching_result_2 = 0

                                    else: 
                                        pattern_matching_result_2 = 1


                                else: 
                                    pattern_matching_result_2 = 1


                            else: 
                                pattern_matching_result_2 = 1


                        else: 
                            pattern_matching_result_2 = 1


                    else: 
                        pattern_matching_result_2 = 1


                else: 
                    pattern_matching_result_2 = 1


            else: 
                pattern_matching_result_2 = 1

            if pattern_matching_result_2 == 0:
                def Value_2(cells_3: FSharpList[FsCell], category_string: Any=category_string, cells: Any=cells) -> OntologyAnnotation:
                    return ActivePattern_ontologyAnnotationFromFsCells(2, 1, cells_3)

                return Value_2

            elif pattern_matching_result_2 == 1:
                return None





def ActivePattern__007CExplication_007C__007C(cells: FSharpList[FsCell]) -> Callable[[DataContext, FSharpList[FsCell]], DataContext] | None:
    active_pattern_result: Callable[[FSharpList[FsCell]], OntologyAnnotation] | None = ActivePattern__007CTerm_007C__007C("Explication", cells)
    if active_pattern_result is not None:
        r: Callable[[FSharpList[FsCell]], OntologyAnnotation] = active_pattern_result
        def Value(dc: DataContext, cells: Any=cells) -> Callable[[FSharpList[FsCell]], DataContext]:
            def _arrow1564(cells_1: FSharpList[FsCell], dc: Any=dc) -> DataContext:
                DataContext__set_Explication_279AAFF2(dc, r(cells_1))
                return dc

            return _arrow1564

        return Value

    else: 
        return None



def ActivePattern__007CUnit_007C__007C(cells: FSharpList[FsCell]) -> Callable[[DataContext, FSharpList[FsCell]], DataContext] | None:
    active_pattern_result: Callable[[FSharpList[FsCell]], OntologyAnnotation] | None = ActivePattern__007CTerm_007C__007C("Unit", cells)
    if active_pattern_result is not None:
        r: Callable[[FSharpList[FsCell]], OntologyAnnotation] = active_pattern_result
        def Value(dc: DataContext, cells: Any=cells) -> Callable[[FSharpList[FsCell]], DataContext]:
            def _arrow1565(cells_1: FSharpList[FsCell], dc: Any=dc) -> DataContext:
                DataContext__set_Unit_279AAFF2(dc, r(cells_1))
                return dc

            return _arrow1565

        return Value

    else: 
        return None



def ActivePattern__007CObjectType_007C__007C(cells: FSharpList[FsCell]) -> Callable[[DataContext, FSharpList[FsCell]], DataContext] | None:
    active_pattern_result: Callable[[FSharpList[FsCell]], OntologyAnnotation] | None = ActivePattern__007CTerm_007C__007C("Object Type", cells)
    if active_pattern_result is not None:
        r: Callable[[FSharpList[FsCell]], OntologyAnnotation] = active_pattern_result
        def Value(dc: DataContext, cells: Any=cells) -> Callable[[FSharpList[FsCell]], DataContext]:
            def _arrow1566(cells_1: FSharpList[FsCell], dc: Any=dc) -> DataContext:
                DataContext__set_ObjectType_279AAFF2(dc, r(cells_1))
                return dc

            return _arrow1566

        return Value

    else: 
        return None



def ActivePattern__007CDescription_007C__007C(cells: FSharpList[FsCell]) -> Callable[[DataContext, FSharpList[FsCell]], DataContext] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result,) = (None,)
    if not is_empty(cell_values):
        if head(cell_values) == "Description":
            if is_empty(tail(cell_values)):
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def Value(dc: DataContext, cells: Any=cells) -> Callable[[FSharpList[FsCell]], DataContext]:
            def _arrow1567(cells_1: FSharpList[FsCell], dc: Any=dc) -> DataContext:
                DataContext__set_Description_6DFDD678(dc, Option_fromValueWithDefault("", ActivePattern_freeTextFromFsCells(cells_1)))
                return dc

            return _arrow1567

        return Value

    elif pattern_matching_result == 1:
        return None



def ActivePattern__007CGeneratedBy_007C__007C(cells: FSharpList[FsCell]) -> Callable[[DataContext, FSharpList[FsCell]], DataContext] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result,) = (None,)
    if not is_empty(cell_values):
        if head(cell_values) == "Generated By":
            if is_empty(tail(cell_values)):
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def Value(dc: DataContext, cells: Any=cells) -> Callable[[FSharpList[FsCell]], DataContext]:
            def _arrow1568(cells_1: FSharpList[FsCell], dc: Any=dc) -> DataContext:
                DataContext__set_GeneratedBy_6DFDD678(dc, Option_fromValueWithDefault("", ActivePattern_freeTextFromFsCells(cells_1)))
                return dc

            return _arrow1568

        return Value

    elif pattern_matching_result == 1:
        return None



def ActivePattern__007CLabel_007C__007C(cells: FSharpList[FsCell]) -> Callable[[DataContext, FSharpList[FsCell]], DataContext] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result,) = (None,)
    if not is_empty(cell_values):
        if head(cell_values) == "Label":
            if is_empty(tail(cell_values)):
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def Value(dc: DataContext, cells: Any=cells) -> Callable[[FSharpList[FsCell]], DataContext]:
            def _arrow1569(cells_1: FSharpList[FsCell], dc: Any=dc) -> DataContext:
                DataContext__set_Label_6DFDD678(dc, Option_fromValueWithDefault("", ActivePattern_freeTextFromFsCells(cells_1)))
                return dc

            return _arrow1569

        return Value

    elif pattern_matching_result == 1:
        return None



def ActivePattern__007CData_007C__007C(cells: FSharpList[FsCell]) -> Callable[[DataContext, FSharpList[FsCell]], DataContext] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result, cols) = (None, None)
    if not is_empty(cell_values):
        if head(cell_values) == "Data":
            pattern_matching_result = 0
            cols = tail(cell_values)

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def Value(dc: DataContext, cells: Any=cells) -> Callable[[FSharpList[FsCell]], DataContext]:
            def _arrow1570(cells_1: FSharpList[FsCell], dc: Any=dc) -> DataContext:
                def mapping_1(y: int) -> int:
                    return 1 + y

                def predicate(s: str) -> bool:
                    return starts_with_exact(s, "Data Format")

                def mapping_2(y_1: int) -> int:
                    return 1 + y_1

                def predicate_1(s_1: str) -> bool:
                    return starts_with_exact(s_1, "Data Selector Format")

                d: Data = ActivePattern_dataFromFsCells(map_1(mapping_1, try_find_index(predicate, cols)), map_1(mapping_2, try_find_index(predicate_1, cols)), cells_1)
                dc.FilePath = d.FilePath
                dc.Selector = d.Selector
                dc.Format = d.Format
                dc.SelectorFormat = d.SelectorFormat
                return dc

            return _arrow1570

        return Value

    elif pattern_matching_result == 1:
        return None



def ActivePattern__007CComment_007C__007C(cells: FSharpList[FsCell]) -> Callable[[DataContext, FSharpList[FsCell]], DataContext] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result, key) = (None, None)
    if not is_empty(cell_values):
        active_pattern_result: str | None = ActivePatterns__007CComment_007C__007C(head(cell_values))
        if active_pattern_result is not None:
            if is_empty(tail(cell_values)):
                pattern_matching_result = 0
                key = active_pattern_result

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def Value(dc: DataContext, cells: Any=cells) -> Callable[[FSharpList[FsCell]], DataContext]:
            def _arrow1571(cells_1: FSharpList[FsCell], dc: Any=dc) -> DataContext:
                def mapping_1(c_1: FsCell) -> str:
                    return c_1.ValueAsString()

                comment: str = item(0, map(mapping_1, cells_1))
                (dc.Comments.append(Comment.create(key, comment)))
                return dc

            return _arrow1571

        return Value

    elif pattern_matching_result == 1:
        return None



def ActivePattern__007CFreetext_007C__007C(cells: FSharpList[FsCell]) -> Callable[[DataContext, FSharpList[FsCell]], DataContext] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result, key) = (None, None)
    if not is_empty(cell_values):
        if is_empty(tail(cell_values)):
            pattern_matching_result = 0
            key = head(cell_values)

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def Value(dc: DataContext, cells: Any=cells) -> Callable[[FSharpList[FsCell]], DataContext]:
            def _arrow1572(cells_1: FSharpList[FsCell], dc: Any=dc) -> DataContext:
                def mapping_1(c_1: FsCell) -> str:
                    return c_1.ValueAsString()

                comment: str = item(0, map(mapping_1, cells_1))
                (dc.Comments.append(Comment.create(key, comment)))
                return dc

            return _arrow1572

        return Value

    elif pattern_matching_result == 1:
        return None



def from_fs_cells(cells: FSharpList[FsCell]) -> Callable[[DataContext, FSharpList[FsCell]], DataContext]:
    (pattern_matching_result, r) = (None, None)
    active_pattern_result: Callable[[DataContext, FSharpList[FsCell]], DataContext] | None = ActivePattern__007CExplication_007C__007C(cells)
    if active_pattern_result is not None:
        pattern_matching_result = 0
        r = active_pattern_result

    else: 
        active_pattern_result_1: Callable[[DataContext, FSharpList[FsCell]], DataContext] | None = ActivePattern__007CUnit_007C__007C(cells)
        if active_pattern_result_1 is not None:
            pattern_matching_result = 0
            r = active_pattern_result_1

        else: 
            active_pattern_result_2: Callable[[DataContext, FSharpList[FsCell]], DataContext] | None = ActivePattern__007CObjectType_007C__007C(cells)
            if active_pattern_result_2 is not None:
                pattern_matching_result = 0
                r = active_pattern_result_2

            else: 
                active_pattern_result_3: Callable[[DataContext, FSharpList[FsCell]], DataContext] | None = ActivePattern__007CDescription_007C__007C(cells)
                if active_pattern_result_3 is not None:
                    pattern_matching_result = 0
                    r = active_pattern_result_3

                else: 
                    active_pattern_result_4: Callable[[DataContext, FSharpList[FsCell]], DataContext] | None = ActivePattern__007CGeneratedBy_007C__007C(cells)
                    if active_pattern_result_4 is not None:
                        pattern_matching_result = 0
                        r = active_pattern_result_4

                    else: 
                        active_pattern_result_5: Callable[[DataContext, FSharpList[FsCell]], DataContext] | None = ActivePattern__007CLabel_007C__007C(cells)
                        if active_pattern_result_5 is not None:
                            pattern_matching_result = 0
                            r = active_pattern_result_5

                        else: 
                            active_pattern_result_6: Callable[[DataContext, FSharpList[FsCell]], DataContext] | None = ActivePattern__007CData_007C__007C(cells)
                            if active_pattern_result_6 is not None:
                                pattern_matching_result = 0
                                r = active_pattern_result_6

                            else: 
                                active_pattern_result_7: Callable[[DataContext, FSharpList[FsCell]], DataContext] | None = ActivePattern__007CComment_007C__007C(cells)
                                if active_pattern_result_7 is not None:
                                    pattern_matching_result = 0
                                    r = active_pattern_result_7

                                else: 
                                    active_pattern_result_8: Callable[[DataContext, FSharpList[FsCell]], DataContext] | None = ActivePattern__007CFreetext_007C__007C(cells)
                                    if active_pattern_result_8 is not None:
                                        pattern_matching_result = 0
                                        r = active_pattern_result_8

                                    else: 
                                        pattern_matching_result = 1









    if pattern_matching_result == 0:
        def _arrow1574(dc: DataContext, cells: Any=cells) -> Callable[[FSharpList[FsCell]], DataContext]:
            def _arrow1573(cells_1: FSharpList[FsCell]) -> DataContext:
                return r(dc)(cells_1)

            return _arrow1573

        return _arrow1574

    elif pattern_matching_result == 1:
        def mapping(c: FsCell, cells: Any=cells) -> str:
            return c.ValueAsString()

        arg: str = join(", ", map(mapping, cells))
        clo_1: Callable[[DataContext, FSharpList[FsCell]], DataContext] = to_fail(printf("Could not parse data map column: %s"))(arg)
        def _arrow1575(arg_1: DataContext, cells: Any=cells) -> Callable[[FSharpList[FsCell]], DataContext]:
            clo_2: Callable[[FSharpList[FsCell]], DataContext] = clo_1(arg_1)
            return clo_2

        return _arrow1575



def to_fs_cells(comment_keys: FSharpList[str]) -> FSharpList[FsCell]:
    def _arrow1584(__unit: None=None, comment_keys: Any=comment_keys) -> IEnumerable_1[FsCell]:
        def _arrow1583(__unit: None=None) -> IEnumerable_1[FsCell]:
            def _arrow1582(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow1581(__unit: None=None) -> IEnumerable_1[FsCell]:
                    def _arrow1580(__unit: None=None) -> IEnumerable_1[FsCell]:
                        def _arrow1579(__unit: None=None) -> IEnumerable_1[FsCell]:
                            def _arrow1578(__unit: None=None) -> IEnumerable_1[FsCell]:
                                def _arrow1577(__unit: None=None) -> IEnumerable_1[FsCell]:
                                    def _arrow1576(ck: str) -> FsCell:
                                        return FsCell(("Comment [" + ck) + "]")

                                    return map_2(_arrow1576, comment_keys)

                                return append(to_enumerable([FsCell("Label")]), delay(_arrow1577))

                            return append(to_enumerable([FsCell("Generated By")]), delay(_arrow1578))

                        return append(to_enumerable([FsCell("Description")]), delay(_arrow1579))

                    return append(to_enumerable([FsCell("Object Type"), FsCell("Term Source REF"), FsCell("Term Accession Number")]), delay(_arrow1580))

                return append(to_enumerable([FsCell("Unit"), FsCell("Term Source REF"), FsCell("Term Accession Number")]), delay(_arrow1581))

            return append(to_enumerable([FsCell("Explication"), FsCell("Term Source REF"), FsCell("Term Accession Number")]), delay(_arrow1582))

        return append(to_enumerable([FsCell("Data"), FsCell("Data Format"), FsCell("Data Selector Format")]), delay(_arrow1583))

    return to_list(delay(_arrow1584))


__all__ = ["ActivePattern_ontologyAnnotationFromFsCells", "ActivePattern_freeTextFromFsCells", "ActivePattern_dataFromFsCells", "ActivePattern__007CTerm_007C__007C", "ActivePattern__007CExplication_007C__007C", "ActivePattern__007CUnit_007C__007C", "ActivePattern__007CObjectType_007C__007C", "ActivePattern__007CDescription_007C__007C", "ActivePattern__007CGeneratedBy_007C__007C", "ActivePattern__007CLabel_007C__007C", "ActivePattern__007CData_007C__007C", "ActivePattern__007CComment_007C__007C", "ActivePattern__007CFreetext_007C__007C", "from_fs_cells", "to_fs_cells"]

