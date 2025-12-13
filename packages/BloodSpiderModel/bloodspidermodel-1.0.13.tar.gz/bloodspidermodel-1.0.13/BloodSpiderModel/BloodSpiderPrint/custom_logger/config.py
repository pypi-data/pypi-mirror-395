# 日志模块配置
import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志文件路径
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, 'logs', 'app.log')

# 日志颜色配置 (ANSI颜色码)
LOG_COLORS = {
    'DEBUG': '\033[94m',      # 蓝色
    'INFO': '\033[92m',       # 绿色
    'WARNING': '\033[93m',    # 黄色
    'ERROR': '\033[91m'       # 红色
}

# 重置颜色
RESET_COLOR = '\033[0m'

# 日志格式配置
LOG_FORMAT = {
    'console': '%(color)s[%(level_name)s] %(time)s - %(file)s:%(line)s - %(message)s%(reset)s',
    'file': '[%(level_name)s] %(time)s - %(file)s:%(line)s - %(message)s'
}

# 日期时间格式
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# 日志级别
LOG_LEVELS = {
    'DEBUG': 10,
    'INFO': 20,
    'WARNING': 30,
    'ERROR': 40
}
