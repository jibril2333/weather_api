from services.util.api_utils import make_api_request
import config

class WeatherService:
    """
    Weather service class, responsible for handling weather-related API requests
    
    Main functions:
    1. Geocoding - Converting city names to latitude and longitude coordinates
    2. Weather data retrieval - Getting detailed weather data based on coordinates
    """
    
    def __init__(self):
        """
        Initialize the weather service
        
        Set up geocoding API and weather API URLs, which are defined in config.py
        """
        self.geocoding_url = config.GEOCODING_API_URL
        self.weather_url = config.WEATHER_API_URL
    
    def get_coordinates(self, city_name):
        """
        Get latitude and longitude coordinates for a city
        
        Workflow:
        1. Build geocoding API request parameters
        2. Send request to the geocoding API
        3. Parse response and extract coordinates
        
        Note: Currently only supports English city names
        
        Args:
            city_name (str): City name, e.g., "Shanghai", "Tokyo", etc.
            
        Returns:
            tuple: (latitude, longitude) like (39.9075, 116.39723) or None (if city not found)
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
            print(f"Geocoding API request error: {e}")
            return None
    
    def get_weather_data(self, city_name):
        """
        Get weather data through city name
        
        Workflow:
        1. Call get_coordinates to obtain city coordinates
        2. Build weather API request parameters
        3. Send request to the weather API
        4. Process response data and return
        
        Args:
            city_name (str): City name, e.g., "Shanghai", "New York", etc.
            
        Returns:
            tuple: (Weather data dictionary, HTTP status code)
                Success: ({"temperature": 25, ...}, 200)
                Failure: ({"error": "error message"}, error status code)
        """
        coords = self.get_coordinates(city_name)
        if not coords:
            return {"error": "Could not find coordinates for the city"}, 400

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
            return {"error": f"Failed to get weather data: {str(e)}"}, 500 