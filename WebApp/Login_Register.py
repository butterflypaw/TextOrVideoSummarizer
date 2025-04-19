# Login_Register.py
import streamlit as st
from Database import verify_user, register_user, get_user_id

def login_register():
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    # Check for the correct rerun function based on Streamlit version
    if hasattr(st, 'rerun'):
        rerun_func = st.rerun
    else:
        rerun_func = st.experimental_rerun
    
    with tab1:
        st.markdown("### Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if verify_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['user_id'] = get_user_id(username)
                st.success("Login successful!")
                rerun_func()  # Use the appropriate rerun function
            else:
                st.error("Invalid username or password")
    
    with tab2:
        st.markdown("### Register")
        new_username = st.text_input("Username", key="register_username")
        new_email = st.text_input("Email", key="register_email")
        new_password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        if st.button("Register"):
            if new_password != confirm_password:
                st.error("Passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long")
            elif register_user(new_username, new_password, new_email):
                st.success("Registration successful! Please login.")
            else:
                st.error("Username already exists")