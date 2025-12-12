from ..fable_modules.fable_library.string_ import replace

def clean(id: str) -> str:
    return replace(id, " ", "_")


__all__ = ["clean"]

