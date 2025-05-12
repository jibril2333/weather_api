from services.util.api_utils import make_api_request  # 导入API请求工具函数
import config  # 导入配置文件

class AIAnalysisService:
    """
    AI分析服务类，用于处理天气数据智能分析
    
    主要功能:
    1. 将天气数据和用户查询发送到OpenAI API
    2. 获取并处理AI分析结果
    3. 提供结构化的天气数据分析
    """
    
    def __init__(self):
        """
        初始化AI分析服务
        
        设置OpenAI API的密钥、URL和模型参数，这些值定义在config.py中
        """
        self.api_key = config.OPENAI_API_KEY      # OpenAI API密钥
        self.api_url = config.OPENAI_API_URL      # OpenAI API端点URL
        self.model = config.DEFAULT_MODEL         # 使用的AI模型，如gpt-4o-mini
    
    def analyze_weather(self, weather_data, user_query):
        """
        使用OpenAI API分析天气数据并回答用户问题
        
        工作流程:
        1. 验证API密钥是否已配置
        2. 构建发送给OpenAI的请求消息
        3. 发送请求到OpenAI API
        4. 解析并返回AI回答
        
        Args:
            weather_data (dict): 天气数据，包含温度、湿度、降水等信息的字典
            user_query (str): 用户查询，例如"我需要带伞吗？"、"今天适合户外活动吗？"
            
        Returns:
            tuple: (分析结果或错误信息, HTTP状态码)
                成功: ({"analysis": "AI分析结果文本"}, 200)
                失败: ({"error": "错误信息"}, 错误状态码)
        """
        # 检查API密钥是否配置，这是调用OpenAI API的必要条件
        if not self.api_key:
            return {"error": "OpenAI API密钥未配置。请在环境变量中设置OPENAI_API_KEY"}, 500
        
        # 构建发送给OpenAI的系统和用户消息
        messages = [
            # 系统消息设置AI助手的角色和行为
            {"role": "system", "content": "你是一位天气分析专家，请根据提供的天气数据回答用户的问题。"},
            # 用户消息包含天气数据和具体查询
            {"role": "user", "content": f"基于以下天气数据:\n{str(weather_data)}\n\n用户问题: {user_query}"}
        ]
        
        # 设置API请求头，包含认证信息
        headers = {
            "Authorization": f"Bearer {self.api_key}",  # Bearer认证方式
            "Content-Type": "application/json"          # 内容类型为JSON
        }
        
        # 构建API请求体
        payload = {
            "model": self.model,                       # 使用的AI模型
            "messages": messages,                      # 对话消息
            "temperature": config.DEFAULT_TEMPERATURE  # 控制输出随机性的参数
        }
        
        try:
            # 发送POST请求到OpenAI API
            data, status_code = make_api_request(
                self.api_url,           # API端点URL
                headers=headers,        # 请求头
                method="POST",          # HTTP方法
                json_data=payload       # JSON格式的请求数据
            )
            
            if status_code == 200:
                # 从API响应中提取AI生成的文本
                ai_response = data["choices"][0]["message"]["content"]
                return {"analysis": ai_response}, 200
            else:
                # 如果请求不成功，直接返回API返回的错误信息
                return data, status_code
            
        except KeyError as e:
            # 处理API响应格式不符合预期的情况
            return {"error": f"OpenAI API响应解析失败: {str(e)}"}, 500
        except Exception as e:
            # 处理其他所有异常
            return {"error": f"处理请求时发生错误: {str(e)}"}, 500 