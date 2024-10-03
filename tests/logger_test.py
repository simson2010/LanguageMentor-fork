#create unit test for logger with unittest
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.logger import LOG

class TestLogger(unittest.TestCase):
    def test_logger(self):
        LOG.info("This is a test info message")
        LOG.error("This is a test error message")

if __name__ == "__main__":
    unittest.main()