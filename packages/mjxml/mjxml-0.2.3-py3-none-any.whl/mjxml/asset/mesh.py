from pydantic.fields import Field
from .material import MaterialAsset
from xml.etree.ElementTree import Element
from pydantic.functional_validators import field_validator
from mjxml.typeutils import ArrayLike, SupportsBool, compare, floatarr_to_str, floatarr_to_tuple, intarr_to_tuple, intarr_to_str
from typing import Literal, Any, SupportsFloat, SupportsInt
from .asset import Asset

__all__ = ["MeshAsset"]

_CONTENT_TYPE = Literal["model/vnd.mujoco.msh", "model/obj", "model/stl"]
_INERTIA_TYPE = Literal["convex", "exact", "legacy", "shell"]
_BUILTIN_TYPE = Literal[
    "sphere", "plane", "cube", "cylinder", "capsule", "ellipsoid", "box"
]


class MeshAsset(Asset):
    """MuJoCo mesh asset element.

    Creates a mesh asset that can be referenced from geoms. Meshes can be loaded
    from binary STL, OBJ, or MSH files, or defined directly via vertex data.
    """

    content_type: _CONTENT_TYPE | None = None
    scale: ArrayLike[SupportsFloat, Literal[3]] | None = None
    inertia: _INERTIA_TYPE = Field(default="exact")
    smoothnormal: SupportsBool | None = None
    maxhullvert: SupportsInt | None = None
    vertex: ArrayLike[SupportsFloat] | None = None
    normal: ArrayLike[SupportsFloat] | None = None
    texcoord: ArrayLike[SupportsFloat] | None = None
    face: ArrayLike[SupportsInt] | None = None
    refpos: ArrayLike[SupportsFloat, Literal[3]] | None = None
    refquat: ArrayLike[SupportsFloat, Literal[4]] | None = None
    builtin: _BUILTIN_TYPE | None = None
    params: ArrayLike[SupportsFloat] | None = None
    material: MaterialAsset | None = None

    @field_validator("maxhullvert")
    def validate_maxhullvert(cls, v: SupportsInt | None) -> SupportsInt | None:
        if v is not None and int(v) <= 2 and v != -1:
            raise ValueError("maxhullvert must be >= 3, or -1")
        return v

    def to_xml(self) -> Element:
        e = Element("mesh")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)
        if self.content_type is not None:
            e.set("content_type", self.content_type)
        if self.scale is not None:
            e.set("scale", " ".join([str(v) for v in self.scale]))
        if self.inertia is not None:
            e.set("inertia", self.inertia)
        if self.smoothnormal is not None:
            e.set("smoothnormal", str(int(self.smoothnormal)))
        if self.maxhullvert is not None:
            e.set("maxhullvert", str(self.maxhullvert))
        if self.vertex is not None:
            e.set("vertex", floatarr_to_str(self.vertex))
        if self.normal is not None:
            e.set("normal", floatarr_to_str(self.normal))
        if self.texcoord is not None:
            e.set("texcoord", floatarr_to_str(self.texcoord))
        if self.face is not None:
            e.set("face", intarr_to_str(self.face))
        if self.refpos is not None:
            e.set("refpos", floatarr_to_str(self.refpos))
        if self.refquat is not None:
            e.set("refquat", floatarr_to_str(self.refquat))
        if self.builtin is not None:
            e.set("builtin", self.builtin)
        if self.params is not None:
            e.set("params", floatarr_to_str(self.params))
        if self.material is not None:
            e.set("material", str(self.material.mjc_name))
        return e

    def attribute_equality(self, other: Any) -> bool:
        """Check equality based on all mesh attributes."""
        if not isinstance(other, MeshAsset):
            return False

        def mat_equal(left: MaterialAsset | None, right: MaterialAsset | None) -> bool:
            if left is right:
                return True
            if left is None or right is None:
                return False
            return left.attribute_equality(right)

        return (
            self.file == other.file  # We ignore name so to detect duplicate meshes
            and self.clazz == other.clazz
            and self.content_type == other.content_type
            and compare(self.scale, other.scale)
            and self.inertia == other.inertia
            and self.smoothnormal == other.smoothnormal
            and self.maxhullvert == other.maxhullvert
            and compare(self.vertex, other.vertex)
            and compare(self.normal, other.normal)
            and compare(self.texcoord, other.texcoord)
            and compare(self.face, other.face)
            and compare(self.refpos, other.refpos)
            and compare(self.refquat, other.refquat)
            and self.builtin == other.builtin
            and compare(self.params, other.params)
            and mat_equal(self.material, other.material)
        )

    def attribute_hash(self) -> int:
        """Generate hash based on mesh attributes."""
        # Convert mutable types to immutable for hashing
        vertex_tuple = floatarr_to_tuple(self.vertex)
        normal_tuple = floatarr_to_tuple(self.normal)
        texcoord_tuple = floatarr_to_tuple(self.texcoord)
        face_tuple = intarr_to_tuple(self.face)
        params_tuple = floatarr_to_tuple(self.params)
        refpos_tuple = floatarr_to_tuple(self.refpos)
        refquat_tuple = floatarr_to_tuple(self.refquat)
        scale_tuple = floatarr_to_tuple(self.scale)
        return hash(
            (
                self.file,
                self.clazz,
                self.content_type,
                scale_tuple,
                self.inertia,
                self.smoothnormal,
                self.maxhullvert,
                vertex_tuple,
                normal_tuple,
                texcoord_tuple,
                face_tuple,
                refpos_tuple,
                refquat_tuple,
                self.builtin,
                params_tuple,
                self.material.attribute_hash() if self.material is not None else None,
            )
        )
