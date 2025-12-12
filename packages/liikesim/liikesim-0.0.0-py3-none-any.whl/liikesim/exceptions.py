from __future__ import print_function
from __future__ import absolute_import


class LiikesimException(Exception):
    """用于不破坏连接的Liikesim错误的异常类，异常可修复，连接可继续使用"""

    def __init__(self, desc):
        Exception.__init__(self, desc)


class FatalLiikesimError(Exception):
    """用于严重错误的异常类，连接无法继续使用"""

    def __init__(self, desc):
        Exception.__init__(self, desc)
