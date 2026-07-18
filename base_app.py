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

if "coin_s_list" not in st.session_state:
    st.session_state.coin_s_list = []

if "coin_s_temp" not in st.session_state:
    st.session_state.coin_s_temp = []

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
def coin_fig(df):
    fig = px.bar(df, x='Successes', y='Count')
    fig.update_traces(marker_color='firebrick')
    fig.update_layout(
        width=600,
        height=400,
        yaxis_range=[0, 20],
        uirevision='constant'
    )
    return fig

def coin_s_fig(l,n):
    coin_sample_df = pd.DataFrame({"Mean": l})

    fig = px.histogram(
        coin_sample_df,
        x="Mean",
        title="Sample Distribution Plot"
    )
    fig.update_traces(marker_color='firebrick',
                      xbins=dict(start=0-(1/(2*n)), end=1+(1/(2*n)), size=1/n))
    fig.update_layout(
        xaxis_range=[0, 1],  # coin flip means are always between 0 and 1
        yaxis_range=[0, 40],  # pick a ceiling generous enough for your density values
        uirevision='constant',
        width=600,
        height=400
    )
    return fig

@st.fragment
def flip_and_plot():
    # Creating button mechanism
    sample_size = 5
    if st.button("Flip Coin"):
        new_flip = coin_flip()
        st.session_state.coin_list.append(new_flip)
        st.session_state.coin_s_temp.append(new_flip)
        # st.success(f"Appended {new_flip}!")

    st.success(f"sample temp list {st.session_state.coin_s_temp}!")

    if len(st.session_state.coin_s_temp) == sample_size:
        s_mean = np.mean(st.session_state.coin_s_temp)
        st.session_state.coin_s_list.append(s_mean)
        st.session_state.coin_s_temp = []
    st.success(f"sample list {st.session_state.coin_s_list}!")

    counts = coin_count(st.session_state.coin_list)

    # Updating Plots
    coin_plot = coin_fig(counts)
    coin_s_plot = coin_s_fig(st.session_state.coin_s_list, sample_size)
    st.plotly_chart(coin_plot, key="coin_chart", use_container_width=False)
    st.plotly_chart(coin_s_plot, key="coin_sample", use_container_width=False)

flip_and_plot()