import streamlit as st
import duckdb
import pandas as pd
from pathlib import Path

# --- CONFIG ---
DATA_PATH = Path("/app/haystack_db/batchrecords/rqc_batch_records.feather")
st.title("🔎 Quick Search Tool")

# --- Check data existence ---
if not DATA_PATH.exists():
    st.error(f"Data file not found at: {DATA_PATH}")
    st.stop()

# --- DuckDB connection ---
@st.cache_resource
def get_duckdb_connection():
    return duckdb.connect(database=':memory:')

con = get_duckdb_connection()

# --- Load Feather into DuckDB ---
@st.cache_data
def load_data():
    # Read Feather into Pandas
    df = pd.read_feather(DATA_PATH)
    
    # Filter out unused rows
    if "Not Used" in df.columns:
        df = df[df["Not Used"] == 'False']

    # Ensure searchable columns are strings
    for col in ["lot", "RunID", "Barcode"]:
        if col in df.columns:
            df[col] = df[col].astype(str)

    # Register table in DuckDB
    con.register("batch_records", df)
    return df

df = load_data()

# --- Search input ---
search_input = st.text_input("Enter Lot, RunID, or Barcode (comma-separated for multiple):")

if st.button("Search"):
    if search_input.strip() == "":
        st.warning("Please enter at least one search term.")
    else:
        search_terms = [s.strip() for s in search_input.split(",")]

        # Build WHERE clause for DuckDB
        conditions = []
        for term in search_terms:
            term = term.replace("'", "''")  # escape quotes
            conditions.append(
                f"(lot ILIKE '%{term}%' OR RunID ILIKE '%{term}%' OR Barcode ILIKE '%{term}%')"
            )

        where_clause = " OR ".join(conditions)
        query = f"SELECT * FROM batch_records WHERE {where_clause}"

        # Execute query in DuckDB
        all_results = con.execute(query).df()

        if all_results.empty:
            st.error("No results found for any search term.")
        else:
            all_results = all_results.drop_duplicates()
            st.success(f"✅ Found {len(all_results)} matching rows")
            st.subheader("📋 Combined Search Results")
            st.dataframe(all_results)

            # --- Lot_Run field ---
            if "lot" in all_results.columns and "RunID" in all_results.columns:
                all_results["Lot_Run"] = all_results["lot"] + " - " + all_results["RunID"]

                # --- Reagent Pivot ---
                if {"Process", "Reagent Name", "Barcode"}.issubset(all_results.columns):
                    reagents_df = all_results[all_results["Process"].str.endswith("_RGT", na=False)]
                    if not reagents_df.empty:
                        reagent_pivot = (
                            reagents_df.groupby(["Reagent Name", "Lot_Run"])["Barcode"]
                            .apply(lambda x: "; ".join(x))
                            .unstack(fill_value="")
                        )
                        st.subheader("🧪 Reagents Used")
                        st.dataframe(reagent_pivot)
                    else:
                        st.info("No reagent data found for these searches.")

                # --- Equipment Pivot ---
                if {"Process", "Equipment", "Equipment ID"}.issubset(all_results.columns):
                    equipment_df = all_results[all_results["Process"].str.endswith("_INSTR", na=False)]
                    if not equipment_df.empty:
                        equipment_pivot = (
                            equipment_df.groupby(["Equipment", "Lot_Run"])["Equipment ID"]
                            .apply(lambda x: "; ".join(x))
                            .unstack(fill_value="")
                        )
                        st.subheader("🔧 Equipment Used")
                        st.dataframe(equipment_pivot)
                    else:
                        st.info("No equipment data found for these searches.")

                # --- Excel Links ---
                if "ExcelLink" in all_results.columns:
                    st.subheader("📎 ExcelLink(s):")
                    for link in all_results["ExcelLink"].dropna().unique():
                        st.write(f"- {link}")
                else:
                    st.info("No ExcelLink column found in data.")
