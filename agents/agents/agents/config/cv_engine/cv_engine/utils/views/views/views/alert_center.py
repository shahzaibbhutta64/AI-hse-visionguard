import streamlit as st
from utils.event_store import get_all_events, update_event_status

def render_alert_center():
    st.title("🚨 Security Alert Center")
    st.caption("Human Verification Terminal: Review AI evidence and confirm or dismiss alerts.")
    
    events = [e for e in get_all_events() if e["status"] == "Pending"]
    
    if not events:
        st.success("🎉 Clear! No pending safety alerts requiring verification.")
        return
        
    for evt in events:
        with st.container(border=True):
            col_img, col_details = st.columns([1, 1])
            
            with col_img:
                st.image(evt["evidence_image"], caption=f"Evidence Frame: {evt['event_id']}", use_container_width=True)
                
            with col_details:
                st.error(f"### ALERT: {evt['raw_violation']}")
                st.write(f"**Camera:** {evt['camera']} | **Location:** {evt['location']}")
                st.write(f"**Timestamp:** {evt['timestamp']}")
                st.write(f"**Assessed Severity:** `{evt.get('severity', 'High')}`")
                
                with st.expander("🤖 CrewAI Multi-Agent Analysis", expanded=True):
                    st.write(evt.get("analysis_summary", "No AI analysis available."))
                    st.info(f"**Recommended Action:** {evt.get('action', 'Verify floor status.')}")
                
                st.markdown("---")
                st.write("**Human Verification Action:**")
                btn_col1, btn_col2 = st.columns(2)
                
                if btn_col1.button("✅ Confirm Violation", key=f"conf_{evt['event_id']}", type="primary"):
                    update_event_status(evt['event_id'], "Confirmed")
                    st.toast(f"Event {evt['event_id']} CONFIRMED!")
                    st.rerun()
                    
                if btn_col2.button("❌ False Alarm", key=f"false_{evt['event_id']}"):
                    update_event_status(evt['event_id'], "False Alarm")
                    st.toast(f"Event {evt['event_id']} marked as False Alarm.")
                    st.rerun()
