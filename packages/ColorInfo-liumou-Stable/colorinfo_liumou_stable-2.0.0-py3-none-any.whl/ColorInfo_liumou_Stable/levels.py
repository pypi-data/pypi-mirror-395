# -*- encoding: utf-8 -*-
"""
Log levels and validation utilities for ColorInfo logging system.
"""

class LogLevel:
    """Log level constants and validation."""
    
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
        Validate and return a valid log level.
        
        Args:
            level (str): The log level to validate
            default (str): Default level if validation fails
            
        Returns:
            str: Validated log level in uppercase
        """
        if not isinstance(level, str) or level.upper() not in LogLevel.LEVEL_LIST:
            return default
        return level.upper()
    
    @staticmethod
    def get_level_value(level):
        """
        Get numeric value for a log level.
        
        Args:
            level (str): The log level
            
        Returns:
            int: Numeric value of the log level
        """
        validated_level = LogLevel.validate_level(level)
        return LogLevel.LEVEL_DIC[validated_level]