from mjxml.asset import Asset
from .inertial import Inertial
from .body import Body
from .joint import Joint
from .worldbodychildren import BodyChildren
from xml.etree.ElementTree import Element

__all__ = ["WorldBody"]


class WorldBody(Body):
    def to_xml(self) -> Element:
        e = Element("worldbody")
        e = self._process(e)

        for child in self.children:
            e.append(child.to_xml())

        return e

    def _process(self, e):
        # Worldbody cannot have any attributes
        return e

    def add(self, obj: BodyChildren) -> None:
        if isinstance(obj, Joint):
            raise TypeError("Joints must be added to bodies, not worldbody") 
        if isinstance(obj, Inertial):
            raise TypeError("Inertial must be added to bodies, not worldbody")
        if isinstance(obj, WorldBody):
            raise TypeError(
                "Cannot add WorldBody to another WorldBody"
                "Consider using model attaching; refer to docs."
            )       
        self.children.append(obj)

    def remove_duplicate_assets(self, existing: dict[int, Asset]) -> None:
        for child in self.children:
            child.remove_duplicate_assets(existing)