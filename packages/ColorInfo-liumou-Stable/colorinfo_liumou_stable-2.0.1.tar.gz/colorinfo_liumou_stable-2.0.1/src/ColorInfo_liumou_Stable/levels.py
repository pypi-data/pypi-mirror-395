# -*- encoding: utf-8 -*-
"""
ColorInfo 日志系统的日志级别和验证工具。
"""

class LogLevel:
    """日志级别常量和验证。"""
    
    # Log level definitions
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    
    # Log level hierarchy (lower number = lower priority)
    LEVEL_DIC = {
        "DEBUG": 0,
        "INFO": 1, 
        "WARNING": 2,
        "ERROR": 3
    }
    
    LEVEL_LIST = ["DEBUG", "INFO", "WARNING", "ERROR"]
    
    @staticmethod
    def validate_level(level, default="DEBUG"):
        """
        验证并返回有效的日志级别。
        
        Args:
            level (str): 要验证的日志级别
            default (str): 如果验证失败，默认级别
            
        Returns:
            str: 验证后的日志级别（大写）
        """
        if not isinstance(level, str) or level.upper() not in LogLevel.LEVEL_LIST:
            return default
        return level.upper()
    
    @staticmethod
    def get_level_value(level):
        """
        获取日志级别的数值。
        
        Args:
            level (str): 日志级别
            
        Returns:
            int: 日志级别的数值
        """
        validated_level = LogLevel.validate_level(level)
        return LogLevel.LEVEL_DIC[validated_level]