"""普通话水平测试报名查询工具."""

__version__ = "0.0.4"

from .psc import get_provinces, get_open_stations, get_next_stations, main

__all__ = [
    "get_provinces",
    "get_open_stations",
    "get_next_stations",
    "main",
    "__version__",
]