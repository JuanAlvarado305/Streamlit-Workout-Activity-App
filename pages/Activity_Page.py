import streamlit as st
from data_fetcher import get_user_workouts, get_user_profile, get_user_posts
from modules import insert_post, display_recent_workouts, display_activity_summary

userId = 'user1'
st.set_page_config(page_title="Activity Summary", layout="wide")

def activity_page():
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
        #st.title("Main Menu")
        
        # User profile section in sidebar
        user_info = get_user_profile(userId)
        st.subheader(f"Welcome, {user_info['Name']}!")
        st.markdown("---")
        
        # Navigation options
        st.subheader("Sections")
        st.markdown("• [Activity Summary](#activity-summary)")
        st.markdown("• [Recent Workouts](#recent-workouts)")
        # st.markdown("• [User Posts](#user-posts)")
        # st.markdown("• [Motivational Quote](#motivational-quote)")
        
        # Add the activity page link
        # st.markdown("---")
        # st.markdown("[Go to Activity Page](activity_page)")
        
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

    # Fetch user data if not already fetched in sidebar
    if 'user_workouts' not in locals():
        user_workouts = get_user_workouts(userId)
    user_posts = get_user_posts(userId)

    st.title("Activity Summary")

    # Add space before the component to ensure it's visible
    st.write("###")  # This adds extra vertical space
    
    # Display the activity summary
    display_activity_summary(user_workouts)
    #st.markdown("---")

    # Add space after the component to prevent cutoff
    #st.write("###")  # This adds extra vertical space
    
    # --- Recent Workouts ---
    st.header("Recent Workouts")
    user_id = "user1"  # Replace with actual user ID
    workouts = get_user_workouts(user_id)
    if workouts:
        display_recent_workouts(workouts)
    else:
        st.write("No recent workouts found.")

    st.write("###")  # This adds extra vertical space
    
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

if __name__ == "__main__":
    activity_page()
