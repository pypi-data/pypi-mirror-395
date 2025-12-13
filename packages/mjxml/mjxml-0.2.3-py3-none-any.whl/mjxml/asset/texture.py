from xml.etree.ElementTree import Element
from pydantic.functional_validators import field_validator
from mjxml.typeutils import ArrayLike, Str, StrictNatural, PosFloat, SupportsBool, compare, floatarr_to_str, intarr_to_str, floatarr_to_tuple, intarr_to_tuple
from typing import Literal, Any, SupportsFloat, SupportsInt
from .asset import Asset

__all__ = ["TextureAsset"]

_TYPE = Literal["2d", "cube", "skybox"]
_COLORSPACE = Literal["auto", "linear", "srgb"]
_CONTENT_TYPE = Literal["image/png", "image/ktx", "image/vnd.mujoco.texture"]
_BUILTIN_TYPE = Literal["none", "gradient", "checker", "flat"]
_MARK_TYPE = Literal["none", "edge", "cross", "random"]


class TextureAsset(Asset):
    """MuJoCo texture asset element.

    Creates a texture asset that can be referenced from materials. Textures can be loaded
    from PNG, KTX, or custom MuJoCo format files, or generated procedurally.
    """

    type: _TYPE | None = None
    colorspace: _COLORSPACE | None = None
    content_type: _CONTENT_TYPE | None = None
    gridsize: ArrayLike[SupportsInt, Literal[2]] | None = None
    gridlayout: Str | None = None
    fileright: Str | None = None
    fileleft: Str | None = None
    fileup: Str | None = None
    filedown: Str | None = None
    filefront: Str | None = None
    fileback: Str | None = None
    builtin: _BUILTIN_TYPE = "none"
    rgb1: ArrayLike[SupportsFloat, Literal[3]] | None = None
    rgb2: ArrayLike[SupportsFloat, Literal[3]] | None = None
    mark: _MARK_TYPE = "none"
    markrgb: ArrayLike[SupportsFloat, Literal[3]] | None = None
    random: PosFloat | None = None
    width: StrictNatural | None = None
    height: StrictNatural | None = None
    hflip: SupportsBool | None = None
    vflip: SupportsBool | None = None
    nchannel: StrictNatural | None = None

    @field_validator("nchannel")
    def validate_nchannel(cls, v: StrictNatural | None, info) -> StrictNatural | None:
        if v is not None and (int(v) > 4 or int(v) == 2):
            raise ValueError(f"{info.field_name} must be 1, 3, or 4")
        return v

    @field_validator("random")
    def validate_random(cls, v: PosFloat | None) -> PosFloat | None:
        if v is not None:
            val = float(v)
            if val < 0 or val > 1:
                raise ValueError("random must be between 0 and 1")
        return v

    def to_xml(self) -> Element:
        e = Element("texture")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)

        if self.type is not None:
            e.set("type", self.type)
        if self.colorspace is not None:
            e.set("colorspace", self.colorspace)
        if self.content_type is not None:
            e.set("content_type", self.content_type)
        if self.gridsize is not None:
            e.set("gridsize", intarr_to_str(self.gridsize))
        if self.gridlayout is not None:
            e.set("gridlayout", str(self.gridlayout))
        if self.fileright is not None:
            e.set("fileright", str(self.fileright))
        if self.fileleft is not None:
            e.set("fileleft", str(self.fileleft))
        if self.fileup is not None:
            e.set("fileup", str(self.fileup))
        if self.filedown is not None:
            e.set("filedown", str(self.filedown))
        if self.filefront is not None:
            e.set("filefront", str(self.filefront))
        if self.fileback is not None:
            e.set("fileback", str(self.fileback))
        if self.builtin is not None:
            e.set("builtin", self.builtin)
        if self.rgb1 is not None:
            e.set("rgb1", floatarr_to_str(self.rgb1))
        if self.rgb2 is not None:
            e.set("rgb2", floatarr_to_str(self.rgb2))
        if self.mark is not None:
            e.set("mark", self.mark)
        if self.markrgb is not None:
            e.set("markrgb", floatarr_to_str(self.markrgb))
        if self.random is not None:
            e.set("random", str(self.random))
        if self.width is not None:
            e.set("width", str(self.width))
        if self.height is not None:
            e.set("height", str(self.height))
        if self.hflip is not None:
            e.set("hflip", str(int(self.hflip)))
        if self.vflip is not None:
            e.set("vflip", str(int(self.vflip)))
        if self.nchannel is not None:
            e.set("nchannel", str(self.nchannel))

        return e

    def attribute_equality(self, other: Any) -> bool:
        """Check equality based on all texture attributes."""
        if not isinstance(other, TextureAsset):
            return False

        return (
            self.file == other.file  # Ignore name to detect duplicates
            and self.clazz == other.clazz
            and self.type == other.type
            and self.colorspace == other.colorspace
            and self.content_type == other.content_type
            and compare(self.gridsize, other.gridsize)
            and self.gridlayout == other.gridlayout
            and self.fileright == other.fileright
            and self.fileleft == other.fileleft
            and self.fileup == other.fileup
            and self.filedown == other.filedown
            and self.filefront == other.filefront
            and self.fileback == other.fileback
            and self.builtin == other.builtin
            and compare(self.rgb1, other.rgb1)
            and compare(self.rgb2, other.rgb2)
            and self.mark == other.mark
            and compare(self.markrgb, other.markrgb)
            and self.random == other.random
            and self.width == other.width
            and self.height == other.height
            and self.hflip == other.hflip
            and self.vflip == other.vflip
            and self.nchannel == other.nchannel
        )

    def attribute_hash(self) -> int:
        """Generate hash based on texture attributes."""
        # Convert mutable types to immutable for hashing
        gridsize_tuple = intarr_to_tuple(self.gridsize)
        rgb1_tuple = floatarr_to_tuple(self.rgb1)
        rgb2_tuple = floatarr_to_tuple(self.rgb2)
        markrgb_tuple = floatarr_to_tuple(self.markrgb)

        return hash(
            (
                self.file,
                self.clazz,
                self.type,
                self.colorspace,
                self.content_type,
                gridsize_tuple,
                self.gridlayout,
                self.fileright,
                self.fileleft,
                self.fileup,
                self.filedown,
                self.filefront,
                self.fileback,
                self.builtin,
                rgb1_tuple,
                rgb2_tuple,
                self.mark,
                markrgb_tuple,
                self.random,
                self.width,
                self.height,
                self.hflip,
                self.vflip,
                self.nchannel,
            )
        )
