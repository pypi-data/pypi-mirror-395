# -*- encoding: utf-8 -*-
"""
Main ColorLogger class that combines all modules.
"""
import inspect
from .colors import ColorConstants
from .levels import LogLevel
from .file_manager import FileManager
from .formatter import MessageFormatter
from .inspector import CallStackInspector

class ColorLogger:
    """
    Enhanced ColorLogger with modular architecture.
    Compatible with Python 3.5+
    """
    
    def __init__(self, file=None, txt=False, cover=False, fileinfo=False, basename=True):
        """
        Initialize the ColorLogger.
        
        Args:
            file (str): Log file path
            txt (bool): Enable text logging
            cover (bool): Overwrite existing log file
            fileinfo (bool): Show file information
            basename (bool): Use basename for display
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
        """Inspect caller information."""
        caller_info = self.inspector.inspect_caller(frame_offset)
        self.caller_class = caller_info['class_name']
        self.fun_name = caller_info['method_name']
    
    def set_format(self, date_on=True, time_on=True, filename_on=True, 
                   class_on=True, fun_on=True, line=True, level=True):
        """
        Set formatting options.
        
        Args:
            date_on (bool): Show date
            time_on (bool): Show time
            filename_on (bool): Show filename
            class_on (bool): Show class name
            fun_on (bool): Show function name
            line (bool): Show line number
            level (bool): Show log level
        """
        self.formatter.set_format(
            date_on=date_on, time_on=time_on, filename_on=filename_on,
            class_on=class_on, fun_on=fun_on, line=line, level=level
        )
    
    def set_level(self, console="DEBUG", text="DEBUG"):
        """
        Set minimum log levels for console and file output.
        
        Args:
            console (str): Minimum level for console output
            text (str): Minimum level for file output
        """
        console_level = LogLevel.validate_level(console)
        text_level = LogLevel.validate_level(text)
        
        self.level_console = LogLevel.LEVEL_DIC[console_level]
        self.level_text = LogLevel.LEVEL_DIC[text_level]
    
    def _log_message(self, level, msg, *args, **kwargs):
        """
        Internal method to handle logging logic.
        
        Args:
            level (str): Log level
            msg (str): Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        try:
            # Find the actual caller frame by skipping logging library frames
            current_frame = inspect.currentframe()
            caller_frame = current_frame.f_back
            
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
                frame_info = self.inspector.get_frame_info(current_frame.f_back)
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
        """Get color for log level."""
        color_map = {
            "DEBUG": self.colors.BLUE,
            "INFO": self.colors.GREEN,
            "WARNING": self.colors.YELLOW,
            "ERROR": self.colors.RED
        }
        return color_map.get(level, self.colors.RESET_ALL)
    
    def debug(self, msg, *args, **kwargs):
        """Log a debug message."""
        self._log_message("DEBUG", msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        """Log an info message."""
        self._log_message("INFO", msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        """Log a warning message."""
        self._log_message("WARNING", msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        """Log an error message."""
        self._log_message("ERROR", msg, *args, **kwargs)
    
    def close(self):
        """Close the logger and cleanup resources."""
        self.file_manager.close()

# Backward compatibility - create default logger instance
logger = ColorLogger()