from math import acos, sin, cos, gcd
import math
import os
import sys
import numpy as np
from typing import List, Tuple

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.append(parent_dir)
import aocs_lab.utils.lib as lib
import aocs_lab.utils.constants as const
import aocs_lab.utils.lib as lib


J2 = 1.08263e-3
J3 = -2.565e-6
a_norm = 6378137
A2 = 1.5*J2
ns = 1.99102128e-07 # 太阳相对地球角速度
DAY_SEC = 86400.0

def repeat_orbit_search(
        height_min = 980e3, 
        height_max = 1200e3, 
        repeat_days_min = 5, 
        repeat_days_max = 25, 
        repeat_revs_min = 100, 
        repeat_revs_max = 300):
    """
    回归轨道搜索

    """

    a1 = height_min + const.EARTH_EQUATORIAL_RADIUS
    a2 = height_max + const.EARTH_EQUATORIAL_RADIUS
    e1, i1 = calc_elements(a1)
    e2, i2 = calc_elements(a2)

    T1 = calc_node_period(a1, e1, i1, np.deg2rad(90))
    T2 = calc_node_period(a2, e2, i2, np.deg2rad(90))

    p1 = T1 / DAY_SEC
    p2 = T2 / DAY_SEC

    results: List[Tuple[float, float, float, int, int]] = []

    for revs in range(repeat_revs_min, repeat_revs_max + 1):
        j_min = max(int(math.ceil(p1 * revs)), repeat_days_min)
        j_max = min(int(math.floor(p2 * revs)), repeat_days_max)
        if j_min > j_max:
            continue
        for days in range(j_min, j_max + 1):
            if gcd(revs, days) == 1:
                T = days / revs * DAY_SEC
                u = 2.0 / 3.0

                semi = (a1 / (T1 ** u) * (T2 - T) + a2 / (T2 ** u) * (T - T1)) * (T ** u) / (T2 - T1)
                e, inc = calc_elements(semi)
                altitude_km = (semi - const.EARTH_EQUATORIAL_RADIUS) / 1000.0
                inc_deg = np.rad2deg(inc)
                results.append((altitude_km, e, inc_deg, revs, days))

    return results



def calc_elements(a):
    """
    计算轨道要素
    """
    no = lib.orbit_angular_rate(a)
    a = a/a_norm
    p = a*(1 - 1e-6)
    i = acos(-ns/(A2/p**2 * no))
    e = sin(i) / (cos(i)**2/sin(i) - 2*J2*a/J3)
    
    return e, i


def calc_node_period(a,e,i,w):
    """
    计算轨道节点周期
    """
    T = lib.orbit_period(a)
    node_period = T *(1 + A2/4/(a/a_norm)**2 * ((-12 - 22 * e**2) + (16 + 29 * e**2) * sin(i)**2 + (16-20*sin(i)**2) * e * cos(w) - (12-15*sin(i)**2) * e**2 * cos(2*w)))

    return node_period

if __name__ == "__main__":
    res = repeat_orbit_search(478e3-50e3, 478e3+50e3, 0, 100, 50, 500)
    # 简单打印前若干行
    print("高度km    e        倾角deg  回归圈  回归天")
    for r in res:
        print(f"{r[0]:8.2f} {r[1]:15.5e} {r[2]:9.4f} {r[3]:7d} {r[4]:7d}")
    print(f"总组合数: {len(res)}")
