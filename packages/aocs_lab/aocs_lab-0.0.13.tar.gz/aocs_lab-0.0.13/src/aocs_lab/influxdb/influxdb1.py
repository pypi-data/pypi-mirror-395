"""操作 influxdb 1.x 数据库"""
from datetime import datetime
from influxdb import InfluxDBClient


def get_database_points(influxdb: dict, time_range, field, tag_key):
    """读取 influx 1.x"""

    # influxDB数据库信息
    influxdb_host_ip = influxdb['host_ip']
    influxdb_host_port = influxdb['host_port']
    influxdb_database = influxdb['database']
    influxdb_measurement = influxdb['measurement']

    # 连接数据库
    client = InfluxDBClient(host=influxdb_host_ip, port=influxdb_host_port)
    client.switch_database(influxdb_database)

    # 构造 SQL 查询语句
    query_str = \
        " SELECT " + field + \
        " FROM " + influxdb_measurement + \
        " WHERE " + time_range + " AND " + tag_key
    
    # print(query_str)

    # 发送查询请求
    result = client.query(query_str)

    # 获取查询结果中的数据
    points = list(result.get_points())

    return points


if __name__ == "__main__":
    time_start = datetime(2025, 1, 7, 0, 0, 0)
    time_end = datetime(2025, 1, 8, 23, 59, 59)
    TAG_KEY = "_satelliteCode = 'PIESAT02_C01'"

    FIELD = "TMK3001"

    time_range = \
        " time > '" + time_start.strftime('%Y-%m-%dT%H:%M:%SZ') + \
        "' AND time < '" + time_end.strftime('%Y-%m-%dT%H:%M:%SZ') + "' "

    database = {
        "host_ip": "172.16.8.161",
        "host_port": 32728,
        "database": "measure",
        "measurement": "tm_all_PIESAT2C"
    }

    # 获取固连系rv
    data = get_database_points(database, time_range, FIELD, TAG_KEY)

    print(data)
