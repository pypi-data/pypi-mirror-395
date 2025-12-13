import unittest

from gig import Ent

TEST_SUBS = """
    ['EC-01H', 'EC-01I', 'EC-01J', 'EC-01K', 'EC-01M',
    'EC-01N', 'EC-01O', 'LG-11031', 'LG-11090', 'LG-11121',
    'LG-11210', 'LG-11240', 'LG-11301', 'LG-11330', 'LK-1106',
    'LK-1109', 'LK-1121', 'LK-1124', 'LK-1133', 'LK-1136',
    'MOH-11031', 'MOH-11060', 'MOH-11212', 'MOH-11330']
"""

TEST_D = dict(
    id="LK-11",
    name="Colombo",
    area_sqkm="642.00",
    center_lat="6.869636028857",
    center_lng="80.01959786729992",
)


class TestEntBase(unittest.TestCase):
    def test_init(self):
        ent = Ent(TEST_D)
        self.assertEqual(ent.id, "LK-11")
        self.assertEqual(ent.name, "Colombo")
        self.assertTrue(ent.is_parent_id("LK-1"))
        self.assertFalse(ent.is_parent_id("LK-1125"))

        self.assertEqual(len(str(ent)), 124)
        self.assertEqual(str(ent)[:10], "{'id': 'LK")

    def test_acronym(self):
        for ent_id, expected_acronym in [
            ("LK-11", "C"),
            ("LK-1127", "T"),
            ("LK-1127025", "KE"),
        ]:
            ent = Ent.from_id(ent_id)
            self.assertEqual(ent.acronym, expected_acronym)

    def test_short_name(self):
        for ent_id, expected_short_name in [
            ("LK-11", "Clmb"),
            ("LK-1127", "Thmbrgsyy"),
            ("LK-1127025", "Kppywtt Est"),
        ]:
            ent = Ent.from_id(ent_id)
            self.assertEqual(ent.short_name, expected_short_name)

    def test_is_parent_id(self):
        for ent_id, cand_parent_id, expected_is_parent_id in [
            ("LK-11", "LK-1", True),
            ("LK-11", "LK-11", True),
            ("LK-11", "LK-112", False),
            ("LK-1127", "LK-1", True),
            ("LK-1127", "LK-11", True),
            ("LK-1127", "LK-113", False),
        ]:
            ent = Ent.from_id(ent_id)
            self.assertEqual(
                ent.is_parent_id(cand_parent_id), expected_is_parent_id
            )

    def test_repr(self):
        ent = Ent(TEST_D)
        self.assertEqual(repr(ent), str(ent))

    def test_eq(self):
        ent1 = Ent(TEST_D)
        ent2 = Ent(TEST_D)
        self.assertEqual(ent1, ent2)
        self.assertNotEqual(ent1, Ent.from_id("LK-1127"))
        self.assertNotEqual(ent1, 1)
