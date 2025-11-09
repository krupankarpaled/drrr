import cv2
import streamlit as st
import mediapipe as mp
import numpy as np
import time

# Streamlit config
st.set_page_config(page_title="Drowsiness Detection Dashboard", layout="wide")

# Custom dark UI
st.markdown("""
    <style>
        body { background-color: #0e1117; color: white; }
        [data-testid="stSidebar"] { background-color: #1a1c23; }
        h1, h2, h3 { color: #58a6ff; }
        .stAlert { border-radius: 12px; font-size: 18px; }
        .metric-container {
            background-color: #161a25;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.4);
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'closed_start' not in st.session_state:
    st.session_state.closed_start = None
if 'alerted' not in st.session_state:
    st.session_state.alerted = False
if 'last_ear' not in st.session_state:
    st.session_state.last_ear = 0.0

# Sidebar
st.sidebar.title("⚙️ Detection Settings")
EAR_THRESHOLD = st.sidebar.slider("EAR Threshold", 0.15, 0.35, 0.25, 0.01)
EYE_CLOSED_SECONDS = st.sidebar.slider("Closed-Eye Duration (s)", 1.0, 4.0, 2.0, 0.1)
st.sidebar.markdown("---")
st.sidebar.info("👁️ Lower EAR = stricter detection.\nIncrease duration for more tolerance.")

# Header
st.markdown("<h1 style='text-align:center;'>😴 Drowsiness Detection Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Real-time drowsiness detection using OpenCV, MediaPipe & Streamlit.</p>", unsafe_allow_html=True)
st.markdown("---")

# Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Eye landmarks
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# EAR function
def eye_aspect_ratio(landmarks, eye_indices):
    try:
        p = np.array([[landmarks[i][0], landmarks[i][1]] for i in eye_indices])
        A = np.linalg.norm(p[1] - p[5])
        B = np.linalg.norm(p[2] - p[4])
        C = np.linalg.norm(p[0] - p[3])
        EAR = (A + B) / (2.0 * C)
        return EAR
    except:
        return None

# Process frame function
def process_frame(frame, ear_threshold, eye_closed_seconds):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)
    
    EAR = None
    status = "No face detected"
    status_color = "#888888"
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            landmarks = [(lm.x * w, lm.y * h) for lm in face_landmarks.landmark]
            
            left_EAR = eye_aspect_ratio(landmarks, LEFT_EYE)
            right_EAR = eye_aspect_ratio(landmarks, RIGHT_EYE)
            
            if left_EAR is not None and right_EAR is not None:
                EAR = (left_EAR + right_EAR) / 2.0
                st.session_state.last_ear = EAR
                
                # Draw eye landmarks
                mp_drawing.draw_landmarks(
                    frame_rgb, 
                    face_landmarks, 
                    mp_face_mesh.FACEMESH_CONTOURS,
                    None,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                )
                
                # Drowsiness detection
                if EAR < ear_threshold:
                    if st.session_state.closed_start is None:
                        st.session_state.closed_start = time.time()
                    elif time.time() - st.session_state.closed_start >= eye_closed_seconds:
                        if not st.session_state.alerted:
                            status = "🚨 Drowsy Detected!"
                            status_color = "#ff4b4b"
                            st.session_state.alerted = True
                            st.sidebar.warning("⚠️ Drowsiness Alert!")
                        else:
                            status = "🚨 Drowsy Detected!"
                            status_color = "#ff4b4b"
                    else:
                        elapsed = time.time() - st.session_state.closed_start
                        status = f"⚠️ Eyes closing ({elapsed:.1f}s)"
                        status_color = "#ffaa00"
                else:
                    st.session_state.closed_start = None
                    st.session_state.alerted = False
                    status = "✅ Awake"
                    status_color = "#00ff88"
            else:
                EAR = st.session_state.last_ear
                status = "Face detected"
                status_color = "#888888"
    
    return frame_rgb, EAR, status, status_color

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    # Use Streamlit's camera input for webcam access
    img_file_buffer = st.camera_input("Take a picture or use webcam", key="camera")
    
    if img_file_buffer is not None:
        # Convert the image buffer to a numpy array
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        
        # Process the frame
        processed_frame, EAR, status, status_color = process_frame(
            cv2_img, 
            EAR_THRESHOLD, 
            EYE_CLOSED_SECONDS
        )
        
        # Display processed frame
        st.image(processed_frame, channels="RGB", use_container_width=True)
        
        # Update metrics in column 2
        with col2:
            st.markdown("<div class='metric-container'><h3>Eye Aspect Ratio (EAR)</h3>", unsafe_allow_html=True)
            if EAR is not None:
                st.metric(label="", value=f"{EAR:.3f}")
            else:
                st.metric(label="", value="N/A")
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='metric-container'><h3>Status</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:{status_color}; font-size:20px;'>{status}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        with col2:
            st.markdown("<div class='metric-container'><h3>Eye Aspect Ratio (EAR)</h3>", unsafe_allow_html=True)
            st.metric(label="", value="Waiting...")
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='metric-container'><h3>Status</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color:#888888; font-size:20px;'>⏳ Ready</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.info("👆 Click the camera button above to start detection")

# Instructions and reset
st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Instructions")
st.sidebar.markdown("""
1. Click the camera button to capture an image
2. The app will detect your face and analyze eye aspect ratio
3. Adjust thresholds in the sidebar for sensitivity
4. For continuous detection, take multiple photos
""")
if st.sidebar.button("🔄 Reset Detection State"):
    st.session_state.closed_start = None
    st.session_state.alerted = False
    st.session_state.last_ear = 0.0
    st.sidebar.success("State reset!")
    st.rerun()
