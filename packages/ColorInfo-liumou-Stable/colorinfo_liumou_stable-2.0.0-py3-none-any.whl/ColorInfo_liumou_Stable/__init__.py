# -*- encoding: utf-8 -*-
"""
ColorInfo logging module - Modular version compatible with Python 3.5+
"""
from .logger import ColorLogger, logger
from .colors import ColorConstants
from .levels import LogLevel
from .file_manager import FileManager
from .formatter import MessageFormatter
from .inspector import CallStackInspector
from .structured import StructuredLogger, JSONStructuredLogger, sugar

__all__ = [
    "ColorLogger", 
    "logger",
    "ColorConstants",
    "LogLevel", 
    "FileManager",
    "MessageFormatter",
    "CallStackInspector",
    "StructuredLogger",
    "JSONStructuredLogger", 
    "sugar"
]