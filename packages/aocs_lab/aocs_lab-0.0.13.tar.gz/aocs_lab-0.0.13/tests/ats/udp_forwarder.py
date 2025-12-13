"""UDP 监听转发服务"""
import socket
import threading


def add_tmprocess_header(data: bytes) -> bytes:
    """添加 TMProcess 头部"""
    length = len(data)  # 数据长度
    length_bytes = length.to_bytes(2, byteorder='big')

    header = b'\xca\xfe' + length_bytes + b'\x15\x01\x00'

    return header + data


def remove_ats_server_header(data: bytes) -> bytes:
    """去除 ATS Server 指令头部"""
    if len(data) > 7:
        # 去除前7个字节
        return data[7:]
    else:
        print("data length is less than 7 bytes")
        # 长度异常直接返回原值
        return data


def udp_forwarder(source_port, destination_ip, destination_port, data_process_func):
    """udp 转发器"""
    # 创建源 UDP 套接字
    source_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    source_sock.bind(('0.0.0.0', source_port))

    # 创建目标 UDP 套接字
    dest_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(
        f"UDP 转发器已启动，从端口 {source_port} 转发到 {destination_ip}:{destination_port}")

    try:
        while True:
            # 接收数据
            data, addr = source_sock.recvfrom(65535)  # 最大 UDP 数据包大小

            modified_data = data_process_func(data)

            # 转发到目标端口
            dest_sock.sendto(
                modified_data, (destination_ip, destination_port))
            print(
                f"已转发 {len(modified_data)} 字节从 {addr} 到 {destination_ip}:{destination_port}")

    except KeyboardInterrupt:
        print(f"\n转发器已停止 (端口 {source_port})")

    finally:
        source_sock.close()
        dest_sock.close()


def main():
    """主线程"""
    # 配置源端口，目标ip，目标端口，转发数据处理函数
    services = [
        (10086, "127.0.0.1", 5555, remove_ats_server_header),
        (10087, "10.60.10.44", 50700, add_tmprocess_header),
    ]

    for source_port, dest_ip, dest_port, func in services:
        thread = threading.Thread(
            target=udp_forwarder, args=(source_port, dest_ip, dest_port, func))
        thread.daemon = True  # 设置为守护线程
        thread.start()

    try:
        while True:
            pass  # 主线程保持运行，等待用户中断
    except KeyboardInterrupt:
        print("\n捕获到中断信号, 程序即将退出...")


if __name__ == "__main__":
    main()
