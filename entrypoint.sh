#!/bin/sh

# 执行 init.sh 脚本
./init.sh

# 启动 WEB 应用
echo "启动web服务: http://127.0.0.1:5000"
exec nohup python app.py > nohup.out 2>&1 &

# 启动 Python 应用
exec python main.py