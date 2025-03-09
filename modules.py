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
    """Write a good docstring here."""
    pass


def display_activity_summary(workouts_list):
    """Write a good docstring here."""
    pass


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
    """Write a good docstring here."""
    pass
