
import unittest
from google.protobuf import json_format

from adsmsg.master import DocumentRecord, DocumentRecords

class TestMsg(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


    def test_document_record(self):
        """test creation of protobuf

        should include at least all fields listed AdsDataSqlSync:adsdata/run.py:nonbib_to_master_fields"""
        document_record = {
                            'bibcode': '2021ApJ...913L...7A',
                            'identifier': ['2021ApJ...913L...7A', '2020arXiv201014533T'],
                            'links': {
                                'DOI': ['10.3847/2041-8213/abe949'],
                                'ARXIV': ['arXiv:2010.14533'],
                                'DATA': {
                                    'SIMBAD': {
                                        'url': ['http://simbad.u-strasbg.fr/simbo.pl?bibcode=2021ApJ...913L...7A'],
                                        'title': ['http://simbad.u-strasbg.fr/simbo.pl?bibcode=2021ApJ...913L...7A'],
                                        'count': 15}},
                                'ESOURCE': {
                                    'EPRINT_HTML': {'url': ['https://arxiv.org/abs/2010.14533'],
                                                    'title': ['https://arxiv.org/abs/2010.14533']},
                                    'EPRINT_PDF': {'url': ['https://arxiv.org/pdf/2010.14533'],
                                                   'title': ['https://arxiv.org/pdf/2010.14533']},
                                    'PUB_HTML': {'url': ['https://doi.org/10.3847%2F2041-8213%2Fabe949'],
                                                 'title': ['https://doi.org/10.3847%2F2041-8213%2Fabe949']},
                                    'PUB_PDF': {
                                        'url': ['http://iopscience.iop.org/article/10.3847/2041-8213/abe949/pdf'],
                                        'title': ['http://iopscience.iop.org/article/10.3847/2041-8213/abe949/pdf']}},
                                'ASSOCIATED': {'url': ['2021ApJ...913L...7A', '2021nova.pres.7954K'],
                                               'title': ['Main Paper', 'Press Release']},
                                'CITATIONS': True,
                                'REFERENCES': True}
                        }
        m = DocumentRecord(**document_record)
        self.assertEqual(m.bibcode, document_record['bibcode'])
        self.assertEqual(m.identifier, document_record['identifier'])
        self.assertEqual(json_format.MessageToDict(m.links), document_record['links'])

    def test_document_records(self):
        """test creation of protobuf"""

        document_records = {
            'status': 2,    #name='new', index=2, number=2,
            'document_records':[
                {
                    'bibcode': '2021ApJ...913L...7A',
                    'identifier': ['2021ApJ...913L...7A', '2020arXiv201014533T'],
                    'links': {
                        'DOI': ['10.3847/2041-8213/abe949'],
                        'ARXIV': ['arXiv:2010.14533'],
                        "DATA": {
                            "SIMBAD": {"url": ["http://simbad.u-strasbg.fr/simbo.pl?bibcode=2021ApJ...913L...7A"],
                                       "title": ["http://simbad.u-strasbg.fr/simbo.pl?bibcode=2021ApJ...913L...7A"],
                                       "count": 15}},
                        "ESOURCE": {
                            "EPRINT_HTML": {"url": ["https://arxiv.org/abs/2010.14533"],
                                            "title": ["https://arxiv.org/abs/2010.14533"]},
                            "EPRINT_PDF": {"url": ["https://arxiv.org/pdf/2010.14533"],
                                           "title": ["https://arxiv.org/pdf/2010.14533"]},
                            "PUB_HTML": {"url": ["https://doi.org/10.3847%2F2041-8213%2Fabe949"],
                                         "title": ["https://doi.org/10.3847%2F2041-8213%2Fabe949"]},
                            "PUB_PDF": {"url": ["http://iopscience.iop.org/article/10.3847/2041-8213/abe949/pdf"],
                                        "title": ["http://iopscience.iop.org/article/10.3847/2041-8213/abe949/pdf"]}},
                        'ASSOCIATED': {'url': ['2021ApJ...913L...7A', '2021nova.pres.7954K'],
                                       'title': ['Main Paper', 'Press Release']},
                        'CITATIONS': True,
                        'REFERENCES': True}
                }, {
                    'bibcode': '2012Sci...338..355D',
                    'identifier': ['2012Sci...338..355D', '2012arXiv1210.6132D'],
                    'links': {
                        'DOI': ['10.1126/science.1224768'],
                        'ARXIV': ['arXiv:1210.6132'],
                        'DATA': {
                            'CDS': {'url': ['http://vizier.u-strasbg.fr/viz-bin/cat/J/other/Sci/338.355'],
                                    'title': ['http://vizier.u-strasbg.fr/viz-bin/cat/J/other/Sci/338.355'],
                                    'count': 1},
                            'SIMBAD': {'url': ['http://simbad.u-strasbg.fr/simbo.pl?bibcode=2012Sci...338..355D'],
                                       'title': ['http://simbad.u-strasbg.fr/simbo.pl?bibcode=2012Sci...338..355D'],
                                       'count': 2}
                        },
                        'ESOURCE': {
                            'EPRINT_HTML': {'url': ['https://arxiv.org/abs/1210.6132'],
                                            'title': ['https://arxiv.org/abs/1210.6132']},
                            'EPRINT_PDF': {'url': ['https://arxiv.org/pdf/1210.6132'],
                                           'title': ['https://arxiv.org/pdf/1210.6132']},
                            'PUB_HTML': {'url': ['http://www.sciencemag.org/cgi/content/full/338/6105/355'],
                                         'title': ['http://www.sciencemag.org/cgi/content/full/338/6105/355']},
                            'PUB_PDF': {'url': ['http://www.sciencemag.org/content/338/6105/355.full'],
                                        'title': ['http://www.sciencemag.org/content/338/6105/355.full']}
                        },
                        'ASSOCIATED': {'url': ['2012yCatp021033801D', '2012Sci...338..355D', '2012Sci...338..355D'],
                                       'title': ['Catalog Description', 'Source Paper', 'Supporting Media']},
                        'PRESENTATION': {'url': ['http://www.youtube.com/watch?v=323IIht3Jpg']}}
                }, {
                        'bibcode': '1995Natur.375..659T',
                        'identifier': ['1995Natur.375..659T','10.1038/375659a0'],
                        'links': {
                            'DOI': ['10.1038/375659a0'],
                            'DATA': {
                                'HEASARC': {'url': ['http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=1995Natur.375..659T'],
                                            'title': ['http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=1995Natur.375..659T'],
                                            'count': 1},
                                'NED': {'url': ['https://ned.ipac.caltech.edu/uri/NED::InRefcode/1995Natur.375..659T'],
                                        'title': ['https://ned.ipac.caltech.edu/uri/NED::InRefcode/1995Natur.375..659T'],
                                        'count': 1},
                                'SIMBAD': {'url': ['http://simbad.u-strasbg.fr/simbo.pl?bibcode=1995Natur.375..659T'],
                                           'title': ['http://simbad.u-strasbg.fr/simbo.pl?bibcode=1995Natur.375..659T'],
                                           'count': 1}
                            },
                        'ESOURCE': {
                            'PUB_HTML': {'url': ['https://doi.org/10.1038%2F375659a0'],
                                         'title': ['https://doi.org/10.1038%2F375659a0']}
                        },
                        'INSPIRE': {'url': ['http://inspirehep.net/search?p=find+j+NATUA,375,659']},
                        'TOC': True}
                    }
            ]
        }

        n = DocumentRecords(**document_records)
        self.assertEqual(n.status, document_records['status'])
        for i, document_record in enumerate(document_records['document_records']):
            self.assertEqual(n.document_records[i].bibcode, document_record['bibcode'])
            self.assertEqual(n.document_records[i].identifier, document_record['identifier'])
            self.assertEqual(json_format.MessageToDict(n.document_records[i].links), document_record['links'])

if __name__ == '__main__':
    unittest.main()
