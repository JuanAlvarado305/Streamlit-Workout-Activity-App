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
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts, get_friends_posts
from pages.Activity_Page import activity_page # Import function instead of module
from pages.hidden.login import login_page  # Import the login page function
from pages.hidden.register import register_page

# Create a session state variable to track the current page
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Check if user is authenticated
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Track current page within login/register flow
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'

# Function to navigate to activity page
def nav_to_activity():
    st.session_state.page = 'activity'
    st.rerun()  # Use st.rerun() instead of experimental_rerun

# Function to navigate back to home
def nav_to_home():
    st.session_state.page = 'home'
    st.rerun()  # Use st.rerun() instead of experimental_rerun

# Function to log out user
def logout():
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.rerun()

def display_home_page():
    """Displays the Community Feed page containing friends' posts and GenAI advice."""
    userId = st.session_state.user_id  # Get user ID from session state
    
    # --- Sidebar Setup ---
    with st.sidebar:
        # User profile section
        user_info = get_user_profile(userId)
        # Use the fetched name, provide fallback if not found
        user_name = user_info.get('Name', 'User') if user_info else 'User'
        st.subheader(f"Welcome, {user_info['full_name']}!")
        st.markdown("---")

        # Quick Stats Section
        st.subheader("Quick Stats")
        try:
            user_workouts = get_user_workouts(userId)
            # Check if user_workouts is not None and is iterable
            if user_workouts:
                 st.metric("Total Workouts", len(user_workouts))
                 # Filter for workouts in the current week correctly
                 st.metric("This Week", sum(1 for w in user_workouts if w.get('is_current_week', False)))
            else:
                 st.metric("Total Workouts", 0)
                 st.metric("This Week", 0)
                 st.write("No workout data available.")
        except Exception as e:
            st.error(f"Could not load workout stats: {e}")
            st.metric("Total Workouts", "N/A")
            st.metric("This Week", "N/A")

        st.markdown("---")
        
        # Add logout button
        if st.button("Logout"):
            logout()

        # Team Members Section
        st.subheader("Spaghetti Crew Team")
        st.markdown("Juan")
        st.markdown("Jona")
        st.markdown("Foluso")
        st.markdown("Loie")
        st.markdown("---")

    # --- Main Page Content ---
    st.title('Welcome to the Spaghetti Crew Workout App!')

    # Display first 10 posts from the user's friends ordered by timestamp
    st.header("What your friends are up to...")
    try:
        friends_posts = get_friends_posts(userId) #list of a user's posts

        if not friends_posts:
            st.info("No posts from your friends to show right now. Connect with more friends or encourage them to post!")
        else:
            # Display up to 10 posts
            for post in friends_posts[:10]:
                 display_post(post)
                 st.markdown("---")  # Adds a separator between posts

            if len(friends_posts) > 10:
                st.markdown("Showing the 10 most recent posts.")
            else:
                st.markdown('You have viewed all recent community posts.')

    except Exception as e:
        pass

    st.markdown("---") # Separator before GenAI advice

    # Display GenAI advice as part of the page with anchor
    st.markdown("<div id='motivational-quote'></div>", unsafe_allow_html=True)
    st.header("Today's Motivation")
    motivate(userId)
    
def display_app_page(): 
    userId = st.session_state.user_id  # Get user ID from session state
    workoutId = 'workout2'  # Fixed variable name
    
    # Create the sidebar
    with st.sidebar:
        st.title("Main Menu")
        
        # User profile section in sidebar
        user_info = get_user_profile(userId)
        st.subheader(f"Welcome, {user_info['full_name']}!")
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
        
        # Add logout button
        if st.button("Logout"):
            logout()
        
        # Maybe add quick stats in sidebar
        st.markdown("---")
        st.subheader("Quick Stats")
        user_workouts = get_user_workouts(userId)
        st.metric("Total Workouts", len(user_workouts))
        st.metric("This Week", sum(1 for w in user_workouts if w.get('is_current_week', False)))
        
        #Team Members 
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
    # Check if user is authenticated
    if not st.session_state.authenticated:
        # Check if account was just created
        if 'account_created' in st.session_state and st.session_state.account_created:
            st.success("Account created successfully! Please log in with your new credentials.")
            # Clear the flag to avoid showing the message again
            st.session_state.account_created = False
        
        
        if st.session_state.current_page == 'login':
            login_page()
        elif st.session_state.current_page == 'register':
            register_page()
    else:
        # If authenticated, check the current page and display appropriate content
        if st.session_state.page == 'home':
            display_home_page()
            #display_app_page()
        elif st.session_state.page == 'activity':
            # Add a "Back to Home" button at the top of the page
            if st.button("Return to Home"):
                nav_to_home()
            # Display activity page content
            activity_page()