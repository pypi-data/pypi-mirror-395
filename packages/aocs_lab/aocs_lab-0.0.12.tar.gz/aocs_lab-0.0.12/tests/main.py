import os
import sys
import numpy as np

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(parent_dir)
import aocs_lab.utils.lib as lib
import aocs_lab.sun_time as sun_time

if __name__ == "__main__":
    # 太阳矢量与轨道面法线夹角
    beta_angle = np.deg2rad(31)
    sun_time.sun_time(beta_angle, 6900e3)

    beta_angle = np.deg2rad(67)
    sun_time.sun_time(beta_angle, 6900e3)

    InsMat = np.array([[-0.707106781186548,  0.707106781186548, 0],
                       [-0.612355272073377, -0.612355272073377, 0.500000000000000],
                       [0.353474843779257,  0.353474843779257, 0.866025403784439]])

    a = lib.dcm2quat(InsMat)

    r = 6908.3e3
    distance = 1500e3

    theta = np.arctan((distance/2)/r)

    print(np.rad2deg(theta))

    n = np.array([np.cos(np.deg2rad(0)) * np.sin(np.deg2rad(45)),
                  np.cos(np.deg2rad(0)) * np.cos(np.deg2rad(135)),
                  np.sin(np.deg2rad(0))])

    theta = lib.vector_angle(n, np.array([0, -1, 0]))

    print(np.rad2deg(np.pi/2 - theta))

    # A 星星敏A
    theta1 = np.array([[120,     30,     90],
                      [ 56.17,  71.25, 140],
                      [131.56, 112.52, 130]])
    
    # A 星星敏B
    theta2 = np.array([[ 56.1742, 108.747,  40],
                       [120,      150,      90],
                       [ 48.4392, 112.521, 130]])
    
    # B 星星敏A
    theta = np.array([[60,     30,     90],
                      [56.17, 108.75,  40],
                      [48.44, 112.52, 130]])

    # B 星星敏B
    theta = np.array([[120,     30,     90],
                      [ 56.17,  71.25, 140],
                      [131.56, 112.52, 130]])

    dcm_SB = lib.theta_deg_to_cos_matrix(theta2)

    q_BS = lib.dcm2quat(dcm_SB.transpose())

    print(q_BS)
