import streamlit as st
import numpy as np
from PIL import Image

def my_stupid_function(stupidity):
    """
    takes some stupidity and returns 1000x more stupidity
    """
    return 1000*stupidity

st.title("Streamlit tutorial")

st.header("This is a header")

st.subheader("This is a subheader")

## Normal text
st.text("Hello mini")

## markdown
st.markdown("> Hello mini in markdown!")

### Text formats
st.success("Successful sample")
st.info("Info: test info")
st.warning("Warning: test warning")
st.error("Error: test error")
st.exception(RuntimeError('This is an exception of type RuntimeError'))

### Writing text: super functiom
st.write(my_stupid_function(10))

### print out documentation
st.help(my_stupid_function)
st.help(st.write)

### displaying images and videos
st.subheader("Displaying images and videos")
st.markdown("---")
img = Image.open('./carbon.png')
st.image(img, caption="Simple image of code", use_column_width=True)

### Working with widgets
st.subheader("Working with widgets")
st.markdown("---")