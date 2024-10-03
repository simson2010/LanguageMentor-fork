# create unit test for vocab_agent with unittest
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.vocab_agent import VocabAgent

class TestVocabAgent(unittest.TestCase):
    def test_init(self):
        agent = VocabAgent()
        self.assertEqual(agent.name, "vocab_study")
        self.assertEqual(agent.prompt_file, "prompts/vocab_study_prompt.txt")
        self.assertEqual(agent.intro_file, None)

if __name__ == "__main__":
    unittest.main()
