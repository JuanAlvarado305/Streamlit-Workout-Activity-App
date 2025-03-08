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
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

# Write your tests below

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
    """Tests the display_genai_advice function."""

    @patch('modules.create_component')
    def test_valid_input(self, mock_create_component):
        """Tests display_genai_advice with valid input data."""
        timestamp = '2024-01-01 00:00:00'
        content = 'Stay motivated!'
        image = 'http://example.com/image.png'
        expected_data = {
            'TIME': timestamp,
            'CONTENT': content,
            'IMAGE': image,
        }
        expected_html_file_name = "genai_advice_module"

        display_genai_advice(timestamp, content, image)
        mock_create_component.assert_called_once_with(expected_data, expected_html_file_name)

    @patch('modules.create_component')
    def test_none_image(self, mock_create_component):
        """Tests display_genai_advice when image is None."""
        timestamp = '2024-01-01 12:00:00'
        content = 'Keep pushing!'
        image = None
        expected_data = {
            'TIME': timestamp,
            'CONTENT': content,
            'IMAGE': image,
        }
        expected_html_file_name = "genai_advice_module"

        display_genai_advice(timestamp, content, image)
        mock_create_component.assert_called_once_with(expected_data, expected_html_file_name)

    @patch('modules.create_component')
    def test_empty_content(self, mock_create_component):
        """Tests display_genai_advice when content is an empty string."""
        timestamp = '2024-01-02 08:30:00'
        content = ''
        image = 'http://example.com/another_image.png'
        expected_data = {
            'TIME': timestamp,
            'CONTENT': content,
            'IMAGE': image,
        }
        expected_html_file_name = "genai_advice_module"

        display_genai_advice(timestamp, content, image)
        mock_create_component.assert_called_once_with(expected_data, expected_html_file_name)

    @patch('modules.create_component')
    def test_none_timestamp(self, mock_create_component):
        """Tests display_genai_advice when timestamp is None."""
        timestamp = None
        content = 'Keep your head up!'
        image = 'http://example.com/image.png'
        expected_data = {
            'TIME': timestamp,
            'CONTENT': content,
            'IMAGE': image,
        }
        expected_html_file_name = "genai_advice_module"

        display_genai_advice(timestamp, content, image)
        mock_create_component.assert_called_once_with(expected_data, expected_html_file_name)


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def test_foo(self):
        """Tests foo."""
        pass


if __name__ == "__main__":
    unittest.main()
