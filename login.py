import streamlit as st
import time
import json
import requests
from data_fetcher import login_user
from streamlit_lottie import st_lottie


# Remove the st.set_page_config line - this should only be in app.py
# st.set_page_config(layout="wide", page_title="Spaghetti Crew Workout App - Login")


def login_page():
    """
    Displays the login page and handles user authentication.
    
    Returns:
        None
    """
    # Hide the sidebar and hamburger menu with more aggressive CSS
    st.markdown("""
    <style>
        /* Hide sidebar and hamburger menu */
        section[data-testid="stSidebar"] {display: none;}
        button[kind="header"] {display: none;}
        [data-testid="collapsedControl"] {display: none !important;}
        
        /* Additional selectors to ensure complete hiding */
        header button[aria-label="Menu"] {display: none !important;}
        .st-emotion-cache-zq5wmm.ezrtsby0 {display: none !important;}
        div[data-testid="stToolbar"] {display: none !important;}
        
        /* Hide the main menu on top right of the page */
        .stApp > header {
            display: none !important;
        }
        
        /* Expand main content to full width */
        .main .block-container {
            max-width: 100%;
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        
        /* Center links */
        div.css-1629p8f.e1nzilvr1 {
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if returning from successful registration
    if 'account_created' in st.session_state and st.session_state.account_created:
        st.success("Account created successfully! Please log in with your new credentials.")
        # Clear the flag to avoid showing the message again
        st.session_state.account_created = False
    
    # For session state management
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0
    
    # Display login form only if not authenticated
    if not st.session_state.authenticated:
        # Create centered login container
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("<h1 style='text-align: center'>Start your workout journey</h1>", unsafe_allow_html=True)

            
            
            
            # Try to load a default Lottie animation from a local file or a different URL
            try:
                # Option 1: Try a different URL for the Lottie animation
                lottie_url = "https://lottie.host/3cabd8b1-4c60-4bea-8b1a-a22da0494f93/zkDH17AbQR.json"
                lottie_runner = load_lottieurl(lottie_url)
                
                if lottie_runner:
                    st_lottie(
                        lottie_runner,
                        speed=3,
                        reverse=False,
                        loop=True,
                        quality="high",
                        height=400
                    )
                # If loading fails, we'll just continue without showing an animation
            except Exception as e:
                # Just skip the animation if it fails, no need to show an error
                pass
            
            # Form inputs
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button("Login")
            
                if submit_button:
                    # Simple validation
                    if not username or not password:
                        st.error("Please enter both username and password")
                    else:
                        # Show a spinner during authentication
                        with st.spinner("Authenticating..."):
                            # Add a small delay to simulate authentication process
                            time.sleep(0.5)
                            user = login_user(username, password)
                            
                            if user:
                                st.session_state.authenticated = True
                                st.session_state.user_id = user["UserId"]
                                st.success("Login successful! Redirecting...")
                                time.sleep(1)  # Brief delay for the success message to be visible
                                st.rerun()  # Refresh the page to apply session state changes
                            else:
                                st.session_state.login_attempts += 1
                                st.error(f"Invalid username or password. Try again. ({st.session_state.login_attempts})")
            
        
            # Registration or password reset links
            st.markdown("---")
            
            # Center links using HTML/CSS
            st.markdown("""
            <div style='display: flex; justify-content: center; gap: 20px;'>
                <a href='pages/1_Register.py' target='_self'>Register new account</a>
                <a href='https://www.youtube.com/watch?v=dQw4w9WgXcQ' target='_blank'>Forgot password?</a>
            </div>
            """, unsafe_allow_html=True)


def load_lottieurl(url: str):
    """
    Load a Lottie animation from a URL
    
    Args:
        url (str): URL to the Lottie animation
        
    Returns:
        dict: The Lottie animation as a dictionary, or None if loading fails
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        # Just return None instead of raising an error
        return None


# For testing the login page directly
if __name__ == "__main__":
    # Only set page config if running this file directly
    st.set_page_config(layout="wide", page_title="Spaghetti Crew Workout App - Login", initial_sidebar_state="collapsed")
    login_page()