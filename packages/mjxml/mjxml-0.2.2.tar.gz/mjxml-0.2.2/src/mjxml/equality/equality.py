from xml.etree.ElementTree import Element
from mjxml.typeutils import SupportsBool, ArrayLike, floatarr_to_str
from mjxml.commons import MJCElement

__all__ = ["Equality"]

class Equality(MJCElement):
    active: SupportsBool | None = None
    solref: ArrayLike[float] | None = None
    solimp: ArrayLike[float] | None = None

    def _process(self, e: Element) -> Element:
        e = super()._process(e)
        if self.active is not None:
            e.set('active', str(bool(e)).lower())
        if self.solref is not None:
            e.set('solref', floatarr_to_str(self.solref))
        if self.solimp is not None:
            e.set('solimp', floatarr_to_str(self.solimp))
        return e