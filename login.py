import streamlit as st
import time
from data_fetcher import login_user

# Remove the st.set_page_config line - this should only be in app.py
# st.set_page_config(layout="wide", page_title="Spaghetti Crew Workout App - Login")


def login_page():
    """
    Displays the login page and handles user authentication.
    
    Returns:
        None
    """
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
            st.title("Welcome to Spaghetti Crew Workout App")
            
            # Logo or app branding could go here
            st.image("https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg", width=200)
            
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
            
        
            # Registration or password reset links could go here
            st.markdown("---")
            cols = st.columns(2)
            with cols[0]:
                st.markdown("[Register new account](#)")
            with cols[1]:
                st.markdown("[Forgot password?](#)")

# For testing the login page directly
if __name__ == "__main__":
    # Only set page config if running this file directly
    st.set_page_config(layout="wide", page_title="Spaghetti Crew Workout App - Login")
    login_page()