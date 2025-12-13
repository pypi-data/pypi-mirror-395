from xml.etree.ElementTree import Element
from typing import Literal

from .asset import Asset

__all__ = ["ModelAsset"]

_CONTENT_TYPE = Literal["text/xml", "text/usd"]


class ModelAsset(Asset):
    content_type: _CONTENT_TYPE | None = None

    def to_xml(self) -> Element:
        e = Element("model")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)
        if self.content_type is not None:
            e.set("content_type", self.content_type)
        return e

    def attribute_hash(self) -> int:
        return hash(
            (
                self.clazz,
                self.file,
                self.content_type,
            )
        )

    def attribute_equality(self, other: object) -> bool:
        if not isinstance(other, ModelAsset):
            return False

        return (
            self.file == other.file  # We ignore name so to detect duplicate models
            and self.clazz == other.clazz
            and self.content_type == other.content_type
        )
