"""
Main application file for the Data Analysis Notebook
This is the entry point for the Streamlit application
"""

import streamlit as st
from config import CUSTOM_CSS, setup_page_config, initialize_session_state
from ui import render_header, render_sidebar, render_main_content, render_footer

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Setup page configuration
setup_page_config()

# Initialize session state
initialize_session_state()

# Render the application
render_header()
render_sidebar()
render_main_content()
render_footer()

