import unittest

from gig import GIGTable

TEST_GIG_TABLE = GIGTable('population-ethnicity', 'regions', '2012')


class TestGIGTable(unittest.TestCase):
    def test_table_id(self):
        gig_table = TEST_GIG_TABLE
        self.assertEqual(
            gig_table.table_id, 'population-ethnicity.regions.2012'
        )

    def test_url_remote_data_path(self):
        gig_table = TEST_GIG_TABLE
        self.assertEqual(
            gig_table.url_remote_data_path,
            '/'.join(
                [
                    'https://raw.githubusercontent.com',
                    'nuuuwan',
                    'gig-data',
                    'master',
                    'gig2',
                    'population-ethnicity.regions.2012.tsv',
                ]
            ),
        )

    def test_remote_data_list(self):
        gig_table = TEST_GIG_TABLE
        remote_data_list = gig_table.remote_data_list
        self.assertEqual(len(remote_data_list), 15_220)
        first_data = remote_data_list[0]
        self.assertEqual(
            first_data,
            {
                'entity_id': 'EC-01',
                'total_population': '2323964.0',
                'sinhalese': '1778826.0',
                'sl_tamil': '234953.0',
                'ind_tamil': '24260.0',
                'sl_moor': '249604.0',
                'burgher': '13305.0',
                'malay': '14444.0',
                'sl_chetty': '909.0',
                'bharatha': '686.0',
                'other_eth': '6977.0',
            },
        )

    def test_remote_data_idx(self):
        gig_table = TEST_GIG_TABLE
        remote_data_idx = gig_table.remote_data_idx
        self.assertEqual(len(remote_data_idx), 15_220)
        first_data = remote_data_idx['EC-01']
        self.assertEqual(
            first_data['entity_id'],
            'EC-01',
        )

    def test_get(self):
        gig_table = TEST_GIG_TABLE
        self.assertEqual(
            gig_table.get('EC-01').total,
            2_323_964,
        )
