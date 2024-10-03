#create unit test for agent_base with unittest
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.agent_base import AgentBase

class TestAgentBase(unittest.TestCase):
    def test_init(self):
        agent = AgentBase("test", "prompts/hotel_checkin_prompt.txt", "content/intro/hotel_checkin.json")
        self.assertEqual(agent.name, "test")
        self.assertEqual(agent.prompt_file, "prompts/hotel_checkin_prompt.txt")
        self.assertEqual(agent.intro_file, "content/intro/hotel_checkin.json")  

if __name__ == "__main__":
    unittest.main()
