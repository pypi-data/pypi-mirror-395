from mjxml.typeutils import Str
from xml.etree.ElementTree import Element
from pydantic.config import ConfigDict
from pydantic.fields import Field
from pydantic.main import BaseModel
from typing import Any, Mapping
from abc import ABC, abstractmethod
from uuid import uuid4
import xml.etree.ElementTree as ET

__all__ = [
    "_XMLSerializable",
    "MJCElement",
    "Defaults",
]

_NAME_LENGTH = 16


class _XMLSerializable(ABC):
    @abstractmethod
    def to_xml(self) -> Element:
        raise NotImplementedError("to_xml method must be implemented by subclasses")

    @abstractmethod
    def _process(self, e: Element) -> Element:
        return e

    def to_xml_str(self, indent: None | int = 2) -> str:
        xml = self.to_xml()
        if indent:
            ET.indent(xml, space=" " * indent)
        xml = ET.tostring(xml, encoding="unicode", xml_declaration=False)
        return xml

    def write(self, filepath: str, indent: int = 2) -> None:
        xml_str = self.to_xml_str(indent=indent)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml_str)


class Defaults(_XMLSerializable, BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    name: Str | None = Field(default_factory=lambda: uuid4().hex[:_NAME_LENGTH])
    attribs: list[Element] = Field(default_factory=list)

    def to_xml(self) -> Element:
        e = Element("default")
        e = self._process(e)
        return e
        
    def _process(self, e: Element) -> Element:
        if self.name is not None:
            e.set("class", str(self.name))
        for attrib in self.attribs:
            e.append(attrib)
        return e


class MJCElement(_XMLSerializable, BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    def model_copy(
        self, 
        *, 
        deep: bool = True, 
        update: Mapping[str, Any] | None = None
    ) -> "MJCElement":
        update: dict[str, Any] = dict(update) if update is not None else {}
        if "name" not in update:
            update["name"] = uuid4().hex[:_NAME_LENGTH]
        return super().model_copy(deep=deep, update=update)

    name: Str | None = Field(default_factory=lambda: uuid4().hex[:_NAME_LENGTH])
    clazz: Defaults | None = Field(default=None)

    def _process(self, e: Element) -> Element:
        if self.name is not None:
            e.set("name", str(self.name))
        if self.clazz is not None:
            e.set("class", str(self.clazz.name))
        return e
