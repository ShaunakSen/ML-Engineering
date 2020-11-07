import streamlit as st
import pandas as pd
import numpy as np


st.title('Uber pickups in NYC')


DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

print (DATA_URL)

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

st.write("""
It turns out that it takes a long time to download data, and load 10,000 lines into a dataframe. Converting the date column into datetime isn’t a quick job either. You don’t want to reload the data each time the app is updated – luckily Streamlit allows you to cache the data.
""")

if st.checkbox(label="Show data", value=False):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')

hour_values = data[DATE_COLUMN].dt.hour

print (max(hour_values), min(hour_values))

hist_values = np.histogram(a=hour_values, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

st.write("""
After a quick review, it looks like the busiest time is 17:00 (5 P.M.).
""")

st.subheader('Map of all pickups')

st.map(data)

st.write("""
After drawing your histogram, you determined that the busiest hour for Uber pickups was 17:00. Let’s redraw the map to show the concentration of pickups at 17:00.
""")

hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
