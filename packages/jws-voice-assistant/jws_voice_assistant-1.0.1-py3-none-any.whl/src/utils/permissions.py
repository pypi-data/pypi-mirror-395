"""
权限管理模块
检查和管理系统权限
"""

import subprocess
import sys
from loguru import logger


def check_permissions() -> bool:
    """
    检查系统权限
    
    Returns:
        如果所有权限都已授予返回 True，否则返回 False
    """
    logger.info("🔐 正在检查系统权限...")
    
    permissions = {
        '辅助功能': check_accessibility_permission(),
        '屏幕录制': check_screen_recording_permission(),
        '麦克风': check_microphone_permission(),
    }
    
    all_granted = all(permissions.values())
    
    if not all_granted:
        logger.warning("⚠️ 以下权限未授予:")
        for name, granted in permissions.items():
            if not granted:
                logger.warning(f"  - {name}")
        logger.info("💡 请在 系统设置 > 隐私与安全性 中授予权限")
    
    return all_granted


def check_accessibility_permission() -> bool:
    """检查辅助功能权限"""
    try:
        # 尝试执行需要辅助功能权限的操作
        script = '''
        tell application "System Events"
            get name of every process
        end tell
        '''
        subprocess.run(['osascript', '-e', script], 
                      capture_output=True, 
                      check=True)
        return True
    except:
        return False


def check_screen_recording_permission() -> bool:
    """检查屏幕录制权限"""
    # macOS 屏幕录制权限检查比较复杂
    # 这里简化处理，实际使用时需要用户手动授予
    return True  # 暂时返回 True，实际使用时需要检查


def check_microphone_permission() -> bool:
    """检查麦克风权限"""
    try:
        # 尝试访问麦克风
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.1)
        return True
    except Exception as e:
        logger.debug(f"麦克风权限检查失败: {e}")
        return False


def request_permissions():
    """请求系统权限"""
    logger.info("📋 正在请求系统权限...")
    
    # 打开系统设置
    subprocess.run(['open', 'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility'])
    
    logger.info("请在系统设置中授予以下权限:")
    logger.info("  1. 辅助功能 - 控制其他应用")
    logger.info("  2. 屏幕录制 - GUI自动化")
    logger.info("  3. 麦克风 - 语音识别")

