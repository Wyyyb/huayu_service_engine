#!/bin/bash

# vLLM Server 停止脚本

PORT=9001

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}停止vLLM服务器...${NC}"

# 查找占用端口的进程
PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t 2>/dev/null)

if [ -z "$PID" ]; then
    echo -e "${YELLOW}端口 $PORT 没有被占用${NC}"
    exit 0
fi

echo -e "${YELLOW}找到进程 PID: $PID${NC}"

# 尝试优雅停止
echo -e "${GREEN}尝试优雅停止进程...${NC}"
kill $PID

# 等待进程停止
sleep 3

# 检查进程是否还在运行
if kill -0 $PID 2>/dev/null; then
    echo -e "${YELLOW}进程仍在运行，强制终止...${NC}"
    kill -9 $PID
    sleep 1
fi

# 最终检查
if kill -0 $PID 2>/dev/null; then
    echo -e "${RED}无法停止进程 PID: $PID${NC}"
    exit 1
else
    echo -e "${GREEN}vLLM服务器已停止${NC}"
fi 