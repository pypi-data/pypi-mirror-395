import unittest

from gig import Ent, GIGTable


class TestEntGIGMixin(unittest.TestCase):
    def test_gig(self):
        gig_table = GIGTable('population-ethnicity', 'regions', '2012')
        ent = Ent.from_id('LK-1')
        gig_row = ent.gig(gig_table)
        self.assertEqual(
            gig_row.total,
            5_850_745,
        )

        self.assertEqual(
            gig_row.dict,
            {
                'sinhalese': 4925402,
                'sl_tamil': 339233,
                'ind_tamil': 56614,
                'sl_moor': 460545,
                'burgher': 25277,
                'malay': 27853,
                'sl_chetty': 4806,
                'bharatha': 1297,
                'other_eth': 9718,
            },
        )
