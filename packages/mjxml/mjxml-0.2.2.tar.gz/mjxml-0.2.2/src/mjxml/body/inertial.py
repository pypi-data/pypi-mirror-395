from mjxml.asset import Asset
from xml.etree.ElementTree import Element
from typing import Literal, SupportsFloat
from mjxml.typeutils import ArrayLike, PosFloat, floatarr_to_str
from .worldbodychildren import BodyChildren
from mjxml.rotations import RotationType, to_mjc
import warnings

__all__ = ["Inertial"]

class Inertial(BodyChildren):
    """MuJoCo inertial element.

    Specifies the mass and inertial properties of the body.
    """
    pos: ArrayLike[SupportsFloat, Literal[3]] # Required
    mass: PosFloat # Required
    rotation: RotationType | None = None
    diaginertia: ArrayLike[SupportsFloat, Literal[3]] | None = None
    fullinertia: ArrayLike[SupportsFloat, Literal[6]] | None = None

    def to_xml(self) -> Element:
        e = Element("inertial")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)
        
        # Required attributes
        e.set("pos", floatarr_to_str(self.pos))
        e.set("mass", str(float(self.mass)))

        # Optional attributes
        if self.rotation is not None:
            e.set(*to_mjc(self.rotation))
        
        if self.diaginertia is not None:
            e.set("diaginertia", floatarr_to_str(self.diaginertia))
        elif self.fullinertia is not None:
            e.set("fullinertia", floatarr_to_str(self.fullinertia))
        else:
            # If neither is provided, MuJoCo might infer or error depending on context,
            # but spec says "If this attribute [diaginertia] is omitted, the next attribute [fullinertia] becomes required."
            # However, it also says "If this element is not included... inertial properties are inferred".
            # But if the element IS included, we probably need one of them unless mass/pos is enough for a point mass?
            # The spec says: "If this attribute [diaginertia] is omitted, the next attribute [fullinertia] becomes required."
            # This implies one of them MUST be present if the inertial element exists.
            warnings.warn("Inertial element requires either 'diaginertia' or 'fullinertia' to be specified.")

        if self.diaginertia is not None and self.fullinertia is not None:
             warnings.warn("Both 'diaginertia' and 'fullinertia' are specified. 'diaginertia' takes precedence.")

        return e

    def remove_duplicate_assets(self, existing: dict[int, Asset]) -> None:
        pass  # Inertial does not reference any assets