# -*- encoding: utf-8 -*-
"""
ColorInfo 日志系统的调用堆栈检查工具。
"""
import inspect

class CallStackInspector:
    """处理日志上下文的调用堆栈检查。"""
    
    def __init__(self):
        """初始化检查器。"""
        self.caller_frame = None
        self.caller_class = None
        self.caller_method = None
        self.fun_name = None
    
    def inspect_caller(self, frame_offset=1):
        """
        检查调用帧。
        
        Args:
            frame_offset (int): 回退多少个帧
            
        Returns:
            dict: 调用者信息
        """
        try:
            # Get the caller frame
            self.caller_frame = inspect.stack()[frame_offset]
            
            # Get class name safely
            frame_locals = self.caller_frame[0].f_locals
            caller_instance = frame_locals.get('self', None)
            
            if caller_instance and hasattr(caller_instance, '__class__'):
                self.caller_class = caller_instance.__class__.__name__
            else:
                self.caller_class = None
            
            # Get method name
            self.caller_method = self.caller_frame[3]
            self.fun_name = self.caller_method
            
            return {
                'class_name': self.caller_class,
                'method_name': self.caller_method,
                'frame': self.caller_frame
            }
            
        except (IndexError, AttributeError):
            return {
                'class_name': None,
                'method_name': '<unknown>',
                'frame': None
            }
    
    def get_frame_info(self, frame):
        """
        从帧中获取信息。
        
        Args:
            frame: 帧对象
            
        Returns:
            dict: 帧信息
        """
        if frame is None:
            return {
                'filename': '<unknown>',
                'line_num': 0,
                'module_name': '<unknown>'
            }
        
        try:
            frame_info = inspect.getframeinfo(frame)
            return {
                'filename': frame_info.filename,
                'line_num': frame_info.lineno,
                'module_name': frame_info.function
            }
        except Exception:
            return {
                'filename': '<unknown>',
                'line_num': 0,
                'module_name': '<unknown>'
            }
    
    def get_current_frame_info(self):
        """
        获取当前帧的信息。
        
        Returns:
            dict: 当前帧信息
        """
        current_frame = inspect.currentframe()
        if current_frame:
            caller_frame = current_frame.f_back
            if caller_frame:
                return self.get_frame_info(caller_frame)
        
        return {
            'filename': '<unknown>',
            'line_num': 0,
            'module_name': '<unknown>'
        }