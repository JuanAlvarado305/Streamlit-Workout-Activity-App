import streamlit as st
import time
import json
import requests
from data_fetcher import login_user
from streamlit_lottie import st_lottie

def login_page():
    """
    Displays the login page and handles user authentication.
    """
    # Hide the sidebar and hamburger menu
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
        button[kind="header"] {display: none;}
        [data-testid="collapsedControl"] {display: none !important;}
        header button[aria-label="Menu"] {display: none !important;}
        .st-emotion-cache-zq5wmm.ezrtsby0 {display: none !important;}
        div[data-testid="stToolbar"] {display: none !important;}
        .stApp > header { display: none !important; }
        .main .block-container {
            max-width: 100%;
            padding-top: 1rem; padding-right: 1rem;
            padding-left: 1rem; padding-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if returning from successful registration
    if 'account_created' in st.session_state and st.session_state.account_created:
        st.success("Account created successfully! Please log in with your new credentials.")
        st.session_state.account_created = False
    
    # Display login form only if not authenticated
    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("<h1 style='text-align: center'>Start your workout journey</h1>", unsafe_allow_html=True)
            
            try:
                lottie_url = "https://lottie.host/3cabd8b1-4c60-4bea-8b1a-a22da0494f93/zkDH17AbQR.json"
                lottie_runner = load_lottieurl(lottie_url)
                if lottie_runner:
                    st_lottie(lottie_runner, speed=3, reverse=False, loop=True, quality="high", height=400)
            except Exception as e:
                pass # Skip animation if it fails
            
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button("Login")
            
                if submit_button:
                    if not username or not password:
                        st.error("Please enter both username and password")
                    else:
                        with st.spinner("Authenticating..."):
                            time.sleep(0.5)
                            user = login_user(username, password)
                            
                            if user:
                                st.session_state.authenticated = True
                                st.session_state.user_id = user["UserId"]
                                st.success("Login successful! Redirecting...")
                                time.sleep(1)
                                st.rerun()
                            else:
                                if 'login_attempts' not in st.session_state:
                                    st.session_state.login_attempts = 0
                                st.session_state.login_attempts += 1
                                st.error(f"Invalid username or password. Try again. ({st.session_state.login_attempts})")
        
        # --- CHANGE STARTS HERE ---
        # Updated navigation for Register and Forgot Password
        col_reg, col_forgot = st.columns(2)
        with col_reg:
            if st.button("Register new account", use_container_width=True):
                st.session_state.current_page = 'register'
                st.rerun()

        with col_forgot:
            if st.button("Forgot password?", use_container_width=True):
                st.session_state.current_page = 'forgot_password' # Navigate to new page
                st.rerun()
        # --- CHANGE ENDS HERE ---

def load_lottieurl(url: str):
    """Loads a Lottie animation from a URL."""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Spaghetti Crew Workout App - Login", initial_sidebar_state="collapsed")
    login_page()