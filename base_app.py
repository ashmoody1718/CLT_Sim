import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

random.seed(420)

# Function that "flips a coin" and outputs a string of 0,1s
def coin_flip():
    is_heads = random.random() < 0.5
    return 1 if is_heads else 0

# Change this to a for loop when the user hits a button, but for now it can be like this.
# When you then automate it to speed up the process, you can make a new dataset and then
# maybe update the graph slowly by extending how much of the dataset it uses

if "coin_list" not in st.session_state:
    st.session_state.coin_list = []

st.header("Coin Flip Graph!")

@st.fragment
def flip_and_plot():
    if st.button("Flip Coin"):
        new_flip = coin_flip()
        st.session_state.coin_list.append(new_flip)
        st.success(f"Appended {new_flip}!")

    coin_df = pd.DataFrame(st.session_state.coin_list, columns=["Successes"])
    counts = coin_df['Successes'].value_counts().reindex([0, 1], fill_value=0).reset_index()
    counts.columns = ['Successes', 'Count']
    counts['Successes'] = counts['Successes'].map({0: 'Tails', 1: 'Heads'})

    fig = px.bar(counts, x='Successes', y='Count')
    fig.update_traces(marker_color='firebrick')
    fig.update_layout(
        yaxis_range=[0, 20],
        uirevision='constant'
    )

    st.plotly_chart(fig, key="coin_chart")
flip_and_plot()