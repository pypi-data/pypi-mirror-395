# 日志模块使用示例
from custom_logger import get_logger, LogLevel, debug, info, warning, error


# 获取默认日志实例
logger = get_logger()

# 设置日志级别
logger.set_level(LogLevel.DEBUG)

# 示例1: 基本用法
print("\n=== 示例1: 基本用法 ===")
logger.debug("这是一个调试信息")
logger.info("这是一个普通信息")
logger.warning("这是一个警告信息")
logger.error("这是一个错误信息")

# 示例2: 便捷函数用法
print("\n=== 示例2: 便捷函数用法 ===")
debug("便捷调试信息")
info("便捷普通信息")
warning("便捷警告信息")
error("便捷错误信息")

# 示例3: 记录异常信息
print("\n=== 示例3: 记录异常信息 ===")
try:
    result = 10 / 0  # 这是故意触发的异常
except Exception as e:
    logger.error(f"发生异常: {e}")
    import traceback
    logger.error(f"异常堆栈: {traceback.format_exc()}")

# 示例4: 自定义日志名称
print("\n=== 示例4: 自定义日志名称 ===")
logger2 = get_logger("my_module")
logger2.info("来自自定义模块的日志")

# 示例5: 获取日志文件路径
print("\n=== 示例5: 获取日志文件路径 ===")
print(f"日志文件路径: {logger.get_log_file_path()}")

# 示例6: 不同日志级别测试
print("\n=== 示例6: 不同日志级别测试 ===")
logger.set_level(LogLevel.WARNING)
logger.debug("这个调试信息不会显示")  # 不会显示
logger.info("这个信息不会显示")        # 不会显示
logger.warning("这个警告会显示")      # 会显示
logger.error("这个错误会显示")        # 会显示

print("\n=== 所有示例运行完成 ===")
