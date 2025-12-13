from typing import Literal, SupportsFloat
from xml.etree.ElementTree import Element

from mjxml.body import Body, Site
from mjxml.typeutils import ArrayLike, floatarr_to_str

from .equality import Equality

__all__ = ["WeldEquality"]


class WeldEquality(Equality):
    """Weld constraint tying two bodies or sites together."""

    body1: Body | None = None
    body2: Body | None = None
    relpos: ArrayLike[SupportsFloat, Literal[3]] | None = None
    relquat: ArrayLike[SupportsFloat, Literal[4]] | None = None
    anchor: ArrayLike[SupportsFloat, Literal[3]] | None = None

    site1: Site | None = None
    site2: Site | None = None
    torquescale: SupportsFloat | None = None

    def to_xml(self) -> Element:
        e = Element("weld")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)

        body_specified = any(
            [self.body1, self.body2, self.anchor, self.relpos, self.relquat]
        )
        site_specified = any([self.site1, self.site2])

        if body_specified and site_specified:
            raise ValueError("WeldEquality must use either bodies or sites, not both")
        if not body_specified and not site_specified:
            raise ValueError("WeldEquality requires body parameters or two sites")

        if body_specified:
            if self.body1 is None:
                raise ValueError("body1 must be provided for body-based welds")
            if self.body1.name is None:
                raise ValueError("body1 must have a name for WeldEquality serialization")
            e.set("body1", str(self.body1.name))

            if self.body2 is not None:
                if self.body2.name is None:
                    raise ValueError("body2 must have a name when provided for welds")
                if str(self.body1.name) == str(self.body2.name):
                    raise ValueError("body1 and body2 must refer to different Body objects")
                e.set("body2", str(self.body2.name))

            relpos_values: list[SupportsFloat] | None = None
            relquat_values: list[SupportsFloat] | None = None

            if self.relpos is not None:
                relpos_values = list(self.relpos)
                if len(relpos_values) != 3:
                    raise ValueError("relpos must contain 3 values")
            if self.relquat is not None:
                relquat_values = list(self.relquat)
                if len(relquat_values) != 4:
                    raise ValueError("relquat must contain 4 values")

            if relpos_values is not None or relquat_values is not None:
                base_pos = relpos_values if relpos_values is not None else [0.0, 0.0, 0.0]
                base_quat = (
                    relquat_values if relquat_values is not None else [1.0, 0.0, 0.0, 0.0]
                )
                relpose = list(base_pos) + list(base_quat)
                e.set("relpose", floatarr_to_str(relpose))

            if self.anchor is not None:
                e.set("anchor", floatarr_to_str(self.anchor))

            if self.torquescale is not None:
                e.set("torquescale", str(float(self.torquescale)))

            return e

        # Site specification path
        assert site_specified
        if self.site1 is None or self.site2 is None:
            raise ValueError("Both site1 and site2 must be provided for site welds")
        if self.site1.name is None or self.site2.name is None:
            raise ValueError("Both site1 and site2 must have names for WeldEquality")
        if self.site1 is self.site2:
            raise ValueError("site1 and site2 must refer to distinct Site objects")
        if str(self.site1.name) == str(self.site2.name):
            raise ValueError("site1 and site2 must refer to different Site objects")

        e.set("site1", str(self.site1.name))
        e.set("site2", str(self.site2.name))

        if self.torquescale is not None:
            e.set("torquescale", str(float(self.torquescale)))

        return e
