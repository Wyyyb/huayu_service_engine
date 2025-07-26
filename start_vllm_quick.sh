#!/bin/bash

# vLLM Server 快速启动脚本
# 简化版本，用于快速启动

set -e

# 配置参数
MODEL_NAME="Qwen/Qwen2.5-7B-Instruct"
PORT=9001
HOST="0.0.0.0"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}启动vLLM服务器...${NC}"
echo "模型: $MODEL_NAME"
echo "端口: $PORT"
echo ""

# 检查GPU
if ! command -v nvidia-smi &> /dev/null; then
    echo -e "${RED}错误: nvidia-smi 未找到${NC}"
    exit 1
fi

# 检查vllm
if ! command -v vllm &> /dev/null; then
    echo -e "${RED}错误: vllm 未安装${NC}"
    exit 1
fi

# 检查端口
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}警告: 端口 $PORT 已被占用${NC}"
    read -p "是否终止占用进程? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t)
        kill -9 $PID
        sleep 2
    else
        exit 1
    fi
fi

# 启动服务器
echo -e "${GREEN}正在启动vLLM服务器...${NC}"
echo "按 Ctrl+C 停止服务器"
echo ""

vllm serve $MODEL_NAME \
    --host $HOST \
    --port $PORT \
    --gpu-memory-utilization 0.9 \
    --max-model-len 8192 \
    --trust-remote-code 