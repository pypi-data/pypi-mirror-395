"""灵知 05 发射时间线绘制"""
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.dates as mdates
from matplotlib.axes import Axes

# 阳照区开始
sun_start = [
    datetime(2024, 12, 17, 3, 16, 50),
    datetime(2024, 12, 17, 4, 52, 11),
    datetime(2024, 12, 17, 6, 27, 32),
    datetime(2024, 12, 17, 8, 2, 54)
]

# 阳照区结束
sun_end = [
    datetime(2024, 12, 17, 4, 18, 46),
    datetime(2024, 12, 17, 5, 54, 7),
    datetime(2024, 12, 17, 7, 29, 28),
    datetime(2024, 12, 17, 9, 4, 49)
]

# 升交点时间
anode_time = [
    datetime(2024, 12, 17, 3, 53, 50),
    datetime(2024, 12, 17, 5, 29, 20),
    datetime(2024, 12, 17, 7, 4, 40),
    datetime(2024, 12, 17, 8, 40, 0)
]

# 卫星事件点
sat_dates0 = [
    {
        "text": "发射",
        "time": datetime(2024, 12, 17, 2, 50, 47)
    }
]

sat_dates1 = [
    {
        "text": "C01 星箭分离 (T0)",
        "time": datetime(2024, 12, 17, 3, 4, 51)
    },
    {
        "text": "\n\n\n\nC02 星箭分离",
        "time": datetime(2024, 12, 17, 3, 4, 52)
    },
    {
        "text": "C03 星箭分离",
        "time": datetime(2024, 12, 17, 3, 5, 26)
    },
    {
        "text": "C04 星箭分离",
        "time": datetime(2024, 12, 17, 3, 5, 56)
    }
]

sat_dates2 = [
    {
        "text": "C01 最早展帆板时间 (T0+220s)",
        "time": sat_dates1[0]['time'] + timedelta(seconds=220)
    },
    {
        "text": "C01 最晚展帆板时间 (T0+250s)\n(初始角速度 2 deg/s)",
        "time": sat_dates1[0]['time'] + timedelta(seconds=250)
    },
    {
        "text": "C01 最早进对日一阶段时间 (T0+370s)",
        "time": sat_dates1[0]['time'] + timedelta(seconds=220) + timedelta(seconds=150)
    },
    {
        "text": "C03 最早展帆板时间",
        "time": sat_dates1[2]['time'] + timedelta(seconds=220)
    },
    {
        "text": "C04 最早展帆板时间",
        "time": sat_dates1[3]['time'] + timedelta(seconds=220)
    },
    # {
    #     "text": "C04 最晚展帆板时间\n(初始角速度 2 deg/s)",
    #     "time": sat_dates1[3]['time'] + timedelta(seconds=250)
    # },
    # {
    #     "text": "C03 最早进对日一阶段时间",
    #     "time": sat_dates1[3]['time'] + timedelta(seconds=220) + timedelta(seconds=150)
    # },
]


#  过站时间线
station_time = [
    {
        "name": "马来站",
        "task": "确认星箭分离\n进阻尼三阶段\n帆板解锁",
        "time":
        [
            datetime.fromisoformat("2024-12-17 03:04:51"),
            datetime.fromisoformat("2024-12-17 03:09:42"),
        ]
    },
    # {
    #     "name": "阿根廷站",
    #     "task": "确认对日四阶段（自旋对日）\nSAR 天线展开",
    #     "time":
    #     [
    #         datetime(2024, 12, 17, 3, 34, 32),
    #         datetime(2024, 12, 17, 3, 44, 48)
    #     ]
    # },
    # {
    #     "name": "中西部地面站",
    #     "task": "确认对日四阶段（自旋对日）\nSAR 天线展开",
    #     "time":
    #     [
    #         datetime(2024, 12, 17, 4, 23, 34),
    #         datetime(2024, 12, 17, 4, 37, 59)
    #     ]
    # },
    # {
    #     "name": "阿根廷站",
    #     "task": "星敏对准、校时、组合开启",
    #     "time":
    #     [
    #         datetime(2024, 12, 17, 5, 10, 4),
    #         datetime(2024, 12, 17, 5, 15, 58)
    #     ]
    # },
    # {
    #     "name": "中西部地面站\n一星一站跟踪",
    #     "task": "星敏接入\n转约束对日",
    #     "time":
    #     [
    #         datetime(2024, 12, 17, 5, 59, 16),
    #         datetime(2024, 12, 17, 6, 10, 7)
    #     ]
    # },
    # {
    #     "name": "阿塞拜疆",
    #     "task": "星敏对准、校时、组合开启\n陀螺温补，零位设置",
    #     "time":
    #     [
    #         datetime(2024, 12, 17, 7, 35, 27),
    #         datetime(2024, 12, 17, 7, 45, 2)
    #     ]
    # },
    # {
    #     "name": "南非",
    #     "time":
    #     [
    #         datetime(2024, 12, 17, 7, 56, 45),
    #         datetime(2024, 12, 17, 8, 5, 42)
    #     ]
    # }
]


def plot_time_line_of_station(plt_ax: Axes, dates: datetime,
                              station_name: str, task: str,
                              color="red", linewidth=5):
    """绘制过站时间线"""
    # 绘制时间线
    plt_ax.hlines(y=-0.1, xmin=min(dates), xmax=max(dates),
              color=color, linewidth=linewidth, zorder=3)
    # 添加站点标签
    plt_ax.text(dates[0], -0.4, dates[0].strftime("%H:%M:%S"),
            ha="right", va="bottom", fontsize=10, rotation=45)
    plt_ax.text(dates[1], -0.4, dates[1].strftime("%H:%M:%S"),
            ha="right", va="bottom", fontsize=10, rotation=45)
    dt = dates[1] - dates[0]
    minutes, seconds = divmod(dt.seconds, 60)
    plt_ax.text(dates[0], -0.6,  f'{station_name}\n{minutes}m{seconds}s',
            ha="left", va="bottom", fontsize=10)
    plt_ax.text(dates[0], -0.8,  f'{task}', ha="left",
            va="bottom", fontsize=10, color="red")


def plot_time_line_of_sat(plt_ax: Axes, times: list[dict]):
    """绘制卫星时间线"""
    timeline = [time["time"] for time in times]
    plt_ax.hlines(y=0, xmin=min(timeline), xmax=max(timeline),
              color="gray", linewidth=1.5)
    plt_ax.scatter(timeline, [0] * len(timeline), color="blue", zorder=2)

    for time in times:
        text = f"{time['text']}\n{time['time'].strftime('%H:%M:%S')}"
        plt_ax.text(time['time'], 0.2, text,
                ha="left", va="bottom", fontsize=10, rotation=45)


if __name__ == "__main__":
    # 全局设置字体为 SimHei
    rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    rcParams['axes.unicode_minus'] = False   # 解决负号显示问题

    # 创建图形
    fig, ax = plt.subplots(figsize=(20, 6))

    # 绘制卫星时间线
    plot_time_line_of_sat(ax, sat_dates1 + sat_dates2)

    # 绘制过站时间线
    for i in range(len(station_time)-6):
        plot_time_line_of_station(
            ax, station_time[i]["time"], station_time[i]["name"], station_time[i]["task"])

    # 阳照区绘制
    for i in range(0):
        ax.axvspan(sun_start[i], sun_end[i],
                   color="yellow", alpha=0.5, zorder=1, ymin=0, ymax=0.5)  # 矩形块
        ax.text(sun_start[i], -0.95,
                f'阳照区时间\n{
                    sun_start[i].strftime("%H:%M:%S")} ~ {sun_end[i].strftime("%H:%M:%S")}',
            ha="left", va="bottom", fontsize=10)

    # 圈次绘制
    for i in range(0):
        ax.axvspan(anode_time[i], anode_time[i+1],
                   color="lightblue", alpha=0.5, zorder=1, ymin=0.5, ymax=1)  # 矩形块
        ax.text(anode_time[i], 0.8,
                f'升交点时间\n{anode_time[i].strftime("%H:%M:%S")}\n圈次计数: {i+1}',
                ha="left", va="bottom", fontsize=10)

    # 设置 x 轴日期格式
    date_format = mdates.DateFormatter('%Y-%m-%d\n%H:%M:%S\n%A')  # 自定义日期格式
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()  # 自动调整日期标签角度

    # 美化时间线
    ax.set_ylim(-1, 1)
    ax.set_yticks([])  # 隐藏 y 轴刻度
    ax.grid(visible=False)  # 不显示网格线
    plt.tight_layout()

    # 显示图形
    plt.savefig("timeline_highres.png", dpi=300,
                bbox_inches="tight")  # 设置分辨率和边框
    # plt.show()
