import streamlit as st
from google.cloud import bigquery
import time

# Remove the st.set_page_config line - this should only be in app.py
# st.set_page_config(layout="wide", page_title="Spaghetti Crew Workout App - Login")

def authenticate_user(username, password):
    """
    Authenticates a user against the database.
    
    Args:
        username (str): The username entered by the user
        password (str): The password entered by the user
        
    Returns:
        tuple: (success, user_id) where success is a boolean indicating whether
               authentication was successful, and user_id is the user's ID if successful
    """
    try:
        # In a real app, you would query BigQuery for user credentials
        # and verify the password with proper hashing
        client = bigquery.Client(project="roberttechx25")
        query = """
            SELECT UserId, Password
            FROM `roberttechx25.ISE.Users`
            WHERE Username = @username
        """
        query_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("username", "STRING", username)
            ]
        )
        results = list(client.query(query, job_config=query_config).result())
        
        if not results:
            return False, None
            
        # In a real app, you would use password hashing!
        # This is simplified for demo purposes
        stored_password = results[0].Password
        if password == stored_password:
            return True, results[0].UserId
        return False, None
    
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return False, None

def login_page():
    """
    Displays the login page and handles user authentication.
    
    Returns:
        None
    """
    # Check if returning from successful registration
    if 'account_created' in st.session_state and st.session_state.account_created:
        st.success("Account created successfully! Please log in with your new credentials.")
        # Clear the flag to avoid showing the message again
        st.session_state.account_created = False
    
    # Check for the back_to_login parameter in URL
    query_params = st.experimental_get_query_params()
    if "back_to_login" in query_params:
        st.info("Please log in to access your account.")
        # Clear the parameter to avoid showing the message again
        st.experimental_set_query_params()
    
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
                            success, user_id = authenticate_user(username, password)
                            
                            if success:
                                st.session_state.authenticated = True
                                st.session_state.user_id = user_id
                                st.success("Login successful! Redirecting...")
                                time.sleep(1)  # Brief delay for the success message to be visible
                                st.rerun()  # Refresh the page to apply session state changes
                            else:
                                st.session_state.login_attempts += 1
                                st.error(f"Invalid username or password. Try again. ({st.session_state.login_attempts})")
            
            # Demo credentials for testing (For real app, you would remove this)
            st.markdown("---")
            st.caption("For demo purposes, try:")
            st.code("Username: user1\nPassword: password123")
        
            # Registration or password reset links could go here
            st.markdown("---")
            cols = st.columns(2)
            with cols[0]:
                # Link to registration page
                st.markdown("[Register new account](/register)")
            with cols[1]:
                st.markdown("[Forgot password?](#)")

# For testing the login page directly
if __name__ == "__main__":
    # Only set page config if running this file directly
    st.set_page_config(layout="wide", page_title="Spaghetti Crew Workout App - Login")
    login_page()