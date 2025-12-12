import sys
import os

import unittest
import adsmsg


class TestPipelineMsg(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.proj_home = os.path.join(os.path.dirname(__file__), '../..')


    def tearDown(self):
        unittest.TestCase.tearDown(self)


    def test_task_hello_world(self):
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main()
