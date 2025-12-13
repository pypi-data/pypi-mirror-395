"""SignalR 消息订阅服务"""
from signalrcore.hub_connection_builder import HubConnectionBuilder


def on_message(messages):
    """处理接收到的消息"""
    print("收到消息:", messages)




def signalr_subscription(hub_url, on_message_recv):
    """SignalR 消息订阅服务"""
    # 创建 Hub 连接
    connection = HubConnectionBuilder()\
        .with_url(hub_url)\
        .with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
            "max_attempts": 5
        })\
        .build()

    # 假设服务器推送的方法名为 "ReceiveMessage"
    connection.on("ReceiveRegulationJobCommandChainProgress", on_message_recv)

    # 连接打开时的回调
    connection.on_open(lambda: print("连接已打开"))

    # 连接关闭时的回调
    connection.on_close(lambda: print("连接已关闭"))

    # 启动连接
    try:
        connection.start()
        print("正在连接到 SignalR Hub...")
    except ConnectionError as e:
        print(f"连接失败: {e}")
        return

    return connection


if __name__ == "__main__":
    signalr_subscription("http://10.60.10.44:10701/pushhub", on_message)
