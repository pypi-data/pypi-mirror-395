from __future__ import annotations
from abc import abstractmethod
from collections.abc import Callable
from typing import (Any, Protocol, TypeVar)
from ..fable_modules.dynamic_obj.dynamic_obj import (DynamicObj, DynamicObj_reflection)
from ..fable_modules.dynamic_obj.hash_codes import merge_hashes
from ..fable_modules.dynamic_obj.property_helper import PropertyHelper
from ..fable_modules.fable_library.map_util import (get_item_from_dict, try_get_value, add_to_dict)
from ..fable_modules.fable_library.option import (default_arg, value as value_3, some, map)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.seq import (iterate, filter as filter_2, choose, exists, to_list, delay, enumerate_while, singleton as singleton_2, empty, try_find, map as map_1, enumerate_from_functions, append, collect)
from ..fable_modules.fable_library.seq2 import List_distinctBy
from ..fable_modules.fable_library.string_ import starts_with_exact
from ..fable_modules.fable_library.types import (Array, FSharpRef)
from ..fable_modules.fable_library.util import (is_iterable, IEnumerable, equals, identity_hash, string_hash, IEnumerable_1, get_enumerator, IEnumerator, curry2, ignore, structural_hash, is_array_like)
from ..Core.Helper.collections_ import ResizeArray_map
from .ldcontext import LDContext

__G = TypeVar("__G")

__F = TypeVar("__F")

__D = TypeVar("__D")

__C = TypeVar("__C")

__B = TypeVar("__B")

__A = TypeVar("__A")

def ActivePattern__007CNonStringEnumerable_007C__007C(o: Any=None) -> IEnumerable[Any] | None:
    if str(type(o)) == "<class \'str\'>":
        return None

    elif is_iterable(o):
        return o

    else: 
        return None



def DynamicObj_DynamicObj__DynamicObj_HasProperty_Z721C83C5(this: DynamicObj, property_name: str) -> bool:
    return this.TryGetPropertyValue(property_name) is not None


class ILDObject(Protocol):
    @property
    @abstractmethod
    def AdditionalType(self) -> Array[str]:
        ...

    @AdditionalType.setter
    @abstractmethod
    def AdditionalType(self, __arg0: Array[str]) -> None:
        ...

    @property
    @abstractmethod
    def Id(self) -> str:
        ...

    @property
    @abstractmethod
    def SchemaType(self) -> Array[str]:
        ...

    @SchemaType.setter
    @abstractmethod
    def SchemaType(self, __arg0: Array[str]) -> None:
        ...


def _expr1656() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDValue", None, LDValue)


class LDValue:
    def __init__(self, value: Any=None, value_type: str | None=None) -> None:
        self.value_type_004054: str = default_arg(value_type, "string")
        self.value_004055: Any = value

    @property
    def Value(self, __unit: None=None) -> Any:
        this: LDValue = self
        return this.value_004055

    @Value.setter
    def Value(self, v: Any=None) -> None:
        this: LDValue = self
        this.value_004055 = v

    @property
    def ValueType(self, __unit: None=None) -> str:
        this: LDValue = self
        return this.value_type_004054

    @ValueType.setter
    def ValueType(self, v: str) -> None:
        this: LDValue = self
        this.value_type_004054 = v

    def __eq__(self, other: Any=None) -> bool:
        this: LDValue = self
        return equals(this.Value, other.Value) if isinstance(other, LDValue) else False

    def __hash__(self, __unit: None=None) -> int:
        this: LDValue = self
        return merge_hashes(123, identity_hash(this.Value))


LDValue_reflection = _expr1656

def LDValue__ctor_77809003(value: Any=None, value_type: str | None=None) -> LDValue:
    return LDValue(value, value_type)


def _expr1657() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDRef", None, LDRef)


class LDRef:
    def __init__(self, id: str) -> None:
        self.id_004075: str = id

    @property
    def Id(self, __unit: None=None) -> str:
        this: LDRef = self
        return this.id_004075

    @Id.setter
    def Id(self, v: str) -> None:
        this: LDRef = self
        this.id_004075 = v

    def __eq__(self, other: Any=None) -> bool:
        this: LDRef = self
        return (this.Id == other.Id) if isinstance(other, LDRef) else False

    def __hash__(self, __unit: None=None) -> int:
        this: LDRef = self
        return merge_hashes(123, string_hash(this.Id))


LDRef_reflection = _expr1657

def LDRef__ctor_Z721C83C5(id: str) -> LDRef:
    return LDRef(id)


def _expr1662() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDGraph", None, LDGraph, DynamicObj_reflection())


class LDGraph(DynamicObj):
    def __init__(self, id: str | None=None, nodes: Array[LDNode] | None=None, context: LDContext | None=None) -> None:
        super().__init__()
        this: FSharpRef[LDGraph] = FSharpRef(None)
        this.contents = self
        self.id_004094: str | None = id
        self.mappings: Any = dict([])
        self.init_004090: int = 1
        if context is None:
            pass

        else: 
            ctx: LDContext = context
            this.contents.SetContext(ctx)

        if nodes is None:
            pass

        else: 
            def action(node: LDNode) -> None:
                add_to_dict(self.mappings, node.Id, node)

            iterate(action, nodes)


    @property
    def Id(self, __unit: None=None) -> str | None:
        this: LDGraph = self
        return this.id_004094

    @Id.setter
    def Id(self, v: str | None=None) -> None:
        this: LDGraph = self
        this.id_004094 = v

    @property
    def Nodes(self, __unit: None=None) -> Array[LDNode]:
        this: LDGraph = self
        return list(this.mappings.values())

    def ContainsNode(self, id: str) -> bool:
        this: LDGraph = self
        return this.mappings.has(id)

    def GetNode(self, id: str) -> LDNode:
        this: LDGraph = self
        return get_item_from_dict(this.mappings, id)

    def TryGetNode(self, id: str) -> LDNode | None:
        this: LDGraph = self
        match_value: tuple[bool, LDNode]
        out_arg: LDNode = None
        def _arrow1658(__unit: None=None) -> LDNode:
            return out_arg

        def _arrow1659(v: LDNode) -> None:
            nonlocal out_arg
            out_arg = v

        match_value = (try_get_value(this.mappings, id, FSharpRef(_arrow1658, _arrow1659)), out_arg)
        return match_value[1] if match_value[0] else None

    def AddNode(self, node: LDNode) -> None:
        this: LDGraph = self
        id: str = node.Id
        match_value: LDNode | None = this.TryGetNode(id)
        if match_value is None:
            add_to_dict(this.mappings, id, node)

        else: 
            existing_node: LDNode = match_value
            node.MergeAppendInto_InPlace(existing_node, this)


    def Compact_InPlace(self, context: LDContext | None=None) -> None:
        this: LDGraph = self
        context_1: LDContext | None
        specific_context: LDContext | None = this.TryGetContext()
        context_1 = LDContext.try_combine_optional(context, specific_context)
        def action(node: LDNode) -> None:
            node.Compact_InPlace(context_1)

        iterate(action, this.Nodes)

    def SetContext(self, context: LDContext) -> None:
        this: LDGraph = self
        this.SetProperty("@context", context)

    @staticmethod
    def set_context(context: LDContext) -> Callable[[__G], None]:
        def _arrow1660(roc: __G | None=None) -> None:
            roc.SetContext(context)

        return _arrow1660

    def TryGetContext(self, __unit: None=None) -> LDContext | None:
        this: LDGraph = self
        match_value: Any | None = this.TryGetPropertyValue("@context")
        if match_value is not None:
            o: Any = value_3(match_value)
            return o if isinstance(o, LDContext) else None

        else: 
            return None


    @staticmethod
    def try_get_context(__unit: None=None) -> Callable[[__F], LDContext | None]:
        def _arrow1661(roc: __F | None=None) -> LDContext | None:
            return roc.TryGetContext()

        return _arrow1661

    def RemoveContext(self, __unit: None=None) -> bool:
        this: LDGraph = self
        return this.RemoveProperty("@context")

    def GetDynamicPropertyHelpers(self, __unit: None=None) -> IEnumerable_1[PropertyHelper]:
        this: LDGraph = self
        def predicate(ph: PropertyHelper) -> bool:
            return not (True if starts_with_exact(ph.Name, "init@") else (ph.Name == "mappings"))

        return filter_2(predicate, this.GetPropertyHelpers(False))

    def GetDynamicPropertyNames(self, context: LDContext | None=None) -> IEnumerable_1[str]:
        this: LDGraph = self
        context_1: LDContext | None
        specific_context: LDContext | None = this.TryGetContext()
        context_1 = LDContext.try_combine_optional(context, specific_context)
        def chooser(ph: PropertyHelper) -> str | None:
            name: str
            if context_1 is None:
                name = ph.Name

            else: 
                ctx: LDContext = context_1
                match_value: str | None = ctx.TryResolveTerm(ph.Name)
                name = ph.Name if (match_value is None) else match_value

            if name == "@context":
                return None

            else: 
                return name


        return choose(chooser, this.GetDynamicPropertyHelpers())


LDGraph_reflection = _expr1662

def LDGraph__ctor_5FC797DE(id: str | None=None, nodes: Array[LDNode] | None=None, context: LDContext | None=None) -> LDGraph:
    return LDGraph(id, nodes, context)


def _expr1719() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDNode", None, LDNode, DynamicObj_reflection())


class LDNode(DynamicObj):
    def __init__(self, id: str, schema_type: Array[str], additional_type: Array[str] | None=None, context: LDContext | None=None) -> None:
        super().__init__()
        this: FSharpRef[LDNode] = FSharpRef(None)
        self.id: str = id
        this.contents = self
        self.schema_type_0040178: Array[str] = schema_type
        self.additional_type_0040179: Array[str] = default_arg(additional_type, [])
        self.init_0040175_002D1: int = 1
        if context is None:
            pass

        else: 
            ctx: LDContext = context
            this.contents.SetContext(ctx)


    @property
    def Id(self, __unit: None=None) -> str:
        this: LDNode = self
        return this.id

    @property
    def SchemaType(self, __unit: None=None) -> Array[str]:
        this: LDNode = self
        return this.schema_type_0040178

    @SchemaType.setter
    def SchemaType(self, value: Array[str]) -> None:
        this: LDNode = self
        this.schema_type_0040178 = value

    @property
    def AdditionalType(self, __unit: None=None) -> Array[str]:
        this: LDNode = self
        return this.additional_type_0040179

    @AdditionalType.setter
    def AdditionalType(self, value: Array[str]) -> None:
        this: LDNode = self
        this.additional_type_0040179 = value

    def HasType(self, schema_type: str, context: LDContext | None=None) -> bool:
        this: LDNode = self
        context_1: LDContext | None
        specific_context: LDContext | None = this.TryGetContext()
        context_1 = LDContext.try_combine_optional(context, specific_context)
        def predicate(st: str) -> bool:
            if st == schema_type:
                return True

            elif context_1 is None:
                return False

            else: 
                ctx: LDContext = context_1
                match_value: str | None = ctx.TryResolveTerm(st)
                match_value_1: str | None = ctx.TryResolveTerm(schema_type)
                if match_value is None:
                    if match_value_1 is not None:
                        schema_type_2: str = match_value_1
                        return st == schema_type_2

                    else: 
                        return False


                elif match_value_1 is None:
                    st_2: str = match_value
                    return st_2 == schema_type

                else: 
                    schema_type_1: str = match_value_1
                    st_1: str = match_value
                    return st_1 == schema_type_1



        return exists(predicate, this.SchemaType)

    def TryGetProperty(self, property_name: str, context: LDContext | None=None) -> Any | None:
        this: LDNode = self
        match_value: Any | None = this.TryGetPropertyValue(property_name)
        if match_value is None:
            match_value_1: LDContext | None
            specific_context: LDContext | None = this.TryGetContext()
            match_value_1 = LDContext.try_combine_optional(context, specific_context)
            if match_value_1 is None:
                return None

            else: 
                ctx: LDContext = match_value_1
                match_value_2: str | None = ctx.TryResolveTerm(property_name)
                if match_value_2 is None:
                    match_value_3: str | None = ctx.TryGetTerm(property_name)
                    if match_value_3 is None:
                        return None

                    else: 
                        term_1: str = match_value_3
                        return this.TryGetPropertyValue(term_1)


                else: 
                    term: str = match_value_2
                    return this.TryGetPropertyValue(term)



        else: 
            return some(value_3(match_value))


    def TryGetPropertyAsSingleton(self, property_name: str, context: LDContext | None=None) -> Any | None:
        this: LDNode = self
        match_value: Any | None = this.TryGetProperty(property_name, context)
        if match_value is not None:
            if str(type(value_3(match_value))) == "<class \'str\'>":
                s: str = value_3(match_value)
                return some(s)

            elif is_iterable(value_3(match_value)):
                e: IEnumerable[Any] = value_3(match_value)
                en: IEnumerator[Any] = get_enumerator(e)
                return some(en.System_Collections_IEnumerator_get_Current()) if en.System_Collections_IEnumerator_MoveNext() else None

            else: 
                o: Any = value_3(match_value)
                return some(o)


        else: 
            return None


    def GetPropertyValues(self, property_name: str, filter: Callable[[Any, LDContext | None], bool] | None=None, context: LDContext | None=None) -> Array[Any]:
        this: LDNode = self
        def _arrow1664(_arg: Any=None) -> Callable[[LDContext | None], bool]:
            def _arrow1663(_arg_1: LDContext | None=None) -> bool:
                return True

            return _arrow1663

        filter_1: Callable[[Any, LDContext | None], bool] = default_arg(map(curry2, filter), _arrow1664)
        match_value: Any | None = this.TryGetProperty(property_name, context)
        (pattern_matching_result, s, e, o_1) = (None, None, None, None)
        if match_value is not None:
            if str(type(value_3(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                s = value_3(match_value)

            elif is_iterable(value_3(match_value)):
                pattern_matching_result = 1
                e = value_3(match_value)

            elif filter_1(value_3(match_value))(context):
                pattern_matching_result = 2
                o_1 = value_3(match_value)

            else: 
                pattern_matching_result = 3


        else: 
            pattern_matching_result = 3

        if pattern_matching_result == 0:
            return [s] if filter_1(s)(context) else []

        elif pattern_matching_result == 1:
            en: IEnumerator[Any] = get_enumerator(e)
            def _arrow1667(__unit: None=None) -> IEnumerable_1[Any]:
                def _arrow1665(__unit: None=None) -> bool:
                    return en.System_Collections_IEnumerator_MoveNext()

                def _arrow1666(__unit: None=None) -> IEnumerable_1[Any]:
                    return singleton_2(en.System_Collections_IEnumerator_get_Current()) if filter_1(en.System_Collections_IEnumerator_get_Current())(context) else empty()

                return enumerate_while(_arrow1665, delay(_arrow1666))

            return list(to_list(delay(_arrow1667)))

        elif pattern_matching_result == 2:
            return [o_1]

        elif pattern_matching_result == 3:
            return []


    def TryGetPropertyAsSingleNode(self, property_name: str, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        this: LDNode = self
        match_value: Any | None = this.TryGetPropertyAsSingleton(property_name, context)
        (pattern_matching_result, n, r_1) = (None, None, None)
        if match_value is not None:
            if isinstance(value_3(match_value), LDNode):
                pattern_matching_result = 0
                n = value_3(match_value)

            elif isinstance(value_3(match_value), LDRef):
                def _arrow1668(__unit: None=None) -> bool:
                    r: LDRef = value_3(match_value)
                    return graph is not None

                if _arrow1668():
                    pattern_matching_result = 1
                    r_1 = value_3(match_value)

                else: 
                    pattern_matching_result = 2


            else: 
                pattern_matching_result = 2


        else: 
            pattern_matching_result = 2

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            match_value_1: LDNode | None = value_3(graph).TryGetNode(r_1.Id)
            return None if (match_value_1 is None) else match_value_1

        elif pattern_matching_result == 2:
            return None


    def GetPropertyNodes(self, property_name: str, filter: Callable[[LDNode, LDContext | None], bool] | None=None, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        this: LDNode = self
        context_1: LDContext | None
        specific_context: LDContext | None = this.TryGetContext()
        context_1 = LDContext.try_combine_optional(context, specific_context)
        def chooser(o: Any=None) -> LDNode | None:
            (pattern_matching_result,) = (None,)
            if isinstance(o, LDRef):
                if graph is not None:
                    pattern_matching_result = 0

                else: 
                    pattern_matching_result = 2


            elif isinstance(o, LDNode):
                pattern_matching_result = 1

            else: 
                pattern_matching_result = 2

            if pattern_matching_result == 0:
                match_value: LDNode | None = value_3(graph).TryGetNode(o.Id)
                if match_value is None:
                    return None

                else: 
                    n: LDNode = match_value
                    if filter is None:
                        return n

                    elif filter(n, context_1):
                        def _arrow1669(f: Callable[[LDNode, LDContext | None], bool], o: Any=o) -> Callable[[LDNode, LDContext | None], bool]:
                            return curry2(f)

                        f_1: Callable[[LDNode, LDContext | None], bool] = map(_arrow1669, filter)
                        return n

                    else: 
                        return None



            elif pattern_matching_result == 1:
                n_1: LDNode = o
                if filter is None:
                    return n_1

                elif filter(n_1, context_1):
                    def _arrow1670(f: Callable[[LDNode, LDContext | None], bool], o: Any=o) -> Callable[[LDNode, LDContext | None], bool]:
                        return curry2(f)

                    f_3: Callable[[LDNode, LDContext | None], bool] = map(_arrow1670, filter)
                    return n_1

                else: 
                    return None


            elif pattern_matching_result == 2:
                return None


        return list(choose(chooser, this.GetPropertyValues(property_name, None, context_1)))

    def GetDynamicPropertyHelpers(self, __unit: None=None) -> IEnumerable_1[PropertyHelper]:
        this: LDNode = self
        def predicate(ph: PropertyHelper) -> bool:
            return not (True if starts_with_exact(ph.Name, "init_") else (ph.Name == "id"))

        return filter_2(predicate, this.GetPropertyHelpers(False))

    def GetPropertyNames(self, context: LDContext | None=None) -> IEnumerable_1[str]:
        this: LDNode = self
        context_1: LDContext | None
        specific_context: LDContext | None = this.TryGetContext()
        context_1 = LDContext.try_combine_optional(context, specific_context)
        def chooser(ph: PropertyHelper) -> str | None:
            name: str
            if context_1 is None:
                name = ph.Name

            else: 
                ctx: LDContext = context_1
                match_value: str | None = ctx.TryResolveTerm(ph.Name)
                name = ph.Name if (match_value is None) else match_value

            if name == "@context":
                return None

            else: 
                return name


        return choose(chooser, this.GetDynamicPropertyHelpers())

    def SetProperty(self, property_name: str, value: Any=None, context: LDContext | None=None) -> Any:
        this: LDNode = self
        context_1: LDContext | None
        specific_context: LDContext | None = this.TryGetContext()
        context_1 = LDContext.try_combine_optional(context, specific_context)
        def predicate(pn: str) -> bool:
            if context_1 is None:
                return pn == property_name

            else: 
                c: LDContext = context_1
                return c.PropertyNamesMatch(pn, property_name)


        property_name_1: str = default_arg(try_find(predicate, this.GetPropertyNames()), property_name)
        super().SetProperty(property_name_1,value)

    def SetOptionalProperty(self, property_name: str, value: Any | None=None, context: LDContext | None=None) -> None:
        this: LDNode = self
        if value is None:
            pass

        else: 
            v: __D = value_3(value)
            this.SetProperty(property_name, v, context)


    def HasProperty(self, property_name: str, context: LDContext | None=None) -> bool:
        this: LDNode = self
        v: Any | None = this.TryGetProperty(property_name, context)
        def _arrow1671(__unit: None=None) -> bool:
            v_2: Any = value_3(v)
            return False

        def _arrow1672(__unit: None=None) -> bool:
            e: IEnumerable[Any] = value_3(v)
            return get_enumerator(e).System_Collections_IEnumerator_MoveNext()

        return (_arrow1671() if equals(value_3(v), None) else (_arrow1672() if is_iterable(value_3(v)) else True)) if (v is not None) else False

    def SetContext(self, context: LDContext) -> None:
        this: LDNode = self
        this.SetProperty("@context", context)

    @staticmethod
    def set_context(context: LDContext) -> Callable[[__C], None]:
        def _arrow1673(roc: __C | None=None) -> None:
            roc.SetContext(context)

        return _arrow1673

    def TryGetContext(self, __unit: None=None) -> LDContext | None:
        this: LDNode = self
        match_value: Any | None = this.TryGetPropertyValue("@context")
        if match_value is not None:
            o: Any = value_3(match_value)
            return o if isinstance(o, LDContext) else None

        else: 
            return None


    @staticmethod
    def try_get_context(__unit: None=None) -> Callable[[__B], LDContext | None]:
        def _arrow1674(roc: __B | None=None) -> LDContext | None:
            return roc.TryGetContext()

        return _arrow1674

    def RemoveContext(self, __unit: None=None) -> bool:
        this: LDNode = self
        return this.RemoveProperty("@context")

    def MergeAppendInto_InPlace(self, other: LDNode, flatten_to: LDGraph | None=None) -> None:
        this: LDNode = self
        flatten_to_singleton: Callable[[Any], Any]
        if flatten_to is None:
            def _arrow1675(x: Any=None) -> Any:
                return x

            flatten_to_singleton = _arrow1675

        else: 
            graph: LDGraph = flatten_to
            def f(o: Any=None) -> Any:
                if isinstance(o, LDNode):
                    ignore(o.Flatten(graph))
                    return LDRef(o.Id)

                else: 
                    return o


            flatten_to_singleton = f

        flatten_to_ra: Callable[[Array[Any]], Array[Any]]
        if flatten_to is None:
            def _arrow1676(x_1: Array[Any]) -> Array[Any]:
                return x_1

            flatten_to_ra = _arrow1676

        else: 
            graph_1: LDGraph = flatten_to
            def _arrow1677(a: Array[Any]) -> Array[Any]:
                return ResizeArray_map(flatten_to_singleton, a)

            flatten_to_ra = _arrow1677

        flatten_to_any: Callable[[Any], Any]
        if flatten_to is None:
            def _arrow1678(x_2: Any=None) -> Any:
                return x_2

            flatten_to_any = _arrow1678

        else: 
            graph_2: LDGraph = flatten_to
            def f_2(o_1: Any=None) -> Any:
                if isinstance(o_1, LDNode):
                    ignore(o_1.Flatten(graph_2))
                    return LDRef(o_1.Id)

                else: 
                    active_pattern_result: IEnumerable[Any] | None = ActivePattern__007CNonStringEnumerable_007C__007C(o_1)
                    if active_pattern_result is not None:
                        e: IEnumerable[Any] = active_pattern_result
                        def _arrow1682(__unit: None=None, o_1: Any=o_1) -> IEnumerable_1[Any]:
                            def _arrow1679(__unit: None=None) -> IEnumerator[Any]:
                                return get_enumerator(e)

                            def _arrow1680(enumerator: IEnumerator[Any]) -> bool:
                                return enumerator.System_Collections_IEnumerator_MoveNext()

                            def _arrow1681(enumerator_1: IEnumerator[Any]) -> Any:
                                return enumerator_1.System_Collections_IEnumerator_get_Current()

                            return map_1(f_2, enumerate_from_functions(_arrow1679, _arrow1680, _arrow1681))

                        return list(to_list(delay(_arrow1682)))

                    else: 
                        return o_1



            flatten_to_any = f_2

        def to_equalitor(o_2: Any=None) -> Any:
            if isinstance(o_2, LDNode):
                return o_2.Id

            elif isinstance(o_2, LDRef):
                return o_2.Id

            else: 
                return o_2


        def action(pn: str) -> None:
            match_value: Any | None = other.TryGetProperty(pn)
            if match_value is None:
                v_3: Any = flatten_to_any(value_3(this.TryGetProperty(pn)))
                other.SetProperty(pn, v_3)

            else: 
                other_val: Any = value_3(match_value)
                this_val: Any = value_3(this.TryGetProperty(pn))
                (pattern_matching_result, e1, e2) = (None, None, None)
                active_pattern_result_1: IEnumerable[Any] | None = ActivePattern__007CNonStringEnumerable_007C__007C(this_val)
                if active_pattern_result_1 is not None:
                    active_pattern_result_2: IEnumerable[Any] | None = ActivePattern__007CNonStringEnumerable_007C__007C(other_val)
                    if active_pattern_result_2 is not None:
                        pattern_matching_result = 0
                        e1 = active_pattern_result_1
                        e2 = active_pattern_result_2

                    else: 
                        pattern_matching_result = 1


                else: 
                    pattern_matching_result = 1

                if pattern_matching_result == 0:
                    def _arrow1692(__unit: None=None, pn: Any=pn) -> IEnumerable_1[Any]:
                        def _arrow1683(v_1: Any=None) -> Any:
                            return v_1

                        def _arrow1684(__unit: None=None) -> IEnumerator[Any]:
                            return get_enumerator(e2)

                        def _arrow1685(enumerator_2: IEnumerator[Any]) -> bool:
                            return enumerator_2.System_Collections_IEnumerator_MoveNext()

                        def _arrow1686(enumerator_3: IEnumerator[Any]) -> Any:
                            return enumerator_3.System_Collections_IEnumerator_get_Current()

                        def _arrow1691(__unit: None=None) -> IEnumerable_1[Any]:
                            def _arrow1687(v_2: Any=None) -> Any:
                                return v_2

                            def _arrow1688(__unit: None=None) -> IEnumerator[Any]:
                                return get_enumerator(e1)

                            def _arrow1689(enumerator_4: IEnumerator[Any]) -> bool:
                                return enumerator_4.System_Collections_IEnumerator_MoveNext()

                            def _arrow1690(enumerator_5: IEnumerator[Any]) -> Any:
                                return enumerator_5.System_Collections_IEnumerator_get_Current()

                            return map_1(_arrow1687, enumerate_from_functions(_arrow1688, _arrow1689, _arrow1690))

                        return append(map_1(_arrow1683, enumerate_from_functions(_arrow1684, _arrow1685, _arrow1686)), delay(_arrow1691))

                    class ObjectExpr1693:
                        @property
                        def Equals(self) -> Callable[[Any, Any], bool]:
                            return equals

                        @property
                        def GetHashCode(self) -> Callable[[Any], int]:
                            return structural_hash

                    l: Array[Any] = flatten_to_ra(list(List_distinctBy(to_equalitor, to_list(delay(_arrow1692)), ObjectExpr1693())))
                    other.SetProperty(pn, l)

                elif pattern_matching_result == 1:
                    active_pattern_result_3: IEnumerable[Any] | None = ActivePattern__007CNonStringEnumerable_007C__007C(this_val)
                    if active_pattern_result_3 is not None:
                        these_vals: IEnumerable[Any] = active_pattern_result_3
                        is_contained: bool = False
                        def _arrow1698(__unit: None=None, pn: Any=pn) -> IEnumerable_1[Any]:
                            def _arrow1694(this_val_1: Any=None) -> IEnumerable_1[Any]:
                                nonlocal is_contained
                                if equals(to_equalitor(this_val_1), to_equalitor(other_val)):
                                    is_contained = True
                                    return singleton_2(flatten_to_singleton(this_val_1))

                                else: 
                                    return singleton_2(this_val_1)


                            def _arrow1695(__unit: None=None) -> IEnumerator[Any]:
                                return get_enumerator(these_vals)

                            def _arrow1696(enumerator_6: IEnumerator[Any]) -> bool:
                                return enumerator_6.System_Collections_IEnumerator_MoveNext()

                            def _arrow1697(enumerator_7: IEnumerator[Any]) -> Any:
                                return enumerator_7.System_Collections_IEnumerator_get_Current()

                            return collect(_arrow1694, enumerate_from_functions(_arrow1695, _arrow1696, _arrow1697))

                        l_1: Array[Any] = list(to_list(delay(_arrow1698)))
                        if not is_contained:
                            (l_1.append(other_val))
                            other.SetProperty(pn, l_1)


                    else: 
                        active_pattern_result_4: IEnumerable[Any] | None = ActivePattern__007CNonStringEnumerable_007C__007C(other_val)
                        if active_pattern_result_4 is not None:
                            other_vals: IEnumerable[Any] = active_pattern_result_4
                            is_contained_1: bool = False
                            def _arrow1705(__unit: None=None, pn: Any=pn) -> IEnumerable_1[Any]:
                                def _arrow1701(other_val_2: Any=None) -> IEnumerable_1[Any]:
                                    def _expr1699():
                                        nonlocal is_contained_1
                                        is_contained_1 = True
                                        return empty()

                                    def _arrow1700(__unit: None=None) -> IEnumerable_1[Any]:
                                        return singleton_2(other_val_2)

                                    return append(_expr1699() if equals(to_equalitor(this_val), to_equalitor(other_val_2)) else empty(), delay(_arrow1700))

                                def _arrow1702(__unit: None=None) -> IEnumerator[Any]:
                                    return get_enumerator(other_vals)

                                def _arrow1703(enumerator_8: IEnumerator[Any]) -> bool:
                                    return enumerator_8.System_Collections_IEnumerator_MoveNext()

                                def _arrow1704(enumerator_9: IEnumerator[Any]) -> Any:
                                    return enumerator_9.System_Collections_IEnumerator_get_Current()

                                return collect(_arrow1701, enumerate_from_functions(_arrow1702, _arrow1703, _arrow1704))

                            l_2: Array[Any] = list(to_list(delay(_arrow1705)))
                            if not is_contained_1:
                                (l_2.append(flatten_to_singleton(this_val)))
                                other.SetProperty(pn, l_2)


                        elif equals(to_equalitor(this_val), to_equalitor(other_val)):
                            pass

                        else: 
                            l_3: Array[Any] = [flatten_to_singleton(this_val), other_val]
                            other.SetProperty(pn, l_3)





        iterate(action, this.GetPropertyNames())

    def Compact_InPlace(self, context: LDContext | None=None, set_context: bool | None=None) -> None:
        this: LDNode = self
        set_context_1: bool = default_arg(set_context, False)
        context_1: LDContext | None
        specific_context: LDContext | None = this.TryGetContext()
        context_1 = LDContext.try_combine_optional(context, specific_context)
        if context_1 is not None:
            context_2: LDContext = value_3(context_1)
            if set_context_1:
                this.SetContext(context_2)

            def _arrow1707(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1706(st: str) -> IEnumerable_1[str]:
                    match_value: str | None = context_2.TryGetTerm(st)
                    return singleton_2(st) if (match_value is None) else singleton_2(match_value)

                return collect(_arrow1706, this.SchemaType)

            new_types: Array[str] = list(to_list(delay(_arrow1707)))
            this.SchemaType = new_types

        def compact_value_in_place(o: Any=None) -> Any:
            (pattern_matching_result, n, s, e, v, x) = (None, None, None, None, None, None)
            if isinstance(o, LDNode):
                pattern_matching_result = 0
                n = o

            elif str(type(o)) == "<class \'str\'>":
                pattern_matching_result = 1
                s = o

            elif isinstance(o, LDValue):
                if is_iterable(o):
                    pattern_matching_result = 2
                    e = o

                else: 
                    pattern_matching_result = 3
                    v = o


            elif is_iterable(o):
                pattern_matching_result = 2
                e = o

            else: 
                pattern_matching_result = 4
                x = o

            if pattern_matching_result == 0:
                n.Compact_InPlace(context_1)
                return n

            elif pattern_matching_result == 1:
                return s

            elif pattern_matching_result == 2:
                en: IEnumerator[Any] = get_enumerator(e)
                def _arrow1710(__unit: None=None, o: Any=o) -> IEnumerable_1[Any]:
                    def _arrow1708(__unit: None=None) -> bool:
                        return en.System_Collections_IEnumerator_MoveNext()

                    def _arrow1709(__unit: None=None) -> IEnumerable_1[Any]:
                        return singleton_2(compact_value_in_place(en.System_Collections_IEnumerator_get_Current()))

                    return enumerate_while(_arrow1708, delay(_arrow1709))

                l: Array[Any] = list(to_list(delay(_arrow1710)))
                if len(l) == 1:
                    return l[0]

                else: 
                    return l


            elif pattern_matching_result == 3:
                return v.Value

            elif pattern_matching_result == 4:
                return x


        def action(ph: PropertyHelper) -> None:
            new_key: str | None
            if context_1 is None:
                new_key = None

            else: 
                ctx: LDContext = context_1
                match_value_1: str | None = ctx.TryGetTerm(ph.Name)
                new_key = None if (match_value_1 is None) else match_value_1

            new_value: Any = compact_value_in_place(ph.GetValue(this))
            (pattern_matching_result_1, key_1) = (None, None)
            if new_key is not None:
                if new_key != ph.Name:
                    pattern_matching_result_1 = 0
                    key_1 = new_key

                else: 
                    pattern_matching_result_1 = 1


            else: 
                pattern_matching_result_1 = 1

            if pattern_matching_result_1 == 0:
                ignore(this.RemoveProperty(ph.Name))
                this.SetProperty(key_1, new_value)

            elif pattern_matching_result_1 == 1:
                ph.SetValue(this, new_value)


        iterate(action, this.GetDynamicPropertyHelpers())

    def Flatten(self, graph: LDGraph | None=None) -> LDGraph:
        this: LDNode = self
        graph_1: LDGraph = LDGraph(None, None, this.TryGetContext()) if (graph is None) else graph
        def flatten_value(o: Any=None) -> Any:
            if isinstance(o, LDNode):
                ignore(o.Flatten(graph_1))
                return LDRef(o.Id)

            elif str(type(o)) == "<class \'str\'>":
                return o

            elif is_iterable(o):
                en: IEnumerator[Any] = get_enumerator(o)
                def _arrow1713(__unit: None=None, o: Any=o) -> IEnumerable_1[Any]:
                    def _arrow1711(__unit: None=None) -> bool:
                        return en.System_Collections_IEnumerator_MoveNext()

                    def _arrow1712(__unit: None=None) -> IEnumerable_1[Any]:
                        return singleton_2(flatten_value(en.System_Collections_IEnumerator_get_Current()))

                    return enumerate_while(_arrow1711, delay(_arrow1712))

                return list(to_list(delay(_arrow1713)))

            else: 
                return o


        def action(ph: PropertyHelper) -> None:
            ph.SetValue(this, flatten_value(ph.GetValue(this)))

        iterate(action, this.GetDynamicPropertyHelpers())
        graph_1.AddNode(this)
        return graph_1

    def Unflatten(self, graph: LDGraph) -> None:
        this: LDNode = self
        def unflatten_value(o: Any=None) -> Any:
            if isinstance(o, LDRef):
                match_value: LDNode | None = graph.TryGetNode(o.Id)
                if match_value is None:
                    return o

                else: 
                    return match_value


            elif isinstance(o, LDNode):
                o.Unflatten(graph)
                return o

            elif is_iterable(o):
                en: IEnumerator[Any] = get_enumerator(o)
                def _arrow1716(__unit: None=None, o: Any=o) -> IEnumerable_1[Any]:
                    def _arrow1714(__unit: None=None) -> bool:
                        return en.System_Collections_IEnumerator_MoveNext()

                    def _arrow1715(__unit: None=None) -> IEnumerable_1[Any]:
                        return singleton_2(unflatten_value(en.System_Collections_IEnumerator_get_Current()))

                    return enumerate_while(_arrow1714, delay(_arrow1715))

                return list(to_list(delay(_arrow1716)))

            else: 
                return o


        def action(ph: PropertyHelper) -> None:
            ph.SetValue(this, unflatten_value(ph.GetValue(this)))

        iterate(action, this.GetDynamicPropertyHelpers())

    @staticmethod
    def remove_context(__unit: None=None) -> Callable[[__A], bool]:
        def _arrow1717(roc: __A | None=None) -> bool:
            return roc.RemoveContext()

        return _arrow1717

    @staticmethod
    def try_from_dynamic_obj(dyn_obj: DynamicObj) -> LDNode | None:
        original_id: str | None
        match_value: Any | None = dyn_obj.TryGetPropertyValue("@id")
        if match_value is not None:
            o: Any = value_3(match_value)
            original_id = o if (str(type(o)) == "<class \'str\'>") else None

        else: 
            original_id = None

        original_type: Array[str] | None
        match_value_1: Any | None = dyn_obj.TryGetPropertyValue("@type")
        (pattern_matching_result, ra, singleton) = (None, None, None)
        if match_value_1 is not None:
            if is_array_like(value_3(match_value_1)):
                pattern_matching_result = 0
                ra = value_3(match_value_1)

            elif str(type(value_3(match_value_1))) == "<class \'str\'>":
                pattern_matching_result = 1
                singleton = value_3(match_value_1)

            else: 
                pattern_matching_result = 2


        else: 
            pattern_matching_result = 2

        if pattern_matching_result == 0:
            original_type = ra

        elif pattern_matching_result == 1:
            original_type = [singleton]

        elif pattern_matching_result == 2:
            original_type = None

        (pattern_matching_result_1, id, st) = (None, None, None)
        if original_id is not None:
            if original_type is not None:
                pattern_matching_result_1 = 0
                id = original_id
                st = original_type

            else: 
                pattern_matching_result_1 = 1


        else: 
            pattern_matching_result_1 = 1

        if pattern_matching_result_1 == 0:
            def _arrow1718(__unit: None=None) -> Array[str] | None:
                match_value_3: Any | None = dyn_obj.TryGetPropertyValue("additionalType")
                (pattern_matching_result_2, ra_1, singleton_1) = (None, None, None)
                if match_value_3 is not None:
                    if is_array_like(value_3(match_value_3)):
                        pattern_matching_result_2 = 0
                        ra_1 = value_3(match_value_3)

                    elif str(type(value_3(match_value_3))) == "<class \'str\'>":
                        pattern_matching_result_2 = 1
                        singleton_1 = value_3(match_value_3)

                    else: 
                        pattern_matching_result_2 = 2


                else: 
                    pattern_matching_result_2 = 2

                if pattern_matching_result_2 == 0:
                    return ra_1

                elif pattern_matching_result_2 == 1:
                    return [singleton_1]

                elif pattern_matching_result_2 == 2:
                    return None


            roc: LDNode = LDNode(id, st, _arrow1718())
            dyn_obj.DeepCopyPropertiesTo(roc, None, False)
            def action(ph: PropertyHelper) -> None:
                if (True if (True if (ph.Name == "@id") else (ph.Name == "@type")) else (ph.Name == "additionalType")) if ph.IsDynamic else False:
                    ph.RemoveValue(roc)


            iterate(action, roc.GetDynamicPropertyHelpers())
            return roc

        elif pattern_matching_result_1 == 1:
            return None



LDNode_reflection = _expr1719

def LDNode__ctor_479BCDCF(id: str, schema_type: Array[str], additional_type: Array[str] | None=None, context: LDContext | None=None) -> LDNode:
    return LDNode(id, schema_type, additional_type, context)


__all__ = ["ActivePattern__007CNonStringEnumerable_007C__007C", "DynamicObj_DynamicObj__DynamicObj_HasProperty_Z721C83C5", "LDValue_reflection", "LDRef_reflection", "LDGraph_reflection", "LDNode_reflection"]

