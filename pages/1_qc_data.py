import streamlit as st
import pandas as pd
import os
import glob

# --- CONFIG ---
BASE_PATH = "/app/haystack_db"

st.title("🪄 Haystack Database Compiler")

# --- Discover all CSVs ending with database.csv ---
csv_paths = glob.glob(os.path.join(BASE_PATH, "**/*database.csv"), recursive=True)

if not csv_paths:
    st.error(f"No CSV files ending with 'database.csv' found in {BASE_PATH}/")
    st.stop()

# --- Group CSVs by environment (TEST, DEV, PROD, etc.) ---
env_files = {}
for path in csv_paths:
    # Find which environment the file belongs to based on its parent folder
    env_name = os.path.basename(os.path.dirname(path))
    env_files.setdefault(env_name, []).append(path)

# --- Sidebar: Environment selection ---
st.sidebar.header("Select environments to include")
selected_envs = st.sidebar.multiselect(
    "Available environments:",
    sorted(env_files.keys()),
    default=sorted(env_files.keys()),
)

# --- Load & Combine Data ---
@st.cache_data
def load_data(selected_envs):
    combined = []
    for env in selected_envs:
        for path in env_files[env]:
            try:
                df = pd.read_csv(path)
                df["Environment"] = env
                df["SourceFile"] = os.path.basename(path)
                combined.append(df)
            except Exception as e:
                st.warning(f"⚠️ Failed to load {path}: {e}")
    if not combined:
        return pd.DataFrame()
    return pd.concat(combined, ignore_index=True)

# --- Display Data ---
if selected_envs:
    combined_df = load_data(selected_envs)
    if combined_df.empty:
        st.warning("No data could be loaded.")
    else:
        st.success(f"✅ Loaded {len(combined_df)} rows from {len(selected_envs)} environments.")
        st.dataframe(combined_df.head(50))

        # --- Download Button ---
        csv = combined_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Combined CSV",
            csv,
            "haystack_combined.csv",
            "text/csv",
        )
else:
    st.warning("Please select at least one environment.")
