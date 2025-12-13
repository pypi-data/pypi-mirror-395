# 自定义日志模块核心实现
import os
import sys
import time
import traceback
from enum import Enum
from .config import LOG_COLORS, RESET_COLOR, LOG_FORMAT, DATETIME_FORMAT, LOG_FILE_PATH, LOG_LEVELS


class LogLevel(Enum):
    """日志级别枚举"""
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class CustomLogger:
    """自定义日志类"""
    
    def __init__(self, name='app', level=LogLevel.INFO):
        """初始化日志器"""
        self.name = name
        self.level = level
        self._ensure_log_dir()
    
    def _ensure_log_dir(self):
        """确保日志目录存在"""
        log_dir = os.path.dirname(LOG_FILE_PATH)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
    
    def _get_caller_info(self):
        """获取调用者信息"""
        # 获取调用栈
        stack = traceback.extract_stack()
        
        # 遍历调用栈，找到第一个不在logger.py中的调用
        # 栈结构: [0] - traceback.extract_stack, [1] - _get_caller_info, 
        # [2] - _log, [3] - debug/info/warning/error, [4] - 用户代码
        for i, frame in enumerate(stack):
            # 跳过当前文件的调用
            if frame.filename == __file__:
                continue
            
            # 返回调用者信息
            return {
                'file': os.path.basename(frame.filename),
                'line': frame.lineno,
                'function': frame.name
            }
        
        return {
            'file': 'unknown',
            'line': 0,
            'function': 'unknown'
        }
    
    def _log_with_caller(self, level, message, caller_info):
        """带调用者信息的核心日志方法"""
        # 检查日志级别
        if LOG_LEVELS[level.value] < LOG_LEVELS[self.level.value]:
            return
        
        # 获取当前时间
        current_time = time.strftime(DATETIME_FORMAT)
        
        # 获取颜色
        color = LOG_COLORS.get(level.value, '')
        
        # 构建日志消息
        console_msg = LOG_FORMAT['console'] % {
            'color': color,
            'level_name': level.value,
            'time': current_time,
            'file': caller_info['file'],
            'line': caller_info['line'],
            'message': message,
            'reset': RESET_COLOR
        }
        
        file_msg = LOG_FORMAT['file'] % {
            'level_name': level.value,
            'time': current_time,
            'file': caller_info['file'],
            'line': caller_info['line'],
            'message': message
        }
        
        # 打印到控制台
        print(console_msg)
        
        # 追加写入到文件
        try:
            with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
                f.write(file_msg + '\n')
        except Exception as e:
            print(f"{LOG_COLORS['ERROR']}[ERROR] 写入日志文件失败: {e}{RESET_COLOR}")
    
    def _log(self, level, message):
        """核心日志方法"""
        # 获取调用者信息
        caller_info = self._get_caller_info()
        self._log_with_caller(level, message, caller_info)
    
    def debug(self, message):
        """调试日志"""
        self._log(LogLevel.DEBUG, message)
    
    def info(self, message):
        """信息日志"""
        self._log(LogLevel.INFO, message)
    
    def warning(self, message):
        """警告日志"""
        self._log(LogLevel.WARNING, message)
    
    def error(self, message):
        """错误日志"""
        self._log(LogLevel.ERROR, message)
    
    def set_level(self, level):
        """设置日志级别"""
        self.level = level
    
    def get_log_file_path(self):
        """获取日志文件路径"""
        return LOG_FILE_PATH
    
    def clear_logs(self):
        """清空日志文件"""
        try:
            with open(LOG_FILE_PATH, 'w', encoding='utf-8') as f:
                f.write('')
            self.info("日志文件已清空")
        except Exception as e:
            self.error(f"清空日志文件失败: {e}")


# 创建全局日志实例
_global_logger = CustomLogger()

def get_logger(name=None):
    """获取全局日志实例"""
    if name is not None:
        _global_logger.name = name
    return _global_logger


# 便捷函数
import inspect

def debug(message):
    """便捷调试日志"""
    # 获取调用者信息并传递
    frame = inspect.currentframe().f_back
    try:
        caller_info = {
            'file': os.path.basename(frame.f_code.co_filename),
            'line': frame.f_lineno,
            'function': frame.f_code.co_name
        }
        _global_logger._log_with_caller(LogLevel.DEBUG, message, caller_info)
    finally:
        del frame

def info(message):
    """便捷信息日志"""
    frame = inspect.currentframe().f_back
    try:
        caller_info = {
            'file': os.path.basename(frame.f_code.co_filename),
            'line': frame.f_lineno,
            'function': frame.f_code.co_name
        }
        _global_logger._log_with_caller(LogLevel.INFO, message, caller_info)
    finally:
        del frame

def warning(message):
    """便捷警告日志"""
    frame = inspect.currentframe().f_back
    try:
        caller_info = {
            'file': os.path.basename(frame.f_code.co_filename),
            'line': frame.f_lineno,
            'function': frame.f_code.co_name
        }
        _global_logger._log_with_caller(LogLevel.WARNING, message, caller_info)
    finally:
        del frame

def error(message):
    """便捷错误日志"""
    frame = inspect.currentframe().f_back
    try:
        caller_info = {
            'file': os.path.basename(frame.f_code.co_filename),
            'line': frame.f_lineno,
            'function': frame.f_code.co_name
        }
        _global_logger._log_with_caller(LogLevel.ERROR, message, caller_info)
    finally:
        del frame
