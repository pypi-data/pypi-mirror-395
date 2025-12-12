import sys
import os

import unittest
import adsmsg
from adsmsg import BibRecord, Status
from adsmsg.msg import Msg
import base64

try:
    import simplejson as json
except ImportError:
    import json

from google.protobuf import json_format


class TestMsg(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


    def test_generic_methods(self):
        # keywords initialization
        b = BibRecord(bibcode='bibcode')
        self.assertEqual(b.bibcode, 'bibcode')
        self.assertEqual(b.data.bibcode, 'bibcode')

        # acces/set attributes directly
        b.bibcode = 'foobar'
        self.assertEqual(b.bibcode, 'foobar')
        self.assertEqual(b.data.bibcode, 'foobar')


    def test_serializer(self):
        b = BibRecord(bibcode='bibcode')
        cls, data = b.dump()

        self.assertEqual('adsmsg.bibrecord.BibRecord', cls)
        if sys.version_info > (3,):
            test_data = b'\n\x07bibcode'
        else:
            test_data = '\n\x07bibcode'
        self.assertEqual(test_data, data)

        b2 = Msg.loads(cls, data)
        self.assertEqual(b2.bibcode, b.bibcode)


    def test_higher_char(self):
        b = BibRecord(bibcode=u'\u01b5')
        cls, data = b.dump()

        self.assertEqual('adsmsg.bibrecord.BibRecord', cls)
        if sys.version_info > (3,):
            test_data = b'\n\x02\xc6\xb5'
        else:
            test_data = '\n\x02\xc6\xb5'
        self.assertEqual(test_data, data)

        b2 = Msg.loads(cls, data)
        self.assertEqual(b2.bibcode, b.bibcode)


    def test_json(self):
        if sys.version_info > (3,):
            test_bib = '\u01b5'
        else:
            test_bib = u'\u01b5'
        b = BibRecord(bibcode=test_bib)
        cls, data = b.dump()
        x = json.dumps(b.__json__())
        z = json.loads(x)
        data2 = base64.b64decode(z['__adsmsg__'][1])
        self.assertEqual(repr(data), repr(data2))

        b1 = Msg.loads(cls, data)
        b2 = Msg.loads(cls, data2)
        self.assertEqual(b1.bibcode, u'\u01b5')
        self.assertEqual(b2.bibcode, u'\u01b5')
        
    
    def test_toJSON(self):
        b = BibRecord(bibcode=u'\u01b5')
        self.assertEqual(b.toJSON(), {'bibcode': u'\u01b5'})
        self.assertTrue(isinstance(b.toJSON(), dict))
        self.assertEqual('{\n  "bibcode": "\\u01b5"\n}', b.toJSON(return_string=True))

    
    def test_status(self):
        b = BibRecord(bibcode='bibcode', status=Status.active)
        self.assertEqual(b.status, 0)

        b = BibRecord(bibcode='bibcode', status='active')
        self.assertEqual(b.status, 0)
        
if __name__ == '__main__':
    unittest.main()
