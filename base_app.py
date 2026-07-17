import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

np.random.seed(420)

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

if st.button("Flip Coin"):
    new_flip = coin_flip()
    st.session_state.coin_list.append(new_flip)
    st.success(f"Appended {new_flip}!")

coin_df = pd.DataFrame(st.session_state.coin_list, columns=["Successes"])

cat_coin_df = coin_df.astype('category')

fig = px.bar(cat_coin_df,
             x="Successes",
             labels={"0":"Tails", "1":"Heads"})
fig.update_traces(marker_color='firebrick')

st.plotly_chart(fig)