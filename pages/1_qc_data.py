import streamlit as st
import pandas as pd
import os
import glob
import re

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
    env_name = os.path.basename(os.path.dirname(path))
    env_files.setdefault(env_name, []).append(path)

# --- Sidebar: Environment selection ---
st.sidebar.header("Select environments")
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
    df = pd.concat(combined, ignore_index=True)

    # --- Extract Project and Job from 'Output Location' ---
    def parse_output_location(val):
        if pd.isna(val):
            return (None, None)
        first_link = str(val).split(";")[0].strip()
        match = re.search(r"/Reagent_QC/([^/]+)/([^/]+)/([^/]+)/", first_link)
        if match:
            return match.group(2), match.group(3)  # Project, Job
        return (None, None)

    if "Output Location" in df.columns:
        df[["Project", "Job"]] = df["Output Location"].apply(lambda x: pd.Series(parse_output_location(x)))
    else:
        st.warning("⚠️ 'Output Location' column not found in data.")
        df["Project"] = None
        df["Job"] = None

    return df


# --- Display ---
if selected_envs:
    combined_df = load_data(selected_envs)

    if combined_df.empty:
        st.warning("No data loaded.")
        st.stop()

    # --- Sidebar: simple dropdown filters (appear only after load) ---
    with st.sidebar:
        st.header("🔍 Filter Data")

        # Projects available in the currently loaded data
        available_projects = sorted(combined_df["Project"].dropna().unique())
        selected_project = st.selectbox(
            "Project",
            [""] + available_projects,
            index=0,
            format_func=lambda x: x if x != "" else "All Projects"
        )

        # Jobs available — if a project is selected, restrict jobs to that project
        if selected_project:
            available_jobs = sorted(
                combined_df.loc[combined_df["Project"] == selected_project, "Job"].dropna().unique()
            )
        else:
            available_jobs = sorted(combined_df["Job"].dropna().unique())

        selected_job = st.selectbox(
            "Job",
            [""] + available_jobs,
            index=0,
            format_func=lambda x: x if x != "" else "All Jobs"
        )

    # --- Apply Filters (note: no Environment selectbox here; use top multiselect to control load) ---
    filtered_df = combined_df[
        ((combined_df["Project"] == selected_project) | (selected_project == "")) &
        ((combined_df["Job"] == selected_job) | (selected_job == ""))
    ]

    st.success(f"✅ Loaded {len(filtered_df)} rows after filtering.")
    st.dataframe(filtered_df.head(50), use_container_width=True)

    # --- Download Button ---
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered CSV",
        csv,
        "haystack_filtered.csv",
        "text/csv",
    )

else:
    st.warning("Please select at least one environment to load (top-left).")
