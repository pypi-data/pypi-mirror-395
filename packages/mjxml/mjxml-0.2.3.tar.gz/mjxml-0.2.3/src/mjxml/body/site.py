from mjxml.asset import Asset, MaterialAsset
from .worldbodychildren import BodyChildren
from mjxml.rotations import RotationType, to_mjc
from xml.etree.ElementTree import Element
from typing import SupportsFloat, Literal, SupportsInt, cast
from mjxml.typeutils import ArrayLike, floatarr_to_str

__all__ = ["Site"]

_SITE_TYPE = Literal[
    "sphere",
    "capsule",
    "ellipsoid",
    "cylinder",
    "box",
]


class Site(BodyChildren):
    """MuJoCo site element.

    Creates a site, which is a location of interest relative to a body. Sites are
    used for sensors, attachment points, and visualization.
    """

    # Basic attributes
    type: _SITE_TYPE | None = None
    group: SupportsInt | None = None

    # Appearance
    material: MaterialAsset | None = None
    rgba: ArrayLike[SupportsFloat, Literal[4]] | None = None

    # Size
    size: ArrayLike[SupportsFloat, Literal[1, 2, 3]] | None = None

    # Position and orientation
    fromto: ArrayLike[SupportsFloat, Literal[6]] | None = None
    pos: ArrayLike[SupportsFloat, Literal[3]] | None = None
    rotation: RotationType | None = None

    # User parameters
    user_params: ArrayLike[SupportsFloat] | None = None

    def to_xml(self) -> Element:
        e = Element("site")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)

        # Basic attributes
        if self.type is not None:
            e.set("type", self.type)
        if self.group is not None:
            e.set("group", str(int(self.group)))

        # Appearance
        if self.material is not None:
            e.set("material", str(self.material.mjc_name))
        if self.rgba is not None:
            e.set("rgba", floatarr_to_str(self.rgba))

        # Size
        if self.size is not None:
            e.set("size", floatarr_to_str(self.size))

        # Position and orientation
        if self.fromto is not None:
            e.set("fromto", floatarr_to_str(self.fromto))
        else:
            if self.pos is not None:
                e.set("pos", floatarr_to_str(self.pos))
            if self.rotation is not None:
                e.set(*to_mjc(self.rotation))

        if self.user_params is not None:
            e.set("user", floatarr_to_str(self.user_params))

        return e

    def remove_duplicate_assets(self, existing: dict[int, Asset]) -> None:
        if self.material is not None:
            mathash = self.material.attribute_hash()
            if mathash in existing:
                self.material = cast(MaterialAsset, existing[mathash])
            else:
                existing[mathash] = self.material