#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""
    """These tests were created with the assistance of Gemini"""

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

    @patch('modules.create_component')
    def test_empty_workouts_list(self, mock_create_component):
        """Tests that the function handles an empty workouts list correctly."""
        
        empty_workouts = []
        display_activity_summary(empty_workouts)
        
        # Check that create_component was called with the right arguments
        mock_create_component.assert_called_once()
        args = mock_create_component.call_args[0]
        
        # Verify the data dictionary has the expected values
        self.assertEqual(args[0]['WORKOUT_COUNT'], 0)
        self.assertEqual(args[0]['TOTAL_DISTANCE'], 0)
        self.assertEqual(args[0]['TOTAL_STEPS'], 0)
        self.assertEqual(args[0]['TOTAL_CALORIES'], 0)
        self.assertEqual(args[1], 'my_custom_component')  # HTML file name

    @patch('modules.create_component')
    def test_single_workout(self, mock_create_component):
        """Tests that the function correctly processes a single workout."""
        single_workout = [{
            'workout_id': 'workout1',
            'start_timestamp': '2024-01-01 00:00:00',
            'end_timestamp': '2024-01-01 00:30:00',
            'distance': 5.5,
            'steps': 6000,
            'calories_burned': 250,
            'start_lat_lng': (1.5, 4.5),
            'end_lat_lng': (1.6, 4.6)
        }]
        
        display_activity_summary(single_workout)
        
        # Check that create_component was called with the right arguments
        mock_create_component.assert_called_once()
        args = mock_create_component.call_args[0]
        
        # Verify the data dictionary has the expected values
        self.assertEqual(args[0]['WORKOUT_COUNT'], 1)
        self.assertEqual(args[0]['TOTAL_DISTANCE'], 5.5)
        self.assertEqual(args[0]['TOTAL_STEPS'], 6000)
        self.assertEqual(args[0]['TOTAL_CALORIES'], 250)
        self.assertEqual(args[1], 'my_custom_component')  # HTML file name
        
        # Check that the activity row contains the date
        self.assertIn('2024-01-01', args[0]['ACTIVITY_ROWS'])


    

    @patch('modules.create_component')
    def test_multiple_workouts(self, mock_create_component):
        """Tests that the function correctly processes multiple workouts."""
        multiple_workouts = [
            {
                'workout_id': 'workout1',
                'start_timestamp': '2024-01-01 00:00:00',
                'end_timestamp': '2024-01-01 00:30:00',
                'distance': 5.5,
                'steps': 6000,
                'calories_burned': 250,
                'start_lat_lng': (1.5, 4.5),
                'end_lat_lng': (1.6, 4.6)
            },
            {
                'workout_id': 'workout2',
                'start_timestamp': '2024-01-02 00:00:00',
                'end_timestamp': '2024-01-02 00:30:00',
                'distance': 3.2,
                'steps': 4000,
                'calories_burned': 180,
                'start_lat_lng': (1.7, 4.7),
                'end_lat_lng': (1.8, 4.8)
            }
        ]
        
        display_activity_summary(multiple_workouts)
        
        # Check that create_component was called with the right arguments
        mock_create_component.assert_called_once()
        args = mock_create_component.call_args[0]
        
        # Verify the data dictionary has the expected values
        self.assertEqual(args[0]['WORKOUT_COUNT'], 2)
        self.assertEqual(args[0]['TOTAL_DISTANCE'], 8.7)  # 5.5 + 3.2
        self.assertEqual(args[0]['TOTAL_STEPS'], 10000)  # 6000 + 4000
        self.assertEqual(args[0]['TOTAL_CALORIES'], 430)  # 250 + 180
        self.assertEqual(args[1], 'my_custom_component')  # HTML file name
        
        # Check that both dates are in the activity rows
        self.assertIn('2024-01-01', args[0]['ACTIVITY_ROWS'])
        self.assertIn('2024-01-02', args[0]['ACTIVITY_ROWS'])
        
    @patch('modules.create_component')
    def test_sorting_by_date(self, mock_create_component):
        """Tests that workouts are sorted by date with most recent first."""
        unsorted_workouts = [
            {
                'workout_id': 'workout1',
                'start_timestamp': '2024-01-01 00:00:00',
                'end_timestamp': '2024-01-01 00:30:00',
                'distance': 5.5,
                'steps': 6000,
                'calories_burned': 250,
            },
            {
                'workout_id': 'workout2',
                'start_timestamp': '2024-01-03 00:00:00',
                'end_timestamp': '2024-01-03 00:30:00',
                'distance': 3.2,
                'steps': 4000,
                'calories_burned': 180,
            },
            {
                'workout_id': 'workout3',
                'start_timestamp': '2024-01-02 00:00:00',
                'end_timestamp': '2024-01-02 00:30:00',
                'distance': 4.0,
                'steps': 5000,
                'calories_burned': 200,
            }
        ]
        
        display_activity_summary(unsorted_workouts)
        
        # Check that dates appear in the expected order in the HTML (most recent first)
        mock_create_component.assert_called_once()
        args = mock_create_component.call_args[0]
        activity_rows = args[0]['ACTIVITY_ROWS']
        
        # The index of the first occurrence of each date in the activity rows
        idx_01_03 = activity_rows.find('2024-01-03')
        idx_01_02 = activity_rows.find('2024-01-02')
        idx_01_01 = activity_rows.find('2024-01-01')
        
        # Verify that dates appear in descending order
        self.assertLess(idx_01_03, idx_01_02)
        self.assertLess(idx_01_02, idx_01_01)


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
        """Tests display_genai_advice when image is None (nopage scenario)."""
        timestamp = '2024-01-01 12:00:00'
        content = 'Keep pushing!'
        image = None
        expected_safe_content = escape(str(content))
        expected_safe_timestamp = escape("01 Jan 2024, 12:00")
        
        display_genai_advice(timestamp, content, image)
        html_output = mock_markdown.call_args[0][0]
        
        self.assertIn(expected_safe_content, html_output)
        self.assertIn(expected_safe_timestamp, html_output)
        self.assertIn("background: linear-gradient(45deg, #024CAA, #00AEEF);", html_output)
        # Since image is None, the f-string converts it to "None" in the src attribute.
        self.assertIn('<img class="image" src="None" alt="">', html_output)
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
    
    @patch('modules.st.write')
    def test_empty_workouts_list(self, mock_write):
        """Tests handling of an empty workouts list."""
        empty_workouts = []
        display_recent_workouts(empty_workouts)
        
        # Check that appropriate message is displayed
        mock_write.assert_called_with("No recent workouts found.")
    
    @patch('modules.st.markdown')
    @patch('modules.st.subheader')
    def test_single_workout(self, mock_subheader, mock_markdown):
        """Tests that a single workout is displayed correctly."""
        single_workout = [{
            'workout_id': 'workout1',
            'start_timestamp': '2024-01-01 00:00:00',
            'end_timestamp': '2024-01-01 00:30:00',
            'distance': 5.5,
            'steps': 6000,
            'calories_burned': 250,
            'start_lat_lng': (1.5, 4.5),
            'end_lat_lng': (1.6, 4.6)
        }]
        
        display_recent_workouts(single_workout)
        
        # Check that subheader is displayed
        mock_subheader.assert_called_with("Recent Workouts")
        
        # Check that markdown is called with workout information
        calls = mock_markdown.call_args_list
        
        # Find the call that contains workout information
        workout_info_found = False
        for call in calls:
            call_content = call[0][0]
            if "January 01, 2024" in call_content and "5.5 km" in call_content and "6,000" in call_content and "250" in call_content:
                workout_info_found = True
                break
                
        self.assertTrue(workout_info_found, "Workout information not properly displayed")
    
    @patch('modules.st.markdown')
    @patch('modules.st.subheader')
    def test_multiple_workouts(self, mock_subheader, mock_markdown):
        """Tests that multiple workouts are displayed in the correct order."""
        multiple_workouts = [
            {
                'workout_id': 'workout1',
                'start_timestamp': '2024-01-01 00:00:00',
                'end_timestamp': '2024-01-01 00:30:00',
                'distance': 5.5,
                'steps': 6000,
                'calories_burned': 250,
            },
            {
                'workout_id': 'workout2',
                'start_timestamp': '2024-01-03 10:00:00',
                'end_timestamp': '2024-01-03 11:00:00',
                'distance': 8.0,
                'steps': 9000,
                'calories_burned': 400,
            }
        ]
        
        display_recent_workouts(multiple_workouts)
        
        # Check that subheader is displayed
        mock_subheader.assert_called_once_with("Recent Workouts")
        
        # Get all markdown calls
        calls = mock_markdown.call_args_list
        
        # Find content for each workout
        workout1_content = None
        workout2_content = None
        
        for call in calls:
            call_content = call[0][0]
            if "January 01, 2024" in call_content and "5.5 km" in call_content:
                workout1_content = call_content
            elif "January 03, 2024" in call_content and "8.0 km" in call_content:
                workout2_content = call_content
        
        # Verify both workouts were displayed
        self.assertIsNotNone(workout1_content, "First workout not displayed")
        self.assertIsNotNone(workout2_content, "Second workout not displayed")
        
        # Find the index of each workout's content in the list of calls
        # to verify they appear in the correct order (most recent first)
        workout1_index = None
        workout2_index = None
        
        for i, call in enumerate(calls):
            call_content = call[0][0]
            if "January 01, 2024" in call_content and "5.5 km" in call_content:
                workout1_index = i
            elif "January 03, 2024" in call_content and "8.0 km" in call_content:
                workout2_index = i
        
        # Verify most recent workout appears first
        self.assertLess(workout2_index, workout1_index, "Workouts not sorted correctly by date")
    
    @patch('modules.st.markdown')
    @patch('modules.st.subheader')
    def test_workout_duration_formatting(self, mock_subheader, mock_markdown):
        """Tests that workout duration is formatted correctly for different time spans."""
        # Test workouts with different durations
        workouts = [
            # Short duration (seconds only)
            {
                'start_timestamp': '2024-01-01 00:00:00',
                'end_timestamp': '2024-01-01 00:00:30',
                'distance': 0.1,
                'steps': 100,
                'calories_burned': 10,
            },
            # Minutes and seconds
            {
                'start_timestamp': '2024-01-02 00:00:00',
                'end_timestamp': '2024-01-02 00:05:30',
                'distance': 0.5,
                'steps': 500,
                'calories_burned': 50,
            },
            # Hours, minutes, and seconds
            {
                'start_timestamp': '2024-01-03 00:00:00',
                'end_timestamp': '2024-01-03 01:30:45',
                'distance': 10.0,
                'steps': 12000,
                'calories_burned': 600,
            }
        ]
        
        display_recent_workouts(workouts)
        
        # Check all markdown calls
        calls = mock_markdown.call_args_list
        
        # Find each workout's content and verify the duration formatting
        seconds_only_found = False
        minutes_seconds_found = False
        hours_minutes_seconds_found = False
        
        for call in calls:
            call_content = call[0][0]
            # Check for the exact duration span for seconds-only workout
            if '<span class="stat-value">30s</span>' in call_content:
                seconds_only_found = True
            if "5m 30s" in call_content:
                minutes_seconds_found = True
            if "1h 30m" in call_content:
                hours_minutes_seconds_found = True
        
        self.assertTrue(seconds_only_found, "Seconds-only duration not formatted correctly")
        self.assertTrue(minutes_seconds_found, "Minutes and seconds duration not formatted correctly")
        self.assertTrue(hours_minutes_seconds_found, "Hours, minutes, and seconds duration not formatted correctly")

    
    @patch('modules.st.error')
    @patch('modules.st.markdown')
    def test_error_handling(self, mock_markdown, mock_error):
        """Tests error handling for invalid workout data."""
        invalid_workouts = [
            # Missing end_timestamp
            {
                'workout_id': 'workout1',
                'start_timestamp': '2024-01-01 00:00:00',
                # No end_timestamp
                'distance': 5.5,
                'steps': 6000,
                'calories_burned': 250,
            },
            # Invalid timestamp format
            {
                'workout_id': 'workout2',
                'start_timestamp': 'invalid-date',
                'end_timestamp': '2024-01-03 11:00:00',
                'distance': 8.0,
                'steps': 9000,
                'calories_burned': 400,
            }
        ]
        
        display_recent_workouts(invalid_workouts)
        
        # Verify error is displayed
        mock_error.assert_called()


if __name__ == "__main__":
    unittest.main()
