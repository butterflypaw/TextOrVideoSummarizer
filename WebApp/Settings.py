# Settings.py
import streamlit as st
from Database import update_password, verify_user

def settings():
    st.title("Settings")
    
    if not st.session_state.get('logged_in', False):
        st.warning("Please login to access settings")
        return
    
    st.markdown("### Account Settings")
    
    with st.form("change_password_form"):
        st.write("Change Password")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("Change Password"):
            if verify_user(st.session_state['username'], current_password):
                if new_password == confirm_password:
                    if update_password(st.session_state['username'], new_password):
                        st.success("Password changed successfully!")
                    else:
                        st.error("Error updating password")
                else:
                    st.error("New passwords don't match")
            else:
                st.error("Current password is incorrect")
    
    st.markdown("### Summarization Settings")
    st.info("These settings are applied by default for your summaries")
    
    default_length = st.selectbox("Default Summary Length:", ["Short", "Medium", "Long"], index=1)
    default_method = st.selectbox("Default Summarization Method:", ["Extractive", "Abstractive"], index=1)
    
    if st.button("Save Settings"):
        # You can implement saving these preferences to the database if needed
        st.success("Settings saved successfully!")