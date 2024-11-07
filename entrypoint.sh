#!/bin/sh

# 执行 init.sh 脚本
./init.sh

# 启动 WEB 应用
exec python app.py

# 启动 Python 应用
exec python main.py