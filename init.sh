#!/bin/bash

# 定义目录路径
VOLUME_DIR="./volume"
EXAMPLE_DIR="./example"

# 检查 volume 目录是否存在，不存在则创建
if [ ! -d "$VOLUME_DIR" ]; then
    mkdir -p "$VOLUME_DIR"
    echo "创建目录: $VOLUME_DIR"
fi

# 检查 volume 目录是否为空
if [ -z "$(ls -A "$VOLUME_DIR")" ]; then
    echo "volume 目录为空，开始复制文件..."
    cp -r "$EXAMPLE_DIR"/* "$VOLUME_DIR"/
    echo "文件复制完成。"
