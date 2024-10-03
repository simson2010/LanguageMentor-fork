#create unit test for conversation_agent with unittest
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.conversation_agent import ConversationAgent

class TestConversationAgent(unittest.TestCase):
    def test_init(self):
        agent = ConversationAgent()
        self.assertEqual(agent.name, "conversation")
        self.assertEqual(agent.prompt_file, "prompts/conversation_prompt.txt")
        self.assertEqual(agent.intro_file, None)

if __name__ == "__main__":
    unittest.main()

