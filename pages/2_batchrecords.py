import streamlit as st
import pandas as pd

st.title("Reagents QC Batch Records")

# Load CSV
df = pd.read_csv("/app/haystack_db/batchrecords/rqc_batch_records.csv")
df = df[df["Not Used"] == 'False']

# --- Split project column into Environment and Project ---
df[['Environment', 'Project']] = df['project'].str.split('/', n=1, expand=True)

# --- Sidebar filters ---
with st.sidebar:
    st.header("🔍 Filter Data")

    environments = df["Environment"].dropna().unique()
    selected_environment = st.selectbox(
        "Environment (PROD/TEST/DEV)",
        [""] + sorted(environments),
        index=0,
        format_func=lambda x: x if x != "" else "Select Environment"
    )

    # Filter projects based on selected environment
    if selected_environment != "":
        available_projects = df[df["Environment"] == selected_environment]["Project"].dropna().unique()
    else:
        available_projects = df["Project"].dropna().unique()

    selected_project = st.selectbox(
        "Project",
        [""] + sorted(available_projects),
        index=0,
        format_func=lambda x: x if x != "" else "Select Project"
    )

    jobs = df["job"].dropna().unique()
    selected_job = st.selectbox(
        "Job",
        [""] + sorted(jobs),
        index=0,
        format_func=lambda x: x if x != "" else "Select QC Method"
    )

# --- Apply filters ---
filtered_df = df[
    ((df["Environment"] == selected_environment) | (selected_environment == "")) &
    ((df["Project"] == selected_project) | (selected_project == "")) &
    ((df["job"] == selected_job) | (selected_job == ""))
]

# --- Create Lot_Run field ---
filtered_df['Lot_Run'] = filtered_df['lot'].astype(str) + ' - ' + filtered_df['RunID'].astype(str)

st.subheader("📋 Filtered Data Table")
st.dataframe(filtered_df)

# --- Filter out "Choose" values for GH Part Number or Reagent Name ---
combined_df = filtered_df[
    ~filtered_df['GH Part Number'].astype(str).str.contains("Choose") &
    ~filtered_df['Reagent Name'].astype(str).str.contains("Choose")
]

# --- Create Reagent GH PN field ---
combined_df['GH_Reagent'] = combined_df['GH Part Number'].fillna('') + " - " + combined_df['Reagent Name'].fillna('')

# --- Reagent Pivot ---
# reagents_df = filtered_df[filtered_df["Process"].str.endswith("_RGT", na=False)]
# if not reagents_df.empty:
#     reagent_pivot = (
#         reagents_df.groupby(["Reagent Name", "Lot_Run"])["Barcode"]
#         .apply(lambda x: "; ".join(x.astype(str)))
#         .unstack(fill_value="")
#     )
#     st.subheader("🧪 Reagents Used")
#     st.dataframe(reagent_pivot)
# else:
#     st.info("No reagent data found for these searches.")


combined_df = combined_df[combined_df["Process"].str.endswith("_RGT", na=False) & combined_df["GH Part Number"].notna()]
if not combined_df.empty:
    combined_pivot = (
        combined_df.groupby(["GH_Reagent", "Lot_Run"])["Barcode"]
        .apply(lambda x: "; ".join(x.astype(str)))
        .unstack(fill_value="")
    )
    st.subheader("🧪 Reagents Used")
    st.dataframe(combined_pivot)
else:
    st.info("No GH Part Number + Reagent data found for these searches.")

# --- Equipment Pivot ---
equipment_df = filtered_df[filtered_df["Process"].str.endswith("_INSTR", na=False)]
if not equipment_df.empty:
    equipment_pivot = (
        equipment_df.groupby(["Equipment", "Lot_Run"])["Equipment ID"]
        .apply(lambda x: "; ".join(x.astype(str)))
        .unstack(fill_value="")
    )
    st.subheader("🔧 Equipment Used")
    st.dataframe(equipment_pivot)
else:
    st.info("No equipment data found for these searches.")
