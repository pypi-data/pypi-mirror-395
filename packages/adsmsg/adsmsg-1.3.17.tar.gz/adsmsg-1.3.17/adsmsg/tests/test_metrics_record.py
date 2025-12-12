
import unittest
from adsmsg.metrics_record import MetricsRecord, MetricsRecordList
from datetime import datetime
import time
from json import dumps, loads
try:
    from __builtin__ import float
except ModuleNotFoundError:
    from builtins import float


class TestMsg(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


    def test_simple_data(self):
        """tests fields where output data that exactly matches input data and data has simple structure"""
        metrics_data = {'bibcode': '1954PhRv...93..256R',
                        'an_citations': 0.15625,
                        'an_refereed_citations': 0.2,
                        'author_num': 4,
                        'citation_num': 11,
                        'citations': ["1954PhRv...93..257G", "1954PhRv...96..730K","1955PhRv...98...79M", "1956RScI...27..809A",
                                      "1958PhRv..112..543S", "1961RScI...32..621H","1963NucPh..45...41A", "1992NDS....67..327K",
                                      "2009NDS...110.2945S", "2013ADNDT..99...22K"],
                        'downloads': [0, 0],
                        'reads': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                        'refereed': False,
                        'refereed_citation_num': 10,
                        'refereed_citations': ["1954PhRv...93..257G", "1954PhRv...96..730K", "1955PhRv...98...79M",
                                               "1956RScI...27..809A", "1958PhRv..112..543S", "1961RScI...32..621H"],
                        'reference_num': 8,
                        'rn_citations':  0.693503
                        }
                        
        m = MetricsRecord(**metrics_data)
        for key in metrics_data:
            if isinstance(metrics_data[key], float):
                self.assertAlmostEqual(getattr(m, key), metrics_data[key], 6)
            else:
                self.assertEqual(getattr(m, key), metrics_data[key])
        self.verify_json(m, 'simple test')

    def test_json_defaults(self):
        """test filling in default values in json"""

        # use some very incomplete test data
        metrics_data = {'bibcode': '1954PhRv...93..256R'}
        m = MetricsRecord(**metrics_data)

        # verify default values not added by default
        j = m.toJSON()
        # verify a default values was not added
        self.assertRaises(KeyError, lambda: j['refereed'])

        # now verify defaults are added when requested
        j = m.toJSON(including_default_value_fields=True)
        self.assertEqual(0, j['an_citations'])
        self.assertEqual(0, j['an_refereed_citations'])
        self.assertEqual(0, j['author_num'])
        self.assertEqual(0, j['citation_num'])
        self.assertEqual(0, len(j['citations']))
        self.assertEqual(0, len(j['downloads']))
        self.assertEqual(0, len(j['reads']))
        self.assertFalse(j['refereed'])
        self.assertEqual(0, j['refereed_citation_num'])
        self.assertEqual(0, len(j['refereed_citations']))
        self.assertEqual(0, j['reference_num'])
        self.assertEqual(0, j['rn_citations'])
        self.assertEqual(0, len(j['rn_citation_data']))


    def verify_json(self, metrics_record, message):
        j = metrics_record.toJSON()
        test = loads(dumps(j))
        self.assertEqual(j, test, message)
            
    def test_time(self):
        """protobuf time field requires conversion back to python datetime"""
        test_datetime = datetime.now()
        time.sleep(.01)  # just incase some other code is doing datetime.now() and using that timestamp
        metrics_data = {'bibcode': '1954PhRv...93..256R',
                        'modtime': test_datetime}
        m = MetricsRecord(**metrics_data)
        m_iso = m.modtime.ToJsonString()
        m_datetime = datetime.strptime(m_iso, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.assertEqual(test_datetime, m_datetime)
        self.verify_json(m, 'time test')


    def test_rn_dict_data(self):
        """rn_citation_data stored as array of dicts"""
        metrics_data = {'bibcode': '1954PhRv...93..256R',
                        'rn_citation_data':
                        [{"ref_norm": 0.2, "pubyear": 1954, "auth_norm": 0.25,
                          "bibcode": "1954PhRv...93..257G", "cityear": 1954},
                         {"ref_norm": 0.07142857142857142, "pubyear": 1954, "auth_norm": 0.25,
                          "bibcode": "1954PhRv...96..730K", "cityear": 1954},
                         {"ref_norm": 0.06666666666666667, "pubyear": 1954, "auth_norm": 0.25,
                          "bibcode": "1955PhRv...98...79M", "cityear": 1955}],
                        }
        m = MetricsRecord(**metrics_data)

        t = metrics_data['rn_citation_data']  # test data
        p = m.rn_citation_data  # protobuf data
        self.assertEqual(len(t), len(p))
        for i in range(0, len(t)):
            for key in t[i]:
                if isinstance(t[i][key], float):
                    self.assertAlmostEqual(t[i][key], getattr(p[i], key), 6, msg='rn_citation_data field {}'.format(key))
                else:
                    self.assertEqual(t[i][key], getattr(p[i], key), msg='rn_citation_data field {}'.format(key))

        
        self.verify_json(m, 'dict test')



    def test_record_list(self):
        """simple test for test MetricsRecordList"""
        metrics_data1 = metrics_data = {'bibcode': '1954PhRv...93..256R', 'refereed': True}
        metrics_data2 = metrics_data = {'bibcode': '1954PhRv...93..256M', 'refereed': False}
        metrics_data3 = metrics_data = {'bibcode': '1954PhRv...93..256S', 'refereed': False}
        metrics_list = [metrics_data1, metrics_data2, metrics_data3]
        m = MetricsRecordList(metrics_records=metrics_list)
        self.assertEqual(len(metrics_list), len(m.metrics_records))
        for i in range(0, len(metrics_list)):
            self.assertEqual(metrics_list[i]['bibcode'], m.metrics_records[i].bibcode)
            self.assertEqual(metrics_list[i]['refereed'], m.metrics_records[i].refereed)



if __name__ == '__main__':
    unittest.main()
