#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################
import unittest
from unittest.mock import patch, MagicMock
from data_fetcher import get_user_posts

class TestDataFetcher(unittest.TestCase):

    def test_foo(self):
        pass
       

class TestGetUserPosts(unittest.TestCase):
    """Tests the get_user_posts function."""
    #Tests were created with the assistance of ChatGPT

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
    def test_get_user_posts_empy(self, mock_client_class):
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


        

if __name__ == "__main__":
    unittest.main()