import streamlit as st
import pandas as pd

def init_event_store():
    if "events" not in st.session_state:
        st.session_state["events"] = []

def add_event(event):
    init_event_store()
    st.session_state["events"].insert(0, event)

def get_all_events():
    init_event_store()
    return st.session_state["events"]

def update_event_status(event_id, new_status):
    init_event_store()
    for evt in st.session_state["events"]:
        if evt["event_id"] == event_id:
            evt["status"] = new_status
            break

def get_event_stats():
    init_event_store()
    events = st.session_state["events"]
    total = len(events)
    pending = sum(1 for e in events if e["status"] == "Pending")
    confirmed = sum(1 for e in events if e["status"] == "Confirmed")
    false_alarms = sum(1 for e in events if e["status"] == "False Alarm")
    
    return {
        "total": total,
        "pending": pending,
        "confirmed": confirmed,
        "false_alarms": false_alarms
    }
