"""获取和处理 TLE 数据"""
import json
import argparse
import requests

def get_tle_json_file(norad_cat_id: int,
                      date_start: str,
                      date_end: str,
                      site_cred: dict,
                      file_path: str):
    """
    date_start and date_end should be in the format of "YYYY-MM-DD"
    """
    uri_base = "https://www.space-track.org"
    request_login = "/ajaxauth/login"
    request_controller = "/basicspacedata"
    request_action = "/query"
    request_class = f"/class/gp_history/NORAD_CAT_ID/{norad_cat_id}"
    request_class_date = f"/orderby/TLE_LINE1 ASC/EPOCH/{
        date_start}--{date_end}"
    request_class_format = "/format/json"

    with requests.Session() as session:
        resp = session.post(uri_base + request_login, data=site_cred)
        if resp.status_code != 200:
            raise ValueError("POST fail on login")

        resp = session.get(uri_base +
                           request_controller +
                           request_action +
                           request_class +
                           request_class_date +
                           request_class_format)
        if resp.status_code != 200:
            print(resp)
            raise ValueError(
                resp, "GET fail on request for Starlink satellites")

        ret_data = json.loads(resp.text)

        # Save JSON response to a file using UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(ret_data, json_file, indent=4)

        session.close()


if __name__ == "__main__":
    # 参数解析
    parser = argparse.ArgumentParser(description="TLE 数据获取与处理")
    parser.add_argument('-d', '--download',
                        action='store_true', help="下载 TLE 数据")
    parser.add_argument('-a', '--analyse',
                        action='store_true', help="分析 TLE 数据")
    args = parser.parse_args()

    cred = {'identity': '', 'password': ''}
    sat_ids = [62333, 62334, 62335, 62336]

    if args.download:
        for sat_id in sat_ids:
            get_tle_json_file(
                sat_id,
                "2024-12-24",
                "2024-12-27",
                cred,
                f"./{sat_id}.json")

    if args.analyse:
        for sat_id in sat_ids:
            with open(f"{sat_id}.json", 'r', encoding='utf-8') as file:
                data = json.load(file)

            print(f"{sat_id}: {data[-1]['SEMIMAJOR_AXIS']} km")
