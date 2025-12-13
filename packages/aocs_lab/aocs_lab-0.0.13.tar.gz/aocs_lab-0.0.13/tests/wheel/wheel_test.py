"""飞轮惯滑时间计算"""
import numpy as np
from aocs_lab.utils import time
from aocs_lab.influxdb import influxdb2
from aocs_lab.wheel import wheel_data_process


def gen_database(sat_name: str) -> dict:
    """生成数据库信息"""
    database = {}
    database['url'] = "http://172.16.110.211:8086"
    database['token'] = (
        "u0OGUlvv6IGGYSxpoZGZNjenBtE-1ADcdun-W-0oacL66cef5DXPmDwVzj93oP1MRBBCCUOWNFS9yMb77o5OCQ=="
    )
    database['org'] = "gs"
    database['bucket'] = f'piesat02_{sat_name}_database'

    return database

# wheel_test_a02 = {
#     "start_time": '2025-02-12T15:10:00',
#     "end_time": '2025-02-12T15:30:00',
#     "tm_tag": ['TMK738', 'TMK739', 'TMK740', 'TMK741']
# }


def letters_to_numbers(letters):
    """字母转数字"""
    return [ord(letter) - ord('A') for letter in letters]


def number_to_letter(number):
    """数字转字母"""
    return chr(number + ord('A'))


def calc_slide_time(
        start_time: str,
        end_time: str,
        sat_name: str,
        wheel_list: list = None,
        tm_tag: list = None) -> str:
    """
    计算飞轮惯滑时间

    Args:
        start_time: 开始时间
        end_time: 结束时间
        sat_name: 卫星名称。例如 'b01'
        wheel_list: 飞轮列表。例如 ['A', 'B', 'C', 'D']
        tm_tag: TM标签。默认为 ['TMKA553', 'TMKA561', 'TMKA569', 'TMKA577']
    """

    if wheel_list is None:
        wheel_list = ['A', 'B', 'C', 'D']

    if tm_tag is None:
        tm_tag = ['TMKA553', 'TMKA561', 'TMKA569', 'TMKA577']

    data_list = influxdb2.get_field_value_from_influxdb(
        gen_database(sat_name),
        time.beijing_to_utc_time_str(start_time),
        time.beijing_to_utc_time_str(end_time),
        tm_tag)

    data_array = np.array(data_list)

    for i in letters_to_numbers(wheel_list):
        dt = wheel_data_process.calc_slide_time(
            data_array[:, 0], data_array[:, i+1], 5990, 3000)
        print(f"飞轮 {number_to_letter(i)} 惯滑时间为 {dt:.0f} s")
        return f"飞轮 {number_to_letter(i)} 惯滑时间为 {dt:.0f} s"


if __name__ == '__main__':
    calc_slide_time(
        '2025-02-19T16:20:00',
        '2025-02-19T16:50:00',
        'b01',
        ['C'])
