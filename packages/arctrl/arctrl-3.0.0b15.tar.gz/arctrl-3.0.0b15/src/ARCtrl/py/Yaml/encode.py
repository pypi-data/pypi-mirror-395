from ..fable_modules.fable_library.option import default_arg

DefaultWhitespace: int = 2

def default_whitespace(spaces: int | None=None) -> int:
    return default_arg(spaces, DefaultWhitespace)


__all__ = ["DefaultWhitespace", "default_whitespace"]

