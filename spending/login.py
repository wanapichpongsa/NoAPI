import streamlit as st
import logging
from db.userdb import UserDatabase

def login():
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        # Double check if vulnerable
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login"):
                if UserDatabase.check_user_exists(username):
                    if UserDatabase.verify_password(username, password):
                        st.success("Login successful")
                        st.session_state.logged_in = True
                        # Might have to check device and location (is that really you?)
                    else:
                        st.error("Wrong username/Password")
                else:
                    st.error("Wrong username/Username does not exist")
        with col2:
            if st.button("new user? Click to register"):
                logging.info("NAV: login -> register")