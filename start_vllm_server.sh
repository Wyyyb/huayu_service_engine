#!/bin/bash

# vLLM Server 启动脚本
# 支持自动选择可用的GPU (cuda:0 或 cuda:1)

set -e  # 遇到错误立即退出

# 配置参数
MODEL_NAME="Qwen/Qwen3-8B"  # 模型名称
PORT=9001                              # 服务端口
HOST="0.0.0.0"                         # 监听地址
MAX_MODEL_LEN=8192                     # 最大模型长度
GPU_MEMORY_UTILIZATION=0.9             # GPU内存利用率
SWAP_SPACE=4                           # 交换空间大小(GB)
TENSOR_PARALLEL_SIZE=1                 # 张量并行大小

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 命令未找到，请先安装 $1"
        exit 1
    fi
}

# 检查GPU状态
check_gpu() {
    log_info "检查GPU状态..."
    
    if ! command -v nvidia-smi &> /dev/null; then
        log_error "nvidia-smi 命令未找到，请确保已安装NVIDIA驱动"
        exit 1
    fi
    
    # 获取GPU信息
    GPU_COUNT=$(nvidia-smi --list-gpus | wc -l)
    log_info "检测到 $GPU_COUNT 个GPU"
    
    if [ $GPU_COUNT -eq 0 ]; then
        log_error "未检测到可用的GPU"
        exit 1
    fi
    
    # 显示GPU详细信息
    log_info "GPU详细信息:"
    nvidia-smi --query-gpu=index,name,memory.total,memory.free,memory.used --format=csv,noheader,nounits | while IFS=, read -r index name total free used; do
        log_info "GPU $index: $name, 总内存: ${total}MB, 已用: ${used}MB, 可用: ${free}MB"
    done
}

# 选择最佳GPU
select_gpu() {
    log_info "选择最佳GPU..."
    
    # 检查GPU 0
    GPU0_FREE=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i 0)
    GPU0_TOTAL=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits -i 0)
    GPU0_USAGE=$(echo "scale=1; $GPU0_FREE * 100 / $GPU0_TOTAL" | bc)
    
    # 检查GPU 1 (如果存在)
    if [ $GPU_COUNT -gt 1 ]; then
        GPU1_FREE=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i 1)
        GPU1_TOTAL=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits -i 1)
        GPU1_USAGE=$(echo "scale=1; $GPU1_FREE * 100 / $GPU1_TOTAL" | bc)
        
        log_info "GPU 0 可用内存: ${GPU0_FREE}MB (${GPU0_USAGE}%)"
        log_info "GPU 1 可用内存: ${GPU1_FREE}MB (${GPU1_USAGE}%)"
        
        # 选择可用内存更多的GPU
        if (( $(echo "$GPU1_FREE > $GPU0_FREE" | bc -l) )); then
            SELECTED_GPU=1
            log_success "选择 GPU 1 (可用内存更多)"
        else
            SELECTED_GPU=0
            log_success "选择 GPU 0 (可用内存更多)"
        fi
    else
        SELECTED_GPU=0
        log_info "GPU 0 可用内存: ${GPU0_FREE}MB (${GPU0_USAGE}%)"
        log_success "选择 GPU 0 (唯一可用GPU)"
    fi
    
    # 检查可用内存是否足够
    MIN_MEMORY=8000  # 最小需要8GB
    if [ $GPU0_FREE -lt $MIN_MEMORY ] && [ $GPU_COUNT -gt 1 ] && [ $GPU1_FREE -lt $MIN_MEMORY ]; then
        log_warning "所有GPU可用内存都不足${MIN_MEMORY}MB，可能影响模型加载"
    fi
}

# 检查端口是否被占用
check_port() {
    log_info "检查端口 $PORT 是否被占用..."
    
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_warning "端口 $PORT 已被占用"
        read -p "是否要终止占用端口的进程? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t)
            log_info "终止进程 PID: $PID"
            kill -9 $PID
            sleep 2
        else
            log_error "端口被占用，无法启动服务"
            exit 1
        fi
    else
        log_success "端口 $PORT 可用"
    fi
}

# 检查模型是否已下载
check_model() {
    log_info "检查模型 $MODEL_NAME 是否已下载..."
    
    # 检查Hugging Face缓存目录
    HF_HOME=${HF_HOME:-$HOME/.cache/huggingface}
    MODEL_PATH="$HF_HOME/hub/models--$(echo $MODEL_NAME | sed 's/\//--/g')"
    
    if [ -d "$MODEL_PATH" ]; then
        log_success "模型已存在于本地缓存: $MODEL_PATH"
    else
        log_warning "模型未下载，首次启动将自动下载模型"
        log_info "模型大小约 14GB，下载可能需要较长时间"
    fi
}

# 启动vLLM服务器
start_server() {
    log_info "启动vLLM服务器..."
    log_info "模型: $MODEL_NAME"
    log_info "GPU: cuda:$SELECTED_GPU"
    log_info "端口: $PORT"
    log_info "主机: $HOST"
    
    # 构建启动命令
    CMD="vllm serve $MODEL_NAME \
        --host $HOST \
        --port $PORT \
        --tensor-parallel-size $TENSOR_PARALLEL_SIZE \
        --gpu-memory-utilization $GPU_MEMORY_UTILIZATION \
        --max-model-len $MAX_MODEL_LEN \
        --swap-space $SWAP_SPACE \
        --trust-remote-code"
    
    log_info "启动命令: $CMD"
    echo
    
    # 启动服务器
    log_success "正在启动vLLM服务器..."
    log_info "服务器启动后，可以通过以下方式测试:"
    log_info "  curl http://localhost:$PORT/v1/models"
    log_info "  python -c \"import requests; print(requests.get('http://localhost:$PORT/v1/models').json())\""
    echo
    
    # 执行启动命令
    exec $CMD
}

# 主函数
main() {
    echo "=========================================="
    echo "           vLLM Server 启动脚本"
    echo "=========================================="
    echo
    
    # 检查必要命令
    check_command "nvidia-smi"
    check_command "vllm"
    check_command "bc"
    check_command "lsof"
    
    # 检查GPU
    check_gpu
    
    # 选择GPU
    select_gpu
    
    # 检查端口
    check_port
    
    # 检查模型
    check_model
    
    echo
    log_info "准备启动vLLM服务器..."
    log_info "按 Ctrl+C 可以停止服务器"
    echo
    
    # 启动服务器
    start_server
}

# 信号处理
trap 'echo; log_warning "收到中断信号，正在停止服务器..."; exit 0' INT TERM

# 运行主函数
main "$@" 