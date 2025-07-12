#!/usr/bin/env python3
"""
客户端调用示例
"""

import requests
import json
import base64

# 服务配置
BASE_URL = "http://localhost:8888"

def call_text_service(service_type, notice_id, content, extra_info=None):
    """调用文本服务"""
    url = f"{BASE_URL}/api/text"
    data = {
        "service_type": service_type,
        "notice_id": notice_id,
        "content": content,
        "extra_info": extra_info or {}
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def call_multimodal_service(notice_id, file_path, extra_info=None):
    """调用多模态服务（文件上传方式）"""
    url = f"{BASE_URL}/api/multimodal"
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'notice_id': notice_id,
                'extra_info': json.dumps(extra_info or {})
            }
            
            response = requests.post(url, files=files, data=data, timeout=30)
            return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """主函数 - 演示各种服务调用"""
    print("华语服务引擎客户端示例")
    print("=" * 50)
    
    # 示例1：招标公告产品服务
    print("\n1. 招标公告产品服务")
    result = call_text_service(
        "bidding_product",
        "BID001",
        "宜城市人民医院采购胰岛素泵四台，预算单价30000元，预算金额120000元。",
        {"source": "政府采购网"}
    )
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 示例2：中标公告产品服务
    print("\n2. 中标公告产品服务")
    result = call_text_service(
        "winning_product",
        "WIN001",
        "襄阳智立医疗器械维修有限公司中标，中标金额118400元。",
        {"source": "政府采购网"}
    )
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 示例3：编号提取服务
    print("\n3. 编号提取服务")
    result = call_text_service(
        "code_extraction",
        "CODE001",
        "项目编号：yc23460020(cgp)，招标编号：yc23460020(cgp)。",
        {"source": "政府采购网"}
    )
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 示例4：地区时间提取服务
    print("\n4. 地区时间提取服务")
    result = call_text_service(
        "district_time",
        "TIME001",
        "宜城市人民医院项目，发布时间2024年1月1日。",
        {"source": "政府采购网"}
    )
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 示例5：公告类型分类
    print("\n5. 公告类型分类")
    result = call_text_service(
        "notice_type",
        "TYPE001",
        "这是一份中标公告。",
        {"source": "政府采购网"}
    )
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 示例6：采购类型分类
    print("\n6. 采购类型分类")
    result = call_text_service(
        "bid_type",
        "BIDTYPE001",
        "本次采购采用公开招标方式。",
        {"source": "政府采购网"}
    )
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 示例7：联系人信息解析
    print("\n7. 联系人信息解析")
    result = call_text_service(
        "contact_info",
        "CONTACT001",
        "联系人：廖主任，电话：0710-4268367。",
        {"source": "政府采购网"}
    )
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    print("\n" + "=" * 50)
    print("示例调用完成！")

if __name__ == "__main__":
    main() 