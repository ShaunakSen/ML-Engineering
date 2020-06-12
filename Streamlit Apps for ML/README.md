## Streamlit Apps for developing ML tools

> Baised on the tutorials by JCharisTech & J-Secur1ty: [link](https://www.youtube.com/watch?v=_9WiB2PDO7k&list=PLJ39kWiJXSixyRMcn3lrbv8xI8ZZoYNZU&index=2&t=0s)

---

### Starting off..

`streamlit --help`: provides some useful initial commands

`streamlit run app.py`: runs the app in a dev server

### Simple text formatting

```python
import streamlit as st

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
```

### st.write: Swiss army knife

This is the Swiss Army knife of Streamlit commands: it does different
things depending on what you throw at it. Unlike other Streamlit commands,
write() has some unique properties:

1. You can pass in multiple arguments, all of which will be written.
2. Its behavior depends on the input types as follows.
3. It returns None, so it's "slot" in the App cannot be reused.

Some example arguments are: pandas dataframe, keras model, matplotlib figure, bokeh plot etc.

### Displaying images

```python
img = Image.open('./carbon.png')
st.image(img, caption="Simple image of code", use_column_width=True)
```

### Different widgets

```python
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
```

