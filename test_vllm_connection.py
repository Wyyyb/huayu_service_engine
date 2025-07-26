#!/usr/bin/env python3
"""
测试vLLM服务器连接
"""

import requests
import json
import sys

def test_vllm_connection():
    """测试vLLM服务器连接"""
    
    # 测试服务器健康状态
    print("🔍 测试vLLM服务器连接...")
    
    # 1. 测试服务器是否运行
    try:
        response = requests.get("http://localhost:9001/v1/models", timeout=5)
        if response.status_code == 200:
            print("✅ vLLM服务器正在运行")
            models = response.json()
            print(f"📋 可用模型: {models}")
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到vLLM服务器 (localhost:9001)")
        print("💡 请先启动vLLM服务器:")
        print("   ./start_vllm_server.sh")
        return False
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False
    
    # 2. 测试聊天完成API
    print("\n🔍 测试聊天完成API...")
    
    test_prompt = "你好，请简单介绍一下自己"
    
    try:
        payload = {
            "model": "Qwen3-8B",
            "messages": [
                {"role": "user", "content": test_prompt}
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        response = requests.post(
            "http://localhost:9001/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and result["choices"]:
                content = result["choices"][0]["message"]["content"]
                print("✅ 聊天API测试成功")
                print(f"📝 测试回复: {content[:100]}...")
                return True
            else:
                print("❌ API响应格式异常")
                print(f"响应内容: {result}")
                return False
        else:
            print(f"❌ API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API测试异常: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("           vLLM 服务器连接测试")
    print("=" * 50)
    
    success = test_vllm_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 所有测试通过！vLLM服务器运行正常")
        print("💡 现在可以运行批量测试脚本:")
        print("   python batch_test_0725.py")
    else:
        print("❌ 测试失败！请检查vLLM服务器状态")
        print("💡 启动vLLM服务器:")
        print("   ./start_vllm_server.sh")
        print("💡 或使用快速启动:")
        print("   ./start_vllm_quick.sh")
    print("=" * 50)

if __name__ == "__main__":
    main() 