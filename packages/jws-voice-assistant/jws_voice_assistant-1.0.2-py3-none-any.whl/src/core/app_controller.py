"""
应用控制模块
负责启动、切换和控制应用程序
"""

import subprocess
import os
from typing import Optional, Dict
from loguru import logger


class AppController:
    """应用控制器"""
    
    def __init__(self, config: Optional[dict] = None):
        """初始化应用控制器"""
        logger.info("📱 初始化应用控制器...")
        self.config = config or {}
        self.app_paths = self._get_app_paths()
        # 加载自定义应用路径
        self._load_custom_app_paths()
    
    def _get_app_paths(self) -> dict:
        """获取应用路径（包括多个位置）"""
        apps = {}
        
        # 搜索多个应用目录
        app_dirs = [
            '/Applications',
            '/Applications/Utilities',
            os.path.expanduser('~/Applications'),
            '/System/Applications',
            '/System/Applications/Utilities',
        ]
        
        for app_dir in app_dirs:
            if os.path.exists(app_dir):
                try:
                    for app in os.listdir(app_dir):
                        if app.endswith('.app'):
                            app_name = app.replace('.app', '')
                            app_path = os.path.join(app_dir, app)
                            # 使用小写作为键，支持多种匹配
                            apps[app_name.lower()] = app_path
                            # 也添加不带空格和特殊字符的版本
                            apps[app_name.lower().replace(' ', '').replace('-', '')] = app_path
                            # 添加中文名称的简化版本
                            if '腾讯' in app_name or 'Tencent' in app_name:
                                apps['腾讯视频'] = app_path
                                apps['tencentvideo'] = app_path
                                apps['腾讯'] = app_path
                except (PermissionError, OSError) as e:
                    logger.debug(f"无法访问目录 {app_dir}: {e}")
        
        logger.debug(f"找到 {len(apps)} 个应用")
        return apps
    
    def _load_custom_app_paths(self):
        """加载自定义应用路径（从配置文件）"""
        custom_paths = self.config.get('custom_app_paths', {})
        for app_name, app_path in custom_paths.items():
            if os.path.exists(app_path):
                self.app_paths[app_name.lower()] = app_path
                logger.info(f"加载自定义应用路径: {app_name} -> {app_path}")
            else:
                logger.warning(f"自定义应用路径不存在: {app_name} -> {app_path}")
    
    def open_app(self, app_name: str) -> str:
        """
        打开应用（增强版，支持多种方式）
        
        Args:
            app_name: 应用名称
        
        Returns:
            操作结果
        """
        try:
            logger.info(f"🚀 正在打开应用: {app_name}")
            
            # 方法1: 尝试从应用路径字典查找
            app_path = self.app_paths.get(app_name.lower())
            if not app_path:
                # 尝试不带空格和特殊字符的版本
                app_path = self.app_paths.get(app_name.lower().replace(' ', '').replace('-', ''))
            
            if app_path and os.path.exists(app_path):
                logger.info(f"找到应用路径: {app_path}")
                result = subprocess.run(['open', app_path], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return f"已打开 {app_name}"
            
            # 方法2: 使用 open -a 命令（macOS 会自动查找应用）
            logger.info(f"尝试使用 open -a: {app_name}")
            result = subprocess.run(
                ['open', '-a', app_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return f"已打开 {app_name}"
            else:
                logger.warning(f"open -a 失败: {result.stderr}")
            
            # 方法3: 使用 AppleScript
            logger.info(f"尝试使用 AppleScript: {app_name}")
            script = f'tell application "{app_name}" to activate'
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return f"已打开 {app_name}"
            else:
                logger.warning(f"AppleScript 失败: {result.stderr}")
            
            # 方法4: 尝试使用 mdfind 查找应用（支持模糊匹配）
            logger.info(f"尝试使用 mdfind 查找: {app_name}")
            
            # 尝试多种搜索方式
            search_queries = [
                f'kMDItemKind == "Application" && kMDItemDisplayName == "{app_name}"',
                f'kMDItemKind == "Application" && kMDItemDisplayName == "*{app_name}*"',
                f'kMDItemKind == "Application" && kMDItemFSName == "*{app_name}*"',
            ]
            
            for query in search_queries:
                find_result = subprocess.run(
                    ['mdfind', query],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if find_result.returncode == 0 and find_result.stdout.strip():
                    app_paths = [p.strip() for p in find_result.stdout.strip().split('\n') if p.strip().endswith('.app')]
                    if app_paths:
                        app_path = app_paths[0]  # 使用第一个匹配的结果
                        logger.info(f"找到应用路径: {app_path}")
                        subprocess.run(['open', app_path], timeout=5)
                        return f"已打开 {app_name}"
            
            # 如果都失败了，提供有用的错误信息
            logger.error(f"无法找到应用: {app_name}")
            logger.info("💡 提示：")
            logger.info("   1. 检查应用名称是否正确")
            logger.info("   2. 确认应用已安装在 /Applications 目录")
            logger.info("   3. 可以尝试使用完整应用名称")
            
            return f"无法找到或打开应用 '{app_name}'。请确认应用已安装，或使用完整应用名称。"
        
        except subprocess.TimeoutExpired:
            logger.error(f"打开应用超时: {app_name}")
            return f"打开应用超时: {app_name}"
        except Exception as e:
            logger.error(f"打开应用失败: {e}")
            return f"无法打开应用 {app_name}: {str(e)}"
    
    def switch_app(self, app_name: str) -> str:
        """
        切换到应用
        
        Args:
            app_name: 应用名称
        
        Returns:
            操作结果
        """
        try:
            logger.info(f"🔄 正在切换到应用: {app_name}")
            
            # 使用 AppleScript 切换到应用
            script = f'''
            tell application "System Events"
                tell process "{app_name}"
                    set frontmost to true
                end tell
            end tell
            tell application "{app_name}"
                activate
            end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return f"已切换到 {app_name}"
        
        except Exception as e:
            logger.error(f"切换应用失败: {e}")
            # 如果切换失败，尝试打开
            return self.open_app(app_name)
    
    def close_app(self, app_name: str) -> str:
        """
        关闭应用
        
        Args:
            app_name: 应用名称
        
        Returns:
            操作结果
        """
        try:
            logger.info(f"🛑 正在关闭应用: {app_name}")
            
            # 方法1: 使用 AppleScript quit 命令
            script = f'''
            tell application "{app_name}"
                quit
            end tell
            '''
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return f"已关闭 {app_name}"
            
            # 方法2: 使用 killall 命令（强制关闭）
            logger.info(f"尝试使用 killall: {app_name}")
            result = subprocess.run(
                ['killall', app_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return f"已关闭 {app_name}"
            elif "No matching processes" in result.stderr:
                return f"应用 {app_name} 未在运行"
            else:
                return f"关闭应用失败: {result.stderr}"
        
        except subprocess.TimeoutExpired:
            return f"关闭应用超时: {app_name}"
        except Exception as e:
            logger.error(f"关闭应用失败: {e}")
            return f"无法关闭应用 {app_name}: {str(e)}"
    
    def get_running_apps(self) -> list:
        """获取正在运行的应用列表"""
        try:
            script = '''
            tell application "System Events"
                set appList to name of every process whose background only is false
            end tell
            return appList
            '''
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                # 解析结果
                apps = result.stdout.strip().split(', ')
                return [app.strip() for app in apps if app.strip()]
            return []
        except Exception as e:
            logger.error(f"获取运行应用列表失败: {e}")
            return []

