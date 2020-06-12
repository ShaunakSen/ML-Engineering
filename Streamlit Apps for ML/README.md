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