#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

import streamlit as st
from html import escape
from internals import create_component
from datetime import datetime


def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    data = {
        'NAME': value,
    }
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username, user_image, timestamp, content, post_image):
    """Displays a user post with an improved layout in Streamlit."""
    """This function was created with the help of ChatGPT and Gemini"""
 
    # Formated Timestamp
    dt_object = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    formatted_time = dt_object.strftime("%d %b %Y, %H:%M")  # 08 Mar 2024, 14:30
 
    # CSS
    st.markdown(
        """
        <style>
            .post-container {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 15px;
                background-color: white;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                width: 600px;
                margin: auto;
                font-family: sans-serif;
            }
            .profile-pic {
                width: 50px;
                height: 50px;
                border-radius: 50%; 
                object-fit: cover;
                margin-bottom: 10px;
            }
            .post-info {
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                gap: 7px;
            }
            .post-content {
                font-size: 14px;
                margin-top: -5px;
                line-height: 1.6;
            }
            .post-image {
                width: 100%;
                border-radius: 10px;
                margin-top: 10px;
            }
            .post-info strong {
                font-size: 16px;
                margin-bottom: 0px;
                padding-bottom: 0px;
                line-height: 1;
            }
            .post-info span {
                font-size: 12px;
                color: #666;
                line-height: 1;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
 
    # main container
    with st.container():
        # Header with name and profile picture
        col1, col2 = st.columns([1, 11])
 
        with col1:
            st.markdown(f'<img src="{user_image}" class="profile-pic">', unsafe_allow_html=True)
 
        with col2:
            st.markdown(
                f"""
                <div class="post-info">
                    <strong>{username}</strong>
                    <span>{formatted_time}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
 
        # Post Content
        st.markdown(f"<p class='post-content'>{content} #GoogleTech2025</p>", unsafe_allow_html=True)
 
        # Post Image (if exists)
        if post_image:
            st.image(post_image, use_container_width=True)


def display_activity_summary(workouts_list):
    """Displays a summary of user workout activities.
    
    This component creates a visual summary showing total number of workouts,
    total distance covered, total steps taken, total calories burned, and 
    a list of recent workouts with their details.
    
    Args:
        workouts_list: A list of dictionaries, where each dictionary contains
            workout information with the following keys:
            - 'start_timestamp': The start time of the workout.
            - 'end_timestamp': The end time of the workout.
            - 'distance': The distance covered in km.
            - 'steps': The number of steps taken.
            - 'calories_burned': The number of calories burned.
            - 'start_lat_lng': The starting coordinates (latitude, longitude).
            - 'end_lat_lng': The ending coordinates (latitude, longitude).
    
    Returns:
        None. Renders the activity summary component in the Streamlit app.
    """
    # Calculate summary statistics
    workout_count = len(workouts_list)
    total_distance = sum(workout.get('distance', 0) for workout in workouts_list)
    total_steps = sum(workout.get('steps', 0) for workout in workouts_list)
    total_calories = sum(workout.get('calories_burned', 0) for workout in workouts_list)
    
    # Format the activity rows HTML
    activity_rows = ""
    # Sort workouts by start timestamp (most recent first)
    sorted_workouts = sorted(workouts_list, 
                             key=lambda x: x.get('start_timestamp', ''), 
                             reverse=True)
    
    for workout in sorted_workouts:
        # Extract the date part of the timestamp (assuming format "YYYY-MM-DD HH:MM:SS")
        date = workout.get('start_timestamp', '').split(' ')[0] if workout.get('start_timestamp') else 'N/A'
        
        # Create a row for each workout
        row_html = f'''
        <div class="activity-row">
            <span>{date}</span>
            <span>{workout.get('distance', 0)} km</span>
            <span>{workout.get('steps', 0)}</span>
            <span>{workout.get('calories_burned', 0)}</span>
        </div>
        '''
        activity_rows += row_html
    
    # Prepare data for the component
    data = {
        'WORKOUT_COUNT': workout_count,
        'TOTAL_DISTANCE': round(total_distance, 1),
        'TOTAL_STEPS': total_steps,
        'TOTAL_CALORIES': total_calories,
        'ACTIVITY_ROWS': activity_rows
    }
    
    # Register and display the component with explicit height
    html_file_name = "my_custom_component"
    
    # The explicit height ensures the component isn't cut off
    # Adjust the height value based on how many workouts you're displaying
    # Add about 100px + (40px × number of workout rows)
    height = 350 + min(len(workouts_list) * 40, 400)  # Base height + row height with a reasonable max
    
    create_component(data, html_file_name, height=height)


def display_genai_advice(timestamp, content, image):
    """
    Creates and displays a motivational advice component using the provided data.
    This function constructs an HTML snippet with embedded CSS and renders it
    using Streamlit. It uses the given timestamp, content, and image URL.
    
    Parameters:
        timestamp (str or datetime): The time when the advice was generated.
        content (str): The motivational advice text to be displayed.
        image (str): The URL or file path of the image associated with the advice.
    """
    # Format the timestamp if it is a string in the format "YYYY-MM-DD HH:MM:SS"
    safe_timestamp_str = str(timestamp) if timestamp is not None else ""
    try:
        dt_object = datetime.strptime(safe_timestamp_str, "%Y-%m-%d %H:%M:%S")
        safe_timestamp_str = dt_object.strftime("%d %b %Y, %H:%M")
    except ValueError:
        pass

    # Escape content and the formatted timestamp to prevent HTML injection
    safe_content = escape(str(content))
    safe_timestamp = escape(safe_timestamp_str)

    html_code = f"""
    <style>
        .custom-component-container {{
            position: relative;
            width: 100%;
            max-width: 1800px;
            height: 230px;
            margin: 20px auto;
            overflow: hidden;
            border-radius: 35px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .image {{
            position: absolute;
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: brightness(50%);
        }}

        .content {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 50px;
            color: #fff;
            font-weight: 700;
            text-align: center;
            z-index: 2;
            margin: 0 20px;
            line-height: 1.2;
        }}

        .time {{
            position: absolute;
            bottom: 13px;
            right: 13px;
            font-size: 14px;
            color: #fff;
            font-style: italic;
            z-index: 2;
        }}
    </style>

    <div class="custom-component-container">
        <img class="image" src="{image}" alt="Motivation">
        <p class="content">{safe_content}</p>
        <p class="time">{safe_timestamp}</p>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


def display_recent_workouts(workouts_list):
    """Displays a list of recent workouts with detailed information.
    
    This function creates a visually appealing display of recent workouts 
    with detailed information about each workout including date, duration,
    distance, steps, and calories burned. The workouts are sorted by date
    with the most recent first.
    
    Args:
        workouts_list: A list of dictionaries, where each dictionary contains
            workout information with the following keys:
            - 'start_timestamp': The start time of the workout.
            - 'end_timestamp': The end time of the workout.
            - 'distance': The distance covered in km.
            - 'steps': The number of steps taken.
            - 'calories_burned': The number of calories burned.
            - 'start_lat_lng': The starting coordinates (latitude, longitude).
            - 'end_lat_lng': The ending coordinates (latitude, longitude).
    
    Returns:
        None. Renders the recent workouts component in the Streamlit app.
    """
    import streamlit as st
    from datetime import datetime
    
    # If no workouts, display message
    if not workouts_list:
        st.write("No recent workouts found.")
        return
    
    # Sort workouts by start timestamp (most recent first)
    sorted_workouts = sorted(workouts_list, 
                         key=lambda x: x.get('start_timestamp', ''), 
                         reverse=True)
    
    # Display header
    st.subheader("Recent Workouts")
    
    # Define CSS for better styling
    st.markdown("""
        <style>
            .workout-card {
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                background-color: white;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            }
            .workout-date {
                font-weight: bold;
                font-size: 18px;
                margin-bottom: 10px;
                color: #1E90FF;
            }
            .workout-details {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
            }
            .workout-stat {
                display: flex;
                flex-direction: column;
            }
            .stat-label {
                color: #888;
                font-size: 12px;
            }
            .stat-value {
                font-weight: bold;
                font-size: 16px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Display each workout
    for workout in sorted_workouts[:5]:  # Limit to 5 most recent workouts
        try:
            # Parse timestamps to calculate duration
            start_time = datetime.strptime(workout.get('start_timestamp', ''), '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(workout.get('end_timestamp', ''), '%Y-%m-%d %H:%M:%S')
            duration = end_time - start_time
            minutes, seconds = divmod(duration.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            
            # Format duration string
            duration_str = ""
            if hours > 0:
                duration_str += f"{hours}h "
            if minutes > 0 or hours > 0:
                duration_str += f"{minutes}m "
            duration_str += f"{seconds}s"
            
            # Format date
            formatted_date = start_time.strftime("%B %d, %Y")  # e.g., January 01, 2024
            formatted_time = start_time.strftime("%I:%M %p")   # e.g., 12:00 AM
            
            # Create workout card
            st.markdown(f"""
                <div class="workout-card">
                    <div class="workout-date">{formatted_date} at {formatted_time}</div>
                    <div class="workout-details">
                        <div class="workout-stat">
                            <span class="stat-label">Duration</span>
                            <span class="stat-value">{duration_str}</span>
                        </div>
                        <div class="workout-stat">
                            <span class="stat-label">Distance</span>
                            <span class="stat-value">{workout.get('distance', 0):.1f} km</span>
                        </div>
                        <div class="workout-stat">
                            <span class="stat-label">Steps</span>
                            <span class="stat-value">{workout.get('steps', 0):,}</span>
                        </div>
                        <div class="workout-stat">
                            <span class="stat-label">Calories Burned</span>
                            <span class="stat-value">{workout.get('calories_burned', 0)}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        except (ValueError, KeyError, Exception) as e:
            # Handle potential errors gracefully
            st.error(f"Error displaying workout: {e}")
