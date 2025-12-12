"""Unit tests for ai_helpers.core using mocks."""

from types import SimpleNamespace
import unittest
from unittest.mock import patch

from ai_helpers.core import format_response, get_response, summarize_text


class DummyChoice:
    def __init__(self, text=None, message_content=None):
        if message_content is not None:
            self.message = SimpleNamespace(content=message_content)
        else:
            self.text = text


class TestCoreHelpers(unittest.TestCase):
    def test_format_response_cleans_text(self):
        raw = "  Hello   world\n\n\nThis   is   a   test.  "
        out = format_response(raw)
        self.assertIn("Hello world", out)
        self.assertNotIn("  ", out)

    @patch("ai_helpers.core._ensure_api_key")
    @patch("ai_helpers.core.openai.ChatCompletion.create")
    def test_get_response_mocked(self, mock_create, mock_ensure):
        # Arrange: create a fake response object
        dummy = SimpleNamespace(choices=[DummyChoice(message_content="Mocked reply")])
        mock_create.return_value = dummy

        # Act
        res = get_response("Say hi")

        # Assert
        self.assertEqual(res, "Mocked reply")

    @patch("ai_helpers.core.get_response")
    def test_summarize_text_uses_get_response(self, mock_get):
        mock_get.return_value = "Short summary"
        out = summarize_text("Long text here")
        self.assertEqual(out, "Short summary")


if __name__ == "__main__":
    unittest.main()
