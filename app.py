#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
import datetime
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts, get_friends_posts
#from activity_page import activity_page

# Set page configuration - add this at the very beginning, before any other st commands
st.set_page_config(page_title="Home")
userId = 'user1'

def display_home_page():
    """Displays the Community Feed page containing friends' posts and GenAI advice."""

    # --- Sidebar Setup ---
    with st.sidebar:
        # User profile section
        user_info = get_user_profile(userId)
        # Use the fetched name, provide fallback if not found
        user_name = user_info.get('Name', 'User') if user_info else 'User'
        st.header(f"Welcome, {user_name}!")
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

        # Team Members Section
        st.subheader("Spaghetti Crew Team")
        st.markdown("Juan")
        st.markdown("Jona")
        st.markdown("Foluso")
        st.markdown("Loie")
        st.markdown("---")
        # Optionally add navigation links if needed later
        # st.page_link("activity_page.py", label="My Activity") # Example using st.page_link

    # --- Main Page Content ---
    st.title('Community Feed')

    # Display first 10 posts from the user's friends ordered by timestamp
    st.header("What your friends are up to...")

    try:
        friends_posts = get_friends_posts(userId)

        if not friends_posts:
            st.info("No posts from your friends to show right now. Connect with more friends or encourage them to post!")
        else:
            # Display up to 10 posts
            for post in friends_posts[:10]:
                 # Pass the Author's Name if available, otherwise use AuthorId
                 author_display_name = post.get('AuthorName', post.get('AuthorId', 'Unknown User'))
                 # Modify display_post call if it needs the Author's Name explicitly
                 # Assuming display_post can handle the dictionary structure from get_friends_posts
                 # You might need to adjust display_post or how you pass data to it
                 display_post(post, author_name=author_display_name) # Pass author_name if display_post uses it
                 st.markdown("---")  # Adds a separator between posts

            if len(friends_posts) > 10:
                 st.markdown("Showing the 10 most recent posts.")
            else:
                 st.markdown("You've seen all recent posts from your friends.")

    except Exception as e:
        st.error(f"Could not load community posts: {e}")
        # Display placeholder posts as a fallback during development/error
        st.subheader("Sample Posts (Error loading actual data):")
        for num in range(3): # Display a few placeholders on error
            display_post({'PostId': f'error_post{num}', 'AuthorId': 'user_error', 'AuthorName': 'System Error', 'Timestamp': datetime.datetime.now(), 'ImageUrl': 'https://fastly.picsum.photos/id/74/4288/2848.jpg?hmac=q02MzzHG23nkhJYRXR-_RgKTr6fpfwRgcXgE0EKvNB8', 'Content': 'Error loading post. This is placeholder content.'})
            st.markdown('---')


    st.markdown("---") # Separator before GenAI advice

    # Display one piece of GenAI advice and encouragement
    st.header("Today's Motivation")
    motivate(userId) # Calls the existing motivate function

# def display_home_page():
#     """Displays the home page of the app containing recent user friends posts and genai advice."""

#     with st.sidebar:        
#         # User profile section in sidebar
#         user_info = get_user_profile(userId)
#         st.header(f"Welcome, {user_info['Name']}!")
#         #st.markdown("---")
        
#         # Navigation options
#         # st.subheader("Sections")
#         # st.markdown("• [Activity Summary](#activity-summary)")
#         # st.markdown("• [Recent Workouts](#recent-workouts)")
#         # st.markdown("• [User Posts](#user-posts)")
#         # st.markdown("• [Motivational Quote](#motivational-quote)")
        
#         # Add the activity page link
#         # st.markdown("---")
#         # st.markdown("[Go to Activity Page](activity_page)")
        
#         # Maybe add quick stats in sidebar
#         st.markdown("---")
#         st.subheader("Quick Stats")
#         user_workouts = get_user_workouts(userId)
#         st.metric("Total Workouts", len(user_workouts))
#         st.metric("This Week", sum(1 for w in user_workouts if w.get('is_current_week', False)))
        
#         #Team Members 
#         st.markdown("---")
#         st.subheader("Spaghetti Crew Team")
#         st.markdown("Juan")
#         st.markdown("Jona")
#         st.markdown("Foluso")
#         st.markdown("Loie")

#     st.title('Welcome to the Spaghetti Crew Workout App!')

#     # First 10 posts from a user’s friends ordered by timestamp
#     st.header('Your Community') 

#     for num in range(10): #placeholder posts to check display
#         display_post({'PostId': 'post1', 'AuthorId': 'user1', 'Timestamp': datetime.datetime(2024, 7, 29, 12, 0), 'ImageUrl': 'https://fastly.picsum.photos/id/74/4288/2848.jpg?hmac=q02MzzHG23nkhJYRXR-_RgKTr6fpfwRgcXgE0EKvNB8', 'Content': 'This is a placeholder!'})
#         st.markdown('---')

#     #gets the list of the user's friends
#     #get all friends posts

#     # for user in user_community:
#     #     all_community_posts.extend(get_user_posts(user))
#     #     #all_community_posts.append(get_user_posts(userId))
    
#     # #{'PostId': 'post1', 'AuthorId': 'user1', 'Timestamp': datetime.datetime(2024, 7, 29, 12, 0), 'ImageUrl': 'http://example.com/posts/post1.jpg', 'Content': None}

#     # #formatted_timestamp = post['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')
#     # #all_community_posts.sort(reverse=True, key=lambda post: post['Timestamp']) #sort list of posts by timestamp

#     # # display 10 posts from user's friends
#     # for post in all_community_posts[:10]:
#     #     if isinstance(post['Timestamp'], datetime.datetime):
#     #         post['Timestamp'] = post['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')
#     #     display_post(post)
#     #     st.markdown("---")  # Adds a separator between posts
    
#     st.markdown('You have viewed all recent community posts.')
#     st.markdown("---")

#     # One piece of GenAI advice and encouragement
#     motivate(userId)   

def display_app_page(): #not called in main
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
        
        # Add the activity page link
        st.markdown("---")
        st.markdown("[Go to Activity Page](activity_page)")
        
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
    display_home_page()
    #display_app_page()