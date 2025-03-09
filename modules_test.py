#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts
from datetime import datetime
# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    def test_display_post_with_image(self):
        """Tests display_post with an image."""
        username = "test_user"
        user_image = "https://picsum.photos/50/50"
        timestamp = "2024-03-15 12:00:00"
        content = "This is a test post with an image."
        post_image = "https://picsum.photos/600/400"

        with patch("streamlit.container") as mock_container, \
             patch("streamlit.columns") as mock_columns, \
             patch("streamlit.markdown") as mock_markdown, \
             patch("streamlit.image") as mock_image:

            mock_col1 = MagicMock()
            mock_col2 = MagicMock()
            mock_columns.return_value = (mock_col1, mock_col2)

            display_post(username, user_image, timestamp, content, post_image)

            # Verify that streamlit.container was called
            mock_container.assert_called_once()

            # Verify that streamlit.columns was called with the correct arguments
            mock_columns.assert_called_once_with([1, 11])

            # Verify that streamlit.markdown was called for the profile image
            mock_markdown.assert_any_call(f'<img src="{user_image}" class="profile-pic">', unsafe_allow_html=True)

            # Verify that streamlit.markdown was called for the username and timestamp
            formatted_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y, %H:%M")
            mock_markdown.assert_any_call(
                f"""
                <div class="post-info">
                    <strong>{username}</strong>
                    <span>{formatted_time}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Verify that streamlit.markdown was called for the post content
            mock_markdown.assert_any_call(f"<p class='post-content'>{content} #GoogleTech2025</p>", unsafe_allow_html=True)

            # Verify that streamlit.image was called for the post image
            mock_image.assert_called_once_with(post_image, use_container_width=True)

    def test_display_post_without_image(self):
        """Tests display_post without an image."""
        username = "test_user"
        user_image = "https://picsum.photos/50/50"
        timestamp = "2024-03-15 12:00:00"
        content = "This is a test post without an image."
        post_image = None

        with patch("streamlit.container") as mock_container, \
             patch("streamlit.columns") as mock_columns, \
             patch("streamlit.markdown") as mock_markdown, \
             patch("streamlit.image") as mock_image:

            mock_col1 = MagicMock()
            mock_col2 = MagicMock()
            mock_columns.return_value = (mock_col1, mock_col2)

            display_post(username, user_image, timestamp, content, post_image)

            # Verify that streamlit.image was not called
            mock_image.assert_not_called()

class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def test_foo(self):
        """Tests foo."""
        pass


if __name__ == "__main__":
    unittest.main()
