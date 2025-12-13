from mjxml.contacts.contacts import Contact
from xml.etree.ElementTree import Element
from mjxml.body import Body

__all__ = ["ContactExclude"]

class ContactExclude(Contact):
    """MuJoCo contact exclude element."""
    body1: Body
    body2: Body

    def to_xml(self) -> Element:
        e = Element("exclude")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        if self.body1.name is None:
            raise ValueError("body1 must have a name")
        if self.body2.name is None:
            raise ValueError("body2 must have a name")

        e.set("name", str(self.name))
        e.set("body1", str(self.body1.name))
        e.set("body2", str(self.body2.name))

        return e
