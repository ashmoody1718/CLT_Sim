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

#Creating count dataframe for plotting
def coin_count(l):
    # Coin distribution
    coin_df = pd.DataFrame(l, columns=["Successes"])
    counts = coin_df['Successes'].value_counts().reindex([0, 1], fill_value=0).reset_index()
    counts.columns = ['Successes', 'Count']
    counts['Successes'] = counts['Successes'].map({0: 'Tails', 1: 'Heads'})
    return counts

# Plotting count dataframe
def coin_fig(c):
    fig = px.bar(c, x='Successes', y='Count')
    fig.update_traces(marker_color='firebrick')
    fig.update_layout(
        width=600,
        height=400,
        yaxis_range=[0, 20],
        uirevision='constant'
    )
    return fig

@st.fragment
def flip_and_plot():
    # Creating button mechanism
    if st.button("Flip Coin"):
        new_flip = coin_flip()
        st.session_state.coin_list.append(new_flip)
        st.success(f"Appended {new_flip}!")

    counts = coin_count(st.session_state.coin_list)

    # Updating Plots
    coin_plot = coin_fig(counts)
    st.plotly_chart(coin_plot, key="coin_chart", use_container_width=False)
flip_and_plot()