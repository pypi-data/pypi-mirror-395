# -*- encoding: utf-8 -*-
"""
结合所有模块的主要 ColorLogger 类。
"""
import inspect
from .colors import ColorConstants
from .levels import LogLevel
from .file_manager import FileManager
from .formatter import MessageFormatter
from .inspector import CallStackInspector

class ColorLogger:
    """
    增强版 ColorLogger，采用模块化架构。
    兼容 Python 3.5+
    """
    
    def __init__(self, file=None, txt=False, cover=False, fileinfo=False, basename=True):
        """
        初始化 ColorLogger。
        
        Args:
            file (str): 日志文件路径
            txt (bool): 启用文本日志记录
            cover (bool): 覆盖现有日志文件
            fileinfo (bool): 显示文件信息
            basename (bool): 使用基本名称显示
        """
        # Initialize color constants
        self.colors = ColorConstants()
        
        # Initialize file manager
        self.file_manager = FileManager(
            file_path=file,
            txt_mode=txt,
            cover=cover,
            basename=basename
        )
        
        # Initialize formatter
        self.formatter = MessageFormatter()
        
        # Initialize inspector
        self.inspector = CallStackInspector()
        
        # Store configuration
        self.fileinfo = fileinfo
        self.txt_mode = txt
        self.cover = cover
        self.basename = basename
        
        # Initialize log levels
        self.level_console = 0  # Console display minimum level
        self.level_text = 0     # File logging minimum level
        
        # Get initial caller information
        self._inspect_caller()
    
    def _inspect_caller(self, frame_offset=2):
        """检查调用者信息。"""
        caller_info = self.inspector.inspect_caller(frame_offset)
        self.caller_class = caller_info['class_name']
        self.fun_name = caller_info['method_name']
    
    def set_format(self, date_on=True, time_on=True, filename_on=True, 
                   class_on=True, fun_on=True, line=True, level=True):
        """
        设置格式化选项。
        
        Args:
            date_on (bool): 显示日期
            time_on (bool): 显示时间
            filename_on (bool): 显示文件名
            class_on (bool): 显示类名
            fun_on (bool): 显示函数名
            line (bool): 显示行号
            level (bool): 显示日志级别
        """
        self.formatter.set_format(
            date_on=date_on, time_on=time_on, filename_on=filename_on,
            class_on=class_on, fun_on=fun_on, line=line, level=level
        )
    
    def set_level(self, console="DEBUG", text="DEBUG"):
        """
        设置控制台和文件输出的最小日志级别。
        
        Args:
            console (str): 控制台输出的最小级别
            text (str): 文件输出的最小级别
        """
        console_level = LogLevel.validate_level(console)
        text_level = LogLevel.validate_level(text)
        
        self.level_console = LogLevel.LEVEL_DIC[console_level]
        self.level_text = LogLevel.LEVEL_DIC[text_level]
    
    def _log_message(self, level, msg, *args, **kwargs):
        """
        内部方法处理日志逻辑。
        
        Args:
            level (str): 日志级别
            msg (str): 日志消息
            *args: 附加参数
            **kwargs: 附加关键字参数
        """
        try:
            # Find the actual caller frame by skipping logging library frames
            current_frame = inspect.currentframe()
            caller_frame = current_frame.f_back if current_frame else None
            
            # Skip frames from the logging library itself
            while caller_frame:
                frame_filename = caller_frame.f_code.co_filename
                # Check if this frame is from our logging library
                if 'ColorInfo_liumou_Stable' not in frame_filename or 'logger.py' not in frame_filename:
                    break
                caller_frame = caller_frame.f_back
            
            # If we found a valid caller frame, use it
            if caller_frame:
                frame_info = self.inspector.get_frame_info(caller_frame)
                # Get class and method info from the actual caller
                frame_locals = caller_frame.f_locals
                caller_instance = frame_locals.get('self', None)
                class_name = caller_instance.__class__.__name__ if caller_instance and hasattr(caller_instance, '__class__') else None
                method_name = caller_frame.f_code.co_name
            else:
                # Fallback to the immediate caller
                frame_info = self.inspector.get_frame_info(current_frame.f_back if current_frame else None)
                class_name = None
                method_name = frame_info['module_name']
            
            # Update time
            self.formatter._update_time()
            
            # Process message
            msg_parts = [str(msg)]
            if args:
                msg_parts.extend(str(arg) for arg in args)
            if kwargs:
                msg_parts.extend("{}={}".format(k, v) for k, v in kwargs.items())
            full_msg = ' '.join(msg_parts)
            
            # Format message
            formatted_msg = self.formatter.format_message(
                msg=full_msg,
                level=level,
                filename=frame_info['filename'],
                line_num=frame_info['line_num'],
                class_name=class_name,
                function_name=method_name
            )
            
            # Get color based on level
            color = self._get_color_for_level(level)
            
            # Console output
            level_value = LogLevel.LEVEL_DIC[level]
            if level_value >= self.level_console:
                console_msg = "{}{}{}".format(color, formatted_msg, self.colors.RESET_ALL)
                if self.fileinfo and self.txt_mode:
                    file_path, file_name = self.file_manager.get_file_info()
                    console_msg = "{}{} <<-- {}{}".format(
                        color, file_name, formatted_msg, self.colors.RESET_ALL)
                print(console_msg)
            
            # File output
            if level_value >= self.level_text and self.txt_mode:
                self.file_manager.write_log(formatted_msg)
                
        except Exception as e:
            print("{}Logger error: {}{}".format(
                self.colors.RED, str(e), self.colors.RESET_ALL))
    
    def _get_color_for_level(self, level):
        """获取日志级别的颜色。"""
        color_map = {
            "DEBUG": self.colors.BLUE,
            "INFO": self.colors.GREEN,
            "WARNING": self.colors.YELLOW,
            "ERROR": self.colors.RED
        }
        return color_map.get(level, self.colors.RESET_ALL)
    
    def debug(self, msg, *args, **kwargs):
        """记录调试消息。"""
        self._log_message("DEBUG", msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        """记录信息消息。"""
        self._log_message("INFO", msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        """记录警告消息。"""
        self._log_message("WARNING", msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        """记录错误消息。"""
        self._log_message("ERROR", msg, *args, **kwargs)
    
    def close(self):
        """关闭日志记录器并清理资源。"""
        self.file_manager.close()

# Backward compatibility - create default logger instance
logger = ColorLogger()