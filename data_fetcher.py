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
        return {
            "distance": 0.0,
            "steps": 0,
            "calories": 0,
            "advice_timestamp": "1970-01-01 00:00:00"
        }
    
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
    return {
        "distance": total_distance,
        "steps": total_steps,
        "calories": total_calories,
        "advice_timestamp": advice_timestamp
    }


def get_genai_advice(user_id):
    """
    Returns a piece of motivational advice from Vertex AI based on the user's data.
    
    This function:
      1. Retrieves user data and the aggregated daily workout data.
      2. Constructs a personalized prompt including workout metrics using the user's username.
      3. Calls Vertex AI to generate multiple pieces of advice.
      4. Randomly selects one piece of advice and, if it doesn't include the user's username, appends the username.
      5. Randomly decides on an image.
      6. Returns a dictionary with keys: advice_id, timestamp, content, and image.
    """
    import vertexai
    import json
    import random
    from vertexai.generative_models import GenerativeModel, GenerationConfig

    user_data = get_user_profile(user_id)
    username = user_data.get("username", "User")

    daily_data = get_user_daily_workout_data(user_id)
    total_distance = daily_data["distance"]
    total_steps = daily_data["steps"]
    total_calories = daily_data["calories"]
    advice_timestamp = daily_data["advice_timestamp"]

    # Construct a detailed prompt that includes the user's workout metrics.
    prompt = (
        f"User {username} has just finished their workout today, covering {total_distance:.1f} km, "
        f"taking {total_steps} steps, and burning {total_calories} calories. Provide a JSON array of 4 unique, "
        f"concise motivational advices. Each advice should be a single sentence that acknowledges these metrics, "
        f"offers personalized encouragement, and ideally references at least one of these workout details."
    )

    PROJECT_ID = "roberttechx25"
    RESPONSE_SCHEMA = {
        "type": "array",
        "items": {"type": "string"}
    }
    vertexai.init(project=PROJECT_ID, location="us-central1")
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
    
    fallback = f"Keep pushing forward, {username}—every step counts!"
    if not advices:
        chosen_advice = fallback
    else:
        chosen_advice = random.choice(advices)
        # Instead of replacing the advice if username is missing, we append it.
        if username not in chosen_advice:
            chosen_advice = f"{chosen_advice} - {username}"

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
    