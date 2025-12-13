"""just for calculate"""
from datetime import datetime, timedelta
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(parent_dir)
import aocs_lab.influxdb.influxdb1 as influxdb1
import aocs_lab.file.csv_file as csv_file

time_info = [
    {
        "sat_name": "C01",
        "direction": "+X",
        "duration": 2400,
        # 2 Jan 2025 10:21:00.000                   21.258
        # 3 Jan 2025 10:09:00.000                   18.225
        # 4 Jan 2025 06:46:00.000                   13.912
        # 5 Jan 2025 06:33:30.000                    9.761
        # 6 Jan 2025 09:32:00.000                    7.711
        "utc": datetime.fromisoformat("2025-01-06 09:32:00.000"),
    },
    {
        "sat_name": "C02",
        "direction": "+X",
        "duration": 2400,
        # 2 Jan 2025 10:18:00.000                   25.390
        # 3 Jan 2025 10:06:00.000                   22.243
        # 5 Jan 2025 06:31:00.000                   13.396
        "utc": datetime.fromisoformat("2025-01-05 06:31:00.000"),
    },
    {
        "sat_name": "C03",
        "direction": "+X",
        "duration": 2400,
        # 6 Jan 2025 09:15:00.000                   13.442
        "utc": datetime.fromisoformat("2025-01-06 09:15:00.000"),
    },
    {
        "sat_name": "C04",
        "direction": "+X",
        "duration": 2400,
        # 14 Jan 2025 00:48:00.000                  347.274
        "utc": datetime.fromisoformat("2025-01-14 00:48:00.000"),
    },
]

evs = [
    {
        "ex": -9.1e-4,
        "ey": -1.2e-4,
        "dir": "+x",
    },
    {
        "ex": -8.6e-4,
        "ey": -2.1e-4,
        "dir": "+x",
    },
    {
        "ex": -10.7e-4,
        "ey": -2.6e-4,
        "dir": "+x",
    },
    {
        "ex": -5.3e-4,
        "ey": 1.3e-4,
        "dir": "+x",
    },
]


def anlyse_orbit():
    """分析轨道"""  
    names = piesat2c["name"]

    # ex, ey 变化
    _, ax = plt.subplots()
    for name in names:
        data = csv_file.read_csv(f"{name['sat_name']}.csv")
        ex = [e['d_ex'] for e in data]
        ey = [e['d_ey'] for e in data]
        ax.plot(ex, ey, label=name['sat_name'], marker='.')

    ax.set_aspect("equal", "box")
    ax.legend()
    ax.set_xlabel("d_ex")
    ax.set_ylabel("d_ey")
    plt.grid()
    plt.xlim(-0.002, 0.002)
    plt.ylim(-0.002, 0.002)
    plt.show()

    _, ax = plt.subplots()
    for name in names:
        data = csv_file.read_csv(f"{name['sat_name']}.csv")
        a = [e['a_mean'] for e in data]
        ax.plot(a, label=name['sat_name'], marker='.')

def anlyse_orbit2():
    """分析轨道"""
    for ev in evs:
        ex = ev["ex"]
        ey = ev["ey"]
        if ev["dir"] == "+x":
            omega = np.arctan2(-ey, -ex)
        else:
            omega = np.arctan2(ey, ex)

        if omega < 0:
            omega += 2*np.pi

        e_norm = np.sqrt(ex**2 + ey**2)
        print(f"omega: {np.degrees(omega):3.0f} deg, e_norm: {e_norm:.5f}")


def fire_time_list(
        first_mid_time: datetime,
        window_start_bj: datetime,
        window_end_bj: datetime,
        period: float,
        fire_duration: float) -> list[datetime]:
    """计算同一纬度幅角的轨控时间列表"""
    # 找第一个轨控时间
    first_mid_time_bj = first_mid_time + timedelta(hours=8)
    for i in range(0, 40, 1):
        mid_time_temp = first_mid_time_bj + timedelta(seconds=period*i)
        if mid_time_temp >= window_start_bj:
            first_mid_time_bj = mid_time_temp
            break

    # 找后续轨控时间
    time_list = []
    for i in range(0, 40, 2):
        mid_time_bj = first_mid_time_bj + timedelta(seconds=period*i)

        if window_start_bj <= mid_time_bj <= window_end_bj:
            start_time_bj = mid_time_bj - timedelta(seconds=fire_duration/2)
            time_list.append(start_time_bj)

    return time_list


def generate_fire_time_file():
    """生成轨控策略文件"""
    window_start_bj = datetime.fromisoformat("2025-01-14 20:00:00.000")
    window_end_bj = datetime.fromisoformat("2025-01-15 12:00:00.000")
    orbit_period = 5710

    txt = ""
    for info in time_info:
        start_time_bj_list = fire_time_list(
            info["utc"],
            window_start_bj,
            window_end_bj,
            orbit_period,
            info["duration"])

        txt += f"# {info["sat_name"]} 星轨控策略\n"
        for index, time_bj in enumerate(start_time_bj_list):
            txt += (f"## 第 {index+1} 次轨控\n")
            txt += (f"  推进方向:     {info["direction"]}\n")
            txt += (f"  轨控开始时间: {time_bj.timestamp():.0f}s  (UTC+8: {time_bj})\n")
            txt += (f"  轨控结束时间: {(time_bj.timestamp() +
                    info["duration"]):.0f}s\n")
            txt += "\n"
        txt += "\n"

    with open(f"{window_start_bj.strftime("%Y%m%d")} 轨控.txt", "w", encoding='utf-8') as file:
        file.write(txt)


def generate_fire_time_file_csv(
        window_start_bj: datetime,
        window_end_bj: datetime,
        orbit_period: float):
    """生成轨控策略文件"""
    txt = ""
    for info in time_info:
        start_time_bj_list = fire_time_list(
            info["utc"],
            window_start_bj,
            window_end_bj,
            orbit_period,
            info["duration"])

        for _, time_bj in enumerate(start_time_bj_list):
            txt += f"{info["sat_name"]},"
            txt += (f"{info["direction"]},")
            txt += (f"{time_bj.timestamp():.0f},")
            txt += (f"{(time_bj.timestamp() + info["duration"]):.0f}")
            txt += "\n"

    with open(f"{window_start_bj.strftime("%Y%m%d")} 轨控.csv", "w", encoding='utf-8') as file:
        file.write(txt)

piesat2c = {
    "name": [
        {
            "sat_name": "A",
            "tag": "PIESAT02_C01",
        },
        {
            "sat_name": "B",
            "tag": "PIESAT02_C02",
        },
        {
            "sat_name": "C",
            "tag": "PIESAT02_C03",
        },
        {
            "sat_name": "D",
            "tag": "PIESAT02_C04",
        },
    ],

    "database": {
        "host_ip": "172.16.8.161",
        "host_port": 32728,
        "database": "measure",
        "measurement": "tm_all_PIESAT2C"
    },

    # 键名映射
    "key_mapping": {
        "TMK3001": "unix_time",
        "TMK3002": "a_mean",
        "TMK3003": "e_mean",
        "TMK3040": "reletive_valid",
        "TMK3041": "d_a",
        "TMK3042": "d_ex",
        "TMK3043": "d_ey",
        "TMK3044": "d_ix",
        "TMK3045": "d_iy",
        "TMK3046": "d_u",
    }
}

def rename_keys(data, key_mapping):
    """
    替换字典中键的命名
    :param data: 输入的字典或字典列表
    :param key_mapping: 键名映射字典，例如 {"old_key": "new_key"}
    :return: 替换键名后的字典或字典列表
    """
    if isinstance(data, dict):
        # 替换字典的键
        return {key_mapping.get(k, k): v for k, v in data.items()}
    elif isinstance(data, list):
        # 如果是列表，则逐个替换其中每个字典的键
        return [rename_keys(item, key_mapping) for item in data]
    else:
        # 如果数据不是字典或列表，直接返回
        return data


def get_data():
    """获取数据"""
    field = ", ".join(piesat2c["key_mapping"].keys())

    time_start = datetime.fromisoformat("2024-12-17 20:00:00.000")
    time_end = datetime.fromisoformat("2025-01-14 12:00:00.000")

    time_range = f" time > '{time_start.strftime(
        '%Y-%m-%dT%H:%M:%SZ')}' AND time < '{time_end.strftime('%Y-%m-%dT%H:%M:%SZ')}' "

    names = piesat2c["name"]
    for name in names:
        tag_key = f"_satelliteCode = '{name['tag']}'"
        data = influxdb1.get_database_points(
            piesat2c["database"],
            time_range,
            field,
            tag_key)

        updated_date = rename_keys(data, piesat2c["key_mapping"])

        csv_file.save_as_csv(f"{name['sat_name']}.csv", updated_date)


if __name__ == "__main__":
    # get_data()
    # anlyse_orbit()


    anlyse_orbit2()

    generate_fire_time_file_csv(
        window_start_bj=datetime.fromisoformat("2025-01-14 20:00:00.000"),
        window_end_bj=datetime.fromisoformat("2025-01-15 12:00:00.000"),
        orbit_period=5710)
