from mjxml.model import MujocoModel
from mjxml.asset import MaterialAsset, TextureAsset
from mjxml.body import Body, Geom
from mjxml.actuator import Actuator
from mjxml.contacts import ContactPair, ContactExclude


def test_mujoco_model_to_xml_sections():
	model = MujocoModel(name="composite")

	texture = TextureAsset(name="tex1")
	model.add_asset(texture)

	body_a = Body(name="body_a")
	body_b = Body(name="body_b")
	geom_a = Geom(name="geom_a")
	geom_b = Geom(name="geom_b")
	body_a.add(geom_a)
	body_b.add(geom_b)
	model.add_body(body_a)
	model.add_body(body_b)

	model.add_actuator(Actuator(name="motor1"))

	model.add_contact(ContactPair(name="pair_ab", geom1=geom_a, geom2=geom_b))
	model.add_contact(ContactExclude(name="exclude_ab", body1=body_a, body2=body_b))

	root = model.to_xml()

	assert root.tag == "mujoco"
	assert root.get("model") == "composite"

	asset_section = root.find("asset")
	assert asset_section is not None
	asset_names = [child.get("name") for child in list(asset_section)]
	assert asset_names == ["tex1"]

	worldbody_section = root.find("worldbody")
	assert worldbody_section is not None
	body_tags = [child.get("name") for child in list(worldbody_section)]
	assert body_tags == ["body_a", "body_b"]

	actuator_section = root.find("actuator")
	assert actuator_section is not None
	actuator = actuator_section.find("general")
	assert actuator is not None
	assert actuator.get("name") == "motor1"

	contact_section = root.find("contact")
	assert contact_section is not None
	pair = contact_section.find("pair")
	exclude = contact_section.find("exclude")
	assert pair is not None and exclude is not None
	assert pair.get("geom1") == "geom_a" and pair.get("geom2") == "geom_b"
	assert exclude.get("body1") == "body_a" and exclude.get("body2") == "body_b"


def test_mujoco_model_remove_duplicate_assets():
	model = MujocoModel()

	tex1 = TextureAsset(file="shared.png")
	tex2 = TextureAsset(file="shared.png")
	model.add_asset(tex1)
	model.add_asset(tex2)

	mat1 = MaterialAsset(rgba=[1.0, 0.0, 0.0, 1.0])
	mat2 = MaterialAsset(rgba=[1.0, 0.0, 0.0, 1.0])
	geom1 = Geom(name="geom1", material=mat1)
	geom2 = Geom(name="geom2", material=mat2)

	body = Body(name="body")
	body.add(geom1)
	body.add(geom2)
	model.add_body(body)

	unique_assets = model.remove_duplicate_assets()

	assert len(unique_assets) == 2
	asset_types = {type(asset) for asset in unique_assets}
	assert asset_types == {TextureAsset, MaterialAsset}

	assert geom1.material is geom2.material
	assert geom1.material in unique_assets
