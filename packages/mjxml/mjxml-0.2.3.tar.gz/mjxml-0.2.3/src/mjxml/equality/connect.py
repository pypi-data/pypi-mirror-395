from typing import Literal, SupportsFloat
from xml.etree.ElementTree import Element

from mjxml.body import Body, Site
from mjxml.typeutils import ArrayLike, floatarr_to_str

from .equality import Equality

__all__ = ["ConnectEquality"]


class ConnectEquality(Equality):
    """Equality constraint that connects two bodies or sites at a point."""

    body1: Body | None = None
    body2: Body | None = None
    anchor: ArrayLike[SupportsFloat, Literal[3]] | None = None

    site1: Site | None = None
    site2: Site | None = None

    def to_xml(self) -> Element:
        e = Element("connect")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)

        body_specified = any([self.body1, self.body2, self.anchor])
        site_specified = any([self.site1, self.site2])

        if body_specified and site_specified:
            raise ValueError(
                "ConnectEquality must be specified using either bodies or sites, not both"
            )
        if not body_specified and not site_specified:
            raise ValueError(
                "ConnectEquality requires body/anchor parameters or two sites"
            )

        if body_specified:
            if self.body1 is None:
                raise ValueError("body1 must be provided when using body anchors")
            if self.body1.name is None:
                raise ValueError("body1 must have a name for ConnectEquality serialization")
            if self.anchor is None:
                raise ValueError("anchor must be provided when using body anchors")

            e.set("body1", str(self.body1.name))
            e.set("anchor", floatarr_to_str(self.anchor))

            if self.body2 is not None:
                if self.body2.name is None:
                    raise ValueError(
                        "body2 must have a name when provided for ConnectEquality"
                    )
                if str(self.body1.name) == str(self.body2.name):
                    raise ValueError("body1 and body2 must refer to different Body objects")
                e.set("body2", str(self.body2.name))
            return e

        # Site specification path
        assert site_specified  # For type-checkers; already validated above.
        if self.site1 is None or self.site2 is None:
            raise ValueError("Both site1 and site2 must be provided when using sites")
        if self.site1.name is None or self.site2.name is None:
            raise ValueError("Both site1 and site2 must have names for ConnectEquality")
        if self.site1 is self.site2:
            raise ValueError("site1 and site2 must refer to different Site objects")

        e.set("site1", str(self.site1.name))
        e.set("site2", str(self.site2.name))
        return e
