#############################################################################
# data_fetcher.py
#
# This file contains functions to fetch data needed for the app.
#
# You will re-write these functions in Unit 3, and are welcome to alter the
# data returned in the meantime. We will replace this file with other data when
# testing earlier units.
#############################################################################

import random
from google.cloud import bigquery


def get_user_sensor_data(user_id, workout_id):
    """Returns a list of timestampped information for a given workout.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    sensor_data = []
    sensor_types = [
        'accelerometer',
        'gyroscope',
        'pressure',
        'temperature',
        'heart_rate',
    ]
    for index in range(random.randint(5, 100)):
        random_minute = str(random.randint(0, 59))
        if len(random_minute) == 1:
            random_minute = '0' + random_minute
        timestamp = '2024-01-01 00:' + random_minute + ':00'
        data = random.random() * 100
        sensor_type = random.choice(sensor_types)
        sensor_data.append(
            {'sensor_type': sensor_type, 'timestamp': timestamp, 'data': data}
        )
    return sensor_data


def get_user_workouts(user_id):
    """Returns a list of user's workouts from the database.
    
    If no workouts are found or there's an error, returns mock data.
    """
    # Define fallback mock data
    mock_workouts = [
        {
            'workout_id': 'workout1',
            'start_timestamp': '2025-04-01 08:00:00',
            'end_timestamp': '2025-04-01 09:00:00',
            'start_lat_lng': (37.7749, -122.4194),
            'end_lat_lng': (37.7749, -122.4194),
            'distance': 5.2,
            'steps': 7500,
            'calories_burned': 350,
        },
        {
            'workout_id': 'workout2',
            'start_timestamp': '2025-04-03 17:00:00',
            'end_timestamp': '2025-04-03 18:30:00',
            'start_lat_lng': (34.0522, -118.2437),
            'end_lat_lng': (34.0522, -118.2437),
            'distance': 7.8,
            'steps': 11200,
            'calories_burned': 520,
        },
        {
            'workout_id': 'workout3',
            'start_timestamp': '2025-04-05 10:00:00',
            'end_timestamp': '2025-04-05 11:15:00',
            'start_lat_lng': (40.7128, -74.0060),
            'end_lat_lng': (40.7128, -74.0060),
            'distance': 6.5,
            'steps': 9300,
            'calories_burned': 410,
        },
    ]
    
    try:
        # Connect to BigQuery
        client = bigquery.Client(project="roberttechx25")
        
        # SQL query to fetch user workouts
        query = """
            SELECT *
            FROM `roberttechx25.ISE.Workouts`
            WHERE UserId = @user_id
            ORDER BY start_timestamp DESC
        """
        
        # Configure query parameters
        query_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)
            ]
        )
        
        # Execute query
        query_job = client.query(query, job_config=query_config)
        results = query_job.result()
        
        # Convert results to list of dictionaries
        workouts = [dict(row) for row in results]
        
        # Return query results if found, otherwise return mock data
        if workouts:
            return workouts
        else:
            print(f"No workouts found for user {user_id}, returning mock data")
            return mock_workouts
            
    except Exception as e:
        # Log the error and return mock data as fallback
        print(f"Error fetching workouts from database: {e}")
        return mock_workouts

    """
    This check was causing a traceback because users is not defined so I commented it out
    
    if user_id not in users:
        return workouts
    return workouts
    """
    

def get_user_profile(user_id):
    """Returns information about the given user."""

    client = bigquery.Client(project="roberttechx25")

    query = f"""
        SELECT
            u.Name,
            u.Username,
            u.DateOfBirth,
            u.ImageUrl,
            ARRAY_AGG(f.UserId2 IGNORE NULLS) AS Friends
        FROM `roberttechx25.ISE.Users` AS u
        LEFT JOIN `roberttechx25.ISE.Friends` AS f
            ON u.UserId = f.UserId1
        WHERE u.UserId = @user_id
        GROUP BY u.Name, u.Username, u.DateOfBirth, u.ImageUrl
    """
    #This query was created with the assistance of ChatGPT
    

    query_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)
        ]
    )

    query_job = client.query(query, job_config=query_config)
    results = list(query_job.result())

    if results:
        return dict(results[0])
    else:
        return {}


def get_user_posts(user_id):
    """Returns a list of a user's posts."""

    client = bigquery.Client(project="roberttechx25")

    query = f"""
        SELECT * FROM `roberttechx25.ISE.Posts`
        WHERE AuthorId = @user_id
        ORDER BY timestamp DESC
    """

    query_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)
        ]
    ) #This part was created with the assistance of ChatGPT

    query_job = client.query(query, job_config=query_config)
    results = query_job.result()
    return [dict(row) for row in results]



def get_genai_advice(user_id):
    """Returns the most recent advice from the genai model.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    advice = random.choice([
        'Your heart rate indicates you can push yourself further. You got this!',
        "You're doing great! Keep up the good work.",
        'You worked hard yesterday, take it easy today.',
        'You have burned 100 calories so far today!',
    ])
    image = random.choice([
        'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        None,
    ])
    return {
        'advice_id': 'advice1',
        'timestamp': '2024-01-01 00:00:00',
        'content': advice,
        'image': image,
    }
