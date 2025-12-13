from math import sqrt, sin, cos, pi
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from . import constants

def latitude_to_angular_velocity(latitude):
    """返回在当地东北天坐标系下的速度分量"""
    omega_north = constants.EARTH_ROTATION_RATE * cos(latitude)
    omega_up = constants.EARTH_ROTATION_RATE * sin(latitude)

    return [0, omega_north, omega_up]

def orbit_period(semimajor_axis):
    """根据轨道半长轴计算轨道周期"""
    # Kepler's Third laws of planetary motion
    return sqrt( 4*pi**2 * semimajor_axis**3 / constants.GM_EARTH )

def orbit_angular_rate(semimajor_axis):
    """根据轨道半长轴计算轨道角速度"""
    return 2*pi / orbit_period(semimajor_axis)

# https://en.wikipedia.org/wiki/Latitude#Latitude_on_the_ellipsoid



def orthogonality_error(A: np.ndarray):
    """
    计算矩阵 A 的正交性误差，基于 Frobenius 范数的偏离度计算。
    :param A: 方向余弦矩阵 (3x3)
    :return: 正交性误差（Frobenius 范数）,该数值越小，代表矩阵越接近正交。
    """
    if np.abs(np.linalg.det(A) - 1) > 1e-5:
        raise ValueError("输入矩阵的行列式应为1，表示为一个有效的旋转矩阵。")

    I = np.eye(A.shape[1])  # 单位矩阵
    error_matrix = A.T @ A - I  # 计算 A^T A 与 I 的差
    frobenius_norm = np.linalg.norm(error_matrix, 'fro')  # Frobenius 范数
    return frobenius_norm

def theta_deg_to_cos_matrix(theta_deg) -> np.ndarray:
    """
    将角度矩阵 (单位: deg) 转换为余弦矩阵。
    :param theta_deg: 3*3 角度矩阵 (单位: deg).
    :return: 余弦矩阵
    """
    theta_rad = np.deg2rad(theta_deg)
    dcm = np.cos(theta_rad)
    return dcm

def vector_angle(v1: npt.ArrayLike, v2: npt.ArrayLike) -> float:
    """
    计算两个矢量的夹角（单位：弧度）
    如果任意一个矢量为零向量，则抛出异常。
    """
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)

    # 防止除以零错误
    if norm_v1 == 0 or norm_v2 == 0:
        raise ValueError("One of the vectors is zero, cannot compute angle.")

    dot_product = np.dot(v1, v2)
    cos_theta = dot_product / (norm_v1 * norm_v2)
    # 防止数值误差导致cos_theta超出[-1, 1]
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    angle = np.arccos(cos_theta)

    return angle

def unit_vector(vector: npt.ArrayLike) -> np.ndarray:
    """ Returns the unit vector of the vector.  """
    vector = np.asarray(vector)
    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("Zero vector cannot be normalized.")
    return vector / norm

def sphere_unit_vector(latitude: float, longitude: float) -> np.ndarray:
    """
    计算球坐标系下的单位矢量。
    """

    x = np.cos(latitude) * np.cos(longitude)
    y = np.cos(latitude) * np.sin(longitude)
    z = np.sin(latitude)

    return np.array([x, y, z])

def dcm2quat(A_FG: np.ndarray) -> np.ndarray:
    """
    方向余弦矩阵到四元数的转换。与 MATLAB dcm2quat 定义一致。
    """
    A_GF = A_FG.T
    q_FG = R.from_matrix(A_GF).as_quat(scalar_first=True)

    return q_FG

def quat2dcm(q_FG: list):
    """
    四元数到方向余弦矩阵的转换。与 MATLAB quat2dcm 定义一致。
    """
    A_GF = R.from_quat(q_FG, scalar_first=True).as_matrix()

    return A_GF.T

def rotate_z(rot) -> np.ndarray:
    """
    绕 Z 轴旋转的方向余弦矩阵。
    :param rot: 旋转角度（弧度）
    :return: 方向余弦矩阵
    """
    # 2.164 (Markley 2014)
    return np.array([[ cos(rot),  sin(rot),  0],
                     [-sin(rot),  cos(rot),  0],
                     [        0,         0,  1]])

def rotate_y(rot) -> np.ndarray:
    """
    绕 Y 轴旋转的方向余弦矩阵。
    :param rot: 旋转角度（弧度）
    :return: 方向余弦矩阵
    """
    # 2.164 (Markley 2014)
    return np.array([[ cos(rot),  0,  -sin(rot)],
                     [        0,  1,         0],
                     [ sin(rot),  0,   cos(rot)]])

def rotate_x(rot) -> np.ndarray:
    """
    绕 X 轴旋转的方向余弦矩阵。
    :param rot: 旋转角度（弧度）
    :return: 方向余弦矩阵
    """
    # 2.164 (Markley 2014)
    return np.array([[ 1,         0,        0],
                     [ 0,  cos(rot),  sin(rot)],
                     [ 0, -sin(rot),  cos(rot)]])

def euler2dcm(seq: str, angles, degrees: bool = False):
    """
    将欧拉角转换为方向余弦矩阵。
    :param euler: 欧拉角列表 [phi, theta, psi]
    :param order: 欧拉角顺序
    :return: 方向余弦矩阵
    """
    r = R.from_euler(seq, angles, degrees).as_matrix().transpose()
    return r


def generate_spherical_points_golden_spiral_method(n):
    """黄金螺旋法，生成球面均匀分布的 n 个点。"""
    phi = (1 + np.sqrt(5)) / 2  # 黄金比例
    points = []
    for i in range(n):
        z = 1 - 2 * i / (n - 1)  # 均匀分布 z 值
        theta = np.arccos(z)  # Polar angle
        azimuth = 2 * np.pi * phi * i  # 经度角
        x = np.sin(theta) * np.cos(azimuth)
        y = np.sin(theta) * np.sin(azimuth)
        points.append((x, y, z))
    return np.array(points)

def tesla2gauss(tesla):
    """
    将特斯拉转换为高斯单位。
    :param tesla: 特斯拉值
    :return: 高斯值
    """
    return tesla * 10000

def gauss2tesla(gauss):
    """
    将高斯单位转换为特斯拉。
    :param gauss: 高斯值
    :return: 特斯拉值
    """
    return gauss / 10000

def rpm2radps(rpm):
    """
    将转速从 rpm 转换为 rad/s。
    :param rpm: 转速（单位：rpm）
    :return: 转速（单位：rad/s）
    """
    return rpm * 2 * np.pi / 60

def radps2rpm(radps):
    """
    将转速从 rad/s 转换为 rpm。
    :param radps: 转速（单位：rad/s）
    :return: 转速（单位：rpm）
    """
    return radps * 60 / (2 * np.pi)


def solve_triangle_ASS(A_deg, a, b):
    """
    求解三角形角边边（Angle-Side-Side, ASS）情形
    """
    A_rad = np.radians(A_deg)
    sinB = b * np.sin(A_rad) / a

    # 检查是否有解
    if sinB > 1:
        return "无解"
    elif np.isclose(sinB, 1):
        B1_rad = np.pi / 2
        B1_deg = 90.0
        C_deg = 180 - A_deg - B1_deg
        C_rad = np.radians(C_deg)
        c = a * np.sin(C_rad) / np.sin(A_rad)
        return [{"A": A_deg, "B": B1_deg, "C": C_deg, "a": a, "b": b, "c": c}]
    else:
        B1_rad = np.arcsin(sinB)
        B1_deg = np.degrees(B1_rad)
        solutions = []

        # 解1：B1
        C1_deg = 180 - A_deg - B1_deg
        if C1_deg > 0:
            C1_rad = np.radians(C1_deg)
            c1 = a * np.sin(C1_rad) / np.sin(A_rad)
            solutions.append({"A": A_deg, "B": B1_deg, "C": C1_deg, "a": a, "b": b, "c": c1})

        # 解2：B2 = 180 - B1
        B2_deg = 180 - B1_deg
        C2_deg = 180 - A_deg - B2_deg
        if C2_deg > 0:
            C2_rad = np.radians(C2_deg)
            c2 = a * np.sin(C2_rad) / np.sin(A_rad)
            solutions.append({"A": A_deg, "B": B2_deg, "C": C2_deg, "a": a, "b": b, "c": c2})

        return solutions


def test():
    q = [0.7071, 0.7071, 0, 0]

    A = quat2dcm(q)

    print(A)

    print(dcm2quat(A))

    # 生成100个点
    points = generate_spherical_points_golden_spiral_method(1000)

    # 绘制3D球面点
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=10)
    ax.set_box_aspect([1, 1, 1])
    # plt.show()

    print(rotate_x(0.1) @ rotate_y(0.2) @ rotate_z(0.3) - euler2dcm('ZYX', [0.3, 0.2, 0.1]))
    print(rotate_z(0.1) @ rotate_y(0.2) @ rotate_x(0.3) - euler2dcm('XYZ', [0.3, 0.2, 0.1]))

if __name__ == "__main__":
    # python -m src.aocs_lab.utils.lib
    test()