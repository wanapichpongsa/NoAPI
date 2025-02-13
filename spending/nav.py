import streamlit as st

class Navigation:
    """
    Use page_link when pages are in seperate py files. But rn I guess keep as 'SPA'
    """
    @staticmethod
    def nav_to_login():
        st.session_state.page = 'login'
    @staticmethod
    def nav_to_register():
        st.session_state.page = 'register'
    @staticmethod
    def nav_to_main():
        st.session_state.page = 'main'