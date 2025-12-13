# -*- encoding: utf-8 -*-
"""
ColorInfo 日志系统的消息格式化工具。
"""
import os
from datetime import datetime

class MessageFormatter:
    """处理日志消息格式化。"""
    
    def __init__(self):
        """使用默认设置初始化格式化器。"""
        self.format_date = True
        self.format_time = True
        self.format_filename = True
        self.format_class = True
        self.format_fun = True
        self.format_line = True
        self.format_level = True
        self.current_date = None
        self._update_time()
    
    def _update_time(self):
        """更新当前时间戳。"""
        self.current_date = str(datetime.now()).split('.')[0]
    
    def set_format(self, date_on=True, time_on=True, filename_on=True, 
                   class_on=True, fun_on=True, line=True, level=True):
        """
        设置格式选项。
        
        Args:
            date_on (bool): 显示日期
            time_on (bool): 显示时间  
            filename_on (bool): 显示文件名
            class_on (bool): 显示类名
            fun_on (bool): 显示函数名
            line (bool): 显示行号
            level (bool): 显示日志级别
        """
        # Validate all parameters are boolean
        params = {
            'date_on': date_on, 'time_on': time_on, 'filename_on': filename_on,
            'class_on': class_on, 'fun_on': fun_on, 'line': line, 'level': level
        }
        
        for param_name, param_value in params.items():
            if not isinstance(param_value, bool):
                raise ValueError("参数 {} 必须是布尔值，但接收到 {} 类型".format(
                    param_name, type(param_value)))
        
        self.format_date = date_on
        self.format_time = time_on
        self.format_filename = filename_on
        self.format_class = class_on
        self.format_fun = fun_on
        self.format_line = line
        self.format_level = level
    
    def format_message(self, msg, level, filename=None, line_num=None, 
                      class_name=None, function_name=None):
        """
        根据当前设置格式化日志消息。
        
        Args:
            msg (str): 日志消息
            level (str): 日志级别
            filename (str): 源文件名
            line_num (int): 行号
            class_name (str): 类名
            function_name (str): 函数名
            
        Returns:
            str: 格式化后的消息
        """
        self._update_time()
        
        try:
            if self.current_date is not None:
                date_part, time_part = self.current_date.split(' ')
            else:
                date_part, time_part = '', ''
        except (AttributeError, ValueError):
            date_part, time_part = '', ''
        
        msg_parts = []
        
        if self.format_date:
            msg_parts.append(date_part)
        if self.format_time:
            msg_parts.append(time_part)
        if self.format_filename and filename:
            msg_parts.append(self._process_filename(filename))
        if self.format_line and line_num is not None:
            msg_parts.append("line: {}".format(line_num))
        if class_name and self.format_class:
            msg_parts.append("Class: {}".format(class_name))
        if function_name and self.format_fun and function_name != '<module>':
            msg_parts.append("Function: {}".format(function_name))
        if self.format_level:
            msg_parts.append("{} : {}".format(level, msg))
        else:
            msg_parts.append(msg)
        
        return ' '.join(msg_parts)
    
    def _process_filename(self, filename):
        """
        处理文件名以提取基本名称。
        
        Args:
            filename (str): 文件名或路径
            
        Returns:
            str: 处理后的文件名
        """
        filename_str = str(filename)
        return os.path.split(filename_str)[1]