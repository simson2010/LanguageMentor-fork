#create unit test for session_history with unittest
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.session_history import get_session_history

class TestSessionHistory(unittest.TestCase):
    def test_get_session_history(self):
        session_id = "test_session_id"
        history = get_session_history(session_id)
        self.assertEqual(history.messages, [])

if __name__ == "__main__":
    unittest.main()
