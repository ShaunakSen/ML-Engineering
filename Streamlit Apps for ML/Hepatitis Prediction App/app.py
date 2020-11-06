### import core packages
import streamlit as st
import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
import matplotlib
import hashlib
import plotly.express as px
matplotlib.use('agg')

### db module
from manage_db import *

st.set_option('deprecation.showPyplotGlobalUse', False)

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

def render_viz_view():
    df = pd.read_csv("./data/clean_hepatitis_dataset.csv")

    st.dataframe(data=df.head())
    df['class'].value_counts().plot(kind='bar')
    st.pyplot()

    ### freq dist plot
    freq_df = pd.read_csv("./data/freq_df_hepatitis_dataset.csv")

    st.dataframe(freq_df[['age', 'count']])

    fig = px.bar(data_frame=freq_df, x='age', y='count')
    st.plotly_chart(fig)
    print ("Here")
    check = st.checkbox(label="Area Chart")
    print (check)
    ### area chart 
    if check:
        all_cols = df.columns.tolist()
        print (all_cols)
        feature_choices = st.multiselect(label="Choose the features to include", options=all_cols)
        new_df = df[feature_choices]
        st.area_chart(data=new_df)

    return

def render_login_view():
    username = st.sidebar.text_input(label='Enter username', max_chars=20)
    password = st.sidebar.text_input(label='Enter password', max_chars=20, type='password')

    ## check if login button clicked
    if st.sidebar.button(label='Login'):
        
        create_usertable()
        hashed_pwd = generate_hashed_pwd(password)
        result = login_user(username, hashed_pwd)

        if len(result) == 1:
            st.success(f"Welcome!! {username}")
            activity = st.selectbox(label='Select activity', options=submenu)
            if activity == submenu[0]:
                st.subheader(submenu[0])
                ### render visualizations view
                render_viz_view()
            elif activity == submenu[1]:
                st.subheader(submenu[1])

        else:
            st.error("Please check username/password")

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


main()

        ### https://scontent.fgau1-2.fna.fbcdn.net/v/t31.0-8/10750009_948237601857597_2994500559473682818_o.jpg?_nc_cat=111&ccb=2&_nc_sid=cdbe9c&_nc_ohc=-tRvZtGJiBoAX9qBWzv&_nc_oc=AQnVeYtGx4s3VBUzzZGEwmNUyPYCBWPTYQmHVpWyWVReLVxY4N05WL0bf6IvRrxRDG_1Ez-O25ptR3NlY-wH7uSe&_nc_ht=scontent.fgau1-2.fna&oh=755190db24cea1900c0b15627df91821&oe=5FC8EEB7