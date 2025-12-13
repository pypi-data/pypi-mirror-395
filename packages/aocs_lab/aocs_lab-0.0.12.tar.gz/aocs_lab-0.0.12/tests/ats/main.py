import subprocess
import sys

def run_script_with_logging(script_path, log_file):
    """
    启动另一个 Python 脚本，将标准输出和错误输出重定向到文件。
    如果脚本执行报错，停止运行。
    
    :param script_path: 要运行的 Python 脚本路径
    :param log_file: 日志文件路径
    """
    try:
        # 打开日志文件
        with open(log_file, 'w', encoding='utf-8') as log:
            # 使用当前 Python 解释器路径（支持虚拟环境）
            python_executable = sys.executable
            # 启动子进程运行脚本
            process = subprocess.run(
                [python_executable, script_path],  # 调用 Python 解释器运行脚本
                stdout=log,               # 标准输出重定向到日志文件
                stderr=log,               # 错误输出重定向到日志文件
                check=True,                # 如果子进程返回非零退出码，则抛出异常
                encoding='utf-8'           # 以 UTF-8 编码解析输出
            )
            print(f"脚本 {script_path} 执行完成，日志已保存到 {log_file}")
    except subprocess.CalledProcessError as e:
        print(f"脚本 {script_path} 执行失败，退出码: {e.returncode}")
        print(f"请检查日志文件 {log_file} 获取详细信息。")
    except FileNotFoundError:
        print(f"无法找到脚本文件: {script_path}")
    except Exception as e:
        print(f"运行脚本时发生未知错误: {e}")


def auto_test():
    """
    自动化测试流程
    """
    process = subprocess.Popen(["python", "udp_forwarder.py"])
    print("遥测遥控转发服务已启动")


    print("发令判读流程开始")
    run_script_with_logging("ats_test.py", "ats_test.log")
    print("发令判读流程结束")

    process.terminate()
    print("遥测遥控转发服务已停止")


# 示例调用
if __name__ == "__main__":
    auto_test()

