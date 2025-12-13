# pyright: strict, reportUnusedFunction=false

from loguru import logger
import sys
import os
from typing import Optional
from .util import *
import logging


class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._logger = logger
        self._initialized = True
        
    def set_logger(
        self,
        log_path: str = "/var/log/ieops",
        app_name: str = "gmi-ieops-sdk",
        log_level: str = "INFO",
        retention: str = "3 days",
        rotation: str = "00:00",
        compression: str = "zip",
        file_enabled: bool = True
    ) -> None:
        """
        设置日志配置
        Args:
            log_path: 日志存储路径
            app_name: 应用名称
            log_level: 日志级别
            retention: 日志保留时间
            rotation: 日志切分时间
            compression: 日志压缩格式
            file_enabled: 是否启用文件日志
        """
        # 移除默认的处理器
        self._logger.remove()
        
        # 定义日志格式
        def format_with_trace_id(record: dict) -> str: # type: ignore
            trace_part = f"|trace_id:{record['extra']['trace_id']}" if 'trace_id' in record["extra"] else "" # type: ignore
            level = record['level'].name # type: ignore
            if level == "DEBUG":
                level = "DEBUG"
            elif level == "INFO":
                level = "INFOO"
            elif level == "WARNING":
                level = "WARNN"
            elif level == "ERROR":
                level = "ERROR"
            return "<level>["+level+"]</level> " \
                   "<green>[{time:YYYY-MM-DD HH:mm:ss.SSS}]</green> " \
                   "<cyan>pid:{process}|{file}:{line}"+trace_part+"|app:{extra[app_name]}</cyan> --- " \
                   "<level>{message}</level>\n" # type: ignore
            
        # 添加标准输出处理器
        self._logger.add(
            sys.stdout,
            format=format_with_trace_id, # type: ignore
            level=log_level,
            enqueue=True
        ) # type: ignore
        
        # 确保日志目录存在
        os.makedirs(log_path, exist_ok=True)
        
        # 添加文件处理器
        if file_enabled:
            log_file = os.path.join(log_path, f"{app_name}.{randstr(10)}.log")
            self._logger.add(
                log_file,
                format=format_with_trace_id, # type: ignore
                level=log_level,
                rotation=rotation,
                retention=retention,
                compression=compression,
                enqueue=True,
                encoding="utf-8"
            )   
        
        # 设置默认的 app_name
        self._logger = self._logger.bind(app_name=app_name)
    
    def get_logger(self, trace_id: Optional[str] = None):
        """
        获取带有 trace_id 的 logger 实例
        
        Args:
            trace_id: 追踪ID，如果为 None 则不显示 trace_id
        """
        if trace_id:
            return self._logger.bind(trace_id=trace_id)
        return self._logger

log = Logger()

uvicorn_logger = logging.getLogger("uvicorn.error")  # use this logger for uvicorn