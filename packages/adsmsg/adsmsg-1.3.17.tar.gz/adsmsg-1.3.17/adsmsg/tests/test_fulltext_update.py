import sys
import os

import unittest
from adsmsg import FulltextUpdate


class TestFulltextUpdate(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.proj_home = os.path.join(os.path.dirname(__file__), '../..')


    def tearDown(self):
        unittest.TestCase.tearDown(self)


    def test_is_valid(self):
        fulltext_update = FulltextUpdate(acknowledgements='foo', dataset=['bar'], facility=['baz'])
        fulltext_update.bibcode = "fta"
        fulltext_update.body = "Introduction\nTHIS IS AN INTERESTING TITLE\n"
        self.assertTrue(fulltext_update.is_valid())


if __name__ == '__main__':
    unittest.main()
