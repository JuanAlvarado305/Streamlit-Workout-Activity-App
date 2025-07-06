import streamlit as st
from data_fetcher import update_password_with_token

def reset_password_page():
    """
    Displays the form for the user to enter and confirm their new password.
    """
    st.title("Set Your New Password")

    # Get the token from the URL query parameters
    try:
        token = st.query_params["token"]
    except KeyError:
        st.error("No password reset token found. Please use the link from your email.")
        return

    with st.form("reset_password_form"):
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        submitted = st.form_submit_button("Set New Password")

        if submitted:
            if not all([new_password, confirm_password]):
                st.error("Please fill out both password fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                # Call the backend function to update the password
                with st.spinner("Updating your password..."):
                    message = update_password_with_token(token, new_password)
                    if "successfully" in message:
                        st.success(message)
                        st.info("You will be redirected to the login page shortly.")
                        # Clear query params and redirect
                        st.query_params.clear()
                        st.session_state.current_page = 'login'
                        st.rerun()
                    else:
                        st.error(message)