
import numpy as np
import pprint

import os
import sys


def get_max_magnetic_disterbuance(
        mag_moment_change_matrix, 
        mag_moment_change_max, 
        magmeter_change_matrix):
    """
    计算磁力矩器对磁强计测量值的最大干扰

    Parameters
    ----------
        mag_moment_change_matrix : 
            标准磁矩变化矩阵 (3x3), 每行一组输出值，一共三组
        mag_moment_change_max : 
            标准磁矩变化最大值 (3x1)。若磁棒最大输出 25 Am^2, 则为[25, 25, 25]
        magnetic_change_matrix : 
            标准磁矩变化矩阵 (3x3), 每行一组测量值，一共三组

    Returns
    -------
        max_magmeter_change : 磁强计测量值的最大干扰量
    """

    # 磁矩与磁强计关系矩阵 (3x3)
    # magmeter_change_matrix = mag_moment_change_matrix @ k
    # [bx, by, bz] = [mx, my, mz] @ k
    k = magmeter_change_matrix @ np.linalg.inv(mag_moment_change_matrix)

    # 枚举磁力矩器最大输出立方体角点
    dir = np.array([[1, 1, 1],
                    [1, 1, -1],
                    [1, -1, 1],
                    [1, -1, -1],
                    [-1, 1, 1],
                    [-1, 1, -1],
                    [-1, -1, 1],
                    [-1, -1, -1]])
    
    m_max_list = mag_moment_change_max * dir

    b_max_list = m_max_list @ k

    # 行向量取模
    b_row_norms = np.linalg.norm(b_max_list, axis=1)

    return max(b_row_norms)


if __name__ == "__main__":
    # 标准磁矩变化矩阵
    dm = np.array([[25, 0, 0],
                   [0, 25, 0],
                   [0, 0, 25]])


    # A星 20250212 磁强计A
    b_std = np.array([[0.0000318, 0.00000831, 0.0000301],
                      [0.0000318, 0.00000831, 0.0000301],
                      [0.0000318, 0.00000831, 0.0000301]])

    # 给定标准磁矩变化矩阵，磁强计测量值
    b_output = np.array([[0.0000282, 0.0000101,  0.0000301],
                         [0.0000311, 0.00000681, 0.0000309],
                         [0.0000407, 0.00000956, 0.0000358]])


    # # B星
    # # 磁强计测量基准值
    # b_std = np.array([[-0.0547, 0.392, 0.292],
    #                   [-0.0547, 0.392, 0.292],
    #                   [-0.0547, 0.392, 0.292]])

    # # 给定标准磁矩变化矩阵，磁强计测量值
    # b_output = np.array([[-0.0722, 0.395, 0.279],
    #                      [-0.0596, 0.364, 0.292],
    #                      [-0.0533, 0.411, 0.290]])


    db_max = get_max_magnetic_disterbuance(dm, [25, 25, 25], b_output - b_std)

    print(f"磁棒对磁强计的最大扰动为 {db_max*1e4:.2e}")
