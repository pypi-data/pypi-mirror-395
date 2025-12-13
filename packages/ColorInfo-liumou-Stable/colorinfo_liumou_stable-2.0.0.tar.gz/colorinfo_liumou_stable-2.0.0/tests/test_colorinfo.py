# -*- encoding: utf-8 -*-
"""
Test suite for ColorInfo modular logging system.
Compatible with Python 3.5+
"""
import unittest
import os
import tempfile
import shutil
from ColorInfo_liumou_Stable import ColorLogger, ColorConstants, LogLevel, FileManager

class TestColorConstants(unittest.TestCase):
    """Test ColorConstants class."""
    
    def test_basic_colors(self):
        """Test basic color constants."""
        colors = ColorConstants()
        self.assertEqual(colors.RED, "\033[31m")
        self.assertEqual(colors.GREEN, "\033[32m")
        self.assertEqual(colors.YELLOW, "\033[33m")
        self.assertEqual(colors.BLUE, "\033[34m")
        self.assertEqual(colors.RESET_ALL, "\033[0m")
    
    def test_additional_colors(self):
        """Test additional color constants."""
        colors = ColorConstants()
        self.assertEqual(colors.MAGENTA, "\033[35m")
        self.assertEqual(colors.CYAN, "\033[36m")
        self.assertEqual(colors.WHITE, "\033[37m")
        self.assertEqual(colors.BLACK, "\033[30m")

class TestLogLevel(unittest.TestCase):
    """Test LogLevel class."""
    
    def test_validate_level_valid(self):
        """Test valid level validation."""
        self.assertEqual(LogLevel.validate_level("debug"), "DEBUG")
        self.assertEqual(LogLevel.validate_level("INFO"), "INFO")
        self.assertEqual(LogLevel.validate_level("warning"), "WARNING")
        self.assertEqual(LogLevel.validate_level("ERROR"), "ERROR")
    
    def test_validate_level_invalid(self):
        """Test invalid level validation."""
        self.assertEqual(LogLevel.validate_level("invalid"), "DEBUG")
        self.assertEqual(LogLevel.validate_level(""), "DEBUG")
        self.assertEqual(LogLevel.validate_level(None, default="INFO"), "INFO")
    
    def test_get_level_value(self):
        """Test getting level numeric values."""
        self.assertEqual(LogLevel.get_level_value("DEBUG"), 0)
        self.assertEqual(LogLevel.get_level_value("INFO"), 1)
        self.assertEqual(LogLevel.get_level_value("WARNING"), 2)
        self.assertEqual(LogLevel.get_level_value("ERROR"), 3)

class TestFileManager(unittest.TestCase):
    """Test FileManager class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.log")
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_file_manager_init(self):
        """Test FileManager initialization."""
        manager = FileManager(file_path=self.test_file, txt_mode=True)
        self.assertEqual(manager.file_path, self.test_file)
        self.assertTrue(manager.txt_mode)
        manager.close()
    
    def test_write_log(self):
        """Test writing log messages."""
        manager = FileManager(file_path=self.test_file, txt_mode=True)
        test_message = "Test log message"
        manager.write_log(test_message)
        manager.close()
        
        # Verify file was created and contains message
        self.assertTrue(os.path.exists(self.test_file))
        with open(self.test_file, 'r') as f:
            content = f.read()
            self.assertIn(test_message, content)
    
    def test_basename_handling(self):
        """Test basename handling."""
        manager = FileManager(file_path=self.test_file, txt_mode=True, basename=True)
        file_path, file_name = manager.get_file_info()
        self.assertEqual(file_name, "test.log")
        manager.close()

class TestColorLogger(unittest.TestCase):
    """Test ColorLogger class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.log")
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_logger_init(self):
        """Test logger initialization."""
        logger = ColorLogger()
        self.assertIsNotNone(logger.colors)
        self.assertIsNotNone(logger.file_manager)
        self.assertIsNotNone(logger.formatter)
        self.assertIsNotNone(logger.inspector)
        logger.close()
    
    def test_logger_with_file(self):
        """Test logger with file output."""
        logger = ColorLogger(file=self.test_file, txt=True)
        self.assertTrue(logger.txt_mode)
        logger.info("Test info message")
        logger.close()
        
        # Verify file was created
        self.assertTrue(os.path.exists(self.test_file))
    
    def test_set_level(self):
        """Test setting log levels."""
        logger = ColorLogger()
        logger.set_level(console="INFO", text="WARNING")
        self.assertEqual(logger.level_console, 1)
        self.assertEqual(logger.level_text, 2)
        logger.close()
    
    def test_set_format(self):
        """Test setting format options."""
        logger = ColorLogger()
        logger.set_format(date_on=False, time_on=False, filename_on=False)
        self.assertFalse(logger.formatter.format_date)
        self.assertFalse(logger.formatter.format_time)
        self.assertFalse(logger.formatter.format_filename)
        logger.close()
    
    def test_debug_logging(self):
        """Test debug level logging."""
        logger = ColorLogger()
        logger.debug("Debug test message")
        logger.close()
    
    def test_info_logging(self):
        """Test info level logging."""
        logger = ColorLogger()
        logger.info("Info test message")
        logger.close()
    
    def test_warning_logging(self):
        """Test warning level logging."""
        logger = ColorLogger()
        logger.warning("Warning test message")
        logger.close()
    
    def test_error_logging(self):
        """Test error level logging."""
        logger = ColorLogger()
        logger.error("Error test message")
        logger.close()
    
    def test_logging_with_args(self):
        """Test logging with additional arguments."""
        logger = ColorLogger()
        logger.info("Test message", "arg1", "arg2", key="value")
        logger.close()
    
    def test_backward_compatibility(self):
        """Test backward compatibility with original API."""
        from ColorInfo_liumou_Stable import logger as default_logger
        
        # Test that default logger works
        default_logger.info("Backward compatibility test")
        default_logger.debug("Debug message")
        default_logger.warning("Warning message")
        default_logger.error("Error message")

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "integration_test.log")
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_full_logging_workflow(self):
        """Test complete logging workflow."""
        logger = ColorLogger(
            file=self.test_file,
            txt=True,
            cover=True,
            fileinfo=True,
            basename=False
        )
        
        # Set levels
        logger.set_level(console="DEBUG", text="INFO")
        
        # Set format
        logger.set_format(
            date_on=True,
            time_on=True,
            filename_on=True,
            class_on=True,
            fun_on=True,
            line=True,
            level=True
        )
        
        # Log messages at different levels
        logger.debug("Debug message - should appear in console only")
        logger.info("Info message - should appear in both")
        logger.warning("Warning message - should appear in both")
        logger.error("Error message - should appear in both")
        
        logger.close()
        
        # Verify file content
        self.assertTrue(os.path.exists(self.test_file))
        with open(self.test_file, 'r') as f:
            content = f.read()
            # Debug should not be in file (level set to INFO)
            self.assertNotIn("Debug message", content)
            # Others should be in file
            self.assertIn("Info message", content)
            self.assertIn("Warning message", content)
            self.assertIn("Error message", content)

if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestColorConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestLogLevel))
    suite.addTests(loader.loadTestsFromTestCase(TestFileManager))
    suite.addTests(loader.loadTestsFromTestCase(TestColorLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)