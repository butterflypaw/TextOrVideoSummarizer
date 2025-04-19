# app.py
import streamlit as st
from streamlit_option_menu import option_menu
import Home
import Summarizer
import Settings
import History
import Login_Register

# Set page configuration
st.set_page_config(page_title="Text Summarizer", layout="wide")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

# Sidebar menu
with st.sidebar:
    if st.session_state['logged_in']:
        select = option_menu(
            "Menu",
            ["Home", "Summarizer", "History", "Settings", "Logout"],
            icons=["house-fill", "card-text", "clock-history", "gear-fill", "door-open"],
            menu_icon="cast",
        )
    else:
        select = option_menu(
            "Menu",
            ["Home", "Summarizer", "Settings", "Login/Register"],
            icons=["house-fill", "card-text", "gear-fill", "key"],
            menu_icon="cast",
        )

# Handling menu selection
if select == 'Summarizer':
    Summarizer.summarizer()
elif select == 'Settings':
    Settings.settings()
elif select == 'Login/Register':
    Login_Register.login_register()
elif select == 'History':
    History.history()
elif select == 'Logout':
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['user_id'] = None
    st.experimental_rerun()
else:
    Home.home()