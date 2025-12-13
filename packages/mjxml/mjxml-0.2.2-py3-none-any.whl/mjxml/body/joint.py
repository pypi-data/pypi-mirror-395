from mjxml.asset import Asset
from .worldbodychildren import BodyChildren
from xml.etree.ElementTree import Element
from typing import Literal, SupportsFloat
from mjxml.typeutils import ArrayLike, PosFloat, SupportsBool, floatarr_to_str
import warnings

__all__ = ["Joint"]

_JOINT_TYPE = Literal["free", "ball", "slide", "hinge"]
_LIMITED_TYPE = Literal["false", "true", "auto"]


class Joint(BodyChildren):
    """MuJoCo joint element.

    Creates a joint that creates motion degrees of freedom between the body where it is
    defined and the body's parent.
    """

    type: _JOINT_TYPE | None = None
    group: int | None = None
    pos: ArrayLike[SupportsFloat, Literal[3]] | None = None
    axis: ArrayLike[SupportsFloat, Literal[3]] | None = None
    springdamper: ArrayLike[SupportsFloat, Literal[2]] | None = None
    solreflimit: ArrayLike[SupportsFloat, Literal[2]] | None = None
    solimplimit: ArrayLike[SupportsFloat, Literal[3]] | None = None
    solreffriction: ArrayLike[SupportsFloat, Literal[2]] | None = None
    solimpfriction: ArrayLike[SupportsFloat, Literal[3]] | None = None
    stiffness: PosFloat | None = None
    range: ArrayLike[SupportsFloat, Literal[2]] | None = None
    limited: _LIMITED_TYPE | None = None
    actuatorfrcrange: ArrayLike[SupportsFloat, Literal[2]] | None = None
    actuatorfrclimited: _LIMITED_TYPE | None = None
    actuatorgravcomp: SupportsBool | None = None
    margin: SupportsFloat | None = None
    ref: SupportsFloat | None = None
    springref: SupportsFloat | None = None
    armature: SupportsFloat | None = None
    damping: PosFloat | None = None
    frictionloss: PosFloat | None = None
    user_params: ArrayLike[SupportsFloat] | None = None

    def to_xml(self) -> Element:
        e = Element("joint")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        if self.type == "free":
            if self.pos is not None:
                warnings.warn("pos is ignored for free joints")
            if self.range is not None or self.limited is not None:
                warnings.warn("limits are not allowed for free joints")
            if self.axis is not None:
                warnings.warn("axis is ignored for free joints")

        if self.type == "ball":
            if self.axis is not None:
                warnings.warn("axis is ignored for ball joints")

        e = super()._process(e)

        if self.type is not None:
            e.set("type", self.type)
        if self.group is not None:
            e.set("group", str(self.group))
        if self.pos is not None and self.type != "free":
            e.set("pos", floatarr_to_str(self.pos))
        if self.axis is not None and self.type not in ("free", "ball"):
            e.set("axis", floatarr_to_str(self.axis))
        if self.springdamper is not None:
            e.set("springdamper", floatarr_to_str(self.springdamper))
        if self.solreflimit is not None:
            e.set("solreflimit", floatarr_to_str(self.solreflimit))
        if self.solimplimit is not None:
            e.set("solimplimit", floatarr_to_str(self.solimplimit))
        if self.solreffriction is not None:
            e.set(
                "solreffriction",
                floatarr_to_str(self.solreffriction),
            )
        if self.solimpfriction is not None:
            e.set(
                "solimpfriction", floatarr_to_str(self.solimpfriction)
            )
        if self.stiffness is not None:
            e.set("stiffness", str(float(self.stiffness)))
        if self.range is not None and self.type != "free":
            e.set("range", floatarr_to_str(self.range))
        if self.limited is not None:
            e.set("limited", self.limited)
        if self.actuatorfrcrange is not None:
            e.set(
                "actuatorfrcrange",
                floatarr_to_str(self.actuatorfrcrange),
            )
        if self.actuatorfrclimited is not None:
            e.set("actuatorfrclimited", self.actuatorfrclimited)
        if self.actuatorgravcomp is not None:
            e.set("actuatorgravcomp", str(bool(self.actuatorgravcomp)).lower())
        if self.margin is not None:
            e.set("margin", str(float(self.margin)))
        if self.ref is not None:
            e.set("ref", str(float(self.ref)))
        if self.springref is not None:
            e.set("springref", str(float(self.springref)))
        if self.armature is not None:
            e.set("armature", str(float(self.armature)))
        if self.damping is not None:
            e.set("damping", str(float(self.damping)))
        if self.frictionloss is not None:
            e.set("frictionloss", str(float(self.frictionloss)))
        if self.user_params is not None:
            e.set("user", floatarr_to_str(self.user_params))

        return e

    def remove_duplicate_assets(self, existing: dict[int, Asset]) -> None:
        pass  # Joint does not reference any assets