import streamlit as st

st.set_page_config(page_title="Guardians Dashboard", page_icon="🧬", layout="wide")

st.title("Guardians Dashboard")

st.markdown("""
Welcome to the **Guardians Dashboard** — your hub for Reagent QC data, batch tracking, and quick lookups.  
Use the sidebar or navigation tabs to access each section:

### Lot Search
- Search by **Lot ID** or **Reagent Name**.  
- Instantly see associated **QC Batch Record links** and **related data files**.  
- Ideal for when you just need to find “where did this lot run?” quickly.

### QC Data
- Explore **Haystack QC results** pulled from environment databases.  
- Filter by **Environment (PROD / TEST / DEV)**, **Project**, and **QC Method (Job)**.  
- Use this when investigating specific QC outputs or verifying data availability.

### Batch Records
- View and filter **QC Batch Records** by Environment, Project, and Job.  
- Review **lot-level reagent and equipment usage**.  
- Download combined batch record summaries for deeper review or tracking.

---

🧠 **Tip:**  
Each section supports filtering and CSV export. Use dropdowns on the left to refine your search — results update automatically.
""")

st.divider()
st.info("➡️ Use the sidebar to navigate between pages.")
