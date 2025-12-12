from __future__ import print_function
from __future__ import absolute_import

from .utils import *
from .exceptions import FatalLiikesimError
from . import  _vehicle
from . import connection


vehicle = _vehicle.VehicleDomain()
_timeStep = 1.0

def start(net_xml: str, timing_xml: str = "", ts: float = 1, host='localhost', port=7000, timeout=10):
    connect(host, port, timeout)
    startSimulation(net_xml, timing_xml, ts)


def connect(host, port, timeout):
    if not connection.isConnected():
        try:
            connection.Connection(host, port, timeout)
        except FatalLiikesimError as e:
            raise e


def startSimulation(net_xml: str, timing_xml: str, ts: float):
    """
    启动仿真。
    Parameters:
    net_xml: str, 路网XML文件绝对路径。
    timing_xml: str, 配时XML文件绝对路径，若无传参，默认为空；配时文件可为空，因为有时候配时文件会直接加在路网文件里。
    time_step:float, 仿真步长，须为1/n，n是正整数，例如0.1、0.2、0.5；默认为1.0。
    """
    clientRequestParameter = {
        "roadNetworkXmlFilePath": str(net_xml),
        "signalTimingXmlFilePath": str(timing_xml),
        "timeStep": float(ts)
    }
    message = formatMessage("startSimulation", clientRequestParameter)
    response = connection.send(message)
    if "开启仿真成功" in response:
        global _timeStep
        _timeStep = ts
    else:
        raise FatalLiikesimError(response)
