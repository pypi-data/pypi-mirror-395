"""
状态显示模块
在 Jws 运行时显示状态提示
"""

import subprocess
import threading
from loguru import logger

try:
    import tkinter as tk
    from tkinter import ttk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    logger.warning("tkinter 不可用，将使用通知方式显示状态")


def show_notification(title: str, message: str, sound: bool = True):
    """
    显示 macOS 通知
    
    Args:
        title: 通知标题
        message: 通知内容
        sound: 是否播放声音
    """
    try:
        # 使用 osascript 显示通知
        script = f'''
        display notification "{message}" with title "{title}"'''
        if sound:
            script += ' sound name "Glass"'
        
        subprocess.run(['osascript', '-e', script], check=False)
        logger.info(f"📢 已显示通知: {title} - {message}")
    except Exception as e:
        logger.error(f"显示通知失败: {e}")


class StatusWindow:
    """状态窗口类"""
    
    def __init__(self):
        """初始化状态窗口"""
        self.window = None
        self.running = True
        
        if TKINTER_AVAILABLE:
            self._create_window()
        else:
            logger.warning("tkinter 不可用，无法创建状态窗口")
    
    def _create_window(self):
        """创建状态窗口"""
        try:
            self.window = tk.Tk()
            self.window.title("Jws 状态")
            self.window.geometry("350x200")
            self.window.resizable(False, False)
            
            # 设置窗口始终置顶
            self.window.attributes('-topmost', True)
            
            # 设置窗口样式
            style = ttk.Style()
            style.theme_use('clam')
            
            # 主框架
            main_frame = ttk.Frame(self.window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # 标题
            title_label = ttk.Label(
                main_frame,
                text="🤖 Jws 智能语音助手",
                font=("Helvetica", 16, "bold")
            )
            title_label.pack(pady=(0, 10))
            
            # 状态标签
            self.status_label = ttk.Label(
                main_frame,
                text="✅ 正在运行中...",
                font=("Helvetica", 12),
                foreground="green"
            )
            self.status_label.pack(pady=5)
            
            # 提示文本
            info_label = ttk.Label(
                main_frame,
                text="🎤 正在监听你的语音指令\n直接说话即可，无需唤醒词",
                font=("Helvetica", 10),
                justify=tk.CENTER,
                foreground="gray"
            )
            info_label.pack(pady=10)
            
            # 状态指示器（动态点）
            self.indicator_label = ttk.Label(
                main_frame,
                text="●",
                font=("Helvetica", 20),
                foreground="green"
            )
            self.indicator_label.pack(pady=5)
            
            # 启动闪烁动画
            self._animate_indicator()
            
            # 窗口关闭事件
            self.window.protocol("WM_DELETE_WINDOW", self._on_close)
            
            logger.info("✅ 状态窗口已创建")
            
        except Exception as e:
            logger.error(f"创建状态窗口失败: {e}")
            self.window = None
    
    def _animate_indicator(self):
        """动画指示器"""
        if not self.window or not self.running:
            return
        
        try:
            current_color = self.indicator_label.cget("foreground")
            if current_color == "green":
                self.indicator_label.config(foreground="#90EE90")  # 浅绿色
            else:
                self.indicator_label.config(foreground="green")
            
            self.window.after(500, self._animate_indicator)
        except:
            pass
    
    def _on_close(self):
        """窗口关闭事件"""
        logger.info("用户关闭了状态窗口")
        self.running = False
        if self.window:
            self.window.destroy()
    
    def show(self):
        """显示窗口"""
        if self.window:
            try:
                # 在新线程中运行窗口
                def run_window():
                    self.window.mainloop()
                
                thread = threading.Thread(target=run_window, daemon=True)
                thread.start()
                logger.info("状态窗口已显示")
            except Exception as e:
                logger.error(f"显示窗口失败: {e}")
    
    def update_status(self, status: str, color: str = "green"):
        """更新状态文本"""
        if self.window and self.status_label:
            try:
                self.status_label.config(text=status, foreground=color)
            except:
                pass
    
    def close(self):
        """关闭窗口"""
        self.running = False
        if self.window:
            try:
                self.window.quit()
                self.window.destroy()
            except:
                pass


def show_running_status():
    """
    显示 Jws 正在运行的状态
    包括通知和状态窗口
    """
    # 显示通知
    show_notification(
        title="🤖 Jws 已启动",
        message="智能语音助手正在运行，正在监听你的语音指令",
        sound=True
    )
    
    # 创建并显示状态窗口
    status_window = StatusWindow()
    status_window.show()
    
    return status_window


def show_stopped_status():
    """显示 Jws 已停止的状态"""
    show_notification(
        title="👋 Jws 已停止",
        message="智能语音助手已关闭",
        sound=False
    )

