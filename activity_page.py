import streamlit as st
from data_fetcher import get_user_workouts
from modules import insert_post, display_recent_workouts

def activity_page_content():
    """Content for the activity page - does not include navigation"""
    st.title("Activity Summary")

    # --- Recent Workouts ---
    st.header("Recent Workouts")
    user_id = "user1"  # Replace with actual user ID
    workouts = get_user_workouts(user_id)
    if workouts:
        display_recent_workouts(workouts)
    else:
        st.write("No recent workouts found.")

    # --- Share Button ---
    st.header("Share Your Activity")
    statistic_to_share = st.selectbox("Select a statistic to share", ["Steps", "Distance", "Calories Burned"])

    if st.button("Share with Community"):
        # Here, you would fetch the actual statistic value and create the post.
        if statistic_to_share == "Steps":
            # steps = get_user_steps(user_id) # Replace user_id and get_user_steps
            steps = workouts[0]['steps'] if workouts else 0 # Get steps from the first workout
            post_content = f"Look at this, I walked {steps} steps today!"
            insert_post(user_id, post_content)
            st.success("Shared successfully!")
        elif statistic_to_share == "Distance":
            distance = workouts[0]['distance'] if workouts else 0
            post_content = f"I covered {distance} km today!"
            insert_post(user_id, post_content)
            st.success("Shared successfully!")
        elif statistic_to_share == "Calories Burned":
            calories = workouts[0]['calories_burned'] if workouts else 0
            post_content = f"I burned {calories} calories today!"
            insert_post(user_id, post_content)
            st.success("Shared successfully!")

# Only for standalone testing - won't be used when imported from app.py
def activity_page():
    """Wrapper function to handle standalone execution"""
    # Create session state if running directly
    if 'page' not in st.session_state:
        st.session_state.page = 'activity'
    
    # Add navigation button in the sidebar
    with st.sidebar:
        st.title("Navigation")
        if st.button("Back to Home"):
            # This won't work fully when run standalone, but included for completeness
            st.session_state.page = 'home'
            # Use st.rerun() instead of experimental_rerun
            st.rerun()
    
    # Display the content
    activity_page_content()

if __name__ == "__main__":
    # This part only runs when this script is executed directly (not imported)
    activity_page()