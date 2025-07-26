# vLLM Server 启动脚本使用说明

## 概述

本项目提供了三个脚本来管理vLLM服务器：

1. **`start_vllm_server.sh`** - 完整功能启动脚本（推荐）
2. **`start_vllm_quick.sh`** - 快速启动脚本
3. **`stop_vllm_server.sh`** - 停止服务器脚本

## 脚本功能对比

| 功能 | start_vllm_server.sh | start_vllm_quick.sh |
|------|---------------------|-------------------|
| GPU自动选择 | ✅ | ❌ |
| GPU内存检查 | ✅ | ❌ |
| 端口冲突处理 | ✅ | ✅ |
| 模型下载检查 | ✅ | ❌ |
| 详细日志输出 | ✅ | ❌ |
| 错误处理 | ✅ | 基础 |
| 启动速度 | 较慢 | 快速 |

## 使用方法

### 1. 完整功能启动（推荐）

```bash
# 启动vLLM服务器（自动选择最佳GPU）
./start_vllm_server.sh
```

**功能特性：**
- 自动检测GPU数量和内存状态
- 智能选择可用内存最多的GPU
- 检查端口冲突并提供解决方案
- 检查模型是否已下载
- 详细的启动日志和错误处理

**输出示例：**
```
==========================================
           vLLM Server 启动脚本
==========================================

[INFO] 检查GPU状态...
[INFO] 检测到 2 个GPU
[INFO] GPU详细信息:
[INFO] GPU 0: NVIDIA GeForce RTX 4090, 总内存: 24576MB, 已用: 2048MB, 可用: 22528MB
[INFO] GPU 1: NVIDIA GeForce RTX 4090, 总内存: 24576MB, 已用: 1024MB, 可用: 23552MB
[INFO] 选择最佳GPU...
[INFO] GPU 0 可用内存: 22528MB (91.7%)
[INFO] GPU 1 可用内存: 23552MB (95.8%)
[SUCCESS] 选择 GPU 1 (可用内存更多)
[INFO] 检查端口 9001 是否被占用...
[SUCCESS] 端口 9001 可用
[INFO] 检查模型 Qwen/Qwen2.5-7B-Instruct 是否已下载...
[SUCCESS] 模型已存在于本地缓存: /home/user/.cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct
```

### 2. 快速启动

```bash
# 快速启动vLLM服务器
./start_vllm_quick.sh
```

**适用场景：**
- 开发测试环境
- 已知GPU配置
- 需要快速启动

### 3. 停止服务器

```bash
# 停止vLLM服务器
./stop_vllm_server.sh
```

## 配置参数

### 默认配置

```bash
MODEL_NAME="Qwen/Qwen3-8B"  # 模型名称
PORT=9001                              # 服务端口
HOST="0.0.0.0"                         # 监听地址
MAX_MODEL_LEN=8192                     # 最大模型长度
GPU_MEMORY_UTILIZATION=0.9             # GPU内存利用率
SWAP_SPACE=4                           # 交换空间大小(GB)
TENSOR_PARALLEL_SIZE=1                 # 张量并行大小
```

### 自定义配置

如需修改配置，可以编辑脚本中的参数：

```bash
# 编辑启动脚本
vim start_vllm_server.sh

# 修改配置参数
MODEL_NAME="Qwen/Qwen2.5-14B-Instruct"  # 更换模型
PORT=9002                               # 更换端口
GPU_MEMORY_UTILIZATION=0.8              # 调整内存利用率
```

## 前置条件

### 1. 系统要求

- **操作系统**: Linux (Ubuntu 18.04+)
- **Python**: 3.8+
- **CUDA**: 11.8+
- **GPU**: NVIDIA GPU with 8GB+ VRAM

### 2. 软件安装

```bash
# 安装NVIDIA驱动
sudo apt update
sudo apt install nvidia-driver-535

# 安装CUDA Toolkit
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run

# 安装vLLM
pip install vllm

# 安装其他依赖
sudo apt install bc lsof
```

### 3. 环境变量

```bash
# 添加到 ~/.bashrc
export CUDA_HOME=/usr/local/cuda
export PATH=$PATH:$CUDA_HOME/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CUDA_HOME/lib64
```

## 测试服务器

### 1. 健康检查

```bash
# 检查服务器状态
curl http://localhost:9001/v1/models

# 使用Python测试
python -c "
import requests
response = requests.get('http://localhost:9001/v1/models')
print(response.json())
"
```

### 2. 简单推理测试

```bash
# 使用curl测试
curl -X POST http://localhost:9001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 100
  }'
```

### 3. Python客户端测试

```python
import requests

def test_vllm_server():
    url = "http://localhost:9001/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [{"role": "user", "content": "你好，请介绍一下自己"}],
        "max_tokens": 200,
        "temperature": 0.7
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print("回复:", result['choices'][0]['message']['content'])
    else:
        print("错误:", response.text)

if __name__ == "__main__":
    test_vllm_server()
```

## 故障排除

### 1. GPU相关问题

**问题**: `nvidia-smi` 命令未找到
```bash
# 解决方案
sudo apt update
sudo apt install nvidia-utils-535
```

**问题**: GPU内存不足
```bash
# 解决方案：调整内存利用率
GPU_MEMORY_UTILIZATION=0.7  # 降低到70%
```

**问题**: CUDA版本不兼容
```bash
# 解决方案：检查CUDA版本
nvcc --version
# 确保vLLM与CUDA版本兼容
pip install vllm --force-reinstall
```

### 2. 端口相关问题

**问题**: 端口被占用
```bash
# 查看占用进程
lsof -i :9001

# 手动终止进程
kill -9 <PID>
```

**问题**: 权限不足
```bash
# 解决方案
sudo chmod +x start_vllm_server.sh
```

### 3. 模型相关问题

**问题**: 模型下载失败
```bash
# 手动下载模型
huggingface-cli download Qwen/Qwen2.5-7B-Instruct

# 或使用git
git lfs install
git clone https://huggingface.co/Qwen/Qwen2.5-7B-Instruct
```

**问题**: 模型加载缓慢
```bash
# 解决方案：使用更快的存储
# 将模型放在SSD上
export HF_HOME=/path/to/ssd/huggingface
```

### 4. 网络相关问题

**问题**: 无法从外部访问
```bash
# 检查防火墙设置
sudo ufw status
sudo ufw allow 9001

# 检查绑定地址
HOST="0.0.0.0"  # 确保绑定到所有接口
```

## 性能优化

### 1. GPU优化

```bash
# 调整GPU内存利用率
GPU_MEMORY_UTILIZATION=0.95  # 提高利用率

# 使用张量并行（多GPU）
TENSOR_PARALLEL_SIZE=2  # 使用2个GPU
```

### 2. 模型优化

```bash
# 使用量化模型
MODEL_NAME="Qwen/Qwen2.5-7B-Instruct-AWQ"

# 调整最大长度
MAX_MODEL_LEN=4096  # 减少内存使用
```

### 3. 系统优化

```bash
# 增加交换空间
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 优化GPU设置
nvidia-smi -pm 1  # 启用持久模式
nvidia-smi -ac 1215,1410  # 设置时钟频率
```

## 监控和维护

### 1. 资源监控

```bash
# 监控GPU使用情况
watch -n 1 nvidia-smi

# 监控进程
ps aux | grep vllm

# 监控端口
netstat -tlnp | grep 9001
```

### 2. 日志管理

```bash
# 查看vLLM日志
tail -f /var/log/vllm.log

# 启动时重定向日志
./start_vllm_server.sh > vllm.log 2>&1 &
```

### 3. 自动重启

```bash
# 创建systemd服务
sudo vim /etc/systemd/system/vllm.service

[Unit]
Description=vLLM Server
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/project
ExecStart=/path/to/project/start_vllm_server.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# 启用服务
sudo systemctl enable vllm
sudo systemctl start vllm
```

## 常见问题

### Q: 如何更换模型？
A: 修改脚本中的 `MODEL_NAME` 参数，例如：
```bash
MODEL_NAME="Qwen/Qwen2.5-14B-Instruct"
```

### Q: 如何调整GPU内存使用？
A: 修改 `GPU_MEMORY_UTILIZATION` 参数：
```bash
GPU_MEMORY_UTILIZATION=0.8  # 使用80%的GPU内存
```

### Q: 如何支持多GPU？
A: 修改 `TENSOR_PARALLEL_SIZE` 参数：
```bash
TENSOR_PARALLEL_SIZE=2  # 使用2个GPU
```

### Q: 如何更改服务端口？
A: 修改 `PORT` 参数：
```bash
PORT=9002  # 使用9002端口
```

### Q: 如何后台运行？
A: 使用nohup或screen：
```bash
nohup ./start_vllm_server.sh > vllm.log 2>&1 &
# 或
screen -S vllm
./start_vllm_server.sh
# Ctrl+A+D 分离screen
``` 