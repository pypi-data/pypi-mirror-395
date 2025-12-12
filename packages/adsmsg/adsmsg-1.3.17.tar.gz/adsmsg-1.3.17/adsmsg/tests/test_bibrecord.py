import sys
import os

import unittest
from adsmsg import BibRecord


class TestBibRecord(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.proj_home = os.path.join(os.path.dirname(__file__), '../..')


    def tearDown(self):
        unittest.TestCase.tearDown(self)


    def test_is_valid(self):
        bibrecord = BibRecord()
        bibrecord.data.bibcode = "2017IAUS..325..341B"
        bibrecord.data.JSON_fingerprint = "JSON"
        bibrecord.data.metadata.general.arxivcategories.append("Instrumentation and Methods for Astrophysics")
        bibrecord.data.text.body.content = "Article..."
        self.assertTrue(bibrecord.is_valid())


    def test_serialization(self):
        bibcode = "2017IAUS..325..341B"
        JSON_fingerprint = "JSON"
        arxiv_category = "Instrumentation and Methods for Astrophysics"
        content = "This is a dummy article."

        bibrecord = BibRecord()
        bibrecord.data.bibcode = bibcode
        bibrecord.data.JSON_fingerprint = JSON_fingerprint
        bibrecord.data.metadata.general.arxivcategories.append(arxiv_category)
        bibrecord.data.text.body.content = content


        data = bibrecord.serialize()
        if sys.version_info > (3,):
            test_data = b'\n\x13%b\x12\x04%b\x1a0\n.\n,%b"\x1c\n\x1a\n\x18%b' % (bibcode.encode(),
                                                                                 JSON_fingerprint.encode(),
                                                                                 arxiv_category.encode(),
                                                                                 content.encode())
        else:
            test_data = '\n\x13{0}\x12\x04{1}\x1a0\n.\n,{2}"\x1c\n\x1a\n\x18{3}'.format(bibcode,
                                                                                        JSON_fingerprint,
                                                                                        arxiv_category,
                                                                                        content)
        self.assertEqual(data, test_data)
        data_str = str(bibrecord)
        self.assertEqual(data_str, 'bibcode: "{0}"\nJSON_fingerprint: "{1}"\nmetadata {{\n  general {{\n    arxivcategories: "{2}"\n  }}\n}}\ntext {{\n  body {{\n    content: "{3}"\n  }}\n}}\n'.format(bibcode, JSON_fingerprint, arxiv_category, content))
        self.assertNotEqual(data, data_str)

        recovered_bibrecord = BibRecord.deserializer(data)
        self.assertTrue(recovered_bibrecord.is_valid())
        self.assertEqual(bibrecord.data.bibcode, bibcode)
        self.assertEqual(bibrecord.data.JSON_fingerprint, JSON_fingerprint)
        self.assertEqual(bibrecord.data.metadata.general.arxivcategories[0], arxiv_category)
        self.assertEqual(bibrecord.data.text.body.content, content)




if __name__ == '__main__':
    unittest.main()
