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
if st.checkbox(label="Show/Hide"):
    st.text("Showing text!")

# radio buttons
mini_likes = st.radio(label="Mini likes what?", options=["Chocolates", "Clothes", "All"])
if mini_likes == "All":
    st.warning("Mini is greedy!")
else:
    st.success(f"Mini can have {mini_likes}")

## select box


## multi select

mini_likes_multiple = st.multiselect(label="What mini likes to eat", options=["Badam halwa", "Gobi parantha", "Paneer", "Beej"])

for mini_food in mini_likes_multiple:
    st.text(f"Mini likes to eat {mini_food}")

## slider
age = st.slider(label="How old is mini", min_value=5, max_value=100, value=24)
st.success(f"Mini is {age} years old!")

## buttons
mini_button = st.button(label="Hi mini!")

count_hi = 0
if mini_button:
    st.success(f"Mini says hi {count_hi+1} times!") ### DOES NOT work
    count_hi+=1

st.text(count_hi)