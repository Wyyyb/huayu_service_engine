#!/usr/bin/env python3
"""
远程服务测试脚本 - 测试部署在测试机上的华宇服务引擎
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

# 远程服务配置
REMOTE_BASE_URL = "http://115.231.130.211:8888"
LOCAL_BASE_URL = "http://localhost:8888"
TIMEOUT = 30

class RemoteServiceTester:
    """远程服务测试器"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.test_results = []
        self.start_time = datetime.now()
        
    def log_test(self, test_name, success, response_time=None, error=None):
        """记录测试结果"""
        result = {
            'test_name': test_name,
            'success': success,
            'response_time': response_time,
            'error': error,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ 通过" if success else "❌ 失败"
        time_info = f" ({response_time:.2f}s)" if response_time else ""
        print(f"{status} {test_name}{time_info}")
        if error:
            print(f"   错误: {error}")
    
    def test_health_check(self):
        """测试健康检查接口"""
        print(f"\n=== 测试健康检查接口 ({self.base_url}/health) ===")
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/health", timeout=TIMEOUT)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("健康检查", True, response_time)
                print(f"   服务状态: {data.get('status', 'unknown')}")
                print(f"   服务名称: {data.get('service', 'unknown')}")
                print(f"   版本: {data.get('version', 'unknown')}")
                return True
            else:
                self.log_test("健康检查", False, response_time, f"HTTP {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.log_test("健康检查", False, None, "连接失败 - 服务可能未启动")
            return False
        except requests.exceptions.Timeout:
            self.log_test("健康检查", False, None, "请求超时")
            return False
        except Exception as e:
            self.log_test("健康检查", False, None, str(e))
            return False
    
    def test_text_service(self, service_type, notice_id, content, extra_info=None):
        """测试文本服务"""
        print(f"\n=== 测试文本服务: {service_type} ===")
        try:
            url = f"{self.base_url}/api/text"
            data = {
                "service_type": service_type,
                "notice_id": notice_id,
                "content": content,
                "extra_info": extra_info or {}
            }
            
            start_time = time.time()
            response = requests.post(url, json=data, timeout=TIMEOUT)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log_test(f"文本服务-{service_type}", True, response_time)
                    print(f"   返回数据: {json.dumps(result.get('data', {}), ensure_ascii=False, indent=4)}")
                    return True
                else:
                    self.log_test(f"文本服务-{service_type}", False, response_time, result.get('error'))
                    return False
            else:
                self.log_test(f"文本服务-{service_type}", False, response_time, f"HTTP {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.log_test(f"文本服务-{service_type}", False, None, "连接失败")
            return False
        except requests.exceptions.Timeout:
            self.log_test(f"文本服务-{service_type}", False, None, "请求超时")
            return False
        except Exception as e:
            self.log_test(f"文本服务-{service_type}", False, None, str(e))
            return False
    
    def test_multimodal_service(self, notice_id, file_type="pdf"):
        """测试多模态服务"""
        print(f"\n=== 测试多模态服务: {file_type} ===")
        try:
            url = f"{self.base_url}/api/multimodal"
            
            if file_type == "pdf":
                # 模拟PDF数据（base64编码的简单PDF）
                pdf_data = "JVBERi0xLjQKJcOkw7zDtsO8DQoxIDAgb2JqDQo8PA0KL1R5cGUgL0NhdGFsb2cNCi9QYWdlcyAyIDAgUg0KPj4NCmVuZG9iag0KMiAwIG9iag0KPDwNCi9UeXBlIC9QYWdlcw0KL0NvdW50IDENCi9LaWRzIFsgMyAwIFIgXQ0KPj4NCmVuZG9iag0KMyAwIG9iag0KPDwNCi9UeXBlIC9QYWdlDQovUGFyZW50IDIgMCBSDQovUmVzb3VyY2VzIDw8DQovRm9udCA8PA0KL0YxIDQgMCBSDQo+Pg0KPj4NCi9Db250ZW50cyA1IDAgUg0KL01lZGlhQm94IFsgMCAwIDYxMiA3OTIgXQ0KPj4NCmVuZG9iag0KNCAwIG9iag0KPDwNCi9UeXBlIC9Gb250DQovU3VidHlwZSAvVHlwZTENCi9CYXNlRm9udCAvQXJpYWwNCi9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nDQo+Pg0KZW5kb2JqDQo1IDAgb2JqDQo8PA0KL0xlbmd0aCAxMw0KPj4NCnN0cmVhbQ0KQlQNCi9GMSAxMiBUZg0KKEhlbGxvIFdvcmxkKSBUag0KRVQNCmVuZHN0cmVhbQ0KZW5kb2JqDQp4cmVmDQowIDYNCjAwMDAwMDAwMDAgNjU1MzUgZiANCjAwMDAwMDAwMTAgMDAwMDAgbg0KMDAwMDAwMDA3OSAwMDAwMCBuDQowMDAwMDAwMTczIDAwMDAwIG4NCjAwMDAwMDAzMDEgMDAwMDAgbg0KMDAwMDAwMDM4MCAwMDAwMCBuDQp0cmFpbGVyDQo8PA0KL1NpemUgNg0KL1Jvb3QgMSAwIFINCj4+DQpzdGFydHhyZWYNCjQ5Mg0KJSVFT0Y="
                data = {
                    "notice_id": notice_id,
                    "file_type": "pdf",
                    "file_data": pdf_data,
                    "extra_info": {"test": True}
                }
            else:
                # 模拟图片数据
                image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
                data = {
                    "notice_id": notice_id,
                    "file_type": "images",
                    "file_data_list": [image_data, image_data],
                    "extra_info": {"test": True}
                }
            
            start_time = time.time()
            response = requests.post(url, json=data, timeout=TIMEOUT)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log_test(f"多模态服务-{file_type}", True, response_time)
                    print(f"   返回数据: {json.dumps(result.get('data', {}), ensure_ascii=False, indent=4)}")
                    return True
                else:
                    self.log_test(f"多模态服务-{file_type}", False, response_time, result.get('error'))
                    return False
            else:
                self.log_test(f"多模态服务-{file_type}", False, response_time, f"HTTP {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.log_test(f"多模态服务-{file_type}", False, None, "连接失败")
            return False
        except requests.exceptions.Timeout:
            self.log_test(f"多模态服务-{file_type}", False, None, "请求超时")
            return False
        except Exception as e:
            self.log_test(f"多模态服务-{file_type}", False, None, str(e))
            return False
    
    def test_network_connectivity(self):
        """测试网络连通性"""
        print(f"\n=== 测试网络连通性 ===")
        try:
            import socket
            host = "115.231.130.211"
            port = 8888
            
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((host, port))
            response_time = time.time() - start_time
            sock.close()
            
            if result == 0:
                self.log_test("网络连通性", True, response_time)
                return True
            else:
                self.log_test("网络连通性", False, response_time, f"端口 {port} 不可达")
                return False
                
        except Exception as e:
            self.log_test("网络连通性", False, None, str(e))
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print(f"开始测试远程服务: {self.base_url}")
        print(f"测试时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 测试网络连通性
        if not self.test_network_connectivity():
            print("\n❌ 网络连通性测试失败，无法连接到远程服务器")
            return False
        
        # 测试健康检查
        if not self.test_health_check():
            print("\n❌ 健康检查失败，服务可能未启动")
            return False
        
        # 测试文本服务
        text_services = [
            ("bidding_product", "BID001", "宜城市人民医院采购胰岛素泵四台，预算单价30000元，预算金额120000元。"),
            ("winning_product", "WIN001", "襄阳智立医疗器械维修有限公司中标，中标金额118400元。"),
            ("code_extraction", "CODE001", "项目编号：yc23460020(cgp)，招标编号：yc23460020(cgp)。"),
            ("district_time", "TIME001", "宜城市人民医院项目，发布时间2024年1月1日。"),
            ("notice_type", "TYPE001", "这是一份中标公告。"),
            ("bid_type", "BIDTYPE001", "本次采购采用公开招标方式。"),
            ("contact_info", "CONTACT001", "联系人：廖主任，电话：0710-4268367。")
        ]
        
        text_success_count = 0
        for service_type, notice_id, content in text_services:
            if self.test_text_service(service_type, notice_id, content, {"test": True, "source": "remote_test"}):
                text_success_count += 1
        
        # 测试多模态服务
        multimodal_success_count = 0
        if self.test_multimodal_service("DOC001", "pdf"):
            multimodal_success_count += 1
        if self.test_multimodal_service("IMG001", "images"):
            multimodal_success_count += 1
        
        # 输出测试结果汇总
        self.print_summary(text_success_count, len(text_services), multimodal_success_count)
        
        return text_success_count == len(text_services) and multimodal_success_count == 2
    
    def print_summary(self, text_success, text_total, multimodal_success):
        """打印测试结果汇总"""
        print(f"\n{'='*60}")
        print("测试结果汇总")
        print(f"{'='*60}")
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        print(f"测试开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"测试结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"测试总耗时: {duration:.2f}秒")
        print(f"测试目标: {self.base_url}")
        print()
        
        print("详细结果:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            time_info = f" ({result['response_time']:.2f}s)" if result['response_time'] else ""
            print(f"  {status} {result['test_name']}{time_info}")
            if result['error']:
                print(f"     错误: {result['error']}")
        
        print()
        print(f"文本服务测试: {text_success}/{text_total} 成功")
        print(f"多模态服务测试: {multimodal_success}/2 成功")
        
        total_tests = text_total + 2
        total_success = text_success + multimodal_success
        
        print(f"总体成功率: {total_success}/{total_tests} ({total_success/total_tests*100:.1f}%)")
        
        if total_success == total_tests:
            print("\n🎉 所有测试通过！远程服务运行正常。")
        else:
            print(f"\n⚠️  部分测试失败，请检查远程服务状态。")
    
    def save_test_report(self, filename=None):
        """保存测试报告"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"remote_test_report_{timestamp}.json"
        
        report = {
            'test_time': self.start_time.isoformat(),
            'target_url': self.base_url,
            'total_tests': len(self.test_results),
            'success_count': sum(1 for r in self.test_results if r['success']),
            'results': self.test_results
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"\n📄 测试报告已保存: {filename}")
        except Exception as e:
            print(f"\n❌ 保存测试报告失败: {e}")

def main():
    """主函数"""
    print("华语服务引擎远程测试脚本")
    print("=" * 60)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--local":
            base_url = LOCAL_BASE_URL
            print("测试本地服务")
        elif sys.argv[1] == "--remote":
            base_url = REMOTE_BASE_URL
            print("测试远程服务")
        else:
            base_url = sys.argv[1]
            print(f"测试自定义地址: {base_url}")
    else:
        base_url = REMOTE_BASE_URL
        print("测试远程服务 (默认)")
    
    print(f"目标地址: {base_url}")
    print()
    
    # 创建测试器并运行测试
    tester = RemoteServiceTester(base_url)
    success = tester.run_all_tests()
    
    # 保存测试报告
    tester.save_test_report()
    
    # 退出码
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 