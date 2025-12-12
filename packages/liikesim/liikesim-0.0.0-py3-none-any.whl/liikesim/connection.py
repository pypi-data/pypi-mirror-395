from __future__ import print_function
from __future__ import absolute_import
import socket
from .exceptions import LiikesimException, FatalLiikesimError

def isConnected():
    return _connection is not None

def send(message: str):
    if _connection is None:
        raise FatalLiikesimError("未连接到仿真端，请先连接到仿真端")
    return _connection.send(message)

class Connection:
    def __init__(self, host, port, timeout, max_byte=1024):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(timeout)
        self._max_byte = max_byte
        try:
            self._socket.connect((host, port))
        except socket.timeout:
            raise FatalLiikesimError("连接超时，请确保仿真端已经启动，并且IP地址和端口号正确")
        except ConnectionRefusedError:
            raise FatalLiikesimError("连接被拒绝，请确保仿真端已经启动，并且IP地址和端口号正确")
        except Exception as e:
            raise FatalLiikesimError(f"连接发生错误：{e}")

        global _connection
        _connection = self

    def send(self, message: str):
        if self._socket is None:
            raise FatalLiikesimError("未连接到仿真端，请先连接到仿真端")
        try:
            self._socket.send(message.encode('utf-8'))
            response = b''
            while True:
                chunk = self._socket.recv(self._max_byte)
                response += chunk
                try:
                    if response.decode('utf-8').endswith("\n"):
                        break
                except Exception as e:
                    continue
            response = response.decode('utf-8').strip("\n\r\t ")
            return response
        except socket.timeout:
            raise FatalLiikesimError("连接超时，请确保仿真端已经启动，并且IP地址和端口号正确")
        except ConnectionRefusedError:
            raise FatalLiikesimError("连接被拒绝，请确保仿真端已经启动，并且IP地址和端口号正确")
        except Exception as e:
            raise FatalLiikesimError(f"连接发生错误：{e}")

