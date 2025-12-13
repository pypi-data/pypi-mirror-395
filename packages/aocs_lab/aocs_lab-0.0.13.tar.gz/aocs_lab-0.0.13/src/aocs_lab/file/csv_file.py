"""文件操作相关的函数"""
import csv

def save_as_csv(csv_file_path: str, data: list[dict]):
    """保存列表数据为 CSV"""
    # 打开 CSV 文件进行写入
    with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
        # 获取 CSV 的列名
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # 写入表头
        writer.writeheader()

        # 写入数据
        for row in data:
            writer.writerow(row)

def read_csv(csv_file_path) -> list[dict]:
    """存储CSV数据的列表"""
    data = []

    # 打开CSV文件进行读取
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # 逐行读取数据
        for row in reader:
            converted_row = {key: float(value) for key, value in row.items()}
            data.append(converted_row)

    return data
