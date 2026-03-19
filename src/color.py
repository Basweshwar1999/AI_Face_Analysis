import cv2
import numpy as np

def get_average_color(image, mask):
    """
    Returns the average BGR color of the image within the given mask.
    """
    mean_val = cv2.mean(image, mask=mask)
    return mean_val[:3]  # Return B, G, R

def analyze_skin_tone(image, landmarks=None):
    """
    Analyzes skin tone using average HSV.
    """
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, w = image.shape[:2]
    
    mask = np.zeros((h, w), dtype=np.uint8)
    
    if landmarks is None or len(landmarks) == 0:
        # Generic cheek estimation
        cv2.rectangle(mask, (int(w*0.3), int(h*0.5)), (int(w*0.4), int(h*0.7)), 255, -1)
        cv2.rectangle(mask, (int(w*0.6), int(h*0.5)), (int(w*0.7), int(h*0.7)), 255, -1)
    else:
        # Use provided landmarks
        points = np.array(landmarks, dtype=np.int32)
        cv2.fillPoly(mask, [points], 255)
    
    mean_hsv = cv2.mean(hsv_image, mask=mask)[:3]
    h_val, s_val, v_val = mean_hsv
    
    # Basic skin tone heuristic based on Value (Brightness)
    if v_val > 200:
        return "Fair"
    elif v_val > 150:
        return "Medium"
    elif v_val > 100:
        return "Olive/Tan"
    else:
        return "Dark"

def analyze_iris_color(image, eye_landmarks=None):
    """
    Analyzes the color of the iris.
    Requires eye landmarks to mask the iris region.
    """
    if eye_landmarks is None or len(eye_landmarks) == 0:
        return "Unknown"
        
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    points = np.array(eye_landmarks, dtype=np.int32)
    cv2.fillPoly(mask, [points], 255)
    
    mean_bgr = get_average_color(image, mask)
    b, g, r = mean_bgr
    
    # Dominant color heuristic
    if b > g + 20 and b > r + 20:
        return "Blue"
    elif g > b + 10 and g > r + 10:
        return "Green"
    elif r > b and r > g and (r - g) > 20:
        return "Hazel/Light Brown"
    elif r > b and g > b and abs(r - g) < 20:
        return "Hazel"
    else:
        return "Dark Brown"
