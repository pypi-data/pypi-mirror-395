import sys
import os

import unittest
from adsmsg import DenormalizedRecord

class TestDenormalizedRecord(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.proj_home = os.path.join(os.path.dirname(__file__), '../..')


    def tearDown(self):
        unittest.TestCase.tearDown(self)


    def test_is_valid(self):
        denormalized_record = DenormalizedRecord()
        self.assertTrue(denormalized_record.is_valid())

    def test_serialization(self):
        abstract = "This is a dummy abstract."
        author = "Foe, J."
        author_count = 1

        denormalized_record = DenormalizedRecord()
        denormalized_record.data.abstract = abstract
        denormalized_record.data.author.append(author)
        denormalized_record.data.author_count = author_count
        data = denormalized_record.serialize()
        if sys.version_info > (3,):
            test_data = b'\n\x19%b:\x07%b@\x01' % (abstract.encode(),
                                                   author.encode())
        else:
            test_data = '\n\x19{0}:\x07{1}@\x01'.format(abstract, author)
        self.assertEqual(data, test_data)
        data_str = str(denormalized_record)
        self.assertEqual(data_str, 'abstract: "{0}"\nauthor: "{1}"\nauthor_count: {2}\n'.format(abstract, author, author_count))
        self.assertNotEqual(data, data_str)

        recovered_bibrecord = DenormalizedRecord.deserializer(data)
        self.assertTrue(recovered_bibrecord.is_valid())
        self.assertEqual(denormalized_record.data.abstract, abstract)
        self.assertEqual(denormalized_record.data.author[0], author)
        self.assertEqual(denormalized_record.data.author_count, author_count)


    def test_full_record(self):
        """This is here also as a documentation."""
        solr_record = {
             'abstract': u'abstract abstract',
             'ack': u'J.H.S. is grateful to Yujin Yang',
             'aff': [u'aff1', u'aff2'],
             'alternate_bibcode': [u'2015arXiv151103789S'],
             'arxiv_class': [u'Astrophysics - Astrophysics of Galaxies'],
             'author': [u'Shinn, Jong-Ho', u'Seon, Kwang-Il'],
             'author_count': 2,
             'author_facet': [u'Shinn, J', u'Seon, K'],
             'author_facet_hier': [u'0/Shinn, J',
                  u'1/Shinn, J/Shinn, Jong-Ho',
                  u'0/Seon, K',
                  u'1/Seon, K/Seon, Kwang-Il'],
             'author_norm': [u'Shinn, J', u'Seon, K'],
             'bibcode': u'2015ApJ...815..133S',
             'bibstem': [u'ApJ', u'ApJ...815'],
             'bibstem_facet': u'ApJ',
             'body': u"body body",
             'citation_count': 0,
             'citation_count_norm': .2,
             'data_count': 20,
             'database': [u'astronomy'],
             'date': u'2015-12-01T00:00:00.000000Z',
             'doctype': u'article',
             'doctype_facet_hier': [u'0/Article', u'1/Article/Journal Article'],
             'doi': [u'10.1088/0004-637X/815/2/133'],
             'eid': u'133',
             'email': [u'jhshinn@kasi.re.kr', u'-'],
             'entry_date': u'2015-12-01T00:00:00.000000Z',
             'esources': [u'AUTHOR_PUB', u'PUB_HTML'],
             'first_author': u'Shinn, Jong-Ho',
             'first_author_facet_hier': [u'0/Shinn, J', u'1/Shinn, J/Shinn, Jong-Ho'],
             'first_author_norm': u'Shinn, J',
             'fulltext_mtime': u'2019-12-01T00:00:00.000000Z',
             'identifier': [u'1511.03789',
              u'10.1088/0004-637X/815/2/133',
              u'2015arXiv151103789S'],
             'issue': u'2',
             'keyword': [u'dust',
              u'extinction',
              u'galaxies: halos'],
             'keyword_facet': [u'dust',
              u'ism dust extinction'],
             'keyword_norm': [u'dust',
              u'-'],
             'keyword_schema': [u'Astronomy',
              u'Astronomy'],
             'links_data': [u'{"access": "", "instances": "7", "title": "", "type": "simbad", "url": "http://$SIMBAD$/simbo.pl?bibcode=2015ApJ...815..133S"}',
              u'{"access": "open", "instances": "", "title": "", "type": "pdf", "url": "http://stacks.iop.org/0004-637X/815/133/pdf"}'],
             'metadata_mtime': u'2019-12-01T00:00:00.000000Z',
             'metrics_mtime': u'2019-12-01T00:00:00.000000Z',
             'nedid': [4,5,6],
             'nedtype': [u'foo', u'bar', u'baz'],
             'ned_object_facet_hier': [u'0/foo', u'1/foo/star'],
             'nonbib_mtime': u'2019-12-01T00:00:00.000000Z',
             'origin': [u'Elsevier', u'ADS metatada'],
             'orcid_mtime': u'2019-12-01T00:00:00.000000Z',
             'page': [u'133'],
             'page_count': 15,
             'page_range': u'133-148',
             'property': [u'OPENACCESS', u'REFEREED'],
             'pub': u'The Astrophysical Journal',
             'pub_raw': u'The Astrophysical Journal, Volume 815, Issue 2, article id. 133, <NUMPAGES>14</NUMPAGES> pp. (2015).',
             'pubdate': u'2015-12-00',
             'pubnote': [u'33 pages, 7 figures, 5 tables, ApJ in press; doi:10.1088/0004-637X/815/2/133'],
             'read_count': 10,
             'reference': [u'1941ApJ....93...70H', u'1966ApJ...145..811P'],
             'simbid': [1,2,3],
             'title': [u'Ultraviolet Radiative Transfer Modeling of Nearby Galaxies'],
             'volume': u'815',
             'year': u'2015',
             'series': u'series name here',
             'publisher': u'Zenodo',
             'version': u'1.0.0'}

        r = DenormalizedRecord(**solr_record)

        # protobuf actually removes zero values, which is imho cool....
        expected = {}
        expected.update(solr_record)
        expected.pop('citation_count')
        self.maxDiff = None
        self.assertEqual(expected, r.toJSON())

if __name__ == '__main__':
    unittest.main()
