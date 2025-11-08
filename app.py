import streamlit as st
from config import CUSTOM_CSS, setup_page_config, initialize_session_state
from ui import render_header, render_sidebar, render_main_content, render_footer

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

setup_page_config()

initialize_session_state()

render_header()
render_sidebar()
render_main_content()
render_footer()

