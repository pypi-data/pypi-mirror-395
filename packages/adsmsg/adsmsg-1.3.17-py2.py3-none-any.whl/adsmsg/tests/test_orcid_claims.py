
import unittest
from adsmsg import OrcidClaims
from adsmsg.bibrecord import BibRecord

class TestMsg(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


    def test(self):
        r = OrcidClaims(bibcode='bicode', authors=['Einstein, A', 'Munger, Charlie'],
                        verified=['-', '0000-0003-3041-2092'],
                        unverified=['0000-0003-3041-2091', '-'],
                        )
        self.assertEqual(r.verified, ['-', '0000-0003-3041-2092'])




if __name__ == '__main__':
    unittest.main()
