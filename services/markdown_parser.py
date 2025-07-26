import re
from typing import List, Dict
from .prompt_templates import get_field_alias

def parse_markdown_table(md: str) -> List[Dict[str, str]]:
    """
    解析markdown表格为dict列表，自动做字段名映射。
    """
    lines = [line.strip() for line in md.strip().splitlines() if line.strip()]
    # 找到表头和分隔线
    header_idx = None
    for i, line in enumerate(lines):
        if re.match(r"\|?\s*[-:]+\s*\|", line):
            header_idx = i - 1
            break
    if header_idx is None or header_idx < 0:
        # 兼容无分隔线的表格
        header_idx = 0
    header_line = lines[header_idx]
    headers = [h.strip().strip('`') for h in header_line.strip('|').split('|')]
    headers = [get_field_alias(h) for h in headers]
    # 数据行
    data_lines = lines[header_idx+2:] if header_idx+2 < len(lines) else lines[header_idx+1:]
    result = []
    for line in data_lines:
        if not line or set(line) <= {'-', '|', ' '}:
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) != len(headers):
            # 容错：补齐或截断
            if len(cells) < len(headers):
                cells += [''] * (len(headers) - len(cells))
            else:
                cells = cells[:len(headers)]
        row = {headers[i]: cells[i] for i in range(len(headers))}
        result.append(row)
    return result 