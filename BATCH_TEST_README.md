# 批量测试脚本使用说明

## 概述

`batch_test_0725.py` 是一个批量测试脚本，用于处理测试数据并调用所有文本服务，将结果保存为JSON文件。

## 功能特性

- ✅ **批量处理** - 自动处理指定目录下的所有txt文件
- ✅ **全服务调用** - 对每个文件调用所有7种文本服务
- ✅ **结果保存** - 为每个文件生成对应的JSON结果文件
- ✅ **性能统计** - 记录每个服务的处理时间和成功率
- ✅ **汇总报告** - 生成批量处理的汇总统计报告
- ✅ **错误处理** - 完善的异常处理和日志记录

## 使用方法

### 1. 基本使用

```bash
# 使用默认参数
python batch_test_0725.py

# 指定输入和输出目录
python batch_test_0725.py --input tests/test_data/text_data_0610 --output tests/test_result/batch_test_0725

# 使用短参数
python batch_test_0725.py -i tests/test_data/text_data_0610 -o tests/test_result/batch_test_0725
```

### 2. 参数说明

| 参数 | 短参数 | 默认值 | 说明 |
|------|--------|--------|------|
| --input | -i | tests/test_data/text_data_0610 | 输入文件夹路径 |
| --output | -o | tests/test_result/batch_test_0725 | 输出文件夹路径 |

### 3. 测试的服务

脚本会自动调用以下7种文本服务：

1. **招标公告产品服务** (bidding_product)
2. **中标公告产品服务** (winning_product)
3. **编号提取服务** (code_extraction)
4. **地区时间提取服务** (district_time)
5. **公告类型分类** (notice_type)
6. **采购类型分类** (bid_type)
7. **联系人信息解析** (contact_info)

## 输出文件结构

### 1. 单个文件结果

每个测试文件会生成一个对应的JSON结果文件，命名格式：`{notice_id}_results.json`

```json
{
  "notice_id": "test_15",
  "filename": "test_15.txt",
  "file_path": "tests/test_data/text_data_0610/test_15.txt",
  "content_length": 1234,
  "process_time": "2024-07-25T10:30:00",
  "total_duration": 15.23,
  "services": {
    "bidding_product": {
      "service_name": "招标公告产品服务",
      "success": true,
      "duration": 2.1,
      "result": {
        "notice_id": "test_15",
        "service_type": "bidding_product",
        "bidding_products": [...]
      },
      "error": null
    },
    "winning_product": {
      "service_name": "中标公告产品服务",
      "success": true,
      "duration": 2.3,
      "result": {
        "notice_id": "test_15",
        "service_type": "winning_product",
        "winning_products": [...]
      },
      "error": null
    }
    // ... 其他服务结果
  }
}
```

### 2. 汇总报告

生成 `batch_test_summary.json` 汇总报告：

```json
{
  "batch_test_info": {
    "input_directory": "tests/test_data/text_data_0610",
    "output_directory": "tests/test_result/batch_test_0725",
    "start_time": "2024-07-25T10:30:00",
    "total_files": 8,
    "success_count": 7,
    "error_count": 1,
    "success_rate": "87.5%"
  }
}
```

## 运行示例

```bash
$ python batch_test_0725.py

2024-07-25 10:30:00 - __main__ - INFO - 开始批量处理
2024-07-25 10:30:00 - __main__ - INFO - 输入目录: tests/test_data/text_data_0610
2024-07-25 10:30:00 - __main__ - INFO - 输出目录: tests/test_result/batch_test_0725
2024-07-25 10:30:00 - __main__ - INFO - 找到 8 个文本文件
2024-07-25 10:30:00 - __main__ - INFO - 处理进度: 1/8
2024-07-25 10:30:00 - __main__ - INFO - 处理文件: tests/test_data/text_data_0610/test_15.txt
2024-07-25 10:30:00 - __main__ - INFO - 调用服务: 招标公告产品服务
2024-07-25 10:30:02 - __main__ - INFO - ✅ 招标公告产品服务 成功 (2.10s)
2024-07-25 10:30:00 - __main__ - INFO - 调用服务: 中标公告产品服务
2024-07-25 10:30:02 - __main__ - INFO - ✅ 中标公告产品服务 成功 (2.30s)
...
2024-07-25 10:30:15 - __main__ - INFO - 文件处理完成: tests/test_data/text_data_0610/test_15.txt (总耗时: 15.23s)
2024-07-25 10:30:15 - __main__ - INFO - 结果已保存: tests/test_result/batch_test_0725/test_15_results.json
...
2024-07-25 10:35:00 - __main__ - INFO - 批量处理完成!
2024-07-25 10:35:00 - __main__ - INFO - 总文件数: 8
2024-07-25 10:35:00 - __main__ - INFO - 成功处理: 7
2024-07-25 10:35:00 - __main__ - INFO - 处理失败: 1
2024-07-25 10:35:00 - __main__ - INFO - 成功率: 87.5%
2024-07-25 10:35:00 - __main__ - INFO - 汇总报告: tests/test_result/batch_test_0725/batch_test_summary.json
```

## 注意事项

### 1. 前置条件

- 确保vllm server已启动并运行在 `http://localhost:9001`
- 确保所有依赖包已安装
- 确保输入目录存在且包含txt文件

### 2. 性能考虑

- 每个文件会调用7个服务，总处理时间可能较长
- 建议先用少量文件测试，确认无误后再批量处理
- 可以通过日志监控处理进度

### 3. 错误处理

- 单个服务失败不会影响其他服务的处理
- 单个文件失败不会影响其他文件的处理
- 所有错误都会记录在日志和结果文件中

### 4. 文件命名

- 公告ID从文件名自动生成
- 支持 `test_15.txt`、`test2.txt` 等格式
- 结果文件命名：`{notice_id}_results.json`

## 故障排除

### 1. vllm server连接失败

```
❌ 招标公告产品服务 失败: 大模型无返回或异常
```

**解决方案：**
- 检查vllm server是否启动
- 确认端口9001是否正确
- 检查网络连接

### 2. 文件读取失败

```
读取文件失败 tests/test_data/text_data_0610/test_15.txt: [Errno 2] No such file or directory
```

**解决方案：**
- 检查输入目录路径是否正确
- 确认文件是否存在
- 检查文件编码是否为UTF-8

### 3. 输出目录权限问题

```
PermissionError: [Errno 13] Permission denied
```

**解决方案：**
- 检查输出目录的写入权限
- 尝试使用不同的输出目录
- 确保磁盘空间充足

## 扩展功能

### 1. 自定义服务配置

可以修改脚本中的服务配置：

```python
self.services = {
    'bidding_product': BiddingProductService(),
    'winning_product': WinningProductService(),
    # 添加或移除服务
}
```

### 2. 并行处理

对于大量文件，可以考虑添加多进程处理：

```python
from multiprocessing import Pool

def process_file_wrapper(args):
    file_path, notice_id = args
    return tester.process_single_file(file_path, notice_id)

with Pool(processes=4) as pool:
    results = pool.map(process_file_wrapper, file_args)
```

### 3. 结果分析

可以基于生成的JSON文件进行进一步分析：

- 服务成功率统计
- 处理时间分析
- 错误类型统计
- 数据质量评估 