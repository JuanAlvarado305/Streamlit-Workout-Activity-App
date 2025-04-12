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
import datetime
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
    """
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
        query_parameters=[bigquery.ScalarQueryParameter("workout_id", "STRING", workout_id)]
    )
    query_job = client.query(query, job_config=query_config)
    sensor_data = [dict(row) for row in query_job.result()]
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
            ORDER BY StartTimestamp DESC
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
    query = """
        SELECT
            u.name AS full_name,  
            u.username,
            u.DateOfBirth,
            u.ImageUrl AS profile_image,
            ARRAY_AGG(f.UserId2 IGNORE NULLS) AS friends
        FROM `roberttechx25.ISE.Users` AS u
        LEFT JOIN `roberttechx25.ISE.Friends` AS f
            ON u.UserId = f.UserId1
        WHERE u.UserId = @user_id
        GROUP BY u.name, u.username, u.DateOfBirth, u.ImageUrl
    """
    query_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)]
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
    query = """
        SELECT *, AuthorId as user_id_alias
        FROM `roberttechx25.ISE.Posts`
        WHERE AuthorId = @user_id
        ORDER BY timestamp DESC
    """
    query_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)]
    )
    query_job = client.query(query, job_config=query_config)
    results = query_job.result()
    posts = [dict(row) for row in results]
    for post in posts:
        if 'user_id_alias' in post:
            post['user_id'] = post.pop('user_id_alias')
        if 'timestamp' not in post:
            post['timestamp'] = "1970-01-01 00:00:00"
        if 'content' not in post:
            post['content'] = "No Content Available"
        if 'image' not in post:
            post['image'] = None
    return posts

def get_friends_posts(user_id): #written with help from Gemini
    """Returns a list of posts from the user's friends, ordered by timestamp descending."""
    client = bigquery.Client(project='roberttechx25')

    # Query to get friends' posts
    query = """
        SELECT
            p.PostId AS PostId,
            p.AuthorId AS AuthorId,
            p.Timestamp AS Timestamp,
            p.ImageUrl AS ImageUrl,
            p.Content AS Content,
            u.Name AS Username,
        FROM `roberttechx25.ISE.Posts` AS p
        JOIN `roberttechx25.ISE.Friends` AS f ON p.AuthorId = f.UserId2
        JOIN `roberttechx25.ISE.Users` AS u ON p.AuthorId = u.UserId -- Join with Users to get name
        WHERE f.UserId1 = @user_id -- Find posts where the author is a friend (UserId2) of the current user (UserId1)
        ORDER BY p.Timestamp DESC
    """

    query_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)
        ]
    )

    try:
        query_job = client.query(query, job_config=query_config)
        results = query_job.result()
        # Convert rows to dictionaries matching expected keys in display_post, adding author_name
        return [
            {
                'post_id': row.PostId,
                'AuthorId': row.AuthorId,
                'Username': row.Username,
                'Timestamp': row.Timestamp,
                'ImageUrl': row.ImageUrl,
                'Content': row.Content
             } for row in results]
    except Exception as e:
        print(f"Error fetching friends' posts for user {user_id}: {e}")
        return [] # Return empty list on error


###############################
# New helper function for GenAI advice
###############################
def get_user_daily_workout_data(user_id) -> dict:
    """
    Retrieves the user's workout data for today (or for the most recent workout),
    aggregates relevant metrics, and returns a summary.
    
    Returns a dictionary with:
      - distance: Total distance (km)
      - steps: Total steps
      - calories: Total calories burned
      - advice_timestamp: The most recent EndTimestamp in "YYYY-MM-DD HH:MM:SS" format
    """
    client = bigquery.Client(project="roberttechx25")
    query = f"""
        SELECT 
          StartTimestamp, 
          EndTimestamp, 
          TotalDistance, 
          TotalSteps, 
          CaloriesBurned
        FROM `roberttechx25.ISE.Workouts`
        WHERE UserId = '{user_id}'
          AND DATE(EndTimestamp) = CURRENT_DATE()
        ORDER BY EndTimestamp DESC
    """
    job = client.query(query)
    results = list(job.result())
    if not results:
        return {"distance": 0.0, "steps": 0, "calories": 0, "advice_timestamp": "1970-01-01 00:00:00"}
    
    total_distance = 0.0
    total_steps = 0
    total_calories = 0
    most_recent_end = None
    for row in results:
        total_distance += row["TotalDistance"] or 0
        total_steps += row["TotalSteps"] or 0
        total_calories += row["CaloriesBurned"] or 0
        end_ts = row["EndTimestamp"]
        if most_recent_end is None or end_ts > most_recent_end:
            most_recent_end = end_ts
    advice_timestamp = most_recent_end.strftime("%Y-%m-%d %H:%M:%S") if most_recent_end else "1970-01-01 00:00:00"
    return {"distance": total_distance, "steps": total_steps, "calories": total_calories, "advice_timestamp": advice_timestamp}


def get_genai_advice(user_id):
    """
    Returns a piece of motivational advice from Vertex AI based on the user's data.
    
    This function:
      1. Retrieves user data and the aggregated daily workout data.
      2. Constructs a personalized prompt including workout metrics using the user's username.
      3. Calls Vertex AI to generate multiple pieces of advice.
      4. Randomly selects one piece of advice and, if it doesn't include the user's username, uses a fallback message.
      5. Randomly decides on an image.
      6. Returns a dictionary with keys: advice_id, timestamp, content, and image.
    """
    import vertexai
    import json
    from vertexai.generative_models import GenerativeModel, GenerationConfig

    user_data = get_user_profile(user_id)
    username = user_data.get("username", "User")

    daily_data = get_user_daily_workout_data(user_id)
    total_distance = daily_data["distance"]
    total_steps = daily_data["steps"]
    total_calories = daily_data["calories"]
    advice_timestamp = daily_data["advice_timestamp"]

    prompt = (
        f"Provide a list of 4 concise motivational advices for {username}. "
        f"Today, they have covered {total_distance:.1f} km, taken {total_steps} steps, "
        f"and burned {total_calories} calories. Each advice should be a single sentence "
        f"that is encouraging and acknowledges their effort."
    )

    PROJECT_ID = "roberttechx25"
    RESPONSE_SCHEMA = {"type": "array", "items": {"type": "string"}}
    
    fallback = f"Keep pushing forward, {username}—every step counts!"
    
    try:
        vertexai.init(project=PROJECT_ID, location="us-central1")
    except Exception:
        return {
            "advice_id": "advice1",
            "timestamp": advice_timestamp,
            "content": fallback,
            "image": random.choice([
                "https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3",
                None
            ])
        }
    
    model = GenerativeModel("gemini-1.5-flash-002")
    generation_config = GenerationConfig(
        response_mime_type="application/json",
        response_schema=RESPONSE_SCHEMA,
        temperature=0.7,
        max_output_tokens=100
    )
    response = model.generate_content(prompt, generation_config=generation_config)

    def parse_response_to_advice(response_obj) -> list:
        try:
            raw = response_obj.candidates[0].content.text
            advices = json.loads(raw)
            if isinstance(advices, list):
                return advices
        except Exception:
            return []
    advices = parse_response_to_advice(response)
    
    if not advices:
        chosen_advice = fallback
    else:
        chosen_advice = random.choice(advices)
        if username.lower() not in chosen_advice.lower():
            chosen_advice = fallback

    image = random.choice([
        "https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3",
        None
    ])

    return {
        "advice_id": "advice1",
        "timestamp": advice_timestamp,
        "content": chosen_advice,
        "image": image,
    }
