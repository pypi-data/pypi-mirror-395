import io
import json
import sys
import time
import unittest
from multiprocessing import Process

from drb.exceptions.core import DrbException
from unittest.mock import patch

import requests

from drb.drivers.http import DrbHttpNode
from tests.utility import start_serve, PATH
from tests.utility import PORT

process = Process(target=start_serve)


class TestDrbHttp(unittest.TestCase):
    url_ok = 'http://localhost:' + PORT + PATH + 'test.txt'
    url_false = 'http://localhost:' + PORT + PATH + 'test.json'

    @classmethod
    def setUpClass(cls) -> None:
        process.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls) -> None:
        process.kill()

    def test_impl_download(self):
        node = DrbHttpNode(self.url_ok)
        with node.get_impl(io.BytesIO) as stream:
            self.assertEqual('This is my awesome test.',
                             stream.read().decode())
        with node.get_impl(io.BytesIO) as stream:
            self.assertEqual('T',
                             stream.read(1).decode())
        with node.get_impl(io.BytesIO, start=5, end=10) as stream:
            self.assertEqual('is my',
                             stream.read().decode())

    def test_impl_download_read_twice(self):
        node = DrbHttpNode(self.url_ok)
        with node.get_impl(io.BytesIO, chunk_size=1) as stream:
            self.assertEqual('This',
                             stream.read(4).decode())
            # Test reward with read all the rest
            self.assertEqual(' is my awesome test.',
                             stream.read().decode())

    def test_impl_download_seek_chunk_10(self):
        node = DrbHttpNode(self.url_ok)

        with node.get_impl(io.BytesIO, chunk_size=1) as stream:
            self.assertTrue(stream.seekable())

            self.assertEqual(stream.seek(10), 10)
            self.assertEqual(stream.seek(1, io.SEEK_CUR), 11)
            self.assertEqual('awe', stream.read().decode()[:3])
            self.assertEqual(stream.tell(), len('This is my awesome test.'))

            # Test reward with read with len 2
            self.assertEqual(stream.seek(6), 6)
            self.assertEqual('s my', stream.read(4).decode())

            self.assertEqual(stream.tell(), 10)

            # Test reward with read all (special case)
            self.assertEqual(stream.seek(5), 5)
            self.assertEqual(stream.tell(), 5)
            self.assertEqual('is my awesome test.', stream.read().decode())

    def test_impl_download_seek_chunk_1(self):
        node = DrbHttpNode(self.url_ok)

        with node.get_impl(io.BytesIO, chunk_size=1) as stream:
            self.assertEqual(stream.seek(10), 10)
            self.assertEqual(stream.seek(1, io.SEEK_CUR), 11)
            self.assertEqual('awe', stream.read().decode()[:3])
            self.assertEqual(stream.tell(), len('This is my awesome test.'))

            # Test reward with read with len 2
            self.assertEqual(stream.seek(6), 6)
            self.assertEqual('s my', stream.read(4).decode())

    def test_impl_download_seek_end(self):
        node = DrbHttpNode(self.url_ok)

        with node.get_impl(io.BytesIO) as stream:
            my_bytes = 'This is my awesome test.'.encode('utf-8')
            self.assertEqual(stream.seek(0, io.SEEK_END), len(my_bytes))
            self.assertEqual(stream.tell(), len(my_bytes))

    def test_impl_download_seek_before_end(self):
        node = DrbHttpNode(self.url_ok)

        with node.get_impl(io.BytesIO) as stream:
            my_bytes = 'This is my awesome test.'.encode('utf-8')
            self.assertEqual(stream.seek(-5, io.SEEK_END), len(my_bytes) - 5)
            self.assertEqual(stream.tell(), len(my_bytes) - 5)
            self.assertEqual('test', stream.read(4).decode())

    def test_impl_argument(self):
        header_key = 'Content-Type'
        header_value = requests.head(self.url_ok).headers[header_key]
        node = DrbHttpNode(self.url_ok, params={"cookies": None})
        self.assertEqual(header_value, node.get_attribute(header_key))

    def test_impl_none_argument(self):
        key = ('params', None)
        with self.assertRaises(KeyError):
            DrbHttpNode(self.url_ok, params={}).attributes[key]

    def test_impl_no_argument(self):
        key = ('params', None)
        with self.assertRaises(KeyError):
            DrbHttpNode(self.url_ok).attributes[key]

    def test_name(self):
        expected = "data.json"
        with patch('requests.head') as mock_head:
            mock_head.return_value.status_code = 200
            mock_head.return_value.headers = {
                'Content-Type': 'application/json',
                'Content-Length': 20,
                'Content-Disposition': f'attachment; filename="{expected}"',
            }
            node = DrbHttpNode('http://something.net/foobar')
            self.assertEqual(expected, node.name)

    def test_namespace_uri(self):
        node = DrbHttpNode(self.url_ok)
        self.assertIsNone(node.namespace_uri)

    def test_value(self):
        path = self.url_ok
        self.assertIsNone(DrbHttpNode(path).value)

    def test_parent(self):
        node = DrbHttpNode(self.url_ok)
        self.assertIsNone(node.parent)

    def test_attributes(self):
        header_key = "Content-Type"
        header_value = requests.head(self.url_ok).headers[header_key]
        node = DrbHttpNode(self.url_ok)

        self.assertEqual(
            header_value,
            node.attributes[header_key.lower(), None]
        )

        self.assertEqual(header_value, node.get_attribute(header_key))
        self.assertEqual(header_value, node.get_attribute(header_key.lower()))

        self.assertEqual(header_value, node @ header_key)
        self.assertEqual(header_value, node @ (header_key, None))
        self.assertEqual(header_value, node @ header_key.lower())
        self.assertEqual(header_value, node @ (header_key.lower(), None))

    def test_wrong_attributes(self):
        with self.assertRaises(DrbException):
            DrbHttpNode(self.url_ok).get_attribute('A Wrong attributes', None)
        with self.assertRaises(DrbException):
            DrbHttpNode(self.url_ok).get_attribute('A Wrong attributes',
                                                   'Something')
        with self.assertRaises(DrbException):
            DrbHttpNode(self.url_ok).get_attribute('Content-Type',
                                                   'Something')

    def test_path(self):
        self.assertEqual(self.url_ok, DrbHttpNode(self.url_ok).path.name)

    def test_children(self):
        node = DrbHttpNode(self.url_ok)
        self.assertEqual(0, len(node))

    def test_bracket(self):
        node = DrbHttpNode(self.url_ok)

        with self.assertRaises(KeyError):
            node['http://test.com/toto']

        with self.assertRaises(NotImplementedError):
            node[None] = DrbHttpNode('http://test.com/toto')

        with self.assertRaises(NotImplementedError):
            del node['http://test.com/toto']

    def test_has_children(self):
        self.assertFalse(DrbHttpNode(self.url_ok).has_child)

    def test_get_attribute(self):
        node = DrbHttpNode(self.url_ok)
        self.assertEqual(
            'text/plain',
            node.get_attribute('Content-Type'))
        node2 = DrbHttpNode(self.url_false)

        with self.assertRaises(DrbException):
            node2.get_attribute('Connection')

        with self.assertRaises(DrbException):
            node.get_attribute('foobar')

    @patch('requests.post')
    def test_post(self, mock_post):
        info = {"test1": "value1", "test2": "value2"}
        headers = {'Content-Type': 'application/json'}
        DrbHttpNode.post(url=self.url_ok,
                         headers=headers,
                         data=json.dumps(info))
        mock_post.assert_called_with(
            url='http://localhost:8756/resources/test.txt',
            headers={'Content-Type': 'application/json'},
            json='{"test1": "value1", "test2": "value2"}',
            allow_redirects=True,
            auth=None)
