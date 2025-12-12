from __future__ import absolute_import
from typing import List
from .utils import *
from . import connection
from .exceptions import LiikesimException


class Vehicle:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "speed" or key == "lastSpeed" or key == "acceleration" or key == "position" or key == "lateralOffset" or key == "xCoordinate" or key == "yCoordinate" or key == "zCoordinate" or key == "angle" or key == "distance" or key == "length" or key == "width" or key == "maxSpeed" or key == "maxAccel" or key == "maxDecel":
                value = float(value)
            elif key == "isTransfer":
                value = bool(value)
            elif key == "edgeId" or key == "laneId" or key == "routeEdgeId" or key == "nextEdgeId":
                value = int(value)
            elif key == "vehicleType":
                value = str(value)
            elif key == "targetLaneIdList":
                if value == "[]":
                    value = []
                else:
                    tempList = value.strip("[]").split(",")
                    value = [int(temp.strip("\n\r\t ")) for temp in tempList]
            else:
                raise ValueError(f"未知参数类型: {key}")
            setattr(self, f"_{key}", value)
        self._initialized = True

    def __getattr__(self, name):
        private_name = f"_{name}"
        try:
            return super().__getattribute__(private_name)
        except AttributeError:
            raise AttributeError(f"未获取车辆的{name}参数")

    def __setattr__(self, name, value):
        if hasattr(self, '_initialized') and self._initialized:
            raise AttributeError(f"不允许设置车辆的任何参数")
        else:
            super().__setattr__(name, value)



class VehicleDomain():

    def getInfo(self, vehID: str, attr: List[str]):
        """
        获取单个指定车辆在当前仿真步的指定信息。

        Parameters:
        vehicle_id: str, 车辆名，唯一标识符。
        attributes: List[str], 要获取的车辆参数列表，支持以下参数：
        {
        "speed":车辆当前仿真步的速度（单位：米（m））,float
        "lastSpeed":车辆上一个仿真步的速度（单位：米/秒（m/s））,float
        "acceleration":车辆当前仿真步的加速度（单位：米/秒^2（m/s^2））,float
        "isTransfer":车辆当前仿真步是否正在交叉口,bool
        "edgeId": 车辆当前仿真步所在的路段编号,int
        "laneId":车辆当前仿真步所在的车道编号,int
        "position":车辆当前仿真步所在的路段位置（若在路段上）/连接器位置（若在连接器上）（单位：米（m））,float
        "lateralOffset":车辆当前仿真步在车道上的横向偏移量（单位：米（m））,float
        "xCoordinate":车辆（中心）当前仿真步的x坐标,float
        "yCoordinate":车辆（中心）当前仿真步的y坐标,float
        "zCoordinate":车辆（中心底盘）当前仿真步的z坐标,float
        "angle":车辆当前仿真步的朝向角度（单位：角度（°））,float
        "routeEdgeId":车辆当前的目标路由路段编号,int,注意若不存在目标路由，则返回-1
        "nextEdgeId":车辆当前的下一路段编号,int,注意若不存在下一路段，则返回-1
        "targetLaneIdList":车辆在当前路段上行驶，由于路由规划、障碍物、车辆类型限制等原因，需要换道到应该行驶的车道列表，List[int]
        "distance":截至当前仿真步，车辆在路网中行驶的距离（单位：米（m））,float
        "length":车辆的长度（单位：米（m））,float
        "width":车辆的宽度（单位：米（m））,float
        "maxSpeed":车辆的最大速度（单位：米（m））,float
        "maxAccel":车辆的最大加速度（单位：米/秒^2（m/s^2））,float
        "maxDecel":车辆的最大减速度（单位：米/秒^2（m/s^2））,float
        "vehicleType":车辆的类型,str
        }

        Returns:
        vehicle: Vehicle, 车辆对象，仅包含指定参数的信息，通过{vehicle.参数名}能获取相应参数信息，例如：vehicle.speed为车辆当前仿真步的速度。

        注意：返回对象的参数不允许进行修改
        """
        clientRequestParameter = {
            "vehicleId": str(vehID),
            "attributes": attr
        }
        message = formatMessage("getSingleVehicleInfo", clientRequestParameter)
        response = connection.send(message)
        if "获取车辆信息失败" not in response:
            vehicle_info = json.loads(response)
            vehicle = Vehicle(**vehicle_info)
            return vehicle
        else:
            raise LiikesimException(response)

