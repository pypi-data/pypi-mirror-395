#!/usr/bin/env python3
"""
Jws - 智能语音助手系统
主程序入口
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.voice_recognition import VoiceRecognition
from src.core.command_parser import CommandParser
from src.core.system_controller import SystemController
from src.core.app_controller import AppController
from src.core.ai_assistant import AIAssistant
from src.core.gui_automation import GUIAutomation
from src.utils.permissions import check_permissions
from src.utils.status_display import show_running_status, show_stopped_status
from loguru import logger
import json
import os
import time
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Jws:
    """Jws 主类 - 智能语音助手系统"""
    
    def __init__(self):
        """初始化 Jws 系统"""
        logger.info("🤖 正在启动 Jws 系统...")
        
        # 检查系统权限
        if not check_permissions():
            logger.error("❌ 系统权限检查失败，请授予必要权限")
            sys.exit(1)
        
        # 先加载配置（AppController 需要配置）
        self.load_config()
        
        # 初始化核心模块
        logger.info("📦 正在初始化核心模块...")
        self.voice_recognition = VoiceRecognition()
        self.command_parser = CommandParser()
        self.system_controller = SystemController()
        self.app_controller = AppController(config=self.config)
        
        # 初始化 AI 助手（Gemini 3 Pro）
        logger.info("🧠 正在初始化 AI 助手（Gemini 3 Pro）...")
        gemini_key = os.getenv('GEMINI_API_KEY') or self.config.get('gemini_api_key')
        self.ai_assistant = AIAssistant(api_key=gemini_key)
        
        # 初始化 GUI 自动化
        logger.info("🖱️ 正在初始化 GUI 自动化...")
        self.gui_automation = GUIAutomation()
        
        logger.info("✅ Jws 系统启动成功！")
        logger.info("🎤 请开始说话，我会执行你的指令...")
        
        # 显示运行状态
        self.status_window = show_running_status()
    
    def load_config(self):
        """加载配置文件"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'config',
            'settings.json'
        )
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            # 默认配置
            self.config = {
                "wake_word": "jws",
                "language": "zh-CN",
                "tts_enabled": True,
                "log_level": "INFO"
            }
            logger.warning("使用默认配置")
    
    def check_wake_word(self, text: str) -> bool:
        """
        检查是否包含唤醒词
        
        Args:
            text: 识别的文本
            
        Returns:
            如果包含唤醒词返回 True
        """
        if not text:
            return False
        
        text_lower = text.lower().strip()
        
        # 从配置中获取唤醒词列表
        wake_words = self.config.get('wake_words', [
            "贾维斯你好",
            "jws你好",
            "jws 你好",
            "贾维斯",
            "你好贾维斯",
            "你好 jws"
        ])
        
        # 也检查默认唤醒词
        default_wake_word = self.config.get('wake_word', 'jws')
        if default_wake_word:
            wake_words.append(f"{default_wake_word}你好")
            wake_words.append(default_wake_word)
        
        for wake_word in wake_words:
            if wake_word.lower() in text_lower:
                logger.info(f"🔔 检测到唤醒词: {wake_word}")
                return True
        
        return False
    
    def listen_and_execute(self):
        """监听语音并执行指令"""
        try:
            wake_word_mode = self.config.get('wake_word_enabled', True)
            is_awake = not wake_word_mode  # 如果禁用唤醒词，则始终处于唤醒状态
            
            while True:
                # 监听语音输入
                if is_awake:
                    logger.info("🎤 正在监听（已唤醒）...")
                else:
                    logger.info("🎤 正在监听（等待唤醒词）...")
                
                text = self.voice_recognition.listen()
                
                if not text:
                    continue
                
                logger.info(f"👂 听到: {text}")
                
                # 检查唤醒词
                if wake_word_mode and not is_awake:
                    if self.check_wake_word(text):
                        is_awake = True
                        logger.info("✅ 已唤醒，请说出你的指令")
                        if self.config.get('tts_enabled', True):
                            self.voice_recognition.speak("你好，我在")
                        continue
                    else:
                        # 未检测到唤醒词，继续监听
                        continue
                
                # 如果听到"再见"或"停止"，退出唤醒状态
                if wake_word_mode and is_awake:
                    if any(word in text.lower() for word in ["再见", "停止", "退出", "休息"]):
                        is_awake = False
                        logger.info("😴 已进入待机模式，等待唤醒词")
                        if self.config.get('tts_enabled', True):
                            self.voice_recognition.speak("好的，再见")
                        continue
                
                # 解析指令
                command = self.command_parser.parse(text)
                
                if command:
                    # 执行指令
                    logger.info(f"⚡ 执行指令: {command['action']}")
                    result = self.execute_command(command)
                    
                    # 语音反馈
                    if self.config.get('tts_enabled', True) and result:
                        self.voice_recognition.speak(result)
                else:
                    logger.warning("⚠️ 无法理解指令")
                    if self.config.get('tts_enabled', True):
                        self.voice_recognition.speak("抱歉，我没有理解你的指令")
        
        except KeyboardInterrupt:
            logger.info("👋 Jws 系统正在关闭...")
            if hasattr(self, 'status_window'):
                self.status_window.close()
            show_stopped_status()
        except Exception as e:
            logger.error(f"❌ 发生错误: {e}")
            if hasattr(self, 'status_window'):
                self.status_window.close()
            show_stopped_status()
            raise
    
    def execute_command(self, command):
        """执行指令（具有最高权限）"""
        action = command.get('action')
        params = command.get('params', {})
        
        try:
            if action == 'open_app':
                return self.app_controller.open_app(params.get('app_name'))
            
            elif action == 'close_app':
                return self.app_controller.close_app(params.get('app_name'))
            
            elif action == 'switch_app':
                return self.app_controller.switch_app(params.get('app_name'))
            
            elif action == 'system_command':
                cmd = params.get('command')
                if cmd in ['lock_screen', 'mute', 'unmute', 'shutdown', 'restart']:
                    return self.system_controller.execute(cmd)
                else:
                    return self.system_controller.execute(cmd)
            
            elif action == 'file_operation':
                return self.system_controller.file_operation(
                    params.get('operation'),
                    params.get('path'),
                    params.get('content')
                )
            
            elif action == 'gui_action':
                return self._execute_gui_action(params)
            
            elif action == 'shell_command':
                return self.system_controller.execute_shell_command(
                    params.get('command'),
                    params.get('timeout', 30)
                )
            
            elif action == 'custom_action':
                # 自定义复杂操作，由 AI 生成执行计划
                return self._execute_custom_action(params)
            
            else:
                return f"未知指令: {action}"
        
        except Exception as e:
            logger.error(f"执行指令失败: {e}")
            return f"执行失败: {str(e)}"
    
    def _execute_gui_action(self, params: dict) -> str:
        """执行 GUI 操作"""
        gui_action = params.get('action')
        
        if gui_action == 'click':
            return self.gui_automation.click(
                params.get('x'),
                params.get('y'),
                params.get('button', 'left'),
                params.get('clicks', 1)
            )
        elif gui_action == 'double_click':
            return self.gui_automation.double_click(
                params.get('x'),
                params.get('y')
            )
        elif gui_action == 'right_click':
            return self.gui_automation.right_click(
                params.get('x'),
                params.get('y')
            )
        elif gui_action == 'type':
            return self.gui_automation.type_text(params.get('text', ''))
        elif gui_action == 'press_key':
            keys = params.get('keys', [])
            return self.gui_automation.press_key(*keys)
        elif gui_action == 'scroll':
            return self.gui_automation.scroll(
                params.get('x'),
                params.get('y'),
                params.get('clicks', 3),
                params.get('direction', 'down')
            )
        elif gui_action == 'move_mouse':
            return self.gui_automation.move_mouse(
                params.get('x'),
                params.get('y'),
                params.get('duration', 0.5)
            )
        elif gui_action == 'screenshot':
            return self.gui_automation.screenshot(params.get('filename'))
        elif gui_action == 'click_image':
            return self.gui_automation.click_image(
                params.get('image_path'),
                params.get('confidence', 0.8)
            )
        else:
            return f"未知的 GUI 操作: {gui_action}"
    
    def _execute_custom_action(self, params: dict) -> str:
        """执行自定义复杂操作"""
        action_type = params.get('type')
        description = params.get('description', '')
        
        logger.info(f"执行自定义操作: {description}")
        
        # 这里可以根据 AI 生成的执行计划执行复杂操作
        # 例如：打开应用 -> 点击按钮 -> 输入文本 -> 保存
        
        steps = params.get('steps', [])
        results = []
        
        for step in steps:
            step_result = self.execute_command(step)
            results.append(step_result)
            time.sleep(0.5)  # 步骤间延迟
        
        return f"自定义操作完成:\n" + "\n".join(results)


def main():
    """主函数"""
    # 配置日志
    logger.add(
        "logs/jws_{time}.log",
        rotation="1 day",
        retention="7 days",
        level="INFO"
    )
    
    # 创建并启动 Jws
    jws = Jws()
    jws.listen_and_execute()


if __name__ == "__main__":
    main()

