from typing import Dict, Any, List
from .base_service import BaseService
from .vllm_client import VLLMClient
from .prompt_templates import get_prompt, get_service_fields
from .markdown_parser import parse_markdown_table
import json

class BiddingProductService(BaseService):
    """招标公告产品服务（真实实现）"""
    def __init__(self):
        super().__init__()
        self.vllm = VLLMClient()
        self.service_type = "bidding_product"
        self.fields = get_service_fields(self.service_type)

    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        try:
            prompt = get_prompt(self.service_type, content)
            llm_output = self.vllm.chat_completion(prompt)
            if not llm_output:
                return self.format_response(False, error="大模型无返回或异常")
            table = parse_markdown_table(llm_output)
            products = []
            for row in table:
                prod = {field: row.get(field, "空") for field in self.fields}
                products.append(prod)
            result = {
                'notice_id': notice_id,
                'service_type': self.service_type,
                'bidding_products': products
            }
            return self.format_response(True, data=result)
        except Exception as e:
            self.logger.error(f"bidding_product服务异常: {e}")
            return self.format_response(False, error=str(e))

class WinningProductService(BaseService):
    """中标公告产品服务（真实实现）"""
    def __init__(self):
        super().__init__()
        self.vllm = VLLMClient()
        self.service_type = "winning_product"
        self.fields = get_service_fields(self.service_type)

    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        try:
            prompt = get_prompt(self.service_type, content)
            llm_output = self.vllm.chat_completion(prompt)
            if not llm_output:
                return self.format_response(False, error="大模型无返回或异常")
            table = parse_markdown_table(llm_output)
            products = []
            for row in table:
                prod = {field: row.get(field, "空") for field in self.fields}
                products.append(prod)
            result = {
                'notice_id': notice_id,
                'service_type': self.service_type,
                'winning_products': products
            }
            return self.format_response(True, data=result)
        except Exception as e:
            self.logger.error(f"winning_product服务异常: {e}")
            return self.format_response(False, error=str(e))

class CodeExtractionService(BaseService):
    """编号提取服务（真实实现）"""
    def __init__(self):
        super().__init__()
        self.vllm = VLLMClient()
        self.service_type = "code_extraction"
        self.fields = get_service_fields(self.service_type)

    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        try:
            prompt = get_prompt(self.service_type, content)
            llm_output = self.vllm.chat_completion(prompt)
            if not llm_output:
                return self.format_response(False, error="大模型无返回或异常")
            # 解析JSON
            try:
                data = json.loads(llm_output)
            except Exception:
                # 容错：尝试提取JSON片段
                match = json.JSONDecoder().raw_decode(llm_output)
                data = match[0] if match else {}
            codes = {field: data.get(field, "空") for field in self.fields}
            result = {
                'notice_id': notice_id,
                'service_type': self.service_type,
                'codes': codes
            }
            return self.format_response(True, data=result)
        except Exception as e:
            self.logger.error(f"code_extraction服务异常: {e}")
            return self.format_response(False, error=str(e))

class DistrictTimeService(BaseService):
    """地区时间提取服务（真实实现）"""
    def __init__(self):
        super().__init__()
        self.vllm = VLLMClient()
        self.service_type = "district_time"
        self.fields = get_service_fields(self.service_type)

    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        try:
            prompt = get_prompt(self.service_type, content)
            llm_output = self.vllm.chat_completion(prompt)
            if not llm_output:
                return self.format_response(False, error="大模型无返回或异常")
            try:
                data = json.loads(llm_output)
            except Exception:
                match = json.JSONDecoder().raw_decode(llm_output)
                data = match[0] if match else {}
            district_time = {field: data.get(field, "空") for field in self.fields}
            result = {
                'notice_id': notice_id,
                'service_type': self.service_type,
                'district_time': district_time
            }
            return self.format_response(True, data=result)
        except Exception as e:
            self.logger.error(f"district_time服务异常: {e}")
            return self.format_response(False, error=str(e))

class NoticeTypeService(BaseService):
    """公告类型分类（真实实现）"""
    def __init__(self):
        super().__init__()
        self.vllm = VLLMClient()
        self.service_type = "notice_type"
        self.fields = get_service_fields(self.service_type)

    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        try:
            prompt = get_prompt(self.service_type, content)
            llm_output = self.vllm.chat_completion(prompt)
            if not llm_output:
                return self.format_response(False, error="大模型无返回或异常")
            try:
                data = json.loads(llm_output)
            except Exception:
                match = json.JSONDecoder().raw_decode(llm_output)
                data = match[0] if match else {}
            notice_type = {field: data.get(field, "空") for field in self.fields}
            result = {
                'notice_id': notice_id,
                'service_type': self.service_type,
                'notice_type': notice_type
            }
            return self.format_response(True, data=result)
        except Exception as e:
            self.logger.error(f"notice_type服务异常: {e}")
            return self.format_response(False, error=str(e))

class BidTypeService(BaseService):
    """采购类型分类（真实实现）"""
    def __init__(self):
        super().__init__()
        self.vllm = VLLMClient()
        self.service_type = "bid_type"
        self.fields = get_service_fields(self.service_type)

    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        try:
            prompt = get_prompt(self.service_type, content)
            llm_output = self.vllm.chat_completion(prompt)
            if not llm_output:
                return self.format_response(False, error="大模型无返回或异常")
            try:
                data = json.loads(llm_output)
            except Exception:
                match = json.JSONDecoder().raw_decode(llm_output)
                data = match[0] if match else {}
            bid_type = {field: data.get(field, "空") for field in self.fields}
            result = {
                'notice_id': notice_id,
                'service_type': self.service_type,
                'bid_type': bid_type
            }
            return self.format_response(True, data=result)
        except Exception as e:
            self.logger.error(f"bid_type服务异常: {e}")
            return self.format_response(False, error=str(e))

class ContactInfoService(BaseService):
    """联系人信息解析（真实实现）"""
    def __init__(self):
        super().__init__()
        self.vllm = VLLMClient()
        self.service_type = "contact_info"
        self.fields = get_service_fields(self.service_type)

    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        try:
            prompt = get_prompt(self.service_type, content)
            llm_output = self.vllm.chat_completion(prompt)
            if not llm_output:
                return self.format_response(False, error="大模型无返回或异常")
            table = parse_markdown_table(llm_output)
            contacts = []
            for row in table:
                contact = {field: row.get(field, "空") for field in self.fields}
                contacts.append(contact)
            result = {
                'notice_id': notice_id,
                'service_type': self.service_type,
                'contacts': contacts
            }
            return self.format_response(True, data=result)
        except Exception as e:
            self.logger.error(f"contact_info服务异常: {e}")
            return self.format_response(False, error=str(e)) 