import streamlit as st
import time
from data_fetcher import generate_password_reset_token

def forgot_password_page():
    """
    Displays the page for the user to enter their email and get a reset link.
    """
    # --- HIDE THE SIDEBAR ---
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)
    # -------------------------

    st.title("Reset Your Password")

    if st.button("← Back to Login"):
        st.session_state.current_page = 'login'
        st.rerun()

    st.write("Please enter your email address. If an account with this email exists, we will generate a password reset link.")

    with st.form("forgot_password_form"):
        email = st.text_input("Email Address")
        submitted = st.form_submit_button("Generate Reset Link")

        if submitted:
            if not email:
                st.error("Please enter an email address.")
            else:
                with st.spinner("Generating link..."):
                    # Call the new backend function
                    token = generate_password_reset_token(email)
                
                if token:
                    # For testing, we display the link on screen.
                    # In a real app, you would email this link.
                    reset_link = f"/?page=reset_password&token={token}"
                    st.success("Password reset link generated successfully!")
                    st.info("In a real app, this link would be emailed to you. For now, click the link below to proceed:")
                    st.markdown(f"**[Click here to reset your password]({reset_link})**")
                else:
                    st.success("If an account with that email exists, a password reset link has been sent.")