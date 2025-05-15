import os
from dotenv import load_dotenv

load_dotenv()

# URLs
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# API keys
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Default weather parameters - Specify the type of data to get from the weather API
# Hourly weather parameters - Weather data for each hour
DEFAULT_HOURLY_PARAMS = "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m"
# Daily weather parameters - Weather data for each day
DEFAULT_DAILY_PARAMS = "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code,sunrise,sunset"
# Current weather parameters - Weather data for the current moment
DEFAULT_CURRENT_PARAMS = "temperature_2m,relative_humidity_2m,weather_code"
# Timezone setting - 'auto' means using the local timezone of the query location
DEFAULT_TIMEZONE = "auto"

# OpenAI config
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.7 