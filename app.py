import streamlit as st

st.set_page_config(
    page_title="TDSS Dashboard",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🔧 TDSS Dashboard")
st.markdown("### Techdev Dashboard for Troubleshooting")

st.markdown("""
Welcome to the **TDSS Dashboard**!

**Features:**
- 📊 Real-time monitoring dashboard  
- 📈 Analytics and insights  
- ⚙️ Customizable settings  
- 🪄 Haystack Database Compiler  
- 🔍 Advanced troubleshooting tools  

""")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Active Systems", "12", "2")
with col2:
    st.metric("Alerts", "3", "-1")
with col3:
    st.metric("Response Time", "245ms", "-12ms")
with col4:
    st.metric("Uptime", "99.8%", "0.1%")
