#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts

userId = 'user1'


def display_app_page():
    """Displays the home page of the app."""
    st.title('Welcome to the Spaghetti Crew Workout App!')

    # Fetch user data
    user_info = get_user_profile(userId)
    user_posts = get_user_posts(userId)
    user_workouts = get_user_workouts(userId)
    
    # Display activity summary section
    st.header(f"Activity Summary for {user_info['full_name']}")
    display_activity_summary(user_workouts)
    
    st.markdown("---")  # Add separator between sections
    
    # Display user posts section
    st.header("User Posts")
    


    ## The code below has no relation to my display_acitivtiy_summary and 
    #  is used to display user posts 
    # Loop through posts and display them
    for post in user_posts:
        display_post(
            username = user_info["username"],
            user_image = user_info["profile_image"],
            timestamp = post["timestamp"],
            content = post["content"],
            post_image = "https://fastly.picsum.photos/id/74/4288/2848.jpg?hmac=q02MzzHG23nkhJYRXR-_RgKTr6fpfwRgcXgE0EKvNB8",
        )
        st.markdown("---")  # Adds a separator between posts


# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()
