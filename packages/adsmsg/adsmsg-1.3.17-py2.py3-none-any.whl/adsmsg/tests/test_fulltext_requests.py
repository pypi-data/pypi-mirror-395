import sys
import os

import unittest
from adsmsg import FulltextRequests


class TestFulltextRequests(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.proj_home = os.path.join(os.path.dirname(__file__), '../..')


    def tearDown(self):
        unittest.TestCase.tearDown(self)


    def test_is_valid(self):
        fulltext_requests = FulltextRequests()
        fulltext_request = fulltext_requests.requests.add()
        fulltext_request.bibcode = "bibcode"
        fulltext_request.provider = "MNRAS"
        fulltext_request.ft_source = "tests/test_integration/stub_data/full_test.txt"
        self.assertTrue(fulltext_requests.is_valid())


if __name__ == '__main__':
    unittest.main()
