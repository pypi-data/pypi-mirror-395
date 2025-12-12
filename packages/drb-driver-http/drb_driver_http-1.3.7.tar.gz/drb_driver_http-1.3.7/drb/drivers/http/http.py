from __future__ import annotations

import io
import re
import sys

import keyring
from deprecated import deprecated
from drb.core import DrbNode, ParsedPath, DrbFactory
from drb.exceptions.core import DrbException
from drb.nodes.abstract_node import AbstractNode
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse

import requests
from requests.models import Response
from requests.auth import AuthBase, HTTPBasicAuth
from tenacity import retry, stop_after_attempt, stop_after_delay, \
    wait_fixed, wait_exponential, retry_if_exception_type

from drb.exceptions.http import DrbHttpServerException, \
    DrbHttpNodeException, DrbHttpAuthException


class EmptyAuth(AuthBase):
    """
    This Empty credential class is used to handle no-credentials cases.
    This class can be used instead of None auth that means credential
    still not initialized.
    """
    def __call__(self, r):
        return r


@retry(stop=stop_after_attempt(5),
       wait=wait_exponential(multiplier=2, min=1, max=10),
       retry=retry_if_exception_type(DrbHttpServerException))
@retry(stop=(stop_after_delay(120) | stop_after_attempt(5)),
       wait=wait_fixed(15),
       retry=retry_if_exception_type(DrbHttpNodeException))
def get(path: str, auth: AuthBase, redirect, headers, params: Dict[str, Any]):
    return requests.get(path, stream=True, auth=auth, allow_redirects=redirect,
                        headers=headers, params=params)


@retry(stop=stop_after_attempt(5),
       wait=wait_exponential(multiplier=2, min=1, max=10),
       retry=retry_if_exception_type(DrbHttpServerException))
@retry(stop=(stop_after_delay(120) | stop_after_attempt(5)),
       wait=wait_fixed(15),
       retry=retry_if_exception_type(DrbHttpNodeException))
def head(path: str, auth: AuthBase, redirect, params: Dict[str, Any]):
    return requests.head(
        path,
        auth=auth,
        allow_redirects=redirect,
        **params
    )


def check_response(resp: Response):
    if resp.status_code >= 500:
        raise DrbHttpServerException(
            "ERROR: " + str(resp.status_code) +
            " reason : " + resp.reason +
            " request : " + resp.request.url
        )
    if 500 > resp.status_code >= 400:
        raise DrbHttpAuthException(
            "ERROR: " + str(resp.status_code) +
            " reason : " + resp.reason +
            " request : " + resp.request.url
        )
    if 400 > resp.status_code >= 300:
        raise DrbHttpNodeException(
            "ERROR: " + str(resp.status_code) +
            " reason : " + resp.reason +
            " request : " + resp.request.url
        )


def check_args(*args):
    return len(args) > 0 and isinstance(
        args[0],
        int
    ) and args[0] > 0


class Download(io.BytesIO):
    def __init__(self, path: str,
                 auth: AuthBase,
                 params: Dict[str, str],
                 headers,
                 chunk_size: int,
                 redirect=True
                 ):
        self.__res = None
        self._chunk_size = chunk_size
        self._path = path
        self._auth = auth
        self._params = params
        self._headers = headers
        self._iter = None
        self._buff = bytearray(0)
        self._pos = 0
        self._seekable = True
        self._redirect = redirect
        self.content_length = -1
        super().__init__()

    def seek(self, offset, whence=0):
        if not self._seekable:
            raise OSError
        if whence == 0:
            pos_seek = 0
        elif whence == 1:
            pos_seek = self._pos
        elif whence == 2:
            if self.content_length == -1:
                # reset position to find end of file
                # in case of we are at end of file...
                self._pos = 0
                self.__init_request()
            pos_seek = self.content_length

        pos_seek += offset
        if pos_seek < 0:
            raise OSError

        if pos_seek != self._pos:
            if pos_seek > self._pos and \
                    (pos_seek - self._pos) < (10 * self._chunk_size):
                read = 1
                to_read = pos_seek - self._pos
                while to_read > 0 and read > 0:
                    if to_read > self._chunk_size:
                        size_to_read = self._chunk_size
                    else:
                        size_to_read = to_read
                    buff = self.read(size_to_read)
                    read = len(buff)
                    to_read -= read

                return self._pos
            if self.__res is not None:
                self.__res.close()
                self.__res = None

            self._pos = pos_seek

        return self._pos

    def tell(self) -> int:
        return self._pos

    def seekable(self, *args, **kwargs):
        return self._seekable

    def __init_request(self):

        pos_start = self._pos

        heads = None
        if self.__res is None or self._iter is None:
            if self._iter is not None:
                self._iter.close()
                self._iter = None
            self._buff = bytearray(0)

            if self._headers is not None:
                pos_start = pos_start + self._headers[0]
                if len(self._headers) > 1:
                    end = pos_start + self._headers[1]
                    heads = {
                        "range":
                            f"bytes={pos_start}"
                            f"-{end}"
                    }
                else:
                    heads = {"range": f"bytes={pos_start}-"}
            elif pos_start > 0:
                heads = {"range": f"bytes={pos_start}-"}
            self.__res = get(
                self._path,
                self._auth,
                self._redirect,
                heads,
                self._params
            )
            check_response(self.__res)
            headers = self.__res.headers
            for k, v in headers.items():
                if k.lower() == 'content-length':
                    self.content_length = int(v) + pos_start

    def getvalue(self) -> bytes:
        self.__init_request()
        return self.__res.content

    def __init_generator(self):
        if self._iter is None:
            self._iter = self.__res.iter_content(self._chunk_size)

    def read(self, *args, **kwargs):
        if not check_args(*args):
            if self.__res is None:
                self.__init_request()

                with self.__res as resp:
                    return resp.content
            else:
                _buff = self._buff[:]
                self._buff = bytearray(0)
                try:
                    while True:
                        _buff.extend(bytearray(next(self._iter)))
                except StopIteration:
                    self._pos += len(_buff)
                return _buff

        self.__init_request()
        self.__init_generator()
        try:
            while len(self._buff) < args[0]:
                self._buff.extend(bytearray(next(self._iter)))

            res = self._buff[0:args[0]]
            del (self._buff[0:args[0]])
            self._pos = self._pos + len(res)
            return res
        except StopIteration:
            if len(self._buff) > 0:
                if args[0] < len(self._buff):
                    res = self._buff[0:args[0]]
                    del (self._buff[0:args[0]])
                    self._pos = self._pos + len(res)
                    return res
                else:
                    self._pos = self._pos + len(self._buff)
                    res = self._buff[:]
                    self._buff = bytearray(0)
                    return res
            else:
                return bytes(0)

    def close(self) -> None:
        super().close()
        if self.__res is not None:
            self.__res.close()


class DrbHttpNode(AbstractNode):
    """
    Parameters:
        path: The url of the http or https server
        auth (AuthBase): The authentication object to get
                         the connexion (default: None)
        params (Dict[str, str]): Parameters to send with all
                                 requests (default: None)
    """

    def __init__(self, path, auth: AuthBase = None,
                 redirect=True,
                 params: Dict[str, Any] = {}):
        super().__init__()
        self._path = path
        self._auth = auth
        self._params = params
        self._children = []
        self._redirect = redirect
        self.add_impl(io.BytesIO, _to_stream)

    def __init_header(self):
        if len(self._attrs) == 0:
            res = head(self._path, self.auth, self._redirect, self._params)
            if res.status_code == 405:
                headers = {"Range": "bytes=0-0"}
                res = get(path=self._path,
                          auth=self.auth,
                          redirect=self._redirect,
                          params=self._params,
                          headers=headers
                          )
            check_response(res)
            for x in res.headers:
                self.__imatmul__((x, res.headers[x]))

    def __get_name_from_url(self):
        parsed_uri = urlparse(self._path)
        return str(parsed_uri.path).split('/')[-1]

    @property
    def name(self) -> str:
        self.__init_header()
        try:
            disposition = self.__matmul__('content-disposition')
            r = re.search(r'filename ?= ?((["\'])?(.*)(["\'])?)', disposition)
            if r:
                return r.group(1).replace("'", "").replace('"', "")
            return self.__get_name_from_url()
        except DrbException:
            return self.__get_name_from_url()

    @property
    @deprecated(version='1.2.0',
                reason='Only bracket browse should be use')
    def children(self) -> List[DrbNode]:
        return self._children

    @property
    def auth(self) -> AuthBase:
        if self._auth is None:
            credential = keyring.get_credential(service_name=self.path.path,
                                                username=None)
            if credential is not None:
                self._auth = HTTPBasicAuth(credential.username,
                                           credential.password)
            else:
                self._auth = EmptyAuth()
        return self._auth

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError

    def __matmul__(self, other):
        new_other = other
        if isinstance(other, str):
            new_other = other.lower(), None
        if isinstance(other, tuple):
            new_other = (other[0].lower(), *other[1:])
        return super().__matmul__(new_other)

    def __imatmul__(self, other):
        new_other = (other[0].lower(), *other[1:])
        super().__imatmul__(new_other)

    @property
    def params(self):
        return self._params

    @property
    def has_child(self, name: str = None, namespace: str = None) -> bool:
        return False

    @property
    def path(self) -> ParsedPath:
        return ParsedPath(self._path)

    @property
    @deprecated(version='1.2.0',
                reason='Usage of the @ operator is recommended')
    def attributes(self) -> Dict[Tuple[str | Any, None], Any]:
        self.__init_header()
        return self._attrs.copy()

    @deprecated(version='1.2.0',
                reason='Usage of the @ operator is recommended')
    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        self.__init_header()
        key = (name.lower(), namespace_uri)
        if namespace_uri is None and key in self.attributes.keys():
            return self.attributes[key]
        raise DrbException(f'Attribute not found name: {name}, '
                           f'namespace: {namespace_uri}')

    @staticmethod
    def post(url: str,
             headers: dict = None,
             data: dict = None,
             auth: AuthBase = None,
             redirect=True
             ) -> DrbNode:
        """
            Send a post request with the headers and
            the data given in argument.

            Parameters:
                url (str): the url you want to send request
                headers (dict): Dictionary, list of tuples, bytes, or file-like
                    object to send in the body.
                data (dict): json data to send in the body.
                auth (AuthBase)
                redirect (Bool)
        """
        response = requests.post(url=url,
                                 headers=headers,
                                 json=data,
                                 allow_redirects=redirect,
                                 auth=auth)
        return DrbHttpResponse(path=url, response=response)


def _to_stream(node: DrbHttpNode, **kwargs):
    headers = None
    if 'start' in kwargs:
        if 'end' in kwargs:
            headers = (kwargs.get('start'), kwargs.get('end'))
        else:
            headers = (kwargs.get('start'),)
    return Download(node.path.name, node.auth, node.params, headers,
                    kwargs.get('chunk_size', 4 * 1048576),
                    kwargs.get('redirect', True))


class DrbHttpResponse(DrbHttpNode):
    def __init__(self, path: str, response: Response):
        super().__init__(path=path)
        self._path = path
        self._resp = response
        self._attrs = {
            (k, None): v for k, v in self._resp.headers.items()
        }
        self.value = response.content
        self.add_impl(io.BytesIO, self._to_stream)

    @staticmethod
    def _to_stream(node: DrbNode, **kwargs):
        if isinstance(node, DrbHttpResponse):
            return io.BytesIO(node.value)


class DrbHttpFactory(DrbFactory):

    @staticmethod
    def _create_from_uri_of_node(node: DrbNode):
        uri = node.path.name
        return DrbHttpNode(uri)

    def _create(self, node: DrbNode) -> DrbNode:
        if isinstance(node, DrbHttpNode):
            return node
        return self._create_from_uri_of_node(node)
