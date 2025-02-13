import streamlit as st
import logging
from db.userdb import UserDatabase

def register():
      st.title("Register")
      username = st.text_input("Username")
      password = st.text_input("Password", type="password")
      confirm_password = st.text_input("Confirm Password", type="password")
      if st.button("Register"):
        if password != confirm_password:
          st.error("Passwords do not match")
        if UserDatabase.check_user_exists(username):
          st.error("Username already exists")
        else:
          UserDatabase.create_user(username, password)
          st.success("Registration successful")
          logging.info("NAV: register -> login")