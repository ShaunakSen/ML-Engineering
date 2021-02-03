#### Based on tutorial by 
#### JCharisTech & J-Secur1ty: https://www.youtube.com/watch?v=vwFR2bXXzTw

import streamlit as st
import pandas as pd
import numpy as np
import pickle


### load image

from PIL import Image

@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return img

def main():
    st.title("File upload")

    menu = ['Home', 'Dataset', 'Document', 'About']

    choice = st.sidebar.selectbox(label='Menu', options=menu)

    if choice == menu[0]:
        st.subheader(menu[0])

        ### Image 
        image_file = st.file_uploader(label='Upload Image', type=['png', 'jpg', 'jpeg'])
        ### some info about the file
        if image_file:
            ## see the details
            st.write(type(image_file))
            st.write(dir(image_file))
            file_details = {
                "filename": image_file.name,
                "filetype": image_file.type,
                "filesize": image_file.size
            }
            st.write(file_details)

            st.image(image=load_image(image_file), caption=file_details['filename'], width=500, height=500)

    elif choice == menu[1]:
        st.subheader(menu[1])
        data_file = st.file_uploader(label='Upload CSV', type=['csv'])

        if data_file:
            st.write(type(data_file))
            # st.write(dir(data_file))
            file_details = {
                "filename": data_file.name,
                "filetype": data_file.type,
                "filesize": data_file.size
            }
            st.write(file_details)

            df = pd.read_csv(data_file)
            st.dataframe(df)

    elif choice == menu[2]:
        st.subheader(menu[2])

    elif choice == menu[3]:
        st.subheader(menu[3])

if __name__ == "__main__":
    main()