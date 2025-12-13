# -*- coding: utf-8 -*-
"""
普通话水平测试(PSC)报名查询工具

提供查询普通话水平测试报名信息的功能，包括:
- 查询支持报名的省份列表
- 查询各省当前开放报名的测试站点
- 查询各省即将开放报名的测试站点
"""

__version__ = "0.0.2"

from .psc import mcp, get_provinces, get_open_stations, get_next_stations

__all__ = [
    "mcp",
    "get_provinces",
    "get_open_stations",
    "get_next_stations",
    "__version__"
]