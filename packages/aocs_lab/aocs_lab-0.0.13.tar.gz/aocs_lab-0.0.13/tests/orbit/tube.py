import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.dates as mdates
from datetime import timedelta, datetime
import re


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.append(parent_dir)
import aocs_lab.utils.lib as lib
import aocs_lab.sun_time as sun_time
import aocs_lab.utils.constants as const



def calc_dnda(a):
    """
    :param a: 轨道半长轴
    :return: 轨道角速度变化量与轨道半长轴变化量之比
    """
    n = lib.orbit_angular_rate(a)
    return -3*n / (2*a)

def calc_du(a, da0, da_dot, du0, t):
    k = calc_dnda(a)
    du = k * (da0 * t + 0.5 * da_dot * t**2) + du0
    return du

def calc_da(da0, da_dot, t):
    """
    计算轨道半长轴变化量
    :param da0: 初始轨道半长轴变化量
    :param da_dot: 轨道半长轴变化率
    :param t: 时间
    :return: 轨道半长轴变化量
    """
    return da0 + da_dot * t

def plot_tube(a, du, da, dix, diy):
    _, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))  # 创建两个纵向子图

    # 第一个子图
    ax[0].plot(a * du, da, label='du', color='blue')
    ax[0].set_xlabel('a*du (m)')
    ax[0].set_ylabel('da (m)')
    ax[0].set_title('a*du vs da')
    ax[0].grid(True)
    ax[0].legend()
    ax[0].set_aspect('equal')

    # 第二个子图
    ax[1].plot(a*diy, da, color='green')
    ax[1].set_xlabel('a*diy (m)')
    ax[1].set_ylabel('da (m)')
    ax[1].set_title('a*diy vs da')
    ax[1].grid(True)
    ax[1].legend()
    ax[1].set_aspect('equal')

    # 标记x轴最大值和最小值对应的点
    x_vals = a * diy
    idx_max = np.argmax(x_vals)
    idx_min = np.argmin(x_vals)
    ax[1].scatter(x_vals[idx_max], da[idx_max], color='red', marker='o', label='x max')
    ax[1].scatter(x_vals[idx_min], da[idx_min], color='orange', marker='o', label='x min')
    # 在图中标注横纵坐标
    ax[1].annotate(f"({x_vals[idx_max]:.2f}, {da[idx_max]:.2f})",
                   (x_vals[idx_max], da[idx_max]),
                   textcoords="offset points", xytext=(10,10), ha='left', color='red')
    ax[1].annotate(f"({x_vals[idx_min]:.2f}, {da[idx_min]:.2f})",
                   (x_vals[idx_min], da[idx_min]),
                   textcoords="offset points", xytext=(10,-20), ha='left', color='orange')
    ax[1].legend()

    # 添加半径为250m的圆
    theta = np.linspace(0, 2 * np.pi, 200)
    circle_x = 250 * np.cos(theta)
    circle_y = 250 * np.sin(theta)
    ax[1].plot(circle_x, circle_y, 'r--', label='r=250m')
    ax[1].legend()

    plt.tight_layout()
    plt.show()

def test():
    # 轨道半长轴
    a = 6913e3
    # 轨道半长轴变化量
    da0 = 100
    # 轨道半长轴变化率
    da_dot = -200 / 86400
    # 时间
    t = 86400/2

    du0 = 1700 / a

    du = calc_du(a, da0, da_dot, du0, t)
    da = calc_da(da0, da_dot, t)

    k = const.EARTH_ROTATION_RATE / lib.orbit_angular_rate(a)

    dix = np.deg2rad(0.001)
    diy = du * k

    en_max = a * np.sqrt(dix**2 + diy**2)
    er_max = da
    e_max = np.sqrt(en_max**2 + er_max**2)

    print(f"da: {da:0.1f} m")
    print(f"du: {du} rad")
    print(f"a*du: {a*du:0.1f} m")
    print(f"er_max: {er_max:0.1f} m")
    print(f"en_max: {en_max:0.1f} m")
    print(f"e_max: {e_max:0.1f} m")

    t = np.arange(0, 86400, 60)
    du = calc_du(a, da0, da_dot, du0, t)
    da = calc_da(da0, da_dot, t)
    diy = du * k

    plot_tube(a, du, da, 0, diy)


if __name__ == "__main__":
    test()
