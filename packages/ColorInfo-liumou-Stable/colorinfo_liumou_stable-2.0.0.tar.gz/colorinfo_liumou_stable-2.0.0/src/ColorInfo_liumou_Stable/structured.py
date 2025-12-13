# -*- encoding: utf-8 -*-
"""
结构化日志功能，类似 Go 语言 Zap 日志库
"""
import json
import time
from datetime import datetime


class StructuredLogger:
    """结构化日志记录器，支持类似 Zap 的字段式日志"""
    
    def __init__(self, base_logger):
        """
        初始化结构化日志记录器
        
        Args:
            base_logger: 基础日志记录器实例
        """
        self.base_logger = base_logger
    
    def _format_fields(self, fields):
        """
        格式化字段为字符串
        
        Args:
            fields (dict): 字段字典
            
        Returns:
            str: 格式化后的字段字符串
        """
        if not fields:
            return ""
        
        # 将字段转换为 key=value 格式
        field_parts = []
        for key, value in fields.items():
            # 处理不同类型的值
            if isinstance(value, str):
                # 字符串值，如果包含空格则加引号
                if ' ' in value:
                    field_parts.append('{}="{}"'.format(key, value))
                else:
                    field_parts.append('{}={}'.format(key, value))
            elif isinstance(value, (int, float, bool)):
                # 数字和布尔值直接转换
                field_parts.append('{}={}'.format(key, value))
            elif value is None:
                # None 值
                field_parts.append('{}=null'.format(key))
            else:
                # 其他类型转换为字符串
                field_parts.append('{}={}'.format(key, str(value)))
        
        return ' '.join(field_parts)
    
    def _create_structured_message(self, msg, fields):
        """
        创建结构化消息
        
        Args:
            msg (str): 基础消息
            fields (dict): 字段字典
            
        Returns:
            str: 结构化消息
        """
        field_str = self._format_fields(fields)
        if field_str:
            return "{} {}".format(msg, field_str)
        return msg
    
    def debug(self, msg, **fields):
        """
        记录 DEBUG 级别结构化日志
        
        Args:
            msg (str): 日志消息
            **fields: 结构化字段
        """
        structured_msg = self._create_structured_message(msg, fields)
        self.base_logger.debug(structured_msg)
    
    def info(self, msg, **fields):
        """
        记录 INFO 级别结构化日志
        
        Args:
            msg (str): 日志消息
            **fields: 结构化字段
        """
        structured_msg = self._create_structured_message(msg, fields)
        self.base_logger.info(structured_msg)
    
    def warning(self, msg, **fields):
        """
        记录 WARNING 级别结构化日志
        
        Args:
            msg (str): 日志消息
            **fields: 结构化字段
        """
        structured_msg = self._create_structured_message(msg, fields)
        self.base_logger.warning(structured_msg)
    
    def error(self, msg, **fields):
        """
        记录 ERROR 级别结构化日志
        
        Args:
            msg (str): 日志消息
            **fields: 结构化字段
        """
        structured_msg = self._create_structured_message(msg, fields)
        self.base_logger.error(structured_msg)
    
    def with_fields(self, **fields):
        """
        创建带有默认字段的新结构化日志记录器
        
        Args:
            **fields: 默认字段
            
        Returns:
            StructuredLogger: 新的结构化日志记录器实例
        """
        # 创建一个新的记录器，继承当前字段
        new_logger = StructuredLogger(self.base_logger)
        new_logger.default_fields = fields.copy()
        return new_logger
    
    def close(self):
        """关闭日志记录器"""
        if hasattr(self.base_logger, 'close'):
            self.base_logger.close()


class JSONStructuredLogger(StructuredLogger):
    """JSON 格式的结构化日志记录器"""
    
    def _create_structured_message(self, msg, fields):
        """
        创建 JSON 格式的结构化消息
        
        Args:
            msg (str): 基础消息
            fields (dict): 字段字典
            
        Returns:
            str: JSON 格式的消息
        """
        log_data = {
            'message': msg,
            'timestamp': datetime.now().isoformat(),
            'fields': fields or {}
        }
        return json.dumps(log_data, ensure_ascii=False, separators=(',', ':'))


# 便捷函数，类似 Zap 的 Sugar 功能
def sugar(logger):
    """
    将普通日志记录器转换为结构化日志记录器
    
    Args:
        logger: 基础日志记录器
        
    Returns:
        StructuredLogger: 结构化日志记录器
    """
    return StructuredLogger(logger)