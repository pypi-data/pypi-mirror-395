class SphinxApeException(Exception):
    """
    Base exception.
    """


class BuildError(SphinxApeException):
    """
    Building the docs failed.
    """


class TestError(SphinxApeException):
    """
    Running doc-tests failed.
    """

    __test__ = False


class PublishError(SphinxApeException):
    """
    Publishing the docs failed.
    """
