import unittest

from adsmsg.nonbibrecord import NonBibRecord, DataLinksRecord, DataLinksRecordList

class TestMsg(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


    def test_nonbib(self):
        """test creation of protobuf 

        should include at least all fields listed AdsDataSqlSync:adsdata/run.py:nonbib_to_master_fields"""
        nonbib_data = {'bibcode': '2003ASPC..295..361M', 
                       'boost': 3.1,
                       'citation_count': 3,
                       'bibgroup': ["Chandra/Technical"],
                       'bibgroup_facet':  ["Chandra/Technical"],
                       'data': ['NED:15', 'CDS:5'],
                       'data_links_rows': [{'link_type': 'a', 'link_sub_type': 'b', 
                                            'url': ['http://a', 'http://b'],
                                            'title': ['x', 'y'],
                                            'item_count':1},
                                           {'link_type': 'aa', 'link_sub_type': 'bb', 
                                            'url': ['http://aa', 'http://bb'],
                                            'title': ['xx', 'yy'],
                                            'item_count':2}],
                       'citation_count_norm': .2,
                       'esource': ['a', 's', 'd', 'f'],
                       'grants': ['g1', 'g2'],
                       'ned_objects': ['ned1', 'ned2'],
                       'norm_cites': 2,
                       'read_count': 7,
                       'readers': ['r1', 'r2'],
                       'reference': ['ref1', 'ref2'],
                       'simbad_objects': ['s1', 's2'],
                       'total_link_counts': 20
                       }
        m = NonBibRecord(**nonbib_data)
        self.assertEqual(m.bibcode, nonbib_data['bibcode'])
        self.assertAlmostEqual(m.boost, nonbib_data['boost'], places=5)
        self.assertEqual(m.citation_count, nonbib_data['citation_count'])
        self.assertEqual(m.bibgroup, nonbib_data['bibgroup'])
        self.assertEqual(m.bibgroup_facet, nonbib_data['bibgroup_facet'])
        self.assertEqual(m.esource, nonbib_data['esource'])
        self.assertEqual(m.grants, nonbib_data['grants'])
        self.assertEqual(m.ned_objects, nonbib_data['ned_objects'])
        self.assertEqual(m.norm_cites, nonbib_data['norm_cites'])
        self.assertEqual(m.read_count, nonbib_data['read_count'])
        self.assertEqual(m.readers, nonbib_data['readers'])
        self.assertEqual(m.reference, nonbib_data['reference'])
        self.assertEqual(m.simbad_objects, nonbib_data['simbad_objects'])
        self.assertEqual(m.total_link_counts, nonbib_data['total_link_counts'])
        self.assertEqual(m.data.data, nonbib_data['data']) # data is a special field name
        self.assertAlmostEqual(m.citation_count_norm, nonbib_data['citation_count_norm'], places=5)

        for i in range(len(nonbib_data['data_links_rows'])):
            self.assertEqual(m.data_links_rows[i].link_type, nonbib_data['data_links_rows'][i]['link_type'])
            self.assertEqual(m.data_links_rows[i].link_sub_type, nonbib_data['data_links_rows'][i]['link_sub_type'])
            self.assertEqual(m.data_links_rows[i].url, nonbib_data['data_links_rows'][i]['url'])
            self.assertEqual(m.data_links_rows[i].title, nonbib_data['data_links_rows'][i]['title'])
            self.assertEqual(m.data_links_rows[i].item_count, nonbib_data['data_links_rows'][i]['item_count'])

    def test_nonbib_links_and_identifier(self):
        """test creation of NonBibRecord with links and identifier parameters"""
        nonbib_data = {
            'bibcode': '2003ASPC..295..361M',
            'links': {
                # Boolean values
                'TOC': True,
                'ABSTRACT': False,
                
                # List values
                'ARXIV': ['1234.5678', '8765.4321'],
                'DOI': ['10.1234/5678', '10.8765/4321'],
                
                # Dict values - DATA
                'DATA': {
                    'CDS': {
                        'url': ['http://cds.u-strasbg.fr/1', 'http://cds.u-strasbg.fr/2'],
                        'title': ['CDS Link 1', 'CDS Link 2'],
                        'count': 2
                    },
                    'NED': {
                        'url': ['http://ned.ipac.caltech.edu/1'],
                        'title': ['NED Object'],
                        'count': 1
                    }
                },
                
                # Dict values - ESOURCE
                'ESOURCE': {
                    'PUB_HTML': {
                        'url': ['http://example.com/pub/html'],
                        'title': ['Publisher HTML']
                    },
                    'PUB_PDF': {
                        'url': ['http://example.com/pub/pdf'],
                        'title': ['Publisher PDF']
                    }
                },
                
                # Other link types
                'ASSOCIATED': {
                    'url': ['http://example.com/associated'],
                    'title': ['Associated Articles'],
                    'count': 5
                },
                'INSPIRE': {
                    'url': ['http://inspirehep.net/record/12345'],
                    'title': ['INSPIRE Record']
                },
                'LIBRARYCATALOG': {
                    'url': ['http://library.example.com/catalog/123'],
                    'title': ['Library Catalog']
                },
                'PRESENTATION': {
                    'url': ['http://example.com/presentation'],
                    'title': ['Presentation'],
                    'count': 1
                }
            },
            'identifier': ['arxiv:1234.5678', 'doi:10.1234/5678']
        }
        
        m = NonBibRecord(**nonbib_data)
        
        # Check basic fields
        self.assertEqual(m.bibcode, nonbib_data['bibcode'])
        
        # Check boolean link values
        self.assertTrue(m.links.TOC)
        self.assertFalse(m.links.ABSTRACT)
        
        # Check list link values
        self.assertEqual(m.links.ARXIV, nonbib_data['links']['ARXIV'])
        self.assertEqual(m.links.DOI, nonbib_data['links']['DOI'])
        
        # Check DATA values
        for subtype in nonbib_data['links']['DATA']:
            self.assertEqual(m.links.DATA[subtype].url, nonbib_data['links']['DATA'][subtype]['url'])
            self.assertEqual(m.links.DATA[subtype].title, nonbib_data['links']['DATA'][subtype]['title'])
            self.assertEqual(m.links.DATA[subtype].count, nonbib_data['links']['DATA'][subtype]['count'])
        
        # Check ESOURCE values
        for subtype in nonbib_data['links']['ESOURCE']:
            self.assertEqual(m.links.ESOURCE[subtype].url, nonbib_data['links']['ESOURCE'][subtype]['url'])
            self.assertEqual(m.links.ESOURCE[subtype].title, nonbib_data['links']['ESOURCE'][subtype]['title'])
        
        # Check ASSOCIATED
        self.assertEqual(m.links.ASSOCIATED.url, nonbib_data['links']['ASSOCIATED']['url'])
        self.assertEqual(m.links.ASSOCIATED.title, nonbib_data['links']['ASSOCIATED']['title'])
        self.assertEqual(m.links.ASSOCIATED.count, nonbib_data['links']['ASSOCIATED']['count'])
        
        # Check INSPIRE
        self.assertEqual(m.links.INSPIRE.url, nonbib_data['links']['INSPIRE']['url'])
        self.assertEqual(m.links.INSPIRE.title, nonbib_data['links']['INSPIRE']['title'])
        
        # Check LIBRARYCATALOG
        self.assertEqual(m.links.LIBRARYCATALOG.url, nonbib_data['links']['LIBRARYCATALOG']['url'])
        self.assertEqual(m.links.LIBRARYCATALOG.title, nonbib_data['links']['LIBRARYCATALOG']['title'])
        
        # Check PRESENTATION
        self.assertEqual(m.links.PRESENTATION.url, nonbib_data['links']['PRESENTATION']['url'])
        self.assertEqual(m.links.PRESENTATION.title, nonbib_data['links']['PRESENTATION']['title'])
        self.assertEqual(m.links.PRESENTATION.count, nonbib_data['links']['PRESENTATION']['count'])
        
        # Check identifier
        self.assertEqual(m.identifier, nonbib_data['identifier'])

    def test_datalinks(self):
        """test creation of protobuf

        should include at least all fields listed AdsDataSqlSync:adsdata/run.py:nonbib_to_master_fields"""
        datalinks_data = {'bibcode': '2003ASPC..295..361M',
                          'data_links_rows': [{'link_type': 'a', 'link_sub_type': 'b',
                                               'url': ['http://a', 'http://b'],
                                               'title': ['x', 'y'],
                                               'item_count':1},
                                              {'link_type': 'aa', 'link_sub_type': 'bb',
                                               'url': ['http://aa', 'http://bb'],
                                               'title': ['xx', 'yy'],
                                               'item_count':2}]
                          }
        m = DataLinksRecord(**datalinks_data)
        self.assertEqual(m.bibcode, datalinks_data['bibcode'])

        for i in range(len(datalinks_data['data_links_rows'])):
            self.assertEqual(m.data_links_rows[i].link_type, datalinks_data['data_links_rows'][i]['link_type'])
            self.assertEqual(m.data_links_rows[i].link_sub_type, datalinks_data['data_links_rows'][i]['link_sub_type'])
            self.assertEqual(m.data_links_rows[i].url, datalinks_data['data_links_rows'][i]['url'])
            self.assertEqual(m.data_links_rows[i].title, datalinks_data['data_links_rows'][i]['title'])
            self.assertEqual(m.data_links_rows[i].item_count, datalinks_data['data_links_rows'][i]['item_count'])


    def test_datalinks_list(self):
        datalinks_list = {
            'status': 2,    #name='new', index=2, number=2,
            'datalinks_records':[{'bibcode': '2013MNRAS.435.1904M',
                                  'data_links_rows': [{'link_type': 'ESOURCE', 'link_sub_type': 'EPRINT_HTML',
                                         'url': ['http://arxiv.org/abs/1307.6556'], 'title': [''], 'item_count':0},
                                        {'link_type': 'ESOURCE', 'link_sub_type': 'EPRINT_PDF',
                                         'url': ['http://arxiv.org/pdf/1307.6556'], 'title': [''], 'item_count':0},
                                        {'link_type': 'ESOURCE', 'link_sub_type': 'PUB_HTML',
                                         'url': ['http://dx.doi.org/10.1093%2Fmnras%2Fstt1379'], 'title': [''], 'item_count':0},
                                        {'link_type': 'ESOURCE', 'link_sub_type': 'PUB_PDF',
                                         'url': ['http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf'], 'title': [''], 'item_count':0}]},
                                 {'bibcode': '2013MNRAS.435.1904M',
                                  'data_links_rows': [{'link_type': 'DATA', 'link_sub_type': 'CXO',
                                         'url': ['http://cda.harvard.edu/chaser?obsid=494'], 'title': ['Chandra Data Archive ObsIds 494'], 'item_count':27},
                                        {'link_type': 'DATA', 'link_sub_type': 'ESA',
                                         'url': ['http://archives.esac.esa.int/ehst/#bibcode=2013MNRAS.435.1904M'], 'title': ['European HST References (EHST)'], 'item_count':1},
                                        {'link_type': 'DATA', 'link_sub_type': 'HEASARC',
                                         'url': ['http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=2013MNRAS.435.1904M'], 'title': ['s'], 'item_count':1},
                                        {'link_type': 'DATA', 'link_sub_type': 'Herschel',
                                         'url': ['http://herschel.esac.esa.int/hpt/publicationdetailsview.do?bibcode=2013MNRAS.435.1904M'], 'title': ['s'], 'item_count':1},
                                        {'link_type': 'DATA', 'link_sub_type': 'NED',
                                         'url': ['http://$NED$/cgi-bin/nph-objsearch?search_type=Search&refcode=2013MNRAS.435.1904M'], 'title': ['NED Objects (1)'], 'item_count':1},
                                        {'link_type': 'DATA', 'link_sub_type': 'SIMBAD',
                                         'url': ['http://$SIMBAD$/simbo.pl?bibcode=2013MNRAS.435.1904M'], 'title': ['SIMBAD Objects (30)'], 'item_count':30},
                                        {'link_type': 'DATA', 'link_sub_type': 'XMM',
                                         'url': ['http://nxsa.esac.esa.int/nxsa-web/#obsid=0097820101'], 'title': ['XMM-Newton Observation Number 0097820101'], 'item_count':1}]},
                                 {'bibcode': '2017MNRAS.467.3556B',
                                  'data_links_rows': [
                                        {'link_type': 'PRESENTATION',  'link_sub_type': '',
                                         'url': ['1971ATsir.615....4D', '1974Afz....10..315D', '1971ATsir.621....7D',
                                                 '1976Afz....12..665D', '1971ATsir.624....1D', '1983Afz....19..229D',
                                                 '1983Ap.....19..134D', '1973ATsir.759....6D', '1984Afz....20..525D',
                                                 '1984Ap.....20..290D', '1974ATsir.809....1D', '1974ATsir.809....2D',
                                                 '1974ATsir.837....2D'],
                                         'title': ['Part  1', 'Part  2', 'Part  3', 'Part  4', 'Part  5', 'Part  6', 'Part  7',
                                                   'Part  8', 'Part  9', 'Part 10', 'Part 11', 'Part 12', 'Part 13'],
                                         'item_count':0}]}]
        }
        m = DataLinksRecordList()
        m.status = datalinks_list['status']
        for datalinks_record in datalinks_list['datalinks_records']:
            m.datalinks_records.add(**datalinks_record)

        self.assertEqual(m.status, datalinks_list['status'])
        for i in range(len(datalinks_list['datalinks_records'])):
            self.assertEqual(m.datalinks_records[i].bibcode, datalinks_list['datalinks_records'][i]['bibcode'])
            for j in range (len(datalinks_list['datalinks_records'][i]['data_links_rows'])):
                self.assertEqual(m.datalinks_records[i].data_links_rows[j].link_type,
                                 datalinks_list['datalinks_records'][i]['data_links_rows'][j]['link_type'])
                self.assertEqual(m.datalinks_records[i].data_links_rows[j].link_sub_type,
                                 datalinks_list['datalinks_records'][i]['data_links_rows'][j]['link_sub_type'])
                self.assertEqual(m.datalinks_records[i].data_links_rows[j].url,
                                 datalinks_list['datalinks_records'][i]['data_links_rows'][j]['url'])
                self.assertEqual(m.datalinks_records[i].data_links_rows[j].title,
                                 datalinks_list['datalinks_records'][i]['data_links_rows'][j]['title'])
                self.assertEqual(m.datalinks_records[i].data_links_rows[j].item_count,
                                 datalinks_list['datalinks_records'][i]['data_links_rows'][j]['item_count'])


if __name__ == '__main__':
    unittest.main()
