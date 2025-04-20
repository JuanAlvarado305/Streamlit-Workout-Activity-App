import streamlit as st
from google.cloud import bigquery
from data_fetcher import register_user
import time
import re
import uuid

st.set_page_config(layout="wide", page_title="Spaghetti Crew Workout App - Register", initial_sidebar_state="collapsed")

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
</style>
""", unsafe_allow_html=True)

def validate_password(password):
    """
    Validate password strength.
    Requires at least 8 characters, one uppercase, one lowercase, one digit.
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, "Password meets requirements"

# Page title
st.title("Create New Account")

# Back to login link using regular markdown
st.markdown("[← Back to Login](../)")

# Registration form
with st.form("registration_form"):
    # Reinstated full name field
    full_name = st.text_input("Full Name*")
    username = st.text_input("Username*", help="Choose a unique username for your account")
    # Email address field still removed
    password = st.text_input("Password*", type="password", 
                           help="Password must be at least 8 characters with uppercase, lowercase, and numbers")
    confirm_password = st.text_input("Confirm Password*", type="password")
    # Date of birth field still removed
    
    # Terms and conditions checkbox
    agree_terms = st.checkbox("I agree to the Terms and Conditions")
    
    submit_button = st.form_submit_button("Create Account")
    
    if submit_button:
        # Validation checks
        error = False
        
        if not full_name or not username or not password or not confirm_password:
            st.error("All fields marked with * are required")
            error = True
            
        if not error:
            password_valid, password_msg = validate_password(password)
            if not password_valid:
                st.error(password_msg)
                error = True
        
        if not error and password != confirm_password:
            st.error("Passwords do not match")
            error = True
            
        if not error and not agree_terms:
            st.error("You must agree to the Terms and Conditions")
            error = True
            
        # If all validations pass, create the user
        if not error:
            with st.spinner("Creating your account..."):
                result = register_user(username, full_name, password)
                
                if result == "¡Successfully registered!":
                    st.success("Account created successfully! You can now log in.")
                    st.session_state.account_created = True
                    time.sleep(2)
                    st.switch_page("app.py")
                else:
                    st.error(f"Failed to create account: {result}")

# Add some instructions and info below the form
st.markdown("---")
st.subheader("Join the Spaghetti Crew Workout Community")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Benefits")
    st.markdown("• Track your workouts and progress")
    st.markdown("• Connect with friends")
    st.markdown("• Share your fitness achievements")
    st.markdown("• Get personalized workout suggestions")

with col2:
    st.markdown("### Privacy")
    st.markdown("• Your data is securely stored")
    st.markdown("• You control what you share")
    st.markdown("• We never sell your information")
    st.markdown("[View our Privacy Policy](https://www.youtube.com/watch?v=dQw4w9WgXcQ)")