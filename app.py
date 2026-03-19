import streamlit as st
import cv2
import numpy as np
import os
from src.camera import Camera
from src.analyzer import FaceAnalyzer
from src.reporter import generate_report

st.set_page_config(page_title="AI Face Analysis", page_icon="🕵️", layout="wide")

st.title("AI Face Analysis & Reporting System 🕵️‍♀️")
st.write("Live scan and deep analysis using OpenCV, DeepFace, and MediaPipe.")

@st.cache_resource
def get_analyzer():
    return FaceAnalyzer()

analyzer = get_analyzer()

col1, col2 = st.columns(2)

with col1:
    st.header("1. Capture")
    # Streamlit native camera is excellent for web.
    # We also include a button to use our custom local opencv script if preferred.
    use_native = st.checkbox("Use Streamlit Native Camera Widget", value=True)
    
    image_bgr = None
    
    if use_native:
        picture = st.camera_input("Take a picture")
        if picture:
            bytes_data = picture.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            image_bgr = cv2_img
    else:
        st.info("Click below to capture a frame from your local webcam (Index 0).")
        if st.button("Trigger Scan (OpenCV)", type="primary"):
            with st.spinner("Opening local webcam..."):
                cam = Camera()
                image_bgr = cam.capture_frame()
                if image_bgr is not None:
                    st.success("Captured successfully!")
                    
    # Display the captured image if we used the local OpenCV capture
    if not use_native and image_bgr is not None:
        st.image(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)

with col2:
    st.header("2. Analysis & Report")
    
    if image_bgr is not None:
        if st.button("Run Deep Analysis", type="primary", use_container_width=True):
            with st.spinner("Analyzing Demographics, Geometry, Colors, and Psychology..."):
                # We save this in session state so it persists if the app reruns (e.g. for generating report)
                st.session_state['last_results'] = analyzer.analyze(image_bgr)
                
    if 'last_results' in st.session_state:
        results = st.session_state['last_results']
        if "error" in results:
            st.error(results["error"])
        else:
            st.write("### Analysis Results")
            
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Demographics", "Geometry", "Eyes", "Psychology", "Recommendation"])
            
            with tab1:
                st.json(results.get('demographics', {}))
            with tab2:
                st.json(results.get('geometry', {}))
            with tab3:
                st.json(results.get('eyes', {}))
            with tab4:
                st.json(results.get('psychology', {}))
            with tab5:
                st.success(f"Best Suited Glasses: {results.get('recommendation', {}).get('glasses', 'Unknown')}")
                
            st.markdown("---")
            st.subheader("3. Download PDF Report")
            
            report_path = "face_analysis_report.pdf"
            
            # Button to generate the PDF
            if st.button("Generate PDF Report", use_container_width=True):
                with st.spinner("Generating PDF..."):
                    generate_report(results, report_path)
                
                with open(report_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_file,
                        file_name="AI_Face_Analysis_Report.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
