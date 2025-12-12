from __future__ import annotations
from abc import abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
import requests
from typing import (Any, Protocol)
from ..fable_modules.fable_library.async_builder import (singleton as singleton_1, Async)
from ..fable_modules.fable_library.map import of_list
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.reflection import (TypeInfo, int32_type, string_type, class_type, record_type)
from ..fable_modules.fable_library.seq import (to_list, delay, map as map_1, collect, singleton)
from ..fable_modules.fable_library.types import Record
from ..fable_modules.fable_library.util import (create_obj, IEnumerable_1, compare_primitives)

class InteropResponseType(Protocol):
    @property
    @abstractmethod
    def encoding(self) -> str:
        ...

    @property
    @abstractmethod
    def headers(self) -> Any:
        ...

    @property
    @abstractmethod
    def status_code(self) -> int:
        ...

    @property
    @abstractmethod
    def text(self) -> str:
        ...


def _expr4026() -> TypeInfo:
    return record_type("ARCtrl.WebRequestHelpers.Py.Response", [], Response, lambda: [("status_code", int32_type), ("text", string_type), ("headers", class_type("Microsoft.FSharp.Collections.FSharpMap`2", [string_type, string_type])), ("encoding", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class Response(Record):
    status_code: int
    text: str
    headers: Any
    encoding: str

Response_reflection = _expr4026

def _expr4027() -> TypeInfo:
    return class_type("ARCtrl.WebRequestHelpers.Py.Requests", None, Requests)


class Requests:
    def __init__(self, __unit: None=None) -> None:
        pass


Requests_reflection = _expr4027

def Requests__ctor(__unit: None=None) -> Requests:
    return Requests(__unit)


def Requests_createHeadersDict_9F3777D(headers: Any | None=None) -> Any | None:
    def mapping(values: Any, headers: Any=headers) -> Any:
        def _arrow4029(__unit: None=None, values: Any=values) -> IEnumerable_1[tuple[str, Any]]:
            def _arrow4028(pair: Any) -> tuple[str, Any]:
                return (pair[0], pair[1])

            return map_1(_arrow4028, values)

        return create_obj(to_list(delay(_arrow4029)))

    return map(mapping, headers)


def Requests_mapResponseType_Z730CA7D4(response: InteropResponseType) -> Response:
    status_code: int = response.status_code or 0
    text: str = response.text
    encoding: str = response.text
    def _arrow4031(__unit: None=None, response: Any=response) -> IEnumerable_1[tuple[str, str]]:
        def _arrow4030(header_name: str) -> IEnumerable_1[tuple[str, str]]:
            return singleton((header_name, response.headers[header_name]))

        return collect(_arrow4030, list(response.headers.keys()))

    class ObjectExpr4032:
        @property
        def Compare(self) -> Callable[[str, str], int]:
            return compare_primitives

    return Response(status_code, text, of_list(to_list(delay(_arrow4031)), ObjectExpr4032()), encoding)


def Requests_get_43A074E6(url: str, headers: Any | None=None) -> Response:
    headers_dict: Any | None = Requests_createHeadersDict_9F3777D(headers)
    return Requests_mapResponseType_Z730CA7D4(requests.get(url, headers=headers_dict))


def Requests_post_147AE53E(url: str, data: str | None=None, headers: Any | None=None) -> Response:
    headers_dict: Any | None = Requests_createHeadersDict_9F3777D(headers)
    return Requests_mapResponseType_Z730CA7D4(requests.post(url, data=data, headers=headers_dict))


def Requests_put_147AE53E(url: str, data: str | None=None, headers: Any | None=None) -> Response:
    headers_dict: Any | None = Requests_createHeadersDict_9F3777D(headers)
    return Requests_mapResponseType_Z730CA7D4(requests.put(url, data=data, headers=headers_dict))


def Requests_delete_147AE53E(url: str, data: str | None=None, headers: Any | None=None) -> Response:
    headers_dict: Any | None = Requests_createHeadersDict_9F3777D(headers)
    return Requests_mapResponseType_Z730CA7D4(requests.delete(url, data=data, headers=headers_dict))


def Requests_head_147AE53E(url: str, data: str | None=None, headers: Any | None=None) -> Response:
    headers_dict: Any | None = Requests_createHeadersDict_9F3777D(headers)
    return Requests_mapResponseType_Z730CA7D4(requests.head(url, data=data, headers=headers_dict))


def Requests_options_147AE53E(url: str, data: str | None=None, headers: Any | None=None) -> Response:
    headers_dict: Any | None = Requests_createHeadersDict_9F3777D(headers)
    return Requests_mapResponseType_Z730CA7D4(requests.head(url, data=data, headers=headers_dict))


def download_file(url: str) -> Async[str]:
    def _arrow4033(__unit: None=None, url: Any=url) -> Async[str]:
        response: Response = Requests_get_43A074E6(url)
        return singleton_1.Return(response.text)

    return singleton_1.Delay(_arrow4033)


__all__ = ["Response_reflection", "Requests_reflection", "Requests_createHeadersDict_9F3777D", "Requests_mapResponseType_Z730CA7D4", "Requests_get_43A074E6", "Requests_post_147AE53E", "Requests_put_147AE53E", "Requests_delete_147AE53E", "Requests_head_147AE53E", "Requests_options_147AE53E", "download_file"]

