# #############################################################################
# # data_fetcher.py
# #
# # This file contains functions to fetch data needed for the app.
# #
# # You will re-write these functions in Unit 3, and are welcome to alter the
# # data returned in the meantime. We will replace this file with other data when
# # testing earlier units.
# #############################################################################

# import random
# import datetime
# import uuid
# import hashlib
# from google.cloud import bigquery

# users = {
#     'user1': {
#         'full_name': 'Remi',
#         'username': 'remi_the_rems',
#         'date_of_birth': '1990-01-01',
#         'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
#         'friends': ['user2', 'user3', 'user4'],
#     },
#     'user2': {
#         'full_name': 'Blake',
#         'username': 'blake',
#         'date_of_birth': '1990-01-01',
#         'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
#         'friends': ['user1'],
#     },
#     'user3': {
#         'full_name': 'Jordan',
#         'username': 'jordanjordanjordan',
#         'date_of_birth': '1990-01-01',
#         'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
#         'friends': ['user1', 'user4'],
#     },
#     'user4': {
#         'full_name': 'Gemmy',
#         'username': 'gems',
#         'date_of_birth': '1990-01-01',
#         'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
#         'friends': ['user1', 'user3'],
#     },
# }


# def get_user_sensor_data(user_id, workout_id):
#     """
#     Returns a list of timestamped sensor data for a given workout from BigQuery.
#     Each item in the returned list is a dictionary with the following keys:
#       - sensor_type: The human-readable name of the sensor (from SensorTypes.Name)
#       - timestamp: The datetime when the sensor reading was taken (from SensorData.Timestamp)
#       - data: The sensor reading value (from SensorData.SensorValue)
#       - units: The measurement units (from SensorTypes.Units)
#     """
#     project_id = "roberttechx25"
#     dataset = "ISE"
#     client = bigquery.Client(project=project_id)
#     query = f"""
#         SELECT
#             st.Name AS sensor_type,
#             sd.Timestamp AS timestamp,
#             sd.SensorValue AS data,
#             st.Units AS units
#         FROM `{project_id}.{dataset}.SensorData` sd
#         JOIN `{project_id}.{dataset}.SensorTypes` st
#             ON sd.SensorId = st.SensorId
#         WHERE sd.WorkoutID = @workout_id
#         ORDER BY sd.Timestamp
#     """
#     query_config = bigquery.QueryJobConfig(
#         query_parameters=[bigquery.ScalarQueryParameter("workout_id", "STRING", workout_id)]
#     )
#     query_job = client.query(query, job_config=query_config)
#     sensor_data = [dict(row) for row in query_job.result()]
#     return sensor_data


# def get_user_workouts(user_id):
#     """Returns a list of user's workouts from the database.
    
#     If no workouts are found or there's an error, returns mock data.
#     """
#     # Define fallback mock data
#     mock_workouts = [
#         {
#             'workout_id': 'workout1',
#             'start_timestamp': '2025-04-01 08:00:00',
#             'end_timestamp': '2025-04-01 09:00:00',
#             'start_lat_lng': (37.7749, -122.4194),
#             'end_lat_lng': (37.7749, -122.4194),
#             'distance': 5.2,
#             'steps': 7500,
#             'calories_burned': 350,
#         },
#         {
#             'workout_id': 'workout2',
#             'start_timestamp': '2025-04-03 17:00:00',
#             'end_timestamp': '2025-04-03 18:30:00',
#             'start_lat_lng': (34.0522, -118.2437),
#             'end_lat_lng': (34.0522, -118.2437),
#             'distance': 7.8,
#             'steps': 11200,
#             'calories_burned': 520,
#         },
#         {
#             'workout_id': 'workout3',
#             'start_timestamp': '2025-04-05 10:00:00',
#             'end_timestamp': '2025-04-05 11:15:00',
#             'start_lat_lng': (40.7128, -74.0060),
#             'end_lat_lng': (40.7128, -74.0060),
#             'distance': 6.5,
#             'steps': 9300,
#             'calories_burned': 410,
#         },
#     ]
    
#     try:
#         # Connect to BigQuery
#         client = bigquery.Client(project="roberttechx25")
        
#         # SQL query to fetch user workouts
#         query = """
#             SELECT *
#             FROM `roberttechx25.ISE.Workouts`
#             WHERE UserId = @user_id
#             ORDER BY StartTimestamp DESC
#         """
        
#         # Configure query parameters
#         query_config = bigquery.QueryJobConfig(
#             query_parameters=[
#                 bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)
#             ]
#         )
        
#         # Execute query
#         query_job = client.query(query, job_config=query_config)
#         results = query_job.result()
        
#         # Convert results to list of dictionaries
#         workouts = [dict(row) for row in results]
        
#         # Return query results if found, otherwise return mock data
#         if workouts:
#             return workouts
#         else:
#             print(f"No workouts found for user {user_id}, returning mock data")
#             return mock_workouts
            
#     except Exception as e:
#         # Log the error and return mock data as fallback
#         print(f"Error fetching workouts from database: {e}")
#         return mock_workouts

#     """
#     This check was causing a traceback because users is not defined so I commented it out
    
#     if user_id not in users:
#         return workouts
#     return workouts
#     """
    

# def get_user_profile(user_id):
#     """Returns information about the given user."""
#     client = bigquery.Client(project="roberttechx25")
#     query = """
#         SELECT
#             u.name AS full_name,  
#             u.username,
#             u.DateOfBirth,
#             u.ImageUrl AS profile_image,
#             ARRAY_AGG(f.UserId2 IGNORE NULLS) AS friends
#         FROM `roberttechx25.ISE.Users` AS u
#         LEFT JOIN `roberttechx25.ISE.Friends` AS f
#             ON u.UserId = f.UserId1
#         WHERE u.UserId = @user_id
#         GROUP BY u.name, u.username, u.DateOfBirth, u.ImageUrl
#     """
#     query_config = bigquery.QueryJobConfig(
#         query_parameters=[bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)]
#     )
#     query_job = client.query(query, job_config=query_config)
#     results = list(query_job.result())

#     if results:
#         return dict(results[0])
#     else:
#         return {}


# def get_user_posts(user_id):
#     """Returns a list of a user's posts."""
#     client = bigquery.Client(project="roberttechx25")
#     query = """
#         SELECT *, AuthorId as user_id_alias
#         FROM `roberttechx25.ISE.Posts`
#         WHERE AuthorId = @user_id
#         ORDER BY timestamp DESC
#     """
#     query_config = bigquery.QueryJobConfig(
#         query_parameters=[bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)]
#     )
#     query_job = client.query(query, job_config=query_config)
#     results = query_job.result()
#     posts = [dict(row) for row in results]
#     for post in posts:
#         if 'user_id_alias' in post:
#             post['user_id'] = post.pop('user_id_alias')
#         if 'timestamp' not in post:
#             post['timestamp'] = "1970-01-01 00:00:00"
#         if 'content' not in post:
#             post['content'] = "No Content Available"
#         if 'image' not in post:
#             post['image'] = None
#     return posts

# def get_friends_posts(user_id):
#     """Returns a list of posts from the user's friends, ordered by timestamp descending."""
#     client = bigquery.Client(project='roberttechx25')
    
#     # Modified query to check for friendships in both directions
#     query = """
#         SELECT
#             p.PostId AS PostId,
#             p.AuthorId AS AuthorId,
#             p.Timestamp AS Timestamp,
#             p.ImageUrl AS ImageUrl,
#             p.Content AS Content,
#             u.Name AS Username,
#         FROM `roberttechx25.ISE.Posts` AS p
#         JOIN `roberttechx25.ISE.Users` AS u ON p.AuthorId = u.UserId
#         JOIN (
#             -- Union of both friendship directions
#             SELECT UserId2 AS FriendId FROM `roberttechx25.ISE.Friends` WHERE UserId1 = @user_id
#             UNION DISTINCT
#             SELECT UserId1 AS FriendId FROM `roberttechx25.ISE.Friends` WHERE UserId2 = @user_id
#         ) AS friends ON p.AuthorId = friends.FriendId
#         ORDER BY p.Timestamp DESC
#     """
    
#     query_config = bigquery.QueryJobConfig(
#         query_parameters=[
#             bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)
#         ]
#     )
    
#     try:
#         query_job = client.query(query, job_config=query_config)
#         results = query_job.result()
#         # Convert rows to dictionaries matching expected keys in display_post, adding author_name
#         return [
#             {
#                 'post_id': row.PostId,
#                 'AuthorId': row.AuthorId,
#                 'Username': row.Username,
#                 'Timestamp': row.Timestamp,
#                 'ImageUrl': row.ImageUrl,
#                 'Content': row.Content 
#             } for row in results]
#     except Exception as e:
#         print(f"Error fetching friends' posts for user {user_id}: {e}")
#         return [] # Return empty list on error


# ###############################
# # New helper function for GenAI advice
# ###############################
# def get_user_daily_workout_data(user_id) -> dict:
#     """
#     Retrieves the user's workout data for today (or for the most recent workout),
#     aggregates relevant metrics, and returns a summary.
    
#     Returns a dictionary with:
#       - distance: Total distance (km)
#       - steps: Total steps
#       - calories: Total calories burned
#       - advice_timestamp: The most recent EndTimestamp in "YYYY-MM-DD HH:MM:SS" format
#     """
#     from google.cloud import bigquery
    
#     client = bigquery.Client(project="roberttechx25")
#     query = """
#         SELECT 
#           StartTimestamp, 
#           EndTimestamp, 
#           TotalDistance, 
#           TotalSteps, 
#           CaloriesBurned
#         FROM `roberttechx25.ISE.Workouts`
#         WHERE UserId = @user_id
#           AND DATE(EndTimestamp) = CURRENT_DATE()
#         ORDER BY EndTimestamp DESC
#     """
#     query_config = bigquery.QueryJobConfig(
#         query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
#     )
#     job = client.query(query, job_config=query_config)
#     results = list(job.result())
    
#     if not results:
#         return {"distance": 0.0, "steps": 0, "calories": 0, "advice_timestamp": "1970-01-01 00:00:00"}
    
#     total_distance = 0.0
#     total_steps = 0
#     total_calories = 0
#     most_recent_end = None
    
#     for row in results:
#         total_distance += row["TotalDistance"] or 0
#         total_steps += row["TotalSteps"] or 0
#         total_calories += row["CaloriesBurned"] or 0
#         end_ts = row["EndTimestamp"]
#         if most_recent_end is None or end_ts > most_recent_end:
#             most_recent_end = end_ts
            
#     advice_timestamp = most_recent_end.strftime("%Y-%m-%d %H:%M:%S") if most_recent_end else "1970-01-01 00:00:00"
    
#     return {
#         "distance": total_distance,
#         "steps": total_steps,
#         "calories": total_calories,
#         "advice_timestamp": advice_timestamp
#     }

# def get_genai_advice(user_id):
#     """
#     Returns a piece of motivational advice from Vertex AI based on the user's data.
    
#     This function:
#       1. Retrieves user data and the aggregated daily workout data.
#       2. Constructs a personalized prompt including workout metrics using the user's username.
#       3. Calls Vertex AI to generate multiple pieces of advice.
#       4. Randomly selects one piece of advice and, if it doesn't include the user's username, uses a fallback message.
#       5. Randomly decides on an image.
#       6. Returns a dictionary with keys: advice_id, timestamp, content, and image.
#     """
#     import vertexai
#     import json
#     from vertexai.generative_models import GenerativeModel, GenerationConfig

#     user_data = get_user_profile(user_id)
#     username = user_data.get("username", "User")

#     daily_data = get_user_daily_workout_data(user_id)
#     total_distance = daily_data["distance"]
#     total_steps = daily_data["steps"]
#     total_calories = daily_data["calories"]
#     advice_timestamp = daily_data["advice_timestamp"]

#     prompt = (
#         f"Provide a list of 4 concise motivational advices for {username}. "
#         f"Today, they have covered {total_distance:.1f} km, taken {total_steps} steps, "
#         f"and burned {total_calories} calories. Each advice should be a single sentence "
#         f"that is encouraging and acknowledges their effort."
#     )

#     PROJECT_ID = "roberttechx25"
#     RESPONSE_SCHEMA = {"type": "array", "items": {"type": "string"}}
    
#     fallback = f"Keep pushing forward, {username}—every step counts!"
    
#     try:
#         vertexai.init(project=PROJECT_ID, location="us-central1")
#     except Exception:
#         return {
#             "advice_id": "advice1",
#             "timestamp": advice_timestamp,
#             "content": fallback,
#             "image": random.choice([
#                 "https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3",
#                 None
#             ])
#         }
    
#     model = GenerativeModel("gemini-1.5-flash-002")
#     generation_config = GenerationConfig(
#         response_mime_type="application/json",
#         response_schema=RESPONSE_SCHEMA,
#         temperature=0.7,
#         max_output_tokens=100
#     )
#     response = model.generate_content(prompt, generation_config=generation_config)

#     def parse_response_to_advice(response_obj) -> list:
#         try:
#             raw = response_obj.candidates[0].content.text
#             advices = json.loads(raw)
#             if isinstance(advices, list):
#                 return advices
#         except Exception:
#             return []
#     advices = parse_response_to_advice(response)
    
#     if not advices:
#         chosen_advice = fallback
#     else:
#         chosen_advice = random.choice(advices)
#         if username.lower() not in chosen_advice.lower():
#             chosen_advice = fallback

#     image = random.choice([
#         "https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3",
#         None
#     ])

#     return {
#         "advice_id": "advice1",
#         "timestamp": advice_timestamp,
#         "content": chosen_advice,
#         "image": image,
#     }

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def login_user(username, password):
#     client = bigquery.Client(project="roberttechx25")

#     query = """
#         SELECT UserId, Username
#         FROM `roberttechx25.ISE.Users`
#         WHERE Username = @username
#         AND password_hash = @password_hash
#     """
    
#     query_config = bigquery.QueryJobConfig(
#         query_parameters=[
#             bigquery.ScalarQueryParameter("username", "STRING", username),
#             bigquery.ScalarQueryParameter("password_hash", "STRING", hash_password(password))
#         ]
#     )
    
#     results = list(client.query(query, job_config=query_config).result())

#     if results:
#         return dict(results[0])  # returns UserId and Username
#     else:
#         return None


# def register_user(username, full_name, password):
#     client = bigquery.Client(project="roberttechx25")

#     #Verify that the user exists
#     check_query = """
#         SELECT Username FROM `roberttechx25.ISE.Users`
#         WHERE Username = @username
#     """
#     config = bigquery.QueryJobConfig(
#         query_parameters=[
#             bigquery.ScalarQueryParameter("username", "STRING", username)
#         ]
#     )
#     existing = list(client.query(check_query, job_config=config).result())
#     if existing:
#         return "That username is already in use."

#     #Generates Id and Hash
#     user_id = str(uuid.uuid4())
#     password_hash = hash_password(password)

#     #Insert the new user
#     insert_query = f"""
#         INSERT INTO `roberttechx25.ISE.Users` (UserId, Name, Username, password_hash)
#         VALUES (@user_id, @name, @username, @password_hash)
#     """
#     insert_config = bigquery.QueryJobConfig(
#         query_parameters=[
#             bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
#             bigquery.ScalarQueryParameter("name", "STRING", full_name),
#             bigquery.ScalarQueryParameter("username", "STRING", username),
#             bigquery.ScalarQueryParameter("password_hash", "STRING", password_hash),
#         ]
#     )
#     client.query(insert_query, job_config=insert_config)

#     return "¡Successfully registered!"

# def get_latest_two_challenges():
#     """
#     Pulls the two most recent challenge date‐ranges from the DB,
#     returning ((this_start, this_end), (last_start, last_end)).
#     """
#     client = bigquery.Client(project="roberttechx25")
#     query = """
#         SELECT StartDate, EndDate
#         FROM `roberttechx25.ISE.Challenges`
#         ORDER BY EndDate DESC
#         LIMIT 2
#     """
#     rows = list(client.query(query).result())
#     if len(rows) < 2:
#         # Fallback: infer last week as 7 days before
#         this_start, this_end = rows[0].StartDate, rows[0].EndDate
#         last_start = this_start - datetime.timedelta(days=7)
#         last_end   = this_end   - datetime.timedelta(days=7)
#         return (this_start, this_end), (last_start, last_end)
#     return (rows[0].StartDate, rows[0].EndDate), (rows[1].StartDate, rows[1].EndDate)


# def get_week_challenges(start_date, end_date):
#     """
#     Returns data for weekly challenges between the given dates
    
#     Args:
#         start_date: date or string in format YYYY-MM-DD
#         end_date: date or string in format YYYY-MM-DD
        
#     Returns:
#         A list with two elements:
#         - Element 0: [start_date, end_date] 
#         - Element 1: List of 3 lists (one for each challenge type: distance, steps, workouts)
#           Each inner list contains dictionaries of participants with their stats
#     """
#     client = bigquery.Client(project="roberttechx25")
    
#     # Convert dates to string format if they aren't already
#     if not isinstance(start_date, str):
#         start_date = start_date.strftime("%Y-%m-%d")
#     if not isinstance(end_date, str):
#         end_date = end_date.strftime("%Y-%m-%d")
    
#     # First, get the challenge IDs for the given date range
#     challenge_query = """
#         SELECT ChallengeId, Type
#         FROM `roberttechx25.ISE.Challenges`
#         WHERE StartDate <= @end_date AND EndDate >= @start_date
#         ORDER BY Type
#     """
    
#     challenge_params = [
#         bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
#         bigquery.ScalarQueryParameter("end_date", "DATE", end_date)
#     ]
    
#     challenge_job_config = bigquery.QueryJobConfig(query_parameters=challenge_params)
#     challenge_results = client.query(challenge_query, job_config=challenge_job_config).result()
#     challenges = [dict(row) for row in challenge_results]
    
#     if not challenges:
#         return [[start_date, end_date], [[], [], []]]
    
#     # For each challenge, get the participants and their metrics
#     challenge_data = [[], [], []]  # Distance, Steps, Workouts
    
#     for challenge in challenges:
#         challenge_id = challenge["ChallengeId"]
#         challenge_type = challenge["Type"]
        
#         # Get participants and their metrics for this challenge
#         metrics_query = """
#             SELECT 
#                 cm.UserId,
#                 u.Username,
#                 u.ImageUrl AS profile_image,
#                 cm.Value
#             FROM `roberttechx25.ISE.ChallengeMetrics` cm
#             JOIN `roberttechx25.ISE.Users` u ON cm.UserId = u.UserId
#             WHERE cm.ChallengeId = @challenge_id
#             ORDER BY cm.Value DESC
#             LIMIT 10
#         """
        
#         metrics_params = [
#             bigquery.ScalarQueryParameter("challenge_id", "STRING", challenge_id)
#         ]
        
#         metrics_job_config = bigquery.QueryJobConfig(query_parameters=metrics_params)
#         metrics_results = client.query(metrics_query, job_config=metrics_job_config).result()
        
#         participants = []
#         for row in metrics_results:
#             participant = {
#                 "user_id": row["UserId"],
#                 "username": row["Username"],
#                 "profile_image": row["profile_image"],
#                 "value": row["Value"]
#             }
#             participants.append(participant)
        
#         # Add the participants to the appropriate challenge type list
#         if challenge_type.lower() == "distance":
#             challenge_data[0] = participants
#         elif challenge_type.lower() == "steps":
#             challenge_data[1] = participants
#         elif challenge_type.lower() == "workouts":
#             challenge_data[2] = participants
    
#     #print(challenge_data)
#     return [[start_date, end_date], challenge_data]

# def get_current_week_challenges():
#     """
#     Returns data for the current week's challenges
    
#     Returns:
#         Same format as get_week_challenges
#     """
#     (this_start, this_end), _ = get_latest_two_challenges()
#     return get_week_challenges(this_start, this_end)

# def get_last_week_challenges():
#     """
#     Returns data for last week's challenges
    
#     Returns:
#         Same format as get_week_challenges
#     """
#     # Calculate last week's start and end dates
#     _, (last_start, last_end) = get_latest_two_challenges()
#     return get_week_challenges(last_start, last_end)

# def get_challenge_id(start_date, end_date, challenge_type):
#     """
#     Retrieves the challenge ID for a specific type and date range
    
#     Args:
#         start_date: date or string in format YYYY-MM-DD
#         end_date: date or string in format YYYY-MM-DD
#         challenge_type: string - "distance", "steps", or "workouts"
        
#     Returns:
#         String - the challenge ID or None if not found
#     """
#     client = bigquery.Client(project="roberttechx25")
    
#     # Convert dates to string format if they aren't already
#     if not isinstance(start_date, str):
#         start_date = start_date.strftime("%Y-%m-%d")
#     if not isinstance(end_date, str):
#         end_date = end_date.strftime("%Y-%m-%d")
    
#     query = """
#         SELECT ChallengeId
#         FROM `roberttechx25.ISE.Challenges`
#         WHERE StartDate = @start_date 
#         AND EndDate = @end_date
#         AND LOWER(Type) = LOWER(@challenge_type)
#     """
    
#     params = [
#         bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
#         bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
#         bigquery.ScalarQueryParameter("challenge_type", "STRING", challenge_type)
#     ]
    
#     job_config = bigquery.QueryJobConfig(query_parameters=params)
#     results = client.query(query, job_config=job_config).result()
#     results_list = list(results)
    
#     if results_list:
#         return results_list[0]["ChallengeId"]
#     return None

# def get_joined_challenge(challenge_id, user_id):
#     """
#     Checks if a user has joined a specific challenge
    
#     Args:
#         challenge_id: String - the challenge ID
#         user_id: String - the user ID
        
#     Returns:
#         Boolean - True if the user has joined the challenge, False otherwise
#     """
#     client = bigquery.Client(project="roberttechx25")
    
#     query = """
#         SELECT COUNT(*) as count
#         FROM `roberttechx25.ISE.ChallengeParticipants`
#         WHERE ChallengeId = @challenge_id AND UserId = @user_id
#     """
    
#     params = [
#         bigquery.ScalarQueryParameter("challenge_id", "STRING", challenge_id),
#         bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
#     ]
    
#     job_config = bigquery.QueryJobConfig(query_parameters=params)
#     results = client.query(query, job_config=job_config).result()
#     results_list = list(results)
    
#     if results_list and results_list[0]["count"] > 0:
#         return True
#     return False

# def join_challenge(challenge_id, user_id):
#     """
#     Adds a user to a challenge
    
#     Args:
#         challenge_id: String - the challenge ID
#         user_id: String - the user ID
        
#     Returns:
#         Boolean - True if successful, False otherwise
#     """
#     # Check if the user has already joined this challenge
#     if get_joined_challenge(challenge_id, user_id):
#         return False
    
#     client = bigquery.Client(project="roberttechx25")
    
#     query = """
#         INSERT INTO `roberttechx25.ISE.ChallengeParticipants` (ChallengeId, UserId)
#         VALUES (@challenge_id, @user_id)
#     """
    
#     params = [
#         bigquery.ScalarQueryParameter("challenge_id", "STRING", challenge_id),
#         bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
#     ]
    
#     job_config = bigquery.QueryJobConfig(query_parameters=params)
    
#     try:
#         client.query(query, job_config=job_config).result()
#         return True
#     except Exception as e:
#         print(f"Error joining challenge: {e}")
#         return False

# def get_challenge_participant_counts():
#     """
#     Gets current participant counts for active challenges
    
#     Returns:
#         Dictionary with challenge types as keys and participant counts as values
#     """
#     client = bigquery.Client(project="roberttechx25")
    
#     query = """
#         SELECT 
#             c.Type,
#             COUNT(DISTINCT cp.UserId) as participant_count
#         FROM `roberttechx25.ISE.Challenges` c
#         LEFT JOIN `roberttechx25.ISE.ChallengeParticipants` cp ON c.ChallengeId = cp.ChallengeId
#         WHERE CURRENT_DATE() BETWEEN c.StartDate AND c.EndDate
#         GROUP BY c.Type
#     """
    
#     results = client.query(query).result()
    
#     counts = {
#         "distance": 0,
#         "steps": 0,
#         "workouts": 0
#     }
    
#     for row in results:
#         challenge_type = row["Type"].lower()
#         if challenge_type in counts:
#             counts[challenge_type] = row["participant_count"]
    
#     return counts






#############################################################################
# data_fetcher.py
#
# This file has been refactored to securely connect to your new
# Google Cloud project and remove hardcoded credentials.
#
#############################################################################
import traceback
import secrets
# data_fetcher.py
from datetime import datetime, timedelta, timezone
import os
import streamlit as st # <-- Change: Added for st.secrets access
import random
import datetime
import uuid
import hashlib
import json
from google.cloud import bigquery
from google.oauth2 import service_account # <-- Change: Added for service account credentials
import vertexai # <-- Change: Added to top-level imports
from vertexai.generative_models import GenerativeModel, GenerationConfig # <-- Change: Added to top-level imports

# --- New Helper Function for Secure BigQuery Connection ---
# data_fetcher.py

# --- New Helper Function for Secure BigQuery Connection ---
# data_fetcher.py
# Make sure these imports are at the top of your file
import os
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
# ... other imports

# --- New, More Robust Helper Function ---
# def _get_bigquery_client():
#     """
#     Creates a BigQuery client, with enhanced debugging to find startup errors.
#     """
#     print("--- [DEBUG] Attempting to get BigQuery client. ---")

#     # This check is for local development
#     if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
#         print("--- [DEBUG] Found local environment variable. Using default credentials. ---")
#         return bigquery.Client()

#     # This check is for deployment on Streamlit Cloud
#     elif "gcp_service_account" in st.secrets:
#         print("--- [DEBUG] Found 'gcp_service_account' in secrets. Processing... ---")
#         try:
#             creds_info = st.secrets["gcp_service_account"]
#             print("--- [DEBUG] Successfully read secrets dictionary from st.secrets. ---")

#             credentials = service_account.Credentials.from_service_account_info(creds_info)
#             print("--- [DEBUG] Successfully created credentials object from secrets info. ---")

#             client = bigquery.Client(credentials=credentials, project=credentials.project_id)
#             print("--- [DEBUG] Successfully created BigQuery client for cloud environment. ---")
#             return client
#         except Exception as e:
#             # This will force the full error traceback to be printed to the logs
#             print(f"!!! [DEBUG] AN ERROR OCCURRED while processing cloud secrets: {e}")
#             traceback.print_exc()
#             raise e

#     # This runs if no credentials are found at all
#     else:
#         print("!!! [DEBUG] No credentials found in environment variables or Streamlit secrets.")
#         raise Exception("Google Cloud credentials not found.")

def _get_bigquery_client():
    """
    Creates and returns a BigQuery client.
    - On Google Cloud, it automatically uses the environment's service account permissions.
    - Locally, it automatically uses the GOOGLE_APPLICATION_CREDENTIALS from your .env file.
    """
    return bigquery.Client()

def get_user_sensor_data(user_id, workout_id):
    """
    Returns a list of timestamped sensor data from your BigQuery project.
    """
    client = _get_bigquery_client() # <-- Change: Use the helper function
    project_id = client.project # <-- Change: Get project ID dynamically
    dataset = "ISE"

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
    return [dict(row) for row in query_job.result()]


def generate_password_reset_token(email):
    """
    Finds a user by email, generates a secure password reset token,
    saves its hash to the database, and returns the original token.
    """
    client = _get_bigquery_client()
    project_id = client.project

    # Find the user by email
    user_query = f"SELECT UserId FROM `{project_id}.ISE.Users` WHERE Email = @email"
    query_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("email", "STRING", email)]
    )
    results = list(client.query(user_query, job_config=query_config).result())

    if not results:
        return None

    user_id = results[0]["UserId"]
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    # --- FIX IS HERE ---
    # Use the full, specific path to the .now() method
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    # --- END FIX ---

    insert_query = f"""
        INSERT INTO `{project_id}.ISE.PasswordResetTokens` (TokenHash, UserId, ExpiresAt)
        VALUES (@token_hash, @user_id, @expires_at)
    """
    insert_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("token_hash", "STRING", token_hash),
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
            bigquery.ScalarQueryParameter("expires_at", "TIMESTAMP", expires_at),
        ]
    )
    client.query(insert_query, job_config=insert_config)

    return token

def get_user_workouts(user_id):
    """Returns a list of user's workouts from your database."""
    client = _get_bigquery_client() # <-- Change: Use the helper function
    project_id = client.project # <-- Change: Get project ID dynamically
    
    try:
        query = f"""
            SELECT *
            FROM `{project_id}.ISE.Workouts`
            WHERE UserId = @user_id
            ORDER BY StartTimestamp DESC
        """
        query_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)
            ]
        )
        query_job = client.query(query, job_config=query_config)
        workouts = [dict(row) for row in query_job.result()]
        
        # This fallback is useful if your new database is empty
        if workouts:
            return workouts
        else:
            return [] # Return empty list if no workouts, can be handled in UI
            
    except Exception as e:
        print(f"Error fetching workouts from database: {e}")
        return []
    

# data_fetcher.py

def update_password_with_token(token, new_password):
    """
    Verifies a password reset token and updates the user's password if the token is valid.
    """
    client = _get_bigquery_client()
    project_id = client.project
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    query = f"""
        SELECT UserId, ExpiresAt
        FROM `{project_id}.ISE.PasswordResetTokens`
        WHERE TokenHash = @token_hash
    """
    query_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("token_hash", "STRING", token_hash)]
    )
    results = list(client.query(query, job_config=query_config).result())

    if not results:
        return "This password reset link is invalid. Please request a new one."

    token_data = results[0]

    # --- FIX IS HERE ---
    # Use the full, specific path to the .now() method
    if token_data["ExpiresAt"].replace(tzinfo=datetime.timezone.utc) < datetime.datetime.now(datetime.timezone.utc):
        return "This password reset link has expired. Please request a new one."
    # --- END FIX ---

    user_id = token_data["UserId"]
    new_password_hash = hash_password(new_password)

    update_query = f"""
        UPDATE `{project_id}.ISE.Users`
        SET password_hash = @new_password_hash
        WHERE UserId = @user_id
    """
    update_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("new_password_hash", "STRING", new_password_hash),
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
        ]
    )
    client.query(update_query, job_config=update_config).result()

    delete_query = f"""
        DELETE FROM `{project_id}.ISE.PasswordResetTokens`
        WHERE TokenHash = @token_hash
    """
    delete_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("token_hash", "STRING", token_hash)]
    )
    client.query(delete_query, job_config=delete_config).result()

    return "Your password has been reset successfully! You can now log in."

def get_user_profile(user_id):
    """Returns information about the given user from your database."""
    client = _get_bigquery_client() # <-- Change: Use the helper function
    project_id = client.project # <-- Change: Get project ID dynamically

    query = f"""
        SELECT
            u.name AS full_name,  
            u.username,
            u.DateOfBirth,
            u.ImageUrl AS profile_image,
            ARRAY_AGG(f.UserId2 IGNORE NULLS) AS friends
        FROM `{project_id}.ISE.Users` AS u
        LEFT JOIN `{project_id}.ISE.Friends` AS f
            ON u.UserId = f.UserId1
        WHERE u.UserId = @user_id
        GROUP BY u.name, u.username, u.DateOfBirth, u.ImageUrl
    """
    query_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)]
    )
    query_job = client.query(query, job_config=query_config)
    results = list(query_job.result())
    return dict(results[0]) if results else {}


def get_user_posts(user_id):
    """Returns a list of a user's posts from your database."""
    client = _get_bigquery_client() # <-- Change: Use the helper function
    project_id = client.project # <-- Change: Get project ID dynamically

    query = f"""
        SELECT *, AuthorId as user_id_alias
        FROM `{project_id}.ISE.Posts`
        WHERE AuthorId = @user_id
        ORDER BY timestamp DESC
    """
    query_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)]
    )
    query_job = client.query(query, job_config=query_config)
    posts = [dict(row) for row in query_job.result()]
    for post in posts:
        post['user_id'] = post.pop('user_id_alias', None)
    return posts

def get_friends_posts(user_id):
    """Returns a list of posts from the user's friends from your database."""
    client = _get_bigquery_client() # <-- Change: Use the helper function
    project_id = client.project # <-- Change: Get project ID dynamically
    
    query = f"""
        SELECT
            p.PostId AS PostId, p.AuthorId AS AuthorId, p.Timestamp AS Timestamp,
            p.ImageUrl AS ImageUrl, p.Content AS Content, u.Name AS Username
        FROM `{project_id}.ISE.Posts` AS p
        JOIN `{project_id}.ISE.Users` AS u ON p.AuthorId = u.UserId
        JOIN (
            SELECT UserId2 AS FriendId FROM `{project_id}.ISE.Friends` WHERE UserId1 = @user_id
            UNION DISTINCT
            SELECT UserId1 AS FriendId FROM `{project_id}.ISE.Friends` WHERE UserId2 = @user_id
        ) AS friends ON p.AuthorId = friends.FriendId
        ORDER BY p.Timestamp DESC
    """
    query_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter('user_id', 'STRING', user_id)]
    )
    query_job = client.query(query, job_config=query_config)
    return [dict(row) for row in query_job.result()]


def get_user_daily_workout_data(user_id) -> dict:
    """Retrieves daily workout data from your database."""
    client = _get_bigquery_client() # <-- Change: Use the helper function
    project_id = client.project # <-- Change: Get project ID dynamically
    
    query = f"""
        SELECT StartTimestamp, EndTimestamp, TotalDistance, TotalSteps, CaloriesBurned
        FROM `{project_id}.ISE.Workouts`
        WHERE UserId = @user_id AND DATE(EndTimestamp) = CURRENT_DATE()
        ORDER BY EndTimestamp DESC
    """
    query_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
    )
    results = list(client.query(query, job_config=query_config).result())
    
    if not results:
        return {"distance": 0.0, "steps": 0, "calories": 0, "advice_timestamp": "1970-01-01 00:00:00"}
    
    total_distance, total_steps, total_calories = 0.0, 0, 0
    most_recent_end = None
    for row in results:
        total_distance += row["TotalDistance"] or 0
        total_steps += row["TotalSteps"] or 0
        total_calories += row["CaloriesBurned"] or 0
        if most_recent_end is None or row["EndTimestamp"] > most_recent_end:
            most_recent_end = row["EndTimestamp"]
            
    advice_timestamp = most_recent_end.strftime("%Y-%m-%d %H:%M:%S") if most_recent_end else "1970-01-01 00:00:00"
    
    return {
        "distance": total_distance, "steps": total_steps,
        "calories": total_calories, "advice_timestamp": advice_timestamp
    }

def get_genai_advice(user_id):
    """Returns motivational advice from Vertex AI."""
    user_data = get_user_profile(user_id)
    username = user_data.get("username", "User")
    daily_data = get_user_daily_workout_data(user_id)
    
    prompt = (
        f"Provide a list of 4 concise motivational advices for {username}. "
        f"Today, they have covered {daily_data['distance']:.1f} km, taken {daily_data['steps']} steps, "
        f"and burned {daily_data['calories']} calories. Each advice should be a single sentence."
    )
    fallback = f"Keep pushing forward, {username}—every step counts!"
    
    try:
        client = _get_bigquery_client() # <-- Change: Get client to find project ID
        vertexai.init(project=client.project, location="us-central1") # <-- Change: Removed hardcoded project
        
        model = GenerativeModel("gemini-1.5-flash-001")
        generation_config = GenerationConfig(
            response_mime_type="application/json",
            response_schema={"type": "array", "items": {"type": "string"}},
            temperature=0.7
        )
        response = model.generate_content(prompt, generation_config=generation_config)
        advices = json.loads(response.candidates[0].content.text)
        chosen_advice = random.choice(advices) if advices else fallback
    except Exception as e:
        print(f"GenAI Error: {e}")
        chosen_advice = fallback

    return {
        "advice_id": str(uuid.uuid4()),
        "timestamp": daily_data["advice_timestamp"],
        "content": chosen_advice,
        "image": random.choice([
            "https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3",
            None
        ]),
    }

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    client = _get_bigquery_client() # <-- Change: Use the helper function
    project_id = client.project # <-- Change: Get project ID dynamically
    query = f"""
        SELECT UserId, Username FROM `{project_id}.ISE.Users`
        WHERE Username = @username AND password_hash = @password_hash
    """
    query_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username),
            bigquery.ScalarQueryParameter("password_hash", "STRING", hash_password(password))
        ]
    )
    results = list(client.query(query, job_config=query_config).result())
    return dict(results[0]) if results else None

# data_fetcher.py

def register_user(username, full_name, password, email):
    client = _get_bigquery_client()
    project_id = client.project
    
    check_query = f"SELECT Username FROM `{project_id}.ISE.Users` WHERE Username = @username"
    config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("username", "STRING", username)]
    )
    if list(client.query(check_query, job_config=config).result()):
        return "That username is already in use."

    user_id = str(uuid.uuid4())
    password_hash = hash_password(password)

    insert_query = f"""
        INSERT INTO `{project_id}.ISE.Users` (UserId, Name, Username, Email, password_hash)
        VALUES (@user_id, @name, @username, @email, @password_hash)
    """
    insert_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
            bigquery.ScalarQueryParameter("name", "STRING", full_name),
            bigquery.ScalarQueryParameter("username", "STRING", username),
            bigquery.ScalarQueryParameter("email", "STRING", email),
            bigquery.ScalarQueryParameter("password_hash", "STRING", password_hash),
        ]
    )
    client.query(insert_query, job_config=insert_config)
    return "¡Successfully registered!"
# --- All Challenge functions refactored ---

def get_latest_two_challenges():
    client = _get_bigquery_client() # <-- Change: Use the helper function
    project_id = client.project # <-- Change: Get project ID dynamically
    query = f"SELECT StartDate, EndDate FROM `{project_id}.ISE.Challenges` ORDER BY EndDate DESC LIMIT 2"
    rows = list(client.query(query).result())
    if len(rows) < 2: return None
    return (rows[0].StartDate, rows[0].EndDate), (rows[1].StartDate, rows[1].EndDate)

# data_fetcher.py

def get_week_challenges(start_date, end_date):
    """
    Returns data for weekly challenges. If a challenge has no real participants,
    it returns a default leaderboard of fake users.
    """
    client = _get_bigquery_client()
    project_id = client.project
    
    if not isinstance(start_date, str): start_date = start_date.strftime("%Y-%m-%d")
    if not isinstance(end_date, str): end_date = end_date.strftime("%Y-%m-%d")
    
    challenge_query = f"""
        SELECT ChallengeId, Type FROM `{project_id}.ISE.Challenges`
        WHERE StartDate <= @end_date AND EndDate >= @start_date ORDER BY Type
    """
    challenge_params = [
        bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
        bigquery.ScalarQueryParameter("end_date", "DATE", end_date)
    ]
    challenge_job_config = bigquery.QueryJobConfig(query_parameters=challenge_params)
    challenges = [dict(row) for row in client.query(challenge_query, job_config=challenge_job_config).result()]
    
    if not challenges: return [[start_date, end_date], [[], [], []]]
    
    challenge_data = [[], [], []]
    for challenge in challenges:
        metrics_query = f"""
            SELECT cm.UserId, u.Username, u.ImageUrl AS profile_image, cm.Value
            FROM `{project_id}.ISE.ChallengeMetrics` cm
            JOIN `{project_id}.ISE.Users` u ON cm.UserId = u.UserId
            WHERE cm.ChallengeId = @challenge_id ORDER BY cm.Value DESC LIMIT 10
        """
        metrics_params = [bigquery.ScalarQueryParameter("challenge_id", "STRING", challenge["ChallengeId"])]
        metrics_job_config = bigquery.QueryJobConfig(query_parameters=metrics_params)
        metrics_results = client.query(metrics_query, job_config=metrics_job_config).result()
        
        participants = [{"user_id": r["UserId"], "username": r["Username"], "profile_image": r["profile_image"], "value": r["Value"]} for r in metrics_results]
        
        # --- FIX STARTS HERE ---
        # If no real participants are found, create a default leaderboard.
        if not participants:
            default_users = [
                {'user_id': 'bot1', 'username': 'AlexTheWinner', 'profile_image': None},
                {'user_id': 'bot2', 'username': 'BrendaRuns', 'profile_image': None},
                {'user_id': 'bot3', 'username': 'CharlieSteps', 'profile_image': None}
            ]
            # Assign different default scores based on the challenge type
            if challenge["Type"].lower() == "distance":
                default_users[0]['value'] = 42.2
                default_users[1]['value'] = 35.5
                default_users[2]['value'] = 28.1
            elif challenge["Type"].lower() == "steps":
                default_users[0]['value'] = 65400
                default_users[1]['value'] = 51200
                default_users[2]['value'] = 48900
            elif challenge["Type"].lower() == "workouts":
                default_users[0]['value'] = 6
                default_users[1]['value'] = 5
                default_users[2]['value'] = 3
            
            participants = default_users
        # --- FIX ENDS HERE ---

        if challenge["Type"].lower() == "distance": challenge_data[0] = participants
        elif challenge["Type"].lower() == "steps": challenge_data[1] = participants
        elif challenge["Type"].lower() == "workouts": challenge_data[2] = participants
            
    return [[start_date, end_date], challenge_data]

def get_current_week_challenges():
    latest_challenges = get_latest_two_challenges()
    if not latest_challenges: return [[], [[],[],[]]]
    (this_start, this_end), _ = latest_challenges
    return get_week_challenges(this_start, this_end)

def get_last_week_challenges():
    latest_challenges = get_latest_two_challenges()
    if not latest_challenges: return [[], [[],[],[]]]
    _, (last_start, last_end) = latest_challenges
    return get_week_challenges(last_start, last_end)

def get_challenge_id(start_date, end_date, challenge_type):
    client = _get_bigquery_client() # <-- Change: Use the helper function
    project_id = client.project # <-- Change: Get project ID dynamically
    
    if not isinstance(start_date, str): start_date = start_date.strftime("%Y-%m-%d")
    if not isinstance(end_date, str): end_date = end_date.strftime("%Y-%m-%d")
    
    query = f"""
        SELECT ChallengeId FROM `{project_id}.ISE.Challenges`
        WHERE StartDate = @start_date AND EndDate = @end_date AND LOWER(Type) = LOWER(@challenge_type)
    """
    params = [
        bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
        bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        bigquery.ScalarQueryParameter("challenge_type", "STRING", challenge_type)
    ]
    job_config = bigquery.QueryJobConfig(query_parameters=params)
    results_list = list(client.query(query, job_config=job_config).result())
    return results_list[0]["ChallengeId"] if results_list else None

def get_joined_challenge(challenge_id, user_id):
    client = _get_bigquery_client() # <-- Change: Use the helper function
    project_id = client.project # <-- Change: Get project ID dynamically
    
    query = f"""
        SELECT COUNT(*) as count FROM `{project_id}.ISE.ChallengeParticipants`
        WHERE ChallengeId = @challenge_id AND UserId = @user_id
    """
    params = [
        bigquery.ScalarQueryParameter("challenge_id", "STRING", challenge_id),
        bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
    ]
    job_config = bigquery.QueryJobConfig(query_parameters=params)
    results_list = list(client.query(query, job_config=job_config).result())
    return results_list[0]["count"] > 0 if results_list else False

def join_challenge(challenge_id, user_id):
    if get_joined_challenge(challenge_id, user_id): return False
    
    client = _get_bigquery_client() # <-- Change: Use the helper function
    project_id = client.project # <-- Change: Get project ID dynamically
    
    query = f"""
        INSERT INTO `{project_id}.ISE.ChallengeParticipants` (ChallengeId, UserId)
        VALUES (@challenge_id, @user_id)
    """
    params = [
        bigquery.ScalarQueryParameter("challenge_id", "STRING", challenge_id),
        bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
    ]
    job_config = bigquery.QueryJobConfig(query_parameters=params)
    
    try:
        client.query(query, job_config=job_config).result()
        return True
    except Exception as e:
        print(f"Error joining challenge: {e}")
        return False

def get_challenge_participant_counts():
    client = _get_bigquery_client() # <-- Change: Use the helper function
    project_id = client.project # <-- Change: Get project ID dynamically
    
    query = f"""
        SELECT c.Type, COUNT(DISTINCT cp.UserId) as participant_count
        FROM `{project_id}.ISE.Challenges` c
        LEFT JOIN `{project_id}.ISE.ChallengeParticipants` cp ON c.ChallengeId = cp.ChallengeId
        WHERE CURRENT_DATE() BETWEEN c.StartDate AND c.EndDate
        GROUP BY c.Type
    """
    results = client.query(query).result()
    counts = {"distance": 0, "steps": 0, "workouts": 0}
    for row in results:
        challenge_type = row["Type"].lower()
        if challenge_type in counts:
            counts[challenge_type] = row["participant_count"]
    return counts