#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component


# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        'NAME': value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username, user_image, timestamp, content, post_image):
    """Write a good docstring here."""
    pass


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
        <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #e9ecef;">
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
    
    # Register and display the component
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_recent_workouts(workouts_list):
    """Write a good docstring here."""
    pass


def display_genai_advice(timestamp, content, image):
    """Write a good docstring here."""
    pass
