#create unit test for agent_base with unittest
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.agent_base import AgentBase

class TestAgentBase(unittest.TestCase):

    def setUp(self):
        # Create a temporary prompt file for testing
        self.invalid_intro_file = 'invalid_intro.json'
        self.dummy_prompt_file = 'dummy_prompt.txt'
        self.invalidJson = "This is not a valid JSON."
        self.dummyPrompt= "This is prompt file"
        
        self.valid_json_file = "valid_intro.json"
        self.validJSON = """[
            "This is a intro",
            "That is a intro"
        ]"""
        self.prepareTestFile()

    def tearDown(self) -> None:
        self.removeTestFile()
        return super().tearDown()

    def prepareTestFile(self):
        # Create a temporary invalid JSON file for testing
        with open(self.invalid_intro_file, 'w', encoding='utf-8') as f:
            f.write(self.invalidJson)
        with open(self.dummy_prompt_file, 'w', encoding='utf-8') as f:
            f.write(self.dummyPrompt)
        with open(self.valid_json_file, 'w', encoding='utf-8') as f:
            f.write(self.validJSON)
        
    def removeTestFile(self):
        import os
        os.remove(self.invalid_intro_file)
        os.remove(self.dummy_prompt_file)
        os.remove(self.valid_json_file)

    def test_init(self):
        testAgent = AgentBase("test", self.dummy_prompt_file, self.valid_json_file)
        self.assertEqual(testAgent.name, "test")
        self.assertEqual(testAgent.prompt_file, self.dummy_prompt_file)
        self.assertEqual(testAgent.intro_file, self.valid_json_file)

    def test_load_prompt_success(self):
        # Test if load_prompt() returns the correct content
        testAgent = AgentBase("test", self.dummy_prompt_file, self.valid_json_file)
        result = testAgent.load_prompt()
        self.assertEqual(result, self.dummyPrompt)

    def test_load_prompt_file_not_found(self):
        # Test if load_prompt() raises FileNotFoundError for a non-existent file
        testAgent = AgentBase("TestAgent", self.dummy_prompt_file, self.valid_json_file)
        testAgent.prompt_file = "non_existent_file.txt"
        with self.assertRaises(FileNotFoundError) as context:
            testAgent.load_prompt()
        self.assertEqual(str(context.exception), "找不到提示文件 non_existent_file.txt!")

    def test_load_intro_success(self):
        # Test if load_intro() returns the correct content
        testAgent = AgentBase("TestAgent", self.dummy_prompt_file, self.valid_json_file)
        result = testAgent.load_intro()
        self.assertEqual(result[0], "This is a intro")
        self.assertEqual(result[1], "That is a intro")

    def test_load_intro_file_not_found(self):
        # Test if load_intro() raises FileNotFoundError for a non-existent file
        testAgent = AgentBase("TestAgent", self.dummy_prompt_file, self.valid_json_file)
        testAgent.intro_file = 'non_existent_file.json'
        with self.assertRaises(FileNotFoundError) as context:
            testAgent.load_intro()
        self.assertEqual(str(context.exception), "找不到初始消息文件 non_existent_file.json!")

    def test_load_intro_invalid_json(self):
        
        testAgent = AgentBase(name="TestAgent", prompt_file=self.dummy_prompt_file, intro_file=self.valid_json_file)
        testAgent.intro_file = self.invalid_intro_file
        with self.assertRaises(ValueError) as context:
            testAgent.load_intro()
        self.assertEqual(str(context.exception), f"初始消息文件 {self.invalid_intro_file} 包含无效的 JSON!")

        # Clean up the invalid file


if __name__ == "__main__":
    unittest.main()
