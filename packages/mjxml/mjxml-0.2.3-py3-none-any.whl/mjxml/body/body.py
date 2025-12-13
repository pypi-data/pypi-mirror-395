from mjxml.asset import Asset
from .worldbodychildren import BodyChildren
from pydantic.fields import Field
from xml.etree.ElementTree import Element
from mjxml.rotations import RotationType, to_mjc
from typing import SupportsFloat, Literal, cast
from mjxml.typeutils import SupportsBool, ArrayLike, PosFloat
from mjxml.commons import Defaults

__all__ = ["Body"]


class Body(BodyChildren):
    childclass: Defaults | None = None
    mocap: SupportsBool | None = None
    pos: ArrayLike[SupportsFloat, Literal[3]] | None = None
    rotation: RotationType | None = None
    gravcomp: PosFloat | None = None
    user_params: ArrayLike[SupportsFloat] | None = None

    children: list[BodyChildren] = Field(default_factory=list)

    def to_xml(self) -> Element:
        e = Element("body")
        e = self._process(e)

        for child in self.children:
            e.append(child.to_xml())

        return e

    def add(self, obj: BodyChildren) -> None:
        self.children.append(obj)

    def _process(self, e):
        e = super()._process(e)
        if self.childclass is not None:
            e.set("childclass", str(self.childclass.name))
        if self.mocap is not None:
            e.set("mocap", str(int(self.mocap)))
        if self.pos is not None:
            e.set("pos", " ".join(str(float(v)) for v in self.pos))
        if self.rotation is not None:
            e.set(*to_mjc(self.rotation))
        if self.gravcomp is not None:
            e.set("gravcomp", str(self.gravcomp))
        if self.user_params is not None:
            e.set("user_params", " ".join(str(v) for v in self.user_params))
        return e

    def remove_duplicate_assets(self, existing: dict[int, Asset]) -> None:
        for child in self.children:
            child.remove_duplicate_assets(existing)

    def model_copy(
            self, 
            *, 
            deep: bool = True, 
            update: dict[str, object] | None = None) -> "Body":
        new = cast(Body, super().model_copy(deep=deep, update=update))
        if deep:
            ch = [child.model_copy(deep=True) for child in self.children]
            new.children = cast(list[BodyChildren], ch)
        return new