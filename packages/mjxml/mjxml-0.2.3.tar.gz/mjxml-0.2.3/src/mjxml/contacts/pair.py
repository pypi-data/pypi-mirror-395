from mjxml.contacts.contacts import Contact
from mjxml.body import Geom
from mjxml.typeutils import ArrayLike, floatarr_to_str
from typing import SupportsFloat, Literal
from xml.etree.ElementTree import Element

__all__ = ["ContactPair"]


class ContactPair(Contact):
    """MuJoCo contact pair element."""

    geom1: Geom
    geom2: Geom

    friction: ArrayLike[SupportsFloat, Literal[1, 2, 3, 5]] | None = None
    solref: ArrayLike[SupportsFloat] | None = None
    solimp: ArrayLike[SupportsFloat] | None = None
    solreffriction: ArrayLike[SupportsFloat] | None = None
    margin: SupportsFloat | None = None
    gap: SupportsFloat | None = None

    def to_xml(self) -> Element:
        e = Element("pair")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)

        if self.geom1.name is None:
            raise ValueError("geom1 must have a name")
        if self.geom2.name is None:
            raise ValueError("geom2 must have a name")

        e.set("geom1", str(self.geom1.name))
        e.set("geom2", str(self.geom2.name))

        if self.friction is not None:
            fric = self.friction
            if len(fric) == 1:
                fric = [fric[0], fric[0]]
            e.set("friction", floatarr_to_str(fric))
            e.set("condim", str(len(fric) + 1))
        if self.solref is not None:
            e.set("solref", floatarr_to_str(self.solref))
        if self.solimp is not None:
            e.set("solimp", floatarr_to_str(self.solimp))
        if self.solreffriction is not None:
            e.set("solreffriction", floatarr_to_str(self.solreffriction))
        if self.margin is not None:
            e.set("margin", str(float(self.margin)))
        if self.gap is not None:
            e.set("gap", str(float(self.gap)))

        return e
