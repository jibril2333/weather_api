import requests  # 导入requests库，用于发送HTTP请求
from typing import Dict, Any, Tuple, Optional  # 导入类型提示相关类型

def make_api_request(url: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None, 
                    method: str = "GET", json_data: Dict[str, Any] = None) -> Tuple[Dict[str, Any], int]:
    """
    通用API请求工具函数 - 封装HTTP请求的发送和错误处理
    
    该函数统一处理项目中所有的API请求，提供以下功能：
    1. 支持GET和POST请求方法
    2. 自动处理各种异常情况
    3. 统一的返回格式，包含数据和状态码
    4. 支持URL参数、请求头和JSON请求体
    
    Args:
        url (str): API端点URL，如 "https://api.example.com/v1/data"
        params (Dict[str, Any], optional): URL查询参数，将被添加到URL后面. 默认为None.
            例如: {"q": "Beijing", "units": "metric"}
        headers (Dict[str, str], optional): HTTP请求头. 默认为None.
            例如: {"Authorization": "Bearer token123", "Content-Type": "application/json"}
        method (str, optional): HTTP请求方法，支持"GET"或"POST". 默认为"GET".
        json_data (Dict[str, Any], optional): POST请求的JSON请求体. 默认为None.
            例如: {"name": "测试", "value": 123}
        
    Returns:
        Tuple[Dict[str, Any], int]: 包含两个元素的元组:
            1. 响应数据（JSON解析后的字典）
            2. HTTP状态码
            
            成功示例: ({"temperature": 25, "humidity": 60}, 200)
            失败示例: ({"error": "API请求失败: 连接超时"}, 500)
    
    Raises:
        不抛出异常，所有异常都在函数内部被捕获并转换为错误响应
    """
    try:
        # 根据请求方法选择不同的处理方式
        if method.upper() == "GET":
            # 发送GET请求
            response = requests.get(url, params=params, headers=headers)
        elif method.upper() == "POST":
            # 发送POST请求，支持JSON请求体
            response = requests.post(url, params=params, headers=headers, json=json_data)
        else:
            # 不支持的HTTP方法，返回错误信息
            return {"error": f"不支持的HTTP方法: {method}"}, 400
            
        # 检查HTTP状态码，如果不是2xx，抛出异常
        response.raise_for_status()
        # 将响应内容解析为JSON并返回，同时返回状态码
        return response.json(), response.status_code
        
    except requests.exceptions.RequestException as e:
        # 处理所有requests相关异常
        # 包括连接错误、超时、HTTP错误等
        return {"error": f"API请求失败: {str(e)}"}, 500
    except ValueError as e:
        # 处理JSON解析错误
        # 当响应内容不是有效的JSON格式时
        return {"error": f"JSON解析失败: {str(e)}"}, 500
    except Exception as e:
        # 处理所有其他未预期的异常
        return {"error": f"请求处理过程中发生错误: {str(e)}"}, 500 