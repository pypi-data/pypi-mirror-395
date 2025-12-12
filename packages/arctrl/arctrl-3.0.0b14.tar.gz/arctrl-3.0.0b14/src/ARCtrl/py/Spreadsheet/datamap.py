from __future__ import annotations
from ..fable_modules.fable_library.seq import (try_pick, for_all)
from ..fable_modules.fable_library.string_ import (to_fail, printf)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from ..fable_modules.fs_spreadsheet.fs_worksheet import FsWorksheet
from ..Core.datamap import Datamap
from .DatamapTable.datamap_table import (try_from_fs_worksheet, to_fs_worksheet)

def from_fs_workbook(doc: FsWorkbook) -> Datamap:
    try: 
        worksheets: Array[FsWorksheet] = doc.GetWorksheets()
        datamap_table: Datamap | None = try_pick(try_from_fs_worksheet, worksheets)
        if datamap_table is None:
            def sheet_is_empty(sheet: FsWorksheet) -> bool:
                return sheet.CellCollection.Count == 0

            if for_all(sheet_is_empty, worksheets):
                return Datamap.init()

            else: 
                raise Exception("No DatamapTable was found in any of the sheets of the workbook")


        else: 
            return datamap_table


    except Exception as err:
        arg: str = str(err)
        return to_fail(printf("Could not parse datamap: \n%s"))(arg)



def to_fs_workbook(datamap: Datamap) -> FsWorkbook:
    doc: FsWorkbook = FsWorkbook()
    sheet: FsWorksheet = to_fs_worksheet(datamap)
    doc.AddWorksheet(sheet)
    return doc


__all__ = ["from_fs_workbook", "to_fs_workbook"]

