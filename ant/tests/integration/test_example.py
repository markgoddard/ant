import unittest

from ant import infra
from ant.infra import ntc


class TestExample(unittest.TestCase):

    def setUp(self):
        self.infra = ntc.Infra()

    def tearDown(self):
        pass

    def test_example(self):
        self.infra.get_cmc()
