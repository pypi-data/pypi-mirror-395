import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import inspect
import json
import functools
import asyncio

# 定义自定义日志级别及其对应的整数值
logging.addLevelName(25, "NOTICE")
NOTICE = 25

# 创建一个函数，用于方便地调用自定义日志级别
def notice(self, msg, *args, **kws):
    if self.isEnabledFor(NOTICE):
        self._log(NOTICE, msg, args, **kws)

logging.Logger.notice = notice

class Log:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, console_level = logging.INFO, log_file_name="app.log"):
        self.Console_LOG_LEVEL = console_level
        self.log_file_name = log_file_name
        self.LOG_FILE_PATH = os.path.join("logs", log_file_name)
        os.makedirs(os.path.dirname(self.LOG_FILE_PATH), exist_ok=True)
        self.logger = self.get_logger()

    def get_logger(self):
        # 设置日志级别为 CRITICAL，这将阻止 INFO 级别的日志输出
        # 你也可以设置为 ERROR, WARNING, 或 FATAL 来过滤更多日志
        httpx_logger = logging.getLogger("httpx")
        httpx_logger.setLevel(logging.WARNING)
        

        # uvicorn logger
        # uvicorn_access_logger = logging.getLogger("uvicorn.access")
        # uvicorn_access_logger.setLevel(logging.WARNING)
        # uvicorn_access_logger.addHandler(file_handler)

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            # --- 4. 配置 Formatter (格式化器) ---
            # 以后有一个标准化的日志要使用logger 而非标的则使用super-log
            formatter = logging.Formatter(
                "%(asctime)s $ %(created)f $ %(levelname)s $ %(funcName)s $ :%(lineno)d $ %(pathname)s $ %(message)s||"
            )
            # --- 5. 配置 Handler (处理器) ---

            # 5.1 控制台处理器 (StreamHandler)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.Console_LOG_LEVEL)  # 控制台只显示 INFO 及以上级别的日志
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            # 文件系统
            ## 主日志本
            file_handler = RotatingFileHandler(  # RotatingFileHandler: 按文件大小轮转
                self.LOG_FILE_PATH,
                maxBytes=20 * 1024 * 1024,  # 10 MB # maxBytes: 单个日志文件的最大字节数 (例如 10MB)
                backupCount=10, # backupCount: 保留的旧日志文件数量
                encoding="utf-8",
            )
            file_handler.setLevel(logging.DEBUG)  # 记录所有日志
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            ## 运行日志本
            file_handler_info = RotatingFileHandler(
                self.LOG_FILE_PATH.replace('.log','_info.log'),
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding="utf-8",
            )
            file_handler_info.setLevel(logging.INFO)  # 记录本系统的日志
            file_handler_info.setFormatter(formatter)
            logger.addHandler(file_handler_info)


            ## 运行日志本
            file_handler_info = RotatingFileHandler(
                self.LOG_FILE_PATH.replace('.log','_notice.log'),
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding="utf-8",
            )
            file_handler_info.setLevel(25)  # 记录本系统的日志
            file_handler_info.setFormatter(formatter)
            logger.addHandler(file_handler_info)

            ## 错误日志本
            file_handler_warning = RotatingFileHandler(
                self.LOG_FILE_PATH.replace('.log','_error.log'),
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding="utf-8",
            )
            file_handler_warning.setLevel(logging.WARNING)  # 记录警告和错误
            file_handler_warning.setFormatter(formatter)
            logger.addHandler(file_handler_warning)

            ## 指定日志本 
            file_handler_super = RotatingFileHandler(
                self.LOG_FILE_PATH.replace('.log','_caitical.log'),
                maxBytes=5 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding="utf-8",
            )
            file_handler_super.setLevel(logging.CRITICAL)  # 记录重点跟踪日志
            file_handler_super.setFormatter(formatter)
            logger.addHandler(file_handler_super)

        return logger


# def log_func(logger):
#     def outer_packing(func):
#         @functools.wraps(func)
#         async def wrapper(*args, **kwargs):
#             try:
#                 if asyncio.iscoroutinefunction(func):
#                     # 如果被装饰的函数是协程，则 await 它
#                     result = await func(*args, **kwargs)
#                 else:
#                     # 否则，直接调用（同步函数）
#                     result = func(*args, **kwargs)
#                 # logger.notice(f'{func.__name__} & {kwargs_dict} & {result}')
#             except Exception as e:
#                 params = locals()
#                 logger.error(f'{func.__name__} & {params}  & {e}')
#                 raise 
#             return result
#         return wrapper
#     return outer_packing



import logging
import json
import traceback
import sys
import inspect
import asyncio
import functools

def _sanitize_value(value, max_len=200):
    """
    对变量值进行清理，截断长字符串，并处理不可序列化的对象。
    """
    if isinstance(value, (int, float, bool, type(None))):
        return value
    elif isinstance(value, str):
        return value[:max_len] + ('...' if len(value) > max_len else '')
    elif isinstance(value, (list, tuple, set)):
        return f"<{type(value).__name__} len={len(value)}>"
    elif isinstance(value, dict):
        return f"<{type(value).__name__} keys={len(value)}>"
    else:
        # 尝试repr()，但限制长度，避免输出过长或复杂对象导致问题
        try:
            r = repr(value)
            return r[:max_len] + ('...' if len(r) > max_len else '')
        except Exception:
            return f"<{type(value).__name__} object at {hex(id(value))}>"

def _get_sanitized_frame_locals(frame, 
                                exclude_keys: list = None, 
                                sensitive_keys: list = None, 
                                max_value_len: int = 200) -> dict:
    """
    获取并清理指定栈帧的局部变量。
    """
    if exclude_keys is None:
        exclude_keys = []
    if sensitive_keys is None:
        sensitive_keys = []

    sanitized_data = {}
    
    for key, value in frame.f_locals.items():
        if key in exclude_keys:
            continue
        
        if key in sensitive_keys:
            sanitized_data[key] = f"***SENSITIVE_DATA_HIDDEN***"
        else:
            sanitized_data[key] = _sanitize_value(value, max_value_len)
            
    return sanitized_data

def log_func(logger=None, 
             exclude_keys: list = None, 
             sensitive_keys: list = None, 
             max_value_len: int = 2000):
    """
    一个用于记录函数执行（包括异常）的装饰器。
    在发生异常时，会记录所有相关栈帧的局部变量。

    Args:
        logger (logging.Logger): 用于记录日志的Logger对象。如果为None，则使用默认logger。
        exclude_keys (list): 一个字符串列表，包含不希望记录的变量名。
        sensitive_keys (list): 一个字符串列表，包含需要脱敏的变量名。
        max_value_len (int): 字符串值的最大长度，超过此长度将被截断。
    """

    # 确保 exclude_keys 和 sensitive_keys 是可变对象的新实例，以防多个装饰器实例共享
    exclude_keys_final = exclude_keys if exclude_keys is not None else []
    sensitive_keys_final = sensitive_keys if sensitive_keys is not None else []

    def outer_packing(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                # logger.notice(f'{func.__name__} & {kwargs_dict} & {result}')
                return result
            except Exception as e:
                # 获取异常信息
                exc_type, exc_value, exc_traceback = sys.exc_info()
                
                # 格式化完整的堆栈信息
                formatted_traceback = traceback.format_exc()

                # 遍历栈帧
                frames_data = []
                tb_frame = exc_traceback
                while tb_frame:
                    frame = tb_frame.tb_frame
                    
                    # 获取栈帧的局部变量
                    frame_locals = _get_sanitized_frame_locals(
                        frame, 
                        exclude_keys=exclude_keys_final, 
                        sensitive_keys=sensitive_keys_final, 
                        max_value_len=max_value_len
                    )
                    
                    # 避免记录装饰器自身的内部变量，或者其他不必要的栈帧
                    # 可以通过检查文件名或函数名来过滤
                    if frame.f_code.co_filename != __file__: # 排除本文件内的栈帧
                        frames_data.append({
                            "filename": frame.f_code.co_filename,
                            "function": frame.f_code.co_name,
                            "lineno": frame.f_lineno,
                            "locals": frame_locals
                        })
                    tb_frame = tb_frame.tb_next

                # 构建结构化的错误信息
                error_info = {
                    "function_name": func.__name__, # 被装饰的函数名
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "traceback": formatted_traceback,
                    "frames": frames_data 
                }
                
                # 使用logger记录错误信息，以JSON格式输出
                logger.error(json.dumps(error_info, indent=4, ensure_ascii=False))
                raise # 重新抛出异常，保持原有的异常行为
            
        return wrapper
    return outer_packing
