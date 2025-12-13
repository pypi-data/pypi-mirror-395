from mjxml.asset.texture import TextureAsset
from mjxml.asset import Asset, MaterialAsset, HFieldAsset, MeshAsset
from .worldbodychildren import BodyChildren
from mjxml.rotations import RotationType, to_mjc
from xml.etree.ElementTree import Element
from typing import SupportsFloat, Literal, SupportsInt, cast, Mapping
from mjxml.typeutils import SupportsBool, ArrayLike, PosFloat, floatarr_to_str
import warnings

__all__ = ["Geom"]

_GEOM_TYPE = Literal[
    "plane",
    "hfield",
    "sphere",
    "capsule",
    "ellipsoid",
    "cylinder",
    "box",
    "mesh",
    "sdf",
]
_FLUID_SHAPE = Literal["none", "ellipsoid"]


class Geom(BodyChildren):
    """MuJoCo geom element.

    Creates a geom attached rigidly to a body. Geoms determine appearance, collision,
    and can contribute to inertial properties at compile time.
    """

    # Basic attributes
    type: _GEOM_TYPE | None = None

    # Contact filtering
    contype: SupportsInt | None = None
    conaffinity: SupportsInt | None = None

    # Organization
    group: SupportsInt | None = None
    priority: SupportsInt | None = None

    # Size and shape
    size: ArrayLike[SupportsFloat, Literal[1, 2, 3]] | None = None

    # Appearance
    material: MaterialAsset | None = None
    rgba: ArrayLike[SupportsFloat, Literal[4]] | None = None

    # Physics properties
    condim: SupportsInt | None = None
    friction: ArrayLike[SupportsFloat, Literal[1, 2, 3]] | None = None
    mass: PosFloat | None = None
    density: PosFloat | None = None
    shellinertia: SupportsBool | None = None

    # Solver parameters
    solmix: PosFloat | None = None
    solref: ArrayLike[SupportsFloat] | None = None
    solimp: ArrayLike[SupportsFloat] | None = None
    margin: SupportsFloat | None = None
    gap: SupportsFloat | None = None

    # Position and orientation
    fromto: ArrayLike[SupportsFloat, Literal[6]] | None = None
    pos: ArrayLike[SupportsFloat, Literal[3]] | None = None
    rotation: RotationType | None = None

    # Asset references
    hfield: HFieldAsset | None = None
    mesh: MeshAsset | None = None
    fitscale: PosFloat | None = None

    # Fluid interaction
    fluidshape: _FLUID_SHAPE | None = None
    fluidcoef: ArrayLike[SupportsFloat, Literal[5]] | None = None

    # User parameters
    user_params: ArrayLike[SupportsFloat] | None = None

    def to_xml(self) -> Element:
        e = Element("geom")
        e = self._process(e)
        return e

    def _produce_type_size_error(self):
        type = self.type if self.type else "sphere"
        size_len = len(self.size) if self.size is not None else 3
        accepted = {  # name, min length
            "plane": 2,
            "hfield": 0,
            "sphere": 1,
            "capsule": 1,
            "ellipsoid": 3,
            "cylinder": 1,
            "box": 3,
            "mesh": 0,
        }
        if size_len < accepted[type]:
            raise ValueError(
                f"Geom of type '{type}' with size length {size_len} is invalid. "
                f"Accepted size lengths for this type must be at least {accepted[type]}."
            )

    def _process(self, e: Element) -> Element:
        e = super()._process(e)

        # Basic attributes
        if self.clazz is not None:
            e.set("class", str(self.clazz))
        if self.type is not None:
            e.set("type", self.type)

        # Contact filtering
        if self.contype is not None:
            e.set("contype", str(int(self.contype)))
        if self.conaffinity is not None:
            e.set("conaffinity", str(int(self.conaffinity)))

        # Organization
        if self.group is not None:
            e.set("group", str(int(self.group)))
        if self.priority is not None:
            e.set("priority", str(int(self.priority)))

        # Size
        self._produce_type_size_error()
        if self.size is not None:
            if self.type not in ["hfield", "mesh"]:
                sz = self.size
                if len(sz) == 2 and self.type == 'plane':
                    # MuJoCo expects 3 values for plane size, this allows an intuitive sizing of 2 variables
                    sz = [sz[0], sz[1], 1.0]
                e.set("size", floatarr_to_str(sz))
            else:
                if self.type == "hfield":
                    warnings.warn(
                        "size attribute is ignored for hfield geoms, use size attribute of the hfield asset instead"
                    )
                if self.type == "mesh":
                    warnings.warn(
                        "size attribute is ignored for mesh geoms, use fitscale attribute instead"
                    )

        # Appearance
        if self.material is not None:
            e.set("material", str(self.material.mjc_name))
        if self.rgba is not None:
            e.set("rgba", floatarr_to_str(self.rgba))

        # Physics properties
        if self.friction is not None:
            e.set("friction", floatarr_to_str(self.friction))
            e.set("condim", str(len(self.friction) + 1))
        if self.condim is not None:
            if self.condim not in [1, 3, 4, 6]:
                raise ValueError(f"condim must be 1, 3, 4, or 6: got {self.condim}")
            e.set("condim", str(int(self.condim)))
        if self.mass is not None:
            e.set("mass", str(float(self.mass)))
        elif self.density is not None:
            e.set("density", str(float(self.density)))
        if self.shellinertia is not None:
            e.set("shellinertia", str(bool(self.shellinertia)).lower())

        # Warn if both mass and density are specified
        if self.mass is not None and self.density is not None:
            warnings.warn("Both mass and density are specified; mass will take precedence")

        # Solver parameters
        if self.solmix is not None:
            e.set("solmix", str(float(self.solmix)))
        if self.solref is not None:
            e.set("solref", floatarr_to_str(self.solref))
        if self.solimp is not None:
            e.set("solimp", floatarr_to_str(self.solimp))
        if self.margin is not None:
            e.set("margin", str(float(self.margin)))
        if self.gap is not None:
            e.set("gap", str(float(self.gap)))

        # Position and orientation
        if self.fromto is not None:
            e.set("fromto", floatarr_to_str(self.fromto))
            if self.pos is not None or self.rotation is not None:
                warnings.warn(
                    "fromto is specified, pos and rotation will be ignored by MuJoCo compiler"
                )
        else:
            if self.pos is not None:
                e.set("pos", floatarr_to_str(self.pos))
            if self.rotation is not None:
                e.set(*to_mjc(self.rotation))

        # Asset references
        # Heightfields
        if self.hfield is not None:
            if self.type != "hfield":
                warnings.warn(
                    "hfield asset is specified, but type is not 'hfield', hfield will be ignored"
                )
            else:
                e.set("hfield", self.hfield.mjc_name)
        else:
            if self.type == "hfield":
                warnings.warn("type is 'hfield' but no hfield asset is specified")

        # Meshes
        if self.mesh is not None:
            if self.type in ["plane", "hfield"]:
                warnings.warn(
                    f"mesh attribute is specified but type is '{self.type}', mesh will be ignored"
                )
            else:
                e.set("mesh", self.mesh.mjc_name)
        else:
            if self.type == "mesh":
                warnings.warn("type is 'mesh' but no mesh asset is specified")

        # Fit scale
        if self.fitscale is not None:
            e.set("fitscale", str(float(self.fitscale)))

        # Fluid interaction
        if self.fluidshape is not None:
            e.set("fluidshape", self.fluidshape)
        if self.fluidcoef is not None:
            e.set("fluidcoef", floatarr_to_str(self.fluidcoef))

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

            if self.material.texture is not None:
                texhash = self.material.texture.attribute_hash()
                if texhash in existing:
                    self.material.texture = cast(
                        TextureAsset, existing[texhash]
                    )
                else:
                    existing[texhash] = self.material.texture

        if self.mesh is not None:
            meshhash = self.mesh.attribute_hash()
            if meshhash in existing:
                self.mesh = cast(MeshAsset, existing[meshhash])
            else:
                existing[meshhash] = self.mesh

        if self.hfield is not None:
            hfieldhash = self.hfield.attribute_hash()
            if hfieldhash in existing:
                self.hfield = cast(HFieldAsset, existing[hfieldhash])
            else:
                existing[hfieldhash] = self.hfield

    def model_copy(
            self, 
            *, 
            deep: bool = False, 
            update: Mapping[str, object] | None = None
        ) -> "Geom":
        new = cast(Geom, super().model_copy(deep=deep, update=update))

        if deep:
            # Deep copy material
            if self.material is not None:
                new.material = cast(MaterialAsset, self.material.model_copy(deep=True))
            # Deep copy hfield
            if self.hfield is not None:
                new.hfield = cast(HFieldAsset, self.hfield.model_copy(deep=True))
            # Deep copy mesh
            if self.mesh is not None:
                new.mesh = cast(MeshAsset, self.mesh.model_copy(deep=True))

        return new