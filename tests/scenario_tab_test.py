# tests/scenario_tab_test.py

import os
import sys
import unittest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tabs.scenario_tab import ScenarioManager  # Adjust the import based on your project structure

class MockConversationAgent:
    def chat_with_history(self, user_input):
        return f"Mock response to: {user_input}"
    
    def start_new_session(self, session_id=None):
        return "init message"
    
test_agents = {
    "job_interview": MockConversationAgent()
}
    
class TestScenarioManager(unittest.TestCase):

    def setUp(self):
        self.manager = ScenarioManager(test_agents, [("job interview","job_interview")], "title", "subtitle")

    def test_get_page_desc_existing_file(self):
        # Test getting description from an existing file
        scenario = 'job_interview'  # Ensure this file exists in content/page/
        description = self.manager.get_page_desc(scenario)
        self.assertIsInstance(description, str)  # Check if the description is a string

    def test_get_page_desc_non_existing_file(self):
        # Test getting description from a non-existing file
        scenario = 'non_existing_scenario'
        description = self.manager.get_page_desc(scenario)
        self.assertEqual(description, "场景介绍文件未找到。")  # Check for the error message

    def test_start_new_scenario_chatbot(self):
        # Test starting a new scenario chatbot
        scenario = 'job_interview'
        chatbot = self.manager.start_new_scenario_chatbot(scenario)
        self.assertIsNotNone(chatbot)  # Ensure chatbot is created

    def test_handle_scenario(self):
        # Test handling a scenario
        scenario = 'job_interview'
        user_input = "Hello"
        chat_history = []  # Assuming chat history is a list
        response = self.manager.handle_scenario(user_input, chat_history, scenario)
        self.assertIsInstance(response, str)  # Check if the response is a string

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()