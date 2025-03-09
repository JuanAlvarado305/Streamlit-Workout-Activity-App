#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component
import streamlit as st
from datetime import datetime



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
    """Displays a user post with an improved layout in Streamlit."""

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
    """Write a good docstring here."""
    pass


def display_recent_workouts(workouts_list):
    """Write a good docstring here."""
    pass


def display_genai_advice(timestamp, content, image):
    """Write a good docstring here."""
    pass
