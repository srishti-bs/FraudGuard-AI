import os
import gdown
import pandas as pd
import streamlit as st

FILE_ID = "1QX2rdLVtxBeNuVhs7fvhCHX-Ukub4reh"
CSV_NAME = "creditcard.csv"

@st.cache_data
def load_dataset():
    if not os.path.exists(CSV_NAME):
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, CSV_NAME, quiet=False)

    return pd.read_csv(CSV_NAME)