# API 接口文档

## 基础信息

- **服务地址**: `http://localhost:8888`
- **内容类型**: `application/json`
- **字符编码**: `UTF-8`

## 通用响应格式

### 成功响应
```json
{
    "success": true,
    "timestamp": "2024-01-01T12:00:00.000000",
    "data": {
        // 具体数据
    }
}
```

### 错误响应
```json
{
    "success": false,
    "timestamp": "2024-01-01T12:00:00.000000",
    "error": "错误描述"
}
```

## 1. 文本服务接口

### 接口地址
`POST /api/text`

### 返回格式说明

不同服务的返回数据格式有所不同：

- **列表格式服务**：`bidding_product`（招标公告产品）、`winning_product`（中标公告产品）、`contact_info`（联系人信息）
  - 返回数组，包含多个产品项或联系人项
  - 适用于一个公告中可能包含多个产品或联系人的情况

- **字典格式服务**：`code_extraction`（编号提取）、`district_time`（地区时间）、`notice_type`（公告类型）、`bid_type`（采购类型）
  - 返回单个对象，包含各种字段信息
  - 适用于提取单一维度的结构化信息

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| service_type | string | 是 | 服务类型 |
| notice_id | string | 是 | 公告ID |
| content | string | 是 | 文本内容 |
| extra_info | object | 否 | 额外信息字典 |

### 支持的服务类型

| service_type | 服务名称 | 说明 | 返回格式 |
|--------------|----------|------|----------|
| bidding_product | 招标公告产品服务 | 处理招标公告产品信息 | 列表 |
| winning_product | 中标公告产品服务 | 处理中标公告产品信息 | 列表 |
| code_extraction | 编号提取服务 | 提取各种编号信息 | 字典 |
| district_time | 地区时间提取服务 | 提取地区和时间信息 | 字典 |
| notice_type | 公告类型分类 | 分类公告类型 | 字典 |
| bid_type | 采购类型分类 | 分类采购类型 | 字典 |
| contact_info | 联系人信息解析 | 解析联系人信息 | 列表 |

### 请求示例

#### 招标公告产品服务
```bash
curl -X POST http://localhost:8888/api/text \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "bidding_product",
    "notice_id": "BID001",
    "content": "某公司招标公告内容...",
    "extra_info": {
      "source": "政府采购网",
      "priority": "high"
    }
  }'
```

#### 编号提取服务
```bash
curl -X POST http://localhost:8888/api/text \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "code_extraction",
    "notice_id": "ID001",
    "content": "项目编号：PRJ2024001，招标编号：TDR2024001...",
    "extra_info": {}
  }'
```

### 响应示例

#### 招标公告产品服务响应（列表格式）
```json
{
    "success": true,
    "timestamp": "2024-01-01T12:00:00.000000",
    "data": {
        "notice_id": "BID001",
        "service_type": "bidding_product",
        "processed_content": "某公司招标公告内容...",
        "bidding_products": [
            {
                "招标单位": "宜城市人民医院",
                "产品": "胰岛素泵",
                "数量": "四台",
                "预算单价": "30000.00元",
                "预算金额": "120000元",
                "最高限价": "120000元"
            }
        ]
    }
}
```

#### 中标公告产品服务响应（列表格式）
```json
{
    "success": true,
    "timestamp": "2024-01-01T12:00:00.000000",
    "data": {
        "notice_id": "WIN001",
        "service_type": "winning_product",
        "processed_content": "中标公告内容...",
        "winning_products": [
            {
                "中标单位": "襄阳智立医疗器械维修有限公司",
                "产品名称": "胰岛素泵",
                "标的名称": "无",
                "标项名称": "无",
                "产品品牌": "迈世通",
                "产品型号": "mti-piii",
                "生产厂家": "无",
                "产品数量": "四台",
                "产品单价": "29600.00元",
                "中标金额": "118400元",
                "品目名称": "无",
                "招标单位": "宜城市人民医院",
                "招标金额": "无",
                "预算金额": "无"
            }
        ]
    }
}
```

#### 编号提取服务响应（字典格式）
```json
{
    "success": true,
    "timestamp": "2024-01-01T12:00:00.000000",
    "data": {
        "notice_id": "ID001",
        "service_type": "code_extraction",
        "processed_content": "项目编号：PRJ2024001...",
        "codes": {
            "项目编号": "yc23460020(cgp)",
            "招标编号": "yc23460020(cgp)",
            "合同编号": "无",
            "采购编号": "无",
            "采购计划编号": "无",
            "意向编号": "无",
            "包号": "无",
            "标段号": "无",
            "订单号": "无",
            "流水号": "无"
        }
    }
}
```

#### 联系人信息解析响应（列表格式）
```json
{
    "success": true,
    "timestamp": "2024-01-01T12:00:00.000000",
    "data": {
        "notice_id": "CON001",
        "service_type": "contact_info",
        "processed_content": "联系人信息内容...",
        "contacts": [
            {
                "所属企业名称": "宜城市人民医院",
                "联系人名字": "廖主任",
                "联系电话": "0710-4268367",
                "账号类型": "无"
            },
            {
                "所属企业名称": "亿诚建设项目管理有限公司",
                "联系人名字": "李工",
                "联系电话": "15671329168",
                "账号类型": "无"
            }
        ]
    }
}
```

## 2. 多模态服务接口

### 接口地址
`POST /api/multimodal`

### 支持的文件类型

- **PDF文件**: `.pdf`
- **图片文件**: `.png`, `.jpg`, `.jpeg`

### 请求方式

#### 方式一：文件上传 (multipart/form-data)

```bash
curl -X POST http://localhost:8888/api/multimodal \
  -F "notice_id=DOC001" \
  -F "extra_info={\"source\":\"upload\"}" \
  -F "file=@document.pdf"
```

#### 方式二：JSON请求 (application/json)

```bash
curl -X POST http://localhost:8888/api/multimodal \
  -H "Content-Type: application/json" \
  -d '{
    "notice_id": "DOC001",
    "file_type": "pdf",
    "file_data": "JVBERi0xLjQKJcOkw7zDtsO...",
    "extra_info": {
      "source": "api"
    }
  }'
```

### 请求参数

#### 文件上传方式
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| notice_id | string | 是 | 公告ID |
| extra_info | string | 否 | 额外信息JSON字符串 |
| file | file | 是 | 上传的文件 |

#### JSON方式
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| notice_id | string | 是 | 公告ID |
| file_type | string | 是 | 文件类型 (pdf/images) |
| file_data | string | 是 | base64编码的文件数据 |
| file_data_list | array | 是 | base64编码的图片数据列表 |
| extra_info | object | 否 | 额外信息字典 |

### 响应示例

#### PDF处理响应
```json
{
    "success": true,
    "timestamp": "2024-01-01T12:00:00.000000",
    "data": {
        "notice_id": "DOC001",
        "service_type": "multimodal_pdf",
        "file_type": "pdf",
        "extracted_text": "待实现 - PDF文本提取",
        "page_count": "待实现",
        "file_size": 1024000
    }
}
```

#### 图片处理响应
```json
{
    "success": true,
    "timestamp": "2024-01-01T12:00:00.000000",
    "data": {
        "notice_id": "DOC001",
        "service_type": "multimodal_images",
        "file_type": "images",
        "image_count": 2,
        "extracted_texts": [
            "待实现 - 图片1的OCR文本提取",
            "待实现 - 图片2的OCR文本提取"
        ],
        "combined_text": "待实现 - 图片1的OCR文本提取 待实现 - 图片2的OCR文本提取"
    }
}
```

## 3. 健康检查接口

### 接口地址
`GET /health`

### 请求示例
```bash
curl http://localhost:8888/health
```

### 响应示例
```json
{
    "status": "healthy",
    "service": "huayu_service_engine",
    "version": "1.0.0"
}
```

## 错误码说明

| HTTP状态码 | 说明 |
|------------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 500 | 服务器内部错误 |

### 常见错误

#### 缺少必需参数
```json
{
    "success": false,
    "error": "Missing required field: service_type"
}
```

#### 不支持的服务类型
```json
{
    "success": false,
    "error": "Unsupported service type: unknown_service"
}
```

#### 文件格式错误
```json
{
    "success": false,
    "error": "No supported files found"
}
```

## 使用示例

### Python客户端示例

```python
import requests
import json

# 文本服务调用
def call_text_service(service_type, notice_id, content, extra_info=None):
    url = "http://localhost:8888/api/text"
    data = {
        "service_type": service_type,
        "notice_id": notice_id,
        "content": content,
        "extra_info": extra_info or {}
    }
    
    response = requests.post(url, json=data)
    return response.json()

# 多模态服务调用
def call_multimodal_service(notice_id, file_path, extra_info=None):
    url = "http://localhost:8888/api/multimodal"
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'notice_id': notice_id,
            'extra_info': json.dumps(extra_info or {})
        }
        
        response = requests.post(url, files=files, data=data)
        return response.json()

# 使用示例
if __name__ == "__main__":
    # 调用招标公告服务
    result = call_text_service(
        "bidding_notice",
        "BID001",
        "某公司招标公告内容...",
        {"source": "test"}
    )
    print(result)
    
    # 调用多模态服务
    result = call_multimodal_service(
        "DOC001",
        "document.pdf",
        {"source": "test"}
    )
    print(result)
```

### JavaScript客户端示例

```javascript
// 文本服务调用
async function callTextService(serviceType, noticeId, content, extraInfo = {}) {
    const response = await fetch('http://localhost:8888/api/text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            service_type: serviceType,
            notice_id: noticeId,
            content: content,
            extra_info: extraInfo
        })
    });
    
    return await response.json();
}

// 多模态服务调用
async function callMultimodalService(noticeId, file, extraInfo = {}) {
    const formData = new FormData();
    formData.append('notice_id', noticeId);
    formData.append('file', file);
    formData.append('extra_info', JSON.stringify(extraInfo));
    
    const response = await fetch('http://localhost:8888/api/multimodal', {
        method: 'POST',
        body: formData
    });
    
    return await response.json();
}

// 使用示例
callTextService('bidding_notice', 'BID001', '招标公告内容...', {source: 'test'})
    .then(result => console.log(result))
    .catch(error => console.error(error));
```

## 注意事项

1. **文件大小限制**: 单个文件最大100MB
2. **并发处理**: 支持多并发请求处理
3. **字符编码**: 所有文本内容使用UTF-8编码
4. **超时设置**: 建议客户端设置适当的超时时间
5. **错误处理**: 建议客户端实现完善的错误处理机制 