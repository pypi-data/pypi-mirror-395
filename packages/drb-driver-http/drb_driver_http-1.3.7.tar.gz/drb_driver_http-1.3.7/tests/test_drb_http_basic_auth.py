import io
import time
import unittest
from multiprocessing import Process

import requests
from requests.auth import HTTPBasicAuth
import keyring

from drb.drivers.http import DrbHttpNode
from drb.exceptions.http import DrbHttpAuthException
from tests.utility import start_auth_serve, PORT, PATH

process = Process(target=start_auth_serve)


class TestDrbHttpBasicAuth(unittest.TestCase):
    url_ok = 'http://localhost:' + PORT + PATH + 'test.txt'

    @classmethod
    def setUpClass(cls) -> None:
        process.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls) -> None:
        process.kill()

    def test_attributes(self):
        key = 'Content-Type'
        self.assertEqual(
            requests.head(self.url_ok).headers[key],
            DrbHttpNode(self.url_ok).get_attribute(key))

    def test_no_credential(self):
        node = DrbHttpNode(self.url_ok)
        with self.assertRaises(DrbHttpAuthException):
            node.get_impl(io.BytesIO).getvalue().decode()

    def test_wrong_credential(self):
        node = DrbHttpNode(self.url_ok, auth=HTTPBasicAuth("Bruce", "Wayne"))
        with self.assertRaises(DrbHttpAuthException):
            node.get_impl(io.BytesIO).getvalue().decode()

    def test_credential(self):
        node = DrbHttpNode(self.url_ok,
                           auth=HTTPBasicAuth('user', 'pwd123456'))
        self.assertEqual('{"path": "/resources/test.txt"}',
                         node.get_impl(io.BytesIO).getvalue().decode())
