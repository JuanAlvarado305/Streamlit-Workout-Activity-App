#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

import streamlit as st
from data_fetcher import get_user_profile
from html import escape
from internals import create_component
from datetime import datetime
import random
from google.cloud import bigquery
import uuid

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

def display_post(post, get_user_data=get_user_profile):
    """Displays a user post with an improved layout in Streamlit.
    This function was created with the help of ChatGPT and Gemini.
    """
    # Get User Data
    userData = get_user_data(post['AuthorId'])
    username = userData['username']
    user_image = userData['profile_image']
    timestamp = post['Timestamp']
    content = post['Content']
    post_image = post['ImageUrl']

    # Format Timestamp
    formatted_time = timestamp.strftime("%d %b %Y, %I:%M %p")  # e.g., 08 Mar 2024, 02:30 PM

    # CSS styles for the post
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
                margin-bottom: 0;
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

    with st.container():
        # Header: profile picture and user info
        col1, col2 = st.columns([1, 20])
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
        # Post Content and optional image
        st.markdown(f"<p class='post-content'>{content} #GoogleTech2025</p>", unsafe_allow_html=True)
        if post_image:
            st.image(post_image, use_container_width=True)

def display_activity_summary(workouts_list):
    """Displays a summary of user workout activities.
    
    This component creates a visual summary showing total number of workouts,
    total distance covered, total steps taken, total calories burned, and 
    a list of recent workouts with their details.
    
    Args:
        workouts_list: A list of dictionaries, each containing workout details.
    
    Returns:
        None. Renders the activity summary component in the Streamlit app.
    """
    workout_count = len(workouts_list)
    total_distance = sum(workout.get('TotalDistance', 0) for workout in workouts_list)
    total_steps = sum(workout.get('TotalSteps', 0) for workout in workouts_list)
    total_calories = sum(workout.get('CaloriesBurned', 0) for workout in workouts_list)

    # Create HTML rows for each workout (sorted most recent first)
    activity_rows = ""
    sorted_workouts = sorted(workouts_list, key=lambda x: x.get('StartTimestamp', ''), reverse=True)
    for workout in sorted_workouts:
        timestamp = workout.get('StartTimestamp')
        date = timestamp.strftime('%d %b %Y, %I:%M %p') if timestamp else 'N/A'
        row_html = f'''
        <div class="activity-row">
            <span>{date}</span>
            <span>{workout.get('TotalDistance', 0)} km</span>
            <span>{workout.get('TotalSteps', 0)}</span>
            <span>{workout.get('CaloriesBurned', 0)}</span>
        </div>
        '''
        activity_rows += row_html

    data = {
        'WORKOUT_COUNT': workout_count,
        'TOTAL_DISTANCE': round(total_distance, 1),
        'TOTAL_STEPS': total_steps,
        'TOTAL_CALORIES': total_calories,
        'ACTIVITY_ROWS': activity_rows
    }
    html_file_name = "my_custom_component"
    height = 350 + min(len(workouts_list) * 40, 400)  # Adjust height according to workout count
    create_component(data, html_file_name, height=height)

def display_genai_advice(timestamp, content, image):
    """
    Creates and displays a motivational advice component using the provided data.
    
    Parameters:
        timestamp (str or datetime): The time when the advice was generated.
        content (str): The motivational advice text.
        image (str): The URL or file path of the image associated with the advice.
    """
    safe_timestamp_str = str(timestamp) if timestamp is not None else ""
    try:
        dt_object = datetime.strptime(safe_timestamp_str, "%Y-%m-%d %H:%M:%S")
        safe_timestamp_str = dt_object.strftime("%d %b %Y, %I:%M %p")
    except ValueError:
        pass
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
            background: linear-gradient(to bottom right, #6dd5fa, #2980b9);
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
        <img class="image" src="{image}" alt="">
        <p class="content">{safe_content}</p>
        <p class="time">{safe_timestamp}</p>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

def create_workout_content(workout):
    """Creates dynamic content based on workout data."""
    if not workout:
        return "Just completed a workout! Feeling great!"
    try:
        # Format the workout end time for readability
        end_time = datetime.strptime(workout['end_timestamp'], '%Y-%m-%d %H:%M:%S')
        workout_date = end_time.strftime('%A, %B %d')
        workout_time = end_time.strftime('%I:%M %p')
        steps = workout.get('steps', 0)
        distance = workout.get('distance', 0)
        calories = workout.get('calories_burned', 0)
        templates = [
            f"Just finished an awesome workout! Walked {steps} steps, covered {distance} km, and burned {calories} calories! 💪 #FitnessJourney",
            f"Workout complete on {workout_date}! {steps} steps, {distance} km distance, and {calories} calories burned. Feeling accomplished! 🏃",
            f"Today's fitness achievement: {steps} steps, {distance} km, and {calories} calories burned! Making progress one step at a time. 🔥",
            f"Just wrapped up my workout at {workout_time}! Stats: {steps} steps, {distance} km, {calories} calories. #StayActive",
            f"Another workout in the books! Logged {steps} steps and burned {calories} calories over {distance} km. #FitnessGoals"
        ]
        return random.choice(templates)
    except (KeyError, ValueError) as e:
        print(f"Error formatting workout content: {e}")
        return "Just completed a workout! Feeling great!"

def display_post_preview(content, image_url=None):
    """Displays a preview of how the post will look."""
    st.subheader("Post Preview:")
    preview_container = st.container()
    with preview_container:
        st.markdown("---")
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image("https://placekitten.com/100/100", width=60)
        with col2:
            st.markdown("**You**")
            st.markdown("*Just now*")
            st.markdown(content)
        if image_url:
            st.image(image_url, width=300)
        st.markdown("---")

def check_duplicate_post(user_id, content):
    """Checks if a very similar post was recently made by this user."""
    client = bigquery.Client(project='roberttechx25')
    query = """
        SELECT COUNT(*) as count
        FROM `roberttechx25.ISE.Posts` 
        WHERE AuthorId = @user_id
        AND Content LIKE @content_pattern
        AND Timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
    """
    content_words = content.split()
    if content_words:
        content_pattern = f"%{' '.join(content_words[:min(5, len(content_words))])}%"
        query_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter('user_id', 'STRING', user_id),
                bigquery.ScalarQueryParameter('content_pattern', 'STRING', content_pattern)
            ]
        )
        try:
            query_job = client.query(query, job_config=query_config)
            results = list(query_job.result())
            return results[0].count > 0
        except Exception as e:
            print(f"Error checking for duplicate posts: {e}")
    return False

def insert_post(user_id, content, image_url=None):
    """Inserts a new post into the database.
    Returns (success, message) tuple.
    """
    client = bigquery.Client(project='roberttechx25')
    post_id = f"post_{uuid.uuid4().hex[:8]}"
    query = """
        INSERT INTO `roberttechx25.ISE.Posts` (PostId, AuthorId, Timestamp, ImageUrl, Content)
        VALUES (@post_id, @author_id, CURRENT_TIMESTAMP(), @image_url, @content)
    """
    query_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('post_id', 'STRING', post_id),
            bigquery.ScalarQueryParameter('author_id', 'STRING', user_id),
            bigquery.ScalarQueryParameter('image_url', 'STRING', image_url),
            bigquery.ScalarQueryParameter('content', 'STRING', content)
        ]
    )
    try:
        query_job = client.query(query, job_config=query_config)
        query_job.result()  # Wait for query to complete
        return True, "Post shared successfully!"
    except Exception as e:
        error_msg = f"Error inserting post: {e}"
        print(error_msg)
        return False, error_msg

def display_recent_workouts(workouts_list):
    """Displays a list of recent workouts with detailed information.
    
    This function creates a visually appealing display of recent workouts 
    with detailed information about each workout including date, duration,
    distance, steps, and calories burned. The workouts are sorted by date
    with the most recent first.
    
    Args:
        workouts_list: A list of dictionaries containing workout details.
    
    Returns:
        None. Renders the recent workouts component in the Streamlit app.
    """
    if not workouts_list:
        st.write("No recent workouts found.")
        return
    sorted_workouts = sorted(workouts_list, key=lambda x: x.get('StartTimestamp', ''), reverse=True)
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
    for workout in sorted_workouts[:5]:
        try:
            start_time = workout.get('StartTimestamp')
            end_time = workout.get('EndTimestamp')
            duration = end_time - start_time
            minutes, seconds = divmod(duration.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            duration_str = ""
            if hours > 0:
                duration_str += f"{hours}h "
            if minutes > 0 or hours > 0:
                duration_str += f"{minutes}m "
            duration_str += f"{seconds}s"
            formatted_date = start_time.strftime("%B %d, %Y")
            formatted_time = start_time.strftime("%I:%M %p")
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
                            <span class="stat-value">{workout.get('TotalDistance', 0):.1f} km</span>
                        </div>
                        <div class="workout-stat">
                            <span class="stat-label">Steps</span>
                            <span class="stat-value">{workout.get('TotalSteps', 0):,}</span>
                        </div>
                        <div class="workout-stat">
                            <span class="stat-label">Calories Burned</span>
                            <span class="stat-value">{workout.get('CaloriesBurned', 0)}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        except (ValueError, KeyError, Exception) as e:
            st.error(f"Error displaying workout: {e}")

def display_user_sensor_data(sensor_data_list):
    """
    Takes in the list of sensor data and displays it to the user using Streamlit
    components with visualizations and interactive elements.
    """
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    if not sensor_data_list:
        st.warning("No sensor data available for this workout.")
        return

    df = pd.DataFrame(sensor_data_list)
    if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    sensor_types = df['sensor_type'].unique()

    st.markdown(
        """
        <style>
            .header {
                font-family: 'Source Sans Pro', sans-serif;
                font-size: 32px;
                font-weight: bold;
                color: #0e1117;
                margin-bottom: 20px;
            }
            .subheader {
                font-family: 'Source Sans Pro', sans-serif;
                font-size: 24px;
                font-weight: bold;
                color: #0e1117;
                margin: 25px 0 15px;
            }
            .summary-box {
                background-color: #f0f2f6;
                color: #0e1117;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 25px;
            }
            .summary-item {
                font-family: 'Source Sans Pro', sans-serif;
                margin: 5px 0;
                font-size: 16px;
                color: #0e1117;
            }
            @media (prefers-color-scheme: dark) {
                .header {
                    color: #ffffff;
                }
                .subheader {
                    color: #ffffff;
                }
                .summary-box {
                    background-color: #2c2c2c;
                    color: #ffffff;
                }
                .summary-item {
                    color: #ffffff;
                }
            }
        </style>
        """, unsafe_allow_html=True
    )

    st.header("Workout Sensor Data")
    st.markdown("<div class='subheader'>Summary</div>", unsafe_allow_html=True)
    workout_duration = (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 60
    summary_html = f"""
        <div class='summary-box'>
            <div class='summary-item'>• <strong>Workout Duration</strong>: {workout_duration:.1f} minutes</div>
            <div class='summary-item'>• <strong>Data Points Collected</strong>: {len(df)}</div>
            <div class='summary-item'>• <strong>Sensors Used</strong>: {len(sensor_types)}</div>
        </div>
    """
    st.markdown(summary_html, unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Charts", "Raw Data", "Insights"])

    with tab1:
        st.markdown("<div class='subheader'>Sensor Data Visualization</div>", unsafe_allow_html=True)
        selected_sensors = st.multiselect(
            "Select sensors to display:",
            options=list(sensor_types),
            default=list(sensor_types)[:min(3, len(sensor_types))]
        )
        if selected_sensors:
            filtered_df = df[df['sensor_type'].isin(selected_sensors)]
            for sensor in selected_sensors:
                sensor_df = filtered_df[filtered_df['sensor_type'] == sensor].sort_values("timestamp")
                units = sensor_df['units'].iloc[0] if not sensor_df.empty else ""
                st.markdown(f"<div class='subheader'>{sensor} ({units})</div>", unsafe_allow_html=True)
                sensor_chart_df = sensor_df.set_index("timestamp")[["data"]]
                st.line_chart(sensor_chart_df)
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Average", f"{sensor_df['data'].mean():.2f} {units}")
                col2.metric("Maximum", f"{sensor_df['data'].max():.2f} {units}")
                col3.metric("Minimum", f"{sensor_df['data'].min():.2f} {units}")
                col4.metric("Readings", f"{len(sensor_df)}")

    with tab2:
        st.markdown("<div class='subheader'>Raw Sensor Data</div>", unsafe_allow_html=True)
        st.dataframe(df.sort_values('timestamp'))
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "sensor_data.csv", "text/csv", key='download-csv')

    with tab3:
        st.markdown("<div class='subheader'>Insights and Patterns</div>", unsafe_allow_html=True)
        if len(sensor_types) > 1:
            st.markdown("<div class='subheader'>Sensor Correlations</div>", unsafe_allow_html=True)
            pivot_df = df.pivot_table(
                index='timestamp',
                columns='sensor_type',
                values='data',
                aggfunc='mean'
            ).reset_index()
            col1, col2 = st.columns(2)
            with col1:
                x_sensor = st.selectbox("Select X-axis sensor:", sensor_types, index=0)
            with col2:
                default_y_index = 1 if len(sensor_types) > 1 else 0
                y_sensor = st.selectbox("Select Y-axis sensor:", sensor_types, index=default_y_index)
            if x_sensor != y_sensor:
                scatter_df = pivot_df.dropna(subset=[x_sensor, y_sensor])
                if not scatter_df.empty:
                    fig = px.scatter(
                        scatter_df,
                        x=x_sensor,
                        y=y_sensor,
                        trendline="ols",
                        labels={
                            x_sensor: f"{x_sensor} ({df[df['sensor_type'] == x_sensor]['units'].iloc[0]})",
                            y_sensor: f"{y_sensor} ({df[df['sensor_type'] == y_sensor]['units'].iloc[0]})"
                        },
                        title=f"Relationship between {x_sensor} and {y_sensor}"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    corr = scatter_df[x_sensor].corr(scatter_df[y_sensor])
                    st.metric("Correlation Coefficient", f"{corr:.3f}")
                    if abs(corr) > 0.7:
                        st.info("Strong correlation detected between these sensors.")
                    elif abs(corr) > 0.4:
                        st.info("Moderate correlation detected between these sensors.")
                    else:
                        st.info("Weak or no correlation detected between these sensors.")
                else:
                    st.warning("Not enough data points to analyze correlation between these sensors.")
            else:
                st.warning("Please select different sensors for comparison.")
        st.markdown("<div class='subheader'>Time-Based Analysis</div>", unsafe_allow_html=True)
        if len(df) > 10:
            selected_sensor = st.selectbox("Select sensor for time analysis:", sensor_types)
            sensor_df = df[df['sensor_type'] == selected_sensor]
            units = sensor_df['units'].iloc[0] if not sensor_df.empty else ""
            window_size = max(3, len(sensor_df) // 10)
            sensor_df = sensor_df.sort_values('timestamp')
            sensor_df['rolling_avg'] = sensor_df['data'].rolling(window=window_size, min_periods=1).mean()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=sensor_df['timestamp'],
                y=sensor_df['data'],
                mode='markers',
                name='Raw readings',
                marker=dict(size=6)
            ))
            fig.add_trace(go.Scatter(
                x=sensor_df['timestamp'],
                y=sensor_df['rolling_avg'],
                mode='lines',
                name=f'{window_size}-point moving average',
                line=dict(width=3)
            ))
            fig.update_layout(
                title=f"{selected_sensor} Trend Analysis",
                xaxis_title="Time",
                yaxis_title=f"Value ({units})",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            start_value = sensor_df['rolling_avg'].iloc[0]
            end_value = sensor_df['rolling_avg'].iloc[-1]
            change_pct = ((end_value - start_value) / start_value) * 100 if start_value != 0 else 0
            if abs(change_pct) < 5:
                st.info(f"The {selected_sensor} values remained relatively stable throughout the workout.")
            elif change_pct > 0:
                st.info(f"The {selected_sensor} values showed an increasing trend of approximately {change_pct:.1f}% from start to finish.")
            else:
                st.info(f"The {selected_sensor} values showed a decreasing trend of approximately {abs(change_pct):.1f}% from start to finish.")
