import streamlit as st
import pandas as pd
import numpy as np
import cv2

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
