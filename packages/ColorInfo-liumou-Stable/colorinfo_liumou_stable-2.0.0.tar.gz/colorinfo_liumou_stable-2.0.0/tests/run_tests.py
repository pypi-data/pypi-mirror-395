# -*- encoding: utf-8 -*-
"""
Test runner for ColorInfo modular logging system.
"""
import sys
import os
import unittest

def run_tests():
    """Run all tests."""
    # Add src to path
    src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
    sys.path.insert(0, src_path)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)