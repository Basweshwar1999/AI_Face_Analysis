import cv2
from deepface import DeepFace
from .geometry import FaceGeometryAnalyzer
from .color import analyze_skin_tone, analyze_iris_color
import logging

logger = logging.getLogger(__name__)

class FaceAnalyzer:
    def __init__(self):
        self.geometry_analyzer = FaceGeometryAnalyzer()
        
    def analyze(self, image):
        """
        Runs the full analysis pipeline on the provided BGR image.
        """
        if image is None:
            return {"error": "No image provided"}
            
        result_data = {}
        
        # 1. DeepFace Analysis (Demographics & Psychology)
        try:
            # enforce_detection=False prevents crash if face isn't perfectly detected by DeepFace backend
            df_results = DeepFace.analyze(
                img_path=image,
                actions=['age', 'gender', 'emotion'],
                enforce_detection=False 
            )
            # DeepFace returns a list of dictionaries if multiple faces are found
            if isinstance(df_results, list):
                df_result = df_results[0]
            else:
                df_result = df_results
                
            result_data['demographics'] = {
                'age': df_result.get('age', 'Unknown'),
                'gender': df_result.get('dominant_gender', df_result.get('gender', 'Unknown')),
            }
            result_data['psychology'] = {
                'dominant_emotion': df_result.get('dominant_emotion', 'Unknown')
            }
        except Exception as e:
            logger.error(f"DeepFace analysis failed: {e}")
            result_data['demographics'] = {'age': 'Unknown', 'gender': 'Unknown'}
            result_data['psychology'] = {'dominant_emotion': 'Unknown'}

        # 2. Geometry & Shape Analysis (MediaPipe)
        geo_data = self.geometry_analyzer.extract_metrics(image)
        if geo_data:
            result_data['geometry'] = {
                'face_shape': geo_data['face_shape'],
                'dimensions': geo_data['dimensions']
            }
            result_data['eyes'] = {
                'has_glasses': geo_data['has_glasses']
            }
            result_data['recommendation'] = {
                'glasses': geo_data['recommended_glasses']
            }
            
            # 3. Color Analysis
            skin_tone = analyze_skin_tone(image, geo_data['skin_landmarks'])
            iris_color = analyze_iris_color(image, geo_data['iris_landmarks'])
            
            result_data['demographics']['skin_tone'] = skin_tone
            if 'eyes' not in result_data:
                result_data['eyes'] = {}
            result_data['eyes']['iris_color'] = iris_color
        else:
            logger.warning("MediaPipe could not extract face metrics.")
            result_data['geometry'] = {'face_shape': 'Unknown', 'dimensions': 'Unknown'}
            result_data['recommendation'] = {'glasses': 'Unknown'}
            result_data['eyes'] = {'has_glasses': 'Unknown', 'iris_color': 'Unknown'}
            result_data['demographics']['skin_tone'] = 'Unknown'
            
        return result_data
