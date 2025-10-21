import streamlit as st
import pandas as pd

st.title("📚 Database Explorer")

# Load CSV
df = pd.read_csv("/screening/scratch/kkwock/haystack_db/rqc_batch_records.csv")
df = df[df["Not Used"] == 'False']

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Data")
    projects = df["project"].dropna().unique()
    selected_project = st.multiselect("Project", sorted(projects), sorted(projects))
    jobs = df["job"].dropna().unique()
    selected_job = st.multiselect("Job", sorted(jobs), sorted(jobs))

# Apply filters
filtered_df = df[
    (df["project"].isin(selected_project)) &
    (df["job"].isin(selected_job))
]

filtered_df['Lot_Run'] = filtered_df['lot'].astype(str) + ' - ' + filtered_df['RunID'].astype(str)

st.subheader("📋 Filtered Data Table")
st.dataframe(filtered_df)

# --- Main Pivot ---
filtered_for_pivot = filtered_df[filtered_df["GH Part Number"].astype(str).str.startswith("GH")]
pivot_table = (
    filtered_for_pivot.groupby(["GH Part Number", "Lot_Run"])["Barcode"]
    .apply(lambda x: "; ".join(x.astype(str)))
    .unstack(fill_value="")
)

operator_row = (
    filtered_df.groupby("Lot_Run")["operator"].first().to_frame().T
)
operator_row.index = ["operator"]

final_pivot = pd.concat([pivot_table, operator_row], axis=0)

st.subheader("📌 GH Part Number vs Lot (Barcodes)")
st.dataframe(final_pivot)

# --- Reagent Table ---
reagents_df = filtered_df[filtered_df["Process"].str.endswith("_RGT", na=False)]
reagent_pivot = (
    reagents_df.groupby(["Reagent Name", "Lot_Run"])["Barcode"]
    .apply(lambda x: "; ".join(x))
    .unstack(fill_value="")
)
st.subheader("🧪 Reagents Used")
st.dataframe(reagent_pivot)

# --- Equipment Table ---
equipment_df = filtered_df[filtered_df["Process"].str.endswith("_INSTR", na=False)]
equipment_pivot = (
    equipment_df.groupby(["Equipment", "Lot_Run"])["Equipment ID"]
    .apply(lambda x: "; ".join(x))
    .unstack(fill_value="")
)
st.subheader("🔧 Equipment Used")
st.dataframe(equipment_pivot)
