#!/usr/bin/env python3
"""
批量测试脚本 - 使用模拟数据（无需vLLM服务器）
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, List
import argparse

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services import (
    BiddingProductService,
    WinningProductService,
    CodeExtractionService,
    DistrictTimeService,
    NoticeTypeService,
    BidTypeService,
    ContactInfoService
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MockVLLMClient:
    """模拟vLLM客户端，返回预设的响应"""
    
    def __init__(self):
        self.mock_responses = {
            "bidding_product": """| 招标单位 | 产品 | 数量 | 预算单价 | 预算金额 | 最高限价 |
|----------|------|------|----------|----------|----------|
| 测试单位 | 测试产品 | 10台 | 1000元 | 10000元 | 12000元 |""",
            
            "winning_product": """| 招标单位 | 供应商 | 产品 | 品牌 | 型号 | 数量 | 单价 | 中标价格 |
|----------|--------|------|------|------|------|------|----------|
| 测试单位 | 测试供应商 | 测试产品 | 测试品牌 | 测试型号 | 10台 | 900元 | 9000元 |""",
            
            "code_extraction": """{"项目编号": "TEST001", "招标编号": "BID001", "合同编号": "CONTRACT001", "采购编号": "PURCHASE001", "采购计划编号": "PLAN001", "意向编号": "INTENT001", "包号": "PACKAGE001", "标段号": "SECTION001", "订单号": "ORDER001", "流水号": "SERIAL001"}""",
            
            "district_time": """{"采购地区": "北京市", "发布时间": "2024-01-01", "报名截止时间": "2024-01-15", "获取招标文件开始时间": "2024-01-02", "获取招标文件截止时间": "2024-01-10", "递交投标文件开始时间": "2024-01-11", "递交投标文件截止时间": "2024-01-20", "报价截止时间": "2024-01-18", "开标时间": "2024-01-21"}""",
            
            "notice_type": """{"公告类型": "招标公告"}""",
            
            "bid_type": """{"采购类型": "公开招标"}""",
            
            "contact_info": """| 所属企业名称 | 联系人名字 | 联系电话 | 账号类型 |
|--------------|------------|----------|----------|
| 测试企业 | 张三 | 13800138000 | 手机号 |"""
        }
    
    def chat_completion(self, prompt: str, **kwargs) -> str:
        """返回模拟响应"""
        # 根据prompt内容判断服务类型
        if "招标公告" in prompt and "产品" in prompt:
            return self.mock_responses["bidding_product"]
        elif "中标公告" in prompt and "产品" in prompt:
            return self.mock_responses["winning_product"]
        elif "编号" in prompt:
            return self.mock_responses["code_extraction"]
        elif "地区" in prompt and "时间" in prompt:
            return self.mock_responses["district_time"]
        elif "公告类型" in prompt:
            return self.mock_responses["notice_type"]
        elif "采购类型" in prompt:
            return self.mock_responses["bid_type"]
        elif "联系人" in prompt:
            return self.mock_responses["contact_info"]
        else:
            return "模拟响应：无法识别的服务类型"

class MockBatchTester:
    """使用模拟数据的批量测试器"""
    
    def __init__(self):
        # 创建模拟服务
        self.services = {
            'bidding_product': self._create_mock_service("bidding_product", "招标公告产品服务"),
            'winning_product': self._create_mock_service("winning_product", "中标公告产品服务"),
            'code_extraction': self._create_mock_service("code_extraction", "编号提取服务"),
            'district_time': self._create_mock_service("district_time", "地区时间提取服务"),
            'notice_type': self._create_mock_service("notice_type", "公告类型分类"),
            'bid_type': self._create_mock_service("bid_type", "采购类型分类"),
            'contact_info': self._create_mock_service("contact_info", "联系人信息解析")
        }
        
        self.service_names = {
            'bidding_product': '招标公告产品服务',
            'winning_product': '中标公告产品服务',
            'code_extraction': '编号提取服务',
            'district_time': '地区时间提取服务',
            'notice_type': '公告类型分类',
            'bid_type': '采购类型分类',
            'contact_info': '联系人信息解析'
        }
    
    def _create_mock_service(self, service_type: str, service_name: str):
        """创建模拟服务"""
        class MockService:
            def __init__(self, service_type, service_name):
                self.service_type = service_type
                self.service_name = service_name
                self.vllm = MockVLLMClient()
                self.logger = logging.getLogger(f"Mock{service_name}")
            
            def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
                try:
                    # 模拟处理时间
                    time.sleep(0.1)
                    
                    # 生成模拟prompt
                    if "product" in self.service_type:
                        prompt = f"请从下列{'招标' if 'bidding' in self.service_type else '中标'}公告文本中，提取产品信息，结果按markdown表格输出。\n\n{content[:100]}..."
                    elif "code" in self.service_type:
                        prompt = f"请从下列公告文本中，提取编号信息，结果以JSON格式输出。\n\n{content[:100]}..."
                    elif "district" in self.service_type:
                        prompt = f"请从下列公告文本中，提取地区时间信息，结果以JSON格式输出。\n\n{content[:100]}..."
                    elif "notice" in self.service_type:
                        prompt = f"请判断下列公告文本的公告类型，结果以JSON格式输出。\n\n{content[:100]}..."
                    elif "bid" in self.service_type:
                        prompt = f"请判断下列公告文本的采购类型，结果以JSON格式输出。\n\n{content[:100]}..."
                    elif "contact" in self.service_type:
                        prompt = f"请从下列公告文本中，提取联系人信息，结果按markdown表格输出。\n\n{content[:100]}..."
                    else:
                        prompt = f"请处理下列文本。\n\n{content[:100]}..."
                    
                    # 获取模拟响应
                    llm_output = self.vllm.chat_completion(prompt)
                    
                    # 构造返回结果
                    if "product" in self.service_type:
                        result = {
                            'notice_id': notice_id,
                            'service_type': self.service_type,
                            f'{self.service_type}_products': [{'模拟产品': '模拟数据'}]
                        }
                    elif "code" in self.service_type:
                        result = {
                            'notice_id': notice_id,
                            'service_type': self.service_type,
                            'codes': {'模拟编号': '模拟数据'}
                        }
                    elif "district" in self.service_type:
                        result = {
                            'notice_id': notice_id,
                            'service_type': self.service_type,
                            'district_time': {'模拟地区': '模拟数据'}
                        }
                    elif "notice" in self.service_type:
                        result = {
                            'notice_id': notice_id,
                            'service_type': self.service_type,
                            'notice_type': '模拟公告类型'
                        }
                    elif "bid" in self.service_type:
                        result = {
                            'notice_id': notice_id,
                            'service_type': self.service_type,
                            'bid_type': '模拟采购类型'
                        }
                    elif "contact" in self.service_type:
                        result = {
                            'notice_id': notice_id,
                            'service_type': self.service_type,
                            'contact_info': [{'模拟联系人': '模拟数据'}]
                        }
                    else:
                        result = {
                            'notice_id': notice_id,
                            'service_type': self.service_type,
                            'data': '模拟数据'
                        }
                    
                    return {'success': True, 'data': result}
                    
                except Exception as e:
                    self.logger.error(f"{self.service_name}服务异常: {e}")
                    return {'success': False, 'error': str(e)}
        
        return MockService(service_type, service_name)
    
    def read_text_file(self, file_path: str) -> str:
        """读取文本文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            return content
        except Exception as e:
            logger.error(f"读取文件失败 {file_path}: {e}")
            return ""
    
    def get_notice_id_from_filename(self, filename: str) -> str:
        """从文件名生成公告ID"""
        name = os.path.splitext(filename)[0]
        if name.startswith('test_'):
            return name
        elif name.startswith('test'):
            return name
        else:
            return name
    
    def process_single_file(self, file_path: str, notice_id: str) -> Dict[str, Any]:
        """处理单个文件，调用所有文本服务"""
        logger.info(f"处理文件: {file_path}")
        
        # 读取文件内容
        content = self.read_text_file(file_path)
        if not content:
            return {"error": "文件内容为空"}
        
        # 记录开始时间
        start_time = time.time()
        
        # 调用所有服务
        results = {
            "notice_id": notice_id,
            "filename": os.path.basename(file_path),
            "file_path": file_path,
            "content_length": len(content),
            "process_time": datetime.now().isoformat(),
            "services": {}
        }
        
        for service_type, service in self.services.items():
            try:
                logger.info(f"调用服务: {self.service_names[service_type]}")
                service_start_time = time.time()
                
                # 调用服务
                result = service.process(notice_id, content, {"batch_test": True})
                
                service_end_time = time.time()
                service_duration = service_end_time - service_start_time
                
                # 记录服务结果
                results["services"][service_type] = {
                    "service_name": self.service_names[service_type],
                    "success": result.get("success", False),
                    "duration": service_duration,
                    "result": result.get("data", {}),
                    "error": result.get("error") if not result.get("success") else None
                }
                
                if result.get("success"):
                    logger.info(f"✅ {self.service_names[service_type]} 成功 ({service_duration:.2f}s)")
                else:
                    logger.warning(f"❌ {self.service_names[service_type]} 失败: {result.get('error')}")
                    
            except Exception as e:
                logger.error(f"❌ {self.service_names[service_type]} 异常: {e}")
                results["services"][service_type] = {
                    "service_name": self.service_names[service_type],
                    "success": False,
                    "duration": 0,
                    "result": {},
                    "error": str(e)
                }
        
        # 记录总处理时间
        total_duration = time.time() - start_time
        results["total_duration"] = total_duration
        
        logger.info(f"文件处理完成: {file_path} (总耗时: {total_duration:.2f}s)")
        return results
    
    def process_directory(self, input_dir: str, output_dir: str):
        """处理整个目录"""
        logger.info(f"开始批量处理 (模拟模式)")
        logger.info(f"输入目录: {input_dir}")
        logger.info(f"输出目录: {output_dir}")
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取所有txt文件
        txt_files = []
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.txt'):
                    txt_files.append(os.path.join(root, file))
        
        logger.info(f"找到 {len(txt_files)} 个文本文件")
        
        # 处理统计
        total_files = len(txt_files)
        success_count = 0
        error_count = 0
        
        # 批量处理
        for i, file_path in enumerate(txt_files, 1):
            try:
                logger.info(f"处理进度: {i}/{total_files}")
                
                # 生成公告ID
                filename = os.path.basename(file_path)
                notice_id = self.get_notice_id_from_filename(filename)
                
                # 处理文件
                result = self.process_single_file(file_path, notice_id)
                
                # 保存结果
                output_filename = f"{notice_id}_results.json"
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                logger.info(f"结果已保存: {output_path}")
                success_count += 1
                
            except Exception as e:
                logger.error(f"处理文件失败 {file_path}: {e}")
                error_count += 1
        
        # 生成汇总报告
        summary = {
            "batch_test_info": {
                "input_directory": input_dir,
                "output_directory": output_dir,
                "start_time": datetime.now().isoformat(),
                "total_files": total_files,
                "success_count": success_count,
                "error_count": error_count,
                "success_rate": f"{success_count/total_files*100:.1f}%" if total_files > 0 else "0%",
                "mode": "mock"
            }
        }
        
        summary_path = os.path.join(output_dir, "batch_test_summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.info(f"批量处理完成!")
        logger.info(f"总文件数: {total_files}")
        logger.info(f"成功处理: {success_count}")
        logger.info(f"处理失败: {error_count}")
        logger.info(f"成功率: {summary['batch_test_info']['success_rate']}")
        logger.info(f"汇总报告: {summary_path}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='批量测试文本服务 (模拟模式)')
    parser.add_argument('--input', '-i', 
                       default='tests/test_data/text_data_0610',
                       help='输入文件夹路径 (默认: tests/test_data/text_data_0610)')
    parser.add_argument('--output', '-o',
                       default='tests/test_result/batch_test_mock',
                       help='输出文件夹路径 (默认: tests/test_result/batch_test_mock)')
    
    args = parser.parse_args()
    
    # 检查输入目录是否存在
    if not os.path.exists(args.input):
        logger.error(f"输入目录不存在: {args.input}")
        sys.exit(1)
    
    # 创建批量测试器
    tester = MockBatchTester()
    
    # 开始批量处理
    try:
        tester.process_directory(args.input, args.output)
    except KeyboardInterrupt:
        logger.info("用户中断处理")
        sys.exit(1)
    except Exception as e:
        logger.error(f"批量处理异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 