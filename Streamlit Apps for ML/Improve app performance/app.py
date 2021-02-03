import streamlit as st

import time


st.header('Improve App Performance')

st.markdown("""
When you mark a function with the `@st.cache decorator`, it tells Streamlit that whenever the function is called it needs to check a few things:

1. The input parameters that you called the function with

2. The value of any external variable used in the function

3. The body of the function

4. The body of any function used inside the cached function

If this is the first time Streamlit has seen these four components with these exact values and in this exact combination and order, it runs the function and stores the result in a local cache. Then, next time the cached function is called, if none of these components changed, Streamlit will just skip executing the function altogether and, instead, return the output previously stored in the cache.

The way Streamlit keeps track of changes in these components is through hashing. Think of the cache as an in-memory key-value store, where the key is a hash of all of the above and the value is the actual output object passed by reference.
""")

st.subheader('Example 1')

def inner_func(a, b):
    st.write("inner_func(", a, ",", b, ") ran")
    return a * b + 10

@st.cache(suppress_st_warning=True)
def expensive_computation(a, b):
    st.write("Cache miss: expensive_computation(", a, ",", b, ") ran")
    time.sleep(2)  # This makes the function take 2s to run
    return inner_func(a, b) + 1



a = 2
b = st.slider("Pick a number", 0, 10)  # 👈 Changed this
res = expensive_computation(a, b)

st.write("Result:", res)

st.markdown("""
Even though `inner_func()` is not annotated with `@st.cache`, when we edit its body we cause a “Cache miss” in the outer `expensive_computation()`.

That’s because Streamlit always traverses your code and its dependencies to verify that the cached values are still valid. This means that while developing your app you can edit your code freely without worrying about the cache. Any change you make to your app, Streamlit should do the right thing!

Streamlit is also smart enough to only traverse dependencies that belong to your app, and skip over any dependency that comes from an installed Python library.
""")

st.subheader("Example 5: Use caching to speed up your app across users")

st.markdown("""
1. If you move the slider to a number Streamlit hasn’t seen before, you’ll have a cache miss again. And every subsequent rerun with the same number will be a cache hit, of course.

2. If you move the slider back to a number Streamlit has seen before, the cache is hit and the app is fast as expected.

But now let’s go one step further! Try the following:

1. Move the slider to a number you haven’t tried before, such as 9.

2. Pretend you’re another user by opening another browser tab pointing to your Streamlit app (usually at http://localhost:8501)

3. In the new tab, move the slider to 9.

Notice how this is actually a cache hit! That is, you don’t actually see the “Cache miss” text on the second tab even though that second user never moved the slider to 9 at any point prior to this.

This happens because the Streamlit cache is global to all users. So everyone contributes to everyone else’s performance.
""")

st.markdown('---')

st.subheader('Action Points')

st.markdown("""
- All filter inputs should go into functions that then can be cached

""")



