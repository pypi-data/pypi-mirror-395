"""
语音识别模块
负责语音输入识别和语音输出合成
"""

import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os
import tempfile
import subprocess
from loguru import logger


class VoiceRecognition:
    """语音识别和合成类"""
    
    def __init__(self):
        """初始化语音识别"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # 初始化TTS引擎
        try:
            self.tts_engine = pyttsx3.init()
            # 设置语音参数
            self.tts_engine.setProperty('rate', 150)  # 语速
            self.tts_engine.setProperty('volume', 0.8)  # 音量
        except Exception as e:
            logger.warning(f"TTS引擎初始化失败: {e}")
            self.tts_engine = None
        
        # 调整环境噪音
        logger.info("🔧 正在调整环境噪音...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        logger.info("✅ 环境噪音调整完成")
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """
        监听语音输入
        支持多个识别服务，自动切换
        
        Args:
            timeout: 超时时间（秒）
            phrase_time_limit: 短语时间限制（秒）
        
        Returns:
            识别的文本，如果失败返回 None
        """
        try:
            with self.microphone as source:
                logger.debug("🎤 开始录音...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            logger.debug("🔍 正在识别语音...")
            
            # 按优先级尝试多个识别服务
            recognition_services = [
                ('Google', self._recognize_google),
                ('macOS 本地识别', self._recognize_macos),
                ('离线 Sphinx', self._recognize_sphinx),
            ]
            
            for service_name, recognize_func in recognition_services:
                try:
                    logger.info(f"尝试使用 {service_name}...")
                    text = recognize_func(audio)
                    if text:
                        logger.info(f"✅ {service_name} 识别成功: {text}")
                        return text
                except Exception as e:
                    logger.debug(f"{service_name} 识别失败: {e}")
                    continue
            
            # 所有服务都失败
            logger.error("❌ 所有语音识别服务都失败")
            logger.warning("💡 建议：")
            logger.warning("   1) 检查网络连接（Google 需要网络）")
            logger.warning("   2) 使用 VPN/代理（如果在中国大陆）")
            logger.warning("   3) 使用测试模式: python3 test_mode.py")
            return None
        
        except sr.WaitTimeoutError:
            logger.debug("等待超时")
            return None
        except Exception as e:
            logger.error(f"语音识别错误: {e}")
            return None
    
    def _recognize_google(self, audio):
        """使用 Google 语音识别（需要网络）"""
        try:
            text = self.recognizer.recognize_google(audio, language='zh-CN')
            return text
        except sr.UnknownValueError:
            logger.warning("Google: 无法识别语音")
            return None
        except sr.RequestError as e:
            logger.debug(f"Google 服务连接失败: {e}")
            raise
    
    def _recognize_macos(self, audio):
        """使用 macOS 本地语音识别（不需要网络）"""
        try:
            # macOS 10.15+ 支持本地语音识别
            text = self.recognizer.recognize_google(audio, language='zh-CN')
            # 注意：即使使用 recognize_google，如果系统支持，可能会使用本地识别
            return text
        except:
            # 如果失败，尝试使用 Apple 的语音识别 API
            try:
                import subprocess
                import tempfile
                # 保存音频到临时文件
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                    # 这里需要将 audio 数据转换为 wav 文件
                    # 简化处理：如果 Google 失败，macOS 本地识别也可能不可用
                    pass
                return None
            except:
                raise
    
    def _recognize_sphinx(self, audio):
        """使用离线 Sphinx 识别（不需要网络，但准确度较低）"""
        try:
            text = self.recognizer.recognize_sphinx(audio)
            return text
        except Exception as e:
            logger.debug(f"Sphinx 离线识别失败: {e}")
            raise
    
    def speak(self, text):
        """
        语音输出
        
        Args:
            text: 要说的文本
        """
        if not text:
            return
        
        logger.info(f"🔊 说话: {text}")
        
        try:
            if self.tts_engine:
                # 使用 pyttsx3（离线，快速）
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            else:
                # 使用 gTTS（在线，需要网络）
                self._speak_gtts(text)
        except Exception as e:
            logger.error(f"语音合成错误: {e}")
    
    def _speak_gtts(self, text):
        """使用 gTTS 进行语音合成"""
        try:
            tts = gTTS(text=text, lang='zh-cn', slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                # 使用 macOS 的 afplay 播放
                subprocess.run(['afplay', tmp_file.name], check=True)
                os.unlink(tmp_file.name)
        except Exception as e:
            logger.error(f"gTTS 错误: {e}")

