import unittest

from gig import GIGTableRow

TEST_D = {
    'entity_id': 'LK-1',
    'a': '100',
    'b': '200',
    'c': '300.45',
    'e': '399.55',
    'total_population': '1000',
}
TEST_GIG_TABLE_ROW = GIGTableRow(TEST_D)


class TestGIGTableRow(unittest.TestCase):
    def test_id(self):
        self.assertEqual(TEST_GIG_TABLE_ROW.id, 'LK-1')

    def test_get_attr(self):
        self.assertEqual(TEST_GIG_TABLE_ROW.a, 100)
        self.assertEqual(TEST_GIG_TABLE_ROW.b, 200)
        self.assertEqual(TEST_GIG_TABLE_ROW.c, 300.45)
        self.assertEqual(TEST_GIG_TABLE_ROW.e, 399.55)

    def test_dict(self):
        self.assertEqual(
            TEST_GIG_TABLE_ROW.dict,
            {
                'a': 100,
                'b': 200,
                'c': 300.45,
                'e': 399.55,
            },
        )

    def test_dict_p(self):
        self.assertEqual(
            TEST_GIG_TABLE_ROW.dict_p,
            {
                'a': 0.1,
                'b': 0.2,
                'c': 0.30045,
                'e': 0.39955,
            },
        )

    def test_total(self):
        self.assertEqual(TEST_GIG_TABLE_ROW.total, 1000)

    def test_str(self):
        self.assertEqual(
            str(TEST_GIG_TABLE_ROW)[:20],
            "{'id': 'LK-1', 'cell",
        )
