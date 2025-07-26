# 字段别名系统
FIELD_ALIASES = {
    # 产品相关
    "产品": ["产品", "采购品目", "货物名称", "品目名称", "标的名称", "标项名称"],
    "品牌": ["品牌", "产品品牌"],
    "型号": ["型号", "产品型号"],
    "数量": ["数量", "产品数量"],
    "单价": ["单价", "产品单价", "预算单价"],
    "中标价格": ["中标金额", "中标价格", "成交金额"],
    "预算金额": ["预算金额"],
    "最高限价": ["最高限价"],
    # 单位相关
    "招标单位": ["招标单位", "采购人", "采购单位", "采购机构", "采购人名称"],
    "供应商": ["供应商", "中标单位", "中标供应商", "成交供应商"],
}

# 反向别名映射（用于后处理字段映射）
REVERSE_FIELD_ALIASES = {}
for k, vs in FIELD_ALIASES.items():
    for v in vs:
        REVERSE_FIELD_ALIASES[v] = k

# 服务字段定义
SERVICE_FIELDS = {
    "bidding_product": ["招标单位", "产品", "数量", "预算单价", "预算金额", "最高限价"],
    "winning_product": ["招标单位", "供应商", "产品", "品牌", "型号", "数量", "单价", "中标价格"],
    "code_extraction": ["项目编号", "招标编号", "合同编号", "采购编号", "采购计划编号", "意向编号", "包号", "标段号", "订单号", "流水号"],
    "district_time": ["采购地区", "发布时间", "报名截止时间", "获取招标文件开始时间", "获取招标文件截止时间", "递交投标文件开始时间", "递交投标文件截止时间", "报价截止时间", "开标时间"],
    "notice_type": ["公告类型"],
    "bid_type": ["采购类型"],
    "contact_info": ["所属企业名称", "联系人名字", "联系电话", "账号类型"],
}

# prompt模板
PROMPT_TEMPLATES = {
    "bidding_product": "请从下列招标公告文本中，提取招标单位、产品、数量、预算单价、预算金额、最高限价，结果按markdown表格输出，空的字段用\"空\"代替。\n\n{content}",
    "winning_product": "请从下列中标公告文本中，提取招标单位、供应商、产品、品牌(如有)、型号、数量、单价、中标价格，结果按markdown表格输出，空的字段用\"空\"代替。\n\n{content}",
    "code_extraction": "请从下列公告文本中，提取项目编号、招标编号、合同编号、采购编号、采购计划编号、意向编号、包号、标段号、订单号、流水号，结果以JSON格式输出，空的字段用\"空\"代替。\n\n{content}",
    "district_time": "请从下列公告文本中，提取采购地区、发布时间、报名截止时间、获取招标文件开始时间、获取招标文件截止时间、递交投标文件开始时间、递交投标文件截止时间、报价截止时间、开标时间，结果以JSON格式输出，空的字段用\"空\"代替。\n\n{content}",
    "notice_type": "请判断下列公告文本的公告类型（如招标、中标、变更、废标等），结果以JSON格式输出。\n\n{content}",
    "bid_type": "请判断下列公告文本的采购类型（如公开招标、竞争性谈判、单一来源等），结果以JSON格式输出。\n\n{content}",
    "contact_info": "请从下列公告文本中，提取所有联系人信息，包括所属企业名称、联系人名字、联系电话、账号类型，结果按markdown表格输出，空的字段用\"空\"代替。\n\n{content}",
}

def get_prompt(service_type: str, content: str) -> str:
    """
    根据服务类型和内容生成prompt
    """
    template = PROMPT_TEMPLATES.get(service_type)
    if not template:
        raise ValueError(f"未知服务类型: {service_type}")
    return template.format(content=content)

def get_field_alias(field: str) -> str:
    """
    获取字段的标准名
    """
    return REVERSE_FIELD_ALIASES.get(field, field)

def get_service_fields(service_type: str):
    return SERVICE_FIELDS.get(service_type, []) 