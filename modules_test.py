#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# (Modified minimally so that the tests match your original modules.py.)
#############################################################################

import unittest
from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest
from html import escape
from datetime import datetime
from modules import (
    display_post, 
    display_activity_summary, 
    display_genai_advice, 
    display_recent_workouts, 
    display_user_sensor_data, 
    insert_post
)

# ---------------------------
# Tests for display_post
# ---------------------------
class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function with refactored arguments."""
    def setUp(self):
        self.mock_user = {
            "username": "test_user",
            "profile_image": "https://picsum.photos/50/50"
        }

    def fake_get_user_profile(self, user_id):
        return self.mock_user

    @patch("modules.get_user_profile")
    def test_display_post_with_image(self, mock_get_profile):
        """Tests display_post with an image."""
        mock_get_profile.return_value = self.mock_user
        post = {
            "PostId": "post1",
            "AuthorId": "user1",
            "Timestamp": datetime.strptime("2024-03-15 12:00:00", "%Y-%m-%d %H:%M:%S"),
            "Content": "This is a test post with an image.",
            "ImageUrl": "https://picsum.photos/600/400"
        }

        with patch("streamlit.container") as mock_container, \
             patch("streamlit.columns") as mock_columns, \
             patch("streamlit.markdown") as mock_markdown, \
             patch("streamlit.image") as mock_image:

            mock_col1 = MagicMock()
            mock_col2 = MagicMock()
            mock_columns.return_value = (mock_col1, mock_col2)

            display_post(post, get_user_data=self.fake_get_user_profile)

            mock_container.assert_called_once()
            mock_columns.assert_called_once_with([1, 11])
            mock_markdown.assert_any_call(
                f'<img src="{self.mock_user["profile_image"]}" class="profile-pic">',
                unsafe_allow_html=True
            )
            formatted_time = post["Timestamp"].strftime("%d %b %Y, %I:%M %p")
            mock_markdown.assert_any_call(
                f"""
                <div class="post-info">
                    <strong>{self.mock_user["username"]}</strong>
                    <span>{formatted_time}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            mock_markdown.assert_any_call(
                f"<p class='post-content'>{post['Content']} #GoogleTech2025</p>",
                unsafe_allow_html=True
            )
            mock_image.assert_called_once_with(post["ImageUrl"], use_container_width=True)

    @patch("modules.get_user_profile")
    def test_display_post_without_image(self, mock_get_profile):
        """Tests display_post without an image."""
        mock_get_profile.return_value = self.mock_user
        post = {
            "PostId": "post1",
            "AuthorId": "user1",
            "Timestamp": datetime.strptime("2024-03-15 12:00:00", "%Y-%m-%d %H:%M:%S"),
            "Content": "This is a test post without an image.",
            "ImageUrl": None
        }

        with patch("streamlit.container") as mock_container, \
             patch("streamlit.columns") as mock_columns, \
             patch("streamlit.markdown") as mock_markdown, \
             patch("streamlit.image") as mock_image:

            mock_col1 = MagicMock()
            mock_col2 = MagicMock()
            mock_columns.return_value = (mock_col1, mock_col2)

            display_post(post, get_user_data=self.fake_get_user_profile)

            mock_image.assert_not_called()


# ---------------------------
# Tests for display_activity_summary
# ---------------------------
class TestDisplayActivitySummary(unittest.TestCase):
    @patch('modules.create_component')
    def test_empty_workouts_list(self, mock_create_component):
        """Tests that an empty workouts list is handled correctly."""
        empty_workouts = []
        display_activity_summary(empty_workouts)
        
        mock_create_component.assert_called_once()
        args = mock_create_component.call_args[0]
        data = args[0]
        self.assertEqual(data['WORKOUT_COUNT'], 0)
        self.assertEqual(data['TOTAL_DISTANCE'], 0)
        self.assertEqual(data['TOTAL_STEPS'], 0)
        self.assertEqual(data['TOTAL_CALORIES'], 0)
        self.assertEqual(args[1], 'my_custom_component')

    @patch('modules.create_component')
    def test_single_workout(self, mock_create_component):
        """Tests that a single workout is processed correctly."""
        single_workout = [{
            'workout_id': 'workout1',
            'StartTimestamp': datetime.strptime("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
            'EndTimestamp': datetime.strptime("2024-01-01 00:30:00", "%Y-%m-%d %H:%M:%S"),
            'TotalDistance': 5.5,
            'TotalSteps': 6000,
            'CaloriesBurned': 250,
            'start_lat_lng': (1.5, 4.5),
            'end_lat_lng': (1.6, 4.6)
        }]
        display_activity_summary(single_workout)
        
        mock_create_component.assert_called_once()
        args = mock_create_component.call_args[0]
        data = args[0]
        self.assertEqual(data['WORKOUT_COUNT'], 1)
        self.assertEqual(data['TOTAL_DISTANCE'], 5.5)
        self.assertEqual(data['TOTAL_STEPS'], 6000)
        self.assertEqual(data['TOTAL_CALORIES'], 250)
        self.assertEqual(args[1], 'my_custom_component')
        # For "2024-01-01 00:00:00", the formatted string is "01 Jan 2024, 12:00 AM"
        self.assertIn("01 Jan 2024, 12:00 AM", data['ACTIVITY_ROWS'])

    @patch('modules.create_component')
    def test_multiple_workouts(self, mock_create_component):
        """Tests that multiple workouts are processed correctly."""
        multiple_workouts = [
            {
                'workout_id': 'workout1',
                'StartTimestamp': datetime.strptime("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
                'TotalDistance': 5.5,
                'TotalSteps': 6000,
                'CaloriesBurned': 250,
            },
            {
                'workout_id': 'workout2',
                'StartTimestamp': datetime.strptime("2024-01-02 00:00:00", "%Y-%m-%d %H:%M:%S"),
                'TotalDistance': 3.2,
                'TotalSteps': 4000,
                'CaloriesBurned': 180,
            }
        ]
        display_activity_summary(multiple_workouts)
        
        mock_create_component.assert_called_once()
        args = mock_create_component.call_args[0]
        data = args[0]
        self.assertEqual(data['WORKOUT_COUNT'], 2)
        self.assertEqual(data['TOTAL_DISTANCE'], round(5.5 + 3.2, 1))
        self.assertEqual(data['TOTAL_STEPS'], 6000 + 4000)
        self.assertEqual(data['TOTAL_CALORIES'], 250 + 180)
        self.assertEqual(args[1], 'my_custom_component')
        self.assertIn("01 Jan 2024", data['ACTIVITY_ROWS'])
        self.assertIn("02 Jan 2024", data['ACTIVITY_ROWS'])

    @patch('modules.create_component')
    def test_sorting_by_date(self, mock_create_component):
        """Tests that workouts are sorted with the most recent first."""
        unsorted_workouts = [
            {
                'workout_id': 'workout1',
                'StartTimestamp': datetime.strptime("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
                'TotalDistance': 5.5,
                'TotalSteps': 6000,
                'CaloriesBurned': 250,
            },
            {
                'workout_id': 'workout2',
                'StartTimestamp': datetime.strptime("2024-01-03 00:00:00", "%Y-%m-%d %H:%M:%S"),
                'TotalDistance': 3.2,
                'TotalSteps': 4000,
                'CaloriesBurned': 180,
            },
            {
                'workout_id': 'workout3',
                'StartTimestamp': datetime.strptime("2024-01-02 00:00:00", "%Y-%m-%d %H:%M:%S"),
                'TotalDistance': 4.0,
                'TotalSteps': 5000,
                'CaloriesBurned': 200,
            }
        ]
        display_activity_summary(unsorted_workouts)
        mock_create_component.assert_called_once()
        args = mock_create_component.call_args[0]
        activity_rows = args[0]['ACTIVITY_ROWS']
        idx_01_03 = activity_rows.find("03 Jan 2024")
        idx_01_02 = activity_rows.find("02 Jan 2024")
        idx_01_01 = activity_rows.find("01 Jan 2024")
        self.assertLess(idx_01_03, idx_01_02)
        self.assertLess(idx_01_02, idx_01_01)

    @patch('modules.create_component')
    def test_error_handling(self, mock_create_component):
        """Tests that a TypeError is raised when workout timestamps are not sortable."""
        invalid_workouts = [
            {
                'workout_id': 'workout1',
                'StartTimestamp': datetime.strptime("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
                'TotalDistance': 5.5,
                'TotalSteps': 6000,
                'CaloriesBurned': 250,
            },
            {
                'workout_id': 'workout2',
                'StartTimestamp': "invalid-date",
                'TotalDistance': 8.0,
                'TotalSteps': 9000,
                'CaloriesBurned': 400,
            }
        ]
        with self.assertRaises(TypeError):
            display_activity_summary(invalid_workouts)


# ---------------------------
# Tests for display_genai_advice
# ---------------------------
class TestDisplayGenAiAdvice(unittest.TestCase):
    @patch('modules.st.markdown')
    def test_valid_input(self, mock_markdown):
        """Tests display_genai_advice with valid input data."""
        timestamp = "2024-01-01 00:00:00"
        content = "Stay motivated!"
        image = "http://example.com/image.png"
        expected_safe_content = escape(str(content))
        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn("01 Jan 2024, 12:00", html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_none_image(self, mock_markdown):
        """Tests display_genai_advice when image is None."""
        timestamp = "2024-01-01 12:00:00"
        content = "Keep pushing!"
        image = None
        expected_safe_content = escape(str(content))
        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn("01 Jan 2024, 12:00", html_output)
        self.assertIn("None", html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_empty_content(self, mock_markdown):
        """Tests display_genai_advice when content is empty."""
        timestamp = "2024-01-02 08:30:00"
        content = ""
        image = "http://example.com/another_image.png"
        expected_safe_content = escape(content)
        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn("02 Jan 2024, 08:30", html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_none_timestamp(self, mock_markdown):
        """Tests display_genai_advice when timestamp is None."""
        timestamp = None
        content = "Keep your head up!"
        image = "http://example.com/image.png"
        expected_safe_content = escape(str(content))
        expected_safe_timestamp = escape("")
        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn(expected_safe_timestamp, html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_html_injection(self, mock_markdown):
        """Tests that content is properly escaped to prevent HTML injection."""
        timestamp = "2024-01-01 00:00:00"
        content = '<script>alert("xss")</script>'
        image = "http://example.com/image.png"
        expected_safe_content = escape(content)
        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn("01 Jan 2024, 12:00", html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_numeric_content(self, mock_markdown):
        """Tests display_genai_advice when content is numeric."""
        timestamp = "2024-01-01 00:00:00"
        content = 12345
        image = "http://example.com/image.png"
        expected_safe_content = escape(str(content))
        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn("01 Jan 2024, 12:00", html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()

    @patch('modules.st.markdown')
    def test_newline_in_content(self, mock_markdown):
        """Tests display_genai_advice with newline characters in content."""
        timestamp = "2024-01-01 00:00:00"
        content = "Hello\nWorld"
        image = "http://example.com/image.png"
        expected_safe_content = escape(content)
        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        self.assertIn(expected_safe_content, html_output)
        self.assertIn("01 Jan 2024, 12:00", html_output)
        self.assertIn(image, html_output)
        mock_markdown.assert_called_once()


# ---------------------------
# Tests for display_recent_workouts
# ---------------------------
class TestDisplayRecentWorkouts(unittest.TestCase):
    @patch('modules.st.write')
    def test_empty_workouts_list(self, mock_write):
        empty_workouts = []
        display_recent_workouts(empty_workouts)
        mock_write.assert_called_with("No recent workouts found.")
    
    @patch('modules.st.markdown')
    @patch('modules.st.subheader')
    def test_single_workout(self, mock_subheader, mock_markdown):
        single_workout = [{
            'workout_id': 'workout1',
            'StartTimestamp': datetime.strptime("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
            'EndTimestamp': datetime.strptime("2024-01-01 00:30:00", "%Y-%m-%d %H:%M:%S"),
            # Use the keys your modules.py expects:
            'TotalDistance': 5.5,
            'TotalSteps': 6000,
            'CaloriesBurned': 250,
            'start_lat_lng': (1.5, 4.5),
            'end_lat_lng': (1.6, 4.6)
        }]
        display_recent_workouts(single_workout)
        mock_subheader.assert_called_with("Recent Workouts")
        calls = mock_markdown.call_args_list
        found = any("January 01, 2024" in call[0][0] and "12:00" in call[0][0] and "5.5 km" in call[0][0] and "6,000" in call[0][0] for call in calls)
        self.assertTrue(found, "Workout information not properly displayed")
    
    @patch('modules.st.markdown')
    @patch('modules.st.subheader')
    def test_multiple_workouts(self, mock_subheader, mock_markdown):
        multiple_workouts = [
            {
                'workout_id': 'workout1',
                'StartTimestamp': datetime.strptime("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
                'EndTimestamp': datetime.strptime("2024-01-01 00:30:00", "%Y-%m-%d %H:%M:%S"),
                'TotalDistance': 5.5,
                'TotalSteps': 6000,
                'CaloriesBurned': 250,
            },
            {
                'workout_id': 'workout2',
                'StartTimestamp': datetime.strptime("2024-01-03 10:00:00", "%Y-%m-%d %H:%M:%S"),
                'EndTimestamp': datetime.strptime("2024-01-03 11:00:00", "%Y-%m-%d %H:%M:%S"),
                'TotalDistance': 8.0,
                'TotalSteps': 9000,
                'CaloriesBurned': 400,
            }
        ]
        display_recent_workouts(multiple_workouts)
        mock_subheader.assert_called_once_with("Recent Workouts")
        calls = mock_markdown.call_args_list
        workout1_found = any("January 01, 2024" in call[0][0] and "5.5 km" in call[0][0] for call in calls)
        workout2_found = any("January 03, 2024" in call[0][0] and "8.0 km" in call[0][0] for call in calls)
        self.assertTrue(workout1_found, "First workout not displayed")
        self.assertTrue(workout2_found, "Second workout not displayed")
    
    @patch('modules.st.error')
    def test_error_handling(self, mock_error):
        invalid_workouts = [
            {
                'workout_id': 'workout1',
                'StartTimestamp': datetime.strptime("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
                'TotalDistance': 5.5,
                'TotalSteps': 6000,
                'CaloriesBurned': 250,
            },
            {
                'workout_id': 'workout2',
                'StartTimestamp': "invalid-date",
                'TotalDistance': 8.0,
                'TotalSteps': 9000,
                'CaloriesBurned': 400,
            }
        ]
        with self.assertRaises(TypeError):
            display_recent_workouts(invalid_workouts)


# ---------------------------
# Tests for display_user_sensor_data
# ---------------------------
class TestDisplayUserSensorData(unittest.TestCase):
    def setUp(self):
        self.sensor_data_list = [
            {
                "sensor_type": "Heart Rate",
                "timestamp": "2024-07-29 07:15:00",
                "data": 120.0,
                "units": "bpm"
            },
            {
                "sensor_type": "Temperature",
                "timestamp": "2024-07-29 07:30:00",
                "data": 36.5,
                "units": "Celsius"
            }
        ]
    
    @patch("modules.st.warning")
    def test_empty_sensor_data(self, mock_warning):
        display_user_sensor_data([])
        mock_warning.assert_called_once_with("No sensor data available for this workout.")
    
    @patch("modules.st.download_button")
    @patch("modules.st.dataframe")
    @patch("modules.st.line_chart")
    @patch("modules.st.multiselect")
    @patch("modules.st.tabs")
    @patch("modules.st.markdown")
    @patch("modules.st.header")
    def test_valid_sensor_data(
        self, mock_header, mock_markdown, mock_tabs, mock_multiselect, 
        mock_line_chart, mock_dataframe, mock_download_button
    ):
        dummy_tab1 = MagicMock()
        dummy_tab2 = MagicMock()
        dummy_tab3 = MagicMock()
        for dummy in (dummy_tab1, dummy_tab2, dummy_tab3):
            dummy.__enter__.return_value = dummy
            dummy.__exit__.return_value = None
        mock_tabs.return_value = (dummy_tab1, dummy_tab2, dummy_tab3)
        mock_multiselect.return_value = ["Heart Rate"]
        display_user_sensor_data(self.sensor_data_list)
        mock_header.assert_called_with("Workout Sensor Data")
        self.assertTrue(mock_markdown.call_count >= 2)
        mock_multiselect.assert_called_once()
        self.assertTrue(mock_line_chart.call_count >= 1)
        mock_dataframe.assert_called_once()
        mock_download_button.assert_called_once()


if __name__ == "__main__":
    unittest.main()
