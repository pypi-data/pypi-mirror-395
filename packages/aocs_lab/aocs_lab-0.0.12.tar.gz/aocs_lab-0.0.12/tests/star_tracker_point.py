"""穷举找到满足需求的星敏指向"""
import sys
import os
import time
from dataclasses import dataclass
import numpy as np
# import matplotlib.pyplot as plt
# from scipy.spatial.transform import Rotation as R


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(parent_dir)
import aocs_lab.utils.lib as lib
import aocs_lab.utils.time as time_utils



def get_angle_min(points):
    """计算点集中两两点之间的最小夹角"""
    points_num = len(points)
    start_time = time.time()

    angle_min_list = []
    for i, point_i in enumerate(points):
        angle_min = np.pi
        for j, point_j in enumerate(points):
            if i != j:
                # angle = lib.vector_angle(point_i, point_j)
                angle = np.acos(np.clip(np.dot(point_i, point_j), -1, 1))
                angle_min = min(angle, angle_min)

            if j % 1000 == 0:
                time_utils.print_percentage(i * points_num + j, points_num * points_num, start_time)

        angle_min_list.append(angle_min)

    return max(angle_min_list)


def gen_sphere_unit_vector_list() -> list:
    """生成球面单位矢量列表"""
    n = []
    for lat in range(-89, 90, 1):
        for lon in range(0, 360, 1):
            n.append(lib.sphere_unit_vector(np.deg2rad(lat), np.deg2rad(lon)))

    # 添加极点
    n.append(lib.sphere_unit_vector(np.deg2rad(-90), np.deg2rad(0)))
    n.append(lib.sphere_unit_vector(np.deg2rad(90), np.deg2rad(0)))

    return n



@dataclass
class VectorInOrbit:
    """轨道坐标系中的矢量及姿态信息"""
    sun: np.array = np.zeros(3)
    dcm_bo: np.array = np.zeros(3,3)

@dataclass
class AttMode:
    """综合一圈轨道的太阳矢量的姿态信息"""
    earth: np.array = np.array([0, 0, 1])

    position: list[VectorInOrbit] = None

    def init(self, beta):
        self.position = []
        for u in range(0, np.deg2rad(360), np.deg2rad(1)):
            sun = np.array([np.cos(np.deg2rad(beta)), np.sin(np.deg2rad(beta)), 0])
            dcm_bo = np.array([[1,0,0],[0,1,0],[0,0,1]])
            self.position.append(VectorInOrbit(sun, dcm_bo))

def get_valid_star_point(points_1, points_2, att_mode: AttMode):
    """根据定义的轨道和姿态，获取有效的星敏指向列表"""

    points_1_valid = []
    points_2_valid = []
    return points_1_valid, points_2_valid

if __name__ == "__main__":
    points = gen_sphere_unit_vector_list()

    # points_in_equ = [point for point in points if np.abs(point[2]) < 0.1]
    # angle_min = get_angle_min(points_in_equ)
    # print(f"\nangle_min: {np.rad2deg(angle_min):.2f} deg")

    print(len(gen_sphere_unit_vector_list()))


# 用经纬度遍历的方法，经纬度步长均为 1 deg，共 64800 个点
# 用螺旋法生成平均间隔 1 deg 的点，需要约 40000 个点，没有太大的改善
