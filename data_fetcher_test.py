#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################

import unittest
import hashlib
import uuid
from unittest.mock import patch, MagicMock
from data_fetcher import (
    get_user_posts,
    get_genai_advice,
    get_user_profile,
    get_user_sensor_data,
    get_user_workouts,
    hash_password,
    login_user,
    register_user,
    get_current_week_challenges
)

# Create fake credentials for authentication patching
fake_credentials = MagicMock()
fake_credentials.universe_domain = "googleapis.com"

class TestGetUserWorkouts(unittest.TestCase):

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_workouts_success(self, mock_client_class):
        """Returns workout data from BigQuery if available."""
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = [
            {
                "workout_id": "bq_workout1",
                "start_timestamp": "2025-04-01 08:00:00",
                "end_timestamp": "2025-04-01 09:00:00",
                "distance": 5.0,
                "steps": 7000,
                "calories_burned": 300,
                "start_lat_lng": (0, 0),
                "end_lat_lng": (0, 0)
            }
        ]
        mock_client.query.return_value = mock_query_job
        mock_client_class.return_value = mock_client

        result = get_user_workouts("user123")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["workout_id"], "bq_workout1")

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_workouts_empty_result(self, mock_client_class):
        """Returns mock data if BigQuery returns empty result."""
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = []  # Empty response

        mock_client.query.return_value = mock_query_job
        mock_client_class.return_value = mock_client

        result = get_user_workouts("user_no_data")
        self.assertEqual(len(result), 3)  # Length of mock_workouts
        self.assertEqual(result[0]["workout_id"], "workout1")  # From mock data

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_workouts_with_error(self, mock_client_class):
        """Returns mock data if BigQuery throws an exception."""
        mock_client = MagicMock()
        mock_client.query.side_effect = Exception("BigQuery failed")

        mock_client_class.return_value = mock_client

        result = get_user_workouts("user_error")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1]["workout_id"], "workout2")  # From mock data
       

class TestGetUserProfile(unittest.TestCase):
    """Tests the get_user_profile function."""
    
    @patch("data_fetcher.bigquery.Client")
    def test_get_user_profile_with_friends(self, mock_client_class):
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = [{
            "name": "Alice Johnson",
            "username": "alicej",
            "DateOfBirth": "1990-01-15",
            "ImageUrl": "http://example.com/images/alice.jpg",
            "friends": ["user2", "user3"]
        }]
        mock_client.query.return_value = mock_query_job
        mock_client_class.return_value = mock_client

        result = get_user_profile("user1")
        self.assertEqual(result["username"], "alicej")
        self.assertIn("user2", result["friends"])
        self.assertEqual(len(result["friends"]), 2)

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_profile_no_friends(self, mock_client_class):
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = [{
            "name": "Charlie Brown",
            "username": "charlieb",
            "DateOfBirth": "1992-11-05",
            "ImageUrl": "http://example.com/images/charlie.jpg",
            "friends": []
        }]
        mock_client.query.return_value = mock_query_job
        mock_client_class.return_value = mock_client

        result = get_user_profile("user3")
        self.assertEqual(result["username"], "charlieb")
        self.assertEqual(result["friends"], [])

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_profile_user_not_found(self, mock_client_class):
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = []
        mock_client.query.return_value = mock_query_job
        mock_client_class.return_value = mock_client

        result = get_user_profile("user999")
        self.assertEqual(result, {})


class TestGetUserPosts(unittest.TestCase):
    """Tests the get_user_posts function."""
    
    @patch("data_fetcher.bigquery.Client")
    def test_get_user_posts_valid(self, mock_client_class):
        """Returns a list of posts from a userID"""
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_result = [
            {
                "PostId": "post1",
                "AuthorId": "user1",
                "Timestamp": "2024-07-29T12:00:00",
                "ImageUrl": "http://example.com/posts/post1.jpg",
                "Content": "Hello World"
            }
        ]
        mock_query_job.result.return_value = mock_result
        mock_client.query.return_value = mock_query_job
        mock_client_class.return_value = mock_client

        result = get_user_posts("user1")
        mock_client.query.assert_called_once()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["AuthorId"], "user1")
        self.assertEqual(result[0]["Content"], "Hello World")

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_posts_empty(self, mock_client_class):
        """Returns empty list when user has no posts"""
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = []
        mock_client.query.return_value = mock_query_job
        mock_client_class.return_value = mock_client

        result = get_user_posts("user999")
        self.assertEqual(result, [])

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_posts_error(self, mock_client_class):
        """Throws exception when BigQuery fails"""
        mock_client = MagicMock()
        mock_client.query.side_effect = Exception("BigQuery Error")
        mock_client_class.return_value = mock_client

        with self.assertRaises(Exception):
            get_user_posts("user1")


class TestGetUserSensorData(unittest.TestCase):
    """Tests the get_user_sensor_data function."""
    
    @patch("data_fetcher.bigquery.Client")
    def test_get_user_sensor_data_valid(self, mock_client_class):
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        sensor_results = [
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
        mock_query_job.result.return_value = sensor_results
        mock_client.query.return_value = mock_query_job
        mock_client_class.return_value = mock_client

        result = get_user_sensor_data("user1", "workout1")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["sensor_type"], "Heart Rate")
        self.assertEqual(result[0]["timestamp"], "2024-07-29 07:15:00")
        self.assertEqual(result[0]["data"], 120.0)
        self.assertEqual(result[0]["units"], "bpm")
        self.assertEqual(result[1]["sensor_type"], "Temperature")
        self.assertEqual(result[1]["timestamp"], "2024-07-29 07:30:00")
        self.assertEqual(result[1]["data"], 36.5)
        self.assertEqual(result[1]["units"], "Celsius")

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_sensor_data_empty(self, mock_client_class):
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = []
        mock_client.query.return_value = mock_query_job
        mock_client_class.return_value = mock_client

        result = get_user_sensor_data("user1", "non_existing_workout")
        self.assertEqual(result, [])

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_sensor_data_error(self, mock_client_class):
        mock_client = MagicMock()
        mock_client.query.side_effect = Exception("BigQuery Error")
        mock_client_class.return_value = mock_client

        with self.assertRaises(Exception):
            get_user_sensor_data("user1", "workout1")


class TestGetGenaiAdvice(unittest.TestCase):
    """Tests the get_genai_advice function which uses Vertex AI and aggregated workout data."""
    
    @patch("google.auth.default", return_value=(fake_credentials, "fake-project"))
    @patch("data_fetcher.get_user_profile")
    @patch("data_fetcher.get_user_daily_workout_data")
    @patch("vertexai.init", return_value=None)
    @patch("vertexai.generative_models.GenerativeModel")
    def test_get_genai_advice_valid(self, mock_gen_model, mock_vertexai_init,
                                    mock_get_daily, mock_get_user_profile, mock_auth_default):
        # Setup user profile and daily workout data.
        mock_get_user_profile.return_value = {"full_name": "Alice Johnson", "username": "alicej"}
        mock_get_daily.return_value = {
            "distance": 5.0,
            "steps": 8000,
            "calories": 400,
            "advice_timestamp": "2024-07-29 08:00:00"
        }
        
        # Configure fake Vertex AI response with valid JSON advice list.
        fake_response = MagicMock()
        fake_candidate = MagicMock()
        fake_candidate.content.text = '["Great job today, alicej!", "Keep up the good work, alicej!"]'
        fake_response.candidates = [fake_candidate]
        
        # Create a mock model instance.
        fake_model_instance = MagicMock()
        fake_model_instance.generate_content.return_value = fake_response
        mock_gen_model.return_value = fake_model_instance

        result = get_genai_advice("user1")
        self.assertIn("advice_id", result)
        self.assertIn("timestamp", result)
        self.assertIn("content", result)
        self.assertIn("image", result)
        self.assertEqual(result["timestamp"], "2024-07-29 08:00:00")
        self.assertTrue(result["content"])
        self.assertIn("alicej", result["content"].lower())
    
    @patch("google.auth.default", return_value=(fake_credentials, "fake-project"))
    @patch("data_fetcher.get_user_profile")
    @patch("data_fetcher.get_user_daily_workout_data")
    @patch("vertexai.init", return_value=None)
    @patch("vertexai.generative_models.GenerativeModel")
    def test_get_genai_advice_fallback(self, mock_gen_model, mock_vertexai_init,
                                        mock_get_daily, mock_get_user_profile, mock_auth_default):
        mock_get_user_profile.return_value = {"full_name": "Alice Johnson", "username": "alicej"}
        mock_get_daily.return_value = {
            "distance": 5.0,
            "steps": 8000,
            "calories": 400,
            "advice_timestamp": "2024-07-29 08:00:00"
        }
        
        # Configure fake Vertex AI response with invalid JSON to trigger fallback.
        fake_response = MagicMock()
        fake_candidate = MagicMock()
        fake_candidate.content.text = "invalid json"
        fake_response.candidates = [fake_candidate]
        
        fake_model_instance = MagicMock()
        fake_model_instance.generate_content.return_value = fake_response
        mock_gen_model.return_value = fake_model_instance

        result = get_genai_advice("user1")
        self.assertTrue(result["content"])
        self.assertIn("alicej", result["content"].lower())
        self.assertEqual(result["timestamp"], "2024-07-29 08:00:00")

class TestAuthFunctions(unittest.TestCase):

    @patch("data_fetcher.bigquery.Client")
    def test_login_user_success(self, mock_client_class):
        """Returns user dict if username and password match"""
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = [{
            "UserId": "user-123",
            "Username": "testuser"
        }]
        mock_client.query.return_value = mock_query_job
        mock_client_class.return_value = mock_client

        result = login_user("testuser", "Test1234")
        self.assertIsNotNone(result)
        self.assertEqual(result["UserId"], "user-123")
        self.assertEqual(result["Username"], "testuser")

    @patch("data_fetcher.bigquery.Client")
    def test_login_user_invalid_credentials(self, mock_client_class):
        """Returns None if username or password is incorrect"""
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = []
        mock_client.query.return_value = mock_query_job
        mock_client_class.return_value = mock_client

        result = login_user("wronguser", "WrongPass123")
        self.assertIsNone(result)

    @patch("data_fetcher.bigquery.Client")
    def test_register_user_success(self, mock_client_class):
        """Registers a new user if username is available"""
        mock_client = MagicMock()
        # First query: check if username exists
        mock_check_job = MagicMock()
        mock_check_job.result.return_value = []
        # Second query: insert user (no result needed)
        mock_insert_job = MagicMock()
        mock_client.query.side_effect = [mock_check_job, mock_insert_job]
        mock_client_class.return_value = mock_client

        result = register_user("newuser", "New User", "NewPass123")
        self.assertEqual(result, "¡Successfully registered!")

    @patch("data_fetcher.bigquery.Client")
    def test_register_user_duplicate_username(self, mock_client_class):
        """Returns error message if username already exists"""
        mock_client = MagicMock()
        mock_check_job = MagicMock()
        mock_check_job.result.return_value = [{"Username": "existinguser"}]
        mock_client.query.return_value = mock_check_job
        mock_client_class.return_value = mock_client

        result = register_user("existinguser", "Existing User", "SomePass123")
        self.assertEqual(result, "That username is already in use.")

class TestGetCurrentWeekChallenges(unittest.TestCase):
    """Tests for get_current_week_challenges(), mocking out its two dependencies."""

    @patch("data_fetcher.get_week_challenges")
    @patch("data_fetcher.get_latest_two_challenges")
    def test_get_current_challenges_success(self, mock_latest_two, mock_week):
        # Arrange: pretend that latest two ranges are (this, last)
        mock_latest_two.return_value = (
            ("2025-04-14", "2025-04-20"),
            ("2025-04-07", "2025-04-13"),
        )
        # And pretend that get_week_challenges returns some nested payload:
        expected = [
            {"user_id": "u1", "username": "alice", "profile_image": None, "value": 100},
            {"user_id": "u2", "username": "bob",   "profile_image": None, "value":  90},
        ]
        mock_week.return_value = [["2025-04-14", "2025-04-20"], expected]

        # Act
        result = get_current_week_challenges()

        # Assert: we got exactly the second element of the mocked get_week_challenges
        self.assertEqual(result, [["2025-04-14", "2025-04-20"], expected])
        mock_latest_two.assert_called_once()
        mock_week.assert_called_once_with("2025-04-14", "2025-04-20")

    @patch("data_fetcher.get_week_challenges")
    @patch("data_fetcher.get_latest_two_challenges")
    def test_get_current_challenges_empty(self, mock_latest_two, mock_week):
        # Arrange: normal dates
        mock_latest_two.return_value = (("2025-04-14", "2025-04-20"), ("2025-04-07", "2025-04-13"))
        # But the week query returns an empty list
        mock_week.return_value = []

        # Act
        result = get_current_week_challenges()

        # Assert: we simply bubble up the empty list
        self.assertEqual(result, [])
        mock_week.assert_called_once()

    @patch("data_fetcher.get_week_challenges")
    @patch("data_fetcher.get_latest_two_challenges")
    def test_get_current_challenges_failure(self, mock_latest_two, mock_week):
        # Arrange: let get_week_challenges throw
        mock_latest_two.return_value = (("2025-04-14", "2025-04-20"), ("2025-04-07", "2025-04-13"))
        mock_week.side_effect = Exception("DB is down")

        # Act / Assert: the exception bubbles up (or you can wrap in try/except
        with self.assertRaises(Exception):
            _ = get_current_week_challenges()
        mock_week.assert_called_once()

if __name__ == "__main__":
    unittest.main()
