import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.append(parent_dir)
from aocs_lab.utils import time
from aocs_lab.influxdb import influxdb2

import numpy as np
import matplotlib.pyplot as plt

def gen_database(sat_name: str) -> dict:
    database = {}
    database['url'] = "http://172.16.110.211:8086"
    database['token'] = "u0OGUlvv6IGGYSxpoZGZNjenBtE-1ADcdun-W-0oacL66cef5DXPmDwVzj93oP1MRBBCCUOWNFS9yMb77o5OCQ=="
    database['org'] = "gs"
    database['bucket'] = f'piesat02_{sat_name}_database'

    return database

gyro_test = {
    "start_time": '2024-11-27T09:00:00',
    "end_time": '2024-11-27T09:30:00',
    "tm_tag": ['TMKA504', 'TMKA505', 'TMKA506']
}

if __name__ == "__main__":
    data_list = influxdb2.get_field_value_from_influxdb(
        gen_database('c01'),
        time.beijing_to_utc_time_str(gyro_test['start_time']), 
        time.beijing_to_utc_time_str(gyro_test['end_time']), 
        gyro_test['tm_tag'])

    data_array = np.array(data_list)

    mean = []
    std = []
    for i in range(1, 4):
        mean.append(np.mean(data_array[:,i]))
        std.append(np.std(data_array[:,i]))

    print(f'陀螺三轴均值 (deg/s):\n{mean[0]:.6f}\n{mean[1]:.6f}\n{mean[2]:.6f}')
    print(f'陀螺三轴标准差 (deg/s):\n{std[0]:.4e}\n{std[1]:.4e}\n{std[2]:.4e}')


    fig, ax = plt.subplots()
    ax.hist(data_array[:,i])
    plt.show()
