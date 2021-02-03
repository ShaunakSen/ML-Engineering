import streamlit as st
import copy
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

st.subheader('Example 6: Mutating cached values')

@st.cache(suppress_st_warning=True)
def expensive_computation2(a, b):
    st.write("Cache miss: expensive_computation(", a, ",", b, ") ran")
    time.sleep(2)  # This makes the function take 2s to run
    return {"output": a * b}  # 👈 Mutable object

a = 2
b = 21
res = expensive_computation2(a, b)

st.write("Result:", res)

### create a new copy before muatating
res_copy = copy.deepcopy(res)

res_copy["output"] = "result was manually mutated"  # 👈 Mutated cached value

st.write("Mutated result:", res_copy)

st.code("""
@st.cache(suppress_st_warning=True)
def expensive_computation(a, b):
    st.write("Cache miss: expensive_computation(", a, ",", b, ") ran")
    time.sleep(2)  # This makes the function take 2s to run
    return {"output": a * b}  # 👈 Mutable object

a = 2
b = 21
res = expensive_computation(a, b)

st.write("Result:", res)

res["output"] = "result was manually mutated"  # 👈 Mutated cached value

st.write("Mutated result:", res)
""")

st.markdown("""
When you run this app for the first time, you should see three messages on the screen:
- Cache miss (…)
- Result: {output: 42}
- Mutated result: {output: “result was manually mutated”}

No surprises here. But now notice what happens when you rerun you app (i.e. press R):

- Result: {output: “result was manually mutated”}
- Mutated result: {output: “result was manually mutated”}
- Cached object mutated. (…)

What’s going on here is that Streamlit caches the output res by reference. When you mutated res["output"] outside the cached function you ended up inadvertently modifying the cache. This means every subsequent call to expensive_computation(2, 21) will return the wrong value!

Since this behavior is usually not what you’d expect, Streamlit tries to be helpful and show you a warning, along with some ideas about how to fix your code.

In this specific case, the fix is just to not mutate res["output"] outside the cached function. There was no good reason for us to do that anyway! Another solution would be to clone the result value with res = deepcopy(expensive_computation(2, 21)). Check out the section entitled Fixing caching issues for more information on these approaches and more.

""")

st.subheader('Advanced caching: The algorithm under the hood')

st.markdown("""
The cache is a key-value store, where the __key__ is a hash of:

- The input parameters that you called the function with
- The value of any external variable used in the function
- The body of the function
- The body of any function used inside the cached function


And the value is a tuple of:

- The cached output
- A hash of the cached output (you’ll see why soon)

For both the key and the output hash, Streamlit uses a specialized hash function that knows how to traverse code, hash special objects, and can have its behavior customized by the user.

For example, when the function `expensive_computation(a, b)`, decorated with `@st.cache`, is executed with `a=2 and b=21`, Streamlit does the following:
1. Computes the cache key
2. If the key is found in the cache, then:
    - Extracts the previously-cached `(output, output_hash)` tuple.
    - Performs an __Output Mutation Check__, where a fresh hash of the output is computed and compared to the stored `output_hash`. This is why we need the `output_hash`
        - If the two hashes are different, shows a __Cached Object Mutated__ warning. (Note: Setting `allow_output_mutation=True` disables this step).
3. If the input key is not found in the cache, then:
    - Executes the cached function (i.e. `output = expensive_computation(2, 21)`).
    - Calculates the `output_hash` from the function’s `output`.
    - Stores `key → (output, output_hash)` in the cache.
4. Returns the output.

If an error is encountered an exception is raised. If the error occurs while hashing either the key or the output an __UnhashableTypeError__ error is thrown. If you run into any issues, see fixing caching issues.


""")


st.markdown('---')

st.subheader('Action Points')

st.markdown("""
- All filter inputs should go into functions that then can be cached

""")



