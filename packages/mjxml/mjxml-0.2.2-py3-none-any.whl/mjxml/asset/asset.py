from xml.etree.ElementTree import Element
from mjxml.typeutils import Str
from abc import abstractmethod
from mjxml.commons import MJCElement
from typing import Literal, Any

__all__ = [
    "Asset",
]

_TEXTURE_TYPE = Literal["2d", "cube", "skybox"]
_TEXTURE_COLORSPACE = Literal["srgb", "linear"]
_TEXTURE_CONTENT_TYPE = Literal["image/png", "image/ktx", "image/vnd.mujoco.texture"]
_TEXTURE_BUILTIN_TYPE = Literal["gradient", "checker", "flat"]
_TEXTURE_MARK_TYPE = Literal["edge", "cross", "random"]

_MODEL_CONTENT_TYPE = Literal["text/xml", "text/usd"]


class Asset(MJCElement):
    file: Str | None = None

    @property
    def mjc_name(self) -> str:
        if self.name is None:
            if self.file is None:
                raise ValueError("Asset must have either a name or a file specified")
            return str(self.file)
        return str(self.name)

    @abstractmethod
    def attribute_equality(self, other: Any) -> bool:
        raise NotImplementedError()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Asset):
            return False
        return self.name == other.name and self.attribute_equality(other)

    @abstractmethod
    def attribute_hash(self) -> int:
        raise NotImplementedError()

    def __hash__(self) -> int:
        return hash((str(self.name), self.attribute_hash()))

    def _process(self, e: Element) -> Element:
        super()._process(e)
        if self.file is not None:
            e.set("file", str(self.file))
        return e