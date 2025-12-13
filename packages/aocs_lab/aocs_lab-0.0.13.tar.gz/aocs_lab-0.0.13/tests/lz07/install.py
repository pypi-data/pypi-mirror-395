import numpy as np
import os, sys
from dataclasses import dataclass
from typing import TypeAlias

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.append(parent_dir)
from aocs_lab.utils import lib

# 类型别名定义
UnitVector3D: TypeAlias = np.ndarray      # 单位三维向量
Dcm: TypeAlias = np.ndarray               # 3x3矩阵
Quaternion: TypeAlias = np.ndarray        # 四元数 [w, x, y, z]
AnglesDeg: TypeAlias = np.ndarray         # 角度列表（度）

# A 星布局报告输出
distribution_report_A = {
"dcm_SB_deg_starA": [
    [-0.707107,  0,         0.707107],
    [-0.298836,  0.906308, -0.298836],
    [-0.640856, -0.422618, -0.640856]],

"dcm_SB_deg_starB": [
    [ 0.707107,  0,         0.707107],
    [-0.298836, -0.906308,  0.298836],
    [ 0.640856, -0.422618, -0.640856]],

"theta_matrix_SB_deg_fiberA": [
        [  0,  90,  90],
        [ 90,  90, 180],
        [ 90,   0,  90]],

"theta_matrix_SB_deg_fiberB" : [
        [180, 90, 90],
        [ 90, 90,  0],
        [ 90,  0, 90]],

"theta_matrix_SB_deg_sun_sensor_A": [
    [  0,  90,  90],
    [ 90,  90,   0],
    [ 90, 180,  90]
],

"theta_matrix_SB_deg_sun_sensor_B": [
    [  0,  90,  90],
    [ 90,  90,   0],
    [ 90, 180,  90]
],

"theta_matrix_SB_deg_magmeter": [
        [180,  90,  90],
        [ 90, 180,  90],
        [ 90,  90,   0]],

"wheel_unit_vector_list": [
    [0.173648,-0.696364,-0.696364],
    [0.173648, 0.696364,-0.696364],
    [0.173648,-0.696364, 0.696364],
    [0.173648, 0.696364, 0.696364]
],

"magtorquer_unit_vector_list": [
    [-1,  0,  0],
    [ 0, -1,  0],
    [ 0,  0,  1]
],

"theta_matrix_SB_deg_trans_atenna_A": [
    [ 90, 150, 60],
    [  0,  90, 90],
    [ 90,  60, 30]
],

"theta_matrix_SB_deg_trans_atenna_B": [
    [ 90, 150, 60],
    [  0,  90, 90],
    [ 90,  60, 30]
]
}

# B 星布局报告输出
distribution_report_B = {
"theta_matrix_SB_deg_starA": [
    [ 60,        30,      90],
    [ 56.1742,  108.747,  40],
    [ 48.4392,  112.521, 130]],

"theta_matrix_SB_deg_starB": [
    [ 120,       30,       90],
    [  56.1742,  71.2528, 140],
    [ 131.561,  112.521,  130]],

"theta_matrix_SB_deg_fiber": [
        [180,  90,  90],
        [ 90, 180,  90],
        [ 90,  90,   0]],

"theta_matrix_SB_deg_mems" : [
        [ 90,  0, 90],
        [ 90, 90,  0],
        [ 0,  90, 90]],

"theta_matrix_SB_deg_sun_sensor_A_close": [
    [ 0, 90,  90],
    [90, 90, 180],
    [90,  0,  90]
],

"theta_matrix_SB_deg_sun_sensor_A_expand": [
    [180,  90,  90],
    [ 90,  90, 180],
    [ 90, 180,  90]
],

"theta_matrix_SB_deg_sun_sensor_B": [
    [180,  90,  90],
    [ 90,  90, 180],
    [ 90, 180,  90]
],

"theta_matrix_SB_deg_magmeter": [
        [ 90,  0,  90],
        [  0, 90,  90],
        [ 90, 90, 180]],

"wheel_vector_angle_deg_list": [
    [76.7559, 46.5044,133.4960],
    [76.7559, 46.5044, 46.5043],
    [76.7559,133.4960, 46.5043],
    [76.7559,133.4960,133.4960]
],

# todo 待确认
"magtorquer_vector_angle_deg_list": [
    [ 0, 90, 90],
    [90,  0, 90],
    [90, 90,  0]
],

"thruster_unit_vector_force": [
    [0,0,1]
],

"theta_matrix_SB_deg_trans_atenna_A": [
    [ 90, 150, 60],
    [  0,  90, 90],
    [ 90,  60, 30]
],

"theta_matrix_SB_deg_trans_atenna_B": [
    [  90, 30, 120],
    [ 180, 90,  90],
    [  90, 60,  30]
]
}

# CD 星布局报告输出
distribution_report_CD = {
# C01 D01
"theta_matrix_SB_deg_starA_C01_D01": [
    [  0,  90,  90],
    [ 90, 128, 142],
    [ 90,  38, 128]],

"theta_matrix_SB_deg_starB_C01_D01": [
    [  0,  90,  90],
    [ 90, 128,  38],
    [ 90, 142, 128]],

# C02 D02
"theta_matrix_SB_deg_starA_C02_D02": [
    [180, 90,  90],
    [ 90, 52,  38],
    [ 90, 38, 128]],

"theta_matrix_SB_deg_starB_C02_D02": [
    [180,  90,  90],
    [ 90,  52, 142],
    [ 90, 142, 128]],

# CD
"theta_matrix_SB_deg_fiber": [
        [180,  90,  90],
        [ 90, 180,  90],
        [ 90,  90,   0]],

"theta_matrix_SB_deg_mems" : [
        [ 90,  0, 90],
        [ 90, 90,  0],
        [ 0,  90, 90]],

"theta_matrix_SB_deg_sun_sensor_A_close": [
        [180,  90,  90],
        [ 90,  90, 180],
        [ 90, 180,  90]],

"theta_matrix_SB_deg_sun_sensor_A_expand": [
        [ 0, 90,  90],
        [90, 90, 180],
        [90,  0,  90]],

"theta_matrix_SB_deg_sun_sensor_B": [
        [ 0, 90,  90],
        [90, 90, 180],
        [90,  0,  90]],

"theta_matrix_SB_deg_magmeter": [
        [ 90,  90, 180],
        [ 90, 180,  90],
        [180,  90,  90]],

"wheel_vector_angle_deg_list": [
    [76.7559, 46.5044, 46.5043],
    [76.7559,133.4960, 46.5043],
    [76.7559, 46.5044,133.4960],
    [76.7559,133.4960,133.4960]
],

"magtorquer_vector_angle_deg_list": [
    [ 0, 90, 90],
    [90,  0, 90],
    [90, 90,  0]
],

"thruster_unit_vector_force": [
    [0,0,1]
],

"theta_matrix_SB_deg_trans_atenna_A": [
    [ 90,  30,  60],
    [180,  90,  90],
    [ 90, 120,  30]
],

"theta_matrix_SB_deg_trans_atenna_B": [
    [ 90, 150, 120],
    [  0,  90,  90],
    [ 90, 120,  30]
]

}

@dataclass
class device_install:
    star_A: Quaternion
    star_B: Quaternion
    gyro_A: Dcm
    gyro_B: Dcm
    sun_sensor_A_close: Dcm
    sun_sensor_A_expand: Dcm
    sun_sensor_B: Dcm
    magmeter_A: Dcm
    magmeter_B: Dcm
    wheel_A: UnitVector3D
    wheel_B: UnitVector3D
    wheel_C: UnitVector3D
    wheel_D: UnitVector3D
    magtorquer_A: UnitVector3D
    magtorquer_B: UnitVector3D
    magtorquer_C: UnitVector3D
    thruster_A: UnitVector3D
    trans_antenna_A: Dcm
    trans_antenna_B: Dcm

    def save_results_to_file(self, filename: str = "satellite_install_results.txt"):
        """将计算结果保存到文本文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# 卫星传感器安装矩阵计算结果\n\n")
            
            # 获取所有成员变量
            import dataclasses
            import numpy as np
            for field in dataclasses.fields(self):
                field_name = field.name
                value = getattr(self, field_name)
                
                f.write(f"{field_name}:\n")
                
                # 根据numpy数组的shape判断类型并格式化输出
                if hasattr(value, 'shape'):
                    if value.shape == (3, 3):
                        # 3x3矩阵 (方向余弦矩阵)
                        f.write("方向余弦矩阵 (单机系到本体系):\n")
                        for row in value:
                            row_str = ", ".join([f"{x:.8f}" for x in row])
                            f.write(f"  [{row_str}]\n")
                            
                    elif value.shape == (4,):
                        # 4元素1维数组 (四元数)
                        quat_str = ", ".join([f"{x:.15f}" for x in value])
                        f.write(f"四元数 [w, x, y, z] (单机系到本体系):\n [{quat_str}]\n")
                        
                    elif value.shape == (3,):
                        # 3元素1维数组 (三维向量)
                        vector_str = ", ".join([f"{x:.8f}" for x in value])
                        f.write(f"单位方向矢量 (本体系): [{vector_str}]\n")
                    else:
                        # 其他shape的numpy数组
                        f.write(f"numpy数组 (shape: {value.shape}): {value}\n")
                        
                else:
                    # 其他类型
                    raise ValueError(f"不支持的类型: {type(value)}")

                f.write("\n")
        
        print(f"计算结果已保存到文件: {filename}")

def star_tracker_quat(theta_matrix_SB_deg: list[list[float]]) -> Quaternion:
    dcm_SB = lib.theta_deg_to_cos_matrix(theta_matrix_SB_deg)
    err = lib.orthogonality_error(dcm_SB)
    dcm_BS = dcm_SB.T
    q_BS = lib.dcm2quat(dcm_BS)

    print("Orthogonality error", err)

    return q_BS

def star_tracker_quat_from_dcm(dcm_SB: np.ndarray) -> Quaternion:
    err = lib.orthogonality_error(dcm_SB)
    dcm_BS = dcm_SB.T
    q_BS = lib.dcm2quat(dcm_BS)

    print("Orthogonality error", err)

    return q_BS


def sensor_3axis_dcm(theta_matrix_SB_deg: list) -> Dcm:
    dcm_SB = lib.theta_deg_to_cos_matrix(theta_matrix_SB_deg)
    err = lib.orthogonality_error(dcm_SB)
    dcm_BS = dcm_SB.T

    print("Orthogonality error", err)

    return dcm_BS

def actuator_unit_vector(angle_deg: list) -> UnitVector3D:
    vector = np.cos(np.deg2rad(angle_deg))

    return vector

lz07_a01 = device_install(
    star_A=star_tracker_quat_from_dcm(np.array(distribution_report_A['dcm_SB_deg_starA'])),
    star_B=star_tracker_quat_from_dcm(np.array(distribution_report_A['dcm_SB_deg_starB'])),
    gyro_A=sensor_3axis_dcm(distribution_report_A['theta_matrix_SB_deg_fiberA']),
    gyro_B=sensor_3axis_dcm(distribution_report_A['theta_matrix_SB_deg_fiberB']),
    sun_sensor_A_close=sensor_3axis_dcm(distribution_report_A['theta_matrix_SB_deg_sun_sensor_A']),
    sun_sensor_A_expand=sensor_3axis_dcm(distribution_report_A['theta_matrix_SB_deg_sun_sensor_A']),
    sun_sensor_B=sensor_3axis_dcm(distribution_report_A['theta_matrix_SB_deg_sun_sensor_B']),
    magmeter_A=sensor_3axis_dcm(distribution_report_A['theta_matrix_SB_deg_magmeter']),
    magmeter_B=sensor_3axis_dcm(distribution_report_A['theta_matrix_SB_deg_magmeter']),
    wheel_A=np.array(distribution_report_A['wheel_unit_vector_list'][0]),
    wheel_B=np.array(distribution_report_A['wheel_unit_vector_list'][1]),
    wheel_C=np.array(distribution_report_A['wheel_unit_vector_list'][2]),
    wheel_D=np.array(distribution_report_A['wheel_unit_vector_list'][3]),
    magtorquer_A=np.array(distribution_report_A['magtorquer_unit_vector_list'][0]),
    magtorquer_B=np.array(distribution_report_A['magtorquer_unit_vector_list'][1]),
    magtorquer_C=np.array(distribution_report_A['magtorquer_unit_vector_list'][2]),
    thruster_A=np.array([0,0,0]),
    trans_antenna_A=sensor_3axis_dcm(distribution_report_A['theta_matrix_SB_deg_trans_atenna_A']),
    trans_antenna_B=sensor_3axis_dcm(distribution_report_A['theta_matrix_SB_deg_trans_atenna_B']),
)


lz07_b01 = device_install(
    star_A=star_tracker_quat(distribution_report_B['theta_matrix_SB_deg_starA']),
    star_B=star_tracker_quat(distribution_report_B['theta_matrix_SB_deg_starB']),
    gyro_A=sensor_3axis_dcm(distribution_report_B['theta_matrix_SB_deg_fiber']),
    gyro_B=sensor_3axis_dcm(distribution_report_B['theta_matrix_SB_deg_mems']),
    sun_sensor_A_close=sensor_3axis_dcm(distribution_report_B['theta_matrix_SB_deg_sun_sensor_A_close']),
    sun_sensor_A_expand=sensor_3axis_dcm(distribution_report_B['theta_matrix_SB_deg_sun_sensor_A_expand']),
    sun_sensor_B=sensor_3axis_dcm(distribution_report_B['theta_matrix_SB_deg_sun_sensor_B']),
    magmeter_A=sensor_3axis_dcm(distribution_report_B['theta_matrix_SB_deg_magmeter']),
    magmeter_B=sensor_3axis_dcm(distribution_report_B['theta_matrix_SB_deg_magmeter']),
    wheel_A=actuator_unit_vector(distribution_report_B['wheel_vector_angle_deg_list'][0]),
    wheel_B=actuator_unit_vector(distribution_report_B['wheel_vector_angle_deg_list'][1]),
    wheel_C=actuator_unit_vector(distribution_report_B['wheel_vector_angle_deg_list'][2]),
    wheel_D=actuator_unit_vector(distribution_report_B['wheel_vector_angle_deg_list'][3]),
    magtorquer_A=actuator_unit_vector(distribution_report_B['magtorquer_vector_angle_deg_list'][0]),
    magtorquer_B=actuator_unit_vector(distribution_report_B['magtorquer_vector_angle_deg_list'][1]),
    magtorquer_C=actuator_unit_vector(distribution_report_B['magtorquer_vector_angle_deg_list'][2]),
    thruster_A=np.array(distribution_report_B['thruster_unit_vector_force'][0]),
    trans_antenna_A=sensor_3axis_dcm(distribution_report_B['theta_matrix_SB_deg_trans_atenna_A']),
    trans_antenna_B=sensor_3axis_dcm(distribution_report_B['theta_matrix_SB_deg_trans_atenna_B']),
)

lz07_c01 = device_install(
    star_A=star_tracker_quat(distribution_report_CD['theta_matrix_SB_deg_starA_C01_D01']),
    star_B=star_tracker_quat(distribution_report_CD['theta_matrix_SB_deg_starB_C01_D01']),
    gyro_A=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_fiber']),
    gyro_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_mems']),
    sun_sensor_A_close=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_sun_sensor_A_close']),
    sun_sensor_A_expand=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_sun_sensor_A_expand']),
    sun_sensor_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_sun_sensor_B']),
    magmeter_A=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_magmeter']),
    magmeter_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_magmeter']),
    wheel_A=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][0]),
    wheel_B=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][1]),
    wheel_C=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][2]),
    wheel_D=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][3]),
    magtorquer_A=actuator_unit_vector(distribution_report_CD['magtorquer_vector_angle_deg_list'][0]),
    magtorquer_B=actuator_unit_vector(distribution_report_CD['magtorquer_vector_angle_deg_list'][1]),
    magtorquer_C=actuator_unit_vector(distribution_report_CD['magtorquer_vector_angle_deg_list'][2]),
    thruster_A=np.array(distribution_report_CD['thruster_unit_vector_force'][0]),
    trans_antenna_A=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_trans_atenna_A']),
    trans_antenna_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_trans_atenna_B']),
)

lz07_c02 = device_install(
    star_A=star_tracker_quat(distribution_report_CD['theta_matrix_SB_deg_starA_C02_D02']),
    star_B=star_tracker_quat(distribution_report_CD['theta_matrix_SB_deg_starB_C02_D02']),
    gyro_A=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_fiber']),
    gyro_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_mems']),
    sun_sensor_A_close=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_sun_sensor_A_close']),
    sun_sensor_A_expand=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_sun_sensor_A_expand']),
    sun_sensor_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_sun_sensor_B']),
    magmeter_A=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_magmeter']),
    magmeter_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_magmeter']),
    wheel_A=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][0]),
    wheel_B=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][1]),
    wheel_C=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][2]),
    wheel_D=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][3]),
    magtorquer_A=actuator_unit_vector(distribution_report_CD['magtorquer_vector_angle_deg_list'][0]),
    magtorquer_B=actuator_unit_vector(distribution_report_CD['magtorquer_vector_angle_deg_list'][1]),
    magtorquer_C=actuator_unit_vector(distribution_report_CD['magtorquer_vector_angle_deg_list'][2]),
    thruster_A=np.array(distribution_report_CD['thruster_unit_vector_force'][0]),
    trans_antenna_A=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_trans_atenna_A']),
    trans_antenna_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_trans_atenna_B']),
)

lz07_d01 = device_install(
    star_A=star_tracker_quat(distribution_report_CD['theta_matrix_SB_deg_starA_C01_D01']),
    star_B=star_tracker_quat(distribution_report_CD['theta_matrix_SB_deg_starB_C01_D01']),
    gyro_A=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_fiber']),
    gyro_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_mems']),
    sun_sensor_A_close=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_sun_sensor_A_close']),
    sun_sensor_A_expand=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_sun_sensor_A_expand']),
    sun_sensor_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_sun_sensor_B']),
    magmeter_A=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_magmeter']),
    magmeter_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_magmeter']),
    wheel_A=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][0]),
    wheel_B=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][1]),
    wheel_C=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][2]),
    wheel_D=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][3]),
    magtorquer_A=actuator_unit_vector(distribution_report_CD['magtorquer_vector_angle_deg_list'][0]),
    magtorquer_B=actuator_unit_vector(distribution_report_CD['magtorquer_vector_angle_deg_list'][1]),
    magtorquer_C=actuator_unit_vector(distribution_report_CD['magtorquer_vector_angle_deg_list'][2]),
    thruster_A=np.array(distribution_report_CD['thruster_unit_vector_force'][0]),
    trans_antenna_A=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_trans_atenna_A']),
    trans_antenna_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_trans_atenna_B']),
)

lz07_d02 = device_install(
    star_A=star_tracker_quat(distribution_report_CD['theta_matrix_SB_deg_starA_C02_D02']),
    star_B=star_tracker_quat(distribution_report_CD['theta_matrix_SB_deg_starB_C02_D02']),
    gyro_A=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_fiber']),
    gyro_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_mems']),
    sun_sensor_A_close=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_sun_sensor_A_close']),
    sun_sensor_A_expand=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_sun_sensor_A_expand']),
    sun_sensor_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_sun_sensor_B']),
    magmeter_A=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_magmeter']),
    magmeter_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_magmeter']),
    wheel_A=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][0]),
    wheel_B=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][1]),
    wheel_C=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][2]),
    wheel_D=actuator_unit_vector(distribution_report_CD['wheel_vector_angle_deg_list'][3]),
    magtorquer_A=actuator_unit_vector(distribution_report_CD['magtorquer_vector_angle_deg_list'][0]),
    magtorquer_B=actuator_unit_vector(distribution_report_CD['magtorquer_vector_angle_deg_list'][1]),
    magtorquer_C=actuator_unit_vector(distribution_report_CD['magtorquer_vector_angle_deg_list'][2]),
    thruster_A=np.array(distribution_report_CD['thruster_unit_vector_force'][0]),
    trans_antenna_A=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_trans_atenna_A']),
    trans_antenna_B=sensor_3axis_dcm(distribution_report_CD['theta_matrix_SB_deg_trans_atenna_B']),
)


def main():
    lz07_a01.save_results_to_file("satellite_install_results_A01.txt")
    lz07_b01.save_results_to_file("satellite_install_results_B01.txt")
    lz07_c01.save_results_to_file("satellite_install_results_C01.txt")
    lz07_c02.save_results_to_file("satellite_install_results_C02.txt")
    lz07_d01.save_results_to_file("satellite_install_results_D01.txt")
    lz07_d02.save_results_to_file("satellite_install_results_D02.txt")

if __name__ == "__main__":
    main()