#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################
import unittest
from unittest.mock import patch, MagicMock
from data_fetcher import (
    get_user_posts,
    get_genai_advice,
    get_user_profile,
    get_user_sensor_data,
    get_user_workouts,
)


class TestDataFetcher(unittest.TestCase):

    def test_foo(self):
        pass
       

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
        moch_result = [
            {
                "PostId": "post1",
                "AuthorId": "user1",
                "Timestamp": "2024-07-29T12:00:00",
                "ImageUrl": "http://example.com/posts/post1.jpg",
                "Content": "Hello World"
            }
        ]
        mock_query_job.result.return_value = moch_result
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
    @patch("data_fetcher.get_user_profile")
    @patch("data_fetcher.get_user_daily_workout_data")
    def test_get_genai_advice_valid(self, mock_get_daily, mock_get_user_profile):
        # Setup user profile and daily workout data.
        mock_get_user_profile.return_value = {"full_name": "Alice Johnson", "username": "alicej"}
        mock_get_daily.return_value = {
            "distance": 5.0,
            "steps": 8000,
            "calories": 400,
            "advice_timestamp": "2024-07-29 08:00:00"
        }
        
        # Setup fake Vertex AI response with valid JSON advice list.
        fake_response = MagicMock()
        fake_candidate = MagicMock()
        fake_candidate.content.text = '["Great job today, alicej!", "Keep up the good work, alicej!"]'
        fake_response.candidates = [fake_candidate]
        
        fake_model_instance = MagicMock()
        fake_model_instance.generate_content.return_value = fake_response

        # Patch the vertexai module in get_genai_advice's globals using patch.dict.
        with patch.dict(get_genai_advice.__globals__, {
            "vertexai": MagicMock()
        }):
            fake_vertexai = get_genai_advice.__globals__["vertexai"]
            fake_vertexai.init.return_value = None
            fake_vertexai.generative_models = MagicMock()
            fake_vertexai.generative_models.GenerativeModel.return_value = fake_model_instance

            result = get_genai_advice("user1")
            
            self.assertIn("advice_id", result)
            self.assertIn("timestamp", result)
            self.assertIn("content", result)
            self.assertIn("image", result)
            self.assertEqual(result["timestamp"], "2024-07-29 08:00:00")
            # Check that the content includes the username "alicej".
            self.assertTrue(result["content"])
            self.assertIn("alicej", result["content"])
    
    @patch("data_fetcher.get_user_profile")
    @patch("data_fetcher.get_user_daily_workout_data")
    def test_get_genai_advice_fallback(self, mock_get_daily, mock_get_user_profile):
        mock_get_user_profile.return_value = {"full_name": "Alice Johnson", "username": "alicej"}
        mock_get_daily.return_value = {
            "distance": 5.0,
            "steps": 8000,
            "calories": 400,
            "advice_timestamp": "2024-07-29 08:00:00"
        }
        
        fake_response = MagicMock()
        fake_candidate = MagicMock()
        fake_candidate.content.text = "invalid json"
        fake_response.candidates = [fake_candidate]
        
        fake_model_instance = MagicMock()
        fake_model_instance.generate_content.return_value = fake_response

        with patch.dict(get_genai_advice.__globals__, {
            "vertexai": MagicMock()
        }):
            fake_vertexai = get_genai_advice.__globals__["vertexai"]
            fake_vertexai.init.return_value = None
            fake_vertexai.generative_models = MagicMock()
            fake_vertexai.generative_models.GenerativeModel.return_value = fake_model_instance

            result = get_genai_advice("user1")
            # Check that even in fallback, the advice includes the username "alicej".
            self.assertTrue(result["content"])
            self.assertIn("alicej", result["content"])
            self.assertEqual(result["timestamp"], "2024-07-29 08:00:00")


if __name__ == "__main__":
    unittest.main()
