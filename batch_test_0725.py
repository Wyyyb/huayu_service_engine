#!/usr/bin/env python3
"""
批量测试脚本 - 处理测试数据并调用各个文本服务
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

class BatchTester:
    """批量测试器"""
    
    def __init__(self):
        # 初始化所有文本服务
        self.services = {
            'bidding_product': BiddingProductService(),
            'winning_product': WinningProductService(),
            'code_extraction': CodeExtractionService(),
            'district_time': DistrictTimeService(),
            'notice_type': NoticeTypeService(),
            'bid_type': BidTypeService(),
            'contact_info': ContactInfoService()
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
        # 移除扩展名
        name = os.path.splitext(filename)[0]
        # 如果文件名包含test_，提取数字部分
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
        logger.info(f"开始批量处理")
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
                "success_rate": f"{success_count/total_files*100:.1f}%" if total_files > 0 else "0%"
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
    parser = argparse.ArgumentParser(description='批量测试文本服务')
    parser.add_argument('--input', '-i', 
                       default='tests/test_data/text_data_0610',
                       help='输入文件夹路径 (默认: tests/test_data/text_data_0610)')
    parser.add_argument('--output', '-o',
                       default='tests/test_result/batch_test_0725',
                       help='输出文件夹路径 (默认: tests/test_result/batch_test_0725)')
    
    args = parser.parse_args()
    
    # 检查输入目录是否存在
    if not os.path.exists(args.input):
        logger.error(f"输入目录不存在: {args.input}")
        sys.exit(1)
    
    # 创建批量测试器
    tester = BatchTester()
    
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