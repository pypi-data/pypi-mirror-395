from xml.etree.ElementTree import Element
from typing import Literal, SupportsFloat
from mjxml.typeutils import ArrayLike, floatarr_to_str
from mjxml.body.joint import Joint
from .equality import Equality

__all__ = ["JointEquality"]

class JointEquality(Equality):
    joint1: Joint
    joint2: Joint

    polycoeff: ArrayLike[SupportsFloat, Literal[2, 3, 4, 5]]

    def to_xml(self) -> Element:
        e = Element('joint')
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)
        if self.joint1 is self.joint2:
            raise ValueError("joint1 and joint2 cannot be the same joint in JointEquality")
        if self.joint1.name is None or self.joint2.name is None:
            raise ValueError(
                "Both joints must have a name assigned for JointEquality serialization"
                f"Got joint1.name={self.joint1.name}, joint2.name={self.joint2.name}")

        n1 = str(self.joint1.name)
        n2 = str(self.joint2.name)
        if n1 == n2:
            raise ValueError("joint1 and joint2 must have different names in JointEquality")

        coeff = list(self.polycoeff)
        while len(coeff) < 5:
            coeff.append(0.0)

        e.set('joint1', n1)
        e.set('joint2', n2)
        e.set('polycoef', floatarr_to_str(coeff))
        return e