"""分析刚体主轴惯量与主轴惯量坐标系"""
from scipy.spatial.transform import Rotation as R
import numpy as np
from .utils import lib


def analyse_principal_moments_of_inertia(inertia_ref):
    """
    分析主轴惯量
    inertia_ref: 参考系 ref 下惯量矩阵
    """
    # 计算特征值和特征向量
    principal_inertia, principal_axes = np.linalg.eig(inertia_ref)
    err = lib.orthogonality_error(principal_axes)

    rotvec = R.from_matrix(principal_axes).as_rotvec()
    rotvec_norm_deg = np.rad2deg(np.linalg.norm(rotvec))

    print("主轴惯量 (kg*m^2):")
    print(f'  Ixx = {principal_inertia[0]:6.1f}')
    print(f'  Iyy = {principal_inertia[1]:6.1f}')
    print(f'  Izz = {principal_inertia[2]:6.1f}')
    print("")
    print(f'主惯量轴坐标系正交性误差:\n  {err:.3e}')
    print("")
    print(f'主惯量轴坐标系相对本体系偏转角度:\n  {rotvec_norm_deg:.3f} deg')


if __name__ == '__main__':
    I_B = np.array([[89, 19, -7],
                    [19, 341, 2],
                    [-7, 2, 294]])

    analyse_principal_moments_of_inertia(I_B)
