# 常用工具类函数
# 作者：Ricky
# 日期：2024-11-22

import os
import json
import socket
from typing import Literal, Optional
from enum import Enum
from faker import Faker

class FakeDataType(Enum):
    NAME = "name"
    COUNTRY = "country"
    COMPANY = "company"
    EMAIL = "email"
    PHONE = "phone_number"
    ADDRESS = "address"
    ALL = "all"

def faker_str(type_name: str = "all") -> str:
    """生成随机假数据
    
    Args:
        type_name: 数据类型，可选值为 name/country/company/email/phone_number/address/all
                  默认为 all (随机选择一种类型)
    
    Returns:
        str: 生成的随机数据
        
    Examples:
        >>> faker_str("name")  
        '张三'
        >>> faker_str("email")
        'example@email.com'
    """
    fake = Faker("zh_CN")
    
    # 数据类型映射表
    type_mapping = {
        FakeDataType.NAME.value: fake.name,
        FakeDataType.COUNTRY.value: fake.country,
        FakeDataType.COMPANY.value: fake.company,
        FakeDataType.EMAIL.value: fake.email,
        FakeDataType.PHONE.value: fake.phone_number,
        FakeDataType.ADDRESS.value: fake.address
    }

    try:
        # 如果类型不存在或为 all，随机选择一个类型
        if type_name not in type_mapping or type_name == FakeDataType.ALL.value:
            type_name = fake.random_element(list(type_mapping.keys()))
            
        return type_mapping[type_name]()
        
    except Exception as e:
        print(f"生成随机数据时发生错误: {str(e)}")
        return fake.name()  # 发生错误时返回默认值

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