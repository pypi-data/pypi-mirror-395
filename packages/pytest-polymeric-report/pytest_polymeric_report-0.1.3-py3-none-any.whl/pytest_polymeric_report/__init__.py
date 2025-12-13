"""
@FileName：__init__.py.py
@Description：
@Author：baojun.wang
@Time：2025/10/20 11:26
"""
# 从 plugin.py 导入插件核心逻辑（确保 Pytest 能找到钩子函数）
from .pytest_custom_report import *

# 插件元信息（可选，但推荐）
__version__ = "0.1.0"
__author__ = "baojun.wang"
