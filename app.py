from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)  # 允许跨域访问

# OpenAI API配置
# 从环境变量获取API密钥
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def get_coordinates(city_name):
    # 使用Open-Meteo Geocoding API替换简单映射
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,  # 只返回最匹配的结果
        "language": "en",
        "format": "json"
    }
    
    try:
        response = requests.get(geocoding_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("results") and len(data["results"]) > 0:
                result = data["results"][0]
                return (result["latitude"], result["longitude"])
        return None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
        
    coords = get_coordinates(city)
    if not coords:
        return jsonify({"error": "Could not find coordinates for the city"}), 400

    lat, lon = coords
    url = "https://api.open-meteo.com/v1/forecast"
    
    # 请求更完整的天气数据
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code,sunrise,sunset",
        "current": "temperature_2m,relative_humidity_2m,weather_code",
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather"}), 500

    # 返回完整的天气数据
    data = response.json()
    data["city_name"] = city
    return jsonify(data)

# 添加一个新的路由，专门用于获取坐标
@app.route("/geocode", methods=["GET"])
def geocode():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
        
    coords = get_coordinates(city)
    if not coords:
        return jsonify({"error": "Could not find coordinates for the city"}), 400
        
    lat, lon = coords
    return jsonify({
        "city": city,
        "latitude": lat,
        "longitude": lon
    })

# 添加OpenAI API服务路由
@app.route("/ai/weather-analysis", methods=["POST"])
def ai_weather_analysis():
    # 检查API密钥是否配置
    if not OPENAI_API_KEY:
        return jsonify({"error": "OpenAI API密钥未配置。请在环境变量中设置OPENAI_API_KEY"}), 500
    
    # 从请求中获取数据
    data = request.json
    if not data or not data.get("weather_data") or not data.get("query"):
        return jsonify({"error": "请求缺少必要参数"}), 400
    
    weather_data = data.get("weather_data")
    user_query = data.get("query")
    
    # 构建发送给OpenAI的消息
    messages = [
        {"role": "system", "content": "你是一位天气分析专家，请根据提供的天气数据回答用户的问题。"},
        {"role": "user", "content": f"基于以下天气数据:\n{str(weather_data)}\n\n用户问题: {user_query}"}
    ]
    
    # 设置API请求头和数据
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",  # 可根据需要更改模型
        "messages": messages,
        "temperature": 0.7
    }
    
    try:
        # 发送请求到OpenAI API
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # 如果请求失败，抛出异常
        
        # 解析响应
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]
        
        return jsonify({
            "analysis": ai_response
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"OpenAI API请求失败: {str(e)}"}), 500
    except KeyError as e:
        return jsonify({"error": f"OpenAI API响应解析失败: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"处理请求时发生错误: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
