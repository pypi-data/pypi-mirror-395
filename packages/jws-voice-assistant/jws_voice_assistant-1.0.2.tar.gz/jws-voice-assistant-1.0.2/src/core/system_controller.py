"""
系统控制模块
负责执行系统级别的操作
具有最高权限，可以执行所有系统命令和文件
"""

import subprocess
import os
import stat
import sys
from typing import Optional
from loguru import logger


class SystemController:
    """系统控制器"""
    
    def __init__(self):
        """初始化系统控制器"""
        logger.info("🔧 初始化系统控制器...")
    
    def execute(self, command: str) -> str:
        """
        执行系统命令
        
        Args:
            command: 系统命令
        
        Returns:
            执行结果
        """
        try:
            logger.info(f"⚡ 执行系统命令: {command}")
            
            if command == '关机':
                return self.shutdown()
            elif command == '重启':
                return self.restart()
            elif command == '锁屏':
                return self.lock_screen()
            elif command == '静音':
                return self.mute()
            elif command == '取消静音':
                return self.unmute()
            else:
                return f"未知的系统命令: {command}"
        
        except Exception as e:
            logger.error(f"执行系统命令失败: {e}")
            return f"执行失败: {str(e)}"
    
    def shutdown(self) -> str:
        """关机"""
        subprocess.run(['osascript', '-e', 'tell app "System Events" to shut down'])
        return "正在关机..."
    
    def restart(self) -> str:
        """重启"""
        subprocess.run(['osascript', '-e', 'tell app "System Events" to restart'])
        return "正在重启..."
    
    def lock_screen(self) -> str:
        """锁屏"""
        subprocess.run(['pmset', 'displaysleepnow'])
        return "屏幕已锁定"
    
    def mute(self) -> str:
        """静音"""
        subprocess.run(['osascript', '-e', 'set volume output muted true'])
        return "已静音"
    
    def unmute(self) -> str:
        """取消静音"""
        subprocess.run(['osascript', '-e', 'set volume output muted false'])
        return "已取消静音"
    
    def file_operation(self, operation: str, path: str, content: Optional[str] = None) -> str:
        """
        文件操作（具有最高权限）
        
        Args:
            operation: 操作类型 (open/create/delete/execute/read/write)
            path: 文件路径
            content: 文件内容（用于 write 操作）
        
        Returns:
            操作结果
        """
        try:
            # 展开路径
            path = os.path.expanduser(path)
            path = os.path.abspath(path)
            
            if operation == 'open':
                # 打开文件或目录
                subprocess.run(['open', path], check=False)
                return f"已打开: {path}"
            
            elif operation == 'create':
                # 创建文件或目录
                if path.endswith('/') or os.path.isdir(os.path.dirname(path)):
                    # 创建目录
                    os.makedirs(path, exist_ok=True)
                    return f"已创建目录: {path}"
                else:
                    # 创建文件
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content or '')
                    return f"已创建文件: {path}"
            
            elif operation == 'delete':
                # 删除文件或目录
                if os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path)
                    return f"已删除目录: {path}"
                else:
                    os.remove(path)
                    return f"已删除文件: {path}"
            
            elif operation == 'execute':
                # 执行文件（具有最高权限）
                return self.execute_file(path)
            
            elif operation == 'read':
                # 读取文件
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return f"文件内容:\n{content[:500]}{'...' if len(content) > 500 else ''}"
            
            elif operation == 'write':
                # 写入文件
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content or '')
                return f"已写入文件: {path}"
            
            else:
                return f"未知的文件操作: {operation}"
        
        except Exception as e:
            logger.error(f"文件操作失败: {e}")
            return f"操作失败: {str(e)}"
    
    def execute_file(self, file_path: str) -> str:
        """
        执行文件（具有最高权限）
        
        Args:
            file_path: 文件路径
            
        Returns:
            执行结果
        """
        try:
            file_path = os.path.expanduser(file_path)
            file_path = os.path.abspath(file_path)
            
            if not os.path.exists(file_path):
                return f"文件不存在: {file_path}"
            
            # 检查文件类型
            if file_path.endswith('.py'):
                # Python 脚本
                result = subprocess.run(
                    [sys.executable, file_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                output = result.stdout + result.stderr
                return f"执行完成:\n{output[:500]}"
            
            elif file_path.endswith('.sh'):
                # Shell 脚本
                os.chmod(file_path, stat.S_IRWXU)  # 添加执行权限
                result = subprocess.run(
                    ['bash', file_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                output = result.stdout + result.stderr
                return f"执行完成:\n{output[:500]}"
            
            elif file_path.endswith('.app'):
                # macOS 应用
                subprocess.run(['open', file_path])
                return f"已启动应用: {file_path}"
            
            else:
                # 尝试直接执行
                os.chmod(file_path, stat.S_IRWXU)
                result = subprocess.run(
                    [file_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                output = result.stdout + result.stderr
                return f"执行完成:\n{output[:500]}"
        
        except subprocess.TimeoutExpired:
            return "执行超时（30秒）"
        except Exception as e:
            logger.error(f"执行文件失败: {e}")
            return f"执行失败: {str(e)}"
    
    def execute_shell_command(self, command: str, timeout: int = 30) -> str:
        """
        执行 Shell 命令（具有最高权限）
        
        Args:
            command: Shell 命令
            timeout: 超时时间（秒）
            
        Returns:
            命令输出
        """
        try:
            logger.warning(f"⚠️ 执行 Shell 命令（最高权限）: {command}")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            output = result.stdout + result.stderr
            return f"命令执行完成:\n{output[:1000]}{'...' if len(output) > 1000 else ''}"
        except subprocess.TimeoutExpired:
            return "命令执行超时"
        except Exception as e:
            logger.error(f"执行命令失败: {e}")
            return f"执行失败: {str(e)}"

