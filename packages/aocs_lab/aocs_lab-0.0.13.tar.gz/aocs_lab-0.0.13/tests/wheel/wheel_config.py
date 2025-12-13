"""飞轮配置设计"""
import itertools
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def plot_wheel_config(n: np.ndarray):
    """绘制飞轮配置"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(0, 0, 0, 1, 0, 0, color='b', label='x')
    ax.quiver(0, 0, 0, 0, 1, 0, color='b', label='y')
    ax.quiver(0, 0, 0, 0, 0, 1, color='b', label='z')
    ax.text(1, 0, 0, 'x', color='b')
    ax.text(0, 1, 0, 'y', color='b')
    ax.text(0, 0, 1, 'z', color='b')

    ax.quiver(0, 0, 0, n[0], n[1], n[2], color='r')
    ax.quiver(0, 0, 0, n[0], n[1], -n[2], color='g')
    ax.quiver(0, 0, 0, n[0], -n[1], n[2], color='k')
    ax.quiver(0, 0, 0, n[0], -n[1], -n[2], color='y')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    ax.set_aspect('equal', adjustable='box')  # 使用 'box' 以保持轴标签的比例·
    plt.grid()
    plt.show()


def calc_wheel_config(inertial: np.ndarray, omega: np.ndarray):
    """计算飞轮配置"""
    # 主轴惯量
    # 角速度需求

    h = inertial * omega
    n = h / np.linalg.norm(h)

    ny = np.array([1, -1, 1])
    nz = np.array([1, 1, -1])

    wheel_n = []
    wheel_n.append(n)
    wheel_n.append(n*ny)
    wheel_n.append(n*nz)
    wheel_n.append(n*ny*nz)

    print(f"三轴动量需求: [{h[0]:.3f}, {h[1]:.3f}, {h[2]:.3f}] Nms")
    print(f"飞轮角动量需求: {np.linalg.norm(h):.3f} Nms")
    print("本体系下飞轮角动量方向单位矢量")
    for i, v in enumerate(wheel_n):
        print(f"飞轮 {i}: [{v[0]:6.3f}, {v[1]:6.3f}, {v[2]:6.3f}]", end=' ')
        print(f"或 [{-v[0]:6.3f}, {-v[1]:6.3f}, {-v[2]:6.3f}]")

    return n

def wheels_envelope(wheel_n: np.ndarray):
    """
    飞轮包络线
    
    arg:
        wheel_n: 飞轮角动量方向单位矢量 (N*3), N 为飞轮个数
    """
    wheel_num = wheel_n.shape[0]

    ratio = np.linspace(-1, 1, 2)
    ratio_all = list(itertools.product(ratio, repeat=wheel_num))# 使用product生成所有可能

    envelope = np.zeros((len(ratio_all), 3))
    for i, ratio in enumerate(ratio_all):
        ratio = np.array(ratio)
        for j in range(wheel_num):
            envelope[i] += ratio[j] * wheel_n[j]

    # 画图
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(0, 0, 0, 3, 0, 0, color='b', label='x')
    ax.quiver(0, 0, 0, 0, 3, 0, color='b', label='y')
    ax.quiver(0, 0, 0, 0, 0, 3, color='b', label='z')
    ax.text(3, 0, 0, 'x', color='b')
    ax.text(0, 3, 0, 'y', color='b')
    ax.text(0, 0, 3, 'z', color='b')

    # 绘制包络多边形顶点
    for i, ratio in enumerate(ratio_all):
        ax.scatter(envelope[i][0], envelope[i][1], envelope[i][2], color='k', alpha=0.9)

    plot_surface(ax, envelope)

    # 绘制飞轮角动量方向
    for i in range(wheel_num):
        ax.quiver(0, 0, 0, wheel_n[i][0], wheel_n[i][1], wheel_n[i][2], color='r')
        ax.quiver(0, 0, 0, -wheel_n[i][0], -wheel_n[i][1], -wheel_n[i][2], color='g')
        ax.text(wheel_n[i][0], wheel_n[i][1], wheel_n[i][2],
                f"w{i}", color='r', fontsize=10)
        ax.text(-wheel_n[i][0], -wheel_n[i][1], -wheel_n[i][2],
                f"w{i}", color='g', fontsize=10)

    lim = 3
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.set_aspect('equal', adjustable='box')  # 使用 'box' 以保持轴标签的比例·
    plt.grid()
    plt.show()

def plot_surface(ax, points):
    """绘制3D凸包表面"""
    # 计算凸包
    hull = ConvexHull(points)

    print(f"volume: {hull.volume:.1f}")
    print(f"area: {hull.area:.1f}")

    # 提取每一个面（hull.simplices 是三角形的点索引）
    faces = [points[simplex] for simplex in hull.simplices]

    # 绘制面
    poly3d = Poly3DCollection(faces, alpha=0.5, edgecolor='k')
    poly3d.set_facecolor('cyan')
    ax.add_collection3d(poly3d)


def test_wheels_envelope():
    """测试飞轮包络线"""
    # wheel_n = np.array([[1, 0, 0],
    #                 [0, 1, 0],
    #                 [0, 0, 1],
    #                 [-0.577, -0.577, 0.577]])
    
    # wheel_n = np.array([[0.577, 0.577, 0.577],
    #                     [-0.577, 0.577, 0.577],
    #                     [0.577, -0.577, 0.577],
    #                     [-0.577, -0.577, 0.577]])
    
    # 中科 1+7 BCD星
    wheel_n = np.array([[ 0.229,  0.688,  0.688],
                        [ 0.229, -0.688,  0.688],
                        [ 0.229,  0.688, -0.688],
                        [ 0.229, -0.688, -0.688]])

    # wheel_n = np.array([[1, 0, 0],
    #                 [0, 1, 0],
    #                 [0, 0, 1]])
    wheels_envelope(wheel_n)
    print("飞轮包络线测试完成")


if __name__ == "__main__":

    # wheel_v = calc_wheel_config(
    #     inertial=np.array([100, 300, 300]),
    #     omega=np.array(np.deg2rad([1, 1, 1])))

    # plot_wheel_config(wheel_v)

    test_wheels_envelope()
