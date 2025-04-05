#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################
import unittest
from data_fetcher import get_user_workouts

class TestDataFetcher(unittest.TestCase):

    def test_get_user_workouts(self):
        """Tests that get_user_workouts returns the correct sample data."""
        workouts = get_user_workouts("user1")
        
        # Check that the function returns a list of workouts
        self.assertIsInstance(workouts, list)
        
        # Check that the list contains the correct number of workouts
        self.assertEqual(len(workouts), 3)
        
        # Check that the first workout has the correct data
        self.assertEqual(workouts[0]['workout_id'], 'workout1')
        self.assertEqual(workouts[0]['start_timestamp'], '2025-04-01 08:00:00')
        self.assertEqual(workouts[0]['distance'], 5.2)
        self.assertEqual(workouts[0]['steps'], 7500)
        self.assertEqual(workouts[0]['calories_burned'], 350)

    def test_get_user_workouts_empty(self):
        """Tests that get_user_workouts returns an empty list when the user has no workouts."""
        workouts = get_user_workouts("nonexistent_user")
        self.assertEqual(len(workouts), 0)


if __name__ == "__main__":
    unittest.main()
