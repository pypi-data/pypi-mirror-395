import streamlit as st

st.title("Page 2")
st.write("This is the second page of your multi-page app.")

# Example content
st.header("Example Form")

with st.form("example_form"):
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=0, max_value=120)
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success(f"Hello {name}, you are {age} years old!")
