import cv2
import logging

logger = logging.getLogger(__name__)

class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
    
    def capture_frame(self):
        """Captures a single frame from the webcam."""
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            logger.error("Could not open webcam.")
            return None
        
        # Give the camera a moment to adjust exposure
        for _ in range(5):
            cap.read()
            
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            logger.error("Failed to capture frame from webcam.")
            return None
            
        return frame
