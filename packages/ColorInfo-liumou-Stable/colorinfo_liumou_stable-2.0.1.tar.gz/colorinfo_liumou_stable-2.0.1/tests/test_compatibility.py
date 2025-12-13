# -*- encoding: utf-8 -*-
"""
Compatibility test to ensure original demo.py works with refactored code.
"""
import unittest
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility with original API."""
    
    def test_original_imports(self):
        """Test that original imports still work."""
        try:
            from ColorInfo_liumou_Stable import ColorLogger, logger
            self.assertIsNotNone(ColorLogger)
            self.assertIsNotNone(logger)
        except ImportError as e:
            self.fail("Import failed: {}".format(str(e)))
    
    def test_original_demo_functionality(self):
        """Test original demo functionality."""
        from ColorInfo_liumou_Stable import ColorLogger, logger
        
        # Test basic logging
        logger.info("Test backward compatibility")
        logger.debug("Debug test")
        logger.warning("Warning test")
        logger.error("Error test")
        
        # Test ColorLogger instantiation
        log = ColorLogger(txt=False, fileinfo=True, basename=False)
        log.info(msg='1', x="23")
        log.error('2', '22', '222')
        log.debug('3', '21')
        log.warning('4', '20', 22)
        log.close()
    
    def test_class_usage(self):
        """Test class-based usage from original demo."""
        from ColorInfo_liumou_Stable import logger
        
        class Demo:
            def __init__(self):
                self.logger = logger
                self.logger.info("初始化")

            def de(self):
                self.logger.debug("de1")
                logger.info("de2")
                logger.warning("de3")
                logger.error("de4")
        
        # Test the class
        d = Demo()
        d.de()

if __name__ == '__main__':
    unittest.main()