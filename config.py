import os  # 导入os模块，用于访问环境变量
from dotenv import load_dotenv  # 导入dotenv，用于从.env文件加载环境变量

# 加载.env文件中的环境变量
# .env文件应包含敏感信息，如API密钥，且应被添加到.gitignore中
load_dotenv()

# API URLs - 各服务的API端点
# 地理编码API - 用于将城市名称转换为经纬度坐标
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
# 天气API - 用于获取天气预报数据
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
# OpenAI API - 用于AI分析天气数据
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# API密钥
# 从环境变量获取OpenAI API密钥，如果未设置则为空字符串
# 注意：使用此应用前必须设置此环境变量
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# 默认天气参数 - 指定从天气API获取的数据类型
# 逐小时天气参数 - 每小时的天气数据
DEFAULT_HOURLY_PARAMS = "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m"
# 逐日天气参数 - 每天的天气数据
DEFAULT_DAILY_PARAMS = "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code,sunrise,sunset"
# 当前天气参数 - 当前时刻的天气数据
DEFAULT_CURRENT_PARAMS = "temperature_2m,relative_humidity_2m,weather_code"
# 时区设置 - auto表示使用查询位置的本地时区
DEFAULT_TIMEZONE = "auto"

# OpenAI配置
# 使用的AI模型 - gpt-4o-mini是一个较为经济且性能良好的选择
DEFAULT_MODEL = "gpt-4o-mini"
# 温度参数 - 控制AI回答的随机性，值越低越确定性，值越高越创造性
DEFAULT_TEMPERATURE = 0.7 