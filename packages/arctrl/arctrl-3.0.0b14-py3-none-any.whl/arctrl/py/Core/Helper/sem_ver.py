from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from ...fable_modules.fable_library.int32 import parse
from ...fable_modules.fable_library.option import value as value_3
from ...fable_modules.fable_library.reflection import (TypeInfo, int32_type, string_type, option_type, record_type)
from ...fable_modules.fable_library.reg_exp import (groups, get_item)
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.fable_library.system_text import (StringBuilder__ctor, StringBuilder__Append_Z721C83C5)
from ...fable_modules.fable_library.types import (Record, to_string)
from ...fable_modules.fable_library.util import ignore
from .regex import ActivePatterns__007CRegex_007C__007C

SemVerAux_Pattern: str = "^(?<major>\\d+)(\\.(?<minor>\\d+))?(\\.(?<patch>\\d+))?(-(?<pre>[0-9A-Za-z-\\.]+))?(\\+(?<build>[0-9A-Za-z-\\.]+))?$"

def _expr696() -> TypeInfo:
    return record_type("ARCtrl.Helper.SemVer.SemVer", [], SemVer, lambda: [("Major", int32_type), ("Minor", int32_type), ("Patch", int32_type), ("PreRelease", option_type(string_type)), ("Metadata", option_type(string_type))])


@dataclass(eq = False, repr = False, slots = True)
class SemVer(Record):
    Major: int
    Minor: int
    Patch: int
    PreRelease: str | None
    Metadata: str | None

SemVer_reflection = _expr696

def SemVer_make(major: int, minor: int, patch: int, pre: str | None=None, meta: str | None=None) -> SemVer:
    return SemVer(major, minor, patch, pre, meta)


def SemVer_create_Z55658624(major: int, minor: int, patch: int, pre: str | None=None, meta: str | None=None) -> SemVer:
    return SemVer(major, minor, patch, pre, meta)


def SemVer_tryOfString_Z721C83C5(str_1: str) -> SemVer | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C(SemVerAux_Pattern, str_1)
    if active_pattern_result is not None:
        m: Any = active_pattern_result
        g: Any = groups(m)
        return SemVer_create_Z55658624(parse(get_item(g, "major") or "", 511, False, 32), parse(get_item(g, "minor") or "", 511, False, 32), parse(get_item(g, "patch") or "", 511, False, 32), (get_item(g, "pre") or "") if (get_item(g, "pre") is not None) else None, (get_item(g, "build") or "") if (get_item(g, "build") is not None) else None)

    else: 
        return None



def SemVer__AsString(this: SemVer) -> str:
    sb: Any = StringBuilder__ctor()
    ignore(StringBuilder__Append_Z721C83C5(sb, to_text(printf("%i.%i.%i"))(this.Major)(this.Minor)(this.Patch)))
    if this.PreRelease is not None:
        def _arrow697(__unit: None=None, this: Any=this) -> str:
            arg_3: str = value_3(this.PreRelease)
            return to_text(printf("-%s"))(arg_3)

        ignore(StringBuilder__Append_Z721C83C5(sb, _arrow697()))

    if this.Metadata is not None:
        def _arrow698(__unit: None=None, this: Any=this) -> str:
            arg_4: str = value_3(this.Metadata)
            return to_text(printf("+%s"))(arg_4)

        ignore(StringBuilder__Append_Z721C83C5(sb, _arrow698()))

    return to_string(sb)


__all__ = ["SemVerAux_Pattern", "SemVer_reflection", "SemVer_make", "SemVer_create_Z55658624", "SemVer_tryOfString_Z721C83C5", "SemVer__AsString"]

