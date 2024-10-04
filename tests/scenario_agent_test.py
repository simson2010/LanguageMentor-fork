#create unit test for scenario_agent with unittest
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.scenario_agent import ScenarioAgent

class TestScenarioAgent(unittest.TestCase):

    def setUp(self):
        self.test_scenario="test_scenario"
        self.test_prompt = "Test Prompt"
        self.test_invalid_intro = "Test Invalid Intro"
        self.test_intro = """[
            "Test Intro"
        ]"""

        self.prepareTestFile()

    def tearDown(self) -> None:
        self.removeTestFiles()
        return super().tearDown()

    def prepareTestFile(self):
        self.prompt_file = f"prompts/{self.test_scenario}_prompt.txt"
        self.intro_file = f"content/intro/{self.test_scenario}.json"
        self.invalid_intro_file = f"content/intro/invalid_{self.test_scenario}.json"
        
        with open(self.prompt_file, 'w', encoding='utf-8') as f:
            f.write(self.test_prompt)
        with open(self.intro_file, 'w', encoding='utf-8') as f:
            f.write(self.test_intro)
        with open(self.invalid_intro_file, 'w', encoding='utf-8') as f:
            f.write(self.test_invalid_intro)

    def removeTestFiles(self):
        import os
        os.remove(self.prompt_file)
        os.remove(self.intro_file)
        os.remove(self.invalid_intro_file)


    @patch('agents.scenario_agent.get_session_history')
    def test_start_new_session_with_new_session(self, mock_get_session_history):
        # Create a mock session history object
        mock_history = MagicMock()
        mock_history.messages = []  # Simulate no previous messages
        mock_get_session_history.return_value = mock_history

        # Create an instance of ScenarioAgent
        agent = ScenarioAgent(scenario_name="test_scenario", session_id="test_session")
        agent.intro_messages = ["Welcome to the test scenario!", "Let's begin!"]

        # Call the start_new_session method
        result = agent.start_new_session(session_id="test_session")

        # Assertions to check if the initial AI message was added to history
        mock_get_session_history.assert_called_once_with("test_session")
        mock_history.add_message.assert_called_once()
        self.assertIn(result, agent.intro_messages)  # Check if the result is one of the intro messages

    @patch('agents.scenario_agent.get_session_history')
    def test_start_new_session_with_existing_session(self, mock_get_session_history):
        # Create a mock session history object
        mock_history = MagicMock()
        mock_history.messages = [MagicMock(content="Previous message")]  # Simulate existing messages
        mock_get_session_history.return_value = mock_history

        # Create an instance of ScenarioAgent
        agent = ScenarioAgent(scenario_name="test_scenario", session_id="test_session")

        # Call the start_new_session method
        result = agent.start_new_session(session_id="test_session")

        # Assertions to check if the last message was returned
        mock_get_session_history.assert_called_once_with("test_session")
        self.assertEqual(result, "Previous message")  # Check if the result is the last message

    def test_initialization(self):
        # Test the initialization of ScenarioAgent
        agent = ScenarioAgent(scenario_name="test_scenario", session_id="test_session")
        self.assertEqual(agent.name, "test_scenario")
        self.assertEqual(agent.prompt_file, self.prompt_file)
        self.assertEqual(agent.intro_file, self.intro_file)
        self.assertEqual(agent.session_id, "test_session")

    @patch('agents.scenario_agent.get_session_history')
    def test_sessionIdNone(self, mock_get_session_history):
        # Create a mock session history object
        mock_history = MagicMock()
        mock_history.messages = [MagicMock(content="Previous message")]  # Simulate existing messages
        mock_get_session_history.return_value = mock_history

        # Create an instance of ScenarioAgent with session_id is None
        agent = ScenarioAgent(scenario_name="test_scenario")

        # Call the start_new_session method without session_id passing in
        result = agent.start_new_session()

        # Assertions to check if the last message was returned
        # without passing in session_id, it would be same with the name
        mock_get_session_history.assert_called_once_with("test_scenario")
        self.assertEqual(result, "Previous message")

if __name__ == "__main__":
    unittest.main()
