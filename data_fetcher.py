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


users = {
    'user1': {
        'full_name': 'Remi',
        'username': 'remi_the_rems',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user2', 'user3', 'user4'],
    },
    'user2': {
        'full_name': 'Blake',
        'username': 'blake',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1'],
    },
    'user3': {
        'full_name': 'Jordan',
        'username': 'jordanjordanjordan',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1', 'user4'],
    },
    'user4': {
        'full_name': 'Gemmy',
        'username': 'gems',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1', 'user3'],
    },
}


def get_user_sensor_data(user_id, workout_id):
    """
    Returns a list of timestamped sensor data for a given workout from BigQuery.
    
    Each item in the returned list is a dictionary with the following keys:
      - sensor_type: The human-readable name of the sensor (from SensorTypes.Name)
      - timestamp: The datetime when the sensor reading was taken (from SensorData.Timestamp)
      - data: The sensor reading value (from SensorData.SensorValue)
      - units: The measurement units (from SensorTypes.Units)
    
    Although the function receives a user_id, the sensor data is retrieved by filtering on workout_id,
    since each workout is uniquely associated with one user.
    """
    from google.cloud import bigquery
    
    # Use your actual project ID and dataset name. Here, we assume:
    # Project ID: "roberttechx25"
    # Dataset (or COURSE_CODE): "ISE"
    project_id = "roberttechx25"
    dataset = "ISE"
    
    client = bigquery.Client(project=project_id)
    
    query = f"""
        SELECT
            st.Name AS sensor_type,
            sd.Timestamp AS timestamp,
            sd.SensorValue AS data,
            st.Units AS units
        FROM `{project_id}.{dataset}.SensorData` sd
        JOIN `{project_id}.{dataset}.SensorTypes` st
            ON sd.SensorId = st.SensorId
        WHERE sd.WorkoutID = @workout_id
        ORDER BY sd.Timestamp
    """
    
    query_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("workout_id", "STRING", workout_id)
        ]
    )
    
    query_job = client.query(query, job_config=query_config)
    sensor_data = [dict(row) for row in query_job.result()]
    
    return sensor_data



def get_user_workouts(user_id):
    """Returns a list of user's workouts.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    workouts = []
    for index in range(random.randint(1, 3)):
        random_lat_lng_1 = (
            1 + random.randint(0, 100) / 100,
            4 + random.randint(0, 100) / 100,
        )
        random_lat_lng_2 = (
            1 + random.randint(0, 100) / 100,
            4 + random.randint(0, 100) / 100,
        )
        workouts.append({
            'workout_id': f'workout{index}',
            'start_timestamp': '2024-01-01 00:00:00',
            'end_timestamp': '2024-01-01 00:30:00',
            'start_lat_lng': random_lat_lng_1,
            'end_lat_lng': random_lat_lng_2,
            'distance': random.randint(0, 200) / 10.0,
            'steps': random.randint(0, 20000),
            'calories_burned': random.randint(0, 100),
        })
    return workouts


def get_user_profile(user_id):
    """Returns information about the given user."""

    client = bigquery.Client(project="roberttechx25")

    # CHANGED: Updated query to use parameter placeholder @user_id
    # Also aliased u.ImageUrl as profile_image to match what modules.py expects.
    query = """
        SELECT
            u.name AS full_name,  
            u.username,
            u.DateOfBirth,
            u.ImageUrl AS profile_image,  -- CHANGED: aliasing ImageUrl as profile_image
            ARRAY_AGG(f.UserId2 IGNORE NULLS) AS friends
        FROM `roberttechx25.ISE.Users` AS u
        LEFT JOIN `roberttechx25.ISE.Friends` AS f
            ON u.UserId = f.UserId1
        WHERE u.UserId = @user_id
        GROUP BY u.name, u.username, u.DateOfBirth, u.ImageUrl
    """
    # This query was created with the assistance of ChatGPT

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

    # CHANGED: Specify the project in the client instantiation.
    client = bigquery.Client(project="roberttechx25")

    # CHANGED: Updated query to use parameter placeholder @user_id and alias AuthorId.
    query = """
        SELECT *, AuthorId as user_id_alias
        FROM `roberttechx25.ISE.Posts`
        WHERE AuthorId = @user_id
        ORDER BY timestamp DESC
    """

    query_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)
        ]
    )  # This part was created with the assistance of ChatGPT

    query_job = client.query(query, job_config=query_config)
    results = query_job.result()
    posts = [dict(row) for row in results]
    # CHANGED: Ensure that each post dictionary includes a 'user_id' key.
    for post in posts:
        if 'user_id_alias' in post:
            post['user_id'] = post.pop('user_id_alias')
        # CHANGED: If 'timestamp' is missing, provide a default value that matches the format.
        if 'timestamp' not in post:
            post['timestamp'] = "1970-01-01 00:00:00"  # CHANGED: Default valid timestamp
        # CHANGED: If 'content' is missing, provide a default value.
        if 'content' not in post:
            post['content'] = "No Content Available"
        # CHANGED: If 'image' is missing, provide a default value.
        if 'image' not in post:
            post['image'] = None
    return posts


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
