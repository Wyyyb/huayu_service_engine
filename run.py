#!/usr/bin/env python3
"""
华语服务引擎启动脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import main

if __name__ == "__main__":
    print("启动华语服务引擎...")
    main() 