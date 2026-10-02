import numpy as np
import cv2
import time

def generate_simulated_frame(cam_id, cam_name, violation_active=False, violation_type="None"):
    """Generates a synthetic camera feed frame with worker and zone overlays."""
    # Create dark grey industrial background (480x640)
    frame = np.full((480, 640, 3), 35, dtype=np.uint8)
    
    # Draw background elements (grid / equipment)
    cv2.rectangle(frame, (50, 100), (590, 420), (50, 50, 50), -1)
    cv2.putText(frame, f"LIVE FEED: {cam_id} - {cam_name}", (20, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (420, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    # Draw simulated worker
    worker_pos = (320, 260)
    if violation_active:
        # Bounding box red
        box_color = (0, 0, 255)
        label = f"VIOLATION: {violation_type}"
        # Red restricted zone
        cv2.rectangle(frame, (200, 180), (440, 340), (0, 0, 180), 2)
        cv2.putText(frame, "RESTRICTED AREA", (210, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    else:
        box_color = (0, 255, 0)
        label = "Worker: OK"
        cv2.rectangle(frame, (200, 180), (440, 340), (100, 100, 100), 1)
    
    # Draw person (head & body)
    cv2.circle(frame, (320, 230), 20, (220, 200, 180), -1) # Head
    cv2.rectangle(frame, (300, 250), (340, 320), (180, 100, 50), -1) # Body
    
    # Detection Box
    cv2.rectangle(frame, (280, 200), (360, 330), box_color, 2)
    cv2.putText(frame, label, (270, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
    
    return frame
