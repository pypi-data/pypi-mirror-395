from mjxml.body.worldbodychildren import BodyChildren
from typing import Self
from mjxml.equality.equality import Equality
from mjxml.contacts.contacts import Contact
from mjxml.actuator.general import Actuator
from mjxml.typeutils import Str
from mjxml.body.worldbody import WorldBody
from xml.etree.ElementTree import Element
from mjxml.asset import Asset
from pydantic.main import BaseModel
from pydantic.fields import Field
from pydantic.config import ConfigDict
from mjxml.commons import _XMLSerializable, MJCElement


class MujocoModel(_XMLSerializable, BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    name: Str = Field(default="default_model")
    worldbody: WorldBody = Field(default_factory=WorldBody)
    assets: list[Asset] = Field(default_factory=list) # A list of manually added assets
    actuators: list[Actuator] = Field(default_factory=list)
    contacts: list[Contact] = Field(default_factory=list)
    equality: list[Equality] = Field(default_factory=list)

    def to_xml(self) -> Element:
        e = Element("mujoco")
        e = self._process(e)
        return e

    def _process(self, e: Element) -> Element:
        e.set('model', str(self.name))

        assets = Element("asset")
        found = self.remove_duplicate_assets()

        asset_set = set()
        for a in found:
            if a.mjc_name in asset_set:
                raise ValueError(f"Duplicate asset name found during serialization: {a.mjc_name}")
            asset_set.add(a.mjc_name)
            assets.append(a.to_xml())
        e.append(assets)

        e.append(self.worldbody.to_xml())

        actuators = Element("actuator")
        for act in self.actuators:
            actuators.append(act.to_xml())
        e.append(actuators)

        contacts = Element("contact")
        for c in self.contacts:
            contacts.append(c.to_xml())
        e.append(contacts)

        equality = Element("equality")
        for eq in self.equality:
            equality.append(eq.to_xml())
        e.append(equality)

        return e

    def add_asset(self, asset: Asset) -> Self:
        self.assets.append(asset)
        return self

    def add_body(self, body: BodyChildren) -> Self:
        self.worldbody.add(body)
        return self

    def add_actuator(self, actuator: Actuator) -> Self:
        self.actuators.append(actuator)
        return self

    def add_contact(self, contact: Contact) -> Self:
        self.contacts.append(contact)
        return self

    def add_equality(self, equality: Equality) -> Self:
        self.equality.append(equality)
        return self

    def add(self, e: MJCElement):
        if isinstance(e, Asset):
            return self.add_asset(e)
        elif isinstance(e, BodyChildren):
            return self.add_body(e)
        elif isinstance(e, Actuator):
            return self.add_actuator(e)
        elif isinstance(e, Contact):
            return self.add_contact(e)
        elif isinstance(e, Equality):
            return self.add_equality(e)
        else:
            raise ValueError(f'type {e} is unsupported to add to MujocoModel')

    def writefile(self, filepath: str, encoding: str = 'utf-8', indent: int|None = 2):
        xml = self.to_xml_str(indent=indent)
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(xml)

    def remove_duplicate_assets(self) -> list[Asset]:
        existing: dict[int, Asset] = {}
        for asset in self.assets:
            ahash = asset.attribute_hash()
            if ahash not in existing:
                existing[ahash] = asset
        self.worldbody.remove_duplicate_assets(existing)
        return list(existing.values())