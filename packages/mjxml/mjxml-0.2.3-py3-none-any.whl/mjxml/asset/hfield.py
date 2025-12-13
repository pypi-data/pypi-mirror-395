from xml.etree.ElementTree import Element
from pydantic.functional_validators import field_validator
from mjxml.typeutils import ArrayLike, StrictNatural, compare, floatarr_to_str, floatarr_to_tuple
from typing import Literal, Any, SupportsFloat
from .asset import Asset

__all__ = ["HFieldAsset"]

_CONTENT_TYPE = Literal["image/png", "image/vnd.mujoco.hfield"]


class HFieldAsset(Asset):
    """MuJoCo height field asset element.

    Creates a height field asset that can be referenced from geoms with type "hfield".
    A height field is a 2D matrix of elevation data that can be loaded from PNG files,
    binary files, or defined programmatically.
    """

    content_type: _CONTENT_TYPE | None = None
    nrow: StrictNatural | None = None
    ncol: StrictNatural | None = None
    elevation: ArrayLike[SupportsFloat] | None = None
    size: ArrayLike[
        SupportsFloat, Literal[4]
    ]  # Required: (radius_x, radius_y, elevation_z, base_z)

    @field_validator("nrow", "ncol")
    def validate_dimensions(cls, v: StrictNatural | None, info) -> StrictNatural | None:
        if v is None:
            return v
        val = int(v)
        if val < 0:
            raise ValueError(f"{info.field_name} must be non-negative")
        return v

    def _prevent_instantiation(self):
        pass

    def to_xml(self) -> Element:
        e = Element("hfield")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)

        if self.content_type is not None:
            e.set("content_type", self.content_type)
        if int(self.nrow) != 0:
            e.set("nrow", str(int(self.nrow)))
        if int(self.ncol) != 0:
            e.set("ncol", str(int(self.ncol)))
        if self.elevation is not None:
            e.set("elevation", floatarr_to_str(self.elevation))
        # size is required
        e.set("size", floatarr_to_str(self.size))

        return e

    def attribute_equality(self, other: Any) -> bool:
        """Check equality based on all height field attributes."""
        if not isinstance(other, HFieldAsset):
            return False

        return (
            self.file == other.file  # Ignore name to detect duplicates
            and self.clazz == other.clazz
            and self.content_type == other.content_type
            and self.nrow == other.nrow
            and self.ncol == other.ncol
            and compare(self.elevation, other.elevation)
            and self.size == other.size
        )

    def attribute_hash(self) -> int:
        """Generate hash based on height field attributes."""
        # Convert mutable types to immutable for hashing
        elevation_tuple = floatarr_to_tuple(self.elevation)
        size_tuple = floatarr_to_tuple(self.size)

        return hash(
            (
                self.file,
                self.clazz,
                self.content_type,
                int(self.nrow),
                int(self.ncol),
                elevation_tuple,
                size_tuple,
            )
        )
