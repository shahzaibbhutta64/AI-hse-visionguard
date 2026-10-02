import cv2
import time
from cv_engine.camera_simulator import generate_simulated_frame

CAMERAS = {
    "CAM-01": {"name": "Production Area", "default_rule": "Missing Safety Helmet"},
    "CAM-02": {"name": "Workshop Zone", "default_rule": "Missing Safety Vest"},
    "CAM-03": {"name": "Conveyor Line", "default_rule": "Person on Conveyor"}
}

def trigger_simulated_detection(cam_id, rule_type):
    """Simulates CV detection, captures evidence frame, and returns event payload."""
    cam_info = CAMERAS.get(cam_id, {"name": "General Zone"})
    frame = generate_simulated_frame(cam_id, cam_info["name"], violation_active=True, violation_type=rule_type)
    
    # Convert OpenCV BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    event_payload = {
        "event_id": f"EVT-{int(time.time())}",
        "camera": cam_id,
        "location": cam_info["name"],
        "timestamp": time.strftime("%H:%M:%S"),
        "date": time.strftime("%Y-%m-%d"),
        "raw_violation": rule_type,
        "description": f"Computer vision detector flagged {rule_type} on {cam_id}.",
        "evidence_image": frame_rgb,
        "status": "Pending"
    }
    return event_payload
