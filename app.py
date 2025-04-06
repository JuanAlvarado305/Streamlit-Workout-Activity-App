#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts, get_users

userId = 'user1'

st.set_page_config(page_title="Home")

def display_home_page():
    """Displays the home page of the app containing recent user friends posts and genai advice."""

    users = get_users() 
    user_community = users[userId]['friends']
    all_community_posts = []
    #all_community_posts = generate_fake_posts()

    st.title('Welcome to the Spaghetti Crew Workout App!')

    # First 10 posts from a user’s friends ordered by timestamp
    st.header('Your Community') 
    for user in user_community:
        all_community_posts.extend(get_user_posts(user))

    all_community_posts.sort(reverse=True, key=lambda post: post['timestamp']) #sort list of posts by timestamp

    # display 10 posts from user's friends
    for post in all_community_posts[:10]:
        display_post(post)
        st.markdown("---")  # Adds a separator between posts
    st.markdown('You have viewed all recent community posts.')
    st.markdown("---")

    # One piece of GenAI advice and encouragement
    motivate(userId)

def display_app_page():
    """Displays the home page of the app."""

    st.title('Welcome to the Spaghetti Crew Workout App!')

    # Fetch user data
    user_info = get_user_profile(userId)
    user_posts = get_user_posts(userId)
    user_workouts = get_user_workouts(userId)
    
    # Display activity summary section
    st.header(f"Activity Summary for {user_info['full_name']}")
    
    # Add space before the component to ensure it's visible
    st.write("###")  # This adds extra vertical space
    
    # Display the activity summary
    display_activity_summary(user_workouts)
    
    # Add space after the component to prevent cutoff
    st.write("###")  # This adds extra vertical space
    
    # Display recent workouts section
    display_recent_workouts(user_workouts)
    
    st.markdown("---")  # Add separator between sections
    
    # Display user posts section
    st.header("User Posts")
    
    # Loop through posts and display them
    for post in user_posts:
        display_post(post)
        st.markdown("---")  # Adds a separator between posts
        
    # Display a custom component example.
    value = st.text_input('Enter your name')
    display_my_custom_component(value)

    # Display GenAI advice as part of the page.
    motivate(userId)
 
 
def motivate(userId):
    """
    Retrieves and displays motivational advice for a given user.
 
    This function fetches motivational advice using the `get_genai_advice` function,
    extracts the timestamp, content, and image from the result, and then displays the
    advice with the `display_genai_advice` function.
 
    Parameters:
        userId (int or str): The identifier for the user for whom the motivational advice is retrieved.
    """
    result = get_genai_advice(userId)
    timestamp = result['timestamp']
    content = result['content']
    image = result['image']
    display_genai_advice(timestamp, content, image)

def generate_fake_posts(): # written by AI
    import datetime
    import random

    posts = []
    user_ids = ['user1', 'user2', 'user3', 'user4']
    image_url = 'https://fastly.picsum.photos/id/74/4288/2848.jpg?hmac=q02MzzHG23nkhJYRXR-_RgKTr6fpfwRgcXgE0EKvNB8'

    # Generate timestamps across a few days
    start_date = datetime.datetime(2025, 4, 1, 10, 0, 0)
    time_deltas = [datetime.timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59)) for _ in range(12)]
    timestamps = sorted([start_date + delta for delta in time_deltas])

    content_options = [
        "Enjoying a sunny afternoon in Atlanta!",
        "Just finished a great workout. Feeling energized!",
        "Trying out a new coffee shop downtown.",
        "Exploring Piedmont Park today. Beautiful!",
        "Making some delicious homemade pizza tonight.",
        "Coding away on my latest project.",
        "Thinking about my next travel adventure.",
        "Caught a beautiful sunset over the city.",
        "Spending time with friends this weekend.",
        "Reading a fascinating book.",
        "Listening to some great music.",
        "Another day, another opportunity."
    ]

    for i in range(12):
        user_id = random.choice(user_ids)
        content = random.choice(content_options)
        posts.append({
            'user_id': user_id,
            'post_id': f'post{i+1}',
            'timestamp': timestamps[i].strftime('%Y-%m-%d %H:%M:%S'),
            'content': content,
            'image': image_url,
        })
    return posts

# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_home_page()
    #display_app_page()