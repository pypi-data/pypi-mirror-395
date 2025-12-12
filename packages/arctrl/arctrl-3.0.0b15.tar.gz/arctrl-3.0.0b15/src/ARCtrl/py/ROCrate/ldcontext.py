from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.map_util import (add_to_dict, get_item_from_dict, try_get_value)
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.reg_exp import (get_item, groups)
from ..fable_modules.fable_library.seq import (reduce, map, sort, try_pick)
from ..fable_modules.fable_library.string_ import (starts_with_exact, to_fail, printf, replace)
from ..fable_modules.fable_library.types import (to_string, Array)
from ..fable_modules.fable_library.uri import Uri
from ..fable_modules.fable_library.util import (IEnumerable_1, get_enumerator, dispose, safe_hash, compare_primitives, string_hash)
from ..fable_modules.fable_library.types import FSharpRef
from ..Core.Helper.collections_ import StringDictionary_ofSeq
from ..Core.Helper.hash_codes import (box_hash_seq, merge_hashes, hash_1 as hash_1_1)
from ..Core.Helper.regex import ActivePatterns__007CRegex_007C__007C

IRIHelper_compactIRIRegex: str = "(?<prefix>.*):(?<suffix>[^\\/][^\\/].*)"

def IRIHelper__007CCompactIri_007C__007C(term_defition: str) -> tuple[str, str] | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C(IRIHelper_compactIRIRegex, term_defition)
    if active_pattern_result is not None:
        result: Any = active_pattern_result
        return (get_item(groups(result), "prefix") or "", get_item(groups(result), "suffix") or "")

    else: 
        return None



def IRIHelper_combine(base_iri: str, relative: str) -> str:
    if True if starts_with_exact(relative, "http://") else starts_with_exact(relative, "https://"):
        return relative

    else: 
        return to_string(Uri.create(Uri.create(base_iri), relative))



def IRIHelper_combineOptional(base_iri: str | None=None, relative: str | None=None) -> str | None:
    if base_iri is None:
        if relative is not None:
            r_1: str = relative
            return r_1

        else: 
            return None


    elif relative is None:
        b_1: str = base_iri
        return b_1

    else: 
        b: str = base_iri
        r: str = relative
        return IRIHelper_combine(b, r)



def _expr1653() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDContext", None, LDContext)


class LDContext:
    def __init__(self, mappings: Any | None=None, base_contexts: Array[LDContext] | None=None) -> None:
        self.base_contexts_004041: Array[LDContext] = default_arg(base_contexts, [])
        self.name: str | None = None
        self.mappings_004045: Any = dict([]) if (mappings is None) else mappings
        self.reverse_mappings: Any = dict([])
        self.compact_reverse_mappings: Any = dict([])
        enumerator: Any = get_enumerator(self.mappings_004045)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                kvp: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                self.add_reverse_mapping(kvp[0], kvp[1])

        finally: 
            dispose(enumerator)


    @property
    def Mappings(self, __unit: None=None) -> Any:
        this: LDContext = self
        return this.mappings_004045

    @property
    def BaseContexts(self, __unit: None=None) -> Array[LDContext]:
        this: LDContext = self
        return this.base_contexts_004041

    @BaseContexts.setter
    def BaseContexts(self, value: Array[LDContext]) -> None:
        this: LDContext = self
        this.base_contexts_004041 = value

    @property
    def Name(self, __unit: None=None) -> str | None:
        this: LDContext = self
        return this.name

    @Name.setter
    def Name(self, value: str | None=None) -> None:
        this: LDContext = self
        this.name = value

    def AddMapping(self, term: str, definition: str) -> None:
        this: LDContext = self
        try: 
            key: str = term
            value: str = definition
            dict_1: Any = this.mappings_004045
            if key in dict_1:
                dict_1[key] = value

            else: 
                add_to_dict(dict_1, key, value)

            this.add_reverse_mapping(term, definition)

        except Exception as ex:
            arg_2: str = str(ex)
            to_fail(printf("Failed to add mapping to context: %s -> %s: %s"))(term)(definition)(arg_2)


    def TryResolveTerm(self, term: str) -> str | None:
        this: LDContext = self
        def mapping(term_1: str) -> str | None:
            return this.try_find_term(term_1)

        return reduce(IRIHelper_combineOptional, map(mapping, term.split(":"))) if (term.find(":") >= 0) else this.try_find_term(term)

    def TryGetTerm(self, iri: str) -> str | None:
        this: LDContext = self
        return this.try_find_iri(iri)

    def PropertyNamesMatch(self, p1: str, p2: str) -> bool:
        this: LDContext = self
        if p1 == p2:
            return True

        else: 
            p1def: str | None = this.TryResolveTerm(p1)
            p2def: str | None = this.TryResolveTerm(p2)
            def _arrow1636(__unit: None=None) -> bool:
                p2def_2: str = p2def
                return p1 == p2def_2

            def _arrow1637(__unit: None=None) -> bool:
                p1def_2: str = p1def
                return p1def_2 == p2

            def _arrow1638(__unit: None=None) -> bool:
                p1def_1: str = p1def
                p2def_1: str = p2def
                return p1def_1 == p2def_1

            return (_arrow1636() if (p2def is not None) else False) if (p1def is None) else (_arrow1637() if (p2def is None) else _arrow1638())


    @staticmethod
    def from_mapping_seq(mappings: IEnumerable_1[tuple[str, str]]) -> LDContext:
        return LDContext(StringDictionary_ofSeq(mappings))

    @staticmethod
    def combine_in_place(base_context: LDContext, specific_context: LDContext) -> LDContext:
        (specific_context.BaseContexts.append(base_context))
        return specific_context

    @staticmethod
    def combine(base_context: LDContext, specific_context: LDContext) -> LDContext:
        return LDContext(None, [specific_context, base_context])

    @staticmethod
    def try_combine_optional(base_context: LDContext | None=None, specific_context: LDContext | None=None) -> LDContext | None:
        def _arrow1639(__unit: None=None) -> LDContext | None:
            s_1: LDContext = specific_context
            return s_1

        def _arrow1640(__unit: None=None) -> LDContext | None:
            f_1: LDContext = base_context
            return f_1

        def _arrow1641(__unit: None=None) -> LDContext | None:
            f: LDContext = base_context
            s: LDContext = specific_context
            return LDContext.combine(f, s)

        return (_arrow1639() if (specific_context is not None) else None) if (base_context is None) else (_arrow1640() if (specific_context is None) else _arrow1641())

    def ShallowCopy(self, __unit: None=None) -> LDContext:
        this: LDContext = self
        new_mappings: Any = dict([])
        enumerator: Any = get_enumerator(this.mappings_004045)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                kvp: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                add_to_dict(new_mappings, kvp[0], kvp[1])

        finally: 
            dispose(enumerator)

        return LDContext(new_mappings, this.base_contexts_004041)

    def DeepCopy(self, __unit: None=None) -> LDContext:
        this: LDContext = self
        new_mappings: Any = dict([])
        enumerator: Any = get_enumerator(this.mappings_004045)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                kvp: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                add_to_dict(new_mappings, kvp[0], kvp[1])

        finally: 
            dispose(enumerator)

        new_base_contexts: Array[LDContext] = []
        enumerator_1: Any = get_enumerator(this.base_contexts_004041)
        try: 
            while enumerator_1.System_Collections_IEnumerator_MoveNext():
                ctx: LDContext = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                (new_base_contexts.append(ctx.DeepCopy()))

        finally: 
            dispose(enumerator_1)

        return LDContext(new_mappings, new_base_contexts)

    def StructurallyEquals(self, other: LDContext) -> bool:
        this: LDContext = self
        return safe_hash(this) == safe_hash(other)

    def ReferenceEquals(self, other: LDContext) -> bool:
        this: LDContext = self
        return this is other

    def __eq__(self, other: Any=None) -> bool:
        this: LDContext = self
        return this.StructurallyEquals(other) if isinstance(other, LDContext) else False

    def __hash__(self, __unit: None=None) -> int:
        this: LDContext = self
        def mapping(k: str) -> int:
            return merge_hashes(hash_1_1(k), hash_1_1(get_item_from_dict(this.Mappings, k)))

        class ObjectExpr1642:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        mappings_hash: int = box_hash_seq(map(mapping, sort(this.Mappings.keys(), ObjectExpr1642())))
        name_hash: int
        match_value: str | None = this.Name
        name_hash = 0 if (match_value is None) else string_hash(match_value)
        base_contexts_hash: int = (0 if (len(this.base_contexts_004041) == 0) else reduce(merge_hashes, map(safe_hash, this.base_contexts_004041))) or 0
        return merge_hashes(merge_hashes(mappings_hash, name_hash), base_contexts_hash)

    def System_ICloneable_Clone(self, __unit: None=None) -> Any:
        this: LDContext = self
        return this.DeepCopy()

    def add_reverse_mapping(self, key: str, value: str) -> None:
        this: LDContext = self
        http: str = replace(value, "https://", "http://")
        https: str = replace(value, "http://", "https://")
        key_1: str = http
        value_1: str = key
        dict_1: Any = this.reverse_mappings
        if key_1 in dict_1:
            dict_1[key_1] = value_1

        else: 
            add_to_dict(dict_1, key_1, value_1)

        key_2: str = https
        value_2: str = key
        dict_1_1: Any = this.reverse_mappings
        if key_2 in dict_1_1:
            dict_1_1[key_2] = value_2

        else: 
            add_to_dict(dict_1_1, key_2, value_2)

        active_pattern_result: tuple[str, str] | None = IRIHelper__007CCompactIri_007C__007C(value)
        if active_pattern_result is not None:
            prefix: str = active_pattern_result[0]
            suffix: str = active_pattern_result[1]
            key_3: str = prefix
            value_3: tuple[str, str] = (suffix, key)
            dict_1_2: Any = this.compact_reverse_mappings
            if key_3 in dict_1_2:
                dict_1_2[key_3] = value_3

            else: 
                add_to_dict(dict_1_2, key_3, value_3)

            match_value: str | None
            pattern_input: tuple[bool, str]
            out_arg: str = None
            def _arrow1643(__unit: None=None) -> str:
                return out_arg

            def _arrow1644(v: str) -> None:
                nonlocal out_arg
                out_arg = v

            pattern_input = (try_get_value(this.mappings_004045, prefix, FSharpRef(_arrow1643, _arrow1644)), out_arg)
            match_value = pattern_input[1] if pattern_input[0] else None
            if match_value is None:
                pass

            else: 
                iri: str = IRIHelper_combine(match_value, suffix)
                this.add_reverse_mapping(key, iri)


        else: 
            match_value_1: tuple[str, str] | None
            pattern_input_1: tuple[bool, tuple[str, str]]
            out_arg_1: tuple[str, str] = None
            def _arrow1645(__unit: None=None) -> tuple[str, str]:
                return out_arg_1

            def _arrow1646(v_2: tuple[str, str]) -> None:
                nonlocal out_arg_1
                out_arg_1 = v_2

            pattern_input_1 = (try_get_value(this.compact_reverse_mappings, key, FSharpRef(_arrow1645, _arrow1646)), out_arg_1)
            match_value_1 = pattern_input_1[1] if pattern_input_1[0] else None
            if match_value_1 is None:
                pass

            else: 
                term: str = match_value_1[1]
                iri_1: str = IRIHelper_combine(value, match_value_1[0])
                this.add_reverse_mapping(term, iri_1)



    def try_find_term(self, term: str) -> str | None:
        this: LDContext = self
        definition: str | None
        match_value: str | None
        pattern_input: tuple[bool, str]
        out_arg: str = None
        def _arrow1647(__unit: None=None) -> str:
            return out_arg

        def _arrow1648(v: str) -> None:
            nonlocal out_arg
            out_arg = v

        pattern_input = (try_get_value(this.mappings_004045, term, FSharpRef(_arrow1647, _arrow1648)), out_arg)
        match_value = pattern_input[1] if pattern_input[0] else None
        def chooser(ctx: LDContext) -> str | None:
            return ctx.TryResolveTerm(term)

        definition = try_pick(chooser, this.base_contexts_004041) if (match_value is None) else match_value
        if definition is None:
            return None

        else: 
            active_pattern_result: tuple[str, str] | None = IRIHelper__007CCompactIri_007C__007C(definition)
            def _arrow1649(__unit: None=None) -> str | None:
                prefix: str = active_pattern_result[0]
                suffix: str = active_pattern_result[1]
                return IRIHelper_combine(prefix if (prefix == term) else default_arg(this.try_find_term(prefix), prefix), suffix if (suffix == term) else default_arg(this.try_find_term(suffix), suffix))

            def _arrow1650(__unit: None=None) -> str | None:
                d: str = definition
                return d

            return _arrow1649() if (active_pattern_result is not None) else _arrow1650()


    def try_find_iri(self, iri: str) -> str | None:
        this: LDContext = self
        match_value: str | None
        pattern_input: tuple[bool, str]
        out_arg: str = None
        def _arrow1651(__unit: None=None) -> str:
            return out_arg

        def _arrow1652(v: str) -> None:
            nonlocal out_arg
            out_arg = v

        pattern_input = (try_get_value(this.reverse_mappings, iri, FSharpRef(_arrow1651, _arrow1652)), out_arg)
        match_value = pattern_input[1] if pattern_input[0] else None
        def chooser(ctx: LDContext) -> str | None:
            return ctx.TryGetTerm(iri)

        return try_pick(chooser, this.base_contexts_004041) if (match_value is None) else match_value

    def try_compact_iri(self, iri: str) -> Any:
        raise Exception("TryCompactIRI is Not implemented yet")


LDContext_reflection = _expr1653

def LDContext__ctor_7878CD77(mappings: Any | None=None, base_contexts: Array[LDContext] | None=None) -> LDContext:
    return LDContext(mappings, base_contexts)


__all__ = ["IRIHelper_compactIRIRegex", "IRIHelper__007CCompactIri_007C__007C", "IRIHelper_combine", "IRIHelper_combineOptional", "LDContext_reflection"]

