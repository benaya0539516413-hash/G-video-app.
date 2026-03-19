import streamlit as st
import sys

st.title("בדיקת מערכת - בניה")

try:
    import cv2
    st.success(f"OpenCV נטען בהצלחה! גרסה: {cv2.__version__}")
except Exception as e:
    st.error(f"שגיאה בטעינת OpenCV: {e}")

st.write(f"גרסת פייתון: {sys.version}")

st.divider()
st.write("בניה, אם אתה רואה את זה - ניצחנו את הדף הלבן!")
