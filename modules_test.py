#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from html import escape
from datetime import datetime
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""
    def test_foo(self):
        """Tests foo."""
        pass

class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""
    def test_foo(self):
        """Tests foo."""
        pass

class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests for the display_genai_advice function."""

    @patch('modules.st.markdown')
    def test_valid_input(self, mock_markdown):
        """Tests display_genai_advice with valid input data."""
        timestamp = '2024-01-01 00:00:00'
        content = 'Stay motivated!'
        image = 'http://example.com/image.png'
        # Expected reformat: "01 Jan 2024, 00:00"
        expected_safe_content = escape(str(content))
        expected_safe_timestamp = escape("01 Jan 2024, 00:00")

        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn(expected_safe_timestamp, html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_none_image(self, mock_markdown):
        """Tests display_genai_advice when image is None."""
        timestamp = '2024-01-01 12:00:00'
        content = 'Keep pushing!'
        image = None
        expected_safe_content = escape(str(content))
        # Expected reformat: "01 Jan 2024, 12:00"
        expected_safe_timestamp = escape("01 Jan 2024, 12:00")

        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn(expected_safe_timestamp, html_output)
        self.assertIn("None", html_output)  # None converts to "None"
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_empty_content(self, mock_markdown):
        """Tests display_genai_advice when content is an empty string."""
        timestamp = '2024-01-02 08:30:00'
        content = ''
        image = 'http://example.com/another_image.png'
        expected_safe_content = escape(content)
        # Expected reformat: "02 Jan 2024, 08:30"
        expected_safe_timestamp = escape("02 Jan 2024, 08:30")

        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn(expected_safe_timestamp, html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_none_timestamp(self, mock_markdown):
        """Tests display_genai_advice when timestamp is None."""
        timestamp = None
        content = 'Keep your head up!'
        image = 'http://example.com/image.png'
        expected_safe_content = escape(str(content))
        # When timestamp is None, safe_timestamp becomes an empty string.
        expected_safe_timestamp = escape("")

        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn(expected_safe_timestamp, html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_html_injection(self, mock_markdown):
        """Tests that special characters in content are escaped."""
        timestamp = '2024-01-01 00:00:00'
        content = '<script>alert("xss")</script>'
        image = 'http://example.com/image.png'
        expected_safe_content = escape(content)
        # Expected timestamp: "01 Jan 2024, 00:00"
        expected_safe_timestamp = escape("01 Jan 2024, 00:00")

        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn(expected_safe_timestamp, html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_numeric_content(self, mock_markdown):
        """Tests display_genai_advice when content is numeric."""
        timestamp = '2024-01-01 00:00:00'
        content = 12345
        image = 'http://example.com/image.png'
        expected_safe_content = escape(str(content))
        # Expected timestamp: "01 Jan 2024, 00:00"
        expected_safe_timestamp = escape("01 Jan 2024, 00:00")

        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn(expected_safe_timestamp, html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_extremely_long_content(self, mock_markdown):
        """Tests display_genai_advice with extremely long content."""
        timestamp = '2024-01-01 00:00:00'
        content = "a" * 1000  # 1000 'a' characters
        image = 'http://example.com/image.png'
        expected_safe_content = escape(content)
        # Expected timestamp: "01 Jan 2024, 00:00"
        expected_safe_timestamp = escape("01 Jan 2024, 00:00")

        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn(expected_safe_timestamp, html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_whitespace_content(self, mock_markdown):
        """Tests display_genai_advice with content that is whitespace only."""
        timestamp = '2024-01-01 00:00:00'
        content = '     '
        image = 'http://example.com/image.png'
        expected_safe_content = escape(content)
        # Expected timestamp: "01 Jan 2024, 00:00"
        expected_safe_timestamp = escape("01 Jan 2024, 00:00")

        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn(expected_safe_timestamp, html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_datetime_timestamp(self, mock_markdown):
        """Tests display_genai_advice when timestamp is a datetime object."""
        timestamp = datetime(2024, 1, 1, 0, 0, 0)
        content = 'Happy New Year!'
        image = 'http://example.com/image.png'
        expected_safe_content = escape(content)
        # The datetime object is converted to "2024-01-01 00:00:00", then formatted.
        expected_safe_timestamp = escape("01 Jan 2024, 00:00")

        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn(expected_safe_timestamp, html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_newline_in_content(self, mock_markdown):
        """Tests display_genai_advice with newline characters in content."""
        timestamp = '2024-01-01 00:00:00'
        content = "Hello\nWorld"
        image = 'http://example.com/image.png'
        expected_safe_content = escape(content)
        # Expected timestamp: "01 Jan 2024, 00:00"
        expected_safe_timestamp = escape("01 Jan 2024, 00:00")

        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn(expected_safe_timestamp, html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""
    def test_foo(self):
        """Tests foo."""
        pass

if __name__ == "__main__":
    unittest.main()
