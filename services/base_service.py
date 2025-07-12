import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseService(ABC):
    """基础服务类，定义所有服务的通用接口"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理文本服务的核心方法
        
        Args:
            notice_id: 公告ID
            content: 文本内容
            extra_info: 额外信息字典
            
        Returns:
            处理结果字典
        """
        pass
    
    def validate_input(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> bool:
        """
        验证输入参数
        
        Args:
            notice_id: 公告ID
            content: 文本内容
            extra_info: 额外信息字典
            
        Returns:
            验证是否通过
        """
        if not notice_id or not isinstance(notice_id, str):
            self.logger.error("Invalid notice_id")
            return False
        
        if not content or not isinstance(content, str):
            self.logger.error("Invalid content")
            return False
        
        if not isinstance(extra_info, dict):
            self.logger.error("Invalid extra_info")
            return False
        
        return True
    
    def format_response(self, success: bool, data: Any = None, error: str = None) -> Dict[str, Any]:
        """
        格式化响应结果
        
        Args:
            success: 是否成功
            data: 响应数据
            error: 错误信息
            
        Returns:
            格式化的响应字典
        """
        response = {
            'success': success,
            'timestamp': self._get_timestamp()
        }
        
        if success and data is not None:
            response['data'] = data
        elif not success and error:
            response['error'] = error
            
        return response
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat() 