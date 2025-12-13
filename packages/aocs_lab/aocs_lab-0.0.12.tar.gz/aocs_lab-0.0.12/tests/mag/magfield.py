import numpy as np

import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(parent_dir)
import aocs_lab.pyIGRF14.igrf as igrf
import aocs_lab.utils.lib as lib

# 上海厂房坐标 31.021018°N 121.393126°E
# 太原坐标 38.8°N 111.6°E， 厂房偏转角度 asin(37.1/58.7)

if __name__ == "__main__":
    # 坐标定义，当地北东地M，当地东北天L，厂房东北天F，卫星本体系B
    mag_M = igrf.get_mag_field(2024.9, 111.6, 38.8, 1)

    A_LM = lib.rotate_z(np.deg2rad(-90)) @ lib.rotate_x(np.deg2rad(180))
    A_FL = lib.rotate_z(np.asin(37.1/58.7))
    A_BF = lib.rotate_z(np.deg2rad(180))
  
    mag_B = A_BF @ A_FL @ A_LM @ mag_M

    print(f'卫星本体系理论磁场强度')
    print(f'x: {mag_B[0]:10.0f} nT')
    print(f'y: {mag_B[1]:10.0f} nT')
    print(f'z: {mag_B[2]:10.0f} nT')