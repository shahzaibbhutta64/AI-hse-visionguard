import streamlit as st
from cv_engine.camera_simulator import generate_simulated_frame
from cv_engine.detector import trigger_simulated_detection, CAMERAS
from config.crew_config import run_hse_crew
from utils.event_store import add_event

def render_monitoring():
    st.title("📹 Live Camera Streams & CV Simulation")
    st.caption("Simulate real-time computer vision rule triggers to evaluate multi-agent reasoning.")
    
    cols = st.columns(3)
    for idx, (cam_id, info) in enumerate(CAMERAS.items()):
        with cols[idx]:
            st.subheader(f"{cam_id}")
            st.caption(f"Location: {info['name']}")
            
            # Display simulated standard feed
            frame = generate_simulated_frame(cam_id, info['name'])
            st.image(frame, channels="RGB", use_container_width=True)
            
            violation_type = st.selectbox(
                "Simulate Violation",
                ["Missing Safety Helmet", "Missing Safety Vest", "Person on Conveyor", "Restricted Zone Entry"],
                key=f"select_{cam_id}"
            )
            
            if st.button(f"⚡ Trigger Violation on {cam_id}", key=f"btn_{cam_id}"):
                with st.spinner("CV Detection triggered! Running CrewAI analysis..."):
                    # 1. Computer Vision Detection Payload
                    event_payload = trigger_simulated_detection(cam_id, violation_type)
                    
                    # 2. CrewAI Multi-Agent Execution
                    agent_results = run_hse_crew(event_payload)
                    
                    # 3. Combine & Store
                    event_payload.update(agent_results)
                    add_event(event_payload)
                    
                    st.success(f"Alert generated for {cam_id}! Sent to Security Control Room.")
