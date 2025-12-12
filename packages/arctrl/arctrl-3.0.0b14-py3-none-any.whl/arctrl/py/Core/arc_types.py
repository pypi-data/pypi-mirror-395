from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.array_ import (contains as contains_1, remove_in_place, add_range_in_place)
from ..fable_modules.fable_library.option import (map, default_arg, value as value_6)
from ..fable_modules.fable_library.range import range_big_int
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.resize_array import find_index
from ..fable_modules.fable_library.seq import (to_array, filter, contains, for_all, length, fold, to_list, delay, map as map_1, item, choose, exists, try_find_index, iterate, remove_at, try_find, append as append_5, collect)
from ..fable_modules.fable_library.seq2 import Array_distinct
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.fable_library.types import (Array, FSharpRef)
from ..fable_modules.fable_library.util import (string_hash, IEnumerable_1, get_enumerator, dispose, equals, safe_hash, to_enumerable, ignore)
from ..CWL.cwlprocessing_unit import CWLProcessingUnit
from ..CWL.parameter_reference import CWLParameterReference
from .comment import (Comment, Remark)
from .datamap import Datamap
from .Helper.collections_ import (ResizeArray_map, ResizeArray_filter, ResizeArray_choose)
from .Helper.hash_codes import (box_hash_array, box_hash_option, box_hash_seq)
from .Helper.identifier import check_valid_characters
from .ontology_annotation import OntologyAnnotation
from .ontology_source_reference import OntologySourceReference
from .person import Person
from .Process.component import Component
from .publication import Publication
from .Table.arc_table import ArcTable
from .Table.arc_tables import (ArcTables, ArcTables_reflection, ArcTablesAux_getIOMap, ArcTablesAux_applyIOMap)
from .Table.composite_cell import CompositeCell
from .Table.composite_column import CompositeColumn
from .Table.composite_header import CompositeHeader

def _expr1143() -> TypeInfo:
    return class_type("ARCtrl.ArcAssay", None, ArcAssay, ArcTables_reflection())


class ArcAssay(ArcTables):
    def __init__(self, identifier: str, title: str | None=None, description: str | None=None, measurement_type: OntologyAnnotation | None=None, technology_type: OntologyAnnotation | None=None, technology_platform: OntologyAnnotation | None=None, tables: Array[ArcTable] | None=None, datamap: Datamap | None=None, performers: Array[Person] | None=None, comments: Array[Comment] | None=None) -> None:
        super().__init__(default_arg(tables, []))
        performers_1: Array[Person] = default_arg(performers, [])
        comments_1: Array[Comment] = default_arg(comments, [])
        def _arrow1142(__unit: None=None) -> str:
            identifier_1: str = identifier.strip()
            check_valid_characters(identifier_1)
            return identifier_1

        self.identifier_0040129: str = _arrow1142()
        self.title_0040133: str | None = title
        self.description_0040134: str | None = description
        self.investigation: ArcInvestigation | None = None
        self.measurement_type_0040136: OntologyAnnotation | None = measurement_type
        self.technology_type_0040137: OntologyAnnotation | None = technology_type
        self.technology_platform_0040138: OntologyAnnotation | None = technology_platform
        self.datamap_0040139: Datamap | None = datamap
        self.performers_0040140_002D1: Array[Person] = performers_1
        self.comments_0040141_002D1: Array[Comment] = comments_1
        self.static_hash: int = 0

    @property
    def Identifier(self, __unit: None=None) -> str:
        this: ArcAssay = self
        return this.identifier_0040129

    @Identifier.setter
    def Identifier(self, i: str) -> None:
        this: ArcAssay = self
        this.identifier_0040129 = i

    @property
    def Investigation(self, __unit: None=None) -> ArcInvestigation | None:
        this: ArcAssay = self
        return this.investigation

    @Investigation.setter
    def Investigation(self, i: ArcInvestigation | None=None) -> None:
        this: ArcAssay = self
        this.investigation = i

    @property
    def Title(self, __unit: None=None) -> str | None:
        this: ArcAssay = self
        return this.title_0040133

    @Title.setter
    def Title(self, t: str | None=None) -> None:
        this: ArcAssay = self
        this.title_0040133 = t

    @property
    def Description(self, __unit: None=None) -> str | None:
        this: ArcAssay = self
        return this.description_0040134

    @Description.setter
    def Description(self, d: str | None=None) -> None:
        this: ArcAssay = self
        this.description_0040134 = d

    @property
    def MeasurementType(self, __unit: None=None) -> OntologyAnnotation | None:
        this: ArcAssay = self
        return this.measurement_type_0040136

    @MeasurementType.setter
    def MeasurementType(self, n: OntologyAnnotation | None=None) -> None:
        this: ArcAssay = self
        this.measurement_type_0040136 = n

    @property
    def TechnologyType(self, __unit: None=None) -> OntologyAnnotation | None:
        this: ArcAssay = self
        return this.technology_type_0040137

    @TechnologyType.setter
    def TechnologyType(self, n: OntologyAnnotation | None=None) -> None:
        this: ArcAssay = self
        this.technology_type_0040137 = n

    @property
    def TechnologyPlatform(self, __unit: None=None) -> OntologyAnnotation | None:
        this: ArcAssay = self
        return this.technology_platform_0040138

    @TechnologyPlatform.setter
    def TechnologyPlatform(self, n: OntologyAnnotation | None=None) -> None:
        this: ArcAssay = self
        this.technology_platform_0040138 = n

    @property
    def Datamap(self, __unit: None=None) -> Datamap | None:
        this: ArcAssay = self
        return this.datamap_0040139

    @Datamap.setter
    def Datamap(self, n: Datamap | None=None) -> None:
        this: ArcAssay = self
        this.datamap_0040139 = n

    @property
    def Performers(self, __unit: None=None) -> Array[Person]:
        this: ArcAssay = self
        return this.performers_0040140_002D1

    @Performers.setter
    def Performers(self, n: Array[Person]) -> None:
        this: ArcAssay = self
        this.performers_0040140_002D1 = n

    @property
    def Comments(self, __unit: None=None) -> Array[Comment]:
        this: ArcAssay = self
        return this.comments_0040141_002D1

    @Comments.setter
    def Comments(self, n: Array[Comment]) -> None:
        this: ArcAssay = self
        this.comments_0040141_002D1 = n

    @property
    def StaticHash(self, __unit: None=None) -> int:
        this: ArcAssay = self
        return this.static_hash

    @StaticHash.setter
    def StaticHash(self, h: int) -> None:
        this: ArcAssay = self
        this.static_hash = h or 0

    @staticmethod
    def init(identifier: str) -> ArcAssay:
        return ArcAssay(identifier)

    @staticmethod
    def create(identifier: str, title: str | None=None, description: str | None=None, measurement_type: OntologyAnnotation | None=None, technology_type: OntologyAnnotation | None=None, technology_platform: OntologyAnnotation | None=None, tables: Array[ArcTable] | None=None, datamap: Datamap | None=None, performers: Array[Person] | None=None, comments: Array[Comment] | None=None) -> ArcAssay:
        return ArcAssay(identifier, title, description, measurement_type, technology_type, technology_platform, tables, datamap, performers, comments)

    @staticmethod
    def make(identifier: str, title: str | None, description: str | None, measurement_type: OntologyAnnotation | None, technology_type: OntologyAnnotation | None, technology_platform: OntologyAnnotation | None, tables: Array[ArcTable], datamap: Datamap | None, performers: Array[Person], comments: Array[Comment]) -> ArcAssay:
        return ArcAssay(identifier, title, description, measurement_type, technology_type, technology_platform, tables, datamap, performers, comments)

    @staticmethod
    def FileName() -> str:
        return "isa.assay.xlsx"

    @property
    def StudiesRegisteredIn(self, __unit: None=None) -> Array[ArcStudy]:
        this: ArcAssay = self
        match_value: ArcInvestigation | None = this.Investigation
        if match_value is None:
            return []

        else: 
            i: ArcInvestigation = match_value
            def predicate(s: ArcStudy) -> bool:
                source: Array[str] = s.RegisteredAssayIdentifiers
                class ObjectExpr1087:
                    @property
                    def Equals(self) -> Callable[[str, str], bool]:
                        def _arrow1086(x: str, y: str) -> bool:
                            return x == y

                        return _arrow1086

                    @property
                    def GetHashCode(self) -> Callable[[str], int]:
                        return string_hash

                return contains(this.Identifier, source, ObjectExpr1087())

            return to_array(filter(predicate, i.Studies))


    @staticmethod
    def add_table(table: ArcTable, index: int | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1089(assay: ArcAssay) -> ArcAssay:
            c: ArcAssay = assay.Copy()
            c.AddTable(table, index)
            return c

        return _arrow1089

    @staticmethod
    def add_tables(tables: IEnumerable_1[ArcTable], index: int | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1092(assay: ArcAssay) -> ArcAssay:
            c: ArcAssay = assay.Copy()
            c.AddTables(tables, index)
            return c

        return _arrow1092

    @staticmethod
    def init_table(table_name: str, index: int | None=None) -> Callable[[ArcAssay], tuple[ArcAssay, ArcTable]]:
        def _arrow1094(assay: ArcAssay) -> tuple[ArcAssay, ArcTable]:
            c: ArcAssay = assay.Copy()
            return (c, c.InitTable(table_name, index))

        return _arrow1094

    @staticmethod
    def init_tables(table_names: IEnumerable_1[str], index: int | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1095(assay: ArcAssay) -> ArcAssay:
            c: ArcAssay = assay.Copy()
            c.InitTables(table_names, index)
            return c

        return _arrow1095

    @staticmethod
    def get_table_at(index: int) -> Callable[[ArcAssay], ArcTable]:
        def _arrow1096(assay: ArcAssay) -> ArcTable:
            new_assay: ArcAssay = assay.Copy()
            return new_assay.GetTableAt(index)

        return _arrow1096

    @staticmethod
    def get_table(name: str) -> Callable[[ArcAssay], ArcTable]:
        def _arrow1097(assay: ArcAssay) -> ArcTable:
            new_assay: ArcAssay = assay.Copy()
            return new_assay.GetTable(name)

        return _arrow1097

    @staticmethod
    def update_table_at(index: int, table: ArcTable) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1099(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.UpdateTableAt(index, table)
            return new_assay

        return _arrow1099

    @staticmethod
    def update_table(name: str, table: ArcTable) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1100(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.UpdateTable(name, table)
            return new_assay

        return _arrow1100

    @staticmethod
    def set_table_at(index: int, table: ArcTable) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1101(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.SetTableAt(index, table)
            return new_assay

        return _arrow1101

    @staticmethod
    def set_table(name: str, table: ArcTable) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1104(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.SetTable(name, table)
            return new_assay

        return _arrow1104

    @staticmethod
    def remove_table_at(index: int) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1105(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RemoveTableAt(index)
            return new_assay

        return _arrow1105

    @staticmethod
    def remove_table(name: str) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1106(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RemoveTable(name)
            return new_assay

        return _arrow1106

    @staticmethod
    def map_table_at(index: int, update_fun: Callable[[ArcTable], None]) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1107(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.MapTableAt(index, update_fun)
            return new_assay

        return _arrow1107

    @staticmethod
    def update_table_by(name: str, update_fun: Callable[[ArcTable], None]) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1108(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.MapTable(name, update_fun)
            return new_assay

        return _arrow1108

    @staticmethod
    def rename_table_at(index: int, new_name: str) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1109(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RenameTableAt(index, new_name)
            return new_assay

        return _arrow1109

    @staticmethod
    def rename_table(name: str, new_name: str) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1110(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RenameTable(name, new_name)
            return new_assay

        return _arrow1110

    @staticmethod
    def add_column_at(table_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None, column_index: int | None=None, force_replace: bool | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1111(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.AddColumnAt(table_index, header, cells, column_index, force_replace)
            return new_assay

        return _arrow1111

    @staticmethod
    def add_column(table_name: str, header: CompositeHeader, cells: Array[CompositeCell] | None=None, column_index: int | None=None, force_replace: bool | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1112(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.AddColumn(table_name, header, cells, column_index, force_replace)
            return new_assay

        return _arrow1112

    @staticmethod
    def remove_column_at(table_index: int, column_index: int) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1113(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RemoveColumnAt(table_index, column_index)
            return new_assay

        return _arrow1113

    @staticmethod
    def remove_column(table_name: str, column_index: int) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1114(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RemoveColumn(table_name, column_index)
            return new_assay

        return _arrow1114

    @staticmethod
    def update_column_at(table_index: int, column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1115(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.UpdateColumnAt(table_index, column_index, header, cells)
            return new_assay

        return _arrow1115

    @staticmethod
    def update_column(table_name: str, column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1116(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.UpdateColumn(table_name, column_index, header, cells)
            return new_assay

        return _arrow1116

    @staticmethod
    def get_column_at(table_index: int, column_index: int) -> Callable[[ArcAssay], CompositeColumn]:
        def _arrow1117(assay: ArcAssay) -> CompositeColumn:
            new_assay: ArcAssay = assay.Copy()
            return new_assay.GetColumnAt(table_index, column_index)

        return _arrow1117

    @staticmethod
    def get_column(table_name: str, column_index: int) -> Callable[[ArcAssay], CompositeColumn]:
        def _arrow1118(assay: ArcAssay) -> CompositeColumn:
            new_assay: ArcAssay = assay.Copy()
            return new_assay.GetColumn(table_name, column_index)

        return _arrow1118

    @staticmethod
    def add_row_at(table_index: int, cells: Array[CompositeCell] | None=None, row_index: int | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1119(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.AddRowAt(table_index, cells, row_index)
            return new_assay

        return _arrow1119

    @staticmethod
    def add_row(table_name: str, cells: Array[CompositeCell] | None=None, row_index: int | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1120(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.AddRow(table_name, cells, row_index)
            return new_assay

        return _arrow1120

    @staticmethod
    def remove_row_at(table_index: int, row_index: int) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1121(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RemoveColumnAt(table_index, row_index)
            return new_assay

        return _arrow1121

    @staticmethod
    def remove_row(table_name: str, row_index: int) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1122(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RemoveRow(table_name, row_index)
            return new_assay

        return _arrow1122

    @staticmethod
    def update_row_at(table_index: int, row_index: int, cells: Array[CompositeCell]) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1123(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.UpdateRowAt(table_index, row_index, cells)
            return new_assay

        return _arrow1123

    @staticmethod
    def update_row(table_name: str, row_index: int, cells: Array[CompositeCell]) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow1124(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.UpdateRow(table_name, row_index, cells)
            return new_assay

        return _arrow1124

    @staticmethod
    def get_row_at(table_index: int, row_index: int) -> Callable[[ArcAssay], Array[CompositeCell]]:
        def _arrow1125(assay: ArcAssay) -> Array[CompositeCell]:
            new_assay: ArcAssay = assay.Copy()
            return new_assay.GetRowAt(table_index, row_index)

        return _arrow1125

    @staticmethod
    def get_row(table_name: str, row_index: int) -> Callable[[ArcAssay], Array[CompositeCell]]:
        def _arrow1126(assay: ArcAssay) -> Array[CompositeCell]:
            new_assay: ArcAssay = assay.Copy()
            return new_assay.GetRow(table_name, row_index)

        return _arrow1126

    @staticmethod
    def set_performers(performers: Array[Person], assay: ArcAssay) -> ArcAssay:
        assay.Performers = performers
        return assay

    def Copy(self, __unit: None=None) -> ArcAssay:
        this: ArcAssay = self
        def f(c: ArcTable) -> ArcTable:
            return c.Copy()

        next_tables: Array[ArcTable] = ResizeArray_map(f, this.Tables)
        def f_1(c_1: Comment) -> Comment:
            return c_1.Copy()

        next_comments: Array[Comment] = ResizeArray_map(f_1, this.Comments)
        def mapping(d: Datamap) -> Datamap:
            return d.Copy()

        next_datamap: Datamap | None = map(mapping, this.Datamap)
        def f_2(c_2: Person) -> Person:
            return c_2.Copy()

        next_performers: Array[Person] = ResizeArray_map(f_2, this.Performers)
        identifier: str = this.Identifier
        title: str | None = this.Title
        description: str | None = this.Description
        measurement_type: OntologyAnnotation | None = this.MeasurementType
        technology_type: OntologyAnnotation | None = this.TechnologyType
        technology_platform: OntologyAnnotation | None = this.TechnologyPlatform
        return ArcAssay.make(identifier, title, description, measurement_type, technology_type, technology_platform, next_tables, next_datamap, next_performers, next_comments)

    def UpdateBy(self, assay: ArcAssay, only_replace_existing: bool | None=None, append_sequences: bool | None=None) -> None:
        this: ArcAssay = self
        only_replace_existing_1: bool = default_arg(only_replace_existing, False)
        append_sequences_1: bool = default_arg(append_sequences, False)
        update_always: bool = not only_replace_existing_1
        if True if (assay.Title is not None) else update_always:
            this.Title = assay.Title

        if True if (assay.Description is not None) else update_always:
            this.Description = assay.Description

        if True if (assay.MeasurementType is not None) else update_always:
            this.MeasurementType = assay.MeasurementType

        if True if (assay.TechnologyType is not None) else update_always:
            this.TechnologyType = assay.TechnologyType

        if True if (assay.TechnologyPlatform is not None) else update_always:
            this.TechnologyPlatform = assay.TechnologyPlatform

        if True if (len(assay.Tables) != 0) else update_always:
            s: Array[ArcTable]
            origin: Array[ArcTable] = this.Tables
            next_1: Array[ArcTable] = assay.Tables
            if not append_sequences_1:
                def f(x: ArcTable) -> ArcTable:
                    return x

                s = ResizeArray_map(f, next_1)

            else: 
                combined: Array[ArcTable] = []
                enumerator: Any = get_enumerator(origin)
                try: 
                    while enumerator.System_Collections_IEnumerator_MoveNext():
                        e: ArcTable = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1127:
                            @property
                            def Equals(self) -> Callable[[ArcTable, ArcTable], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[ArcTable], int]:
                                return safe_hash

                        if not contains_1(e, combined, ObjectExpr1127()):
                            (combined.append(e))


                finally: 
                    dispose(enumerator)

                enumerator_1: Any = get_enumerator(next_1)
                try: 
                    while enumerator_1.System_Collections_IEnumerator_MoveNext():
                        e_1: ArcTable = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1128:
                            @property
                            def Equals(self) -> Callable[[ArcTable, ArcTable], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[ArcTable], int]:
                                return safe_hash

                        if not contains_1(e_1, combined, ObjectExpr1128()):
                            (combined.append(e_1))


                finally: 
                    dispose(enumerator_1)

                s = combined

            this.Tables = s

        if True if (len(assay.Performers) != 0) else update_always:
            s_1: Array[Person]
            origin_1: Array[Person] = this.Performers
            next_1_1: Array[Person] = assay.Performers
            if not append_sequences_1:
                def f_1(x_3: Person) -> Person:
                    return x_3

                s_1 = ResizeArray_map(f_1, next_1_1)

            else: 
                combined_1: Array[Person] = []
                enumerator_2: Any = get_enumerator(origin_1)
                try: 
                    while enumerator_2.System_Collections_IEnumerator_MoveNext():
                        e_2: Person = enumerator_2.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1129:
                            @property
                            def Equals(self) -> Callable[[Person, Person], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[Person], int]:
                                return safe_hash

                        if not contains_1(e_2, combined_1, ObjectExpr1129()):
                            (combined_1.append(e_2))


                finally: 
                    dispose(enumerator_2)

                enumerator_1_1: Any = get_enumerator(next_1_1)
                try: 
                    while enumerator_1_1.System_Collections_IEnumerator_MoveNext():
                        e_1_1: Person = enumerator_1_1.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1130:
                            @property
                            def Equals(self) -> Callable[[Person, Person], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[Person], int]:
                                return safe_hash

                        if not contains_1(e_1_1, combined_1, ObjectExpr1130()):
                            (combined_1.append(e_1_1))


                finally: 
                    dispose(enumerator_1_1)

                s_1 = combined_1

            this.Performers = s_1

        if True if (len(assay.Comments) != 0) else update_always:
            s_2: Array[Comment]
            origin_2: Array[Comment] = this.Comments
            next_1_2: Array[Comment] = assay.Comments
            if not append_sequences_1:
                def f_2(x_6: Comment) -> Comment:
                    return x_6

                s_2 = ResizeArray_map(f_2, next_1_2)

            else: 
                combined_2: Array[Comment] = []
                enumerator_3: Any = get_enumerator(origin_2)
                try: 
                    while enumerator_3.System_Collections_IEnumerator_MoveNext():
                        e_3: Comment = enumerator_3.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1131:
                            @property
                            def Equals(self) -> Callable[[Comment, Comment], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[Comment], int]:
                                return safe_hash

                        if not contains_1(e_3, combined_2, ObjectExpr1131()):
                            (combined_2.append(e_3))


                finally: 
                    dispose(enumerator_3)

                enumerator_1_2: Any = get_enumerator(next_1_2)
                try: 
                    while enumerator_1_2.System_Collections_IEnumerator_MoveNext():
                        e_1_2: Comment = enumerator_1_2.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1132:
                            @property
                            def Equals(self) -> Callable[[Comment, Comment], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[Comment], int]:
                                return safe_hash

                        if not contains_1(e_1_2, combined_2, ObjectExpr1132()):
                            (combined_2.append(e_1_2))


                finally: 
                    dispose(enumerator_1_2)

                s_2 = combined_2

            this.Comments = s_2


    def __str__(self, __unit: None=None) -> str:
        this: ArcAssay = self
        arg: str = this.Identifier
        arg_1: str | None = this.Title
        arg_2: str | None = this.Description
        arg_3: OntologyAnnotation | None = this.MeasurementType
        arg_4: OntologyAnnotation | None = this.TechnologyType
        arg_5: OntologyAnnotation | None = this.TechnologyPlatform
        arg_6: Array[ArcTable] = this.Tables
        arg_7: Array[Person] = this.Performers
        arg_8: Array[Comment] = this.Comments
        return to_text(printf("ArcAssay({\r\n    Identifier = \"%s\",\r\n    Title = %A,\r\n    Description = %A,\r\n    MeasurementType = %A,\r\n    TechnologyType = %A,\r\n    TechnologyPlatform = %A,\r\n    Tables = %A,\r\n    Performers = %A,\r\n    Comments = %A\r\n})"))(arg)(arg_1)(arg_2)(arg_3)(arg_4)(arg_5)(arg_6)(arg_7)(arg_8)

    def AddToInvestigation(self, investigation: ArcInvestigation) -> None:
        this: ArcAssay = self
        this.Investigation = investigation

    def RemoveFromInvestigation(self, __unit: None=None) -> None:
        this: ArcAssay = self
        this.Investigation = None

    def UpdateReferenceByAssayFile(self, assay: ArcAssay, only_replace_existing: bool | None=None) -> None:
        this: ArcAssay = self
        update_always: bool = not default_arg(only_replace_existing, False)
        if True if (assay.Title is not None) else update_always:
            this.Title = assay.Title

        if True if (assay.Description is not None) else update_always:
            this.Description = assay.Description

        if True if (assay.MeasurementType is not None) else update_always:
            this.MeasurementType = assay.MeasurementType

        if True if (assay.TechnologyPlatform is not None) else update_always:
            this.TechnologyPlatform = assay.TechnologyPlatform

        if True if (assay.TechnologyType is not None) else update_always:
            this.TechnologyType = assay.TechnologyType

        if True if (len(assay.Tables) != 0) else update_always:
            this.Tables = assay.Tables

        if True if (len(assay.Comments) != 0) else update_always:
            this.Comments = assay.Comments

        this.Datamap = assay.Datamap
        if True if (len(assay.Performers) != 0) else update_always:
            this.Performers = assay.Performers


    def StructurallyEquals(self, other: ArcAssay) -> bool:
        this: ArcAssay = self
        def predicate(x: bool) -> bool:
            return x == True

        def _arrow1135(__unit: None=None) -> bool:
            a: IEnumerable_1[ArcTable] = this.Tables
            b: IEnumerable_1[ArcTable] = other.Tables
            def folder(acc: bool, e: bool) -> bool:
                if acc:
                    return e

                else: 
                    return False


            def _arrow1134(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1133(i_1: int) -> bool:
                    return equals(item(i_1, a), item(i_1, b))

                return map_1(_arrow1133, range_big_int(0, 1, length(a) - 1))

            return fold(folder, True, to_list(delay(_arrow1134))) if (length(a) == length(b)) else False

        def _arrow1138(__unit: None=None) -> bool:
            a_1: IEnumerable_1[Person] = this.Performers
            b_1: IEnumerable_1[Person] = other.Performers
            def folder_1(acc_1: bool, e_1: bool) -> bool:
                if acc_1:
                    return e_1

                else: 
                    return False


            def _arrow1137(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1136(i_2: int) -> bool:
                    return equals(item(i_2, a_1), item(i_2, b_1))

                return map_1(_arrow1136, range_big_int(0, 1, length(a_1) - 1))

            return fold(folder_1, True, to_list(delay(_arrow1137))) if (length(a_1) == length(b_1)) else False

        def _arrow1141(__unit: None=None) -> bool:
            a_2: IEnumerable_1[Comment] = this.Comments
            b_2: IEnumerable_1[Comment] = other.Comments
            def folder_2(acc_2: bool, e_2: bool) -> bool:
                if acc_2:
                    return e_2

                else: 
                    return False


            def _arrow1140(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1139(i_3: int) -> bool:
                    return equals(item(i_3, a_2), item(i_3, b_2))

                return map_1(_arrow1139, range_big_int(0, 1, length(a_2) - 1))

            return fold(folder_2, True, to_list(delay(_arrow1140))) if (length(a_2) == length(b_2)) else False

        return for_all(predicate, to_enumerable([this.Identifier == other.Identifier, equals(this.Title, other.Title), equals(this.Description, other.Description), equals(this.MeasurementType, other.MeasurementType), equals(this.TechnologyType, other.TechnologyType), equals(this.TechnologyPlatform, other.TechnologyPlatform), equals(this.Datamap, other.Datamap), _arrow1135(), _arrow1138(), _arrow1141()]))

    def ReferenceEquals(self, other: ArcAssay) -> bool:
        this: ArcAssay = self
        return this is other

    def __eq__(self, other: Any=None) -> bool:
        this: ArcAssay = self
        return this.StructurallyEquals(other) if isinstance(other, ArcAssay) else False

    def GetLightHashCode(self, __unit: None=None) -> Any:
        this: ArcAssay = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.MeasurementType), box_hash_option(this.TechnologyType), box_hash_option(this.TechnologyPlatform), box_hash_seq(this.Tables), box_hash_seq(this.Performers), box_hash_seq(this.Comments)])

    def __hash__(self, __unit: None=None) -> Any:
        this: ArcAssay = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.MeasurementType), box_hash_option(this.TechnologyType), box_hash_option(this.TechnologyPlatform), box_hash_option(this.Datamap), box_hash_seq(this.Tables), box_hash_seq(this.Performers), box_hash_seq(this.Comments)])


ArcAssay_reflection = _expr1143

def ArcAssay__ctor_Z69B192EC(identifier: str, title: str | None=None, description: str | None=None, measurement_type: OntologyAnnotation | None=None, technology_type: OntologyAnnotation | None=None, technology_platform: OntologyAnnotation | None=None, tables: Array[ArcTable] | None=None, datamap: Datamap | None=None, performers: Array[Person] | None=None, comments: Array[Comment] | None=None) -> ArcAssay:
    return ArcAssay(identifier, title, description, measurement_type, technology_type, technology_platform, tables, datamap, performers, comments)


def _expr1212() -> TypeInfo:
    return class_type("ARCtrl.ArcStudy", None, ArcStudy, ArcTables_reflection())


class ArcStudy(ArcTables):
    def __init__(self, identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, study_design_descriptors: Array[OntologyAnnotation] | None=None, tables: Array[ArcTable] | None=None, datamap: Datamap | None=None, registered_assay_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None) -> None:
        super().__init__(default_arg(tables, []))
        publications_1: Array[Publication] = default_arg(publications, [])
        contacts_1: Array[Person] = default_arg(contacts, [])
        study_design_descriptors_1: Array[OntologyAnnotation] = default_arg(study_design_descriptors, [])
        registered_assay_identifiers_1: Array[str] = default_arg(registered_assay_identifiers, [])
        comments_1: Array[Comment] = default_arg(comments, [])
        def _arrow1211(__unit: None=None) -> str:
            identifier_1: str = identifier.strip()
            check_valid_characters(identifier_1)
            return identifier_1

        self.identifier_0040579: str = _arrow1211()
        self.investigation: ArcInvestigation | None = None
        self.title_0040584: str | None = title
        self.description_0040585: str | None = description
        self.submission_date_0040586: str | None = submission_date
        self.public_release_date_0040587: str | None = public_release_date
        self.publications_0040588_002D1: Array[Publication] = publications_1
        self.contacts_0040589_002D1: Array[Person] = contacts_1
        self.study_design_descriptors_0040590_002D1: Array[OntologyAnnotation] = study_design_descriptors_1
        self.datamap_0040591: Datamap | None = datamap
        self.registered_assay_identifiers_0040592_002D1: Array[str] = registered_assay_identifiers_1
        self.comments_0040593_002D1: Array[Comment] = comments_1
        self.static_hash: int = 0

    @property
    def Identifier(self, __unit: None=None) -> str:
        this: ArcStudy = self
        return this.identifier_0040579

    @Identifier.setter
    def Identifier(self, i: str) -> None:
        this: ArcStudy = self
        this.identifier_0040579 = i

    @property
    def Investigation(self, __unit: None=None) -> ArcInvestigation | None:
        this: ArcStudy = self
        return this.investigation

    @Investigation.setter
    def Investigation(self, i: ArcInvestigation | None=None) -> None:
        this: ArcStudy = self
        this.investigation = i

    @property
    def Title(self, __unit: None=None) -> str | None:
        this: ArcStudy = self
        return this.title_0040584

    @Title.setter
    def Title(self, n: str | None=None) -> None:
        this: ArcStudy = self
        this.title_0040584 = n

    @property
    def Description(self, __unit: None=None) -> str | None:
        this: ArcStudy = self
        return this.description_0040585

    @Description.setter
    def Description(self, n: str | None=None) -> None:
        this: ArcStudy = self
        this.description_0040585 = n

    @property
    def SubmissionDate(self, __unit: None=None) -> str | None:
        this: ArcStudy = self
        return this.submission_date_0040586

    @SubmissionDate.setter
    def SubmissionDate(self, n: str | None=None) -> None:
        this: ArcStudy = self
        this.submission_date_0040586 = n

    @property
    def PublicReleaseDate(self, __unit: None=None) -> str | None:
        this: ArcStudy = self
        return this.public_release_date_0040587

    @PublicReleaseDate.setter
    def PublicReleaseDate(self, n: str | None=None) -> None:
        this: ArcStudy = self
        this.public_release_date_0040587 = n

    @property
    def Publications(self, __unit: None=None) -> Array[Publication]:
        this: ArcStudy = self
        return this.publications_0040588_002D1

    @Publications.setter
    def Publications(self, n: Array[Publication]) -> None:
        this: ArcStudy = self
        this.publications_0040588_002D1 = n

    @property
    def Contacts(self, __unit: None=None) -> Array[Person]:
        this: ArcStudy = self
        return this.contacts_0040589_002D1

    @Contacts.setter
    def Contacts(self, n: Array[Person]) -> None:
        this: ArcStudy = self
        this.contacts_0040589_002D1 = n

    @property
    def StudyDesignDescriptors(self, __unit: None=None) -> Array[OntologyAnnotation]:
        this: ArcStudy = self
        return this.study_design_descriptors_0040590_002D1

    @StudyDesignDescriptors.setter
    def StudyDesignDescriptors(self, n: Array[OntologyAnnotation]) -> None:
        this: ArcStudy = self
        this.study_design_descriptors_0040590_002D1 = n

    @property
    def Datamap(self, __unit: None=None) -> Datamap | None:
        this: ArcStudy = self
        return this.datamap_0040591

    @Datamap.setter
    def Datamap(self, n: Datamap | None=None) -> None:
        this: ArcStudy = self
        this.datamap_0040591 = n

    @property
    def RegisteredAssayIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcStudy = self
        return this.registered_assay_identifiers_0040592_002D1

    @RegisteredAssayIdentifiers.setter
    def RegisteredAssayIdentifiers(self, n: Array[str]) -> None:
        this: ArcStudy = self
        this.registered_assay_identifiers_0040592_002D1 = n

    @property
    def Comments(self, __unit: None=None) -> Array[Comment]:
        this: ArcStudy = self
        return this.comments_0040593_002D1

    @Comments.setter
    def Comments(self, n: Array[Comment]) -> None:
        this: ArcStudy = self
        this.comments_0040593_002D1 = n

    @property
    def StaticHash(self, __unit: None=None) -> int:
        this: ArcStudy = self
        return this.static_hash

    @StaticHash.setter
    def StaticHash(self, h: int) -> None:
        this: ArcStudy = self
        this.static_hash = h or 0

    @staticmethod
    def init(identifier: str) -> ArcStudy:
        return ArcStudy(identifier)

    @staticmethod
    def create(identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, study_design_descriptors: Array[OntologyAnnotation] | None=None, tables: Array[ArcTable] | None=None, datamap: Datamap | None=None, registered_assay_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None) -> ArcStudy:
        return ArcStudy(identifier, title, description, submission_date, public_release_date, publications, contacts, study_design_descriptors, tables, datamap, registered_assay_identifiers, comments)

    @staticmethod
    def make(identifier: str, title: str | None, description: str | None, submission_date: str | None, public_release_date: str | None, publications: Array[Publication], contacts: Array[Person], study_design_descriptors: Array[OntologyAnnotation], tables: Array[ArcTable], datamap: Datamap | None, registered_assay_identifiers: Array[str], comments: Array[Comment]) -> ArcStudy:
        return ArcStudy(identifier, title, description, submission_date, public_release_date, publications, contacts, study_design_descriptors, tables, datamap, registered_assay_identifiers, comments)

    @property
    def is_empty(self, __unit: None=None) -> bool:
        this: ArcStudy = self
        return (len(this.Comments) == 0) if ((len(this.RegisteredAssayIdentifiers) == 0) if ((len(this.Tables) == 0) if ((len(this.StudyDesignDescriptors) == 0) if ((len(this.Contacts) == 0) if ((len(this.Publications) == 0) if (equals(this.PublicReleaseDate, None) if (equals(this.SubmissionDate, None) if (equals(this.Description, None) if equals(this.Title, None) else False) else False) else False) else False) else False) else False) else False) else False) else False

    @staticmethod
    def FileName() -> str:
        return "isa.study.xlsx"

    @property
    def RegisteredAssayIdentifierCount(self, __unit: None=None) -> int:
        this: ArcStudy = self
        return len(this.RegisteredAssayIdentifiers)

    @property
    def RegisteredAssayCount(self, __unit: None=None) -> int:
        this: ArcStudy = self
        return len(this.RegisteredAssays)

    @property
    def RegisteredAssays(self, __unit: None=None) -> Array[ArcAssay]:
        this: ArcStudy = self
        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        def chooser(assay_identifier: str) -> ArcAssay | None:
            return inv.TryGetAssay(assay_identifier)

        return list(choose(chooser, this.RegisteredAssayIdentifiers))

    @property
    def VacantAssayIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcStudy = self
        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        def predicate(arg: str) -> bool:
            return not inv.ContainsAssay(arg)

        return list(filter(predicate, this.RegisteredAssayIdentifiers))

    def AddRegisteredAssay(self, assay: ArcAssay) -> None:
        this: ArcStudy = self
        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        inv.AddAssay(assay)
        inv.RegisterAssay(this.Identifier, assay.Identifier)

    @staticmethod
    def add_registered_assay(assay: ArcAssay) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1144(study: ArcStudy) -> ArcStudy:
            new_study: ArcStudy = study.Copy()
            new_study.AddRegisteredAssay(assay)
            return new_study

        return _arrow1144

    def InitRegisteredAssay(self, assay_identifier: str) -> ArcAssay:
        this: ArcStudy = self
        assay: ArcAssay = ArcAssay(assay_identifier)
        this.AddRegisteredAssay(assay)
        return assay

    @staticmethod
    def init_registered_assay(assay_identifier: str) -> Callable[[ArcStudy], tuple[ArcStudy, ArcAssay]]:
        def _arrow1145(study: ArcStudy) -> tuple[ArcStudy, ArcAssay]:
            copy: ArcStudy = study.Copy()
            return (copy, copy.InitRegisteredAssay(assay_identifier))

        return _arrow1145

    def RegisterAssay(self, assay_identifier: str) -> None:
        this: ArcStudy = self
        class ObjectExpr1147:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1146(x: str, y: str) -> bool:
                    return x == y

                return _arrow1146

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if contains(assay_identifier, this.RegisteredAssayIdentifiers, ObjectExpr1147()):
            raise Exception(("Assay `" + assay_identifier) + "` is already registered on the study.")

        (this.RegisteredAssayIdentifiers.append(assay_identifier))

    @staticmethod
    def register_assay(assay_identifier: str) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1148(study: ArcStudy) -> ArcStudy:
            copy: ArcStudy = study.Copy()
            copy.RegisterAssay(assay_identifier)
            return copy

        return _arrow1148

    def DeregisterAssay(self, assay_identifier: str) -> None:
        this: ArcStudy = self
        class ObjectExpr1150:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1149(x: str, y: str) -> bool:
                    return x == y

                return _arrow1149

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        ignore(remove_in_place(assay_identifier, this.RegisteredAssayIdentifiers, ObjectExpr1150()))

    @staticmethod
    def deregister_assay(assay_identifier: str) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1151(study: ArcStudy) -> ArcStudy:
            copy: ArcStudy = study.Copy()
            copy.DeregisterAssay(assay_identifier)
            return copy

        return _arrow1151

    def GetRegisteredAssay(self, assay_identifier: str) -> ArcAssay:
        this: ArcStudy = self
        class ObjectExpr1153:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1152(x: str, y: str) -> bool:
                    return x == y

                return _arrow1152

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if not contains(assay_identifier, this.RegisteredAssayIdentifiers, ObjectExpr1153()):
            raise Exception(("Assay `" + assay_identifier) + "` is not registered on the study.")

        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        return inv.GetAssay(assay_identifier)

    @staticmethod
    def get_registered_assay(assay_identifier: str) -> Callable[[ArcStudy], ArcAssay]:
        def _arrow1154(study: ArcStudy) -> ArcAssay:
            copy: ArcStudy = study.Copy()
            return copy.GetRegisteredAssay(assay_identifier)

        return _arrow1154

    @staticmethod
    def get_registered_assays(__unit: None=None) -> Callable[[ArcStudy], Array[ArcAssay]]:
        def _arrow1155(study: ArcStudy) -> Array[ArcAssay]:
            copy: ArcStudy = study.Copy()
            return copy.RegisteredAssays

        return _arrow1155

    def GetRegisteredAssaysOrIdentifier(self, __unit: None=None) -> Array[ArcAssay]:
        this: ArcStudy = self
        match_value: ArcInvestigation | None = this.Investigation
        if match_value is None:
            def f_1(identifier_1: str) -> ArcAssay:
                return ArcAssay.init(identifier_1)

            return ResizeArray_map(f_1, this.RegisteredAssayIdentifiers)

        else: 
            i: ArcInvestigation = match_value
            def f(identifier: str) -> ArcAssay:
                match_value_1: ArcAssay | None = i.TryGetAssay(identifier)
                if match_value_1 is None:
                    return ArcAssay.init(identifier)

                else: 
                    return match_value_1


            return ResizeArray_map(f, this.RegisteredAssayIdentifiers)


    @staticmethod
    def get_registered_assays_or_identifier(__unit: None=None) -> Callable[[ArcStudy], Array[ArcAssay]]:
        def _arrow1156(study: ArcStudy) -> Array[ArcAssay]:
            copy: ArcStudy = study.Copy()
            return copy.GetRegisteredAssaysOrIdentifier()

        return _arrow1156

    @staticmethod
    def add_table(table: ArcTable, index: int | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1157(study: ArcStudy) -> ArcStudy:
            c: ArcStudy = study.Copy()
            c.AddTable(table, index)
            return c

        return _arrow1157

    @staticmethod
    def add_tables(tables: IEnumerable_1[ArcTable], index: int | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1158(study: ArcStudy) -> ArcStudy:
            c: ArcStudy = study.Copy()
            c.AddTables(tables, index)
            return c

        return _arrow1158

    @staticmethod
    def init_table(table_name: str, index: int | None=None) -> Callable[[ArcStudy], tuple[ArcStudy, ArcTable]]:
        def _arrow1159(study: ArcStudy) -> tuple[ArcStudy, ArcTable]:
            c: ArcStudy = study.Copy()
            return (c, c.InitTable(table_name, index))

        return _arrow1159

    @staticmethod
    def init_tables(table_names: IEnumerable_1[str], index: int | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1160(study: ArcStudy) -> ArcStudy:
            c: ArcStudy = study.Copy()
            c.InitTables(table_names, index)
            return c

        return _arrow1160

    @staticmethod
    def get_table_at(index: int) -> Callable[[ArcStudy], ArcTable]:
        def _arrow1161(study: ArcStudy) -> ArcTable:
            new_assay: ArcStudy = study.Copy()
            return new_assay.GetTableAt(index)

        return _arrow1161

    @staticmethod
    def get_table(name: str) -> Callable[[ArcStudy], ArcTable]:
        def _arrow1162(study: ArcStudy) -> ArcTable:
            new_assay: ArcStudy = study.Copy()
            return new_assay.GetTable(name)

        return _arrow1162

    @staticmethod
    def update_table_at(index: int, table: ArcTable) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1163(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.UpdateTableAt(index, table)
            return new_assay

        return _arrow1163

    @staticmethod
    def update_table(name: str, table: ArcTable) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1164(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.UpdateTable(name, table)
            return new_assay

        return _arrow1164

    @staticmethod
    def set_table_at(index: int, table: ArcTable) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1165(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.SetTableAt(index, table)
            return new_assay

        return _arrow1165

    @staticmethod
    def set_table(name: str, table: ArcTable) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1166(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.SetTable(name, table)
            return new_assay

        return _arrow1166

    @staticmethod
    def remove_table_at(index: int) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1167(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RemoveTableAt(index)
            return new_assay

        return _arrow1167

    @staticmethod
    def remove_table(name: str) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1168(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RemoveTable(name)
            return new_assay

        return _arrow1168

    @staticmethod
    def map_table_at(index: int, update_fun: Callable[[ArcTable], None]) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1169(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.MapTableAt(index, update_fun)
            return new_assay

        return _arrow1169

    @staticmethod
    def map_table(name: str, update_fun: Callable[[ArcTable], None]) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1170(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.MapTable(name, update_fun)
            return new_assay

        return _arrow1170

    @staticmethod
    def rename_table_at(index: int, new_name: str) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1171(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RenameTableAt(index, new_name)
            return new_assay

        return _arrow1171

    @staticmethod
    def rename_table(name: str, new_name: str) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1172(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RenameTable(name, new_name)
            return new_assay

        return _arrow1172

    @staticmethod
    def add_column_at(table_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None, column_index: int | None=None, force_replace: bool | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1173(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.AddColumnAt(table_index, header, cells, column_index, force_replace)
            return new_assay

        return _arrow1173

    @staticmethod
    def add_column(table_name: str, header: CompositeHeader, cells: Array[CompositeCell] | None=None, column_index: int | None=None, force_replace: bool | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1174(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.AddColumn(table_name, header, cells, column_index, force_replace)
            return new_assay

        return _arrow1174

    @staticmethod
    def remove_column_at(table_index: int, column_index: int) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1175(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RemoveColumnAt(table_index, column_index)
            return new_assay

        return _arrow1175

    @staticmethod
    def remove_column(table_name: str, column_index: int) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1176(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RemoveColumn(table_name, column_index)
            return new_assay

        return _arrow1176

    @staticmethod
    def update_column_at(table_index: int, column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1177(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.UpdateColumnAt(table_index, column_index, header, cells)
            return new_assay

        return _arrow1177

    @staticmethod
    def update_column(table_name: str, column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1178(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.UpdateColumn(table_name, column_index, header, cells)
            return new_assay

        return _arrow1178

    @staticmethod
    def get_column_at(table_index: int, column_index: int) -> Callable[[ArcStudy], CompositeColumn]:
        def _arrow1179(study: ArcStudy) -> CompositeColumn:
            new_assay: ArcStudy = study.Copy()
            return new_assay.GetColumnAt(table_index, column_index)

        return _arrow1179

    @staticmethod
    def get_column(table_name: str, column_index: int) -> Callable[[ArcStudy], CompositeColumn]:
        def _arrow1180(study: ArcStudy) -> CompositeColumn:
            new_assay: ArcStudy = study.Copy()
            return new_assay.GetColumn(table_name, column_index)

        return _arrow1180

    @staticmethod
    def add_row_at(table_index: int, cells: Array[CompositeCell] | None=None, row_index: int | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1181(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.AddRowAt(table_index, cells, row_index)
            return new_assay

        return _arrow1181

    @staticmethod
    def add_row(table_name: str, cells: Array[CompositeCell] | None=None, row_index: int | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1182(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.AddRow(table_name, cells, row_index)
            return new_assay

        return _arrow1182

    @staticmethod
    def remove_row_at(table_index: int, row_index: int) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1184(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RemoveColumnAt(table_index, row_index)
            return new_assay

        return _arrow1184

    @staticmethod
    def remove_row(table_name: str, row_index: int) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1185(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RemoveRow(table_name, row_index)
            return new_assay

        return _arrow1185

    @staticmethod
    def update_row_at(table_index: int, row_index: int, cells: Array[CompositeCell]) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1186(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.UpdateRowAt(table_index, row_index, cells)
            return new_assay

        return _arrow1186

    @staticmethod
    def update_row(table_name: str, row_index: int, cells: Array[CompositeCell]) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow1187(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.UpdateRow(table_name, row_index, cells)
            return new_assay

        return _arrow1187

    @staticmethod
    def get_row_at(table_index: int, row_index: int) -> Callable[[ArcStudy], Array[CompositeCell]]:
        def _arrow1189(study: ArcStudy) -> Array[CompositeCell]:
            new_assay: ArcStudy = study.Copy()
            return new_assay.GetRowAt(table_index, row_index)

        return _arrow1189

    @staticmethod
    def get_row(table_name: str, row_index: int) -> Callable[[ArcStudy], Array[CompositeCell]]:
        def _arrow1190(study: ArcStudy) -> Array[CompositeCell]:
            new_assay: ArcStudy = study.Copy()
            return new_assay.GetRow(table_name, row_index)

        return _arrow1190

    def AddToInvestigation(self, investigation: ArcInvestigation) -> None:
        this: ArcStudy = self
        this.Investigation = investigation

    def RemoveFromInvestigation(self, __unit: None=None) -> None:
        this: ArcStudy = self
        this.Investigation = None

    def Copy(self, copy_investigation_ref: bool | None=None) -> ArcStudy:
        this: ArcStudy = self
        copy_investigation_ref_1: bool = default_arg(copy_investigation_ref, False)
        next_tables: Array[ArcTable] = []
        next_assay_identifiers: Array[str] = list(this.RegisteredAssayIdentifiers)
        enumerator: Any = get_enumerator(this.Tables)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                table: ArcTable = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                copy: ArcTable = table.Copy()
                (next_tables.append(copy))

        finally: 
            dispose(enumerator)

        def f(c: Comment) -> Comment:
            return c.Copy()

        next_comments: Array[Comment] = ResizeArray_map(f, this.Comments)
        def f_1(c_1: Person) -> Person:
            return c_1.Copy()

        next_contacts: Array[Person] = ResizeArray_map(f_1, this.Contacts)
        def f_2(c_2: Publication) -> Publication:
            return c_2.Copy()

        next_publications: Array[Publication] = ResizeArray_map(f_2, this.Publications)
        def f_3(c_3: OntologyAnnotation) -> OntologyAnnotation:
            return c_3.Copy()

        next_study_design_descriptors: Array[OntologyAnnotation] = ResizeArray_map(f_3, this.StudyDesignDescriptors)
        def mapping(d: Datamap) -> Datamap:
            return d.Copy()

        next_datamap: Datamap | None = map(mapping, this.Datamap)
        study: ArcStudy
        identifier: str = this.Identifier
        title: str | None = this.Title
        description: str | None = this.Description
        submission_date: str | None = this.SubmissionDate
        public_release_date: str | None = this.PublicReleaseDate
        study = ArcStudy.make(identifier, title, description, submission_date, public_release_date, next_publications, next_contacts, next_study_design_descriptors, next_tables, next_datamap, next_assay_identifiers, next_comments)
        if copy_investigation_ref_1:
            study.Investigation = this.Investigation

        return study

    def UpdateReferenceByStudyFile(self, study: ArcStudy, only_replace_existing: bool | None=None, keep_unused_ref_tables: bool | None=None) -> None:
        this: ArcStudy = self
        update_always: bool = not default_arg(only_replace_existing, False)
        if True if (study.Title is not None) else update_always:
            this.Title = study.Title

        if True if (study.Description is not None) else update_always:
            this.Description = study.Description

        if True if (study.SubmissionDate is not None) else update_always:
            this.SubmissionDate = study.SubmissionDate

        if True if (study.PublicReleaseDate is not None) else update_always:
            this.PublicReleaseDate = study.PublicReleaseDate

        if True if (len(study.Publications) != 0) else update_always:
            this.Publications = study.Publications

        if True if (len(study.Contacts) != 0) else update_always:
            this.Contacts = study.Contacts

        if True if (len(study.StudyDesignDescriptors) != 0) else update_always:
            this.StudyDesignDescriptors = study.StudyDesignDescriptors

        if True if (len(study.Tables) != 0) else update_always:
            tables: ArcTables = ArcTables.update_reference_tables_by_sheets(ArcTables(this.Tables), ArcTables(study.Tables), keep_unused_ref_tables)
            this.Tables = tables.Tables

        this.Datamap = study.Datamap
        if True if (len(study.RegisteredAssayIdentifiers) != 0) else update_always:
            this.RegisteredAssayIdentifiers = study.RegisteredAssayIdentifiers

        if True if (len(study.Comments) != 0) else update_always:
            this.Comments = study.Comments


    def StructurallyEquals(self, other: ArcStudy) -> bool:
        this: ArcStudy = self
        def predicate(x: bool) -> bool:
            return x == True

        def _arrow1195(__unit: None=None) -> bool:
            a: IEnumerable_1[Publication] = this.Publications
            b: IEnumerable_1[Publication] = other.Publications
            def folder(acc: bool, e: bool) -> bool:
                if acc:
                    return e

                else: 
                    return False


            def _arrow1194(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1193(i_1: int) -> bool:
                    return equals(item(i_1, a), item(i_1, b))

                return map_1(_arrow1193, range_big_int(0, 1, length(a) - 1))

            return fold(folder, True, to_list(delay(_arrow1194))) if (length(a) == length(b)) else False

        def _arrow1198(__unit: None=None) -> bool:
            a_1: IEnumerable_1[Person] = this.Contacts
            b_1: IEnumerable_1[Person] = other.Contacts
            def folder_1(acc_1: bool, e_1: bool) -> bool:
                if acc_1:
                    return e_1

                else: 
                    return False


            def _arrow1197(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1196(i_2: int) -> bool:
                    return equals(item(i_2, a_1), item(i_2, b_1))

                return map_1(_arrow1196, range_big_int(0, 1, length(a_1) - 1))

            return fold(folder_1, True, to_list(delay(_arrow1197))) if (length(a_1) == length(b_1)) else False

        def _arrow1201(__unit: None=None) -> bool:
            a_2: IEnumerable_1[OntologyAnnotation] = this.StudyDesignDescriptors
            b_2: IEnumerable_1[OntologyAnnotation] = other.StudyDesignDescriptors
            def folder_2(acc_2: bool, e_2: bool) -> bool:
                if acc_2:
                    return e_2

                else: 
                    return False


            def _arrow1200(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1199(i_3: int) -> bool:
                    return equals(item(i_3, a_2), item(i_3, b_2))

                return map_1(_arrow1199, range_big_int(0, 1, length(a_2) - 1))

            return fold(folder_2, True, to_list(delay(_arrow1200))) if (length(a_2) == length(b_2)) else False

        def _arrow1204(__unit: None=None) -> bool:
            a_3: IEnumerable_1[ArcTable] = this.Tables
            b_3: IEnumerable_1[ArcTable] = other.Tables
            def folder_3(acc_3: bool, e_3: bool) -> bool:
                if acc_3:
                    return e_3

                else: 
                    return False


            def _arrow1203(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1202(i_4: int) -> bool:
                    return equals(item(i_4, a_3), item(i_4, b_3))

                return map_1(_arrow1202, range_big_int(0, 1, length(a_3) - 1))

            return fold(folder_3, True, to_list(delay(_arrow1203))) if (length(a_3) == length(b_3)) else False

        def _arrow1207(__unit: None=None) -> bool:
            a_4: IEnumerable_1[str] = this.RegisteredAssayIdentifiers
            b_4: IEnumerable_1[str] = other.RegisteredAssayIdentifiers
            def folder_4(acc_4: bool, e_4: bool) -> bool:
                if acc_4:
                    return e_4

                else: 
                    return False


            def _arrow1206(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1205(i_5: int) -> bool:
                    return item(i_5, a_4) == item(i_5, b_4)

                return map_1(_arrow1205, range_big_int(0, 1, length(a_4) - 1))

            return fold(folder_4, True, to_list(delay(_arrow1206))) if (length(a_4) == length(b_4)) else False

        def _arrow1210(__unit: None=None) -> bool:
            a_5: IEnumerable_1[Comment] = this.Comments
            b_5: IEnumerable_1[Comment] = other.Comments
            def folder_5(acc_5: bool, e_5: bool) -> bool:
                if acc_5:
                    return e_5

                else: 
                    return False


            def _arrow1209(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1208(i_6: int) -> bool:
                    return equals(item(i_6, a_5), item(i_6, b_5))

                return map_1(_arrow1208, range_big_int(0, 1, length(a_5) - 1))

            return fold(folder_5, True, to_list(delay(_arrow1209))) if (length(a_5) == length(b_5)) else False

        return for_all(predicate, to_enumerable([this.Identifier == other.Identifier, equals(this.Title, other.Title), equals(this.Description, other.Description), equals(this.SubmissionDate, other.SubmissionDate), equals(this.PublicReleaseDate, other.PublicReleaseDate), equals(this.Datamap, other.Datamap), _arrow1195(), _arrow1198(), _arrow1201(), _arrow1204(), _arrow1207(), _arrow1210()]))

    def ReferenceEquals(self, other: ArcStudy) -> bool:
        this: ArcStudy = self
        return this is other

    def __str__(self, __unit: None=None) -> str:
        this: ArcStudy = self
        arg: str = this.Identifier
        arg_1: str | None = this.Title
        arg_2: str | None = this.Description
        arg_3: str | None = this.SubmissionDate
        arg_4: str | None = this.PublicReleaseDate
        arg_5: Array[Publication] = this.Publications
        arg_6: Array[Person] = this.Contacts
        arg_7: Array[OntologyAnnotation] = this.StudyDesignDescriptors
        arg_8: Array[ArcTable] = this.Tables
        arg_9: Array[str] = this.RegisteredAssayIdentifiers
        arg_10: Array[Comment] = this.Comments
        return to_text(printf("ArcStudy {\r\n    Identifier = %A,\r\n    Title = %A,\r\n    Description = %A,\r\n    SubmissionDate = %A,\r\n    PublicReleaseDate = %A,\r\n    Publications = %A,\r\n    Contacts = %A,\r\n    StudyDesignDescriptors = %A,\r\n    Tables = %A,\r\n    RegisteredAssayIdentifiers = %A,\r\n    Comments = %A,\r\n}"))(arg)(arg_1)(arg_2)(arg_3)(arg_4)(arg_5)(arg_6)(arg_7)(arg_8)(arg_9)(arg_10)

    def __eq__(self, other: Any=None) -> bool:
        this: ArcStudy = self
        return this.StructurallyEquals(other) if isinstance(other, ArcStudy) else False

    def __hash__(self, __unit: None=None) -> Any:
        this: ArcStudy = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.SubmissionDate), box_hash_option(this.PublicReleaseDate), box_hash_option(this.Datamap), box_hash_seq(this.Publications), box_hash_seq(this.Contacts), box_hash_seq(this.StudyDesignDescriptors), box_hash_seq(this.Tables), box_hash_seq(this.RegisteredAssayIdentifiers), box_hash_seq(this.Comments)])

    def GetLightHashCode(self, __unit: None=None) -> Any:
        this: ArcStudy = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.SubmissionDate), box_hash_option(this.PublicReleaseDate), box_hash_seq(this.Publications), box_hash_seq(this.Contacts), box_hash_seq(this.StudyDesignDescriptors), box_hash_seq(this.Tables), box_hash_seq(this.RegisteredAssayIdentifiers), box_hash_seq(this.Comments)])


ArcStudy_reflection = _expr1212

def ArcStudy__ctor_Z273F64C5(identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, study_design_descriptors: Array[OntologyAnnotation] | None=None, tables: Array[ArcTable] | None=None, datamap: Datamap | None=None, registered_assay_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None) -> ArcStudy:
    return ArcStudy(identifier, title, description, submission_date, public_release_date, publications, contacts, study_design_descriptors, tables, datamap, registered_assay_identifiers, comments)


def _expr1242() -> TypeInfo:
    return class_type("ARCtrl.ArcWorkflow", None, ArcWorkflow)


class ArcWorkflow:
    def __init__(self, identifier: str, title: str | None=None, description: str | None=None, workflow_type: OntologyAnnotation | None=None, uri: str | None=None, version: str | None=None, sub_workflow_identifiers: Array[str] | None=None, parameters: Array[OntologyAnnotation] | None=None, components: Array[Component] | None=None, datamap: Datamap | None=None, contacts: Array[Person] | None=None, cwl_description: CWLProcessingUnit | None=None, comments: Array[Comment] | None=None) -> None:
        def _arrow1241(__unit: None=None) -> str:
            identifier_1: str = identifier.strip()
            check_valid_characters(identifier_1)
            return identifier_1

        self.identifier_00401151: str = _arrow1241()
        self.investigation: ArcInvestigation | None = None
        self.title_00401156: str | None = title
        self.description_00401157: str | None = description
        self.sub_workflow_identifiers_00401158: Array[str] = default_arg(sub_workflow_identifiers, [])
        self.workflow_type_00401159: OntologyAnnotation | None = workflow_type
        self.uri_00401160: str | None = uri
        self.version_00401161: str | None = version
        self.parameters_00401162: Array[OntologyAnnotation] = default_arg(parameters, [])
        self.components_00401163: Array[Component] = default_arg(components, [])
        self.datamap_00401164: Datamap | None = datamap
        self.contacts_00401165: Array[Person] = default_arg(contacts, [])
        self.cwl_description_00401166: CWLProcessingUnit | None = cwl_description
        self.comments_00401167: Array[Comment] = default_arg(comments, [])
        self.static_hash: int = 0

    @property
    def Identifier(self, __unit: None=None) -> str:
        this: ArcWorkflow = self
        return this.identifier_00401151

    @Identifier.setter
    def Identifier(self, i: str) -> None:
        this: ArcWorkflow = self
        this.identifier_00401151 = i

    @property
    def Investigation(self, __unit: None=None) -> ArcInvestigation | None:
        this: ArcWorkflow = self
        return this.investigation

    @Investigation.setter
    def Investigation(self, a: ArcInvestigation | None=None) -> None:
        this: ArcWorkflow = self
        this.investigation = a

    @property
    def Title(self, __unit: None=None) -> str | None:
        this: ArcWorkflow = self
        return this.title_00401156

    @Title.setter
    def Title(self, t: str | None=None) -> None:
        this: ArcWorkflow = self
        this.title_00401156 = t

    @property
    def Description(self, __unit: None=None) -> str | None:
        this: ArcWorkflow = self
        return this.description_00401157

    @Description.setter
    def Description(self, d: str | None=None) -> None:
        this: ArcWorkflow = self
        this.description_00401157 = d

    @property
    def SubWorkflowIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcWorkflow = self
        return this.sub_workflow_identifiers_00401158

    @SubWorkflowIdentifiers.setter
    def SubWorkflowIdentifiers(self, s: Array[str]) -> None:
        this: ArcWorkflow = self
        this.sub_workflow_identifiers_00401158 = s

    @property
    def WorkflowType(self, __unit: None=None) -> OntologyAnnotation | None:
        this: ArcWorkflow = self
        return this.workflow_type_00401159

    @WorkflowType.setter
    def WorkflowType(self, w: OntologyAnnotation | None=None) -> None:
        this: ArcWorkflow = self
        this.workflow_type_00401159 = w

    @property
    def URI(self, __unit: None=None) -> str | None:
        this: ArcWorkflow = self
        return this.uri_00401160

    @URI.setter
    def URI(self, u: str | None=None) -> None:
        this: ArcWorkflow = self
        this.uri_00401160 = u

    @property
    def Version(self, __unit: None=None) -> str | None:
        this: ArcWorkflow = self
        return this.version_00401161

    @Version.setter
    def Version(self, v: str | None=None) -> None:
        this: ArcWorkflow = self
        this.version_00401161 = v

    @property
    def Parameters(self, __unit: None=None) -> Array[OntologyAnnotation]:
        this: ArcWorkflow = self
        return this.parameters_00401162

    @Parameters.setter
    def Parameters(self, p: Array[OntologyAnnotation]) -> None:
        this: ArcWorkflow = self
        this.parameters_00401162 = p

    @property
    def Components(self, __unit: None=None) -> Array[Component]:
        this: ArcWorkflow = self
        return this.components_00401163

    @Components.setter
    def Components(self, c: Array[Component]) -> None:
        this: ArcWorkflow = self
        this.components_00401163 = c

    @property
    def Datamap(self, __unit: None=None) -> Datamap | None:
        this: ArcWorkflow = self
        return this.datamap_00401164

    @Datamap.setter
    def Datamap(self, dm: Datamap | None=None) -> None:
        this: ArcWorkflow = self
        this.datamap_00401164 = dm

    @property
    def Contacts(self, __unit: None=None) -> Array[Person]:
        this: ArcWorkflow = self
        return this.contacts_00401165

    @Contacts.setter
    def Contacts(self, c: Array[Person]) -> None:
        this: ArcWorkflow = self
        this.contacts_00401165 = c

    @property
    def CWLDescription(self, __unit: None=None) -> CWLProcessingUnit | None:
        this: ArcWorkflow = self
        return this.cwl_description_00401166

    @CWLDescription.setter
    def CWLDescription(self, c: CWLProcessingUnit | None=None) -> None:
        this: ArcWorkflow = self
        this.cwl_description_00401166 = c

    @property
    def Comments(self, __unit: None=None) -> Array[Comment]:
        this: ArcWorkflow = self
        return this.comments_00401167

    @Comments.setter
    def Comments(self, c: Array[Comment]) -> None:
        this: ArcWorkflow = self
        this.comments_00401167 = c

    @property
    def StaticHash(self, __unit: None=None) -> int:
        this: ArcWorkflow = self
        return this.static_hash

    @StaticHash.setter
    def StaticHash(self, s: int) -> None:
        this: ArcWorkflow = self
        this.static_hash = s or 0

    @staticmethod
    def init(identifier: str) -> ArcWorkflow:
        return ArcWorkflow(identifier)

    @staticmethod
    def create(identifier: str, title: str | None=None, description: str | None=None, workflow_type: OntologyAnnotation | None=None, uri: str | None=None, version: str | None=None, sub_workflow_identifiers: Array[str] | None=None, parameters: Array[OntologyAnnotation] | None=None, components: Array[Component] | None=None, datamap: Datamap | None=None, contacts: Array[Person] | None=None, cwl_description: CWLProcessingUnit | None=None, comments: Array[Comment] | None=None) -> ArcWorkflow:
        return ArcWorkflow(identifier, title, description, workflow_type, uri, version, sub_workflow_identifiers, parameters, components, datamap, contacts, cwl_description, comments)

    @staticmethod
    def make(identifier: str, title: str | None, description: str | None, workflow_type: OntologyAnnotation | None, uri: str | None, version: str | None, sub_workflow_identifiers: Array[str], parameters: Array[OntologyAnnotation], components: Array[Component], datamap: Datamap | None, contacts: Array[Person], cwl_description: CWLProcessingUnit | None, comments: Array[Comment]) -> ArcWorkflow:
        return ArcWorkflow(identifier, title, description, workflow_type, uri, version, sub_workflow_identifiers, parameters, components, datamap, contacts, cwl_description, comments)

    @staticmethod
    def FileName() -> str:
        return "isa.run.xlsx"

    @property
    def SubWorkflowIdentifiersCount(self, __unit: None=None) -> int:
        this: ArcWorkflow = self
        return len(this.SubWorkflowIdentifiers)

    @property
    def SubWorkflowCount(self, __unit: None=None) -> int:
        this: ArcWorkflow = self
        return len(this.SubWorkflows)

    @property
    def SubWorkflows(self, __unit: None=None) -> Array[ArcWorkflow]:
        this: ArcWorkflow = self
        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        def chooser(workflow_identifier: str) -> ArcWorkflow | None:
            return inv.TryGetWorkflow(workflow_identifier)

        return list(choose(chooser, this.SubWorkflowIdentifiers))

    @property
    def VacantSubWorkflowIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcWorkflow = self
        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        def predicate(arg: str) -> bool:
            return not inv.ContainsWorkflow(arg)

        return list(filter(predicate, this.SubWorkflowIdentifiers))

    def AddSubWorkflow(self, sub_workflow: ArcWorkflow) -> None:
        this: ArcWorkflow = self
        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        inv.AddWorkflow(sub_workflow)

    @staticmethod
    def add_sub_workflow(sub_workflow: ArcWorkflow) -> Callable[[ArcWorkflow], ArcWorkflow]:
        def _arrow1213(workflow: ArcWorkflow) -> ArcWorkflow:
            new_workflow: ArcWorkflow = workflow.Copy()
            new_workflow.AddSubWorkflow(sub_workflow)
            return new_workflow

        return _arrow1213

    def InitSubWorkflow(self, sub_workflow_identifier: str) -> ArcWorkflow:
        this: ArcWorkflow = self
        sub_workflow: ArcWorkflow = ArcWorkflow(sub_workflow_identifier)
        this.AddSubWorkflow(sub_workflow)
        return sub_workflow

    @staticmethod
    def init_sub_workflow(sub_workflow_identifier: str) -> Callable[[ArcWorkflow], tuple[ArcWorkflow, ArcWorkflow]]:
        def _arrow1214(workflow: ArcWorkflow) -> tuple[ArcWorkflow, ArcWorkflow]:
            copy: ArcWorkflow = workflow.Copy()
            return (copy, copy.InitSubWorkflow(sub_workflow_identifier))

        return _arrow1214

    def RegisterSubWorkflow(self, sub_workflow_identifier: str) -> None:
        this: ArcWorkflow = self
        class ObjectExpr1216:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1215(x: str, y: str) -> bool:
                    return x == y

                return _arrow1215

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if contains(sub_workflow_identifier, this.SubWorkflowIdentifiers, ObjectExpr1216()):
            raise Exception(("SubWorkflow `" + sub_workflow_identifier) + "` is already registered on the workflow.")

        (this.SubWorkflowIdentifiers.append(sub_workflow_identifier))

    @staticmethod
    def register_sub_workflow(sub_workflow_identifier: str) -> Callable[[ArcWorkflow], ArcWorkflow]:
        def _arrow1217(workflow: ArcWorkflow) -> ArcWorkflow:
            copy: ArcWorkflow = workflow.Copy()
            copy.RegisterSubWorkflow(sub_workflow_identifier)
            return copy

        return _arrow1217

    def DeregisterSubWorkflow(self, sub_workflow_identifier: str) -> None:
        this: ArcWorkflow = self
        class ObjectExpr1219:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1218(x: str, y: str) -> bool:
                    return x == y

                return _arrow1218

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        ignore(remove_in_place(sub_workflow_identifier, this.SubWorkflowIdentifiers, ObjectExpr1219()))

    @staticmethod
    def deregister_sub_workflow(sub_workflow_identifier: str) -> Callable[[ArcWorkflow], ArcWorkflow]:
        def _arrow1220(workflow: ArcWorkflow) -> ArcWorkflow:
            copy: ArcWorkflow = workflow.Copy()
            copy.DeregisterSubWorkflow(sub_workflow_identifier)
            return copy

        return _arrow1220

    def GetRegisteredSubWorkflow(self, sub_workflow_identifier: str) -> ArcWorkflow:
        this: ArcWorkflow = self
        class ObjectExpr1222:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1221(x: str, y: str) -> bool:
                    return x == y

                return _arrow1221

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if not contains(sub_workflow_identifier, this.SubWorkflowIdentifiers, ObjectExpr1222()):
            raise Exception(("SubWorkflow `" + sub_workflow_identifier) + "` is not registered on the workflow.")

        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        return inv.GetWorkflow(sub_workflow_identifier)

    @staticmethod
    def get_registered_sub_workflow(sub_workflow_identifier: str) -> Callable[[ArcWorkflow], ArcWorkflow]:
        def _arrow1223(workflow: ArcWorkflow) -> ArcWorkflow:
            copy: ArcWorkflow = workflow.Copy()
            return copy.GetRegisteredSubWorkflow(sub_workflow_identifier)

        return _arrow1223

    @staticmethod
    def get_registered_sub_workflows(__unit: None=None) -> Callable[[ArcWorkflow], Array[ArcWorkflow]]:
        def _arrow1224(workflow: ArcWorkflow) -> Array[ArcWorkflow]:
            copy: ArcWorkflow = workflow.Copy()
            return copy.SubWorkflows

        return _arrow1224

    def GetRegisteredSubWorkflowsOrIdentifier(self, __unit: None=None) -> Array[ArcWorkflow]:
        this: ArcWorkflow = self
        match_value: ArcInvestigation | None = this.Investigation
        if match_value is None:
            def f_1(identifier_1: str) -> ArcWorkflow:
                return ArcWorkflow.init(identifier_1)

            return ResizeArray_map(f_1, this.SubWorkflowIdentifiers)

        else: 
            i: ArcInvestigation = match_value
            def f(identifier: str) -> ArcWorkflow:
                match_value_1: ArcWorkflow | None = i.TryGetWorkflow(identifier)
                if match_value_1 is None:
                    return ArcWorkflow.init(identifier)

                else: 
                    return match_value_1


            return ResizeArray_map(f, this.SubWorkflowIdentifiers)


    @staticmethod
    def get_registered_sub_workflows_or_identifier(__unit: None=None) -> Callable[[ArcWorkflow], Array[ArcWorkflow]]:
        def _arrow1225(workflow: ArcWorkflow) -> Array[ArcWorkflow]:
            copy: ArcWorkflow = workflow.Copy()
            return copy.GetRegisteredSubWorkflowsOrIdentifier()

        return _arrow1225

    def Copy(self, copy_investigation_ref: bool | None=None) -> ArcWorkflow:
        this: ArcWorkflow = self
        copy_investigation_ref_1: bool = default_arg(copy_investigation_ref, False)
        def mapping(w: OntologyAnnotation) -> OntologyAnnotation:
            return w.Copy()

        next_work_flow_type: OntologyAnnotation | None = map(mapping, this.WorkflowType)
        next_sub_workflow_identifiers: Array[str] = list(this.SubWorkflowIdentifiers)
        def f(x: OntologyAnnotation) -> OntologyAnnotation:
            return x

        next_parameters: Array[OntologyAnnotation] = ResizeArray_map(f, this.Parameters)
        def f_1(x_1: Component) -> Component:
            return x_1

        next_components: Array[Component] = ResizeArray_map(f_1, this.Components)
        def mapping_1(d: Datamap) -> Datamap:
            return d.Copy()

        next_datamap: Datamap | None = map(mapping_1, this.Datamap)
        def f_2(c: Person) -> Person:
            return c.Copy()

        next_contacts: Array[Person] = ResizeArray_map(f_2, this.Contacts)
        def f_3(c_1: Comment) -> Comment:
            return c_1.Copy()

        next_comments: Array[Comment] = ResizeArray_map(f_3, this.Comments)
        workflow: ArcWorkflow
        identifier: str = this.Identifier
        title: str | None = this.Title
        description: str | None = this.Description
        uri: str | None = this.URI
        version: str | None = this.Version
        cwl_description: CWLProcessingUnit | None = this.CWLDescription
        workflow = ArcWorkflow.make(identifier, title, description, next_work_flow_type, uri, version, next_sub_workflow_identifiers, next_parameters, next_components, next_datamap, next_contacts, cwl_description, next_comments)
        if copy_investigation_ref_1:
            workflow.Investigation = this.Investigation

        return workflow

    def StructurallyEquals(self, other: ArcWorkflow) -> bool:
        this: ArcWorkflow = self
        def predicate(x: bool) -> bool:
            return x == True

        def _arrow1228(__unit: None=None) -> bool:
            a: IEnumerable_1[str] = this.SubWorkflowIdentifiers
            b: IEnumerable_1[str] = other.SubWorkflowIdentifiers
            def folder(acc: bool, e: bool) -> bool:
                if acc:
                    return e

                else: 
                    return False


            def _arrow1227(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1226(i_1: int) -> bool:
                    return item(i_1, a) == item(i_1, b)

                return map_1(_arrow1226, range_big_int(0, 1, length(a) - 1))

            return fold(folder, True, to_list(delay(_arrow1227))) if (length(a) == length(b)) else False

        def _arrow1231(__unit: None=None) -> bool:
            a_1: IEnumerable_1[OntologyAnnotation] = this.Parameters
            b_1: IEnumerable_1[OntologyAnnotation] = other.Parameters
            def folder_1(acc_1: bool, e_1: bool) -> bool:
                if acc_1:
                    return e_1

                else: 
                    return False


            def _arrow1230(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1229(i_2: int) -> bool:
                    return equals(item(i_2, a_1), item(i_2, b_1))

                return map_1(_arrow1229, range_big_int(0, 1, length(a_1) - 1))

            return fold(folder_1, True, to_list(delay(_arrow1230))) if (length(a_1) == length(b_1)) else False

        def _arrow1234(__unit: None=None) -> bool:
            a_2: IEnumerable_1[Component] = this.Components
            b_2: IEnumerable_1[Component] = other.Components
            def folder_2(acc_2: bool, e_2: bool) -> bool:
                if acc_2:
                    return e_2

                else: 
                    return False


            def _arrow1233(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1232(i_3: int) -> bool:
                    return equals(item(i_3, a_2), item(i_3, b_2))

                return map_1(_arrow1232, range_big_int(0, 1, length(a_2) - 1))

            return fold(folder_2, True, to_list(delay(_arrow1233))) if (length(a_2) == length(b_2)) else False

        def _arrow1237(__unit: None=None) -> bool:
            a_3: IEnumerable_1[Person] = this.Contacts
            b_3: IEnumerable_1[Person] = other.Contacts
            def folder_3(acc_3: bool, e_3: bool) -> bool:
                if acc_3:
                    return e_3

                else: 
                    return False


            def _arrow1236(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1235(i_4: int) -> bool:
                    return equals(item(i_4, a_3), item(i_4, b_3))

                return map_1(_arrow1235, range_big_int(0, 1, length(a_3) - 1))

            return fold(folder_3, True, to_list(delay(_arrow1236))) if (length(a_3) == length(b_3)) else False

        def _arrow1240(__unit: None=None) -> bool:
            a_4: IEnumerable_1[Comment] = this.Comments
            b_4: IEnumerable_1[Comment] = other.Comments
            def folder_4(acc_4: bool, e_4: bool) -> bool:
                if acc_4:
                    return e_4

                else: 
                    return False


            def _arrow1239(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1238(i_5: int) -> bool:
                    return equals(item(i_5, a_4), item(i_5, b_4))

                return map_1(_arrow1238, range_big_int(0, 1, length(a_4) - 1))

            return fold(folder_4, True, to_list(delay(_arrow1239))) if (length(a_4) == length(b_4)) else False

        return for_all(predicate, to_enumerable([this.Identifier == other.Identifier, equals(this.Title, other.Title), equals(this.Description, other.Description), equals(this.WorkflowType, other.WorkflowType), equals(this.URI, other.URI), equals(this.Version, other.Version), _arrow1228(), _arrow1231(), _arrow1234(), equals(this.Datamap, other.Datamap), _arrow1237(), equals(this.CWLDescription, other.CWLDescription), _arrow1240()]))

    def ReferenceEquals(self, other: ArcStudy) -> bool:
        this: ArcWorkflow = self
        return this is other

    def __str__(self, __unit: None=None) -> str:
        this: ArcWorkflow = self
        arg: str = this.Identifier
        arg_1: str | None = this.Title
        arg_2: str | None = this.Description
        arg_3: OntologyAnnotation | None = this.WorkflowType
        arg_4: str | None = this.URI
        arg_5: str | None = this.Version
        arg_6: Array[str] = this.SubWorkflowIdentifiers
        arg_7: Array[OntologyAnnotation] = this.Parameters
        arg_8: Array[Component] = this.Components
        arg_9: Datamap | None = this.Datamap
        arg_10: Array[Person] = this.Contacts
        arg_11: Array[Comment] = this.Comments
        return to_text(printf("ArcWorkflow {\r\n    Identifier = %A,\r\n    Title = %A,\r\n    Description = %A,\r\n    WorkflowType = %A,\r\n    URI = %A,\r\n    Version = %A,\r\n    SubWorkflowIdentifiers = %A,\r\n    Parameters = %A,\r\n    Components = %A,\r\n    Datamap = %A,\r\n    Contacts = %A,\r\n    Comments = %A}"))(arg)(arg_1)(arg_2)(arg_3)(arg_4)(arg_5)(arg_6)(arg_7)(arg_8)(arg_9)(arg_10)(arg_11)

    def __eq__(self, other: Any=None) -> bool:
        this: ArcWorkflow = self
        return this.StructurallyEquals(other) if isinstance(other, ArcWorkflow) else False

    def __hash__(self, __unit: None=None) -> Any:
        this: ArcWorkflow = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.WorkflowType), box_hash_option(this.URI), box_hash_option(this.Version), box_hash_seq(this.SubWorkflowIdentifiers), box_hash_seq(this.Parameters), box_hash_seq(this.Components), box_hash_option(this.Datamap), box_hash_seq(this.Contacts), box_hash_option(this.CWLDescription), box_hash_seq(this.Comments)])

    def GetLightHashCode(self, __unit: None=None) -> Any:
        this: ArcWorkflow = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.WorkflowType), box_hash_option(this.URI), box_hash_option(this.Version), box_hash_seq(this.SubWorkflowIdentifiers), box_hash_seq(this.Parameters), box_hash_seq(this.Components), box_hash_seq(this.Contacts), box_hash_seq(this.Comments)])


ArcWorkflow_reflection = _expr1242

def ArcWorkflow__ctor_Z5FF2D3D5(identifier: str, title: str | None=None, description: str | None=None, workflow_type: OntologyAnnotation | None=None, uri: str | None=None, version: str | None=None, sub_workflow_identifiers: Array[str] | None=None, parameters: Array[OntologyAnnotation] | None=None, components: Array[Component] | None=None, datamap: Datamap | None=None, contacts: Array[Person] | None=None, cwl_description: CWLProcessingUnit | None=None, comments: Array[Comment] | None=None) -> ArcWorkflow:
    return ArcWorkflow(identifier, title, description, workflow_type, uri, version, sub_workflow_identifiers, parameters, components, datamap, contacts, cwl_description, comments)


def _expr1303() -> TypeInfo:
    return class_type("ARCtrl.ArcRun", None, ArcRun, ArcTables_reflection())


class ArcRun(ArcTables):
    def __init__(self, identifier: str, title: str | None=None, description: str | None=None, measurement_type: OntologyAnnotation | None=None, technology_type: OntologyAnnotation | None=None, technology_platform: OntologyAnnotation | None=None, workflow_identifiers: Array[str] | None=None, tables: Array[ArcTable] | None=None, datamap: Datamap | None=None, performers: Array[Person] | None=None, cwl_description: CWLProcessingUnit | None=None, cwl_input: Array[CWLParameterReference] | None=None, comments: Array[Comment] | None=None) -> None:
        super().__init__(default_arg(tables, []))
        performers_1: Array[Person] = default_arg(performers, [])
        comments_1: Array[Comment] = default_arg(comments, [])
        workflow_identifiers_1: Array[str] = default_arg(workflow_identifiers, [])
        cwl_input_1: Array[CWLParameterReference] = default_arg(cwl_input, [])
        def _arrow1302(__unit: None=None) -> str:
            identifier_1: str = identifier.strip()
            check_valid_characters(identifier_1)
            return identifier_1

        self.identifier_00401453: str = _arrow1302()
        self.title_00401457: str | None = title
        self.description_00401458: str | None = description
        self.investigation: ArcInvestigation | None = None
        self.measurement_type_00401460: OntologyAnnotation | None = measurement_type
        self.technology_type_00401461: OntologyAnnotation | None = technology_type
        self.technology_platform_00401462: OntologyAnnotation | None = technology_platform
        self.workflow_identifiers_00401463_002D1: Array[str] = workflow_identifiers_1
        self.datamap_00401464: Datamap | None = datamap
        self.performers_00401465_002D1: Array[Person] = performers_1
        self.cwl_description_00401466: CWLProcessingUnit | None = cwl_description
        self.cwl_input_00401467_002D1: Array[CWLParameterReference] = cwl_input_1
        self.comments_00401468_002D1: Array[Comment] = comments_1
        self.static_hash: int = 0

    @property
    def Identifier(self, __unit: None=None) -> str:
        this: ArcRun = self
        return this.identifier_00401453

    @Identifier.setter
    def Identifier(self, i: str) -> None:
        this: ArcRun = self
        this.identifier_00401453 = i

    @property
    def Investigation(self, __unit: None=None) -> ArcInvestigation | None:
        this: ArcRun = self
        return this.investigation

    @Investigation.setter
    def Investigation(self, i: ArcInvestigation | None=None) -> None:
        this: ArcRun = self
        this.investigation = i

    @property
    def Title(self, __unit: None=None) -> str | None:
        this: ArcRun = self
        return this.title_00401457

    @Title.setter
    def Title(self, t: str | None=None) -> None:
        this: ArcRun = self
        this.title_00401457 = t

    @property
    def Description(self, __unit: None=None) -> str | None:
        this: ArcRun = self
        return this.description_00401458

    @Description.setter
    def Description(self, d: str | None=None) -> None:
        this: ArcRun = self
        this.description_00401458 = d

    @property
    def MeasurementType(self, __unit: None=None) -> OntologyAnnotation | None:
        this: ArcRun = self
        return this.measurement_type_00401460

    @MeasurementType.setter
    def MeasurementType(self, n: OntologyAnnotation | None=None) -> None:
        this: ArcRun = self
        this.measurement_type_00401460 = n

    @property
    def TechnologyType(self, __unit: None=None) -> OntologyAnnotation | None:
        this: ArcRun = self
        return this.technology_type_00401461

    @TechnologyType.setter
    def TechnologyType(self, n: OntologyAnnotation | None=None) -> None:
        this: ArcRun = self
        this.technology_type_00401461 = n

    @property
    def TechnologyPlatform(self, __unit: None=None) -> OntologyAnnotation | None:
        this: ArcRun = self
        return this.technology_platform_00401462

    @TechnologyPlatform.setter
    def TechnologyPlatform(self, n: OntologyAnnotation | None=None) -> None:
        this: ArcRun = self
        this.technology_platform_00401462 = n

    @property
    def WorkflowIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcRun = self
        return this.workflow_identifiers_00401463_002D1

    @WorkflowIdentifiers.setter
    def WorkflowIdentifiers(self, w: Array[str]) -> None:
        this: ArcRun = self
        this.workflow_identifiers_00401463_002D1 = w

    @property
    def Datamap(self, __unit: None=None) -> Datamap | None:
        this: ArcRun = self
        return this.datamap_00401464

    @Datamap.setter
    def Datamap(self, n: Datamap | None=None) -> None:
        this: ArcRun = self
        this.datamap_00401464 = n

    @property
    def Performers(self, __unit: None=None) -> Array[Person]:
        this: ArcRun = self
        return this.performers_00401465_002D1

    @Performers.setter
    def Performers(self, n: Array[Person]) -> None:
        this: ArcRun = self
        this.performers_00401465_002D1 = n

    @property
    def CWLDescription(self, __unit: None=None) -> CWLProcessingUnit | None:
        this: ArcRun = self
        return this.cwl_description_00401466

    @CWLDescription.setter
    def CWLDescription(self, n: CWLProcessingUnit | None=None) -> None:
        this: ArcRun = self
        this.cwl_description_00401466 = n

    @property
    def CWLInput(self, __unit: None=None) -> Array[CWLParameterReference]:
        this: ArcRun = self
        return this.cwl_input_00401467_002D1

    @CWLInput.setter
    def CWLInput(self, n: Array[CWLParameterReference]) -> None:
        this: ArcRun = self
        this.cwl_input_00401467_002D1 = n

    @property
    def Comments(self, __unit: None=None) -> Array[Comment]:
        this: ArcRun = self
        return this.comments_00401468_002D1

    @Comments.setter
    def Comments(self, n: Array[Comment]) -> None:
        this: ArcRun = self
        this.comments_00401468_002D1 = n

    @property
    def StaticHash(self, __unit: None=None) -> int:
        this: ArcRun = self
        return this.static_hash

    @StaticHash.setter
    def StaticHash(self, h: int) -> None:
        this: ArcRun = self
        this.static_hash = h or 0

    @staticmethod
    def init(identifier: str) -> ArcRun:
        return ArcRun(identifier)

    @staticmethod
    def create(identifier: str, title: str | None=None, description: str | None=None, measurement_type: OntologyAnnotation | None=None, technology_type: OntologyAnnotation | None=None, technology_platform: OntologyAnnotation | None=None, workflow_identifiers: Array[str] | None=None, tables: Array[ArcTable] | None=None, datamap: Datamap | None=None, performers: Array[Person] | None=None, cwl_description: CWLProcessingUnit | None=None, cwl_input: Array[CWLParameterReference] | None=None, comments: Array[Comment] | None=None) -> ArcRun:
        return ArcRun(identifier, title, description, measurement_type, technology_type, technology_platform, workflow_identifiers, tables, datamap, performers, cwl_description, cwl_input, comments)

    @staticmethod
    def make(identifier: str, title: str | None, description: str | None, measurement_type: OntologyAnnotation | None, technology_type: OntologyAnnotation | None, technology_platform: OntologyAnnotation | None, workflow_identifiers: Array[str], tables: Array[ArcTable], datamap: Datamap | None, performers: Array[Person], cwl_description: CWLProcessingUnit | None, cwl_input: Array[CWLParameterReference], comments: Array[Comment]) -> ArcRun:
        return ArcRun(identifier, title, description, measurement_type, technology_type, technology_platform, workflow_identifiers, tables, datamap, performers, cwl_description, cwl_input, comments)

    @staticmethod
    def FileName() -> str:
        return "isa.run.xlsx"

    @property
    def WorkflowIdentifierCount(self, __unit: None=None) -> int:
        this: ArcRun = self
        return len(this.WorkflowIdentifiers)

    @property
    def WorkflowCount(self, __unit: None=None) -> int:
        this: ArcRun = self
        return len(this.Workflows)

    @property
    def Workflows(self, __unit: None=None) -> Array[ArcWorkflow]:
        this: ArcRun = self
        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        def chooser(workflow_identifier: str) -> ArcWorkflow | None:
            return inv.TryGetWorkflow(workflow_identifier)

        return list(choose(chooser, this.WorkflowIdentifiers))

    @property
    def VacantWorkflowIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcRun = self
        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        def predicate(arg: str) -> bool:
            return not inv.ContainsWorkflow(arg)

        return list(filter(predicate, this.WorkflowIdentifiers))

    @staticmethod
    def add_table(table: ArcTable, index: int | None=None) -> Callable[[ArcRun], ArcRun]:
        def _arrow1243(run: ArcRun) -> ArcRun:
            c: ArcRun = run.Copy()
            c.AddTable(table, index)
            return c

        return _arrow1243

    @staticmethod
    def add_tables(tables: IEnumerable_1[ArcTable], index: int | None=None) -> Callable[[ArcRun], ArcRun]:
        def _arrow1244(run: ArcRun) -> ArcRun:
            c: ArcRun = run.Copy()
            c.AddTables(tables, index)
            return c

        return _arrow1244

    @staticmethod
    def init_table(table_name: str, index: int | None=None) -> Callable[[ArcRun], tuple[ArcRun, ArcTable]]:
        def _arrow1245(run: ArcRun) -> tuple[ArcRun, ArcTable]:
            c: ArcRun = run.Copy()
            return (c, c.InitTable(table_name, index))

        return _arrow1245

    @staticmethod
    def init_tables(table_names: IEnumerable_1[str], index: int | None=None) -> Callable[[ArcRun], ArcRun]:
        def _arrow1246(run: ArcRun) -> ArcRun:
            c: ArcRun = run.Copy()
            c.InitTables(table_names, index)
            return c

        return _arrow1246

    @staticmethod
    def get_table_at(index: int) -> Callable[[ArcRun], ArcTable]:
        def _arrow1247(run: ArcRun) -> ArcTable:
            new_run: ArcRun = run.Copy()
            return new_run.GetTableAt(index)

        return _arrow1247

    @staticmethod
    def get_table(name: str) -> Callable[[ArcRun], ArcTable]:
        def _arrow1248(run: ArcRun) -> ArcTable:
            new_run: ArcRun = run.Copy()
            return new_run.GetTable(name)

        return _arrow1248

    @staticmethod
    def update_table_at(index: int, table: ArcTable) -> Callable[[ArcRun], ArcRun]:
        def _arrow1249(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.UpdateTableAt(index, table)
            return new_run

        return _arrow1249

    @staticmethod
    def update_table(name: str, table: ArcTable) -> Callable[[ArcRun], ArcRun]:
        def _arrow1250(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.UpdateTable(name, table)
            return new_run

        return _arrow1250

    @staticmethod
    def set_table_at(index: int, table: ArcTable) -> Callable[[ArcRun], ArcRun]:
        def _arrow1251(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.SetTableAt(index, table)
            return new_run

        return _arrow1251

    @staticmethod
    def set_table(name: str, table: ArcTable) -> Callable[[ArcRun], ArcRun]:
        def _arrow1252(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.SetTable(name, table)
            return new_run

        return _arrow1252

    @staticmethod
    def remove_table_at(index: int) -> Callable[[ArcRun], ArcRun]:
        def _arrow1253(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.RemoveTableAt(index)
            return new_run

        return _arrow1253

    @staticmethod
    def remove_table(name: str) -> Callable[[ArcRun], ArcRun]:
        def _arrow1254(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.RemoveTable(name)
            return new_run

        return _arrow1254

    @staticmethod
    def map_table_at(index: int, update_fun: Callable[[ArcTable], None]) -> Callable[[ArcRun], ArcRun]:
        def _arrow1255(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.MapTableAt(index, update_fun)
            return new_run

        return _arrow1255

    @staticmethod
    def map_table(name: str, update_fun: Callable[[ArcTable], None]) -> Callable[[ArcRun], ArcRun]:
        def _arrow1256(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.MapTable(name, update_fun)
            return new_run

        return _arrow1256

    @staticmethod
    def rename_table_at(index: int, new_name: str) -> Callable[[ArcRun], ArcRun]:
        def _arrow1257(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.RenameTableAt(index, new_name)
            return new_run

        return _arrow1257

    @staticmethod
    def rename_table(name: str, new_name: str) -> Callable[[ArcRun], ArcRun]:
        def _arrow1258(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.RenameTable(name, new_name)
            return new_run

        return _arrow1258

    @staticmethod
    def add_column_at(table_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None, column_index: int | None=None, force_replace: bool | None=None) -> Callable[[ArcRun], ArcRun]:
        def _arrow1259(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.AddColumnAt(table_index, header, cells, column_index, force_replace)
            return new_run

        return _arrow1259

    @staticmethod
    def add_column(table_name: str, header: CompositeHeader, cells: Array[CompositeCell] | None=None, column_index: int | None=None, force_replace: bool | None=None) -> Callable[[ArcRun], ArcRun]:
        def _arrow1260(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.AddColumn(table_name, header, cells, column_index, force_replace)
            return new_run

        return _arrow1260

    @staticmethod
    def remove_column_at(table_index: int, column_index: int) -> Callable[[ArcRun], ArcRun]:
        def _arrow1261(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.RemoveColumnAt(table_index, column_index)
            return new_run

        return _arrow1261

    @staticmethod
    def remove_column(table_name: str, column_index: int) -> Callable[[ArcRun], ArcRun]:
        def _arrow1262(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.RemoveColumn(table_name, column_index)
            return new_run

        return _arrow1262

    @staticmethod
    def update_column_at(table_index: int, column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> Callable[[ArcRun], ArcRun]:
        def _arrow1263(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.UpdateColumnAt(table_index, column_index, header, cells)
            return new_run

        return _arrow1263

    @staticmethod
    def update_column(table_name: str, column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> Callable[[ArcRun], ArcRun]:
        def _arrow1264(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.UpdateColumn(table_name, column_index, header, cells)
            return new_run

        return _arrow1264

    @staticmethod
    def get_column_at(table_index: int, column_index: int) -> Callable[[ArcRun], CompositeColumn]:
        def _arrow1265(run: ArcRun) -> CompositeColumn:
            new_run: ArcRun = run.Copy()
            return new_run.GetColumnAt(table_index, column_index)

        return _arrow1265

    @staticmethod
    def get_column(table_name: str, column_index: int) -> Callable[[ArcRun], CompositeColumn]:
        def _arrow1266(run: ArcRun) -> CompositeColumn:
            new_run: ArcRun = run.Copy()
            return new_run.GetColumn(table_name, column_index)

        return _arrow1266

    @staticmethod
    def add_row_at(table_index: int, cells: Array[CompositeCell] | None=None, row_index: int | None=None) -> Callable[[ArcRun], ArcRun]:
        def _arrow1267(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.AddRowAt(table_index, cells, row_index)
            return new_run

        return _arrow1267

    @staticmethod
    def add_row(table_name: str, cells: Array[CompositeCell] | None=None, row_index: int | None=None) -> Callable[[ArcRun], ArcRun]:
        def _arrow1268(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.AddRow(table_name, cells, row_index)
            return new_run

        return _arrow1268

    @staticmethod
    def remove_row_at(table_index: int, row_index: int) -> Callable[[ArcRun], ArcRun]:
        def _arrow1269(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.RemoveColumnAt(table_index, row_index)
            return new_run

        return _arrow1269

    @staticmethod
    def remove_row(table_name: str, row_index: int) -> Callable[[ArcRun], ArcRun]:
        def _arrow1270(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.RemoveRow(table_name, row_index)
            return new_run

        return _arrow1270

    @staticmethod
    def update_row_at(table_index: int, row_index: int, cells: Array[CompositeCell]) -> Callable[[ArcRun], ArcRun]:
        def _arrow1271(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.UpdateRowAt(table_index, row_index, cells)
            return new_run

        return _arrow1271

    @staticmethod
    def update_row(table_name: str, row_index: int, cells: Array[CompositeCell]) -> Callable[[ArcRun], ArcRun]:
        def _arrow1272(run: ArcRun) -> ArcRun:
            new_run: ArcRun = run.Copy()
            new_run.UpdateRow(table_name, row_index, cells)
            return new_run

        return _arrow1272

    @staticmethod
    def get_row_at(table_index: int, row_index: int) -> Callable[[ArcRun], Array[CompositeCell]]:
        def _arrow1273(run: ArcRun) -> Array[CompositeCell]:
            new_run: ArcRun = run.Copy()
            return new_run.GetRowAt(table_index, row_index)

        return _arrow1273

    @staticmethod
    def get_row(table_name: str, row_index: int) -> Callable[[ArcRun], Array[CompositeCell]]:
        def _arrow1274(run: ArcRun) -> Array[CompositeCell]:
            new_run: ArcRun = run.Copy()
            return new_run.GetRow(table_name, row_index)

        return _arrow1274

    @staticmethod
    def set_performers(performers: Array[Person], run: ArcRun) -> ArcRun:
        run.Performers = performers
        return run

    def Copy(self, __unit: None=None) -> ArcRun:
        this: ArcRun = self
        def f(c: ArcTable) -> ArcTable:
            return c.Copy()

        next_tables: Array[ArcTable] = ResizeArray_map(f, this.Tables)
        def f_1(c_1: Comment) -> Comment:
            return c_1.Copy()

        next_comments: Array[Comment] = ResizeArray_map(f_1, this.Comments)
        def mapping(d: Datamap) -> Datamap:
            return d.Copy()

        next_datamap: Datamap | None = map(mapping, this.Datamap)
        def f_2(c_2: Person) -> Person:
            return c_2.Copy()

        next_performers: Array[Person] = ResizeArray_map(f_2, this.Performers)
        def f_3(c_3: str) -> str:
            return c_3

        next_workflow_identifiers: Array[str] = ResizeArray_map(f_3, this.WorkflowIdentifiers)
        identifier: str = this.Identifier
        title: str | None = this.Title
        description: str | None = this.Description
        measurement_type: OntologyAnnotation | None = this.MeasurementType
        technology_type: OntologyAnnotation | None = this.TechnologyType
        technology_platform: OntologyAnnotation | None = this.TechnologyPlatform
        cwl_description: CWLProcessingUnit | None = this.CWLDescription
        cwl_input: Array[CWLParameterReference] = this.CWLInput
        return ArcRun.make(identifier, title, description, measurement_type, technology_type, technology_platform, next_workflow_identifiers, next_tables, next_datamap, next_performers, cwl_description, cwl_input, next_comments)

    def UpdateBy(self, run: ArcRun, only_replace_existing: bool | None=None, append_sequences: bool | None=None) -> None:
        this: ArcRun = self
        only_replace_existing_1: bool = default_arg(only_replace_existing, False)
        append_sequences_1: bool = default_arg(append_sequences, False)
        update_always: bool = not only_replace_existing_1
        if True if (run.Title is not None) else update_always:
            this.Title = run.Title

        if True if (run.Description is not None) else update_always:
            this.Description = run.Description

        if True if (run.MeasurementType is not None) else update_always:
            this.MeasurementType = run.MeasurementType

        if True if (run.TechnologyType is not None) else update_always:
            this.TechnologyType = run.TechnologyType

        if True if (run.TechnologyPlatform is not None) else update_always:
            this.TechnologyPlatform = run.TechnologyPlatform

        if True if (len(run.WorkflowIdentifiers) != 0) else update_always:
            s: Array[str]
            origin: Array[str] = this.WorkflowIdentifiers
            next_1: Array[str] = run.WorkflowIdentifiers
            if not append_sequences_1:
                def f(x: str) -> str:
                    return x

                s = ResizeArray_map(f, next_1)

            else: 
                combined: Array[str] = []
                enumerator: Any = get_enumerator(origin)
                try: 
                    while enumerator.System_Collections_IEnumerator_MoveNext():
                        e: str = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1276:
                            @property
                            def Equals(self) -> Callable[[str, str], bool]:
                                def _arrow1275(x_1: str, y: str) -> bool:
                                    return x_1 == y

                                return _arrow1275

                            @property
                            def GetHashCode(self) -> Callable[[str], int]:
                                return string_hash

                        if not contains_1(e, combined, ObjectExpr1276()):
                            (combined.append(e))


                finally: 
                    dispose(enumerator)

                enumerator_1: Any = get_enumerator(next_1)
                try: 
                    while enumerator_1.System_Collections_IEnumerator_MoveNext():
                        e_1: str = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1278:
                            @property
                            def Equals(self) -> Callable[[str, str], bool]:
                                def _arrow1277(x_2: str, y_1: str) -> bool:
                                    return x_2 == y_1

                                return _arrow1277

                            @property
                            def GetHashCode(self) -> Callable[[str], int]:
                                return string_hash

                        if not contains_1(e_1, combined, ObjectExpr1278()):
                            (combined.append(e_1))


                finally: 
                    dispose(enumerator_1)

                s = combined

            this.WorkflowIdentifiers = s

        if True if (run.Datamap is not None) else update_always:
            this.Datamap = run.Datamap

        if True if (len(run.Tables) != 0) else update_always:
            s_1: Array[ArcTable]
            origin_1: Array[ArcTable] = this.Tables
            next_1_1: Array[ArcTable] = run.Tables
            if not append_sequences_1:
                def f_1(x_3: ArcTable) -> ArcTable:
                    return x_3

                s_1 = ResizeArray_map(f_1, next_1_1)

            else: 
                combined_1: Array[ArcTable] = []
                enumerator_2: Any = get_enumerator(origin_1)
                try: 
                    while enumerator_2.System_Collections_IEnumerator_MoveNext():
                        e_2: ArcTable = enumerator_2.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1279:
                            @property
                            def Equals(self) -> Callable[[ArcTable, ArcTable], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[ArcTable], int]:
                                return safe_hash

                        if not contains_1(e_2, combined_1, ObjectExpr1279()):
                            (combined_1.append(e_2))


                finally: 
                    dispose(enumerator_2)

                enumerator_1_1: Any = get_enumerator(next_1_1)
                try: 
                    while enumerator_1_1.System_Collections_IEnumerator_MoveNext():
                        e_1_1: ArcTable = enumerator_1_1.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1280:
                            @property
                            def Equals(self) -> Callable[[ArcTable, ArcTable], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[ArcTable], int]:
                                return safe_hash

                        if not contains_1(e_1_1, combined_1, ObjectExpr1280()):
                            (combined_1.append(e_1_1))


                finally: 
                    dispose(enumerator_1_1)

                s_1 = combined_1

            this.Tables = s_1

        if True if (len(run.Performers) != 0) else update_always:
            s_2: Array[Person]
            origin_2: Array[Person] = this.Performers
            next_1_2: Array[Person] = run.Performers
            if not append_sequences_1:
                def f_2(x_6: Person) -> Person:
                    return x_6

                s_2 = ResizeArray_map(f_2, next_1_2)

            else: 
                combined_2: Array[Person] = []
                enumerator_3: Any = get_enumerator(origin_2)
                try: 
                    while enumerator_3.System_Collections_IEnumerator_MoveNext():
                        e_3: Person = enumerator_3.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1281:
                            @property
                            def Equals(self) -> Callable[[Person, Person], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[Person], int]:
                                return safe_hash

                        if not contains_1(e_3, combined_2, ObjectExpr1281()):
                            (combined_2.append(e_3))


                finally: 
                    dispose(enumerator_3)

                enumerator_1_2: Any = get_enumerator(next_1_2)
                try: 
                    while enumerator_1_2.System_Collections_IEnumerator_MoveNext():
                        e_1_2: Person = enumerator_1_2.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1282:
                            @property
                            def Equals(self) -> Callable[[Person, Person], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[Person], int]:
                                return safe_hash

                        if not contains_1(e_1_2, combined_2, ObjectExpr1282()):
                            (combined_2.append(e_1_2))


                finally: 
                    dispose(enumerator_1_2)

                s_2 = combined_2

            this.Performers = s_2

        if True if (run.CWLDescription is not None) else update_always:
            this.CWLDescription = run.CWLDescription

        if True if (len(run.CWLInput) != 0) else update_always:
            s_3: Array[CWLParameterReference]
            origin_3: Array[CWLParameterReference] = this.CWLInput
            next_1_3: Array[CWLParameterReference] = run.CWLInput
            if not append_sequences_1:
                def f_3(x_9: CWLParameterReference) -> CWLParameterReference:
                    return x_9

                s_3 = ResizeArray_map(f_3, next_1_3)

            else: 
                combined_3: Array[CWLParameterReference] = []
                enumerator_4: Any = get_enumerator(origin_3)
                try: 
                    while enumerator_4.System_Collections_IEnumerator_MoveNext():
                        e_4: CWLParameterReference = enumerator_4.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1283:
                            @property
                            def Equals(self) -> Callable[[CWLParameterReference, CWLParameterReference], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[CWLParameterReference], int]:
                                return safe_hash

                        if not contains_1(e_4, combined_3, ObjectExpr1283()):
                            (combined_3.append(e_4))


                finally: 
                    dispose(enumerator_4)

                enumerator_1_3: Any = get_enumerator(next_1_3)
                try: 
                    while enumerator_1_3.System_Collections_IEnumerator_MoveNext():
                        e_1_3: CWLParameterReference = enumerator_1_3.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1284:
                            @property
                            def Equals(self) -> Callable[[CWLParameterReference, CWLParameterReference], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[CWLParameterReference], int]:
                                return safe_hash

                        if not contains_1(e_1_3, combined_3, ObjectExpr1284()):
                            (combined_3.append(e_1_3))


                finally: 
                    dispose(enumerator_1_3)

                s_3 = combined_3

            this.CWLInput = s_3

        if True if (len(run.Comments) != 0) else update_always:
            s_4: Array[Comment]
            origin_4: Array[Comment] = this.Comments
            next_1_4: Array[Comment] = run.Comments
            if not append_sequences_1:
                def f_4(x_12: Comment) -> Comment:
                    return x_12

                s_4 = ResizeArray_map(f_4, next_1_4)

            else: 
                combined_4: Array[Comment] = []
                enumerator_5: Any = get_enumerator(origin_4)
                try: 
                    while enumerator_5.System_Collections_IEnumerator_MoveNext():
                        e_5: Comment = enumerator_5.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1285:
                            @property
                            def Equals(self) -> Callable[[Comment, Comment], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[Comment], int]:
                                return safe_hash

                        if not contains_1(e_5, combined_4, ObjectExpr1285()):
                            (combined_4.append(e_5))


                finally: 
                    dispose(enumerator_5)

                enumerator_1_4: Any = get_enumerator(next_1_4)
                try: 
                    while enumerator_1_4.System_Collections_IEnumerator_MoveNext():
                        e_1_4: Comment = enumerator_1_4.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1286:
                            @property
                            def Equals(self) -> Callable[[Comment, Comment], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[Comment], int]:
                                return safe_hash

                        if not contains_1(e_1_4, combined_4, ObjectExpr1286()):
                            (combined_4.append(e_1_4))


                finally: 
                    dispose(enumerator_1_4)

                s_4 = combined_4

            this.Comments = s_4


    def __str__(self, __unit: None=None) -> str:
        this: ArcRun = self
        arg: str = this.Identifier
        arg_1: str | None = this.Title
        arg_2: str | None = this.Description
        arg_3: OntologyAnnotation | None = this.MeasurementType
        arg_4: OntologyAnnotation | None = this.TechnologyType
        arg_5: OntologyAnnotation | None = this.TechnologyPlatform
        arg_6: Array[str] = this.WorkflowIdentifiers
        arg_7: Datamap | None = this.Datamap
        arg_8: Array[ArcTable] = this.Tables
        arg_9: Array[Person] = this.Performers
        arg_10: Array[Comment] = this.Comments
        return to_text(printf("ArcRun({\r\n    Identifier = \"%s\",\r\n    Title = %A,\r\n    Description = %A,\r\n    MeasurementType = %A,\r\n    TechnologyType = %A,\r\n    TechnologyPlatform = %A,\r\n    WorkflowIdentifiers = %A,\r\n    Datamap = %A,\r\n    Tables = %A,\r\n    Performers = %A,\r\n    Comments = %A\r\n})"))(arg)(arg_1)(arg_2)(arg_3)(arg_4)(arg_5)(arg_6)(arg_7)(arg_8)(arg_9)(arg_10)

    def AddToInvestigation(self, investigation: ArcInvestigation) -> None:
        this: ArcRun = self
        this.Investigation = investigation

    def RemoveFromInvestigation(self, __unit: None=None) -> None:
        this: ArcRun = self
        this.Investigation = None

    def StructurallyEquals(self, other: ArcRun) -> bool:
        this: ArcRun = self
        def predicate(x: bool) -> bool:
            return x == True

        def _arrow1289(__unit: None=None) -> bool:
            a: IEnumerable_1[str] = this.WorkflowIdentifiers
            b: IEnumerable_1[str] = other.WorkflowIdentifiers
            def folder(acc: bool, e: bool) -> bool:
                if acc:
                    return e

                else: 
                    return False


            def _arrow1288(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1287(i_1: int) -> bool:
                    return item(i_1, a) == item(i_1, b)

                return map_1(_arrow1287, range_big_int(0, 1, length(a) - 1))

            return fold(folder, True, to_list(delay(_arrow1288))) if (length(a) == length(b)) else False

        def _arrow1292(__unit: None=None) -> bool:
            a_1: IEnumerable_1[ArcTable] = this.Tables
            b_1: IEnumerable_1[ArcTable] = other.Tables
            def folder_1(acc_1: bool, e_1: bool) -> bool:
                if acc_1:
                    return e_1

                else: 
                    return False


            def _arrow1291(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1290(i_2: int) -> bool:
                    return equals(item(i_2, a_1), item(i_2, b_1))

                return map_1(_arrow1290, range_big_int(0, 1, length(a_1) - 1))

            return fold(folder_1, True, to_list(delay(_arrow1291))) if (length(a_1) == length(b_1)) else False

        def _arrow1295(__unit: None=None) -> bool:
            a_2: IEnumerable_1[Person] = this.Performers
            b_2: IEnumerable_1[Person] = other.Performers
            def folder_2(acc_2: bool, e_2: bool) -> bool:
                if acc_2:
                    return e_2

                else: 
                    return False


            def _arrow1294(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1293(i_3: int) -> bool:
                    return equals(item(i_3, a_2), item(i_3, b_2))

                return map_1(_arrow1293, range_big_int(0, 1, length(a_2) - 1))

            return fold(folder_2, True, to_list(delay(_arrow1294))) if (length(a_2) == length(b_2)) else False

        def _arrow1298(__unit: None=None) -> bool:
            a_3: IEnumerable_1[CWLParameterReference] = this.CWLInput
            b_3: IEnumerable_1[CWLParameterReference] = other.CWLInput
            def folder_3(acc_3: bool, e_3: bool) -> bool:
                if acc_3:
                    return e_3

                else: 
                    return False


            def _arrow1297(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1296(i_4: int) -> bool:
                    return equals(item(i_4, a_3), item(i_4, b_3))

                return map_1(_arrow1296, range_big_int(0, 1, length(a_3) - 1))

            return fold(folder_3, True, to_list(delay(_arrow1297))) if (length(a_3) == length(b_3)) else False

        def _arrow1301(__unit: None=None) -> bool:
            a_4: IEnumerable_1[Comment] = this.Comments
            b_4: IEnumerable_1[Comment] = other.Comments
            def folder_4(acc_4: bool, e_4: bool) -> bool:
                if acc_4:
                    return e_4

                else: 
                    return False


            def _arrow1300(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1299(i_5: int) -> bool:
                    return equals(item(i_5, a_4), item(i_5, b_4))

                return map_1(_arrow1299, range_big_int(0, 1, length(a_4) - 1))

            return fold(folder_4, True, to_list(delay(_arrow1300))) if (length(a_4) == length(b_4)) else False

        return for_all(predicate, to_enumerable([this.Identifier == other.Identifier, equals(this.Title, other.Title), equals(this.Description, other.Description), equals(this.MeasurementType, other.MeasurementType), equals(this.TechnologyType, other.TechnologyType), equals(this.TechnologyPlatform, other.TechnologyPlatform), _arrow1289(), equals(this.Datamap, other.Datamap), _arrow1292(), _arrow1295(), equals(this.CWLDescription, other.CWLDescription), _arrow1298(), _arrow1301()]))

    def ReferenceEquals(self, other: ArcRun) -> bool:
        this: ArcRun = self
        return this is other

    def __eq__(self, other: Any=None) -> bool:
        this: ArcRun = self
        return this.StructurallyEquals(other) if isinstance(other, ArcRun) else False

    def GetLightHashCode(self, __unit: None=None) -> Any:
        this: ArcRun = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.MeasurementType), box_hash_option(this.TechnologyType), box_hash_option(this.TechnologyPlatform), box_hash_seq(this.WorkflowIdentifiers), box_hash_seq(this.Tables), box_hash_seq(this.Performers), box_hash_seq(this.Comments)])

    def __hash__(self, __unit: None=None) -> Any:
        this: ArcRun = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.MeasurementType), box_hash_option(this.TechnologyType), box_hash_option(this.TechnologyPlatform), box_hash_option(this.Datamap), box_hash_seq(this.WorkflowIdentifiers), box_hash_seq(this.Tables), box_hash_seq(this.Performers), box_hash_option(this.CWLDescription), box_hash_seq(this.CWLInput), box_hash_seq(this.Comments)])


ArcRun_reflection = _expr1303

def ArcRun__ctor_287C1303(identifier: str, title: str | None=None, description: str | None=None, measurement_type: OntologyAnnotation | None=None, technology_type: OntologyAnnotation | None=None, technology_platform: OntologyAnnotation | None=None, workflow_identifiers: Array[str] | None=None, tables: Array[ArcTable] | None=None, datamap: Datamap | None=None, performers: Array[Person] | None=None, cwl_description: CWLProcessingUnit | None=None, cwl_input: Array[CWLParameterReference] | None=None, comments: Array[Comment] | None=None) -> ArcRun:
    return ArcRun(identifier, title, description, measurement_type, technology_type, technology_platform, workflow_identifiers, tables, datamap, performers, cwl_description, cwl_input, comments)


def _expr1438() -> TypeInfo:
    return class_type("ARCtrl.ArcInvestigation", None, ArcInvestigation)


class ArcInvestigation:
    def __init__(self, identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, ontology_source_references: Array[OntologySourceReference] | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, assays: Array[ArcAssay] | None=None, studies: Array[ArcStudy] | None=None, workflows: Array[ArcWorkflow] | None=None, runs: Array[ArcRun] | None=None, registered_study_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None, remarks: Array[Remark] | None=None) -> None:
        this: FSharpRef[ArcInvestigation] = FSharpRef(None)
        this.contents = self
        ontology_source_references_1: Array[OntologySourceReference] = default_arg(ontology_source_references, [])
        publications_1: Array[Publication] = default_arg(publications, [])
        contacts_1: Array[Person] = default_arg(contacts, [])
        assays_1: Array[ArcAssay]
        ass: Array[ArcAssay] = default_arg(assays, [])
        enumerator: Any = get_enumerator(ass)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                a: ArcAssay = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                a.Investigation = this.contents

        finally: 
            dispose(enumerator)

        assays_1 = ass
        studies_1: Array[ArcStudy]
        sss: Array[ArcStudy] = default_arg(studies, [])
        enumerator_1: Any = get_enumerator(sss)
        try: 
            while enumerator_1.System_Collections_IEnumerator_MoveNext():
                s: ArcStudy = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                s.Investigation = this.contents

        finally: 
            dispose(enumerator_1)

        studies_1 = sss
        workflows_1: Array[ArcWorkflow]
        wss: Array[ArcWorkflow] = default_arg(workflows, [])
        enumerator_2: Any = get_enumerator(wss)
        try: 
            while enumerator_2.System_Collections_IEnumerator_MoveNext():
                w: ArcWorkflow = enumerator_2.System_Collections_Generic_IEnumerator_1_get_Current()
                w.Investigation = this.contents

        finally: 
            dispose(enumerator_2)

        workflows_1 = wss
        runs_1: Array[ArcRun]
        rss: Array[ArcRun] = default_arg(runs, [])
        enumerator_3: Any = get_enumerator(rss)
        try: 
            while enumerator_3.System_Collections_IEnumerator_MoveNext():
                r: ArcRun = enumerator_3.System_Collections_Generic_IEnumerator_1_get_Current()
                r.Investigation = this.contents

        finally: 
            dispose(enumerator_3)

        runs_1 = rss
        registered_study_identifiers_1: Array[str] = default_arg(registered_study_identifiers, [])
        comments_1: Array[Comment] = default_arg(comments, [])
        remarks_1: Array[Remark] = default_arg(remarks, [])
        self.identifier_00401951: str = identifier
        self.title_00401952: str | None = title
        self.description_00401953: str | None = description
        self.submission_date_00401954: str | None = submission_date
        self.public_release_date_00401955: str | None = public_release_date
        self.ontology_source_references_00401956_002D1: Array[OntologySourceReference] = ontology_source_references_1
        self.publications_00401957_002D1: Array[Publication] = publications_1
        self.contacts_00401958_002D1: Array[Person] = contacts_1
        self.assays_00401959_002D1: Array[ArcAssay] = assays_1
        self.studies_00401960_002D1: Array[ArcStudy] = studies_1
        self.workflows_00401961_002D1: Array[ArcWorkflow] = workflows_1
        self.runs_00401962_002D1: Array[ArcRun] = runs_1
        self.registered_study_identifiers_00401963_002D1: Array[str] = registered_study_identifiers_1
        self.comments_00401964_002D1: Array[Comment] = comments_1
        self.remarks_00401965_002D1: Array[Remark] = remarks_1
        self.static_hash: int = 0
        self.init_00401922: int = 1

    @property
    def Identifier(self, __unit: None=None) -> str:
        this: ArcInvestigation = self
        return this.identifier_00401951

    @Identifier.setter
    def Identifier(self, i: str) -> None:
        this: ArcInvestigation = self
        this.identifier_00401951 = i

    @property
    def Title(self, __unit: None=None) -> str | None:
        this: ArcInvestigation = self
        return this.title_00401952

    @Title.setter
    def Title(self, n: str | None=None) -> None:
        this: ArcInvestigation = self
        this.title_00401952 = n

    @property
    def Description(self, __unit: None=None) -> str | None:
        this: ArcInvestigation = self
        return this.description_00401953

    @Description.setter
    def Description(self, n: str | None=None) -> None:
        this: ArcInvestigation = self
        this.description_00401953 = n

    @property
    def SubmissionDate(self, __unit: None=None) -> str | None:
        this: ArcInvestigation = self
        return this.submission_date_00401954

    @SubmissionDate.setter
    def SubmissionDate(self, n: str | None=None) -> None:
        this: ArcInvestigation = self
        this.submission_date_00401954 = n

    @property
    def PublicReleaseDate(self, __unit: None=None) -> str | None:
        this: ArcInvestigation = self
        return this.public_release_date_00401955

    @PublicReleaseDate.setter
    def PublicReleaseDate(self, n: str | None=None) -> None:
        this: ArcInvestigation = self
        this.public_release_date_00401955 = n

    @property
    def OntologySourceReferences(self, __unit: None=None) -> Array[OntologySourceReference]:
        this: ArcInvestigation = self
        return this.ontology_source_references_00401956_002D1

    @OntologySourceReferences.setter
    def OntologySourceReferences(self, n: Array[OntologySourceReference]) -> None:
        this: ArcInvestigation = self
        this.ontology_source_references_00401956_002D1 = n

    @property
    def Publications(self, __unit: None=None) -> Array[Publication]:
        this: ArcInvestigation = self
        return this.publications_00401957_002D1

    @Publications.setter
    def Publications(self, n: Array[Publication]) -> None:
        this: ArcInvestigation = self
        this.publications_00401957_002D1 = n

    @property
    def Contacts(self, __unit: None=None) -> Array[Person]:
        this: ArcInvestigation = self
        return this.contacts_00401958_002D1

    @Contacts.setter
    def Contacts(self, n: Array[Person]) -> None:
        this: ArcInvestigation = self
        this.contacts_00401958_002D1 = n

    @property
    def Assays(self, __unit: None=None) -> Array[ArcAssay]:
        this: ArcInvestigation = self
        return this.assays_00401959_002D1

    @Assays.setter
    def Assays(self, n: Array[ArcAssay]) -> None:
        this: ArcInvestigation = self
        this.assays_00401959_002D1 = n

    @property
    def Studies(self, __unit: None=None) -> Array[ArcStudy]:
        this: ArcInvestigation = self
        return this.studies_00401960_002D1

    @Studies.setter
    def Studies(self, n: Array[ArcStudy]) -> None:
        this: ArcInvestigation = self
        this.studies_00401960_002D1 = n

    @property
    def Workflows(self, __unit: None=None) -> Array[ArcWorkflow]:
        this: ArcInvestigation = self
        return this.workflows_00401961_002D1

    @Workflows.setter
    def Workflows(self, n: Array[ArcWorkflow]) -> None:
        this: ArcInvestigation = self
        this.workflows_00401961_002D1 = n

    @property
    def Runs(self, __unit: None=None) -> Array[ArcRun]:
        this: ArcInvestigation = self
        return this.runs_00401962_002D1

    @Runs.setter
    def Runs(self, n: Array[ArcRun]) -> None:
        this: ArcInvestigation = self
        this.runs_00401962_002D1 = n

    @property
    def RegisteredStudyIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcInvestigation = self
        return this.registered_study_identifiers_00401963_002D1

    @RegisteredStudyIdentifiers.setter
    def RegisteredStudyIdentifiers(self, n: Array[str]) -> None:
        this: ArcInvestigation = self
        this.registered_study_identifiers_00401963_002D1 = n

    @property
    def Comments(self, __unit: None=None) -> Array[Comment]:
        this: ArcInvestigation = self
        return this.comments_00401964_002D1

    @Comments.setter
    def Comments(self, n: Array[Comment]) -> None:
        this: ArcInvestigation = self
        this.comments_00401964_002D1 = n

    @property
    def Remarks(self, __unit: None=None) -> Array[Remark]:
        this: ArcInvestigation = self
        return this.remarks_00401965_002D1

    @Remarks.setter
    def Remarks(self, n: Array[Remark]) -> None:
        this: ArcInvestigation = self
        this.remarks_00401965_002D1 = n

    @property
    def StaticHash(self, __unit: None=None) -> int:
        this: ArcInvestigation = self
        return this.static_hash

    @StaticHash.setter
    def StaticHash(self, h: int) -> None:
        this: ArcInvestigation = self
        this.static_hash = h or 0

    @staticmethod
    def FileName() -> str:
        return "isa.investigation.xlsx"

    @staticmethod
    def init(identifier: str) -> ArcInvestigation:
        return ArcInvestigation(identifier)

    @staticmethod
    def create(identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, ontology_source_references: Array[OntologySourceReference] | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, assays: Array[ArcAssay] | None=None, studies: Array[ArcStudy] | None=None, workflows: Array[ArcWorkflow] | None=None, runs: Array[ArcRun] | None=None, registered_study_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None, remarks: Array[Remark] | None=None) -> ArcInvestigation:
        return ArcInvestigation(identifier, title, description, submission_date, public_release_date, ontology_source_references, publications, contacts, assays, studies, workflows, runs, registered_study_identifiers, comments, remarks)

    @staticmethod
    def make(identifier: str, title: str | None, description: str | None, submission_date: str | None, public_release_date: str | None, ontology_source_references: Array[OntologySourceReference], publications: Array[Publication], contacts: Array[Person], assays: Array[ArcAssay], studies: Array[ArcStudy], workflows: Array[ArcWorkflow], runs: Array[ArcRun], registered_study_identifiers: Array[str], comments: Array[Comment], remarks: Array[Remark]) -> ArcInvestigation:
        return ArcInvestigation(identifier, title, description, submission_date, public_release_date, ontology_source_references, publications, contacts, assays, studies, workflows, runs, registered_study_identifiers, comments, remarks)

    @property
    def AssayCount(self, __unit: None=None) -> int:
        this: ArcInvestigation = self
        return len(this.Assays)

    @property
    def AssayIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcInvestigation = self
        def mapping(x: ArcAssay) -> str:
            return x.Identifier

        return list(map_1(mapping, this.Assays))

    @property
    def UnregisteredAssays(self, __unit: None=None) -> Array[ArcAssay]:
        this: ArcInvestigation = self
        def f(a: ArcAssay) -> bool:
            def predicate(s: ArcStudy, a: Any=a) -> bool:
                def _arrow1304(i: str, s: Any=s) -> bool:
                    return i == a.Identifier

                return exists(_arrow1304, s.RegisteredAssayIdentifiers)

            return not exists(predicate, this.RegisteredStudies)

        return ResizeArray_filter(f, this.Assays)

    def AddAssay(self, assay: ArcAssay, register_in: Array[ArcStudy] | None=None) -> None:
        this: ArcInvestigation = self
        assay_ident: str = assay.Identifier
        def predicate(x_1: str) -> bool:
            return x_1 == assay_ident

        def mapping(x: ArcAssay) -> str:
            return x.Identifier

        match_value: int | None = try_find_index(predicate, map_1(mapping, this.Assays))
        if match_value is None:
            pass

        else: 
            raise Exception(((("Cannot create assay with name " + assay_ident) + ", as assay names must be unique and assay at index ") + str(match_value)) + " has the same name.")

        assay.Investigation = this
        (this.Assays.append(assay))
        if register_in is not None:
            enumerator: Any = get_enumerator(value_6(register_in))
            try: 
                while enumerator.System_Collections_IEnumerator_MoveNext():
                    study: ArcStudy = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                    study.RegisterAssay(assay.Identifier)

            finally: 
                dispose(enumerator)



    @staticmethod
    def add_assay(assay: ArcAssay, register_in: Array[ArcStudy] | None=None) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1305(inv: ArcInvestigation) -> ArcInvestigation:
            new_investigation: ArcInvestigation = inv.Copy()
            new_investigation.AddAssay(assay, register_in)
            return new_investigation

        return _arrow1305

    def InitAssay(self, assay_identifier: str, register_in: Array[ArcStudy] | None=None) -> ArcAssay:
        this: ArcInvestigation = self
        assay: ArcAssay = ArcAssay(assay_identifier)
        this.AddAssay(assay, register_in)
        return assay

    @staticmethod
    def init_assay(assay_identifier: str, register_in: Array[ArcStudy] | None=None) -> Callable[[ArcInvestigation], ArcAssay]:
        def _arrow1306(inv: ArcInvestigation) -> ArcAssay:
            new_investigation: ArcInvestigation = inv.Copy()
            return new_investigation.InitAssay(assay_identifier, register_in)

        return _arrow1306

    def DeleteAssayAt(self, index: int) -> None:
        this: ArcInvestigation = self
        this.Assays.pop(index)

    @staticmethod
    def delete_assay_at(index: int) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1307(inv: ArcInvestigation) -> ArcInvestigation:
            new_investigation: ArcInvestigation = inv.Copy()
            new_investigation.DeleteAssayAt(index)
            return new_investigation

        return _arrow1307

    def DeleteAssay(self, assay_identifier: str) -> None:
        this: ArcInvestigation = self
        index: int = this.GetAssayIndex(assay_identifier) or 0
        this.DeleteAssayAt(index)

    @staticmethod
    def delete_assay(assay_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1308(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.DeleteAssay(assay_identifier)
            return new_inv

        return _arrow1308

    def RemoveAssayAt(self, index: int) -> None:
        this: ArcInvestigation = self
        ident: str = this.GetAssayAt(index).Identifier
        this.Assays.pop(index)
        enumerator: Any = get_enumerator(this.Studies)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                study: ArcStudy = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                study.DeregisterAssay(ident)

        finally: 
            dispose(enumerator)


    @staticmethod
    def remove_assay_at(index: int) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1309(inv: ArcInvestigation) -> ArcInvestigation:
            new_investigation: ArcInvestigation = inv.Copy()
            new_investigation.RemoveAssayAt(index)
            return new_investigation

        return _arrow1309

    def RemoveAssay(self, assay_identifier: str) -> None:
        this: ArcInvestigation = self
        index: int = this.GetAssayIndex(assay_identifier) or 0
        this.RemoveAssayAt(index)

    @staticmethod
    def remove_assay(assay_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1310(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.RemoveAssay(assay_identifier)
            return new_inv

        return _arrow1310

    def RenameAssay(self, old_identifier: str, new_identifier: str) -> None:
        this: ArcInvestigation = self
        def action(a: ArcAssay) -> None:
            if a.Identifier == old_identifier:
                a.Identifier = new_identifier


        iterate(action, this.Assays)
        def action_1(s: ArcStudy) -> None:
            def predicate(ai: str, s: Any=s) -> bool:
                return ai == old_identifier

            index: int | None = try_find_index(predicate, s.RegisteredAssayIdentifiers)
            if index is not None:
                index_1: int = index or 0
                s.RegisteredAssayIdentifiers[index_1] = new_identifier


        iterate(action_1, this.Studies)

    @staticmethod
    def rename_assay(old_identifier: str, new_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1311(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.RenameAssay(old_identifier, new_identifier)
            return new_inv

        return _arrow1311

    def RenameRun(self, old_identifier: str, new_identifier: str) -> None:
        this: ArcInvestigation = self
        def action(a: ArcRun) -> None:
            if a.Identifier == old_identifier:
                a.Identifier = new_identifier


        iterate(action, this.Runs)

    @staticmethod
    def rename_run(old_identifier: str, new_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1312(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.RenameRun(old_identifier, new_identifier)
            return new_inv

        return _arrow1312

    def RenameWorkflow(self, old_identifier: str, new_identifier: str) -> None:
        this: ArcInvestigation = self
        def action(w: ArcWorkflow) -> None:
            if w.Identifier == old_identifier:
                w.Identifier = new_identifier

            def predicate(sub_id: str, w: Any=w) -> bool:
                return sub_id == old_identifier

            match_value: int | None = try_find_index(predicate, w.SubWorkflowIdentifiers)
            if match_value is not None:
                i: int = match_value or 0
                w.SubWorkflowIdentifiers[i] = new_identifier


        iterate(action, this.Workflows)
        def action_1(r: ArcRun) -> None:
            def predicate_1(w_id: str, r: Any=r) -> bool:
                return w_id == old_identifier

            match_value_1: int | None = try_find_index(predicate_1, r.WorkflowIdentifiers)
            if match_value_1 is not None:
                i_1: int = match_value_1 or 0
                r.WorkflowIdentifiers[i_1] = new_identifier


        iterate(action_1, this.Runs)

    @staticmethod
    def rename_workflow(old_identifier: str, new_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1313(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.RenameWorkflow(old_identifier, new_identifier)
            return new_inv

        return _arrow1313

    def SetAssayAt(self, index: int, assay: ArcAssay) -> None:
        this: ArcInvestigation = self
        assay_ident: str = assay.Identifier
        def predicate(x: str) -> bool:
            return x == assay_ident

        def mapping(a: ArcAssay) -> str:
            return a.Identifier

        match_value: int | None = try_find_index(predicate, map_1(mapping, remove_at(index, this.Assays)))
        if match_value is None:
            pass

        else: 
            raise Exception(((("Cannot create assay with name " + assay_ident) + ", as assay names must be unique and assay at index ") + str(match_value)) + " has the same name.")

        assay.Investigation = this
        this.Assays[index] = assay
        this.DeregisterMissingAssays()

    @staticmethod
    def set_assay_at(index: int, assay: ArcAssay) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1315(inv: ArcInvestigation) -> ArcInvestigation:
            new_investigation: ArcInvestigation = inv.Copy()
            new_investigation.SetAssayAt(index, assay)
            return new_investigation

        return _arrow1315

    def SetAssay(self, assay_identifier: str, assay: ArcAssay) -> None:
        this: ArcInvestigation = self
        index: int = this.GetAssayIndex(assay_identifier) or 0
        this.SetAssayAt(index, assay)

    @staticmethod
    def set_assay(assay_identifier: str, assay: ArcAssay) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1316(inv: ArcInvestigation) -> ArcInvestigation:
            new_investigation: ArcInvestigation = inv.Copy()
            new_investigation.SetAssay(assay_identifier, assay)
            return new_investigation

        return _arrow1316

    def GetAssayIndex(self, assay_identifier: str) -> int:
        this: ArcInvestigation = self
        def _arrow1317(a: ArcAssay) -> bool:
            return a.Identifier == assay_identifier

        index: int = find_index(_arrow1317, this.Assays) or 0
        if index == -1:
            raise Exception(("Unable to find assay with specified identifier \'" + assay_identifier) + "\'!")

        return index

    @staticmethod
    def get_assay_index(assay_identifier: str) -> Callable[[ArcInvestigation], int]:
        def _arrow1318(inv: ArcInvestigation) -> int:
            return inv.GetAssayIndex(assay_identifier)

        return _arrow1318

    def GetAssayAt(self, index: int) -> ArcAssay:
        this: ArcInvestigation = self
        return this.Assays[index]

    @staticmethod
    def get_assay_at(index: int) -> Callable[[ArcInvestigation], ArcAssay]:
        def _arrow1321(inv: ArcInvestigation) -> ArcAssay:
            new_investigation: ArcInvestigation = inv.Copy()
            return new_investigation.GetAssayAt(index)

        return _arrow1321

    def GetAssay(self, assay_identifier: str) -> ArcAssay:
        this: ArcInvestigation = self
        match_value: ArcAssay | None = this.TryGetAssay(assay_identifier)
        if match_value is None:
            raise Exception(ArcTypesAux_ErrorMsgs_unableToFindAssayIdentifier(assay_identifier, this.Identifier))

        else: 
            return match_value


    @staticmethod
    def get_assay(assay_identifier: str) -> Callable[[ArcInvestigation], ArcAssay]:
        def _arrow1322(inv: ArcInvestigation) -> ArcAssay:
            new_investigation: ArcInvestigation = inv.Copy()
            return new_investigation.GetAssay(assay_identifier)

        return _arrow1322

    def TryGetAssay(self, assay_identifier: str) -> ArcAssay | None:
        this: ArcInvestigation = self
        def _arrow1323(a: ArcAssay) -> bool:
            return a.Identifier == assay_identifier

        return try_find(_arrow1323, this.Assays)

    @staticmethod
    def try_get_assay(assay_identifier: str) -> Callable[[ArcInvestigation], ArcAssay | None]:
        def _arrow1324(inv: ArcInvestigation) -> ArcAssay | None:
            new_investigation: ArcInvestigation = inv.Copy()
            return new_investigation.TryGetAssay(assay_identifier)

        return _arrow1324

    def ContainsAssay(self, assay_identifier: str) -> bool:
        this: ArcInvestigation = self
        def predicate(a: ArcAssay) -> bool:
            return a.Identifier == assay_identifier

        return exists(predicate, this.Assays)

    @staticmethod
    def contains_assay(assay_identifier: str) -> Callable[[ArcInvestigation], bool]:
        def _arrow1325(inv: ArcInvestigation) -> bool:
            return inv.ContainsAssay(assay_identifier)

        return _arrow1325

    @property
    def RegisteredStudyIdentifierCount(self, __unit: None=None) -> int:
        this: ArcInvestigation = self
        return len(this.RegisteredStudyIdentifiers)

    @property
    def RegisteredStudies(self, __unit: None=None) -> Array[ArcStudy]:
        this: ArcInvestigation = self
        def f(identifier: str) -> ArcStudy | None:
            return this.TryGetStudy(identifier)

        return ResizeArray_choose(f, this.RegisteredStudyIdentifiers)

    @property
    def RegisteredStudyCount(self, __unit: None=None) -> int:
        this: ArcInvestigation = self
        return len(this.RegisteredStudies)

    @property
    def VacantStudyIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcInvestigation = self
        def f(arg: str) -> bool:
            return not this.ContainsStudy(arg)

        return ResizeArray_filter(f, this.RegisteredStudyIdentifiers)

    @property
    def StudyCount(self, __unit: None=None) -> int:
        this: ArcInvestigation = self
        return len(this.Studies)

    @property
    def StudyIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcInvestigation = self
        def mapping(x: ArcStudy) -> str:
            return x.Identifier

        return to_array(map_1(mapping, this.Studies))

    @property
    def UnregisteredStudies(self, __unit: None=None) -> Array[ArcStudy]:
        this: ArcInvestigation = self
        def f(s: ArcStudy) -> bool:
            def _arrow1328(__unit: None=None, s: Any=s) -> bool:
                source: Array[str] = this.RegisteredStudyIdentifiers
                def _arrow1327(__unit: None=None) -> Callable[[str], bool]:
                    x: str = s.Identifier
                    def _arrow1326(y: str) -> bool:
                        return x == y

                    return _arrow1326

                return exists(_arrow1327(), source)

            return not _arrow1328()

        return ResizeArray_filter(f, this.Studies)

    def AddStudy(self, study: ArcStudy) -> None:
        this: ArcInvestigation = self
        study_1: ArcStudy = study
        def predicate(x: ArcStudy) -> bool:
            return x.Identifier == study_1.Identifier

        match_value: int | None = try_find_index(predicate, this.Studies)
        if match_value is None:
            pass

        else: 
            raise Exception(((("Cannot create study with name " + study_1.Identifier) + ", as study names must be unique and study at index ") + str(match_value)) + " has the same name.")

        study.Investigation = this
        (this.Studies.append(study))

    @staticmethod
    def add_study(study: ArcStudy) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1329(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.AddStudy(study)
            return copy

        return _arrow1329

    def InitStudy(self, study_identifier: str) -> ArcStudy:
        this: ArcInvestigation = self
        study: ArcStudy = ArcStudy.init(study_identifier)
        this.AddStudy(study)
        return study

    @staticmethod
    def init_study(study_identifier: str) -> Callable[[ArcInvestigation], tuple[ArcInvestigation, ArcStudy]]:
        def _arrow1343(inv: ArcInvestigation) -> tuple[ArcInvestigation, ArcStudy]:
            copy: ArcInvestigation = inv.Copy()
            return (copy, copy.InitStudy(study_identifier))

        return _arrow1343

    def RegisterStudy(self, study_identifier: str) -> None:
        this: ArcInvestigation = self
        study_ident: str = study_identifier
        def predicate(x: str) -> bool:
            return x == study_ident

        match_value: str | None = try_find(predicate, this.StudyIdentifiers)
        if match_value is not None:
            pass

        else: 
            raise Exception(("The given study with identifier \'" + study_ident) + "\' must be added to Investigation before it can be registered.")

        study_ident_1: str = study_identifier
        class ObjectExpr1345:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1344(x_1: str, y: str) -> bool:
                    return x_1 == y

                return _arrow1344

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if contains(study_ident_1, this.RegisteredStudyIdentifiers, ObjectExpr1345()):
            raise Exception(("Study with identifier \'" + study_ident_1) + "\' is already registered!")

        (this.RegisteredStudyIdentifiers.append(study_identifier))

    @staticmethod
    def register_study(study_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1346(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.RegisterStudy(study_identifier)
            return copy

        return _arrow1346

    def AddRegisteredStudy(self, study: ArcStudy) -> None:
        this: ArcInvestigation = self
        this.AddStudy(study)
        this.RegisterStudy(study.Identifier)

    @staticmethod
    def add_registered_study(study: ArcStudy) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1347(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            study_1: ArcStudy = study.Copy()
            copy.AddRegisteredStudy(study_1)
            return copy

        return _arrow1347

    def DeleteStudyAt(self, index: int) -> None:
        this: ArcInvestigation = self
        this.Studies.pop(index)

    @staticmethod
    def delete_study_at(index: int) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1348(i: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = i.Copy()
            copy.DeleteStudyAt(index)
            return copy

        return _arrow1348

    def DeleteStudy(self, study_identifier: str) -> None:
        this: ArcInvestigation = self
        def _arrow1349(s: ArcStudy) -> bool:
            return s.Identifier == study_identifier

        index: int = find_index(_arrow1349, this.Studies) or 0
        this.DeleteStudyAt(index)

    @staticmethod
    def delete_study(study_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1350(i: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = i.Copy()
            copy.DeleteStudy(study_identifier)
            return copy

        return _arrow1350

    def RemoveStudyAt(self, index: int) -> None:
        this: ArcInvestigation = self
        ident: str = this.GetStudyAt(index).Identifier
        this.Studies.pop(index)
        this.DeregisterStudy(ident)

    @staticmethod
    def remove_study_at(index: int) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1351(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.RemoveStudyAt(index)
            return new_inv

        return _arrow1351

    def RemoveStudy(self, study_identifier: str) -> None:
        this: ArcInvestigation = self
        index: int = this.GetStudyIndex(study_identifier) or 0
        this.RemoveStudyAt(index)

    @staticmethod
    def remove_study(study_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1352(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.RemoveStudy(study_identifier)
            return copy

        return _arrow1352

    def RenameStudy(self, old_identifier: str, new_identifier: str) -> None:
        this: ArcInvestigation = self
        def action(s: ArcStudy) -> None:
            if s.Identifier == old_identifier:
                s.Identifier = new_identifier


        iterate(action, this.Studies)
        def predicate(si: str) -> bool:
            return si == old_identifier

        index: int | None = try_find_index(predicate, this.RegisteredStudyIdentifiers)
        if index is not None:
            index_1: int = index or 0
            this.RegisteredStudyIdentifiers[index_1] = new_identifier


    @staticmethod
    def rename_study(old_identifier: str, new_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1353(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.RenameStudy(old_identifier, new_identifier)
            return new_inv

        return _arrow1353

    def SetStudyAt(self, index: int, study: ArcStudy) -> None:
        this: ArcInvestigation = self
        study_1: ArcStudy = study
        def predicate(x: ArcStudy) -> bool:
            return x.Identifier == study_1.Identifier

        match_value: int | None = try_find_index(predicate, remove_at(index, this.Studies))
        if match_value is None:
            pass

        else: 
            raise Exception(((("Cannot create study with name " + study_1.Identifier) + ", as study names must be unique and study at index ") + str(match_value)) + " has the same name.")

        study.Investigation = this
        this.Studies[index] = study

    @staticmethod
    def set_study_at(index: int, study: ArcStudy) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1354(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.SetStudyAt(index, study)
            return new_inv

        return _arrow1354

    def SetStudy(self, study_identifier: str, study: ArcStudy) -> None:
        this: ArcInvestigation = self
        index: int = this.GetStudyIndex(study_identifier) or 0
        this.SetStudyAt(index, study)

    @staticmethod
    def set_study(study_identifier: str, study: ArcStudy) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1355(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.SetStudy(study_identifier, study)
            return new_inv

        return _arrow1355

    def GetStudyIndex(self, study_identifier: str) -> int:
        this: ArcInvestigation = self
        def _arrow1356(s: ArcStudy) -> bool:
            return s.Identifier == study_identifier

        index: int = find_index(_arrow1356, this.Studies) or 0
        if index == -1:
            raise Exception(("Unable to find study with specified identifier \'" + study_identifier) + "\'!")

        return index

    @staticmethod
    def get_study_index(study_identifier: str) -> Callable[[ArcInvestigation], int]:
        def _arrow1357(inv: ArcInvestigation) -> int:
            return inv.GetStudyIndex(study_identifier)

        return _arrow1357

    def GetStudyAt(self, index: int) -> ArcStudy:
        this: ArcInvestigation = self
        return this.Studies[index]

    @staticmethod
    def get_study_at(index: int) -> Callable[[ArcInvestigation], ArcStudy]:
        def _arrow1358(inv: ArcInvestigation) -> ArcStudy:
            new_inv: ArcInvestigation = inv.Copy()
            return new_inv.GetStudyAt(index)

        return _arrow1358

    def GetStudy(self, study_identifier: str) -> ArcStudy:
        this: ArcInvestigation = self
        match_value: ArcStudy | None = this.TryGetStudy(study_identifier)
        if match_value is None:
            raise Exception(ArcTypesAux_ErrorMsgs_unableToFindStudyIdentifier(study_identifier, this.Identifier))

        else: 
            return match_value


    @staticmethod
    def get_study(study_identifier: str) -> Callable[[ArcInvestigation], ArcStudy]:
        def _arrow1359(inv: ArcInvestigation) -> ArcStudy:
            new_inv: ArcInvestigation = inv.Copy()
            return new_inv.GetStudy(study_identifier)

        return _arrow1359

    def TryGetStudy(self, study_identifier: str) -> ArcStudy | None:
        this: ArcInvestigation = self
        def predicate(s: ArcStudy) -> bool:
            return s.Identifier == study_identifier

        return try_find(predicate, this.Studies)

    @staticmethod
    def try_get_study(study_identifier: str) -> Callable[[ArcInvestigation], ArcStudy | None]:
        def _arrow1360(inv: ArcInvestigation) -> ArcStudy | None:
            new_inv: ArcInvestigation = inv.Copy()
            return new_inv.TryGetStudy(study_identifier)

        return _arrow1360

    def ContainsStudy(self, study_identifier: str) -> bool:
        this: ArcInvestigation = self
        def predicate(s: ArcStudy) -> bool:
            return s.Identifier == study_identifier

        return exists(predicate, this.Studies)

    @staticmethod
    def contains_study(study_identifier: str) -> Callable[[ArcInvestigation], bool]:
        def _arrow1361(inv: ArcInvestigation) -> bool:
            return inv.ContainsStudy(study_identifier)

        return _arrow1361

    def RegisterAssayAt(self, study_index: int, assay_identifier: str) -> None:
        this: ArcInvestigation = self
        study: ArcStudy = this.GetStudyAt(study_index)
        def predicate(x: str) -> bool:
            return x == assay_identifier

        def mapping(a: ArcAssay) -> str:
            return a.Identifier

        match_value: str | None = try_find(predicate, map_1(mapping, this.Assays))
        if match_value is not None:
            pass

        else: 
            raise Exception("The given assay must be added to Investigation before it can be registered.")

        assay_ident_1: str = assay_identifier
        def predicate_1(x_1: str) -> bool:
            return x_1 == assay_ident_1

        match_value_1: int | None = try_find_index(predicate_1, study.RegisteredAssayIdentifiers)
        if match_value_1 is None:
            pass

        else: 
            raise Exception(((("Cannot create assay with name " + assay_ident_1) + ", as assay names must be unique and assay at index ") + str(match_value_1)) + " has the same name.")

        study.RegisterAssay(assay_identifier)

    @staticmethod
    def register_assay_at(study_index: int, assay_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1362(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.RegisterAssayAt(study_index, assay_identifier)
            return copy

        return _arrow1362

    def RegisterAssay(self, study_identifier: str, assay_identifier: str) -> None:
        this: ArcInvestigation = self
        index: int = this.GetStudyIndex(study_identifier) or 0
        this.RegisterAssayAt(index, assay_identifier)

    @staticmethod
    def register_assay(study_identifier: str, assay_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1363(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.RegisterAssay(study_identifier, assay_identifier)
            return copy

        return _arrow1363

    def DeregisterAssayAt(self, study_index: int, assay_identifier: str) -> None:
        this: ArcInvestigation = self
        study: ArcStudy = this.GetStudyAt(study_index)
        study.DeregisterAssay(assay_identifier)

    @staticmethod
    def deregister_assay_at(study_index: int, assay_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1364(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.DeregisterAssayAt(study_index, assay_identifier)
            return copy

        return _arrow1364

    def DeregisterAssay(self, study_identifier: str, assay_identifier: str) -> None:
        this: ArcInvestigation = self
        index: int = this.GetStudyIndex(study_identifier) or 0
        this.DeregisterAssayAt(index, assay_identifier)

    @staticmethod
    def deregister_assay(study_identifier: str, assay_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1365(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.DeregisterAssay(study_identifier, assay_identifier)
            return copy

        return _arrow1365

    def DeregisterStudy(self, study_identifier: str) -> None:
        this: ArcInvestigation = self
        class ObjectExpr1367:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1366(x: str, y: str) -> bool:
                    return x == y

                return _arrow1366

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        ignore(remove_in_place(study_identifier, this.RegisteredStudyIdentifiers, ObjectExpr1367()))

    @staticmethod
    def deregister_study(study_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1368(i: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = i.Copy()
            copy.DeregisterStudy(study_identifier)
            return copy

        return _arrow1368

    @property
    def WorkflowCount(self, __unit: None=None) -> int:
        this: ArcInvestigation = self
        return len(this.Workflows)

    @property
    def WorkflowIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcInvestigation = self
        def mapping(x: ArcWorkflow) -> str:
            return x.Identifier

        return to_array(map_1(mapping, this.Workflows))

    def GetWorkflowIndex(self, workflow_identifier: str) -> int:
        this: ArcInvestigation = self
        def _arrow1369(w: ArcWorkflow) -> bool:
            return w.Identifier == workflow_identifier

        index: int = find_index(_arrow1369, this.Workflows) or 0
        if index == -1:
            raise Exception(("Unable to find workflow with specified identifier \'" + workflow_identifier) + "\'!")

        return index

    @staticmethod
    def get_workflow_index(workflow_identifier: str) -> Callable[[ArcInvestigation], int]:
        def _arrow1370(inv: ArcInvestigation) -> int:
            return inv.GetWorkflowIndex(workflow_identifier)

        return _arrow1370

    def AddWorkflow(self, workflow: ArcWorkflow) -> None:
        this: ArcInvestigation = self
        workflow_1: ArcWorkflow = workflow
        def predicate(x: ArcWorkflow) -> bool:
            return x.Identifier == workflow_1.Identifier

        match_value: int | None = try_find_index(predicate, this.Workflows)
        if match_value is None:
            pass

        else: 
            raise Exception(((("Cannot create workflow with name " + workflow_1.Identifier) + ", as workflow names must be unique and workflow at index ") + str(match_value)) + " has the same name.")

        workflow.Investigation = this
        (this.Workflows.append(workflow))

    @staticmethod
    def add_workflow(workflow: ArcWorkflow) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1371(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.AddWorkflow(workflow)
            return copy

        return _arrow1371

    def InitWorkflow(self, workflow_identifier: str) -> ArcWorkflow:
        this: ArcInvestigation = self
        workflow: ArcWorkflow = ArcWorkflow.init(workflow_identifier)
        this.AddWorkflow(workflow)
        return workflow

    @staticmethod
    def init_workflow(workflow_identifier: str) -> Callable[[ArcInvestigation], ArcWorkflow]:
        def _arrow1372(inv: ArcInvestigation) -> ArcWorkflow:
            copy: ArcInvestigation = inv.Copy()
            return copy.InitWorkflow(workflow_identifier)

        return _arrow1372

    def DeleteWorkflowAt(self, index: int) -> None:
        this: ArcInvestigation = self
        this.Workflows.pop(index)

    @staticmethod
    def delete_workflow_at(index: int) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1373(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.DeleteWorkflowAt(index)
            return copy

        return _arrow1373

    def DeleteWorkflow(self, workflow_identifier: str) -> None:
        this: ArcInvestigation = self
        def _arrow1374(w: ArcWorkflow) -> bool:
            return w.Identifier == workflow_identifier

        index: int = find_index(_arrow1374, this.Workflows) or 0
        this.DeleteWorkflowAt(index)
        def action(w_1: ArcWorkflow) -> None:
            def predicate(swi: str, w_1: Any=w_1) -> bool:
                return swi == workflow_identifier

            match_value: int | None = try_find_index(predicate, w_1.SubWorkflowIdentifiers)
            if match_value is not None:
                swi_index: int = match_value or 0
                w_1.SubWorkflowIdentifiers.pop(swi_index)


        iterate(action, this.Workflows)
        def action_1(r: ArcRun) -> None:
            def predicate_1(wi: str, r: Any=r) -> bool:
                return wi == workflow_identifier

            match_value_1: int | None = try_find_index(predicate_1, r.WorkflowIdentifiers)
            if match_value_1 is not None:
                wi_index: int = match_value_1 or 0
                r.WorkflowIdentifiers.pop(wi_index)


        iterate(action_1, this.Runs)

    @staticmethod
    def delete_workflow(workflow_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1375(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.DeleteWorkflow(workflow_identifier)
            return copy

        return _arrow1375

    def GetWorkflowAt(self, index: int) -> ArcWorkflow:
        this: ArcInvestigation = self
        return this.Workflows[index]

    @staticmethod
    def get_workflow_at(index: int) -> Callable[[ArcInvestigation], ArcWorkflow]:
        def _arrow1376(inv: ArcInvestigation) -> ArcWorkflow:
            copy: ArcInvestigation = inv.Copy()
            return copy.GetWorkflowAt(index)

        return _arrow1376

    def GetWorkflow(self, workflow_identifier: str) -> ArcWorkflow:
        this: ArcInvestigation = self
        match_value: ArcWorkflow | None = this.TryGetWorkflow(workflow_identifier)
        if match_value is None:
            raise Exception(ArcTypesAux_ErrorMsgs_unableToFindWorkflowIdentifier(workflow_identifier, this.Identifier))

        else: 
            return match_value


    @staticmethod
    def get_workflow(workflow_identifier: str) -> Callable[[ArcInvestigation], ArcWorkflow]:
        def _arrow1377(inv: ArcInvestigation) -> ArcWorkflow:
            copy: ArcInvestigation = inv.Copy()
            return copy.GetWorkflow(workflow_identifier)

        return _arrow1377

    def TryGetWorkflow(self, workflow_identifier: str) -> ArcWorkflow | None:
        this: ArcInvestigation = self
        def predicate(w: ArcWorkflow) -> bool:
            return w.Identifier == workflow_identifier

        return try_find(predicate, this.Workflows)

    @staticmethod
    def try_get_workflow(workflow_identifier: str) -> Callable[[ArcInvestigation], ArcWorkflow | None]:
        def _arrow1378(inv: ArcInvestigation) -> ArcWorkflow | None:
            copy: ArcInvestigation = inv.Copy()
            return copy.TryGetWorkflow(workflow_identifier)

        return _arrow1378

    def ContainsWorkflow(self, workflow_identifier: str) -> bool:
        this: ArcInvestigation = self
        def predicate(w: ArcWorkflow) -> bool:
            return w.Identifier == workflow_identifier

        return exists(predicate, this.Workflows)

    @staticmethod
    def contains_workflow(workflow_identifier: str) -> Callable[[ArcInvestigation], bool]:
        def _arrow1379(inv: ArcInvestigation) -> bool:
            return inv.ContainsWorkflow(workflow_identifier)

        return _arrow1379

    def SetWorkflowAt(self, index: int, workflow: ArcWorkflow) -> None:
        this: ArcInvestigation = self
        workflow_1: ArcWorkflow = workflow
        def predicate(x: ArcWorkflow) -> bool:
            return x.Identifier == workflow_1.Identifier

        match_value: int | None = try_find_index(predicate, remove_at(index, this.Workflows))
        if match_value is None:
            pass

        else: 
            raise Exception(((("Cannot create workflow with name " + workflow_1.Identifier) + ", as workflow names must be unique and workflow at index ") + str(match_value)) + " has the same name.")

        workflow.Investigation = this
        this.Workflows[index] = workflow

    def SetWorkflow(self, workflow_identifier: str, workflow: ArcWorkflow) -> None:
        this: ArcInvestigation = self
        index: int = this.GetWorkflowIndex(workflow_identifier) or 0
        this.SetWorkflowAt(index, workflow)

    @staticmethod
    def set_workflow(workflow_identifier: str, workflow: ArcWorkflow) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1380(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.SetWorkflow(workflow_identifier, workflow)
            return copy

        return _arrow1380

    @staticmethod
    def set_workflow_at(index: int, workflow: ArcWorkflow) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1381(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.SetWorkflowAt(index, workflow)
            return copy

        return _arrow1381

    @property
    def RunCount(self, __unit: None=None) -> int:
        this: ArcInvestigation = self
        return len(this.Runs)

    @property
    def RunIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcInvestigation = self
        def mapping(x: ArcRun) -> str:
            return x.Identifier

        return to_array(map_1(mapping, this.Runs))

    def GetRunIndex(self, run_identifier: str) -> int:
        this: ArcInvestigation = self
        def _arrow1382(r: ArcRun) -> bool:
            return r.Identifier == run_identifier

        index: int = find_index(_arrow1382, this.Runs) or 0
        if index == -1:
            raise Exception(("Unable to find run with specified identifier \'" + run_identifier) + "\'!")

        return index

    @staticmethod
    def get_run_index(run_identifier: str) -> Callable[[ArcInvestigation], int]:
        def _arrow1385(inv: ArcInvestigation) -> int:
            return inv.GetRunIndex(run_identifier)

        return _arrow1385

    def AddRun(self, run: ArcRun) -> None:
        this: ArcInvestigation = self
        run_1: ArcRun = run
        def predicate(x: ArcRun) -> bool:
            return x.Identifier == run_1.Identifier

        match_value: int | None = try_find_index(predicate, this.Runs)
        if match_value is None:
            pass

        else: 
            raise Exception(((("Cannot create run with name " + run_1.Identifier) + ", as run names must be unique and run at index ") + str(match_value)) + " has the same name.")

        run.Investigation = this
        (this.Runs.append(run))

    @staticmethod
    def add_run(run: ArcRun) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1386(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.AddRun(run)
            return copy

        return _arrow1386

    def InitRun(self, run_identifier: str) -> ArcRun:
        this: ArcInvestigation = self
        run: ArcRun = ArcRun.init(run_identifier)
        this.AddRun(run)
        return run

    @staticmethod
    def init_run(run_identifier: str) -> Callable[[ArcInvestigation], ArcRun]:
        def _arrow1387(inv: ArcInvestigation) -> ArcRun:
            copy: ArcInvestigation = inv.Copy()
            return copy.InitRun(run_identifier)

        return _arrow1387

    def DeleteRunAt(self, index: int) -> None:
        this: ArcInvestigation = self
        this.Runs.pop(index)

    @staticmethod
    def delete_run_at(index: int) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1388(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.DeleteRunAt(index)
            return copy

        return _arrow1388

    def DeleteRun(self, run_identifier: str) -> None:
        this: ArcInvestigation = self
        def _arrow1389(w: ArcRun) -> bool:
            return w.Identifier == run_identifier

        index: int = find_index(_arrow1389, this.Runs) or 0
        this.DeleteRunAt(index)

    @staticmethod
    def delete_run(run_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1390(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.DeleteRun(run_identifier)
            return copy

        return _arrow1390

    def GetRunAt(self, index: int) -> ArcRun:
        this: ArcInvestigation = self
        return this.Runs[index]

    @staticmethod
    def get_run_at(index: int) -> Callable[[ArcInvestigation], ArcRun]:
        def _arrow1391(inv: ArcInvestigation) -> ArcRun:
            copy: ArcInvestigation = inv.Copy()
            return copy.GetRunAt(index)

        return _arrow1391

    def GetRun(self, run_identifier: str) -> ArcRun:
        this: ArcInvestigation = self
        match_value: ArcRun | None = this.TryGetRun(run_identifier)
        if match_value is None:
            raise Exception(ArcTypesAux_ErrorMsgs_unableToFindRunIdentifier(run_identifier, this.Identifier))

        else: 
            return match_value


    @staticmethod
    def get_run(run_identifier: str) -> Callable[[ArcInvestigation], ArcRun]:
        def _arrow1392(inv: ArcInvestigation) -> ArcRun:
            copy: ArcInvestigation = inv.Copy()
            return copy.GetRun(run_identifier)

        return _arrow1392

    def TryGetRun(self, run_identifier: str) -> ArcRun | None:
        this: ArcInvestigation = self
        def predicate(w: ArcRun) -> bool:
            return w.Identifier == run_identifier

        return try_find(predicate, this.Runs)

    @staticmethod
    def try_get_run(run_identifier: str) -> Callable[[ArcInvestigation], ArcRun | None]:
        def _arrow1393(inv: ArcInvestigation) -> ArcRun | None:
            copy: ArcInvestigation = inv.Copy()
            return copy.TryGetRun(run_identifier)

        return _arrow1393

    def ContainsRun(self, run_identifier: str) -> bool:
        this: ArcInvestigation = self
        def predicate(w: ArcRun) -> bool:
            return w.Identifier == run_identifier

        return exists(predicate, this.Runs)

    @staticmethod
    def contains_run(run_identifier: str) -> Callable[[ArcInvestigation], bool]:
        def _arrow1394(inv: ArcInvestigation) -> bool:
            return inv.ContainsRun(run_identifier)

        return _arrow1394

    def SetRunAt(self, index: int, run: ArcRun) -> None:
        this: ArcInvestigation = self
        run_1: ArcRun = run
        def predicate(x: ArcRun) -> bool:
            return x.Identifier == run_1.Identifier

        match_value: int | None = try_find_index(predicate, remove_at(index, this.Runs))
        if match_value is None:
            pass

        else: 
            raise Exception(((("Cannot create run with name " + run_1.Identifier) + ", as run names must be unique and run at index ") + str(match_value)) + " has the same name.")

        run.Investigation = this
        this.Runs[index] = run

    def SetRun(self, run_identifier: str, run: ArcRun) -> None:
        this: ArcInvestigation = self
        index: int = this.GetRunIndex(run_identifier) or 0
        this.SetRunAt(index, run)

    @staticmethod
    def set_run_at(index: int, run: ArcRun) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1395(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.SetRunAt(index, run)
            return copy

        return _arrow1395

    @staticmethod
    def set_run(run_identifier: str, run: ArcRun) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1396(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.SetRun(run_identifier, run)
            return copy

        return _arrow1396

    def GetAllPersons(self, __unit: None=None) -> Array[Person]:
        this: ArcInvestigation = self
        persons: Array[Person] = []
        enumerator: Any = get_enumerator(this.Assays)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                a: ArcAssay = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                add_range_in_place(a.Performers, persons)

        finally: 
            dispose(enumerator)

        enumerator_1: Any = get_enumerator(this.Studies)
        try: 
            while enumerator_1.System_Collections_IEnumerator_MoveNext():
                s: ArcStudy = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                add_range_in_place(s.Contacts, persons)

        finally: 
            dispose(enumerator_1)

        add_range_in_place(this.Contacts, persons)
        class ObjectExpr1397:
            @property
            def Equals(self) -> Callable[[Person, Person], bool]:
                return equals

            @property
            def GetHashCode(self) -> Callable[[Person], int]:
                return safe_hash

        return Array_distinct(list(persons), ObjectExpr1397())

    def GetAllPublications(self, __unit: None=None) -> Array[Publication]:
        this: ArcInvestigation = self
        pubs: Array[Publication] = []
        enumerator: Any = get_enumerator(this.Studies)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                s: ArcStudy = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                add_range_in_place(s.Publications, pubs)

        finally: 
            dispose(enumerator)

        add_range_in_place(this.Publications, pubs)
        class ObjectExpr1398:
            @property
            def Equals(self) -> Callable[[Publication, Publication], bool]:
                return equals

            @property
            def GetHashCode(self) -> Callable[[Publication], int]:
                return safe_hash

        return Array_distinct(list(pubs), ObjectExpr1398())

    def DeregisterMissingAssays(self, __unit: None=None) -> None:
        this: ArcInvestigation = self
        inv: ArcInvestigation = this
        existing_assays: Array[str] = inv.AssayIdentifiers
        enumerator: Any = get_enumerator(inv.Studies)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                study: ArcStudy = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                enumerator_1: Any = get_enumerator(list(study.RegisteredAssayIdentifiers))
                try: 
                    while enumerator_1.System_Collections_IEnumerator_MoveNext():
                        registered_assay: str = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1400:
                            @property
                            def Equals(self) -> Callable[[str, str], bool]:
                                def _arrow1399(x: str, y: str) -> bool:
                                    return x == y

                                return _arrow1399

                            @property
                            def GetHashCode(self) -> Callable[[str], int]:
                                return string_hash

                        if not contains(registered_assay, existing_assays, ObjectExpr1400()):
                            value_1: None = study.DeregisterAssay(registered_assay)
                            ignore(None)


                finally: 
                    dispose(enumerator_1)


        finally: 
            dispose(enumerator)


    @staticmethod
    def deregister_missing_assays(__unit: None=None) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1401(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.DeregisterMissingAssays()
            return copy

        return _arrow1401

    def UpdateIOTypeByEntityID(self, __unit: None=None) -> None:
        this: ArcInvestigation = self
        def _arrow1407(__unit: None=None) -> IEnumerable_1[ArcTable]:
            def _arrow1402(study: ArcStudy) -> IEnumerable_1[ArcTable]:
                return study.Tables

            def _arrow1406(__unit: None=None) -> IEnumerable_1[ArcTable]:
                def _arrow1403(assay: ArcAssay) -> IEnumerable_1[ArcTable]:
                    return assay.Tables

                def _arrow1405(__unit: None=None) -> IEnumerable_1[ArcTable]:
                    def _arrow1404(run: ArcRun) -> IEnumerable_1[ArcTable]:
                        return run.Tables

                    return collect(_arrow1404, this.Runs)

                return append_5(collect(_arrow1403, this.Assays), delay(_arrow1405))

            return append_5(collect(_arrow1402, this.Studies), delay(_arrow1406))

        io_map: Any = ArcTablesAux_getIOMap(list(to_list(delay(_arrow1407))))
        enumerator: Any = get_enumerator(this.Studies)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                study_1: ArcStudy = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                ArcTablesAux_applyIOMap(io_map, study_1.Tables)

        finally: 
            dispose(enumerator)

        enumerator_1: Any = get_enumerator(this.Assays)
        try: 
            while enumerator_1.System_Collections_IEnumerator_MoveNext():
                assay_1: ArcAssay = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                ArcTablesAux_applyIOMap(io_map, assay_1.Tables)

        finally: 
            dispose(enumerator_1)

        enumerator_2: Any = get_enumerator(this.Runs)
        try: 
            while enumerator_2.System_Collections_IEnumerator_MoveNext():
                run_1: ArcRun = enumerator_2.System_Collections_Generic_IEnumerator_1_get_Current()
                ArcTablesAux_applyIOMap(io_map, run_1.Tables)

        finally: 
            dispose(enumerator_2)


    def Copy(self, __unit: None=None) -> ArcInvestigation:
        this: ArcInvestigation = self
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
        return ArcInvestigation(this.Identifier, this.Title, this.Description, this.SubmissionDate, this.PublicReleaseDate, next_ontology_source_references, next_publications, next_contacts, next_assays, next_studies, next_workflows, next_runs, next_study_identifiers, next_comments, next_remarks)

    def StructurallyEquals(self, other: ArcInvestigation) -> bool:
        this: ArcInvestigation = self
        def predicate(x: bool) -> bool:
            return x == True

        def _arrow1410(__unit: None=None) -> bool:
            a: IEnumerable_1[Publication] = this.Publications
            b: IEnumerable_1[Publication] = other.Publications
            def folder(acc: bool, e: bool) -> bool:
                if acc:
                    return e

                else: 
                    return False


            def _arrow1409(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1408(i_1: int) -> bool:
                    return equals(item(i_1, a), item(i_1, b))

                return map_1(_arrow1408, range_big_int(0, 1, length(a) - 1))

            return fold(folder, True, to_list(delay(_arrow1409))) if (length(a) == length(b)) else False

        def _arrow1413(__unit: None=None) -> bool:
            a_1: IEnumerable_1[Person] = this.Contacts
            b_1: IEnumerable_1[Person] = other.Contacts
            def folder_1(acc_1: bool, e_1: bool) -> bool:
                if acc_1:
                    return e_1

                else: 
                    return False


            def _arrow1412(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1411(i_2: int) -> bool:
                    return equals(item(i_2, a_1), item(i_2, b_1))

                return map_1(_arrow1411, range_big_int(0, 1, length(a_1) - 1))

            return fold(folder_1, True, to_list(delay(_arrow1412))) if (length(a_1) == length(b_1)) else False

        def _arrow1416(__unit: None=None) -> bool:
            a_2: IEnumerable_1[OntologySourceReference] = this.OntologySourceReferences
            b_2: IEnumerable_1[OntologySourceReference] = other.OntologySourceReferences
            def folder_2(acc_2: bool, e_2: bool) -> bool:
                if acc_2:
                    return e_2

                else: 
                    return False


            def _arrow1415(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1414(i_3: int) -> bool:
                    return equals(item(i_3, a_2), item(i_3, b_2))

                return map_1(_arrow1414, range_big_int(0, 1, length(a_2) - 1))

            return fold(folder_2, True, to_list(delay(_arrow1415))) if (length(a_2) == length(b_2)) else False

        def _arrow1419(__unit: None=None) -> bool:
            a_3: IEnumerable_1[ArcAssay] = this.Assays
            b_3: IEnumerable_1[ArcAssay] = other.Assays
            def folder_3(acc_3: bool, e_3: bool) -> bool:
                if acc_3:
                    return e_3

                else: 
                    return False


            def _arrow1418(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1417(i_4: int) -> bool:
                    return equals(item(i_4, a_3), item(i_4, b_3))

                return map_1(_arrow1417, range_big_int(0, 1, length(a_3) - 1))

            return fold(folder_3, True, to_list(delay(_arrow1418))) if (length(a_3) == length(b_3)) else False

        def _arrow1422(__unit: None=None) -> bool:
            a_4: IEnumerable_1[ArcStudy] = this.Studies
            b_4: IEnumerable_1[ArcStudy] = other.Studies
            def folder_4(acc_4: bool, e_4: bool) -> bool:
                if acc_4:
                    return e_4

                else: 
                    return False


            def _arrow1421(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1420(i_5: int) -> bool:
                    return equals(item(i_5, a_4), item(i_5, b_4))

                return map_1(_arrow1420, range_big_int(0, 1, length(a_4) - 1))

            return fold(folder_4, True, to_list(delay(_arrow1421))) if (length(a_4) == length(b_4)) else False

        def _arrow1425(__unit: None=None) -> bool:
            a_5: IEnumerable_1[ArcWorkflow] = this.Workflows
            b_5: IEnumerable_1[ArcWorkflow] = other.Workflows
            def folder_5(acc_5: bool, e_5: bool) -> bool:
                if acc_5:
                    return e_5

                else: 
                    return False


            def _arrow1424(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1423(i_6: int) -> bool:
                    return equals(item(i_6, a_5), item(i_6, b_5))

                return map_1(_arrow1423, range_big_int(0, 1, length(a_5) - 1))

            return fold(folder_5, True, to_list(delay(_arrow1424))) if (length(a_5) == length(b_5)) else False

        def _arrow1428(__unit: None=None) -> bool:
            a_6: IEnumerable_1[ArcRun] = this.Runs
            b_6: IEnumerable_1[ArcRun] = other.Runs
            def folder_6(acc_6: bool, e_6: bool) -> bool:
                if acc_6:
                    return e_6

                else: 
                    return False


            def _arrow1427(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1426(i_7: int) -> bool:
                    return equals(item(i_7, a_6), item(i_7, b_6))

                return map_1(_arrow1426, range_big_int(0, 1, length(a_6) - 1))

            return fold(folder_6, True, to_list(delay(_arrow1427))) if (length(a_6) == length(b_6)) else False

        def _arrow1431(__unit: None=None) -> bool:
            a_7: IEnumerable_1[str] = this.RegisteredStudyIdentifiers
            b_7: IEnumerable_1[str] = other.RegisteredStudyIdentifiers
            def folder_7(acc_7: bool, e_7: bool) -> bool:
                if acc_7:
                    return e_7

                else: 
                    return False


            def _arrow1430(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1429(i_8: int) -> bool:
                    return item(i_8, a_7) == item(i_8, b_7)

                return map_1(_arrow1429, range_big_int(0, 1, length(a_7) - 1))

            return fold(folder_7, True, to_list(delay(_arrow1430))) if (length(a_7) == length(b_7)) else False

        def _arrow1434(__unit: None=None) -> bool:
            a_8: IEnumerable_1[Comment] = this.Comments
            b_8: IEnumerable_1[Comment] = other.Comments
            def folder_8(acc_8: bool, e_8: bool) -> bool:
                if acc_8:
                    return e_8

                else: 
                    return False


            def _arrow1433(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1432(i_9: int) -> bool:
                    return equals(item(i_9, a_8), item(i_9, b_8))

                return map_1(_arrow1432, range_big_int(0, 1, length(a_8) - 1))

            return fold(folder_8, True, to_list(delay(_arrow1433))) if (length(a_8) == length(b_8)) else False

        def _arrow1437(__unit: None=None) -> bool:
            a_9: IEnumerable_1[Remark] = this.Remarks
            b_9: IEnumerable_1[Remark] = other.Remarks
            def folder_9(acc_9: bool, e_9: bool) -> bool:
                if acc_9:
                    return e_9

                else: 
                    return False


            def _arrow1436(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1435(i_10: int) -> bool:
                    return equals(item(i_10, a_9), item(i_10, b_9))

                return map_1(_arrow1435, range_big_int(0, 1, length(a_9) - 1))

            return fold(folder_9, True, to_list(delay(_arrow1436))) if (length(a_9) == length(b_9)) else False

        return for_all(predicate, to_enumerable([this.Identifier == other.Identifier, equals(this.Title, other.Title), equals(this.Description, other.Description), equals(this.SubmissionDate, other.SubmissionDate), equals(this.PublicReleaseDate, other.PublicReleaseDate), _arrow1410(), _arrow1413(), _arrow1416(), _arrow1419(), _arrow1422(), _arrow1425(), _arrow1428(), _arrow1431(), _arrow1434(), _arrow1437()]))

    def ReferenceEquals(self, other: ArcInvestigation) -> bool:
        this: ArcInvestigation = self
        return this is other

    def __str__(self, __unit: None=None) -> str:
        this: ArcInvestigation = self
        arg: str = this.Identifier
        arg_1: str | None = this.Title
        arg_2: str | None = this.Description
        arg_3: str | None = this.SubmissionDate
        arg_4: str | None = this.PublicReleaseDate
        arg_5: Array[OntologySourceReference] = this.OntologySourceReferences
        arg_6: Array[Publication] = this.Publications
        arg_7: Array[Person] = this.Contacts
        arg_8: Array[ArcAssay] = this.Assays
        arg_9: Array[ArcStudy] = this.Studies
        arg_10: Array[ArcWorkflow] = this.Workflows
        arg_11: Array[ArcRun] = this.Runs
        arg_12: Array[str] = this.RegisteredStudyIdentifiers
        arg_13: Array[Comment] = this.Comments
        arg_14: Array[Remark] = this.Remarks
        return to_text(printf("ArcInvestigation {\r\n    Identifier = %A,\r\n    Title = %A,\r\n    Description = %A,\r\n    SubmissionDate = %A,\r\n    PublicReleaseDate = %A,\r\n    OntologySourceReferences = %A,\r\n    Publications = %A,\r\n    Contacts = %A,\r\n    Assays = %A,\r\n    Studies = %A,\r\n    Workflows = %A,\r\n    Runs = %A,\r\n    RegisteredStudyIdentifiers = %A,\r\n    Comments = %A,\r\n    Remarks = %A,\r\n}"))(arg)(arg_1)(arg_2)(arg_3)(arg_4)(arg_5)(arg_6)(arg_7)(arg_8)(arg_9)(arg_10)(arg_11)(arg_12)(arg_13)(arg_14)

    def __eq__(self, other: Any=None) -> bool:
        this: ArcInvestigation = self
        return this.StructurallyEquals(other) if isinstance(other, ArcInvestigation) else False

    def __hash__(self, __unit: None=None) -> Any:
        this: ArcInvestigation = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.SubmissionDate), box_hash_option(this.PublicReleaseDate), box_hash_seq(this.Publications), box_hash_seq(this.Contacts), box_hash_seq(this.OntologySourceReferences), box_hash_seq(this.Assays), box_hash_seq(this.Studies), box_hash_seq(this.Workflows), box_hash_seq(this.Runs), box_hash_seq(this.RegisteredStudyIdentifiers), box_hash_seq(this.Comments), box_hash_seq(this.Remarks)])

    def GetLightHashCode(self, __unit: None=None) -> Any:
        this: ArcInvestigation = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.SubmissionDate), box_hash_option(this.PublicReleaseDate), box_hash_seq(this.Publications), box_hash_seq(this.Contacts), box_hash_seq(this.OntologySourceReferences), box_hash_seq(this.RegisteredStudyIdentifiers), box_hash_seq(this.Comments), box_hash_seq(this.Remarks)])


ArcInvestigation_reflection = _expr1438

def ArcInvestigation__ctor_Z67823F6C(identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, ontology_source_references: Array[OntologySourceReference] | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, assays: Array[ArcAssay] | None=None, studies: Array[ArcStudy] | None=None, workflows: Array[ArcWorkflow] | None=None, runs: Array[ArcRun] | None=None, registered_study_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None, remarks: Array[Remark] | None=None) -> ArcInvestigation:
    return ArcInvestigation(identifier, title, description, submission_date, public_release_date, ontology_source_references, publications, contacts, assays, studies, workflows, runs, registered_study_identifiers, comments, remarks)


def ArcTypesAux_ErrorMsgs_unableToFindAssayIdentifier(assay_identifier: Any, investigation_identifier: Any) -> str:
    return ((("Error. Unable to find assay with identifier \'" + str(assay_identifier)) + "\' in investigation ") + str(investigation_identifier)) + "."


def ArcTypesAux_ErrorMsgs_unableToFindStudyIdentifier(study_identifer: Any, investigation_identifier: Any) -> str:
    return ((("Error. Unable to find study with identifier \'" + str(study_identifer)) + "\' in investigation ") + str(investigation_identifier)) + "."


def ArcTypesAux_ErrorMsgs_unableToFindWorkflowIdentifier(workflow_identifier: Any, investigation_identifier: Any) -> str:
    return ((("Error. Unable to find workflow with identifier \'" + str(workflow_identifier)) + "\' in investigation ") + str(investigation_identifier)) + "."


def ArcTypesAux_ErrorMsgs_unableToFindRunIdentifier(run_identifier: Any, investigation_identifier: Any) -> str:
    return ((("Error. Unable to find run with identifier \'" + str(run_identifier)) + "\' in investigation ") + str(investigation_identifier)) + "."


__all__ = ["ArcAssay_reflection", "ArcStudy_reflection", "ArcWorkflow_reflection", "ArcRun_reflection", "ArcInvestigation_reflection", "ArcTypesAux_ErrorMsgs_unableToFindAssayIdentifier", "ArcTypesAux_ErrorMsgs_unableToFindStudyIdentifier", "ArcTypesAux_ErrorMsgs_unableToFindWorkflowIdentifier", "ArcTypesAux_ErrorMsgs_unableToFindRunIdentifier"]

