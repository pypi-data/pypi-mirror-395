"""ats server api 调试"""
import json
import uuid
import time
import sys
import xml.etree.ElementTree as ET
import http.client
import requests
import signalr_sub


sys.stdout.reconfigure(encoding='utf-8')

# 启用 http.client 的调试
http.client.HTTPConnection.debuglevel = 0


def get_token(path):
    """
    获取 token
    """
    ams_server = "http://10.60.10.44:7000"
    url = ams_server + '/api/v1/user/login'
    data_user = {
        "name": "wangzhao",
        "password": "wangzhao"
    }

    response = requests.post(url, json=data_user, timeout=10)

    if response.status_code == 200:
        json_data = response.json()

        formatted_json = json.dumps(json_data, indent=4, ensure_ascii=False)
        print(formatted_json)

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=4)
    else:
        print(f"请求失败，状态码: {response.status_code}")


def read_token(path):
    """
    读取 token
    """
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['data']['token']


def cmd(ats_server: str, token: str):
    """
    发送单条命令
    """
    url = ats_server + '/api/v1/Tc/Send'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    data = {
        "commandType": "TcPacket",
        "isSecret": False,
        "commandCode": "TCK2000",
        "commandParam": {
            "type": '0x99999999',
            "control_mode": '0x22222222',
        },
        "targetDevice": "CAN",
        "isJudge": False,
        "judgeTimeout": 10,
        "remark": "string",
        "canOption": {
            "canType": "Outer",
            "canBus": "A",
            "showConsole": True
        },
        "customBaseJudgeOption": {
            "isAddWithDefault": True,
            "judge": "string"
        },
        "customDiffJudgeOption": {
            "isAddWithDefault": True,
            "judge": "string"
        },
        "customParamJudgeOption": {
            "isAddWithDefault": True,
            "judge": "string"
        }
    }

    # response = requests.get(url, headers=headers, json=data, timeout=10)
    response = requests.post(url, headers=headers, json=data, timeout=10)

    # 检查请求是否成功
    if response.status_code == 200:
        json_data = response.json()

        formatted_json = json.dumps(json_data, indent=4, ensure_ascii=False)
        print(formatted_json)
    else:
        print(f"请求失败，状态码: {response.status_code}")


def cmd_list(ats_server: str, token: str, command_chain: dict, jobid: str):
    """
    发送指令链
    """
    url = ats_server + '/api/v1/Regulation/Start'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    data = {
        "jobId": jobid,
        "fileName": "...............",
        "test": "...............",
        "testId": "1",
        "isJudge": True,
        "ignoreJudgeFailure": False,
        "isSecret": False,
        "loop": 1,
        "id": "",
        "version": "",
        "targetDevice": "CAN",
        "commandType": "TcPacket",
        "canOption": {
            "canType": "Inner",
            "canBus": "A",
            "showConsole": True
        },
        "commandChain": [
            command_chain
        ],
        "recovery": ""
    }

    response = requests.post(url, headers=headers, json=data, timeout=10)

    # 检查请求是否成功
    if response.status_code == 200:
        # json_data = response.json()
        # print(json_data)
        pass
    else:
        print(f"指令链执行: 请求失败，状态码: {response.status_code}")


def cmd_list_get(ats_server: str, jobid: str):
    """获取任务执行信息ID列表"""
    url = ats_server + '/api/v1/Regulation/JobInfo' + f'/{jobid}'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    response = requests.get(url, headers=headers, timeout=10)

    # 检查请求是否成功
    cmd_list_over = True
    if response.status_code == 200:
        json_data = response.json()

        # formatted_json = json.dumps(json_data, indent=4, ensure_ascii=False)
        # print(formatted_json)

        if json_data['data'] is not None:
            if json_data['data']['status'] == 'Running':
                cmd_list_over = False
    else:
        print(f"指令链执行情况查询: 请求失败，状态码: {response.status_code}")
        cmd_list_over = True

    return cmd_list_over

def cmd_list_err_ignore(ats_server: str, jobid: str, token: str):
    """获取任务执行信息ID列表"""
    url = ats_server + '/api/v1/Job/Manage'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    data = {
        "jobId": jobid,
        "type": "Ignore"
    }

    response = requests.post(url, headers=headers, json=data, timeout=10)

    # 检查请求是否成功
    if response.status_code == 200:
        # json_data = response.json()
        # formatted_json = json.dumps(json_data, indent=4, ensure_ascii=False)
        # print(formatted_json)
        pass

    else:
        print(f"指令链判读失败忽略: 请求失败，状态码: {response.status_code}")



def parse_xml(xml_file: str):
    """
    解析 ats web 导出的指令链 xml 文件
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    result = {
        'id': '',
        'version': '',
        "variables": [],
        'name': '',
        'commands': []
    }

    for _, command_chain in enumerate(root.find('CommandChains').findall('CommandChain')):
        chain = {
            'type': command_chain.get('Type'),
            'code': command_chain.get('Code'),
            'name': '...',
            'count': int(command_chain.get('Count')),
            'delayAfter': int(command_chain.get('Delay')),
            'judgeTimeout': int(command_chain.get('PostJudgeTimeout')),
            'params': {},
        }

        # 解析 Params
        params = command_chain.find('Params')
        for param in params.findall('Map'):
            chain['params'][param.get('Key')] = param.get('Value')

        # 解析 Judges
        judge = command_chain.find('BaseJudge')

        chain['customBaseJudge'] = {
            'judge': judge.get('Custom'),
            'isAddWithDefault': bool(judge.get('Logic') == 'AND')
        }

        judge = command_chain.find('DiffJudge')
        chain['customDiffJudge'] = {
            'judge': judge.get('Custom'),
            'isAddWithDefault': bool(judge.get('Logic') == 'AND')
        }

        judge = command_chain.find('ParamJudge')
        chain['customParamJudge'] = {
            'judge': judge.get('Custom'),
            'isAddWithDefault': bool(judge.get('Logic') == 'AND')
        }

        result['commands'].append(chain)

    # print(json.dumps(result, indent=4, ensure_ascii=False))

    return result

command_chain_all = [
    {
        "path": 'cmd_chain/自动化测试-1.xml',
        "uuid": "",
    },
    {
        "path": 'cmd_chain/自动化测试-2.xml',
        "uuid": "",
    }
]

ATS_SERVER = 'http://10.60.10.44:10701'

def on_message(messages):
    """处理接收到的消息"""
    for command_chain in command_chain_all:
        if messages[0] == command_chain['uuid']:
            # print(f"收到消息: {messages}")
            if messages[5] == 'Failed':
                cmd_list_err_ignore(ATS_SERVER, command_chain['uuid'], read_token('user.json'))

            if messages[5] == 'Successed' or messages[5] == 'Failed':
                print(f"cmd list: {command_chain['path']}, cmd index: {messages[2]}, status: {messages[5]}")



def main():
    """
    主函数
    """

    # cmd(ats_server, user_token)
    # cmd_list(ATS_SERVER, read_token('user.json'))

    # 读取 token, token 有效期为一周，超时需要重新获取
    # get_token('user.json')
    user_token = read_token('user.json')

    # 启动 signalr 订阅
    connection = signalr_sub.signalr_subscription(
        ATS_SERVER + "/pushhub",
        on_message)

    # 遍历发送指令链
    for index, chain in enumerate(command_chain_all):
        command_chain_json = parse_xml(chain['path'])

        jobid = str(uuid.uuid4())
        command_chain_all[index]['uuid'] = jobid

        cmd_list(ATS_SERVER,
                 user_token,
                 command_chain_json,
                 jobid)

        # 轮询队列执行状态，执行结束后开始下一指令链
        while True:
            time.sleep(1)
            if cmd_list_get(ATS_SERVER, jobid) is True:
                break

    # 停止 signalr 订阅
    connection.stop()





if __name__ == '__main__':
    main()
