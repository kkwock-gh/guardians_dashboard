import streamlit as st
import pandas as pd
import os
import glob

# --- CONFIG ---
BASE_PATH = "/screening/scratch/kkwock/haystack_db"

st.title("🪄 Haystack Database Compiler")

# --- Discover CSVs ---
csv_paths = glob.glob(os.path.join(BASE_PATH, "**/*database.csv"), recursive=True)

if not csv_paths:
    st.error("No CSV files ending with 'database.csv' found in haystack_db/")
    st.stop()

# Extract environment names based on folder structure
env_files = {}
for path in csv_paths:
    env_name = os.path.basename(os.path.dirname(path))  # folder name = environment
    env_files[env_name] = path

# --- User Selection ---
st.sidebar.header("Select environments to include")
selected_envs = st.sidebar.multiselect(
    "Available environments:", list(env_files.keys()), default=list(env_files.keys())
)

# --- Load & Combine ---
@st.cache_data
def load_data(env_selection):
    dfs = []
    for env in env_selection:
        path = env_files[env]
        df = pd.read_csv(path)
        df["Environment"] = env
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

if selected_envs:
    combined_df = load_data(selected_envs)
    st.success(f"Loaded {len(combined_df)} rows from {len(selected_envs)} environments.")

    # --- Show sample ---
    st.dataframe(combined_df.head(50))

    # --- Download combined CSV ---
    csv = combined_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Combined CSV",
        csv,
        "haystack_combined.csv",
        "text/csv",
    )
else:
    st.warning("Please select at least one environment.")
