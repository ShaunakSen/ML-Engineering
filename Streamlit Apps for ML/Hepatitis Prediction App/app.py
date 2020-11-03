### import core packages
import streamlit as st
import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
import matplotlib
import hashlib
matplotlib.use('agg')

### db module
from manage_db import *

menu = ['Home', 'Login', 'Register']
submenu = ['Visualizations', 'Predictions']

def generate_hashed_pwd(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def verify_hashes(password, hashed_text):
    if generate_hashed_pwd(password) == hashed_text:
        return hashed_text
    return False

def render_home_view():
    st.subheader('Home')
    st.text('Sort Home desc goes here....')

def render_login_view():
    username = st.sidebar.text_input(label='Enter username', max_chars=20)
    password = st.sidebar.text_input(label='Enter password', max_chars=20, type='password')

    ## check if login button clicked
    if st.sidebar.button(label='Login'):
        ## check password
        if password == 'mini':
            st.success(f"Welcome!! {username}")
            activity = st.selectbox(label='Select activity', options=submenu)
            if activity == submenu[0]:
                st.subheader(submenu[0])
            elif activity == submenu[1]:
                st.subheader(submenu[1])

def render_registration_view():
    new_username = st.text_input(label='Enter username', max_chars=20)
    new_password = st.text_input(label='Enter password', max_chars=20, type='password')

    confirm_password = st.text_input(label='Confirm password', max_chars=20, type='password')

    if new_password == confirm_password:
        st.success("Password confirmed")
    else:
        st.warning("Passwords did not match!")

    ### Submit button

    if st.button(label='Register'):
        print ("Register button clicked")
        ### 1. create users table (if already exists part is taken care of in the query)
        create_usertable()
        ### 2. Add that users data : you should hash the passworda and then store it in db
        hash_password = generate_hashed_pwd(new_password)
        print (hash_password)
        add_user_data(new_username, hash_password)

        st.success(f"Welcome!! {new_username}")
        st.info("Login to get started")

def main():
    """
    Hepatitis Mortality Prediction App
    """
    st.title("Disease Mortatlity Prediction App")
    
    choice = st.sidebar.selectbox(label='Menu', options=menu)

    if choice == 'Home':
        ### render home view
        render_home_view()
    elif choice == 'Login':
        ### render login view
        render_login_view()
    elif choice == 'Register':
        ### render registration view
        render_registration_view()


if __name__ == "__main__":
    main()