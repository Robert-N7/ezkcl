from ezkcl.files.obj import load_obj_mats
from ezkcl.lib.kcl_material import KclMaterial
from tests.base_test import BaseTest


class TestObj(BaseTest):
    def test_load_mats(self):
        file = self.get_fixture('simple.obj')
        mats = list(load_obj_mats(file).values())
        expected = [
            KclMaterial('road_2', 0x00c0),
            KclMaterial('offroad_3', 0x00c2),
        ]
        self.assertEqual(mats, expected)
