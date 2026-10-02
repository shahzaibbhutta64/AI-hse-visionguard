import streamlit as st
from utils.event_store import init_event_store
from views.dashboard import render_dashboard
from views.monitoring import render_monitoring
from views.alert_center import render_alert_center
from views.event_history import render_event_history
from views.hse_summary import render_hse_summary

# Page setup
st.set_page_config(
    page_title="VisionGuard AI - HSE Surveillance",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Session Storage
init_event_store()

# Sidebar Navigation
st.sidebar.title("🛡️ VisionGuard AI")
st.sidebar.caption("Workplace Safety Surveillance")

page = st.sidebar.radio(
    "Navigation",
    [
        "1. Control Dashboard",
        "2. Camera Monitoring",
        "3. Security Alert Center",
        "4. Event History",
        "5. HSE Analytics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("**Security Status:** Online\n**Model:** groq/openai/gpt-oss-20b")

# Route Page Rendering
if page == "1. Control Dashboard":
    render_dashboard()
elif page == "2. Camera Monitoring":
    render_monitoring()
elif page == "3. Security Alert Center":
    render_alert_center()
elif page == "4. Event History":
    render_event_history()
elif page == "5. HSE Analytics":
    render_hse_summary()
