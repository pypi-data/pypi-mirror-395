# 计算飞轮惯滑时间

import numpy as np


def get_cross_index(data, threshold, cross_dir):
    index = -1

    if cross_dir == 'up':
        for i in range(len(data) - 1):
            if data[i] < threshold and data[i + 1] >= threshold:
                index = i

    elif cross_dir == 'down':
        for i in range(len(data) - 1):
            if data[i] > threshold and data[i + 1] <= threshold:
                index = i
    else:
        raise ValueError("wrong direction")

    if index < 0:
        raise ValueError("can't find cross point")

    return index


def calc_slide_time(time_list, speed_list, high_speed, low_speed):
    start_index = get_cross_index(speed_list, high_speed, 'down')
    end_index = get_cross_index(speed_list, low_speed, 'down')

    return time_list[end_index] - time_list[start_index]


if __name__ == "__main__":
    sat_info = [{"sat_name": "C01", "sat_file": "C01_wheel_speed.csv"},
                {"sat_name": "C02", "sat_file": "C02_wheel_speed.csv"},
                {"sat_name": "C03", "sat_file": "C03_wheel_speed.csv"},
                {"sat_name": "C04", "sat_file": "C04_wheel_speed.csv"}]

    for sat_index in range(len(sat_info)):
        data = np.loadtxt(sat_info[sat_index]['sat_file'],
                          delimiter=',', skiprows=1, encoding='utf-8')

        valid_index = []
        for i in range(len(data[:, 0])):
            if data[i, 1] == 0 and data[i, 2] == 0 and data[i, 3] == 0 and data[i, 4] == 0:
                pass
            else:
                valid_index.append(i)

        print(f"{sat_info[sat_index]['sat_name']} 卫星")
        for wheel_num in range(4):
            dt = calc_slide_time(
                data[valid_index, 0]/1000, data[valid_index, wheel_num + 1], 5990, 3000)
            print(f"飞轮 {wheel_num} 惯滑时间为 {dt:.0f} s")
