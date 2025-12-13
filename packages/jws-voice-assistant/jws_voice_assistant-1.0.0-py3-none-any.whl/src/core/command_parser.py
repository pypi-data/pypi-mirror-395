"""
指令解析模块
负责理解用户的自然语言指令并转换为可执行的命令
"""

import re
from loguru import logger
from typing import Dict, Optional


class CommandParser:
    """指令解析器"""
    
    def __init__(self):
        """初始化指令解析器"""
        # 定义指令模式
        self.patterns = {
            # 打开应用
            'open_app': [
                r'打开(.+)',
                r'启动(.+)',
                r'运行(.+)',
                r'开启(.+)',
            ],
            # 关闭应用
            'close_app': [
                r'关闭(.+)',
                r'退出(.+)',
                r'关闭(.+)应用',
                r'退出(.+)应用',
                r'关闭(.+)程序',
            ],
            # 切换应用
            'switch_app': [
                r'切换到(.+)',
                r'切换到(.+)应用',
                r'打开(.+)应用',
            ],
            # 系统命令
            'system_command': [
                r'关机',
                r'重启',
                r'锁屏',
                r'静音',
                r'取消静音',
            ],
            # 文件操作
            'file_operation': [
                r'打开文件(.+)',
                r'创建文件(.+)',
                r'删除文件(.+)',
            ],
        }
        
        # 应用名称映射（中文到英文）
        self.app_mapping = {
            '浏览器': 'Safari',
            'safari': 'Safari',
            'chrome': 'Google Chrome',
            '谷歌浏览器': 'Google Chrome',
            '邮件': 'Mail',
            'mail': 'Mail',
            '邮件应用': 'Mail',
            '备忘录': 'Notes',
            'notes': 'Notes',
            '终端': 'Terminal',
            'terminal': 'Terminal',
            'finder': 'Finder',
            '访达': 'Finder',
            '微信': 'WeChat',
            'wechat': 'WeChat',
            'qq': 'QQ',
            '音乐': 'Music',
            'music': 'Music',
            '音乐应用': 'Music',
            '腾讯视频': '腾讯视频',
            'tencentvideo': '腾讯视频',
            '腾讯': '腾讯视频',
            '视频': '腾讯视频',
        }
    
    def parse(self, text: str) -> Optional[Dict]:
        """
        解析用户指令
        
        Args:
            text: 用户输入的文本
        
        Returns:
            解析后的指令字典，如果无法解析返回 None
        """
        if not text:
            return None
        
        text = text.strip().lower()
        logger.debug(f"解析指令: {text}")
        
        # 尝试匹配各种指令模式
        for action, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return self._build_command(action, match, text)
        
        # 如果没有匹配到，尝试智能理解
        return self._intelligent_parse(text)
    
    def _build_command(self, action: str, match: re.Match, original_text: str) -> Dict:
        """构建指令字典"""
        params = {}
        
        if action in ['open_app', 'switch_app', 'close_app']:
            app_name = match.group(1).strip()
            # 映射应用名称
            app_name = self.app_mapping.get(app_name.lower(), app_name)
            params['app_name'] = app_name
        
        elif action == 'system_command':
            params['command'] = match.group(0).strip()
        
        elif action == 'file_operation':
            if '打开' in original_text:
                params['operation'] = 'open'
            elif '创建' in original_text:
                params['operation'] = 'create'
            elif '删除' in original_text:
                params['operation'] = 'delete'
            params['path'] = match.group(1).strip()
        
        return {
            'action': action,
            'params': params,
            'original_text': original_text
        }
    
    def _intelligent_parse(self, text: str) -> Optional[Dict]:
        """智能解析（使用简单的关键词匹配）"""
        # 这里可以集成更高级的NLP模型，如 OpenAI API
        
        # 打开应用的关键词
        if any(word in text for word in ['打开', '启动', '运行', '开启']):
            # 尝试提取应用名
            for app_cn, app_en in self.app_mapping.items():
                if app_cn in text:
                    return {
                        'action': 'open_app',
                        'params': {'app_name': app_en},
                        'original_text': text
                    }
            # 如果没有匹配到映射，尝试提取应用名
            for word in ['打开', '启动', '运行', '开启']:
                if word in text:
                    app_name = text.split(word)[-1].strip()
                    if app_name:
                        return {
                            'action': 'open_app',
                            'params': {'app_name': app_name},
                            'original_text': text
                        }
        
        # 关闭应用的关键词
        if any(word in text for word in ['关闭', '退出']):
            # 尝试提取应用名
            for app_cn, app_en in self.app_mapping.items():
                if app_cn in text:
                    return {
                        'action': 'close_app',
                        'params': {'app_name': app_en},
                        'original_text': text
                    }
            # 如果没有匹配到映射，尝试提取应用名
            for word in ['关闭', '退出']:
                if word in text:
                    app_name = text.split(word)[-1].strip()
                    if app_name:
                        return {
                            'action': 'close_app',
                            'params': {'app_name': app_name},
                            'original_text': text
                        }
        
        return None

