from flask import Flask, request, jsonify  # 导入Flask框架核心组件
from flask_cors import CORS  # 导入CORS扩展，用于处理跨域资源共享
from dotenv import load_dotenv  # 导入dotenv，用于加载环境变量

# 导入服务层组件
from services.weather import WeatherService  # 导入天气服务，负责获取天气数据
from services.ai_analysis import AIAnalysisService  # 导入AI分析服务，负责分析天气数据

# 加载环境变量，从.env文件中读取配置
load_dotenv()

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 启用CORS，允许前端跨域访问API

# 初始化服务实例
weather_service = WeatherService()  # 创建天气服务实例
ai_service = AIAnalysisService()  # 创建AI分析服务实例

@app.route("/weather", methods=["GET"])
def get_weather():
    """
    获取天气数据API端点
    
    接收参数:
        city (str): 城市名称，通过URL查询参数传递
        
    返回:
        JSON: 天气数据或错误信息
        状态码: 200表示成功，400表示请求参数错误，500表示服务器错误
    """
    # 从请求参数中获取城市名称
    city = request.args.get("city")
    if not city:
        # 如果未提供城市参数，返回错误信息
        return jsonify({"error": "City parameter is required"}), 400
        
    # 调用天气服务获取数据
    # weather_service.get_weather_data会返回数据和状态码
    data, status_code = weather_service.get_weather_data(city)
    return jsonify(data), status_code

@app.route("/ai/weather-analysis", methods=["POST"])
def ai_weather_analysis():
    """
    AI天气分析API端点
    
    请求体格式(JSON):
        {
            "weather_data": {...},  # 天气数据对象
            "query": "用户问题"      # 用户想要分析的问题
        }
        
    返回:
        JSON: AI分析结果或错误信息
        状态码: 200表示成功，400表示请求参数错误，500表示服务器错误
    """
    # 从POST请求体中获取JSON数据
    data = request.json
    # 验证请求数据的完整性
    if not data or not data.get("weather_data") or not data.get("query"):
        return jsonify({"error": "请求缺少必要参数"}), 400
    
    # 提取天气数据和用户查询
    weather_data = data.get("weather_data")
    user_query = data.get("query")
    
    # 调用AI服务分析天气
    # ai_service.analyze_weather会返回分析结果和状态码
    result, status_code = ai_service.analyze_weather(weather_data, user_query)
    return jsonify(result), status_code

# 应用入口点
if __name__ == "__main__":
    # 启动Flask应用，debug=True表示开发模式，会自动重载代码
    app.run(debug=True)
