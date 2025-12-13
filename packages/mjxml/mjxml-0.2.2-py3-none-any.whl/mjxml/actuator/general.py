from mjxml.body import Site, Joint
from mjxml.commons import MJCElement
from mjxml.typeutils import ArrayLike, SupportsBool, PosFloat, floatarr_to_str
from typing import SupportsFloat, Literal, SupportsInt
from xml.etree.ElementTree import Element

__all__ = ["Actuator"]

_DYN_TYPE = Literal["none", "integrator", "filter", "filterexact", "muscle", "user"]
_GAIN_TYPE = Literal["fixed", "affine", "muscle", "user"]
_BIAS_TYPE = Literal["none", "affine", "muscle", "user"]

# TODO: Add aliases for motor and stuff
class Actuator(MJCElement):
    """MuJoCo general actuator element."""

    # Common actuator attributes
    group: SupportsInt | None = None
    ctrllimited: SupportsBool | None = None
    forcelimited: SupportsBool | None = None
    actlimited: SupportsBool | None = None

    ctrlrange: ArrayLike[SupportsFloat, Literal[2]] | None = None
    forcerange: ArrayLike[SupportsFloat, Literal[2]] | None = None
    actrange: ArrayLike[SupportsFloat, Literal[2]] | None = None
    lengthrange: ArrayLike[SupportsFloat, Literal[2]] | None = None

    gear: ArrayLike[SupportsFloat, Literal[1, 2, 3, 4, 5, 6]] | None = None
    cranklength: PosFloat | None = None

    # Transmission references
    joint: Joint | None = None
    jointinparent: Joint | None = None
    site: Site | None = None
    refsite: Site | None = None
    body: Site | None = None
    # TODO: Implement tendons and come back to this
    tendon: None = None
    cranksite: Site | None = None
    slidersite: Site | None = None

    # Dynamics / gain settings
    actdim: SupportsFloat | None = None
    dyntype: _DYN_TYPE | None = None
    gaintype: _GAIN_TYPE | None = None
    biastype: _BIAS_TYPE | None = None

    dynprm: ArrayLike[SupportsFloat] | None = None
    gainprm: ArrayLike[SupportsFloat] | None = None
    biasprm: ArrayLike[SupportsFloat] | None = None

    actearly: SupportsBool | None = None
    user_params: ArrayLike[SupportsFloat] | None = None

    def to_xml(self) -> Element:
        e = Element("general")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)

        if self.group not in (None, 0):
            e.set("group", str(int(self.group)))

        if self.ctrllimited is not None:
            e.set("ctrllimited", str(bool(self.ctrllimited)).lower())
        if self.forcelimited is not None:
            e.set("forcelimited", str(bool(self.forcelimited)).lower())
        if self.actlimited is not None:
            e.set("actlimited", str(bool(self.actlimited)).lower())

        if self.ctrlrange is not None:
            e.set("ctrlrange", floatarr_to_str(self.ctrlrange))
        if self.forcerange is not None:
            e.set("forcerange", floatarr_to_str(self.forcerange))
        if self.actrange is not None:
            e.set("actrange", floatarr_to_str(self.actrange))
        if self.lengthrange is not None:
            e.set("lengthrange", floatarr_to_str(self.lengthrange))

        if self.gear is not None:
            e.set("gear", floatarr_to_str(self.gear))
        if self.cranklength is not None:
            e.set("cranklength", str(float(self.cranklength)))

        if self.joint is not None:
            e.set("joint", str(self.joint.name))
        if self.jointinparent is not None:
            e.set("jointinparent", str(self.jointinparent.name))
        if self.site is not None:
            e.set("site", str(self.site.name))
        if self.refsite is not None:
            e.set("refsite", str(self.refsite.name))
        if self.body is not None:
            e.set("body", str(self.body.name))
        if self.tendon is not None:
            e.set("tendon", str(self.tendon))
        if self.cranksite is not None:
            e.set("cranksite", str(self.cranksite.name))
        if self.slidersite is not None:
            e.set("slidersite", str(self.slidersite.name))

        if self.actdim is not None:
            e.set("actdim", str(float(self.actdim)))
        if self.dyntype is not None:
            e.set("dyntype", self.dyntype)
        if self.gaintype is not None:
            e.set("gaintype", self.gaintype)
        if self.biastype is not None:
            e.set("biastype", self.biastype)

        if self.dynprm is not None:
            e.set("dynprm", floatarr_to_str(self.dynprm))
        if self.gainprm is not None:
            e.set("gainprm", floatarr_to_str(self.gainprm))
        if self.biasprm is not None:
            e.set("biasprm", floatarr_to_str(self.biasprm))

        if self.actearly is not None:
            e.set("actearly", str(bool(self.actearly)).lower())
        if self.user_params is not None:
            e.set("user", floatarr_to_str(self.user_params))

        return e