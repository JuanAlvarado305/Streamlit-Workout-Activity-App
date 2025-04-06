#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
# Set page to wide mode - add this at the very beginning, before any other st commands
st.set_page_config(layout="wide")

from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts
from activity_page import activity_page

userId = 'user1'

def display_app_page():
    """Displays the home page of the app."""
    
    # Add custom CSS focusing on making the activity summary taller
    st.markdown("""
    <style>
        .activity-summary-container {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            min-height: 600px !important; /* Significantly increased height */
            height: auto !important;
            overflow: visible !important;
        }
        
        /* Ensure content within doesn't get cut off */
        .activity-summary-container > div {
            min-height: 550px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title('Welcome to the Spaghetti Crew Workout App!')
    st.markdown("[Go to Activity Page](activity_page)")

    # Fetch user data
    user_info = get_user_profile(userId)
    user_posts = get_user_posts(userId)
    user_workouts = get_user_workouts(userId)
    
    # Display activity summary section
    st.header(f"Activity Summary for {user_info['full_name']}")
    
    # Add space before the component to ensure it's visible
    st.write("###")  # This adds extra vertical space
    
    # Display the activity summary
    
    """This code is having an issue with the my custom component feature, check it out
    and fix the issue """

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
    

    # Comment out this line of code becuase am already displaying custom component to
    # the screen
    # display_my_custom_component(value)

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

# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()