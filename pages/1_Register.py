import streamlit as st
from google.cloud import bigquery
import time
import re
import uuid

st.set_page_config(layout="wide", page_title="Spaghetti Crew Workout App - Register")

def validate_email(email):
    """Validate email format using regex pattern."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

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

def check_username_exists(username):
    """Check if username already exists in the database."""
    try:
        client = bigquery.Client(project="roberttechx25")
        query = """
            SELECT COUNT(*) as count
            FROM `roberttechx25.ISE.Users`
            WHERE Username = @username
        """
        query_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("username", "STRING", username)
            ]
        )
        results = list(client.query(query, job_config=query_config).result())
        return results[0].count > 0
    except Exception as e:
        st.error(f"Database error: {e}")
        return False

def check_email_exists(email):
    """Check if email already exists in the database."""
    try:
        client = bigquery.Client(project="roberttechx25")
        query = """
            SELECT COUNT(*) as count
            FROM `roberttechx25.ISE.Users`
            WHERE Email = @email
        """
        query_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("email", "STRING", email)
            ]
        )
        results = list(client.query(query, job_config=query_config).result())
        return results[0].count > 0
    except Exception as e:
        st.error(f"Database error: {e}")
        return False

def create_user(full_name, username, email, password, date_of_birth):
    """
    Create a new user in the database.
    
    Args:
        full_name (str): The user's full name
        username (str): The user's username
        email (str): The user's email
        password (str): The user's password (should be hashed in production)
        date_of_birth (str): The user's date of birth in YYYY-MM-DD format
        
    Returns:
        tuple: (success, user_id or error_message)
    """
    try:
        # Generate a unique user ID
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        
        # In a real app, you would hash the password before storing
        client = bigquery.Client(project="roberttechx25")
        
        # Default profile image
        default_profile_image = "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg"
        
        query = """
            INSERT INTO `roberttechx25.ISE.Users` 
            (UserId, Name, Username, Email, Password, DateOfBirth, ImageUrl)
            VALUES 
            (@user_id, @full_name, @username, @email, @password, @date_of_birth, @image_url)
        """
        
        query_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                bigquery.ScalarQueryParameter("full_name", "STRING", full_name),
                bigquery.ScalarQueryParameter("username", "STRING", username),
                bigquery.ScalarQueryParameter("email", "STRING", email),
                bigquery.ScalarQueryParameter("password", "STRING", password),
                bigquery.ScalarQueryParameter("date_of_birth", "STRING", date_of_birth),
                bigquery.ScalarQueryParameter("image_url", "STRING", default_profile_image)
            ]
        )
        
        job = client.query(query, job_config=query_config)
        job.result()  # Wait for the query to complete
        
        return True, user_id
        
    except Exception as e:
        error_msg = f"Error creating user: {e}"
        return False, error_msg

# Page title
st.title("Create New Account")

# Back to login link
st.page_link("app.py", label="← Back to Login")

# Registration form
with st.form("registration_form"):
    full_name = st.text_input("Full Name*")
    username = st.text_input("Username*", help="Choose a unique username for your account")
    email = st.text_input("Email Address*")
    password = st.text_input("Password*", type="password", 
                           help="Password must be at least 8 characters with uppercase, lowercase, and numbers")
    confirm_password = st.text_input("Confirm Password*", type="password")
    date_of_birth = st.date_input("Date of Birth*")
    
    # Terms and conditions checkbox
    agree_terms = st.checkbox("I agree to the Terms and Conditions")
    
    submit_button = st.form_submit_button("Create Account")
    
    if submit_button:
        # Validation checks
        error = False
        
        if not full_name or not username or not email or not password or not confirm_password:
            st.error("All fields marked with * are required")
            error = True
        
        if not error and check_username_exists(username):
            st.error("This username is already taken. Please choose another one.")
            error = True
            
        if not error and check_email_exists(email):
            st.error("This email is already registered. Please use another email or try to log in.")
            error = True
        
        if not error and not validate_email(email):
            st.error("Please enter a valid email address")
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
                dob_str = date_of_birth.strftime("%Y-%m-%d")
                success, result = create_user(full_name, username, email, password, dob_str)
                
                if success:
                    st.success("Account created successfully! You can now log in.")
                    # Set up session state to indicate account was created successfully
                    if 'account_created' not in st.session_state:
                        st.session_state.account_created = True
                    # Redirect to main page after 2 seconds
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
    st.markdown("[View our Privacy Policy](#)")