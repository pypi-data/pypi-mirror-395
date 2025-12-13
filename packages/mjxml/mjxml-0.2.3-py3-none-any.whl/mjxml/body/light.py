from mjxml.asset import Asset
from .worldbodychildren import BodyChildren
from xml.etree.ElementTree import Element
from typing import Literal, SupportsFloat
from mjxml.typeutils import SupportsBool, ArrayLike, PosFloat, Str, floatarr_to_str

__all__ = ["Light"]

_LIGHT_MODE = Literal["fixed", "track", "trackcom", "targetbody", "targetbodycom"]
_LIGHT_TYPE = Literal["spot", "directional", "point", "image"]


class Light(BodyChildren):
    """MuJoCo light element.

    Creates a light attached to a body (or worldbody for fixed lights).
    """

    # Kinematic mode and targeting
    pos: ArrayLike[SupportsFloat, Literal[3]] | None = None
    mode: _LIGHT_MODE | None = None
    target: BodyChildren | None = None

    # Type and legacy directional flag
    type: _LIGHT_TYPE | None = None
    directional: SupportsBool | None = None  # deprecated legacy attribute

    # Shadowing / activation
    castshadow: SupportsBool | None = None
    active: SupportsBool | None = None

    dir: ArrayLike[SupportsFloat, Literal[3]] | None = None

    # Colors and appearance
    diffuse: ArrayLike[SupportsFloat, Literal[3]] | None = None
    ambient: ArrayLike[SupportsFloat, Literal[3]] | None = None
    specular: ArrayLike[SupportsFloat, Literal[3]] | None = None

    # Image-based lighting
    texture: Str | None = None
    intensity: PosFloat | None = None  # for physically-based lighting

    # Spotlight and attenuation parameters
    range: SupportsFloat | None = None
    bulbradius: SupportsFloat | None = None
    attenuation: ArrayLike[SupportsFloat, Literal[3]] | None = None
    cutoff: SupportsFloat | None = None
    exponent: SupportsFloat | None = None

    def to_xml(self) -> Element:
        e = Element("light")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)

        # Kinematic mode and target
        if self.mode is not None:
            e.set("mode", self.mode)
        if self.target is not None:
            if self.target.name is None:
                raise ValueError(
                    "Target body must have a name to be referenced by light"
                )
            e.set("target", str(self.target.name))

        # Light type handling, honoring legacy 'directional' flag when type missing
        if self.type is not None:
            e.set("type", self.type)
        elif self.directional is not None and bool(self.directional):
            e.set("type", "directional")

        # Shadowing / activation
        if self.castshadow is not None:
            e.set("castshadow", str(bool(self.castshadow)).lower())
        if self.active is not None:
            e.set("active", str(bool(self.active)).lower())

        # Pose and direction
        if self.pos is not None:
            e.set("pos", floatarr_to_str(self.pos))
        if self.dir is not None:
            e.set("dir", floatarr_to_str(self.dir))

        # Colors and appearance
        if self.diffuse is not None:
            e.set("diffuse", floatarr_to_str(self.diffuse))
        if self.ambient is not None:
            e.set("ambient", floatarr_to_str(self.ambient))
        if self.specular is not None:
            e.set("specular", floatarr_to_str(self.specular))

        # Image-based lighting
        if self.texture is not None:
            e.set("texture", str(self.texture))
        if self.intensity is not None:
            e.set("intensity", str(float(self.intensity)))

        # Spotlight and attenuation parameters
        if self.range is not None:
            e.set("range", str(float(self.range)))
        if self.bulbradius is not None:
            e.set("bulbradius", str(float(self.bulbradius)))
        if self.attenuation is not None:
            e.set("attenuation", floatarr_to_str(self.attenuation))
        if self.cutoff is not None:
            e.set("cutoff", str(float(self.cutoff)))
        if self.exponent is not None:
            e.set("exponent", str(float(self.exponent)))

        return e

    def remove_duplicate_assets(self, existing: dict[int, Asset]) -> None:
        pass  # Light does not reference any assets