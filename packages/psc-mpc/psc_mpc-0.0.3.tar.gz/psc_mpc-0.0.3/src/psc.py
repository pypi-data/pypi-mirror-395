"""
普通话水平测试(PSC)报名查询工具

该模块提供了一个用于查询普通话水平测试报名信息的工具，包括:
- 查询支持报名的省份列表
- 查询各省当前开放报名的测试站点
- 查询各省即将开放报名的测试站点

依赖的API接口:
- https://psc.urabas.com/psc/api/provinces - 获取省份列表
- https://psc.urabas.com/psc/api/stations/open - 获取开放报名的测试站点
- https://psc.urabas.com/psc/api/stations/next - 获取即将开放报名的测试站点
"""

from fastmcp import FastMCP
import requests
import json

mcp = FastMCP("普通话考试报名查询工具",
   instructions="""
       普通话查询工具，
        调用 get_provinces() 获取省份列表。
        每次调用都需要重新获取省份列表，因为省份数据可能会变化。
        province_id 为省份的唯一标识符，例如 "ningxia"。这个数据从 get_provinces() 返回的列表中获取。
        调用 get_open_stations(province_id) 获取指定省份的开放报名测试站点。
        调用 get_next_stations(province_id) 获取指定省份即将开放报名的测试站点。

    """,
    tool_transformations=[
        {
            "name": "get_provinces",
            "description": "获取支持报名的省份列表"
        },
        {
            "name": "get_open_stations",
            "description": "获取指定省份当前开放报名的测试站点"
        },
        {
            "name": "get_next_stations",
            "description": "获取指定省份即将开放报名的测试站点"
        }
    ]
    )

def fetch_api_data(url: str, error_context: str = "") -> dict:
    """
    从API获取数据的辅助函数，包含错误处理机制
    
    Args:
        url (str): 要请求的API地址
        error_context (str): 错误上下文描述，用于错误信息提示
        
    Returns:
        dict: API返回的JSON数据
        
    Raises:
        Exception: 当网络请求失败或JSON解析失败时抛出异常
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"获取{error_context}时发生网络错误: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"解析{error_context}的JSON响应时发生错误: {str(e)}")

def get_provinces_data() -> list:
    """
    获取省份列表的辅助函数，统一数据格式
    
    从API获取省份数据，并确保返回统一的列表格式。
    处理不同API可能返回的不同数据结构。
    
    Returns:
        list: 省份数据列表，每个元素为包含省份信息的字典
    """
    provinces_data = fetch_api_data("https://psc.urabas.com/psc/api/provinces", "省份数据")
    
    # 统一数据格式处理
    if isinstance(provinces_data, list):
        # 提取provinceId和provinceName
        edit_provinces_data = [{"provinceId": i["provinceId"], "provinceName": i["provinceName"]} for i in provinces_data]
        return edit_provinces_data
    elif isinstance(provinces_data, dict) and 'data' in provinces_data:
        edit_provinces_data = [{"provinceId": i["provinceId"], "provinceName": i["provinceName"]} for i in provinces_data['data']]
        return edit_provinces_data
    else:
        return []



@mcp.tool
def get_provinces() -> str:
    """
    获取省份列表
    
    从API获取支持普通话水平测试报名的所有省份列表
    
    Returns:
        str: JSON格式的省份列表数据
    """
    try:
        provinces_data = get_provinces_data()
        return json.dumps(provinces_data, ensure_ascii=False, indent=2)
    except Exception as e:
        return str(e)

@mcp.tool
def get_open_stations(province_id: str) -> str:
    """
    获取指定省份当前开放报名的测试站点
    
    Args:
        province_id (str): 省份ID
        
    Returns:
        str: JSON格式的开放报名测试站点数据
    """
    try:
        url = f"https://psc.urabas.com/psc/api/stations/open?provinceId={province_id}"
        stations_data = fetch_api_data(url, f"省份{province_id}的开放报名站点")
        return json.dumps(stations_data, ensure_ascii=False, indent=2)
    except Exception as e:
        return str(e)



@mcp.tool
def get_next_stations(province_id: str) -> str:
    """
    获取指定省份即将开放报名的测试站点
    
    Args:
        province_id (str): 省份ID
        
    Returns:
        str: JSON格式的即将开放报名测试站点数据
    """
    try:
        url = f"https://psc.urabas.com/psc/api/stations/next?provinceId={province_id}"
        stations_data = fetch_api_data(url, f"省份{province_id}的即将开放报名站点")
        return json.dumps(stations_data, ensure_ascii=False, indent=2)
    except Exception as e:
        return str(e)

def main():
    """主函数，用于启动PSC MPC服务"""
    mcp.run(transport="http", port=8000)

if __name__ == "__main__":
    main()