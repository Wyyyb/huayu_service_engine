#!/usr/bin/env python3
"""
服务测试脚本
"""

import requests
import json
import time
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 服务配置
BASE_URL = "http://localhost:8888"
TIMEOUT = 30

def test_health_check():
    """测试健康检查接口"""
    print("=== 测试健康检查接口 ===")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def test_text_service(service_type, notice_id, content, extra_info=None):
    """测试文本服务"""
    print(f"\n=== 测试文本服务: {service_type} ===")
    try:
        url = f"{BASE_URL}/api/text"
        data = {
            "service_type": service_type,
            "notice_id": notice_id,
            "content": content,
            "extra_info": extra_info or {}
        }
        
        response = requests.post(url, json=data, timeout=TIMEOUT)
        print(f"状态码: {response.status_code}")
        print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"文本服务测试失败: {e}")
        return False

def test_multimodal_service_json(notice_id, file_type, file_data, extra_info=None):
    """测试多模态服务（JSON方式）"""
    print(f"\n=== 测试多模态服务 (JSON): {file_type} ===")
    try:
        url = f"{BASE_URL}/api/multimodal"
        data = {
            "notice_id": notice_id,
            "file_type": file_type,
            "file_data": file_data,
            "extra_info": extra_info or {}
        }
        
        response = requests.post(url, json=data, timeout=TIMEOUT)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"多模态服务测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("开始运行服务测试...")
    
    # 测试健康检查
    if not test_health_check():
        print("健康检查失败，请确保服务已启动")
        return False
    
    # 测试文本服务
    text_services = [
        ("bidding_product", "BID001", "某公司招标公告：采购办公设备一批，预算金额100万元，投标截止时间2024年2月1日。"),
        ("winning_product", "WIN001", "中标公告：某项目由ABC公司中标，中标金额95万元，中标时间2024年1月15日。"),
        ("code_extraction", "ID001", "项目编号：PRJ2024001，招标编号：TDR2024001，合同编号：CTR2024001。"),
        ("district_time", "LOC001", "北京市朝阳区某项目，发布时间：2024年1月1日，截止时间：2024年2月1日。"),
        ("notice_type", "CLS001", "这是一份招标公告，涉及政府采购项目。"),
        ("bid_type", "PUR001", "采购类型：货物采购，预算金额：100万元。"),
        ("contact_info", "CON001", "联系人：张三，电话：010-12345678，邮箱：zhangsan@example.com，地址：北京市朝阳区。")
    ]
    
    text_success_count = 0
    for service_type, notice_id, content in text_services:
        if test_text_service(service_type, notice_id, content, {"test": True}):
            text_success_count += 1
    
    # 测试多模态服务
    multimodal_success_count = 0
    
    # 模拟PDF数据（base64编码的简单PDF）
    pdf_data = "JVBERi0xLjQKJcOkw7zDtsO8DQoxIDAgb2JqDQo8PA0KL1R5cGUgL0NhdGFsb2cNCi9QYWdlcyAyIDAgUg0KPj4NCmVuZG9iag0KMiAwIG9iag0KPDwNCi9UeXBlIC9QYWdlcw0KL0NvdW50IDENCi9LaWRzIFsgMyAwIFIgXQ0KPj4NCmVuZG9iag0KMyAwIG9iag0KPDwNCi9UeXBlIC9QYWdlDQovUGFyZW50IDIgMCBSDQovUmVzb3VyY2VzIDw8DQovRm9udCA8PA0KL0YxIDQgMCBSDQo+Pg0KPj4NCi9Db250ZW50cyA1IDAgUg0KL01lZGlhQm94IFsgMCAwIDYxMiA3OTIgXQ0KPj4NCmVuZG9iag0KNCAwIG9iag0KPDwNCi9UeXBlIC9Gb250DQovU3VidHlwZSAvVHlwZTENCi9CYXNlRm9udCAvQXJpYWwNCi9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nDQo+Pg0KZW5kb2JqDQo1IDAgb2JqDQo8PA0KL0xlbmd0aCAxMw0KPj4NCnN0cmVhbQ0KQlQNCi9GMSAxMiBUZg0KKEhlbGxvIFdvcmxkKSBUag0KRVQNCmVuZHN0cmVhbQ0KZW5kb2JqDQp4cmVmDQowIDYNCjAwMDAwMDAwMDAgNjU1MzUgZiANCjAwMDAwMDAwMTAgMDAwMDAgbg0KMDAwMDAwMDA3OSAwMDAwMCBuDQowMDAwMDAwMTczIDAwMDAwIG4NCjAwMDAwMDAzMDEgMDAwMDAgbg0KMDAwMDAwMDM4MCAwMDAwMCBuDQp0cmFpbGVyDQo8PA0KL1NpemUgNg0KL1Jvb3QgMSAwIFINCj4+DQpzdGFydHhyZWYNCjQ5Mg0KJSVFT0Y="
    
    if test_multimodal_service_json("DOC001", "pdf", pdf_data, {"test": True}):
        multimodal_success_count += 1
    
    # 测试图片服务（模拟数据）
    image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    image_data_list = [image_data, image_data]
    
    # 测试图片服务（模拟数据）
    image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    image_data_list = [image_data, image_data]
    
    try:
        url = f"{BASE_URL}/api/multimodal"
        data = {
            "notice_id": "IMG001",
            "file_type": "images",
            "file_data_list": image_data_list,
            "extra_info": {"test": True}
        }
        
        response = requests.post(url, json=data, timeout=TIMEOUT)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        if response.status_code == 200:
            multimodal_success_count += 1
    except Exception as e:
        print(f"图片服务测试失败: {e}")
    
    # 输出测试结果
    print(f"\n=== 测试结果汇总 ===")
    print(f"文本服务测试: {text_success_count}/{len(text_services)} 成功")
    print(f"多模态服务测试: {multimodal_success_count}/2 成功")
    
    total_tests = len(text_services) + 2
    total_success = text_success_count + multimodal_success_count
    
    print(f"总体成功率: {total_success}/{total_tests} ({total_success/total_tests*100:.1f}%)")
    
    return total_success == total_tests

if __name__ == "__main__":
    print("华语服务引擎测试脚本")
    print("=" * 50)
    
    success = run_all_tests()
    
    if success:
        print("\n✅ 所有测试通过！")
        sys.exit(0)
    else:
        print("\n❌ 部分测试失败，请检查服务状态")
        sys.exit(1) 