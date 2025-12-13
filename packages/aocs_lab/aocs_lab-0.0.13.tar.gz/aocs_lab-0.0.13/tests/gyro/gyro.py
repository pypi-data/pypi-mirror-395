import numpy as np

import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.append(parent_dir)
import aocs_lab.utils.lib as lib

# 上海厂房坐标 31.021018°N 121.393126°E
# 方舟实验室 40°03'16"N 116°21'08"E, 厂房偏转角度 asin(67/316) = 12.2°
# 太原坐标 38.8°N 111.6°E， 厂房偏转角度 asin(37.1/58.7)

def dms_to_decimal(deg: float, minutes: float = 0.0, seconds: float = 0.0, hemisphere: str | None = None) -> float:
    """
    将度分秒转换为度小数。
    - deg: 度（可为负）
    - minutes: 分（0~60）
    - seconds: 秒（0~60）
    - hemisphere: 方位字母，可为 'N','S','E','W'（大小写均可），如提供则决定正负

    返回：度小数（float）
    """
    if minutes < 0 or minutes >= 60 or seconds < 0 or seconds >= 60:
        raise ValueError("minutes 和 seconds 应满足 0 <= minutes < 60, 0 <= seconds < 60")

    # 由方位字母确定符号（若有）
    sign = 1
    if hemisphere:
        h = hemisphere.upper()
        if h not in ("N", "S", "E", "W"):
            raise ValueError("hemisphere 必须是 N/S/E/W")
        sign = -1 if h in ("S", "W") else 1

    # 如果未提供方位字母，则使用度的符号
    if hemisphere is None and deg < 0:
        sign = -1

    abs_deg = abs(float(deg))
    dec = abs_deg + float(minutes) / 60.0 + float(seconds) / 3600.0
    return sign * dec

if __name__ == "__main__":
    # 坐标定义，当地东北天L，厂房东北天F，卫星本体系B
    latitude_deg = dms_to_decimal(40, 3, 16, 'N')
    print(f'纬度 {latitude_deg}°')
    omega_L = lib.latitude_to_angular_velocity(np.deg2rad(latitude_deg))
    A_FL = lib.rotate_z(0)  # 当地东北天 到 厂房东北天坐标系
    A_BF = lib.rotate_z(np.deg2rad(12.2+90)) 
  
    omega_B = A_BF @ A_FL @ omega_L
    omega_B_deg = np.rad2deg(omega_B)

    print(f'卫星本体系理论角速度')
    print(f'x: {omega_B_deg[0]:10.6f} deg/s')
    print(f'y: {omega_B_deg[1]:10.6f} deg/s')
    print(f'z: {omega_B_deg[2]:10.6f} deg/s')
