# 常用工具类函数
# 作者：Ricky
# 日期：2024-11-22

from urllib.parse import quote
import os
import json
import socket
import requests


# 推送通知
# https://api.day.app/[token]/这里改成你自己的推送内容
def bark_ts(token, content):
    # 1.推送内容，并urlencode编码
    content = quote(content)
    # 2.推送url,content参数需要urlencode编码
    url = f'https://api.day.app/{token}/{content}'
    # 3.发送请求
    response = requests.get(url=url)


# 检查端口是否被占用
# 返回值：
# used_ports 已使用端口数组,
# unused_ports 未使用端口数组
def check_port(ports):
    unused_ports = []
    used_ports = []
    tPort = ports[0]
    while tPort < ports[-1]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', tPort))
        if result == 0:
            sock.close()
            used_ports.append(tPort)
        else:
            unused_ports.append(tPort)
        tPort += 1
    return used_ports, unused_ports

# log.json文件
def update_data_log(taskname, username, updateDict):
    dataLogFile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'volume', 'data', 'log.json')
    dataLog = json.load(open(dataLogFile, 'r', encoding='utf-8'))
    k = f"{taskname}=={username}"
    for key, value in updateDict.items():
        if key == "finishDate":
            if value not in dataLog["task"][k]["finishDates"]:
                dataLog["task"][k]["finishDates"].append(value)
        else:
            dataLog["task"][k][key] = value

    json.dump(dataLog, open(dataLogFile, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

# 获取config.json的task
def get_config_task(taskname, username):
    configFile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'volume', 'config', 'config.json')
    config = json.load(open(configFile, 'r', encoding='utf-8'))
    task = None
    for item in config["taskList"]:
        if item["name"] == taskname and item["username"] == username:
            task = item
            break

    return task