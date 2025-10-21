import streamlit as st
import pandas as pd

st.title("🔎 Quick Search Tool")

# Load default CSV
try:
    df = pd.read_csv("/app/haystack_db/batchrecords/rqc_batch_records.csv")
    df = df[df["Not Used"] == 'False']
except FileNotFoundError:
    st.error("File 'rqc_batch_records.csv' not found.")
    st.stop()

# Allow comma-separated search terms
search_input = st.text_input("Enter Lot, RunID, or Barcode (comma-separated for multiple):")

if st.button("Search"):
    if search_input.strip() == "":
        st.warning("Please enter at least one search term.")
    else:
        search_terms = [s.strip() for s in search_input.split(",")]
        all_results = pd.DataFrame()

        # Collect results for each search term
        for term in search_terms:
            term_results = df[
                df.apply(lambda row: row.astype(str).str.contains(term, case=False).any(), axis=1)
            ]
            if not term_results.empty:
                all_results = pd.concat([all_results, term_results], ignore_index=True)

        if all_results.empty:
            st.error("No results found for any search term.")
        else:
            all_results = all_results.drop_duplicates()
            st.success(f"✅ Found {len(all_results)} matching rows")
            st.subheader("📋 Combined Search Results")
            st.dataframe(all_results)

            # Create Lot_Run field
            all_results["Lot_Run"] = all_results["lot"].astype(str) + " - " + all_results["RunID"].astype(str)

            # --- Reagent Pivot ---
            reagents_df = all_results[all_results["Process"].str.endswith("_RGT", na=False)]
            if not reagents_df.empty:
                reagent_pivot = (
                    reagents_df.groupby(["Reagent Name", "Lot_Run"])["Barcode"]
                    .apply(lambda x: "; ".join(x.astype(str)))
                    .unstack(fill_value="")
                )
                st.subheader("🧪 Reagents Used")
                st.dataframe(reagent_pivot)
            else:
                st.info("No reagent data found for these searches.")

            # --- Equipment Pivot ---
            equipment_df = all_results[all_results["Process"].str.endswith("_INSTR", na=False)]
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

            # --- Excel Links ---
            if "ExcelLink" in all_results.columns:
                st.subheader("📎 ExcelLink(s):")
                for link in all_results["ExcelLink"].dropna().unique():
                    st.write(f"- {link}")
            else:
                st.info("No ExcelLink column found in data.")
