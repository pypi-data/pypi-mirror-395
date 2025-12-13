"""
GUI 自动化模块
使用 PyAutoGUI 实现点击、输入、滚动等操作
"""

import time
import subprocess
from typing import Tuple, Optional, List
from loguru import logger

try:
    import pyautogui
    import pyperclip
    PYAUTOGUI_AVAILABLE = True
    # 设置安全模式，防止意外操作
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logger.warning("PyAutoGUI 不可用，GUI 自动化功能将受限")


class GUIAutomation:
    """GUI 自动化控制器"""
    
    def __init__(self):
        """初始化 GUI 自动化"""
        if not PYAUTOGUI_AVAILABLE:
            logger.warning("PyAutoGUI 不可用")
            return
        
        logger.info("🖱️ 初始化 GUI 自动化...")
        self.screen_width, self.screen_height = pyautogui.size()
        logger.info(f"屏幕尺寸: {self.screen_width}x{self.screen_height}")
    
    def click(self, x: Optional[int] = None, y: Optional[int] = None, 
              button: str = 'left', clicks: int = 1, interval: float = 0.1) -> str:
        """
        点击屏幕位置
        
        Args:
            x: X 坐标（None 表示当前鼠标位置）
            y: Y 坐标（None 表示当前鼠标位置）
            button: 鼠标按钮 ('left', 'right', 'middle')
            clicks: 点击次数
            interval: 点击间隔（秒）
            
        Returns:
            操作结果
        """
        if not PYAUTOGUI_AVAILABLE:
            return "GUI 自动化功能不可用"
        
        try:
            if x is None or y is None:
                # 点击当前鼠标位置
                pyautogui.click(button=button, clicks=clicks, interval=interval)
                return f"已在当前位置点击 {clicks} 次（{button}键）"
            else:
                # 验证坐标
                if not (0 <= x <= self.screen_width and 0 <= y <= self.screen_height):
                    return f"坐标超出屏幕范围: ({x}, {y})"
                
                pyautogui.click(x, y, button=button, clicks=clicks, interval=interval)
                return f"已点击位置 ({x}, {y}) {clicks} 次（{button}键）"
        except Exception as e:
            logger.error(f"点击操作失败: {e}")
            return f"点击失败: {str(e)}"
    
    def double_click(self, x: Optional[int] = None, y: Optional[int] = None) -> str:
        """双击"""
        return self.click(x, y, button='left', clicks=2)
    
    def right_click(self, x: Optional[int] = None, y: Optional[int] = None) -> str:
        """右键点击"""
        return self.click(x, y, button='right')
    
    def type_text(self, text: str, interval: float = 0.05) -> str:
        """
        输入文本
        
        Args:
            text: 要输入的文本
            interval: 字符输入间隔（秒）
            
        Returns:
            操作结果
        """
        if not PYAUTOGUI_AVAILABLE:
            return "GUI 自动化功能不可用"
        
        try:
            # 使用剪贴板处理中文和特殊字符
            pyperclip.copy(text)
            time.sleep(0.1)
            pyautogui.hotkey('command', 'v')
            time.sleep(0.1)
            return f"已输入文本: {text[:50]}{'...' if len(text) > 50 else ''}"
        except Exception as e:
            logger.error(f"输入文本失败: {e}")
            return f"输入失败: {str(e)}"
    
    def press_key(self, *keys: str) -> str:
        """
        按下键盘按键
        
        Args:
            *keys: 按键名称（支持组合键，如 'command', 'c'）
            
        Returns:
            操作结果
        """
        if not PYAUTOGUI_AVAILABLE:
            return "GUI 自动化功能不可用"
        
        try:
            pyautogui.hotkey(*keys)
            keys_str = '+'.join(keys)
            return f"已按下按键: {keys_str}"
        except Exception as e:
            logger.error(f"按键操作失败: {e}")
            return f"按键失败: {str(e)}"
    
    def scroll(self, x: Optional[int] = None, y: Optional[int] = None, 
               clicks: int = 3, direction: str = 'down') -> str:
        """
        滚动
        
        Args:
            x: X 坐标（None 表示屏幕中心）
            y: Y 坐标（None 表示屏幕中心）
            clicks: 滚动次数（正数向下，负数向上）
            direction: 方向 ('up', 'down')
            
        Returns:
            操作结果
        """
        if not PYAUTOGUI_AVAILABLE:
            return "GUI 自动化功能不可用"
        
        try:
            if x is None:
                x = self.screen_width // 2
            if y is None:
                y = self.screen_height // 2
            
            scroll_amount = clicks if direction == 'down' else -clicks
            pyautogui.scroll(scroll_amount, x=x, y=y)
            return f"已滚动 {abs(clicks)} 次（{direction}）"
        except Exception as e:
            logger.error(f"滚动操作失败: {e}")
            return f"滚动失败: {str(e)}"
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> str:
        """
        移动鼠标
        
        Args:
            x: 目标 X 坐标
            y: 目标 Y 坐标
            duration: 移动时间（秒）
            
        Returns:
            操作结果
        """
        if not PYAUTOGUI_AVAILABLE:
            return "GUI 自动化功能不可用"
        
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return f"鼠标已移动到 ({x}, {y})"
        except Exception as e:
            logger.error(f"移动鼠标失败: {e}")
            return f"移动失败: {str(e)}"
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """获取当前鼠标位置"""
        if not PYAUTOGUI_AVAILABLE:
            return (0, 0)
        return pyautogui.position()
    
    def screenshot(self, filename: Optional[str] = None) -> str:
        """
        截图
        
        Args:
            filename: 保存的文件名（None 表示自动生成）
            
        Returns:
            操作结果
        """
        if not PYAUTOGUI_AVAILABLE:
            return "GUI 自动化功能不可用"
        
        try:
            if filename is None:
                import datetime
                filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            return f"截图已保存: {filename}"
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return f"截图失败: {str(e)}"
    
    def find_image(self, image_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        """
        在屏幕上查找图像
        
        Args:
            image_path: 图像文件路径
            confidence: 匹配置信度
            
        Returns:
            找到的位置 (x, y)，未找到返回 None
        """
        if not PYAUTOGUI_AVAILABLE:
            return None
        
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                return center
            return None
        except Exception as e:
            logger.error(f"查找图像失败: {e}")
            return None
    
    def click_image(self, image_path: str, confidence: float = 0.8) -> str:
        """
        查找并点击图像
        
        Args:
            image_path: 图像文件路径
            confidence: 匹配置信度
            
        Returns:
            操作结果
        """
        location = self.find_image(image_path, confidence)
        if location:
            return self.click(location[0], location[1])
        return f"未找到图像: {image_path}"

