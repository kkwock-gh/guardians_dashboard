"""
TDSS Dashboard - Techdev Dashboard for Troubleshooting
A Streamlit-based dashboard application
"""

import streamlit as st


def main():
    """Main function to run the Streamlit dashboard"""
    
    # Page configuration
    st.set_page_config(
        page_title="TDSS Dashboard",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title and description
    st.title("🔧 TDSS Dashboard")
    st.markdown("### Techdev Dashboard for Troubleshooting")
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select a page:",
            ["Home", "Dashboard", "Analytics", "Settings"]
        )
    
    # Main content based on selected page
    if page == "Home":
        show_home_page()
    elif page == "Dashboard":
        show_dashboard_page()
    elif page == "Analytics":
        show_analytics_page()
    elif page == "Settings":
        show_settings_page()


def show_home_page():
    """Display the home page"""
    st.header("Welcome to TDSS Dashboard")
    
    st.markdown("""
    This is a Streamlit-based dashboard for technical troubleshooting and monitoring.
    
    **Features:**
    - 📊 Real-time monitoring dashboard
    - 📈 Analytics and insights
    - ⚙️ Customizable settings
    - 🔍 Advanced troubleshooting tools
    
    Use the sidebar to navigate between different sections.
    """)
    
    # Example metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Systems", "12", "2")
    
    with col2:
        st.metric("Alerts", "3", "-1")
    
    with col3:
        st.metric("Response Time", "245ms", "-12ms")
    
    with col4:
        st.metric("Uptime", "99.8%", "0.1%")


def show_dashboard_page():
    """Display the dashboard page"""
    st.header("Dashboard")
    
    st.info("This is the main dashboard page. Add your monitoring visualizations here.")
    
    # Example chart
    import pandas as pd
    import numpy as np
    
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=["System A", "System B", "System C"]
    )
    
    st.line_chart(chart_data)


def show_analytics_page():
    """Display the analytics page"""
    st.header("Analytics")
    
    st.info("This is the analytics page. Add your data analysis and insights here.")
    
    # Example data
    import pandas as pd
    
    data = pd.DataFrame({
        "Component": ["API", "Database", "Cache", "Frontend"],
        "Performance Score": [95, 88, 92, 90],
        "Incidents": [2, 5, 1, 3]
    })
    
    st.dataframe(data, use_container_width=True)


def show_settings_page():
    """Display the settings page"""
    st.header("Settings")
    
    st.markdown("Configure your dashboard preferences:")
    
    # Example settings
    refresh_rate = st.slider("Refresh Rate (seconds)", 5, 60, 30)
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    notifications = st.checkbox("Enable Notifications", value=True)
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")


if __name__ == "__main__":
    main()
