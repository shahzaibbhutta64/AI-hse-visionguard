import streamlit as st
import pandas as pd
from utils.event_store import get_all_events

def render_event_history():
    st.title("📋 Event History")
    events = get_all_events()
    
    if not events:
        st.info("No recorded events in log history.")
        return
        
    # Filters
    col1, col2 = st.columns(2)
    status_filter = col1.multiselect("Filter by Status", ["Pending", "Confirmed", "False Alarm"], default=["Pending", "Confirmed", "False Alarm"])
    
    filtered_events = [e for e in events if e["status"] in status_filter]
    
    for evt in filtered_events:
        with st.expander(f"[{evt['status']}] {evt['event_id']} - {evt['camera']} ({evt['raw_violation']}) @ {evt['timestamp']}"):
            c1, c2 = st.columns([1, 2])
            c1.image(evt["evidence_image"], use_container_width=True)
            c2.write(f"**Location:** {evt['location']}")
            c2.write(f"**Date/Time:** {evt['date']} {evt['timestamp']}")
            c2.write(f"**Violation Type:** {evt['raw_violation']}")
            c2.write(f"**Severity:** {evt.get('severity', 'N/A')}")
            c2.write(f"**AI Summary:** {evt.get('analysis_summary', 'N/A')}")
