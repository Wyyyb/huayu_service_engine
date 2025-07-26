import json
import re
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    从文本中提取JSON对象，支持多种格式
    
    Args:
        text: 包含JSON的文本
        
    Returns:
        解析后的JSON对象，如果解析失败返回None
    """
    if not text or not isinstance(text, str):
        return None
    
    # 1. 尝试直接解析
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError as e:
        logger.debug(f"直接JSON解析失败: {e}")
        pass
    
    # 2. 查找JSON对象模式
    try:
        # 匹配 { ... } 格式
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, text, re.DOTALL)
        
        logger.debug(f"找到 {len(matches)} 个JSON对象模式匹配")
        for i, match in enumerate(matches):
            try:
                result = json.loads(match)
                logger.debug(f"第 {i+1} 个匹配解析成功: {result}")
                return result
            except json.JSONDecodeError as e:
                logger.debug(f"第 {i+1} 个匹配解析失败: {e}")
                continue
    except Exception as e:
        logger.debug(f"正则匹配失败: {e}")
    
    # 3. 尝试提取键值对
    try:
        # 匹配 "key": "value" 格式
        kv_pattern = r'"([^"]+)"\s*:\s*"([^"]*)"'
        matches = re.findall(kv_pattern, text)
        
        if matches:
            result = {}
            for key, value in matches:
                result[key] = value
            return result
    except Exception as e:
        logger.debug(f"键值对提取失败: {e}")
    
    # 4. 尝试提取中文键值对
    try:
        # 匹配中文键值对格式
        chinese_kv_pattern = r'["""]([^"""]+)["""]\s*[:：]\s*["""]([^"""]*)["""]'
        matches = re.findall(chinese_kv_pattern, text)
        
        if matches:
            result = {}
            for key, value in matches:
                result[key] = value
            return result
    except Exception as e:
        logger.debug(f"中文键值对提取失败: {e}")
    
    # 5. 尝试手动构建JSON
    try:
        # 查找常见的字段名
        fields = {
            "项目编号": None,
            "招标编号": None,
            "合同编号": None,
            "采购编号": None,
            "采购地区": None,
            "发布时间": None,
            "公告类型": None,
            "采购类型": None
        }
        
        for field in fields.keys():
            # 查找字段值
            pattern = rf'{field}[：:]\s*([^\n\r,，;；]+)'
            match = re.search(pattern, text)
            if match:
                fields[field] = match.group(1).strip()
        
        # 过滤掉None值
        result = {k: v for k, v in fields.items() if v is not None}
        if result:
            return result
    except Exception as e:
        logger.debug(f"手动构建JSON失败: {e}")
    
    return None

def safe_json_parse(text: str, default: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    安全解析JSON，提供默认值
    
    Args:
        text: 要解析的文本
        default: 默认值，如果解析失败返回此值
        
    Returns:
        解析后的JSON对象或默认值
    """
    if default is None:
        default = {}
    
    result = extract_json_from_text(text)
    if result is not None:
        return result
    
    # 详细记录解析失败的情况
    logger.error(f"JSON解析失败，原始响应内容:")
    logger.error(f"响应长度: {len(text)} 字符")
    logger.error(f"响应内容: {text}")
    logger.error(f"使用默认值: {default}")
    return default 