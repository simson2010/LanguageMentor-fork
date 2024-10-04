# create unit test for vocab_agent with unittest
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.vocab_agent import VocabAgent

class TestVocabAgent(unittest.TestCase):

    @patch('agents.vocab_agent.get_session_history')
    def test_restart_session(self, mock_get_session_history):
        # Create a mock session history object
        mock_history = MagicMock()
        mock_get_session_history.return_value = mock_history

        # Create an instance of VocabAgent
        agent = VocabAgent(session_id="test_session")

        # Call the restart_session method
        result = agent.restart_session(session_id="test_session")

        # Assertions to check if the session history was cleared
        mock_get_session_history.assert_called_once_with("test_session")
        mock_history.clear.assert_called_once()
        self.assertEqual(result, mock_history)

    @patch('agents.vocab_agent.get_session_history')
    def test_restart_session_no_session_id(self, mock_get_session_history):
        # Create a mock session history object
        mock_history = MagicMock()
        mock_get_session_history.return_value = mock_history

        # Create an instance of VocabAgent without a session_id
        agent = VocabAgent()

        # Call the restart_session method without a session_id
        result = agent.restart_session()

        # Assertions to check if the session history was cleared
        mock_get_session_history.assert_called_once_with(agent.session_id)
        mock_history.clear.assert_called_once()
        self.assertEqual(result, mock_history)

    def test_initialization(self):
        # Test the initialization of VocabAgent
        agent = VocabAgent(session_id="test_session")
        self.assertEqual(agent.name, "vocab_study")
        self.assertEqual(agent.prompt_file, "prompts/vocab_study_prompt.txt")
        self.assertEqual(agent.session_id, "test_session")


if __name__ == "__main__":
    unittest.main()
