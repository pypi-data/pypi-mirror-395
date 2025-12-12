from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Contract.contract import (Contract, DTOType, DTO as DTO_2)
from ..FileSystem.path import combine
from ..cross_async import (catch_with, start_sequential)
from ..fable_modules.fable_library.array_ import (fold, append)
from ..fable_modules.fable_library.async_builder import (singleton, Async)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import curry2
from ..fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from .file_system_helper import (read_file_xlsx_async, read_file_text_async, ensure_directory_of_file_async, write_file_text_async, write_file_xlsx_async, rename_file_or_directory_async, delete_file_or_directory_async)

def fulfill_read_contract_async(base_path: str, c: Contract) -> Async[FSharpResult_2[Contract, str]]:
    def f(e_1: Exception, base_path: Any=base_path, c: Any=c) -> FSharpResult_2[Contract, str]:
        def _arrow4038(__unit: None=None, e_1: Any=e_1) -> str:
            arg_4: str = str(e_1)
            return to_text(printf("Error reading contract %s: %s"))(c.Path)(arg_4)

        return FSharpResult_2(1, _arrow4038())

    def _arrow4044(__unit: None=None, base_path: Any=base_path, c: Any=c) -> Async[FSharpResult_2[Contract, str]]:
        def _arrow4041(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
            match_value: DTOType | None = c.DTOType
            (pattern_matching_result,) = (None,)
            if match_value is not None:
                if match_value.tag == 0:
                    pattern_matching_result = 0

                elif match_value.tag == 4:
                    pattern_matching_result = 0

                elif match_value.tag == 1:
                    pattern_matching_result = 0

                elif match_value.tag == 2:
                    pattern_matching_result = 0

                elif match_value.tag == 3:
                    pattern_matching_result = 0

                elif match_value.tag == 5:
                    pattern_matching_result = 0

                elif match_value.tag == 10:
                    pattern_matching_result = 1

                elif match_value.tag == 8:
                    pattern_matching_result = 1

                elif match_value.tag == 9:
                    pattern_matching_result = 1

                else: 
                    pattern_matching_result = 2


            else: 
                pattern_matching_result = 2

            if pattern_matching_result == 0:
                path: str = combine(base_path, c.Path)
                def _arrow4039(_arg: FsWorkbook) -> Async[FSharpResult_2[Contract, str]]:
                    return singleton.Return(FSharpResult_2(0, Contract(c.Operation, c.Path, c.DTOType, DTO_2(0, _arg))))

                return singleton.Bind(read_file_xlsx_async(path), _arrow4039)

            elif pattern_matching_result == 1:
                path_1: str = combine(base_path, c.Path)
                def _arrow4040(_arg_1: str) -> Async[FSharpResult_2[Contract, str]]:
                    return singleton.Return(FSharpResult_2(0, Contract(c.Operation, c.Path, c.DTOType, DTO_2(1, _arg_1))))

                return singleton.Bind(read_file_text_async(path_1), _arrow4040)

            elif pattern_matching_result == 2:
                return singleton.Return(FSharpResult_2(1, to_text(printf("Contract %s is neither an ISA nor a freetext contract"))(c.Path)))


        def _arrow4043(_arg_2: Exception) -> Async[FSharpResult_2[Contract, str]]:
            def _arrow4042(__unit: None=None) -> str:
                arg_2: str = str(_arg_2)
                return to_text(printf("Error reading contract %s: %s"))(c.Path)(arg_2)

            return singleton.Return(FSharpResult_2(1, _arrow4042()))

        return singleton.TryWith(singleton.Delay(_arrow4041), _arrow4043)

    return catch_with(f, singleton.Delay(_arrow4044))


def fullfill_contract_batch_async_by(contract_f: Callable[[str, Contract], Async[FSharpResult_2[Contract, str]]], base_path: str, cs: Array[Contract]) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
    def _arrow4046(__unit: None=None, contract_f: Any=contract_f, base_path: Any=base_path, cs: Any=cs) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
        def _arrow4045(_arg: Array[FSharpResult_2[Contract, str]]) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
            def folder(acc: FSharpResult_2[Array[Contract], Array[str]], cr: FSharpResult_2[Contract, str]) -> FSharpResult_2[Array[Contract], Array[str]]:
                copy_of_struct: FSharpResult_2[Array[Contract], Array[str]] = acc
                if copy_of_struct.tag == 1:
                    copy_of_struct_1: FSharpResult_2[Contract, str] = cr
                    if copy_of_struct_1.tag == 1:
                        return FSharpResult_2(1, append(copy_of_struct.fields[0], [copy_of_struct_1.fields[0]], None))

                    else: 
                        return FSharpResult_2(1, copy_of_struct.fields[0])


                else: 
                    copy_of_struct_2: FSharpResult_2[Contract, str] = cr
                    if copy_of_struct_2.tag == 1:
                        return FSharpResult_2(1, [copy_of_struct_2.fields[0]])

                    else: 
                        return FSharpResult_2(0, append(copy_of_struct.fields[0], [copy_of_struct_2.fields[0]], None))



            res: FSharpResult_2[Array[Contract], Array[str]] = fold(folder, FSharpResult_2(0, []), _arg)
            return singleton.Return(res)

        return singleton.Bind(start_sequential(curry2(contract_f)(base_path), cs), _arrow4045)

    return singleton.Delay(_arrow4046)


def fulfill_write_contract_async(base_path: str, c: Contract) -> Async[FSharpResult_2[Contract, str]]:
    def f(e_1: Exception, base_path: Any=base_path, c: Any=c) -> FSharpResult_2[Contract, str]:
        def _arrow4047(__unit: None=None, e_1: Any=e_1) -> str:
            arg_4: str = str(e_1)
            return to_text(printf("Error writing contract %s: %s"))(c.Path)(arg_4)

        return FSharpResult_2(1, _arrow4047())

    def _arrow4057(__unit: None=None, base_path: Any=base_path, c: Any=c) -> Async[FSharpResult_2[Contract, str]]:
        def _arrow4054(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
            match_value: DTO_2 | None = c.DTO
            if match_value is None:
                path_2: str = combine(base_path, c.Path)
                def _arrow4049(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    def _arrow4048(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                        return singleton.Return(FSharpResult_2(0, c))

                    return singleton.Bind(write_file_text_async(path_2, ""), _arrow4048)

                return singleton.Bind(ensure_directory_of_file_async(path_2), _arrow4049)

            elif match_value.tag == 1:
                t: str = match_value.fields[0]
                path: str = combine(base_path, c.Path)
                def _arrow4051(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    def _arrow4050(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                        return singleton.Return(FSharpResult_2(0, c))

                    return singleton.Bind(write_file_text_async(path, t), _arrow4050)

                return singleton.Bind(ensure_directory_of_file_async(path), _arrow4051)

            elif match_value.tag == 0:
                wb: Any = match_value.fields[0]
                path_1: str = combine(base_path, c.Path)
                def _arrow4053(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    def _arrow4052(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                        return singleton.Return(FSharpResult_2(0, c))

                    return singleton.Bind(write_file_xlsx_async(path_1, wb), _arrow4052)

                return singleton.Bind(ensure_directory_of_file_async(path_1), _arrow4053)

            else: 
                return singleton.Return(FSharpResult_2(1, to_text(printf("Contract %s is not an ISA contract"))(c.Path)))


        def _arrow4056(_arg_6: Exception) -> Async[FSharpResult_2[Contract, str]]:
            def _arrow4055(__unit: None=None) -> str:
                arg_2: str = str(_arg_6)
                return to_text(printf("Error writing contract %s: %s"))(c.Path)(arg_2)

            return singleton.Return(FSharpResult_2(1, _arrow4055()))

        return singleton.TryWith(singleton.Delay(_arrow4054), _arrow4056)

    return catch_with(f, singleton.Delay(_arrow4057))


def fulfill_update_contract_async(base_path: str, c: Contract) -> Async[FSharpResult_2[Contract, str]]:
    def f(e_1: Exception, base_path: Any=base_path, c: Any=c) -> FSharpResult_2[Contract, str]:
        def _arrow4058(__unit: None=None, e_1: Any=e_1) -> str:
            arg_4: str = str(e_1)
            return to_text(printf("Error updating contract %s: %s"))(c.Path)(arg_4)

        return FSharpResult_2(1, _arrow4058())

    def _arrow4068(__unit: None=None, base_path: Any=base_path, c: Any=c) -> Async[FSharpResult_2[Contract, str]]:
        def _arrow4065(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
            match_value: DTO_2 | None = c.DTO
            if match_value is None:
                path_2: str = combine(base_path, c.Path)
                def _arrow4060(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    def _arrow4059(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                        return singleton.Return(FSharpResult_2(0, c))

                    return singleton.Bind(write_file_text_async(path_2, ""), _arrow4059)

                return singleton.Bind(ensure_directory_of_file_async(path_2), _arrow4060)

            elif match_value.tag == 1:
                t: str = match_value.fields[0]
                path: str = combine(base_path, c.Path)
                def _arrow4062(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    def _arrow4061(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                        return singleton.Return(FSharpResult_2(0, c))

                    return singleton.Bind(write_file_text_async(path, t), _arrow4061)

                return singleton.Bind(ensure_directory_of_file_async(path), _arrow4062)

            elif match_value.tag == 0:
                wb: Any = match_value.fields[0]
                path_1: str = combine(base_path, c.Path)
                def _arrow4064(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    def _arrow4063(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                        return singleton.Return(FSharpResult_2(0, c))

                    return singleton.Bind(write_file_xlsx_async(path_1, wb), _arrow4063)

                return singleton.Bind(ensure_directory_of_file_async(path_1), _arrow4064)

            else: 
                return singleton.Return(FSharpResult_2(1, to_text(printf("Contract %s is not an ISA contract"))(c.Path)))


        def _arrow4067(_arg_6: Exception) -> Async[FSharpResult_2[Contract, str]]:
            def _arrow4066(__unit: None=None) -> str:
                arg_2: str = str(_arg_6)
                return to_text(printf("Error updating contract %s: %s"))(c.Path)(arg_2)

            return singleton.Return(FSharpResult_2(1, _arrow4066()))

        return singleton.TryWith(singleton.Delay(_arrow4065), _arrow4067)

    return catch_with(f, singleton.Delay(_arrow4068))


def fullfill_rename_contract_async(base_path: str, c: Contract) -> Async[FSharpResult_2[Contract, str]]:
    def f(e_1: Exception, base_path: Any=base_path, c: Any=c) -> FSharpResult_2[Contract, str]:
        def _arrow4069(__unit: None=None, e_1: Any=e_1) -> str:
            arg_5: str = str(e_1)
            return to_text(printf("Error renaming contract %s: %s"))(c.Path)(arg_5)

        return FSharpResult_2(1, _arrow4069())

    def _arrow4074(__unit: None=None, base_path: Any=base_path, c: Any=c) -> Async[FSharpResult_2[Contract, str]]:
        def _arrow4071(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
            match_value: DTO_2 | None = c.DTO
            (pattern_matching_result, t_2) = (None, None)
            if match_value is not None:
                if match_value.tag == 1:
                    if match_value.fields[0] == c.Path:
                        pattern_matching_result = 0

                    else: 
                        pattern_matching_result = 1
                        t_2 = match_value.fields[0]


                else: 
                    pattern_matching_result = 2


            else: 
                pattern_matching_result = 2

            if pattern_matching_result == 0:
                return singleton.Return(FSharpResult_2(1, to_text(printf("Rename Contract %s old and new Path are the same"))(c.Path)))

            elif pattern_matching_result == 1:
                new_path: str = combine(base_path, t_2)
                old_path: str = combine(base_path, c.Path)
                def _arrow4070(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                    return singleton.Return(FSharpResult_2(0, c))

                return singleton.Bind(rename_file_or_directory_async(old_path, new_path), _arrow4070)

            elif pattern_matching_result == 2:
                return singleton.Return(FSharpResult_2(1, to_text(printf("Rename Contract %s does not contain new Path"))(c.Path)))


        def _arrow4073(_arg_1: Exception) -> Async[FSharpResult_2[Contract, str]]:
            def _arrow4072(__unit: None=None) -> str:
                arg_3: str = str(_arg_1)
                return to_text(printf("Error renaming contract %s: %s"))(c.Path)(arg_3)

            return singleton.Return(FSharpResult_2(1, _arrow4072()))

        return singleton.TryWith(singleton.Delay(_arrow4071), _arrow4073)

    return catch_with(f, singleton.Delay(_arrow4074))


def fullfill_delete_contract_async(base_path: str, c: Contract) -> Async[FSharpResult_2[Contract, str]]:
    def f(e_1: Exception, base_path: Any=base_path, c: Any=c) -> FSharpResult_2[Contract, str]:
        def _arrow4075(__unit: None=None, e_1: Any=e_1) -> str:
            arg_3: str = str(e_1)
            return to_text(printf("Error deleting contract %s: %s"))(c.Path)(arg_3)

        return FSharpResult_2(1, _arrow4075())

    def _arrow4080(__unit: None=None, base_path: Any=base_path, c: Any=c) -> Async[FSharpResult_2[Contract, str]]:
        def _arrow4077(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
            path: str = combine(base_path, c.Path)
            def _arrow4076(__unit: None=None) -> Async[FSharpResult_2[Contract, str]]:
                return singleton.Return(FSharpResult_2(0, c))

            return singleton.Bind(delete_file_or_directory_async(path), _arrow4076)

        def _arrow4079(_arg_1: Exception) -> Async[FSharpResult_2[Contract, str]]:
            def _arrow4078(__unit: None=None) -> str:
                arg_1: str = str(_arg_1)
                return to_text(printf("Error deleting contract %s: %s"))(c.Path)(arg_1)

            return singleton.Return(FSharpResult_2(1, _arrow4078()))

        return singleton.TryWith(singleton.Delay(_arrow4077), _arrow4079)

    return catch_with(f, singleton.Delay(_arrow4080))


def full_fill_contract(base_path: str, c: Contract) -> Async[FSharpResult_2[Contract, str]]:
    def f(e: Exception, base_path: Any=base_path, c: Any=c) -> FSharpResult_2[Contract, str]:
        def _arrow4081(__unit: None=None, e: Any=e) -> str:
            arg_2: str = str(e)
            return to_text(printf("Error fulfilling contract %s: %s"))(c.Path)(arg_2)

        return FSharpResult_2(1, _arrow4081())

    def _arrow4082(__unit: None=None, base_path: Any=base_path, c: Any=c) -> Async[FSharpResult_2[Contract, str]]:
        match_value: str = c.Operation
        return singleton.ReturnFrom(fulfill_read_contract_async(base_path, c)) if (match_value == "READ") else (singleton.ReturnFrom(fulfill_write_contract_async(base_path, c)) if (match_value == "CREATE") else (singleton.ReturnFrom(fulfill_update_contract_async(base_path, c)) if (match_value == "UPDATE") else (singleton.ReturnFrom(fullfill_delete_contract_async(base_path, c)) if (match_value == "DELETE") else (singleton.ReturnFrom(fullfill_rename_contract_async(base_path, c)) if (match_value == "RENAME") else singleton.Return(FSharpResult_2(1, to_text(printf("Operation %A not supported"))(c.Operation)))))))

    return catch_with(f, singleton.Delay(_arrow4082))


def full_fill_contract_batch_async(base_path: str, cs: Array[Contract]) -> Async[FSharpResult_2[Array[Contract], Array[str]]]:
    def _arrow4083(base_path_1: str, c: Contract, base_path: Any=base_path, cs: Any=cs) -> Async[FSharpResult_2[Contract, str]]:
        return full_fill_contract(base_path_1, c)

    return fullfill_contract_batch_async_by(_arrow4083, base_path, cs)


__all__ = ["fulfill_read_contract_async", "fullfill_contract_batch_async_by", "fulfill_write_contract_async", "fulfill_update_contract_async", "fullfill_rename_contract_async", "fullfill_delete_contract_async", "full_fill_contract", "full_fill_contract_batch_async"]

