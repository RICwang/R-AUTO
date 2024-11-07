# 导入
import multiprocessing
import os
import json
import time
import logging
import logging.handlers

from func.common import *
from lib.AutoV2ex import AutoV2ex
from lib.AutoMicrosoft import AutoMicrosoft

# 项目根目录
rootPath = os.path.dirname(__file__)

# 读取配置文件
configFile = os.path.join(rootPath, 'volume', 'config', 'config.json')
config = json.load(open(configFile, 'r', encoding='utf-8'))

# 日志配置
logFolder = os.path.join(rootPath, 'volume', 'logs')
logFormat = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s'
maxBytes = 20 * 1024 * 1024
backupCount = 5
logFile = os.path.join(logFolder, f"logger-main.log")
loggerMain = logging.getLogger()
logLevel = logging.DEBUG if config["debug"] else logging.INFO
loggerMain.setLevel(logLevel)
formatter = logging.Formatter(logFormat)
fileHandler = logging.handlers.RotatingFileHandler(logFile, maxBytes=maxBytes, backupCount=backupCount, encoding='utf-8')
fileHandler.setFormatter(formatter)
loggerMain.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
loggerMain.addHandler(consoleHandler)

# 初始化数据
loggerMain.info(f'正在初始化数据...')
dataLogFile = os.path.join(os.path.join(rootPath, 'volume', 'data'), 'log.json')
# 初始化data操作日志文件
dataLog = json.load(open(dataLogFile, 'r', encoding='utf-8'))
for task in config["taskList"]:
    if task["username"] == "":
        continue
    k = f'{task["name"]}=={task["username"]}'
    if k not in dataLog["task"]:
        dataLog["task"][k] = {
            "status": 0,
            "port": 0,
            "handlingDate": "",
            "finishDates": []
        }
json.dump(dataLog, open(dataLogFile, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
loggerMain.info(f'初始化数据完成')

# 消费者，执行任务
def task_worker(taskname, username, password, port):
    loggerMain.info(f'【{taskname}】任务开始')
    if username is None or password is None:
        loggerMain.info(f'用户名和密码没配置')
        return
    if port is None:
        loggerMain.info(f'端口没配置')
        return
    clz = None
    if taskname == "v2ex":
        clz = AutoV2ex(username=username, password=password, port=port, logger=loggerMain)
    elif taskname == "Microsoft":
        clz = AutoMicrosoft(username=username, password=password, port=port, logger=loggerMain)

    if clz is None:
        return
    
    while True:
        try:
            clz.main()
            if clz.res:
                loggerMain.info(f'【{taskname}】任务已完成')
                
                updateDictNew = {
                    'status': 0,
                    'port': 0,
                    "handlingDate": "",
                    "finishDate": time.strftime("%Y%m%d", time.localtime())
                }
                update_data_log(taskname=taskname, username=username, updateDict=updateDictNew)
                break
        except Exception as e:
            # 将e所有内容都输出到日志
            loggerMain.error(e, exc_info=True)

# 主函数
def main():
    loggerMain.info('开始任务')

    # 创建一个进程字典，port为key，进程为value
    processes = {}

    # 无限循环，每20秒执行一次
    while True:
        todayStr = time.strftime("%Y%m%d", time.localtime())
        timeStr = time.strftime("%H:%M:%S", time.localtime())

        # 判断是否在执行时间内
        if timeStr <= config["taskTime"][0] or timeStr >= config["taskTime"][1]:
            time.sleep(20)
            continue

        # 遍历检查端口是否被占用
        used_ports, unused_ports = check_port(config["ports"])
        loggerMain.debug(f'已使用端口：{used_ports}，未使用端口：{unused_ports}')

        # 读取json文件
        dataLog = json.load(open(dataLogFile, 'r', encoding='utf-8'))
        for k, task in dataLog["task"].items():
            kArray = k.split('==')
            taskname = kArray[0]
            username = kArray[1]
            finishDates = task["finishDates"] 
            # 执行完成的任务不再执行
            if todayStr in finishDates:
                continue
            
            # 任务正在执行中
            if task["status"] == 1:
                if task["port"] in unused_ports:
                    loggerMain.info(f'【{taskname}】端口【{task["port"]}】被释放，重启服务')
                    updateDictNew = {
                        "status" : 0,
                        "port" : 0,
                        "handlingDate" : ""
                    }
                    update_data_log(taskname=taskname, username=username, updateDict=updateDictNew)
                    continue

                handlingDate = task["handlingDate"]
                if todayStr != handlingDate:
                    # 今天之前的任务还在执行中，杀掉任务重启
                    if task["port"] in processes:
                        processes[task["port"]].terminate()
                        processes.pop(task["port"])

                    updateDictNew = {
                        "status" : 0,
                        "port" : 0,
                        "handlingDate" : ""
                    }
                    update_data_log(taskname=taskname, username=username, updateDict=updateDictNew)
                    loggerMain.info(f'重置【{taskname}】进程')
                    continue

            # 任务未执行
            if task["status"] == 0:
                loggerMain.info(f'【{taskname}】开始任务')
                # 更新config.json文件，将status置为1
                updateDictNew = {
                    "status": 1,
                    "handlingDate" : todayStr
                }
                # 从unused_ports取出一个端口，并从unused_ports中删除
                port = unused_ports.pop(0)
                updateDictNew["port"] = port
                
                update_data_log(taskname=taskname, username=username, updateDict=updateDictNew)
                configTask = get_config_task(taskname=taskname, username=username)
                loggerMain.info(f'【{taskname}】任务配置：{configTask}')

                # 创建进程
                p = multiprocessing.Process(target=task_worker, args=(taskname, username, configTask["password"], port))
                # 启动进程
                p.start()
                # 将进程加入到进程列表中
                processes[port] = p
            
        time.sleep(20)

if __name__ == '__main__':
    loggerMain.info(f'欢迎使用【{config["projectName"]}】项目，当前版本：【{config["version"]}】')
    main()
