import os
import sys
import unittest
import uuid
from drb.core.factory import FactoryLoader
from drb.nodes.logical_node import DrbLogicalNode
from drb.topics.dao import ManagerDao
from drb.topics.topic import TopicCategory

from drb.drivers.http import DrbHttpFactory


class TestDrbHttpFactory(unittest.TestCase):
    fc_loader = None
    ic_loader = None
    http_id = uuid.UUID('b065a5aa-35a3-11ec-8d3d-0242ac130003')

    @classmethod
    def setUpClass(cls) -> None:
        cls.fc_loader = FactoryLoader()
        cls.topic_loader = ManagerDao()

    def test_impl_loading(self):
        factory_name = 'http'

        factory = self.fc_loader.get_factory(factory_name)
        self.assertIsNotNone(factory)
        self.assertIsInstance(factory, DrbHttpFactory)

        topic = self.topic_loader.get_drb_topic(self.http_id)
        self.assertIsNotNone(factory)
        self.assertEqual(self.http_id, topic.id)
        self.assertEqual('http', topic.label)
        self.assertIsNone(topic.description)
        self.assertEqual(TopicCategory.PROTOCOL, topic.category)
        self.assertEqual(factory_name, topic.factory)

    def test_impl_signatures(self):
        topic = self.topic_loader.get_drb_topic(self.http_id)

        node = DrbLogicalNode('http://gitlab.com/drb-python')
        self.assertTrue(topic.matches(node))

        node = DrbLogicalNode('.')
        self.assertFalse(topic.matches(node))
