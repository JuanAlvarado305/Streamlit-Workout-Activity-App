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
    
    # Add space before the component to ensure it's visible
    st.write("###")  # This adds extra vertical space
    
    # Display the activity summary
    display_activity_summary(user_workouts)
    
    # Add space after the component to prevent cutoff
    st.write("###")  # This adds extra vertical space
    
    st.markdown("---")  # Add separator between sections
    
    # Display user posts section
    st.header("User Posts")
    
    
# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()