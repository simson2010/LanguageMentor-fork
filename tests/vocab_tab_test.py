import unittest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tabs.vocab_tab import VocabManager

class TestVocabManager(unittest.TestCase):

    def setUp(self):
        # 创建一个 VocabManager 实例，并使用 MagicMock 模拟 VocabAgent
        self.vocab_manager = VocabManager(agent=MagicMock(), feature="vocab_study")

    def test_get_page_desc_file_found(self):
        # 测试获取页面描述时文件存在的情况
        feature = 'vocab_study'
        with open(f"content/page/{feature}.md", "r", encoding="utf-8") as file:
            scenario_intro = file.read().strip()
        result = self.vocab_manager.get_page_desc("vocab_study")
        self.assertEqual(result, scenario_intro)

    def test_get_page_desc_file_not_found(self):
        # 测试获取页面描述时文件不存在的情况
        
        result = self.vocab_manager.get_page_desc("vocab_study_not_found")
        self.assertEqual(result, "词汇学习介绍文件未找到。")

    def test_restart_vocab_study_chatbot(self):
        # 测试重启聊天机器人会话
        self.vocab_manager.agent.restart_session = MagicMock()
        self.vocab_manager.agent.chat_with_history = MagicMock(return_value="机器人的回应")
        chatbot = self.vocab_manager.restart_vocab_study_chatbot()
        self.assertIn("机器人的回应", chatbot.value[0])

    def test_handle_vocab(self):
        # 测试处理用户输入的单词学习消息
        self.vocab_manager.agent.chat_with_history = MagicMock(return_value="机器人的回应")
        bot_message = self.vocab_manager.handle_vocab("用户输入", [])
        self.assertEqual(bot_message, "机器人的回应")

    @patch('gradio.Tab')
    @patch('gradio.Markdown')
    @patch('gradio.Chatbot')
    @patch('gradio.ClearButton')
    @patch('gradio.ChatInterface')
    def test_create_vocab_tab(self, mock_chat_interface, mock_clear_button, mock_chatbot, mock_markdown, mock_tab):
        # Mock the return value of get_page_desc
        self.vocab_manager.get_page_desc = MagicMock(return_value="测试介绍内容")

        # Call the method to test
        self.vocab_manager.create_vocab_tab()

        # Assertions to check if the Gradio components were called correctly
        mock_tab.assert_called_once_with(self.vocab_manager.title)
        mock_markdown.assert_any_call(f"## {self.vocab_manager.subtitle}")
        mock_markdown.assert_any_call("测试介绍内容")
        mock_chatbot.assert_called_once_with(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>开始学习新单词吧！",
            height=800,
        )
        mock_clear_button.assert_called_once_with(value="下一关")
        mock_chat_interface.assert_called_once_with(
            fn=self.vocab_manager.handle_vocab,
            chatbot=mock_chatbot.return_value,
            retry_btn=None,
            undo_btn=None,
            clear_btn=None,
            submit_btn="发送",
        )

if __name__ == '__main__':
    unittest.main()