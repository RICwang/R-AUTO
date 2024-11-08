#!/bin/sh

# 执行 init.sh 脚本
./init.sh

# 启动 WEB 应用
exec nohup python app.py > nohup.out 2>&1 &

# 启动 Python 应用
exec python main.py