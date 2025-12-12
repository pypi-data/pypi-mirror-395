import unittest
from drb.core import DrbNode

from drb.drivers.http import DrbHttpNode, DrbHttpFactory
from tests.utility import PORT, PATH


class TestDrbHttpFactory(unittest.TestCase):

    def test_create(self):
        factory = DrbHttpFactory()
        node = factory.create('http://localhost:'+PORT+PATH+'test.txt')
        self.assertIsInstance(node, (DrbHttpNode, DrbNode))
