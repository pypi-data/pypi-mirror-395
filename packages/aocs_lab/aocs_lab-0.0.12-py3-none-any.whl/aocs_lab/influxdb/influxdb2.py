from influxdb_client import InfluxDBClient
from ..utils.time import beijing_to_utc_time_str

def get_field_value_from_influxdb(database: dict, time_start: str, time_end: str, fields: list):
    fields_str = ''
    for i in range(len(fields)):
        if i == 0:
            fields_str += f'r._field == "{fields[i]}"'
        else:
            fields_str += f' or r._field == "{fields[i]}"'

    query = (f'from(bucket: "{database["bucket"]}") '
            f'|> range(start: {time_start}, stop: {time_end}) '
            f'|> filter(fn: (r) => {fields_str}) '
            f'|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")  ')


    with InfluxDBClient(url=database['url'], token=database['token'], org=database['org']) as client:
        tables = client.query_api().query(query)


    data_rows = []
    # 遍历查询结果
    for table in tables:
        for record in table.records:
            # 提取时间戳和每个字段的值
            row = []
            row.append(record.get_time().timestamp())
            for field in fields:
                row.append(record.values.get(field))
            
            data_rows.append(row)

    return data_rows



if __name__ == "__main__":
    sat_database = {
        'url': "http://172.16.110.211:8086",
        'token': "u0OGUlvv6IGGYSxpoZGZNjenBtE-1ADcdun-W-0oacL66cef5DXPmDwVzj93oP1MRBBCCUOWNFS9yMb77o5OCQ==",
        'org': "gs",
        'bucket': "piesat02_c04_database"
    }

    start_time = '2024-11-27T09:00:00'
    end_time = '2024-11-27T09:30:00'
    tm_tag = ['TMKA553', 'TMKA561', 'TMKA569', 'TMKA577']
    
    data_list = get_field_value_from_influxdb(
        sat_database,
        beijing_to_utc_time_str(start_time), 
        beijing_to_utc_time_str(end_time), 
        tm_tag)
    
    print(data_list)