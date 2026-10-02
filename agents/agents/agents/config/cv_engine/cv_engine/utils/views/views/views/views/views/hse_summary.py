import streamlit as st
import pandas as pd
from utils.event_store import get_all_events, get_event_stats

def render_hse_summary():
    st.title("📊 HSE Safety Metrics")
    stats = get_event_stats()
    events = get_all_events()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Flagged Alerts", stats["total"])
    c2.metric("Confirmed Incidents", stats["confirmed"])
    c3.metric("Dismissed False Alarms", stats["false_alarms"])
    
    st.markdown("---")
    st.subheader("Violation Types Distribution")
    
    if not events:
        st.info("No data available for analytics.")
        return
        
    df = pd.DataFrame(events)
    if "raw_violation" in df.columns and not df.empty:
        counts = df["raw_violation"].value_counts()
        st.bar_chart(counts)
