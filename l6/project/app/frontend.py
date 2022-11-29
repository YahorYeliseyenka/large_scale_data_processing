import streamlit as st
import requests


url = 'http://172.17.0.1:8080'
subreddits = {
    1: "AskReddit",
    2: "aww",
    3: "gaming",
    4: "funny",
    5: "science"
}

def format_func(option):
    return subreddits[option]

st.title("LSDP - Last Light")

option = st.selectbox("Subreddit", options=list(subreddits.keys()), format_func=format_func)
# st.write(f"You selected option {option} called {format_func(option)}")

input_title = st.text_input("Title", "test")


if st.button("Predict"):
    if option and input_title:
        response = requests.post(f"{url}/{input_title}/{subreddits[option]}")
        st.write(f"Over 18 -> {bool(response.json()['res'])}")