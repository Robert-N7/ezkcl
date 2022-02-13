import os
import unittest


class BaseTest(unittest.TestCase):

    @staticmethod
    def get_fixture(name):
        return os.path.join(os.path.dirname(__file__), 'fixtures', name)
