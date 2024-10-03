#create unit test for conversation_tab with unittest
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tabs.conversation_tab import ConversationManager

class MockConversationAgent:
    def chat_with_history(self, user_input):
        return f"Mock response to: {user_input}"


class TestConversationTab(unittest.TestCase):
    
    def test_handle_conversation(self):
        user_input = "hello test"
        manager = ConversationManager(MockConversationAgent(), "test title", "test sub")
        botMessage = manager.handle_conversation(user_input,[])
        self.assertEqual(botMessage, f"Mock response to: {user_input}")

    @patch('tabs.conversation_tab.gr')
    def test_create_conversation_tab(self, mock_gr):
        # Arrange
        mock_tab = MagicMock()
        mock_gr.Tab.return_value.__enter__.return_value = mock_tab
        
        manager = ConversationManager(MockConversationAgent(), "Test Title", "Test Subtitle")

        # Act
        manager.create_conversation_tab()

        # Assert
        mock_gr.Tab.assert_called_once_with("Test Title")
        mock_gr.Markdown.assert_called_once_with("## Test Subtitle ")
        mock_gr.Chatbot.assert_called_once()
        mock_gr.ChatInterface.assert_called_once()

        # Check if ChatInterface was called with correct parameters
        chat_interface_call = mock_gr.ChatInterface.call_args
        self.assertIsNotNone(chat_interface_call)
        _, kwargs = chat_interface_call
        self.assertIn('fn', kwargs)
        self.assertIn('chatbot', kwargs)
        self.assertIsNone(kwargs.get('retry_btn'))
        self.assertIsNone(kwargs.get('undo_btn'))
        self.assertEqual(kwargs.get('clear_btn'), "清除历史记录")
        self.assertEqual(kwargs.get('submit_btn'), "发送")


if __name__ == "__main__":
    unittest.main()
