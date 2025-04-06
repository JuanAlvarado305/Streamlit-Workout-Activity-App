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
    """Displays a user post with an improved layout in Streamlit."""
    """This function was created with the help of ChatGPT and Gemini"""
    
    #Get User Data
    userData = get_user_data(post['user_id'])
    username = userData['username']
    user_image = userData['profile_image']
    timestamp = post['timestamp']
    content = post['content']
    post_image = post['image']

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

def display_user_sensor_data(sensor_data_list):
    """
    Takes in the list of sensor data and displays it to the user using Streamlit components
    with visualizations and interactive elements.
    """
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from datetime import datetime

    if not sensor_data_list:
        st.warning("No sensor data available for this workout.")
        return

    # Convert the sensor data list to a DataFrame for easier manipulation.
    df = pd.DataFrame(sensor_data_list)

    # Convert the 'timestamp' column to datetime (if not already)
    if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Extract unique sensor types.
    sensor_types = df['sensor_type'].unique()

    # CSS styling that adapts to light and dark mode.
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
            /* Dark mode styles */
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

    # Add header using st.header (for testing and clarity)
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

    # Create tabs for different views.
    tab1, tab2, tab3 = st.tabs(["Charts", "Raw Data", "Insights"])

    # Tab 1: Charts
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
                # Prepare data for st.line_chart by setting timestamp as the index.
                sensor_chart_df = sensor_df.set_index("timestamp")[["data"]]
                st.line_chart(sensor_chart_df)
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Average", f"{sensor_df['data'].mean():.2f} {units}")
                col2.metric("Maximum", f"{sensor_df['data'].max():.2f} {units}")
                col3.metric("Minimum", f"{sensor_df['data'].min():.2f} {units}")
                col4.metric("Readings", f"{len(sensor_df)}")

    # Tab 2: Raw Data
    with tab2:
        st.markdown("<div class='subheader'>Raw Sensor Data</div>", unsafe_allow_html=True)
        st.dataframe(df.sort_values('timestamp'))
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download CSV",
            csv,
            "sensor_data.csv",
            "text/csv",
            key='download-csv'
        )

    # Tab 3: Insights
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
                