import streamlit as st

def initialize_session():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'location' not in st.session_state:
        st.session_state.location = None
    if 'keyword' not in st.session_state:
        st.session_state.keyword = None
    if 'selected_facility' not in st.session_state:
        st.session_state.selected_facility = None
    if 'invalid_keyword' not in st.session_state:
        st.session_state.invalid_keyword = False
