# 服务配置
SERVICE_CONFIG = {
    'port': 8888,
    'host': '0.0.0.0',
    'debug': True,
    'max_buffer_size': 104857600,  # 100MB
    'max_body_size': 104857600,    # 100MB
}

# 支持的文件类型
SUPPORTED_IMAGE_TYPES = ['png', 'jpg', 'jpeg']
SUPPORTED_DOCUMENT_TYPES = ['pdf']

# 服务类型定义
SERVICE_TYPES = {
    'bidding_product': 'BiddingProductService',      # 招标公告产品服务
    'winning_product': 'WinningProductService',      # 中标公告产品服务  
    'code_extraction': 'CodeExtractionService',      # 编号提取服务
    'district_time': 'DistrictTimeService',          # 地区时间提取服务
    'notice_type': 'NoticeTypeService',              # 公告类型分类
    'bid_type': 'BidTypeService',                    # 采购类型分类
    'contact_info': 'ContactInfoService',            # 联系人信息解析
    'multimodal': 'MultimodalService'                # 多模态服务
} 