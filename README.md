# 天气API服务

这是一个提供天气数据和AI分析功能的RESTful API服务。

## 功能

- 通过城市名称获取天气数据
- 使用OpenAI API对天气数据进行智能分析
- 支持多种天气参数，包括温度、湿度、降水等

## 安装

1. 克隆仓库
```bash
git clone <仓库地址>
cd weather_api
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
创建一个.env文件，添加以下内容：
```
OPENAI_API_KEY=你的OpenAI_API密钥
```

4. 运行服务
```bash
python app.py
```

服务将在 http://localhost:5000 启动。

## 项目结构

```
weather_api/
├── app.py              # 主应用入口，路由定义
├── config.py           # 配置管理
├── services/           # 服务逻辑目录
│   ├── __init__.py
│   ├── weather.py      # 天气服务 (包含地理编码功能)
│   ├── ai_analysis.py  # AI分析服务
│   └── util/           # 工具函数
│       ├── __init__.py
│       └── api_utils.py # API请求工具
├── requirements.txt
└── README.md
```

## API 文档

### 获取天气数据

获取指定城市的天气数据。

**URL**: `/weather`
**方法**: GET
**参数**: 
- `city` (必填): 城市名称

**示例请求**:
```
GET /weather?city=beijing
```

**成功响应**:
```json
{
  "city_name": "beijing",
  "current": {
    "temperature_2m": 22.3,
    "relative_humidity_2m": 65,
    "weather_code": 1
  },
  "daily": {
    "temperature_2m_max": [25.6, 26.2, ...],
    "temperature_2m_min": [18.3, 19.1, ...],
    ...
  },
  "hourly": {
    "temperature_2m": [22.1, 23.4, ...],
    "relative_humidity_2m": [68, 65, ...],
    ...
  },
  ...
}
```

### AI天气分析

使用OpenAI API对天气数据进行智能分析。

**URL**: `/ai/weather-analysis`
**方法**: POST
**请求体**:
```json
{
  "weather_data": {
    "city": "shanghai",
    "temperature": 25.6,
    "humidity": 70,
    "forecast": [...]
  },
  "query": "明天的天气适合户外活动吗？"
}
```

**成功响应**:
```json
{
  "analysis": "根据天气数据，明天上海的气温约为26°C，湿度较高（70%），有轻微降水可能。虽然气温适宜，但因有降水可能，建议携带雨具进行户外活动，或选择有遮蔽的场所。"
}
```

## 错误处理

所有API都会返回适当的HTTP状态码和错误信息：

```json
{
  "error": "错误描述"
}
```

## 开发笔记

### 代码重构：从单文件到模块化架构

在项目初期，我们的天气API只包含获取城市天气数据的功能，将所有服务放在单个`app.py`文件中是合理且高效的做法。

随着项目的发展，我们添加了基于OpenAI的天气分析服务，使应用功能更加丰富。然而，随着代码量增加和功能复杂度提高，将所有服务维持在同一个文件中开始对后续开发和维护造成困难。因此，我们决定对代码进行重构。

重构过程中，我们考虑到地理编码功能与天气服务密切相关，不需要作为单独的服务暴露给用户。因此，我们将地理编码功能整合到了天气服务中，作为其内部功能使用。这样设计使API更加简洁，同时保持了模块化的代码结构。

重构后的项目组织结构更加清晰：
- 主应用入口(`app.py`)负责路由定义和请求处理
- 配置管理(`config.py`)集中管理所有配置参数
- 服务模块(`services/`)处理具体的业务逻辑
- 工具函数(`services/util/`)提供通用功能支持

这次重构提高了代码的可维护性和可扩展性，同时优化了API接口设计，使其更加符合RESTful原则。通过把相关功能组合在一起，我们减少了API的复杂度，提供了更好的用户体验。

## 许可证

[MIT](LICENSE) 