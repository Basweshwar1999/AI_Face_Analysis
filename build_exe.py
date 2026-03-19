import PyInstaller.__main__
import os
import streamlit
import mediapipe

# Streamlit relies on static web files (HTML/CSS/JS) tightly coupled to its source.
streamlit_static_dir = os.path.join(os.path.dirname(streamlit.__file__), "static")

# MediaPipe relies on hard-coded .tflite ML models stored inside its modules directory.
mediapipe_modules_dir = os.path.join(os.path.dirname(mediapipe.__file__), "modules")

print(f"Bundling Streamlit Static Files from: {streamlit_static_dir}")
print(f"Bundling MediaPipe Models from: {mediapipe_modules_dir}")

PyInstaller.__main__.run([
    'run_main.py',
    '--name=AI_Face_Analysis',
    '--noconfirm',
    '--onedir',          # Output to a folder (much faster startup time compared to a single massive .exe)
    '--console',         # Keep the console visible so the server can log, otherwise Streamlit crashes
    
    # Critical UI and ML Model Data Files
    f'--add-data={streamlit_static_dir};streamlit/static',
    f'--add-data={mediapipe_modules_dir};mediapipe/modules',
    
    # Application Source Code
    '--add-data=app.py;.',
    '--add-data=src;src',
    
    # Metadata required by DeepFace and Streamlit dependencies
    '--copy-metadata=streamlit',
    '--copy-metadata=fpdf2',
    '--copy-metadata=deepface',
    '--copy-metadata=tqdm',
    
    # Forcing explicit imports for dynamic libraries
    '--hidden-import=streamlit',
    '--hidden-import=cv2',
    '--hidden-import=deepface',
    '--hidden-import=mediapipe',
    '--hidden-import=numpy',
    '--hidden-import=pandas',
])
