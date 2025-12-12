
import unittest
from adsmsg import msg

from adsmsg.augmentrecord import AugmentAffiliationRequestRecord, AugmentAffiliationResponseRecord, AugmentAffiliationRequestRecordList, AugmentAffiliationResponseRecordList

class TestMsg(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_affiliation_request(self):
        d = {'bibcode': '1983ESASP.201...47K',
             'status': 2,
             'aff':  [
                "Harvard-Smithsonian Center for Astrophysics, Cambridge, MA."
             ],
             "author": [
                "Kurtz, M. J."
             ]}
        a = AugmentAffiliationRequestRecord(**d)
        self.assertEqual(a.bibcode, d['bibcode'])
        self.assertEqual(a.status, d['status'])
        self.assertEqual(a.aff, d['aff'])
        self.assertEqual(a.author, d['author'])


    def test_affiliation_request_list(self):
        d_list = [{'bibcode': '1983ESASP.201...47K',
             'status': 2,
             'aff':  [
                "Harvard-Smithsonian Center for Astrophysics, Cambridge, MA."
             ],
             "author": [
                "Kurtz, M. J."
             ]}]
        m = AugmentAffiliationRequestRecordList()
        m.status = 2
        for r in d_list:
            m.affiliation_requests.add(**r)
        for i in range(len(d_list)):
            self.assertEqual(m.affiliation_requests[i].bibcode, d_list[i]['bibcode'])
            self.assertEqual(m.affiliation_requests[i].status, d_list[i]['status'])
            self.assertEqual(m.affiliation_requests[i].aff, d_list[i]['aff'])
            self.assertEqual(m.affiliation_requests[i].author, d_list[i]['author'])

    def test_affiliation_response(self):
        d = {'bibcode': '1983ESASP.201...47K',
             'status': 2,
             'aff':  [
                "Harvard-Smithsonian Center for Astrophysics, Cambridge, MA."
             ],
             "author": [
                "Kurtz, M. J."
             ],
             "aff_abbrev": [
                "CfA"
             ],
            "aff_canonical": [
                "Harvard Smithsonian Center for Astrophysics"
            ], 
            "aff_facet_hier": [
                "0/Harvard U", 
                "1/Harvard U/CfA", 
                "0/SI", 
                "1/SI/CfA"
            ],
             "aff_id": ['placeholder'],
             "institution": [
                "CfA"
             ],
             'aff_raw':  [
                "Harvard-Smithsonian Center for Astrophysics, Cambridge, MA."
             ]
        }
        a = AugmentAffiliationResponseRecord(**d)
        self.assertEqual(a.bibcode, d['bibcode'])
        self.assertEqual(a.status, d['status'])
        self.assertEqual(a.aff, d['aff'])
        self.assertEqual(a.author, d['author'])
        self.assertEqual(a.aff_abbrev, d['aff_abbrev'])
        self.assertEqual(a.aff_canonical, d['aff_canonical'])
        self.assertEqual(a.aff_facet_hier, d['aff_facet_hier'])
        self.assertEqual(a.aff_id, d['aff_id'])
        self.assertEqual(a.aff_raw, d['aff_raw'])
        self.assertEqual(a.institution, d['institution'])
        
    def test_affiliation_response_list(self):
        d = {'bibcode': '1983ESASP.201...47K',
             'status': 2,
             'aff':  [
                "Harvard-Smithsonian Center for Astrophysics, Cambridge, MA."
             ],
             "author": [
                "Kurtz, M. J."
             ],
             "aff_abbrev": [
                "CfA"
            ], 
            "aff_canonical": [
                "Harvard Smithsonian Center for Astrophysics"
            ], 
            "aff_facet_hier": [
                "0/Harvard U", 
                "1/Harvard U/CfA", 
                "0/SI", 
                "1/SI/CfA"
            ],
             "aff_id": ['placeholder'],
             "institution": [
                "CfA"
             ],
             'aff_raw':  [
                "Harvard-Smithsonian Center for Astrophysics, Cambridge, MA."
             ]
        }
        d_list = [d]
        m = AugmentAffiliationResponseRecordList()
        m.status = 2
        for r in d_list:
            m.affiliation_responses.add(**r)
        for i in range(len(d_list)):
            self.assertEqual(m.affiliation_responses[i].bibcode, d_list[i]['bibcode'])
            self.assertEqual(m.affiliation_responses[i].status, d_list[i]['status'])
            self.assertEqual(m.affiliation_responses[i].aff, d_list[i]['aff'])
            self.assertEqual(m.affiliation_responses[i].author, d_list[i]['author'])
            self.assertEqual(m.affiliation_responses[i].aff_abbrev, d_list[i]['aff_abbrev'])
            self.assertEqual(m.affiliation_responses[i].aff_canonical, d_list[i]['aff_canonical'])
            self.assertEqual(m.affiliation_responses[i].aff_facet_hier, d_list[i]['aff_facet_hier'])
            self.assertEqual(m.affiliation_responses[i].aff_id, d_list[i]['aff_id'])
            self.assertEqual(m.affiliation_responses[i].aff_raw, d_list[i]['aff_raw'])
            self.assertEqual(m.affiliation_responses[i].institution, d_list[i]['institution'])
