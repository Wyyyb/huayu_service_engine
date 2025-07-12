# 华语服务引擎 (Huayu Service Engine)

基于Tornado的多服务文本处理引擎，提供多种文本分析和多模态处理服务。

## 项目结构

```
huayu_service_engine/
├── app.py                 # 主应用文件
├── run.py                 # 启动脚本
├── config.py              # 配置文件
├── requirements.txt       # 依赖包
├── README.md             # 项目说明
├── API_DOCUMENTATION.md  # API接口文档
├── services/             # 服务模块
│   ├── __init__.py
│   ├── base_service.py   # 基础服务类
│   ├── text_services.py  # 文本服务实现
│   └── multimodal_service.py # 多模态服务
└── handlers/             # 请求处理器
    ├── __init__.py
    └── service_handler.py
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动服务

### 方式一：使用启动脚本
```bash
python run.py
```

### 方式二：直接运行应用
```bash
python app.py
```

### 方式三：指定端口和主机
```bash
python app.py --port=8888 --host=0.0.0.0 --debug=true
```

## 服务类型

### 文本服务
1. **招标公告产品服务** (bidding_product) - 返回列表格式
2. **中标公告产品服务** (winning_product) - 返回列表格式
3. **编号提取服务** (code_extraction) - 返回字典格式
4. **地区时间提取服务** (district_time) - 返回字典格式
5. **公告类型分类** (notice_type) - 返回字典格式
6. **采购类型分类** (bid_type) - 返回字典格式
7. **联系人信息解析** (contact_info) - 返回列表格式

### 多模态服务
- **PDF文本提取** (multimodal_pdf)
- **图片OCR文本提取** (multimodal_images)

## 配置说明

在 `config.py` 中可以修改以下配置：

- `port`: 服务端口 (默认: 8888)
- `host`: 服务主机 (默认: 0.0.0.0)
- `debug`: 调试模式 (默认: True)
- `max_buffer_size`: 最大缓冲区大小 (默认: 100MB)
- `max_body_size`: 最大请求体大小 (默认: 100MB)

## 开发说明

### 添加新的文本服务

1. 在 `services/text_services.py` 中创建新的服务类
2. 继承 `BaseService` 类
3. 实现 `process` 方法
4. 在 `TextServiceHandler` 中注册新服务

### 扩展多模态服务

1. 在 `services/multimodal_service.py` 中添加新的处理方法
2. 在 `MultimodalServiceHandler` 中添加相应的处理逻辑

## 日志

服务运行时会输出详细的日志信息，包括：
- 请求处理日志
- 错误日志
- 服务启动信息

## 健康检查

访问 `GET /health` 可以检查服务状态。

## 远程测试

项目提供了专门的远程测试脚本，用于测试部署在测试机上的服务：

### 快速测试
```bash
python quick_test.py
```

### 完整测试
```bash
# 测试远程服务（默认）
python test_remote_services.py

# 测试本地服务
python test_remote_services.py --local

# 测试自定义地址
python test_remote_services.py http://your-server:8888
```

详细使用说明请参考 `REMOTE_TEST_README.md`。

## 许可证

MIT License 