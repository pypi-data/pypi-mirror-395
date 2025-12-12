from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from ...fable_modules.fable_library.list import (FSharpList, try_find, exists, append, singleton, filter, empty)
from ...fable_modules.fable_library.option import (map, default_arg)
from ...fable_modules.fable_library.reflection import (TypeInfo, string_type, option_type, list_type, record_type)
from ...fable_modules.fable_library.types import Record
from ...fable_modules.fable_library.util import equals
from ..comment import (Comment, Comment_reflection)
from ..ontology_annotation import (OntologyAnnotation, OntologyAnnotation_reflection)
from .component import (Component, Component_reflection)
from .protocol_parameter import (ProtocolParameter, ProtocolParameter_reflection)

def _expr763() -> TypeInfo:
    return record_type("ARCtrl.Process.Protocol", [], Protocol, lambda: [("ID", option_type(string_type)), ("Name", option_type(string_type)), ("ProtocolType", option_type(OntologyAnnotation_reflection())), ("Description", option_type(string_type)), ("Uri", option_type(string_type)), ("Version", option_type(string_type)), ("Parameters", option_type(list_type(ProtocolParameter_reflection()))), ("Components", option_type(list_type(Component_reflection()))), ("Comments", option_type(list_type(Comment_reflection())))])


@dataclass(eq = False, repr = False, slots = True)
class Protocol(Record):
    ID: str | None
    Name: str | None
    ProtocolType: OntologyAnnotation | None
    Description: str | None
    Uri: str | None
    Version: str | None
    Parameters: FSharpList[ProtocolParameter] | None
    Components: FSharpList[Component] | None
    Comments: FSharpList[Comment] | None

Protocol_reflection = _expr763

def Protocol_make(id: str | None=None, name: str | None=None, protocol_type: OntologyAnnotation | None=None, description: str | None=None, uri: str | None=None, version: str | None=None, parameters: FSharpList[ProtocolParameter] | None=None, components: FSharpList[Component] | None=None, comments: FSharpList[Comment] | None=None) -> Protocol:
    return Protocol(id, name, protocol_type, description, uri, version, parameters, components, comments)


def Protocol_create_Z414665E7(Id: str | None=None, Name: str | None=None, ProtocolType: OntologyAnnotation | None=None, Description: str | None=None, Uri: str | None=None, Version: str | None=None, Parameters: FSharpList[ProtocolParameter] | None=None, Components: FSharpList[Component] | None=None, Comments: FSharpList[Comment] | None=None) -> Protocol:
    return Protocol_make(Id, Name, ProtocolType, Description, Uri, Version, Parameters, Components, Comments)


def Protocol_get_empty(__unit: None=None) -> Protocol:
    return Protocol_create_Z414665E7()


def Protocol_tryGetByName(name: str, protocols: FSharpList[Protocol]) -> Protocol | None:
    def _arrow764(p: Protocol, name: Any=name, protocols: Any=protocols) -> bool:
        return equals(p.Name, name)

    return try_find(_arrow764, protocols)


def Protocol_existsByName(name: str, protocols: FSharpList[Protocol]) -> bool:
    def _arrow765(p: Protocol, name: Any=name, protocols: Any=protocols) -> bool:
        return equals(p.Name, name)

    return exists(_arrow765, protocols)


def Protocol_add(protocols: FSharpList[Protocol], protocol: Protocol) -> FSharpList[Protocol]:
    return append(protocols, singleton(protocol))


def Protocol_removeByName(name: str, protocols: FSharpList[Protocol]) -> FSharpList[Protocol]:
    def _arrow766(p: Protocol, name: Any=name, protocols: Any=protocols) -> bool:
        return not equals(p.Name, name)

    return filter(_arrow766, protocols)


def Protocol_getComments_3BF20962(protocol: Protocol) -> FSharpList[Comment] | None:
    return protocol.Comments


def Protocol_mapComments(f: Callable[[FSharpList[Comment]], FSharpList[Comment]], protocol: Protocol) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, protocol.ProtocolType, protocol.Description, protocol.Uri, protocol.Version, protocol.Parameters, protocol.Components, map(f, protocol.Comments))


def Protocol_setComments(protocol: Protocol, comments: FSharpList[Comment]) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, protocol.ProtocolType, protocol.Description, protocol.Uri, protocol.Version, protocol.Parameters, protocol.Components, comments)


def Protocol_getProtocolType_3BF20962(protocol: Protocol) -> OntologyAnnotation | None:
    return protocol.ProtocolType


def Protocol_mapProtocolType(f: Callable[[OntologyAnnotation], OntologyAnnotation], protocol: Protocol) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, map(f, protocol.ProtocolType), protocol.Description, protocol.Uri, protocol.Version, protocol.Parameters, protocol.Components, protocol.Comments)


def Protocol_setProtocolType(protocol: Protocol, protocol_type: OntologyAnnotation) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, protocol_type, protocol.Description, protocol.Uri, protocol.Version, protocol.Parameters, protocol.Components, protocol.Comments)


def Protocol_getVersion_3BF20962(protocol: Protocol) -> str | None:
    return protocol.Version


def Protocol_mapVersion(f: Callable[[str], str], protocol: Protocol) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, protocol.ProtocolType, protocol.Description, protocol.Uri, map(f, protocol.Version), protocol.Parameters, protocol.Components, protocol.Comments)


def Protocol_setVersion(protocol: Protocol, version: str) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, protocol.ProtocolType, protocol.Description, protocol.Uri, version, protocol.Parameters, protocol.Components, protocol.Comments)


def Protocol_getName_3BF20962(protocol: Protocol) -> str | None:
    return protocol.Name


def Protocol_mapName(f: Callable[[str], str], protocol: Protocol) -> Protocol:
    return Protocol(protocol.ID, map(f, protocol.Name), protocol.ProtocolType, protocol.Description, protocol.Uri, protocol.Version, protocol.Parameters, protocol.Components, protocol.Comments)


def Protocol_setName(protocol: Protocol, name: str) -> Protocol:
    return Protocol(protocol.ID, name, protocol.ProtocolType, protocol.Description, protocol.Uri, protocol.Version, protocol.Parameters, protocol.Components, protocol.Comments)


def Protocol_getDescription_3BF20962(protocol: Protocol) -> str | None:
    return protocol.Description


def Protocol_mapDescription(f: Callable[[str], str], protocol: Protocol) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, protocol.ProtocolType, map(f, protocol.Description), protocol.Uri, protocol.Version, protocol.Parameters, protocol.Components, protocol.Comments)


def Protocol_setDescription(protocol: Protocol, description: str) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, protocol.ProtocolType, description, protocol.Uri, protocol.Version, protocol.Parameters, protocol.Components, protocol.Comments)


def Protocol_getUri_3BF20962(protocol: Protocol) -> str | None:
    return protocol.Uri


def Protocol_mapUri(f: Callable[[str], str], protocol: Protocol) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, protocol.ProtocolType, protocol.Description, map(f, protocol.Uri), protocol.Version, protocol.Parameters, protocol.Components, protocol.Comments)


def Protocol_setUri(protocol: Protocol, uri: str) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, protocol.ProtocolType, protocol.Description, uri, protocol.Version, protocol.Parameters, protocol.Components, protocol.Comments)


def Protocol_getComponents_3BF20962(protocol: Protocol) -> FSharpList[Component] | None:
    return protocol.Components


def Protocol_mapComponents(f: Callable[[FSharpList[Component]], FSharpList[Component]], protocol: Protocol) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, protocol.ProtocolType, protocol.Description, protocol.Uri, protocol.Version, protocol.Parameters, map(f, protocol.Components), protocol.Comments)


def Protocol_setComponents(protocol: Protocol, components: FSharpList[Component]) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, protocol.ProtocolType, protocol.Description, protocol.Uri, protocol.Version, protocol.Parameters, components, protocol.Comments)


def Protocol_addComponent(comp: Component, protocol: Protocol) -> Protocol:
    return Protocol_setComponents(protocol, append(default_arg(protocol.Components, empty()), singleton(comp)))


def Protocol_getParameters_3BF20962(protocol: Protocol) -> FSharpList[ProtocolParameter] | None:
    return protocol.Parameters


def Protocol_mapParameters(f: Callable[[FSharpList[ProtocolParameter]], FSharpList[ProtocolParameter]], protocol: Protocol) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, protocol.ProtocolType, protocol.Description, protocol.Uri, protocol.Version, map(f, protocol.Parameters), protocol.Components, protocol.Comments)


def Protocol_setParameters(protocol: Protocol, parameters: FSharpList[ProtocolParameter]) -> Protocol:
    return Protocol(protocol.ID, protocol.Name, protocol.ProtocolType, protocol.Description, protocol.Uri, protocol.Version, parameters, protocol.Components, protocol.Comments)


def Protocol_addParameter(parameter: ProtocolParameter, protocol: Protocol) -> Protocol:
    return Protocol_setParameters(protocol, append(default_arg(protocol.Parameters, empty()), singleton(parameter)))


__all__ = ["Protocol_reflection", "Protocol_make", "Protocol_create_Z414665E7", "Protocol_get_empty", "Protocol_tryGetByName", "Protocol_existsByName", "Protocol_add", "Protocol_removeByName", "Protocol_getComments_3BF20962", "Protocol_mapComments", "Protocol_setComments", "Protocol_getProtocolType_3BF20962", "Protocol_mapProtocolType", "Protocol_setProtocolType", "Protocol_getVersion_3BF20962", "Protocol_mapVersion", "Protocol_setVersion", "Protocol_getName_3BF20962", "Protocol_mapName", "Protocol_setName", "Protocol_getDescription_3BF20962", "Protocol_mapDescription", "Protocol_setDescription", "Protocol_getUri_3BF20962", "Protocol_mapUri", "Protocol_setUri", "Protocol_getComponents_3BF20962", "Protocol_mapComponents", "Protocol_setComponents", "Protocol_addComponent", "Protocol_getParameters_3BF20962", "Protocol_mapParameters", "Protocol_setParameters", "Protocol_addParameter"]

