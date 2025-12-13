from xml.etree.ElementTree import Element
from pydantic.functional_validators import field_validator
from mjxml.typeutils import ArrayLike, PosFloat, SupportsBool, compare, floatarr_to_str, floatarr_to_tuple
from typing import Literal, Any, SupportsFloat
from .asset import Asset
from .texture import TextureAsset

__all__ = ["MaterialAsset"]


class MaterialAsset(Asset):
    """MuJoCo material asset element.

    Creates a material asset that can be referenced from skins, geoms, sites and tendons
    to set their appearance properties beyond just color.
    """

    texture: TextureAsset | None = None
    texrepeat: ArrayLike[SupportsFloat, Literal[2]] | None = None
    texuniform: SupportsBool | None = None
    emission: PosFloat | None = None
    specular: PosFloat | None = None
    shininess: PosFloat | None = None
    reflectance: PosFloat | None = None
    metallic: SupportsFloat | None = None
    roughness: SupportsFloat | None = None
    rgba: ArrayLike[SupportsFloat, Literal[4]] | None = None

    @field_validator("specular", "shininess", "reflectance")
    def validate_unit_range(cls, v: PosFloat | None, info) -> PosFloat | None:
        if v is None:
            return v
        val = float(v)
        if val < 0 or val > 1:
            raise ValueError(f"{info.field_name} must be between 0 and 1")
        return v

    def to_xml(self) -> Element:
        e = Element("material")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)

        if self.texture is not None:
            e.set("texture", str(self.texture.mjc_name))
        if self.texrepeat is not None:
            e.set("texrepeat", floatarr_to_str(self.texrepeat))
        if self.texuniform is not None:
            e.set("texuniform", str(int(self.texuniform)))
        if self.emission is not None:
            e.set("emission", str(float(self.emission)))
        if self.specular is not None:
            e.set("specular", str(float(self.specular)))
        if self.shininess is not None:
            e.set("shininess", str(float(self.shininess)))
        if self.reflectance is not None:
            e.set("reflectance", str(float(self.reflectance)))
        if self.metallic is not None:
            e.set("metallic", str(float(self.metallic)))
        if self.roughness is not None:
            e.set("roughness", str(float(self.roughness)))
        if self.rgba is not None:
            e.set("rgba", floatarr_to_str(self.rgba))

        return e

    def attribute_equality(self, other: Any) -> bool:
        """Check equality based on all material attributes."""
        if not isinstance(other, MaterialAsset):
            return False

        def textures_equal(left: TextureAsset | None, right: TextureAsset | None) -> bool:
            if left is right:
                return True
            if left is None or right is None:
                return left is None and right is None
            return left.attribute_equality(right)

        return (
            self.file == other.file  # Ignore name to detect duplicates
            and self.clazz == other.clazz
            and textures_equal(self.texture, other.texture)
            and compare(self.texrepeat, other.texrepeat)
            and self.texuniform == other.texuniform
            and self.emission == other.emission
            and self.specular == other.specular
            and self.shininess == other.shininess
            and self.reflectance == other.reflectance
            and self.metallic == other.metallic
            and self.roughness == other.roughness
            and compare(self.rgba, other.rgba)
        )

    def __hash__(self) -> int:
        """Generate hash including name."""
        texname = str(self.texture.name) if self.texture is not None else None
        return hash((str(self.name), texname, self.attribute_hash()))

    def attribute_hash(self) -> int:
        """Generate hash based on material attributes."""
        # Convert mutable types to immutable for hashing
        texrepeat_tuple = floatarr_to_tuple(self.texrepeat)
        rgba_tuple = floatarr_to_tuple(self.rgba)

        return hash(
            (
                self.file,
                self.clazz,
                self.texture.attribute_hash() if self.texture is not None else None,
                texrepeat_tuple,
                self.texuniform,
                self.emission,
                self.specular,
                self.shininess,
                self.reflectance,
                self.metallic,
                self.roughness,
                rgba_tuple,
            )
        )
