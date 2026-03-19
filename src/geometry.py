import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

class FaceGeometryAnalyzer:
    def __init__(self):
        self.face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )
    
    def process_image(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_image)
        return results

    def extract_metrics(self, image):
        results = self.process_image(image)
        if not results.multi_face_landmarks:
            return None
        
        landmarks = results.multi_face_landmarks[0].landmark
        h, w, _ = image.shape
        
        # Helper to get pixel coordinates
        def get_pt(idx):
            return np.array([landmarks[idx].x * w, landmarks[idx].y * h])
            
        # Key landmark indices (Mediapipe Face Mesh)
        TOP_OF_HEAD = 10
        BOTTOM_OF_CHIN = 152
        LEFT_CHEEK = 234
        RIGHT_CHEEK = 454
        LEFT_JAW = 132
        RIGHT_JAW = 361
        
        face_length = np.linalg.norm(get_pt(TOP_OF_HEAD) - get_pt(BOTTOM_OF_CHIN))
        face_width = np.linalg.norm(get_pt(LEFT_CHEEK) - get_pt(RIGHT_CHEEK))
        jaw_width = np.linalg.norm(get_pt(LEFT_JAW) - get_pt(RIGHT_JAW))
        
        # Simple face shape classification
        shape = self.classify_shape(face_length, face_width, jaw_width)
        
        # Glasses recommendation
        glasses = self.recommend_glasses(shape)
        
        # Detect if wearing glasses
        has_glasses = self.detect_glasses(image, landmarks, w, h)
        
        # Get forehead landmarks for color analysis (skin tone)
        forehead_indices = [10, 109, 67, 103, 54, 21]
        forehead_points = [get_pt(idx) for idx in forehead_indices]
        
        # Get left iris landmarks for iris color
        # In refine_landmarks, iris indices are 468-472 for left, 473-477 for right
        # We'll use 468-472 (left iris)
        if len(landmarks) > 468:
            iris_indices = [468, 469, 470, 471, 472]
            iris_points = [get_pt(idx) for idx in iris_indices]
        else:
            iris_points = []
        
        return {
            "face_shape": shape,
            "dimensions": {
                "face_length": round(face_length, 2),
                "face_width": round(face_width, 2),
                "jaw_width": round(jaw_width, 2)
            },
            "recommended_glasses": glasses,
            "has_glasses": "Yes" if has_glasses else "No",
            "iris_landmarks": iris_points,
            "skin_landmarks": forehead_points
        }
        
    def classify_shape(self, length, width, jaw):
        ratio = length / width
        if ratio > 1.4:
            return "Oblong"
        elif ratio > 1.2:
            if jaw < width * 0.8:
                return "Oval"
            else:
                return "Square"
        else:
            if jaw < width * 0.8:
                return "Heart"
            else:
                return "Round"
                
    def recommend_glasses(self, shape):
        recommendations = {
            "Oval": "Geometric, Rectangular, or Aviator frames",
            "Square": "Round or Oval frames to soften features",
            "Round": "Rectangular or Square frames to add angles",
            "Heart": "Bottom-heavy or Round frames",
            "Oblong": "Tall, Oversized, or Thick frames"
        }
        return recommendations.get(shape, "Standard Wayfarer frames")
        
    def detect_glasses(self, image, landmarks, w, h):
        """
        Heuristic for glasses detection: check for edges along the bridge of the nose.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        mask = np.zeros_like(gray)
        bridge_top = int(landmarks[168].y * h)
        bridge_bottom = int(landmarks[197].y * h)
        bridge_x = int(landmarks[168].x * w)
        
        if bridge_bottom > bridge_top:
            cv2.rectangle(mask, (bridge_x - 15, bridge_top - 10), (bridge_x + 15, bridge_bottom + 10), 255, -1)
            
        edge_zone = cv2.bitwise_and(edges, edges, mask=mask)
        edge_density = np.sum(edge_zone > 0)
        
        return edge_density > 30
