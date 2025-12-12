from drb.exceptions.core import DrbException, DrbFactoryException


class DrbHttpNodeException(DrbException):
    pass


class DrbHttpAuthException(DrbException):
    pass


class DrbHttpServerException(DrbException):
    pass


class DrbHttpNodeFactoryException(DrbFactoryException):
    pass
