import io
import unittest
from drb.exceptions.core import DrbException

from drb.drivers.http import DrbHttpNode, HTTPOAuth2
from drb.exceptions.http import DrbHttpAuthException
from tests.utility import stop_mock_oauth2_serve, start_mock_oauth2_serve


class TestDrbHttpOAuth2(unittest.TestCase):
    url_ok = 'https://something.com/resources/test.txt'
    url_ko = 'https://something.com/resources/not_here.txt'
    service_url = 'https://something.com/'

    user = 'user'.encode("utf-8")
    passwd = 'pass'.encode("utf-8")
    token_url = "https://something.com/resources/token"
    bad_token_url = "https://something.com/resources/bad_token"
    client_id = 'test'

    @classmethod
    def setUpClass(cls) -> None:
        start_mock_oauth2_serve()

    @classmethod
    def tearDownClass(cls) -> None:
        stop_mock_oauth2_serve()

    def test_Oauth2_token_create(self):
        auth = HTTPOAuth2(username=self.user, password=self.passwd,
                          token_url=self.token_url,
                          client_id=self.client_id)
        self.assertEqual('new_token', auth.get_token())

    def test_Oauth2_token_expired(self):
        auth = HTTPOAuth2(username=self.user,
                          password=self.passwd,
                          token_url=self.token_url,
                          client_id=self.client_id)
        self.assertEqual('new_token', auth.get_token())
        auth.oauth.expire = -1
        self.assertEqual('refresh_token', auth.get_token())
        auth.oauth.expire = -1

    def test_Oauth2_token_refresh_expired(self):
        auth = HTTPOAuth2(username=self.user, password=self.passwd,
                          token_url=self.token_url,
                          client_id=self.client_id)
        self.assertEqual('new_token', auth.get_token())
        auth.oauth.expire = -1
        self.assertEqual('refresh_token', auth.get_token())
        auth.oauth.refresh_expire = -1
        self.assertEqual('new_token', auth.get_token())

    def test_Oauth2_wrong_user(self):
        auth = HTTPOAuth2(username=self.user, password=self.passwd,
                          token_url=self.bad_token_url,
                          client_id=self.client_id)

        node = DrbHttpNode(self.url_ok, auth)

        with self.assertRaises(DrbHttpAuthException):
            node.get_impl(io.BytesIO).getvalue().decode()

    def test_Oauth2_download(self):
        auth = HTTPOAuth2(username=self.user, password=self.passwd,
                          token_url=self.token_url,
                          client_id=self.client_id)

        node = DrbHttpNode(self.url_ok, auth)
        self.assertEqual('This is my awesome test.',
                         node.get_impl(io.BytesIO).getvalue().decode())

    def test_Oauth2_not_here(self):
        auth = HTTPOAuth2(username=self.user, password=self.passwd,
                          token_url=self.token_url,
                          client_id=self.client_id)

        node = DrbHttpNode(self.url_ko, auth)
        with self.assertRaises(DrbException):
            node.get_impl(io.BytesIO).getvalue().decode()
