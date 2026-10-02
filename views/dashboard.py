import streamlit as st
from utils.event_store import get_event_stats, get_all_events

def render_dashboard():
    st.title("🛡️ Control Room Dashboard")
    stats = get_event_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Cameras Online", "3 / 3")
    col2.metric("Active Alerts (Pending)", stats["pending"])
    col3.metric("Confirmed Violations", stats["confirmed"])
    col4.metric("False Alarms", stats["false_alarms"])
    
    st.markdown("---")
    st.subheader("Recent Safety Events")
    events = get_all_events()
    
    if not events:
        st.info("No safety alerts recorded in session.")
        return
        
    for evt in events[:3]:
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([1, 2, 2, 1])
            c1.write(f"**{evt['event_id']}**")
            c2.write(f"📍 {evt['camera']} - {evt['location']}")
            c3.write(f"⚠️ {evt['raw_violation']}")
            status_color = "orange" if evt['status'] == "Pending" else ("red" if evt['status'] == "Confirmed" else "green")
            c4.markdown(f":{status_color}[**{evt['status']}**]")
