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
from unittest.mock import patch, MagicMock

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    def test_foo(self):
        """Tests foo."""
        pass


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