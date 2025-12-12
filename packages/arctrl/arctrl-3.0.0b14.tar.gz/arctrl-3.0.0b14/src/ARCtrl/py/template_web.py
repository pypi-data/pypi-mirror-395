from __future__ import annotations
from typing import Any
from .Core.template import Template
from .JsonIO.Table.templates import Templates_fromJsonString
from .fable_modules.fable_library.async_builder import (singleton, Async)
from .fable_modules.fable_library.option import default_arg
from .fable_modules.fable_library.types import Array
from .WebRequest.web_request import download_file

def get_templates(url: str | None=None) -> Async[Array[Template]]:
    url_1: str = default_arg(url, "https://github.com/nfdi4plants/Swate-templates/releases/download/latest/templates_v2.0.0.json")
    def _arrow4035(__unit: None=None, url: Any=url) -> Async[Array[Template]]:
        def _arrow4034(_arg: str) -> Async[Array[Template]]:
            map_result: Array[Template] = Templates_fromJsonString(_arg)
            return singleton.Return(map_result)

        return singleton.Bind(download_file(url_1), _arrow4034)

    return singleton.Delay(_arrow4035)


__all__ = ["get_templates"]

