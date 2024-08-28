import pandas as pd
import seaborn as sns  # pip install seaborn
import streamlit as st

from st_dataplot import ScatterPlot

df = sns.load_dataset("iris")
df["species"] = pd.Categorical(df["species"])

with st.sidebar:
    cfg = ScatterPlot.from_ui(df)

with st.container(border=False):
    fig = cfg.make_fig(df)
    cfg.display(fig, filename="iris-plot.png")

st.dataframe(df, use_container_width=True)
