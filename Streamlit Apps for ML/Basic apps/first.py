import streamlit as st
import numpy as np
import pandas as pd
import time


st.title('Mini App')

st.write("Here's our first attempt at using data to create a table:")

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

st.write(df)

checkbox = st.checkbox('Show line chart', value=False)
print (checkbox)
if checkbox:
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.dataframe(chart_data)
    st.line_chart(chart_data)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])


st.dataframe(map_data)
st.map(map_data)


option = st.sidebar.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected:', option

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'