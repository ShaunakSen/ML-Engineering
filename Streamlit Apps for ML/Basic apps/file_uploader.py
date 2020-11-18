#### Based on tutorial by 
#### JCharisTech & J-Secur1ty: https://www.youtube.com/watch?v=vwFR2bXXzTw

import streamlit as st
import pandas as pd
import numpy as np
import pickle

def main():
    st.title("File upload")

    menu = ['Home', 'Dataset', 'Document', 'About']

    choice = st.sidebar.selectbox(label='Menu', options=menu)

    if choice == menu[0]:
        st.subheader(menu[0])

    elif choice == menu[1]:
        st.subheader(menu[1])

    elif choice == menu[2]:
        st.subheader(menu[2])

    elif choice == menu[3]:
        st.subheader(menu[3])

if __name__ == "__main__":
    main()