# -*- encoding: utf-8 -*-
"""
File utilities for ColorInfo logging system.
"""
import os
from sys import exit

class FileManager:
    """Handles file operations for logging."""
    
    def __init__(self, file_path=None, txt_mode=False, cover=False, basename=True):
        """
        Initialize file manager.
        
        Args:
            file_path (str): Log file path
            txt_mode (bool): Whether to enable text logging
            cover (bool): Whether to overwrite existing file
            basename (bool): Whether to use basename for display
        """
        self.file_path = file_path
        self.txt_mode = txt_mode
        self.cover = cover
        self.basename = basename
        self.file_name = None
        self.txt_wr = None
        
        if self.txt_mode:
            self._initialize_file()
    
    def _initialize_file(self):
        """Initialize log file operations."""
        if self.file_path is None:
            home_dir = os.getenv('HOME') or os.getenv('USERPROFILE')
            if not home_dir:
                raise EnvironmentError("无法获取用户主目录，请检查环境变量 'HOME' 或 'USERPROFILE'")
            self.file_path = os.path.abspath(os.path.join(home_dir, 'ColorInfo.log'))
        
        try:
            mode = 'w+' if self.cover else 'a+'
            self.txt_wr = open(file=self.file_path, mode=mode, encoding='utf-8')
        except (IOError, OSError) as e:
            print("无法打开文件 '{}'，错误信息: {}".format(self.file_path, e))
            exit(1)
        
        if self.basename:
            self.file_name = os.path.basename(self.file_path)
        else:
            self.file_name = self.file_path
    
    def write_log(self, message):
        """
        Write log message to file.
        
        Args:
            message (str): The log message to write
        """
        if not self.txt_mode or self.txt_wr is None:
            return
        
        try:
            self.txt_wr.write("{}\n".format(message))
            self.txt_wr.flush()
        except (OSError, AttributeError) as e:
            print("写入文件时发生错误: {}".format(str(e)))
    
    def close(self):
        """Close the file handle."""
        if self.txt_wr and hasattr(self.txt_wr, 'close'):
            self.txt_wr.close()
    
    def get_file_info(self):
        """
        Get file information for display.
        
        Returns:
            tuple: (file_path, file_name)
        """
        return self.file_path, self.file_name