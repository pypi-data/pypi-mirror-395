from __future__ import annotations
from abc import abstractmethod
from typing import Protocol
from .ontology_annotation import OntologyAnnotation
from .value import Value

class IPropertyValue(Protocol):
    @abstractmethod
    def AlternateName(self) -> str | None:
        ...

    @abstractmethod
    def Description(self) -> str | None:
        ...

    @abstractmethod
    def GetAdditionalType(self) -> str:
        ...

    @abstractmethod
    def GetCategory(self) -> OntologyAnnotation | None:
        ...

    @abstractmethod
    def GetUnit(self) -> OntologyAnnotation | None:
        ...

    @abstractmethod
    def GetValue(self) -> Value | None:
        ...

    @abstractmethod
    def MeasurementMethod(self) -> str | None:
        ...


