### import core packages
import streamlit as st
import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')

menu = ['Home', 'Login', 'Register']
submenu = ['Visualizations', 'Predictions']

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
        pass

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