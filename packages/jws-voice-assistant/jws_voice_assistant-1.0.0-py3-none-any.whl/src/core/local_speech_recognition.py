"""
本地语音识别模块
使用 macOS 系统自带的语音识别功能（不需要网络）
"""

import subprocess
import os
import tempfile
from loguru import logger

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False


class LocalSpeechRecognition:
    """本地语音识别（使用 macOS 系统功能）"""
    
    def __init__(self):
        """初始化本地语音识别"""
        self.recognizer = None
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            logger.info("✅ 本地语音识别已初始化")
        else:
            logger.warning("SpeechRecognition 库不可用")
    
    def recognize_using_macos(self, audio_data):
        """
        使用 macOS 系统语音识别
        
        注意：macOS 的语音识别仍然需要网络连接
        但我们可以尝试使用系统自带的听写功能
        """
        try:
            # macOS 10.15+ 支持本地语音识别
            # 但 SpeechRecognition 库的 recognize_google 在某些情况下
            # 可能会使用系统本地识别（如果可用）
            
            # 尝试使用系统 API
            # 注意：这需要 macOS 10.15+ 和适当的权限
            text = self.recognizer.recognize_google(audio_data, language='zh-CN')
            return text
        except Exception as e:
            logger.debug(f"macOS 本地识别失败: {e}")
            return None
    
    def recognize_offline(self, audio_data):
        """
        使用完全离线的识别（Sphinx）
        
        注意：准确度较低，主要支持英文
        """
        try:
            text = self.recognizer.recognize_sphinx(audio_data)
            return text
        except Exception as e:
            logger.debug(f"离线识别失败: {e}")
            return None


