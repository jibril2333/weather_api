from services.util.api_utils import make_api_request
import config

class WeatherService:
    """
    天气服务类，负责处理天气相关的API请求
    
    主要功能:
    1. 地理编码 - 将城市名称转换为经纬度坐标
    2. 天气查询 - 根据经纬度获取详细天气数据
    """
    
    def __init__(self):
        """
        初始化天气服务
        
        设置地理编码API和天气API的URL，这些URL定义在config.py中
        """
        self.geocoding_url = config.GEOCODING_API_URL
        self.weather_url = config.WEATHER_API_URL
    
    def get_coordinates(self, city_name):
        """
        获取城市的经纬度坐标
        
        工作流程:
        1. 构建地理编码API请求参数
        2. 发送请求到地理编码API
        3. 解析响应并提取坐标
        
        Args:
            city_name (str): 城市名称，例如 "Beijing"、"Tokyo"等
            
        Returns:
            tuple: (纬度, 经度) 如 (39.9075, 116.39723) 或 None（如果城市未找到）
        """
        params = {
            "name": city_name,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        try:
            data, status_code = make_api_request(self.geocoding_url, params=params)
            if status_code == 200 and data.get("results") and len(data["results"]) > 0:
                result = data["results"][0]
                return (result["latitude"], result["longitude"])
            return None
        except Exception as e:
            print(f"地理编码API请求错误: {e}")
            return None
    
    def get_weather_data(self, city_name):
        """
        通过城市名称获取天气数据
        
        工作流程:
        1. 调用get_coordinates获取城市坐标
        2. 构建天气API请求参数
        3. 发送请求到天气API
        4. 处理响应数据并返回
        
        Args:
            city_name (str): 城市名称，例如 "Shanghai"、"New York"等
            
        Returns:
            tuple: (天气数据字典, HTTP状态码)
                成功: ({"temperature": 25, ...}, 200)
                失败: ({"error": "错误信息"}, 错误状态码)
        """
        coords = self.get_coordinates(city_name)
        if not coords:
            return {"error": "无法找到该城市的坐标"}, 400

        lat, lon = coords
        
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": config.DEFAULT_HOURLY_PARAMS,
            "daily": config.DEFAULT_DAILY_PARAMS,
            "current": config.DEFAULT_CURRENT_PARAMS,
            "timezone": config.DEFAULT_TIMEZONE
        }

        try:
            data, status_code = make_api_request(self.weather_url, params=params)
            if status_code == 200:
                data["city_name"] = city_name
            return data, status_code
        except Exception as e:
            return {"error": f"获取天气数据失败: {str(e)}"}, 500 