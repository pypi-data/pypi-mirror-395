from ..fable_modules.fable_library.async_builder import Async
from .web_request_py import download_file as download_file_1

def download_file(url: str) -> Async[str]:
    return download_file_1(url)


__all__ = ["download_file"]

