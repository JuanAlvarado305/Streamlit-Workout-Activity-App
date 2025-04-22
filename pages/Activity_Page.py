import streamlit as st
from data_fetcher import get_user_workouts, get_user_profile, get_user_posts, get_user_sensor_data
from modules import  display_recent_workouts, display_activity_summary, create_workout_content, display_post_preview, check_duplicate_post, insert_post, display_user_sensor_data



# st.set_page_config(page_title="Activity Summary", layout="wide")

def activity_page():
    # Add custom CSS focusing on making the activity summary taller

    userId = st.session_state.user_id
    user_workouts = get_user_workouts(userId)

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
        st.subheader(f"Welcome, {user_info['full_name']}!")
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
        st.metric("Total Workouts", len(user_workouts))
        st.metric("This Week", sum(1 for w in user_workouts if w.get('is_current_week', False)))
        
        #Team Members 
        st.markdown("---")
        st.subheader("Spaghetti Crew Team")
        st.markdown("Juan")
        st.markdown("Jona")
        st.markdown("Foluso")
        st.markdown("Loie")


    st.title("Activity Summary")

    # Add space before the component to ensure it's visible
    st.write("###")  # This adds extra vertical space
    
    # Display the activity summary
    display_activity_summary(user_workouts)
    #st.markdown("---")

    # Fetch sensor data for the given workout and display it.
    sensor_data = get_user_sensor_data(userId, "workout2")
    display_user_sensor_data(sensor_data)
    
    # --- Recent Workouts ---
    st.header("Recent Workouts")
    
    user_workouts = get_user_workouts(userId)
    if user_workouts:
        display_recent_workouts(user_workouts)
    else:
        st.write("No recent workouts found.")

    st.write("###")  # This adds extra vertical space
    
   # --- Share Your Activity Section ---
    st.header("Share Your Activity")
    st.write("Preview your activity to share:")

    # Get workout content from external function if workouts exist
    if user_workouts:  # Assuming workouts is defined earlier
        default_content = create_workout_content(user_workouts[0])  # External function
    else:
        default_content = "Just completed a workout! Feeling great!"

    # Allow user to edit content
    content = st.text_area("Post Preview", default_content, height=100)

    # Image URL selection
    use_custom_image = st.checkbox("Use custom image URL")

    default_image_url = "https://cdn.pixabay.com/photo/2021/09/12/17/43/jogging-6619078_1280.jpg"

    if use_custom_image:
        image_url = st.text_input("Enter image URL", default_image_url)
    else:
        image_url = default_image_url

    # Show image preview
    if image_url:
        st.image(image_url, caption="Image Preview", width=300)

    # Show post preview using external function
    display_post_preview(content, image_url)  # External function

    # Confirm and post button
    if st.button("Confirm and Post"):
        if content.strip():  # Make sure content is not empty
            # Check for duplicates using external function
            is_duplicate = check_duplicate_post(userId, content)
            if is_duplicate:
                st.warning("You've already shared similar content recently.")
            
            success, message = insert_post(userId, content, image_url)
            
            if success:
                st.success(message)
            else:
                st.error(message)
        else:
            st.error("Post content cannot be empty.")

if __name__ == "__main__":
    activity_page()
