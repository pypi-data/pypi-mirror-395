# -*- encoding: utf-8 -*-
"""
Message formatting utilities for ColorInfo logging system.
"""
import os
from datetime import datetime

class MessageFormatter:
    """Handles log message formatting."""
    
    def __init__(self):
        """Initialize the formatter with default settings."""
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
        """Update current timestamp."""
        self.current_date = str(datetime.now()).split('.')[0]
    
    def set_format(self, date_on=True, time_on=True, filename_on=True, 
                   class_on=True, fun_on=True, line=True, level=True):
        """
        Set format options.
        
        Args:
            date_on (bool): Show date
            time_on (bool): Show time  
            filename_on (bool): Show filename
            class_on (bool): Show class name
            fun_on (bool): Show function name
            line (bool): Show line number
            level (bool): Show log level
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
        Format a log message according to current settings.
        
        Args:
            msg (str): The log message
            level (str): The log level
            filename (str): Source filename
            line_num (int): Line number
            class_name (str): Class name
            function_name (str): Function name
            
        Returns:
            str: Formatted message
        """
        self._update_time()
        
        try:
            date_part, time_part = self.current_date.split(' ')
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
        Process filename to extract basename.
        
        Args:
            filename (str): The filename or path
            
        Returns:
            str: Processed filename
        """
        filename_str = str(filename)
        return os.path.split(filename_str)[1]