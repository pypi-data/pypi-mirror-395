"""获取和处理 TLE 数据"""
import os
import sys
import json
import argparse
import requests

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.append(parent_dir)
import aocs_lab.spacetrack.tle as tle


if __name__ == "__main__":
    # 参数解析
    parser = argparse.ArgumentParser(description="TLE 数据获取与处理")
    parser.add_argument('-d', '--download',
                        action='store_true', help="下载 TLE 数据")
    parser.add_argument('-a', '--analyse',
                        action='store_true', help="分析 TLE 数据")
    args = parser.parse_args()

    cred = {'identity': 'wzhmwz@163.com', 'password': 'JXC5urv_rqr4gup3wmd'}
    sat_ids = [62333, 62334, 62335, 62336]

    if args.download:
        for sat_id in sat_ids:
            tle.get_tle_json_file(
                sat_id,
                "2024-12-24",
                "2024-12-27",
                cred,
                f"./{sat_id}.json")

    if args.analyse:
        for sat_id in sat_ids:
            file_path = f"{sat_id}.json"
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            print(f"{sat_id}: {data[-1]['SEMIMAJOR_AXIS']} km")


# A: 6904.259 km, 75.921 deg
# B: 6903.398 km, 85.391 deg
# C: 6903.139 km, 88.081 deg
# D: 6902.575 km, 94.432 deg
