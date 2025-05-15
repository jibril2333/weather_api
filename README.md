# 天气API服务

这是一个提供天气数据和AI分析功能的RESTful API服务，结合了开放天气数据和OpenAI大语言模型，支持多轮对话分析天气信息。

## 目录

- [功能特点](#功能特点)
- [快速开始](#快速开始)
  - [前提条件](#前提条件)
  - [安装步骤](#安装步骤)
  - [配置说明](#配置说明)
- [API文档](#api文档)
  - [获取天气数据](#获取天气数据)
  - [AI天气分析](#ai天气分析)
- [错误处理](#错误处理)
- [项目结构](#项目结构)
- [许可证](#许可证)

## 功能特点

- **天气数据获取**：通过城市名称获取实时和预报天气数据
- **AI智能分析**：使用OpenAI API对天气数据进行自然语言分析
- **多轮对话支持**：通过会话令牌维持对话上下文，提供连贯的交互体验
- **无状态设计**：基于会话令牌的无状态架构，易于扩展和部署
- **丰富的天气参数**：支持温度、湿度、降水、风速等多种天气指标

## 快速开始

### 前提条件

- Python 3.8+
- OpenAI API密钥
- 互联网连接（用于访问天气API和OpenAI API）

### 安装步骤

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
   ```bash
   # 创建.env文件并添加API密钥
   echo "OPENAI_API_KEY=你的OpenAI_API密钥" > .env
   ```

4. 启动服务
   ```bash
   python app.py
   ```

服务将在 http://localhost:5000 启动。

### 配置说明

主要配置项位于`config.py`文件中，包括：
- API端点URL
- 默认天气参数
- OpenAI模型设置
- 温度参数调整

## API文档

### 获取天气数据

获取指定城市的天气数据。

- **URL**: `/weather`
- **方法**: GET
- **参数**: 
  - `city` (必填): 城市名称

**示例请求**:
```
GET /weather?city=beijing
```

**成功响应** (200 OK):
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

使用OpenAI API对天气数据进行智能分析，支持多轮对话。

- **URL**: `/ai/weather-analysis`
- **方法**: POST
- **内容类型**: `application/json`

**请求体**:

1. 开始新对话:
```json
{
  "city": "shanghai",
  "query": "明天的天气适合户外活动吗？"
}
```

2. 继续已有对话:
```json
{
  "query": "我需要带伞吗？",
  "session_token": "550e8400-e29b-41d4-a716-446655440000",
  "conversation_history": [
    {"role": "system", "content": "你是一位天气分析专家，当前分析的是上海的天气。请根据提供的天气数据回答用户的问题。"},
    {"role": "user", "content": "基于以下天气数据:\n{'temperature': 25.6, 'humidity': 70, ...}\n\n用户问题: 明天的天气适合户外活动吗？"},
    {"role": "assistant", "content": "根据天气数据，明天上海的气温约为26°C，湿度较高（70%），有轻微降水可能。虽然气温适宜，但因有降水可能，建议携带雨具进行户外活动，或选择有遮蔽的场所。"}
  ]
}
```

**成功响应** (200 OK):

1. 开始新对话:
```json
{
  "analysis": "根据天气数据，明天上海的气温约为26°C，湿度较高（70%），有轻微降水可能。虽然气温适宜，但因有降水可能，建议携带雨具进行户外活动，或选择有遮蔽的场所。",
  "session_token": "550e8400-e29b-41d4-a716-446655440000",
  "conversation_history": [...],
  "city": "shanghai"
}
```

2. 继续对话:
```json
{
  "analysis": "是的，根据预报数据显示有降水可能，建议您带上雨伞以防万一。",
  "session_token": "550e8400-e29b-41d4-a716-446655440000",
  "conversation_history": [...]
}
```

## 错误处理

所有API都会返回适当的HTTP状态码和错误信息：

- **400 Bad Request**: 请求参数不完整或无效
- **404 Not Found**: 资源未找到
- **500 Internal Server Error**: 服务器内部错误

错误响应格式：
```json
{
  "error": "错误描述"
}
```

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
├── requirements.txt    # 项目依赖
├── README.md           # 项目文档
└── DEVELOPMENT_NOTES.md # 开发笔记
```

## 许可证

[MIT](LICENSE) 