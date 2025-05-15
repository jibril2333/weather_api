from flask import Flask, request, jsonify
from flask_cors import CORS

from services.weather import WeatherService
from services.ai_analysis import AIAnalysisService

app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests from frontend

# Initialize service instances
weather_service = WeatherService()
ai_service = AIAnalysisService()

@app.route("/weather", methods=["GET"])
def get_weather():
    """
    Weather data API endpoint
    
    Parameters:
        city (str): City name, passed as URL query parameter
        
    Returns:
        JSON: Weather data or error message
        Status code: 200 for success, 400 for request error, 500 for server error
    """
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
        
    data, status_code = weather_service.get_weather_data(city)
    return jsonify(data), status_code

@app.route("/ai/weather-analysis", methods=["POST"])
def ai_weather_analysis():
    """
    AI weather analysis API endpoint, supporting multi-round conversations
    
    Request body format (JSON):
        {
            "query": "user question",  # Required, user's analysis question
            "session_token": "xxx",  # Optional, session token to identify the same conversation
            "conversation_history": [...],  # Optional, previous conversation history
            "city": "city name"  # Optional, city name to get weather data
        }
        
    Returns:
        JSON: {
            "analysis": "AI analysis result",
            "session_token": "session token",
            "conversation_history": [...], # Updated conversation history
            "city": "city name"  # If city was included in the request
        }
        Status code: 200 for success, 400 for request error, 500 for server error
    """
    # Get JSON data from POST request body
    data = request.json
    
    if not data or not data.get("query"):
        return jsonify({"error": "Request missing required parameter: query"}), 400
    
    # Extract parameters
    user_query = data.get("query")
    session_token = data.get("session_token")
    conversation_history = data.get("conversation_history")
    city = data.get("city")
    
    result, status_code, session_token = ai_service.analyze_weather(
        user_query=user_query,
        conversation_history=conversation_history,
        session_token=session_token,
        city=city
    )
    
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True)
