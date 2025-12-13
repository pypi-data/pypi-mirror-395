from mjxml.asset import Asset
from .worldbodychildren import BodyChildren
from mjxml.rotations import RotationType, to_mjc
from xml.etree.ElementTree import Element
from typing import SupportsFloat, Literal
from mjxml.typeutils import ArrayLike, PosFloat, SupportsBool, floatarr_to_str
import warnings

__all__ = ["Camera"]

_CAMERA_MODE = Literal["fixed", "track", "trackcom", "targetbody", "targetbodycom"]


class Camera(BodyChildren):
    """MuJoCo camera element.

    Creates a camera attached to a body (or worldbody).
    """

    # Mode and targeting
    mode: _CAMERA_MODE | None = None
    target: BodyChildren | None = None

    # Optical properties
    orthographic: SupportsBool | None = None
    fovy: PosFloat | None = None
    ipd: PosFloat | None = None
    resolution: ArrayLike[SupportsFloat, Literal[2]] | None = None
    focal: ArrayLike[SupportsFloat, Literal[2]] | None = None
    focalpixel: ArrayLike[SupportsFloat, Literal[2]] | None = None
    principal: ArrayLike[SupportsFloat, Literal[2]] | None = None
    principalpixel: ArrayLike[SupportsFloat, Literal[2]] | None = None
    sensorsize: ArrayLike[SupportsFloat, Literal[2]] | None = None

    # Position and orientation
    pos: ArrayLike[SupportsFloat, Literal[3]] | None = None
    rotation: RotationType | None = None

    # User parameters
    user_params: ArrayLike[SupportsFloat] | None = None

    def to_xml(self) -> Element:
        e = Element("camera")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e = super()._process(e)

        # Mode and targeting
        if self.mode is not None:
            e.set("mode", self.mode)
            if self.mode in ["targetbody", "targetbodycom"] and self.target is None:
                warnings.warn(
                    f"mode is '{self.mode}' but no target body is specified. "
                    "MuJoCo requires a target for this mode."
                )

        if self.target is not None:
            if self.target.name is None:
                raise ValueError(
                    "Target body must have a name to be referenced by camera"
                )
            e.set("target", str(self.target.name))
        
        # Optical properties
        if self.orthographic is not None:
            e.set("orthographic", str(bool(self.orthographic)).lower())

        if self.fovy is not None:
            e.set("fovy", str(float(self.fovy)))
            if any(x is not None for x in [self.focal, self.focalpixel, self.principal, self.principalpixel, self.sensorsize]):
                 warnings.warn("fovy is mutually exclusive with focal, principal, and sensorsize attributes.")

        if self.ipd is not None:
            e.set("ipd", str(float(self.ipd)))
        
        if self.resolution is not None:
            e.set("resolution", floatarr_to_str(self.resolution))
        
        if self.focal is not None:
            e.set("focal", floatarr_to_str(self.focal))
        
        if self.focalpixel is not None:
            e.set("focalpixel", floatarr_to_str(self.focalpixel))
            if self.focal is not None:
                warnings.warn("Both focal and focalpixel are specified. focal will be ignored.")

        if self.principal is not None:
            e.set("principal", floatarr_to_str(self.principal))
        
        if self.principalpixel is not None:
            e.set("principalpixel", floatarr_to_str(self.principalpixel))
            if self.principal is not None:
                warnings.warn("Both principal and principalpixel are specified. principal will be ignored.")

        if self.sensorsize is not None:
            e.set("sensorsize", floatarr_to_str(self.sensorsize))
            if self.resolution is None or (self.focal is None and self.focalpixel is None):
                 warnings.warn("sensorsize requires resolution and focal (or focalpixel) to be specified.")

        # Position and orientation
        if self.pos is not None:
            e.set("pos", floatarr_to_str(self.pos))
        if self.rotation is not None:
            e.set(*to_mjc(self.rotation))

        if self.user_params is not None:
            e.set("user", floatarr_to_str(self.user_params))

        return e

    def remove_duplicate_assets(self, existing: dict[int, Asset]) -> None:
        pass