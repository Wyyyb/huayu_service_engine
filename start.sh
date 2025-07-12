#!/bin/bash

# 华语服务引擎启动脚本

echo "启动华语服务引擎..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查依赖是否安装
echo "检查依赖..."
if ! python3 -c "import tornado" 2>/dev/null; then
    echo "安装依赖包..."
    pip3 install -r requirements.txt
fi

# 启动服务
echo "启动服务..."
python3 run.py 