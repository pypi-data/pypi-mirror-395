"""
AI 助手模块
使用 Google Gemini 3 Pro 提供智能理解能力
"""

import os
import json
from typing import Dict, Optional, List
from loguru import logger

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai 未安装，将使用基础指令解析")


class AIAssistant:
    """AI 助手 - 使用 Gemini 3 Pro"""
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化 AI 助手"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = None
        self.available = False
        
        if not GEMINI_AVAILABLE:
            logger.warning("Gemini SDK 不可用，AI 功能将受限")
            return
        
        if not self.api_key:
            logger.warning("未设置 GEMINI_API_KEY，AI 功能将不可用")
            logger.info("💡 提示：设置环境变量 GEMINI_API_KEY 或创建 .env 文件")
            return
        
        try:
            genai.configure(api_key=self.api_key)
            # 使用 Gemini 1.5 Pro (最新可用版本)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            self.available = True
            logger.info("✅ Gemini AI 助手已初始化")
        except Exception as e:
            logger.error(f"初始化 Gemini AI 失败: {e}")
            self.available = False
    
    def understand_command(self, user_input: str, context: Optional[Dict] = None) -> Dict:
        """
        使用 AI 理解用户指令
        
        Args:
            user_input: 用户输入的文本
            context: 上下文信息（当前应用、系统状态等）
            
        Returns:
            解析后的指令字典
        """
        if not self.available:
            return {'action': 'unknown', 'params': {}, 'original_text': user_input}
        
        try:
            # 构建提示词
            system_prompt = self._build_system_prompt(context)
            user_prompt = f"用户说：{user_input}\n\n请分析这个指令，并返回 JSON 格式的指令。"
            
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            # 调用 Gemini API
            response = self.model.generate_content(full_prompt)
            
            # 解析响应
            result = self._parse_ai_response(response.text, user_input)
            logger.info(f"🤖 AI 理解结果: {result}")
            return result
            
        except Exception as e:
            logger.error(f"AI 理解失败: {e}")
            return {'action': 'unknown', 'params': {}, 'original_text': user_input}
    
    def _build_system_prompt(self, context: Optional[Dict] = None) -> str:
        """构建系统提示词"""
        prompt = """你是一个智能语音助手 Jws（类似钢铁侠的 JARVIS），具有以下能力：

1. **应用控制**：打开、切换、关闭应用
2. **系统控制**：锁屏、静音、音量控制、关机、重启等
3. **文件操作**：打开、创建、删除、执行文件
4. **GUI 自动化**：点击、输入、滚动、截图等
5. **命令执行**：运行终端命令、执行脚本

请将用户的自然语言指令转换为 JSON 格式：
{
    "action": "动作类型",
    "params": {
        "参数名": "参数值"
    },
    "confidence": 0.9,
    "description": "指令描述"
}

可用动作类型：
- open_app: 打开应用
- switch_app: 切换应用
- system_command: 系统命令（lock_screen, mute, unmute, shutdown, restart等）
- file_operation: 文件操作（open, create, delete, execute）
- gui_action: GUI 操作（click, type, scroll, screenshot）
- shell_command: 执行 Shell 命令
- custom_action: 自定义复杂操作

请根据用户指令智能判断意图，并返回最合适的动作类型和参数。"""
        
        if context:
            prompt += f"\n\n当前上下文：{json.dumps(context, ensure_ascii=False)}"
        
        return prompt
    
    def _parse_ai_response(self, response_text: str, original_input: str) -> Dict:
        """解析 AI 响应"""
        try:
            # 尝试提取 JSON
            import re
            json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                result = json.loads(json_str)
                result['original_text'] = original_input
                return result
        except Exception as e:
            logger.warning(f"解析 AI 响应失败: {e}")
        
        # 如果解析失败，返回基础结构
        return {
            'action': 'unknown',
            'params': {},
            'original_text': original_input,
            'ai_response': response_text
        }
    
    def generate_response(self, context: str) -> str:
        """
        生成对话响应
        
        Args:
            context: 上下文信息
            
        Returns:
            AI 生成的响应文本
        """
        if not self.available:
            return "抱歉，AI 功能暂时不可用"
        
        try:
            prompt = f"作为智能助手 Jws，请用友好、简洁的方式回复：{context}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"生成响应失败: {e}")
            return "抱歉，我无法生成回复"


