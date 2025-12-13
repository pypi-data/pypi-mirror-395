import unittest

from gig import EntType


class TestEntType(unittest.TestCase):
    def test_list(self):
        self.assertEqual(
            EntType.list(),
            [
                EntType.COUNTRY,
                EntType.PROVINCE,
                EntType.DISTRICT,
                EntType.DSD,
                EntType.GND,
                EntType.ED,
                EntType.PD,
                EntType.LG,
                EntType.MOH,
            ],
        )

    def test_get_entity_type(self):
        for [id, expected_ent_type] in [
            ["LK", EntType.COUNTRY],
            ["LK-1", EntType.PROVINCE],
            ["LK-11", EntType.DISTRICT],
            ["LK-1127", EntType.DSD],
            ["LK-1127025", EntType.GND],
            ["XX-112702512", EntType.UNKNOWN],
            ["EC-11", EntType.ED],
            ["EC-11A", EntType.PD],
            ["LG-12345", EntType.LG],
            ["MOH-12345", EntType.MOH],
            ["XX-1234", EntType.UNKNOWN],
        ]:
            self.assertEqual(
                EntType.from_id(id),
                expected_ent_type,
            )

    def test_url_remote_data_path(self):
        self.assertEqual(
            EntType.PROVINCE.url_remote_data_path,
            "/".join(
                [
                    "https://raw.githubusercontent.com/nuuuwan"
                    + "/lk_admin_regions/master/data/ents/provinces.tsv",
                ]
            ),
        )

    def test_remote_data_list(self):
        data_list = EntType.PROVINCE.remote_data_list
        self.assertEqual(
            len(data_list),
            9,
        )
        first_data = data_list[0]
        self.assertEqual(
            first_data,
            {
                "id": "LK-1",
                "name": "Western",
                "name_si": "බස්නාහිර පළාත",
                "name_ta": "மேல் மாகாணம்",
                "area_sqkm": "3751.55742292",
                "center_lat": "6.82758732",
                "center_lon": "80.03300355",
            },
        )
