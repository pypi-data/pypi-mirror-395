# -*- encoding: utf-8 -*-
"""
Demonstration of the modular ColorInfo logging system.
Compatible with Python 3.5+
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ColorInfo_liumou_Stable import ColorLogger, ColorConstants, LogLevel, FileManager

def demo_basic_logging():
    """Demonstrate basic logging functionality."""
    print("=== Basic Logging Demo ===")
    
    # Create logger with file output
    logger = ColorLogger(
        file="demo_output.log",
        txt=True,
        cover=True,
        fileinfo=True
    )
    
    # Log messages at different levels
    logger.debug("This is a debug message")
    logger.info("This is an info message") 
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    logger.close()
    print("Basic logging completed. Check demo_output.log for file output.\n")

def demo_formatting_options():
    """Demonstrate formatting options."""
    print("=== Formatting Options Demo ===")
    
    logger = ColorLogger()
    
    # Show different formatting options
    print("Default formatting:")
    logger.info("Message with all formatting options")
    
    print("\nCustom formatting (no date/time):")
    logger.set_format(date_on=False, time_on=False)
    logger.info("Message without date and time")
    
    print("\nMinimal formatting:")
    logger.set_format(
        date_on=False, time_on=False, filename_on=False,
        class_on=False, fun_on=False, line=False, level=False
    )
    logger.info("Message with minimal formatting")
    
    logger.close()
    print()

def demo_log_levels():
    """Demonstrate log level filtering."""
    print("=== Log Levels Demo ===")
    
    logger = ColorLogger()
    
    print("All levels visible (DEBUG and above):")
    logger.set_level(console="DEBUG", text="DEBUG")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    print("\nOnly INFO and above:")
    logger.set_level(console="INFO", text="INFO")
    logger.debug("This debug message should not appear")
    logger.info("This info message should appear")
    logger.warning("This warning should appear")
    logger.error("This error should appear")
    
    logger.close()
    print()

def demo_modular_components():
    """Demonstrate individual modular components."""
    print("=== Modular Components Demo ===")
    
    # Use ColorConstants directly
    colors = ColorConstants()
    print("Available colors:")
    print("{}Red{}, {}Green{}, {}Yellow{}, {}Blue{}".format(
        colors.RED, colors.RESET_ALL,
        colors.GREEN, colors.RESET_ALL,
        colors.YELLOW, colors.RESET_ALL,
        colors.BLUE, colors.RESET_ALL
    ))
    
    # Use LogLevel utilities
    print("\nLog level validation:")
    print("Valid level 'info':", LogLevel.validate_level("info"))
    print("Invalid level 'invalid':", LogLevel.validate_level("invalid"))
    print("Level values:", LogLevel.LEVEL_DIC)
    
    # Use FileManager directly
    print("\nFileManager demo:")
    file_mgr = FileManager(txt_mode=True, basename=True)
    file_path, file_name = file_mgr.get_file_info()
    print("Default log file:", file_name)
    file_mgr.close()
    
    print()

def demo_class_usage():
    """Demonstrate usage within a class."""
    print("=== Class Usage Demo ===")
    
    class DemoClass:
        def __init__(self):
            self.logger = ColorLogger(txt=True, file="class_demo.log")
            self.logger.info("DemoClass initialized")
        
        def do_something(self):
            self.logger.debug("Entering do_something method")
            self.logger.info("Performing some operation")
            self.logger.warning("This is a warning from a class method")
            self.logger.error("This is an error from a class method")
        
        def cleanup(self):
            self.logger.info("Cleaning up DemoClass")
            self.logger.close()
    
    demo = DemoClass()
    demo.do_something()
    demo.cleanup()
    print("Class demo completed. Check class_demo.log for output.\n")

def demo_backward_compatibility():
    """Demonstrate backward compatibility with original API."""
    print("=== Backward Compatibility Demo ===")
    
    # This should work exactly like the original
    from ColorInfo_liumou_Stable import logger
    
    logger.info("Using default logger instance")
    logger.debug("Debug with default logger")
    logger.warning("Warning with default logger")
    logger.error("Error with default logger")
    
    print("Backward compatibility demo completed.\n")

def main():
    """Run all demonstrations."""
    print("ColorInfo Modular Logging System Demo")
    print("=" * 40)
    print()
    
    try:
        demo_basic_logging()
        demo_formatting_options()
        demo_log_levels()
        demo_modular_components()
        demo_class_usage()
        demo_backward_compatibility()
        
        print("All demos completed successfully!")
        print("Check the generated .log files for file output examples.")
        
    except Exception as e:
        print("Demo failed with error:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()