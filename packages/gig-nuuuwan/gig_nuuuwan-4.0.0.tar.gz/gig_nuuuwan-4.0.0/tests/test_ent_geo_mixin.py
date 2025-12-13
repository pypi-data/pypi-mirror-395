import os
import tempfile
from unittest import TestCase

import matplotlib.pyplot as plt

from gig import Ent

TEST_ENT = Ent.from_id("LK-1127")
DIR_TMP = tempfile.gettempdir()


class TestEntGeoMixin(TestCase):
    def test_url_remote_geo_data_path(self):
        print(TEST_ENT.url_remote_geo_data_path)

        self.assertEqual(
            TEST_ENT.url_remote_geo_data_path,
            "/".join(
                [
                    "https://raw.githubusercontent.com",
                    "nuuuwan",
                    "lk_admin_regions",
                    "master",
                    "data",
                    "geo",
                    "json",
                    "original",
                    "dsds.json",
                    "LK-1127.json",
                ]
            ),
        )

    def test_raw_geo(self):
        raw_geo = TEST_ENT.get_raw_geo()
        self.assertEqual(len(raw_geo), 1)
        self.assertEqual(len(raw_geo[0]), 2177)
        self.assertEqual(len(raw_geo[0][0]), 2)
        self.assertAlmostEqual(raw_geo[0][0][0], 79.88620694600019, 4)
        self.assertAlmostEqual(raw_geo[0][0][1], 6.92412304100003, 4)

    def test_raw_geo_after_delete(self):
        if os.path.exists(TEST_ENT.raw_geo_file.path):
            os.remove(TEST_ENT.raw_geo_file.path)
        raw_geo = TEST_ENT.get_raw_geo()
        self.assertEqual(len(raw_geo), 1)

    def test_geo(self):
        for id in ["LK-1", "LK-11", "LK-1127", "LK-1127025"]:
            ent = Ent.from_id(id)
            geo = ent.geo()
            geo.plot()
            png_file_name = f"gig.TestEntGeoMixin.{id}.png"
            test_png_file_path = os.path.join(DIR_TMP, png_file_name)
            plt.savefig(test_png_file_path)
            plt.close()

            control_png_file_path = os.path.join("tests", png_file_name)
            self.assertAlmostEqual(
                os.path.getsize(test_png_file_path),
                os.path.getsize(control_png_file_path),
                delta=10000,
            )

    def test_geo_safe(self):
        geo = TEST_ENT.geo_safe()
        self.assertEqual(len(geo), 1)
        self.assertEqual(len(geo.columns), 1)
        self.assertEqual(geo.crs.to_string(), "EPSG:4326")
        self.assertEqual(geo.geometry.type[0], "MultiPolygon")

    def test_ent_id_to_geo(self):
        ent_ids = ["LK-1", "LK-11", "LK-1127", "LK-1127025"]
        ent_id_to_geo = Ent.get_ent_id_to_geo(ent_ids)
        self.assertEqual(len(ent_id_to_geo), 4)
