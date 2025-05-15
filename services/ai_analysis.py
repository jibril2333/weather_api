from services.util.api_utils import make_api_request
from services.weather import WeatherService
import config
import uuid

class AIAnalysisService:
    """
    AI分析服务类，用于处理天气数据智能分析
    
    主要功能:
    1. 将天气数据和用户查询发送到OpenAI API
    2. 获取并处理AI分析结果
    3. 提供结构化的天气数据分析
    4. 支持基于会话令牌的多轮对话
    5. 支持通过城市名称自动获取天气数据
    """
    
    def __init__(self):
        """
        初始化AI分析服务
        
        设置OpenAI API的密钥、URL和模型参数，这些值定义在config.py中
        初始化天气服务
        """
        self.api_key = config.OPENAI_API_KEY
        self.api_url = config.OPENAI_API_URL
        self.model = config.DEFAULT_MODEL
        self.weather_service = WeatherService()
    
    def generate_session_token(self):
        """
        生成唯一的会话令牌
        
        Returns:
            str: 新生成的会话令牌
        """
        return str(uuid.uuid4())
    
    def analyze_weather(self, user_query=None, conversation_history=None, session_token=None, city=None):
        """
        智能天气分析服务，支持多种调用方式：
        1. 提供session_token和conversation_history继续已有对话
        2. 提供city获取该城市天气并开始新对话
        
        工作流程:
        1. 验证必要参数
        2. 根据参数组合决定行为模式
        3. 获取或构建天气数据
        4. 构建AI提示并发送请求
        5. 返回分析结果和会话状态
        
        Args:
            user_query (str, required): 用户查询内容
            conversation_history (list, optional): 已有对话历史
            session_token (str, optional): 会话令牌
            city (str, optional): 城市名称，用于获取天气数据
            
        Returns:
            tuple: (分析结果或错误信息, HTTP状态码, 会话令牌)
        """
        # 验证用户查询
        if not user_query:
            return {"error": "必须提供用户查询(query)参数"}, 400, session_token
        
        # 生成新会话令牌（如果不存在）
        if not session_token:
            session_token = self.generate_session_token()
        
        # 天气数据变量
        weather_data = None
        
        # 数据获取逻辑
        # 1. 如果有对话历史，直接继续对话
        if conversation_history:
            # 使用现有对话历史继续对话，不需要新的天气数据
            pass
        
        # 2. 如果没有对话历史但有城市，获取天气数据
        elif city:
            weather_data, status_code = self.weather_service.get_weather_data(city)
            if status_code != 200:
                return weather_data, status_code, session_token
        
        # 3. 如果既没有对话历史也没有城市，则无法继续
        else:
            return {"error": "必须提供city参数或有效的对话历史"}, 400, session_token
        
        # 构建AI提示并生成回答
        # 构建消息列表
        if not conversation_history:
            # 开始新对话，此时一定有city和weather_data
            system_content = f"你是一位天气分析专家，当前分析的是{city}的天气。请根据提供的天气数据回答用户的问题。"
            
            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": f"基于以下天气数据:\n{str(weather_data)}\n\n用户问题: {user_query}"}
            ]
        else:
            # 继续现有对话
            messages = conversation_history
            # 直接添加用户的新问题到对话中
            messages.append({"role": "user", "content": f"用户问题: {user_query}"})
        
        # 检查API密钥
        if not self.api_key:
            return {"error": "OpenAI API密钥未配置。请在环境变量中设置OPENAI_API_KEY"}, 500, session_token
        
        # 设置API请求
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": config.DEFAULT_TEMPERATURE
        }
        
        # 发送请求并处理响应
        try:
            data, status_code = make_api_request(
                self.api_url,
                headers=headers,
                method="POST",
                json_data=payload
            )
            
            if status_code == 200:
                # 提取AI回答
                ai_response = data["choices"][0]["message"]["content"]
                
                # 更新对话历史
                new_conversation_history = messages.copy()
                new_conversation_history.append({"role": "assistant", "content": ai_response})
                
                # 构建响应
                response = {
                    "analysis": ai_response,
                    "session_token": session_token,
                    "conversation_history": new_conversation_history
                }
                
                # 如果有城市信息，也一并返回
                if city:
                    response["city"] = city
                    
                return response, 200, session_token
            else:
                return {
                    "error": data.get("error", "未知错误"),
                    "session_token": session_token
                }, status_code, session_token
            
        except KeyError as e:
            return {
                "error": f"OpenAI API响应解析失败: {str(e)}",
                "session_token": session_token
            }, 500, session_token
        except Exception as e:
            return {
                "error": f"处理请求时发生错误: {str(e)}",
                "session_token": session_token
            }, 500, session_token 