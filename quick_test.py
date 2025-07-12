#!/usr/bin/env python3
"""
快速测试脚本 - 简单的连通性检查
"""

import requests
import sys
import time

# 配置
REMOTE_URL = "http://115.231.130.211:8888"
TIMEOUT = 10

def quick_test():
    """快速测试远程服务"""
    print("🔍 快速测试远程服务连通性...")
    print(f"目标: {REMOTE_URL}")
    print("-" * 50)
    
    # 测试健康检查
    try:
        start_time = time.time()
        response = requests.get(f"{REMOTE_URL}/health", timeout=TIMEOUT)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 服务正常 (响应时间: {response_time:.2f}s)")
            print(f"   状态: {data.get('status', 'unknown')}")
            print(f"   服务: {data.get('service', 'unknown')}")
            print(f"   版本: {data.get('version', 'unknown')}")
            return True
        else:
            print(f"❌ 服务异常 (HTTP {response.status_code})")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败 - 服务可能未启动或网络不通")
        return False
    except requests.exceptions.Timeout:
        print("❌ 请求超时 - 服务响应过慢")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def test_one_service():
    """测试一个文本服务"""
    print("\n🧪 测试文本服务...")
    
    try:
        url = f"{REMOTE_URL}/api/text"
        data = {
            "service_type": "bidding_product",
            "notice_id": "QUICK_TEST",
            "content": "测试内容",
            "extra_info": {"test": True}
        }
        
        start_time = time.time()
        response = requests.post(url, json=data, timeout=TIMEOUT)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ 文本服务正常 (响应时间: {response_time:.2f}s)")
                return True
            else:
                print(f"❌ 文本服务错误: {result.get('error')}")
                return False
        else:
            print(f"❌ 文本服务异常 (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ 文本服务测试失败: {e}")
        return False

def main():
    """主函数"""
    print("华语服务引擎 - 快速测试")
    print("=" * 50)
    
    # 健康检查
    health_ok = quick_test()
    
    if health_ok:
        # 测试文本服务
        service_ok = test_one_service()
        
        if service_ok:
            print("\n🎉 所有测试通过！服务运行正常。")
            sys.exit(0)
        else:
            print("\n⚠️  服务部分异常，请检查详细日志。")
            sys.exit(1)
    else:
        print("\n❌ 服务不可用，请检查网络连接和服务状态。")
        sys.exit(1)

if __name__ == "__main__":
    main() 