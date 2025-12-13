"""分析对日姿态的能源效率"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(parent_dir)
from aocs_lab.utils.lib import vector_angle, orbit_period, euler2dcm
import aocs_lab.utils.constants as constants

SEMIMAJAR_AXIS = 6913.49e3  # 卫星轨道半长轴
SAMPLE_TIME = 10  # 采样时间
sample_num = int(orbit_period(SEMIMAJAR_AXIS) / SAMPLE_TIME)  # 一轨周期采样点数

def sun_cone_in_vvlh(beta_angle: float) -> list:
    """
    计算太阳矢量在VVLH系的圆锥遍历
    返回太阳单位矢量列表
    """

    phi_line = np.linspace(0, 2*np.pi, sample_num)

    v_sun_cone = []
    for phi in phi_line:
        y = np.sin(beta_angle)
        xz = np.cos(beta_angle)
        v_sun = np.array([xz*np.sin(phi), y, xz*np.cos(phi)])

        v_sun_cone.append(v_sun)

    return v_sun_cone


def sun_vector_in_light(v_sun_cone: list, semimajor_axis: float) -> list:
    """计算太阳矢量在光照区遍历"""
    v_earth = np.array([0, 0, 1])
    v_sun_in_light_index = []
    for index, v_sun in enumerate(v_sun_cone):
        earth_sun_angle = vector_angle(v_earth, v_sun)
        if earth_sun_angle > np.arcsin(constants.EARTH_EQUATORIAL_RADIUS/semimajor_axis):
            v_sun_in_light_index.append(index)

    return v_sun_in_light_index

def calc_panel_normal(v_sun_unit: np.ndarray) -> np.ndarray:
    """计算太阳帆板法向"""
    v_earth_unit = np.array([0,0,1])

    sun_on_z = np.dot(v_earth_unit, v_sun_unit) * v_earth_unit
    sun_on_xy_plane = v_sun_unit - sun_on_z
    sun_on_xy_plane_unit = sun_on_xy_plane / np.linalg.norm(sun_on_xy_plane)

    if v_sun_unit[2] < 0:
        v_panel = 2.2*v_sun_unit + sun_on_xy_plane_unit
    else:
        v_panel = v_sun_unit + 3*sun_on_xy_plane_unit
    # v_panel[0] = np.abs(v_panel[0]) * v_panel[0]
    v_panel_unit = v_panel / np.linalg.norm(v_panel)

    return v_panel_unit

def calc_sun_att(v_panel_normal_unit: np.ndarray) -> Rotation:
    """计算约束对日姿态"""
    v_earth_unit = np.array([0, 0, 1])

    y_unit = - v_panel_normal_unit
    x = np.cross(y_unit, v_earth_unit)
    x_unit = x / np.linalg.norm(x)
    z = np.cross(x_unit, y_unit)
    z_unit = z / np.linalg.norm(z)

    dcm_bo = np.array([x_unit, y_unit, z_unit])
    # rot = Rotation.from_matrix([x_unit, y_unit, z_unit])

    # print(rot.as_rotvec(degrees=True))

    return dcm_bo

def calc_att_angular_rate(att_bo: np.ndarray, att_blast_o: np.ndarray, dt: float) -> np.ndarray:
    """计算姿态角速度"""
    att_b_blast =  att_bo @ att_blast_o.transpose()
    rot = Rotation.from_matrix(att_b_blast)
    att_rate = rot.as_rotvec() / dt

    return att_rate

def calc_att_angular_acceleration(
        att_rate: np.ndarray,
        att_rate_last: np.ndarray,
        dt: float) -> np.ndarray:
    """计算姿态角加速度"""
    att_acceleration = (att_rate - att_rate_last) / dt

    return att_acceleration


def panel_normal_cone(v_sun_cone: list) -> list:
    """计算太阳帆板法向圆锥"""
    panel_n_cone = []
    for v_sun in v_sun_cone:
        panel_normal = calc_panel_normal(v_sun)
        panel_n_cone.append(panel_normal)

    return panel_n_cone


def energy_efficiency(
        sun_cone: list,
        sun_cone_in_light_index: list,
        panel_n_cone: list) -> float:
    """计算能源效率"""
    sun_cone_in_light = [sun_cone[i] for i in sun_cone_in_light_index]
    panel_normal_cone_in_light = [panel_n_cone[i] for i in sun_cone_in_light_index]

    energy_one_orbit = 0
    for v_sun in sun_cone:
        energy_one_orbit += 1

    energy_in_light = 0
    for v_sun in sun_cone_in_light:
        energy_in_light += 1

    energy_real = 0
    for panel_normal, v_sun in zip(panel_normal_cone_in_light, sun_cone_in_light):
        energy_real += np.cos(vector_angle(v_sun, panel_normal))

    print(f"光照区能量总量 与 一轨能量之比: {100 * energy_in_light/energy_one_orbit:.1f} %")
    print(f"实际能量 与 光照区能量总量之比: {100 * energy_real/energy_in_light:.1f} %")

def anlyse_sun_att(panel_n_cone: list):
    """分析对日姿态"""
    att_last = Rotation.from_euler('ZYX', [0, 0, 0]).as_matrix()
    att_rate_last = np.array([0, 0, 0])

    att_rate_list = []
    att_acceleration_list = []

    for index, v_panel in enumerate(panel_n_cone) :
        att_bo = calc_sun_att(v_panel)
        att_rate = calc_att_angular_rate(att_bo, att_last, SAMPLE_TIME)
        att_acceleration = calc_att_angular_acceleration(att_rate, att_rate_last, SAMPLE_TIME)

        if index > 0:
            att_rate_list.append(att_rate)

        if index > 1:
            att_acceleration_list.append(att_acceleration)

        att_last = att_bo
        att_rate_last = att_rate

    timeline = np.linspace(0, SAMPLE_TIME*len(att_rate_list), len(att_rate_list))
    print(len(att_rate_list))
    _, ax = plt.subplots(2, 1)
    ax[0].plot(timeline, np.rad2deg(att_rate_list))
    ax[0].set_title('Attitude Rate')
    ax[0].set_xlabel('Time (s)')
    ax[0].set_ylabel('Attitude Rate (deg/s)')
    ax[0].grid()
    ax[0].legend(['x', 'y', 'z'])
    # mark_max_min(ax[0], timeline, np.rad2deg(att_rate_list))
    plt.subplots_adjust(hspace=0.35)  # 增加两幅图的纵向间距
    timeline = np.linspace(0, SAMPLE_TIME*len(att_acceleration_list), len(att_acceleration_list))
    ax[1].plot(timeline, np.rad2deg(att_acceleration_list))
    ax[1].set_title('Attitude Acceleration')
    ax[1].set_xlabel('Time (s)')
    ax[1].set_ylabel('Attitude Acceleration (deg/s^2)')
    ax[1].legend(['x', 'y', 'z'])
    ax[1].grid()
    # mark_max_min(ax[1], timeline, np.rad2deg(att_acceleration_list))
    plt.show(block=False)

def plot_sun_cone(
        sun_cone: list,
        sun_cone_in_light_index: list,
        panel_n_cone: list):
    """绘制太阳矢量圆锥"""
    sun_cone_in_light = [sun_cone[i] for i in sun_cone_in_light_index]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('Sun Cone in VVLH')
    for v_sun in sun_cone:
        ax.quiver(0, 0, 0, v_sun[0], v_sun[1], v_sun[2], arrow_length_ratio=0.1)

    for v_sun in sun_cone_in_light:
        ax.quiver(0, 0, 0, v_sun[0], v_sun[1], v_sun[2], color='r', arrow_length_ratio=0.1)

    for v_sun in panel_n_cone:
        ax.quiver(0, 0, 0, v_sun[0], v_sun[1], v_sun[2], color='g', arrow_length_ratio=0.1)

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    ax.set_aspect('equal', adjustable='box')  # 使用 'box' 以保持轴标签的比例·
    plt.show(block=False)

    angle_light = []
    angle_shadow = []
    roll_angle = []
    for index, (v_sun, v_panel) in enumerate(zip(sun_cone, panel_n_cone)):
        if index in sun_cone_in_light_index:
            angle_light.append(vector_angle(v_sun, v_panel))
        else:
            angle_shadow.append(vector_angle(v_sun, v_panel))
        roll_angle.append(np.pi/2 - vector_angle(v_panel, np.array([0, 0, -1])))

    print(f"阳照区太阳与帆板法向夹角最大值: {np.rad2deg(max(angle_light)):.2f} deg")
    print(f"阴影区太阳与帆板法向夹角最大值: {np.rad2deg(max(angle_shadow)):.2f} deg")
    print(f"滚转角最大值: {np.rad2deg(max(roll_angle)):.2f} deg")
    print(f"滚转角最小值: {np.rad2deg(min(roll_angle)):.2f} deg")

    # fig = plt.figure()
    # ax = fig.add_subplot()
    # ax.plot(np.rad2deg(angle_light))
    # ax.plot(np.rad2deg(angle_shadow))
    # ax.grid()
    # plt.show(block=False)

    return roll_angle

def plot_orbit_frame(ax: plt.Axes):
    """绘制轨道坐标系"""
    ax.quiver(-1, 0, 2, 0, color="b", scale=1, scale_units="xy")
    ax.quiver(0, 1, 0, -2, color="b", scale=1, scale_units="xy")
    ax.text(1, 0 - 0.1, "$y_O$", fontsize=10, color="b")
    ax.text(0, -1 - 0.1, "$z_O$", fontsize=10, color="b")
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    ax.set_xticks([])  # 删除x轴刻度
    ax.set_yticks([])  # 删除y轴刻度
    ax.grid(False)     # 删除网格

    # 绘制太阳矢量
    beta_min = 4.6 # deg
    beta_max = 19.2 # deg

    ax.quiver(0,0,
            np.cos(np.deg2rad(beta_min+90)),
            np.sin(np.deg2rad(beta_min+90)),
            color="y", scale=0.9, scale_units="xy")

    ax.text(np.cos(np.deg2rad(beta_min+90))-0.2,
            np.sin(np.deg2rad(beta_min+90))+0.2,
            "$sun$", fontsize=10, color="y")

    ax.quiver(0,0,
            np.cos(np.deg2rad(beta_max + 90)),
            np.sin(np.deg2rad(beta_max + 90)),
            color="y", scale=0.9, scale_units="xy")

def rotate_2d_vector(vector, alpha):
    """
    旋转二维向量
    Args:
        vector: 要旋转的二维向量 (x, y)
        alpha: 旋转角度（弧度制）绕z轴旋转为正
    Returns:
        旋转后的二维向量
    """
    # 定义旋转矩阵
    rotation_matrix = np.array([
        [np.cos(alpha), -np.sin(alpha)],
        [np.sin(alpha),  np.cos(alpha)]
    ])

    # 进行矩阵乘法
    rotated_vector = np.dot(rotation_matrix, vector)
    return rotated_vector

def plot_body_frame(ax: plt.Axes, roll_angle: float):
    """
    绘制卫星本体坐标系，YOZ平面
    Args:
        roll_angle: 旋转角度（弧度制）绕z轴旋转为正
    """
    gnss_install_angle = np.deg2rad(0)
    gnss_vector = np.array([np.sin(gnss_install_angle), np.cos(gnss_install_angle)])
    start_points_y = np.array([-1,0])
    start_points_z = np.array([0,1])
    end_points_y = np.array([1, 0])
    end_points_z = np.array([0, -1])

    ax.quiver(rotate_2d_vector(start_points_y, -roll_angle),
              rotate_2d_vector(start_points_z, -roll_angle),
              rotate_2d_vector(end_points_y-start_points_y, -roll_angle),
              rotate_2d_vector(end_points_z-start_points_z, -roll_angle),
              color="r", scale=1, scale_units="xy")

    end_points_y_roll = rotate_2d_vector(end_points_y, -roll_angle)
    end_points_z_roll = rotate_2d_vector(end_points_z, -roll_angle)

    ax.text(end_points_y_roll[0], end_points_z_roll[0]-0.1, "$y_B$", fontsize=10, color="r")
    ax.text(end_points_y_roll[1], end_points_z_roll[1]-0.1, "$z_B$", fontsize=10, color="r")

    # # 绘制GNSS天线方向
    # gnss_vector_roll = rotate_2d_vector(gnss_vector, -roll_angle)
    # ax.quiver(0,0,
    #           gnss_vector_roll[0],
    #           gnss_vector_roll[1],
    #           color="g", scale=0.9, scale_units="xy")

    # gnss_up_angle = vector_angle(gnss_vector_roll, np.array([0, 1]))
    # ax.text(-1, -1.2, f"GNSS angle: {np.rad2deg(gnss_up_angle):.1f} deg", fontsize=10)

    # 绘制星敏光轴方向
    # star_tracker_angle = [np.deg2rad(40), np.deg2rad(120)]
    # star_tracker_vector = []
    # star_tracker_vector.append([np.cos(star_tracker_angle[0]), np.sin(star_tracker_angle[0])]) 
    # star_tracker_vector.append([np.cos(star_tracker_angle[1]), np.sin(star_tracker_angle[1])])

    # star_tracker_vector_roll = []
    # star_tracker_vector_roll.append(rotate_2d_vector(star_tracker_vector[0], -roll_angle))
    # star_tracker_vector_roll.append(rotate_2d_vector(star_tracker_vector[1], -roll_angle))
    # ax.quiver(0,0,
    #           star_tracker_vector_roll[0][0],
    #           star_tracker_vector_roll[0][1],
    #           color="g", scale=0.9, scale_units="xy")
    # ax.quiver(0,0,
    #           star_tracker_vector_roll[1][0],
    #           star_tracker_vector_roll[1][1],
    #           color="g", scale=0.9, scale_units="xy")

    # ax.text(star_tracker_vector_roll[0][0],
    #         star_tracker_vector_roll[0][1]+0.1,
    #         "star_A", fontsize=10, color="g")
    # ax.text(star_tracker_vector_roll[1][0],
    #         star_tracker_vector_roll[1][1]+0.1,
    #         "star_B", fontsize=10, color="g")

    ax.text(-1, -1.3, f"roll angle: {np.rad2deg(roll_angle):.1f} deg", fontsize=10)



def plot_body_in_orbit_frame(sun_light_roll: float, sun_shadow_roll: float):
    """
    绘制卫星在轨道坐标系中的姿态
    """
    _, ax = plt.subplots(2, 2, figsize=(10, 8))

    ax[0, 0].set_title("sun - light")
    plot_orbit_frame(ax[0, 0])
    plot_body_frame(ax[0, 0], sun_light_roll)

    ax[0, 1].set_title("sun - shadow")
    plot_orbit_frame(ax[0, 1])
    plot_body_frame(ax[0, 1], sun_shadow_roll)

    ax[1, 0].set_title("earth - left swing")
    plot_orbit_frame(ax[1, 0])
    plot_body_frame(ax[1, 0], np.deg2rad(30))

    ax[1, 1].set_title("earth - right swing")
    plot_orbit_frame(ax[1, 1])
    plot_body_frame(ax[1, 1], np.deg2rad(-30))

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show the plot
    plt.show(block=False)
    plt.savefig("att_in_orbit_frame.png", dpi=300)  # 保存为高分辨率图片

def check_star_tracker():
    """检查星敏光轴视场（与太阳和地球的夹角）"""
    # 星敏光轴矢量定义
    a1 = np.deg2rad(33)
    a2 = np.deg2rad(43)
    s1_b = np.array([ np.sin(a1), -np.cos(a1)*np.cos(a2), -np.cos(a1)*np.sin(a2)])
    s2_b = np.array([-np.sin(a1), -np.cos(a1)*np.cos(a2), -np.cos(a1)*np.sin(a2)])
    s_b_list = [s1_b, s2_b]

    # 检查约束对日星敏的视场
    beta = -19.2
    sun_cone = sun_cone_in_vvlh(np.deg2rad(beta))
    panel_n_cone = panel_normal_cone(sun_cone)
    r_bo_list = [calc_sun_att(panel_n) for panel_n in panel_n_cone]
    calc_star_tracker_field_of_view(s_b_list, sun_cone, r_bo_list, f'Sun Attitude, beta={beta} deg')

    # 检查对地模式星敏的视场
    # 右侧视
    r_bo_list = [euler2dcm('ZYX', [3.8, 0, -30], degrees=True) for _ in range(len(sun_cone))]
    calc_star_tracker_field_of_view(s_b_list, sun_cone, r_bo_list, f'Right Swing 30 deg, beta={beta} deg')

    # 左侧视
    r_bo_list = [euler2dcm('ZYX', [3.8, 0, 30], degrees=True) for _ in range(len(sun_cone))]
    calc_star_tracker_field_of_view(s_b_list, sun_cone, r_bo_list, f'Left Swing 30 deg, beta={beta} deg')

    # 正对地
    r_bo_list = [euler2dcm('ZYX', [0, 0, 0], degrees=True) for _ in range(len(sun_cone))]
    calc_star_tracker_field_of_view(s_b_list, sun_cone, r_bo_list, f'Earth [0,0,0], beta={beta} deg')

    # 检查轨控模式星敏视场
    # # +X推进
    r_bo_list = [euler2dcm('XYZ', [0, 90, 90], degrees=True) for _ in range(len(sun_cone))]
    calc_star_tracker_field_of_view(s_b_list, sun_cone, r_bo_list, f'Orbit control +X, beta={beta} deg')

    # # -X推进
    r_bo_list = [euler2dcm('XYZ', [0, -90, -90], degrees=True) for _ in range(len(sun_cone))]
    calc_star_tracker_field_of_view(s_b_list, sun_cone, r_bo_list, f'Orbit control -X, beta={beta} deg')

    # # -Y推进
    r_bo_list = [euler2dcm('ZYX', [0, 0, 90], degrees=True) for _ in range(len(sun_cone))]
    calc_star_tracker_field_of_view(s_b_list, sun_cone, r_bo_list, f'Orbit control -Y, beta={beta} deg')

def calc_star_tracker_field_of_view(
        s_b_list: list[np.ndarray],
        sun_cone: list, 
        r_bo_list: list[np.ndarray],
        title: str):
    """
    计算星敏光轴与太阳矢量夹角
    s_b_list: 星敏光轴列表。例：两个星敏就是两个三维矢量
    sun_cone: 太阳矢量列表
    r_bo_list: 轨道系到本体系的旋转矩阵列表（与sun_cone 一一对应）
    """

    star_tracker_num = len(s_b_list)
    sun_angle = [[] for _ in range(star_tracker_num)]
    earth_angle = [[] for _ in range(star_tracker_num)]
    earth = np.array([0, 0, 1])

    for v_sun, r_bo in zip(sun_cone, r_bo_list):
        for index, s_b in enumerate(s_b_list):
            r_ob = r_bo.transpose()
            s_o = r_ob @ s_b  # 星敏光轴在轨道系下的矢量
            sun_angle[index].append(vector_angle(v_sun, s_o))
            earth_angle[index].append(vector_angle(earth, s_o))

    alpha = np.linspace(0, 2*np.pi, sample_num)

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    # plt.subplots_adjust(hspace=0.35)  # 增加两幅图的纵向间距

    fig.suptitle(title, fontsize=16)
    ax[0].set_title("Star Tracker Light Axis to Sun")
    for index, theta in enumerate(sun_angle):
        ax[0].plot(np.rad2deg(alpha), np.rad2deg(theta), label=f"star tracker {index+1}")
        mark_max_min(ax[0], np.rad2deg(alpha), np.rad2deg(theta))
    ax[0].set_xlabel("Phase (deg)")
    ax[0].set_ylabel("Angle (deg)")
    ax[0].grid(True)
    ax[0].legend()

    ax[1].set_title("Star Tracker Light Axis to Earth")
    for index, theta in enumerate(earth_angle):
        ax[1].plot(np.rad2deg(alpha), np.rad2deg(theta), label=f"star tracker {index+1}")
        mark_max_min(ax[1], np.rad2deg(alpha), np.rad2deg(theta))
    ax[1].set_xlabel("Phase (deg)")
    ax[1].set_ylabel("Angle (deg)")
    ax[1].grid(True)
    ax[1].legend()

    plt.show(block=False)

def mark_max_min(ax, x, y, label=None, color_max='red', color_min='blue'):
    """
    在ax上标记y的最大值和最小值
    ax: matplotlib的axes对象
    x: x数据（1维数组）
    y: y数据（1维数组）
    label: 可选，标注前缀
    color_max: 最大值点颜色
    color_min: 最小值点颜色
    """
    y = np.array(y)
    x = np.array(x)
    idx_max = np.argmax(y)
    idx_min = np.argmin(y)
    # 标记最大值
    ax.scatter(x[idx_max], y[idx_max], color=color_max, marker='o')
    txt = f"max:{y[idx_max]:.1f}" if label is None else f"{label} max:{y[idx_max]:.1f}"
    ax.annotate(txt, (x[idx_max], y[idx_max]), textcoords="offset points", xytext=(0,10), ha='center', color=color_max)
    # 标记最小值
    ax.scatter(x[idx_min], y[idx_min], color=color_min, marker='o')
    txt = f"min:{y[idx_min]:.1f}" if label is None else f"{label} min:{y[idx_min]:.1f}"
    ax.annotate(txt, (x[idx_min], y[idx_min]), textcoords="offset points", xytext=(0,-15), ha='center', color=color_min)

def main():
    """分析主函数"""
    sun_cone = sun_cone_in_vvlh(np.deg2rad(-19.2))
    sun_cone_in_light_index = sun_vector_in_light(sun_cone, SEMIMAJAR_AXIS)
    panel_n_cone = panel_normal_cone(sun_cone)

    # 计算星敏光轴与太阳矢量夹角
    # check_star_tracker()

    anlyse_sun_att(panel_n_cone)

    # energy_efficiency(
    #     sun_cone,
    #     sun_cone_in_light_index,
    #     panel_n_cone)

    # roll_angle = plot_sun_cone(
    #     sun_cone,
    #     sun_cone_in_light_index,
    #     panel_n_cone)

    # plot_body_in_orbit_frame(max(roll_angle), min(roll_angle))

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
