#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
# Set page to wide mode - add this at the very beginning, before any other st commands
st.set_page_config(layout="wide")

from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts, display_user_sensor_data
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts
from activity_page import activity_page_content  # Import function instead of module

# Create a session state variable to track the current page
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Function to navigate to activity page
def nav_to_activity():
    st.session_state.page = 'activity'
    st.rerun()  # Use st.rerun() instead of experimental_rerun

# Function to navigate back to home
def nav_to_home():
    st.session_state.page = 'home'
    st.rerun()  # Use st.rerun() instead of experimental_rerun

userId = 'user1'
workoutId = 'workout1'  # Fixed variable name

def display_app_page():
    """Displays the home page of the app."""
    
    # Add custom CSS focusing on making the activity summary taller
    st.markdown(
        """
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
    """
    , unsafe_allow_html=True)
    
    # Create the sidebar
    with st.sidebar:
        st.title("Main Menu")
        
        # User profile section in sidebar
        user_info = get_user_profile(userId)
        st.subheader(f"Welcome, {user_info['Name']}!")
        st.markdown("---")
        
        # Navigation options
        st.subheader("Sections")
        st.markdown("• [Activity Summary](#activity-summary)")
        st.markdown("• [Recent Workouts](#recent-workouts)")
        st.markdown("• [User Posts](#user-posts)")
        st.markdown("• [Motivational Quote](#motivational-quote)")
        
        # Add the activity page button (replacing the markdown link)
        st.markdown("---")
        if st.button("Go to Activity Page"):
            nav_to_activity()
        
        # Maybe add quick stats in sidebar
        st.markdown("---")
        st.subheader("Quick Stats")
        user_workouts = get_user_workouts(userId)
        st.metric("Total Workouts", len(user_workouts))
        st.metric("This Week", sum(1 for w in user_workouts if w.get('is_current_week', False)))
        
        #Team Memebers 
        st.markdown("---")
        st.subheader("Spaghetti Crew Team")
        st.markdown("Juan")
        st.markdown("Jona")
        st.markdown("Foluso")
        st.markdown("Loie")

    # Main content area
    st.title('Welcome to the Spaghetti Crew Workout App!')

    # Fetch user data if not already fetched in sidebar
    if 'user_workouts' not in locals():
        user_workouts = get_user_workouts(userId)
    user_posts = get_user_posts(userId)
    

    # Display activity summary section with anchor
    st.markdown("<div id='activity-summary'></div>", unsafe_allow_html=True)
    st.header(f"Activity Summary")

    
    # Add space before the component to ensure it's visible
    st.write("###")  # This adds extra vertical space
    
    # Display the activity summary
    display_activity_summary(user_workouts)
    st.markdown("---")

    # Add space after the component to prevent cutoff
    st.write("###")  # This adds extra vertical space
    
    # Display recent workouts section with anchor
    st.markdown("<div id='recent-workouts'></div>", unsafe_allow_html=True)
    st.header("Recent Workouts")
    display_recent_workouts(user_workouts)
    
    st.markdown("---")  # Add separator between sections
    
    # Display user posts section with anchor
    st.markdown("<div id='user-posts'></div>", unsafe_allow_html=True)
    st.header("User Posts")
    
    # Loop through posts and display them
    for post in user_posts:
        display_post(post)
        st.markdown("---")  # Adds a separator between posts
        
    # Display a custom component example.
    value = st.text_input('Enter your name')
    display_my_custom_component(value)

    # Fetch sensor data for the given workout and display it.
    sensor_data = get_user_sensor_data(userId, workoutId)
    display_user_sensor_data(sensor_data)

    # Display GenAI advice as part of the page with anchor
    st.markdown("<div id='motivational-quote'></div>", unsafe_allow_html=True)
    st.header("Today's Motivation")
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
    # Check the current page and display appropriate content
    if st.session_state.page == 'home':
        display_app_page()
    elif st.session_state.page == 'activity':
        # Add a "Back to Home" button at the top of the page
        if st.button("Return to Home"):
            nav_to_home()
        # Display activity page content
        activity_page_content()