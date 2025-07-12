from typing import Dict, Any, List
from .base_service import BaseService

class BiddingProductService(BaseService):
    """招标公告产品服务"""
    
    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理招标公告产品信息
        
        Args:
            notice_id: 公告ID
            content: 文本内容
            extra_info: 额外信息字典
            
        Returns:
            处理结果
        """
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        
        try:
            # 默认返回招标公告产品信息（列表格式）
            result = {
                'notice_id': notice_id,
                'service_type': 'bidding_product',
                'processed_content': content,
                'bidding_products': [
                    {
                        "招标单位": "宜城市人民医院",
                        "产品": "胰岛素泵",
                        "数量": "四台",
                        "预算单价": "30000.00元",
                        "预算金额": "120000元",
                        "最高限价": "120000元"
                    }
                ]
            }
            
            return self.format_response(True, data=result)
            
        except Exception as e:
            self.logger.error(f"Error processing bidding products: {str(e)}")
            return self.format_response(False, error=str(e))

class WinningProductService(BaseService):
    """中标公告产品服务"""
    
    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理中标公告产品信息
        
        Args:
            notice_id: 公告ID
            content: 文本内容
            extra_info: 额外信息字典
            
        Returns:
            处理结果
        """
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        
        try:
            # 默认返回中标公告产品信息（列表格式）
            result = {
                'notice_id': notice_id,
                'service_type': 'winning_product',
                'processed_content': content,
                'winning_products': [
                    {
                        "中标单位": "襄阳智立医疗器械维修有限公司",
                        "产品名称": "胰岛素泵",
                        "标的名称": "无",
                        "标项名称": "无",
                        "产品品牌": "迈世通",
                        "产品型号": "mti-piii",
                        "生产厂家": "无",
                        "产品数量": "四台",
                        "产品单价": "29600.00元",
                        "中标金额": "118400元",
                        "品目名称": "无",
                        "招标单位": "宜城市人民医院",
                        "招标金额": "无",
                        "预算金额": "无"
                    }
                ]
            }
            
            return self.format_response(True, data=result)
            
        except Exception as e:
            self.logger.error(f"Error processing winning products: {str(e)}")
            return self.format_response(False, error=str(e))

class CodeExtractionService(BaseService):
    """编号提取服务"""
    
    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        提取编号信息
        
        Args:
            notice_id: 公告ID
            content: 文本内容
            extra_info: 额外信息字典
            
        Returns:
            处理结果
        """
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        
        try:
            # 默认返回编号信息（字典格式）
            result = {
                'notice_id': notice_id,
                'service_type': 'code_extraction',
                'processed_content': content,
                'codes': {
                    "项目编号": "yc23460020(cgp)",
                    "招标编号": "yc23460020(cgp)",
                    "合同编号": "无",
                    "采购编号": "无",
                    "采购计划编号": "无",
                    "意向编号": "无",
                    "包号": "无",
                    "标段号": "无",
                    "订单号": "无",
                    "流水号": "无"
                }
            }
            
            return self.format_response(True, data=result)
            
        except Exception as e:
            self.logger.error(f"Error extracting codes: {str(e)}")
            return self.format_response(False, error=str(e))

class DistrictTimeService(BaseService):
    """地区时间提取服务"""
    
    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        提取地区和时间信息
        
        Args:
            notice_id: 公告ID
            content: 文本内容
            extra_info: 额外信息字典
            
        Returns:
            处理结果
        """
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        
        try:
            # 默认返回地区时间信息（字典格式）
            result = {
                'notice_id': notice_id,
                'service_type': 'district_time',
                'processed_content': content,
                'district_time': {
                    "采购地区": "宜城市",
                    "发布时间": "无",
                    "报名截止时间": "无",
                    "获取招标文件开始时间": "无",
                    "获取招标文件截止时间": "无",
                    "递交投标文件开始时间": "无",
                    "递交投标文件截止时间": "无",
                    "报价截止时间": "无",
                    "开标时间": "无"
                }
            }
            
            return self.format_response(True, data=result)
            
        except Exception as e:
            self.logger.error(f"Error extracting district and time: {str(e)}")
            return self.format_response(False, error=str(e))

class NoticeTypeService(BaseService):
    """公告类型分类"""
    
    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分类公告类型
        
        Args:
            notice_id: 公告ID
            content: 文本内容
            extra_info: 额外信息字典
            
        Returns:
            处理结果
        """
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        
        try:
            # 默认返回公告类型信息（字典格式）
            result = {
                'notice_id': notice_id,
                'service_type': 'notice_type',
                'processed_content': content,
                'notice_type': {
                    "公告类型": "中标"
                }
            }
            
            return self.format_response(True, data=result)
            
        except Exception as e:
            self.logger.error(f"Error classifying notice type: {str(e)}")
            return self.format_response(False, error=str(e))

class BidTypeService(BaseService):
    """采购类型分类"""
    
    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分类采购类型
        
        Args:
            notice_id: 公告ID
            content: 文本内容
            extra_info: 额外信息字典
            
        Returns:
            处理结果
        """
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        
        try:
            # 默认返回采购类型信息（字典格式）
            result = {
                'notice_id': notice_id,
                'service_type': 'bid_type',
                'processed_content': content,
                'bid_type': {
                    "采购类型": "公开招标"
                }
            }
            
            return self.format_response(True, data=result)
            
        except Exception as e:
            self.logger.error(f"Error classifying bid type: {str(e)}")
            return self.format_response(False, error=str(e))

class ContactInfoService(BaseService):
    """联系人信息解析"""
    
    def process(self, notice_id: str, content: str, extra_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析联系人信息
        
        Args:
            notice_id: 公告ID
            content: 文本内容
            extra_info: 额外信息字典
            
        Returns:
            处理结果
        """
        if not self.validate_input(notice_id, content, extra_info):
            return self.format_response(False, error="Invalid input parameters")
        
        try:
            # 默认返回联系人信息（列表格式）
            result = {
                'notice_id': notice_id,
                'service_type': 'contact_info',
                'processed_content': content,
                'contacts': [
                    {
                        "所属企业名称": "宜城市人民医院",
                        "联系人名字": "廖主任",
                        "联系电话": "0710-4268367",
                        "账号类型": "无"
                    },
                    {
                        "所属企业名称": "亿诚建设项目管理有限公司",
                        "联系人名字": "李工",
                        "联系电话": "15671329168",
                        "账号类型": "无"
                    }
                ]
            }
            
            return self.format_response(True, data=result)
            
        except Exception as e:
            self.logger.error(f"Error parsing contact info: {str(e)}")
            return self.format_response(False, error=str(e)) 