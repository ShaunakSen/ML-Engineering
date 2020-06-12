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