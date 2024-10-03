#create unit test for scenario_agent with unittest
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.scenario_agent import ScenarioAgent

class TestScenarioAgent(unittest.TestCase):
    def test_initHotelCheckin(self):
        agent = ScenarioAgent("hotel_checkin")
        self.assertEqual(agent.name, "hotel_checkin")
        self.assertEqual(agent.prompt_file, "prompts/hotel_checkin_prompt.txt")
        self.assertEqual(agent.intro_file, "content/intro/hotel_checkin.json")

    def test_initJobInterview(self):
        agent = ScenarioAgent("job_interview")
        self.assertEqual(agent.name, "job_interview")
        self.assertEqual(agent.prompt_file, "prompts/job_interview_prompt.txt")
        self.assertEqual(agent.intro_file, "content/intro/job_interview.json")

if __name__ == "__main__":
    unittest.main()
