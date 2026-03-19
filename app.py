import streamlit as st
import cv2
import numpy as np


st.set_page_config(page_title="מערכת ניתוח פיזיקלית", layout="wide")

st.title("📊 ניתוח תנועה ומדידה (עם כיול)")

# תפריט צד להגדרות פיזיקליות
st.sidebar.header("⚙️ הגדרות כיול ומדידה")
calibration_m = st.sidebar.number_input("אורך מוט כיול (מטרים):", min_value=0.01, value=1.0, step=0.1)
pixel_width = st.sidebar.number_input("כמה פיקסלים המוט תופס?", min_value=1, value=100)

# חישוב יחס המרה (מטר לכל פיקסל)
m_per_pixel = calibration_m / pixel_width

uploaded_file = st.file_uploader("העלה סרטון לניתוח (MP4)", type=["mp4", "mov"])

if uploaded_file is not None:
    st.video(uploaded_file)
    
    st.success(f"הגדרת כיול: כל פיקסל שווה ל-{m_per_pixel:.4f} מטרים")
    
    # כאן יבוא העיבוד של OpenCV (אנחנו נדמה כרגע תנועה שממירה פיקסלים למטרים)
    st.subheader("📈 גרף מקום-זמן (מטרים)")
    
    # יצירת ציר זמן
    t = np.linspace(0, 10, 100)
    # נניח שהאובייקט זז 5 פיקסלים בכל פריים
    pixels_y = 5 * t**2
    meters_y = pixels_y * m_per_pixel
    
    chart_data = pd.DataFrame({
        'זמן (שניות)': t,
        'מיקום (מטרים)': meters_y
    })
    
    st.line_chart(chart_data.set_index('זמן (שניות)'))
    
    st.info("בשלב הבא נוסיף את המעקב האוטומטי אחרי נקודת צבע בסרטון.")
else:
    st.info("אנא העלה סרטון והגדר את אורך מוט הכיול בצד.")
import streamlit as st
import cv2
import numpy as np
import pandas as pd
import tempfile

st.set_page_config(page_title="מערכת ניתוח תנועה", layout="wide")
st.title("📏 מעקב אוטומטי ומדידה פיזיקלית")

# תפריט כיול
st.sidebar.header("⚙️ הגדרות כיול")
m_length = st.sidebar.number_input("אורך מוט כיול (מטרים):", min_value=0.1, value=1.0)
pixel_dist = st.sidebar.number_input("מרחק בפיקסלים:", min_value=1, value=100)
m_per_pixel = m_length / pixel_dist

uploaded_file = st.file_uploader("העלה סרטון לניתוח", type=["mp4", "mov"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    positions = []
    
    # עיבוד הסרטון - זיהוי תנועה בסיסי
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        # המרה ל-HSV כדי לזהות צבע (למשל כדור אדום/כתום)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_color = np.array([0, 120, 70])
        upper_color = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_color, upper_color)
        
        # מציאת מרכז הכובד של האובייקט
        M = cv2.moments(mask)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            positions.append(cy) # עוקב אחרי ציר ה-Y (נפילה חופשית למשל)

    cap.release()
    
    if positions:
        # חישוב נתונים פיזיקליים
        time = np.arange(len(positions)) / fps
        dist_meters = (np.array(positions) - positions[0]) * m_per_pixel
        
        df = pd.DataFrame({"זמן (שניות)": time, "מיקום (מטרים)": dist_meters})
        st.line_chart(df.set_index("זמן (שניות)"))
        st.success("הניתוח הושלם בהצלחה!")
