import streamlit as st
import sys

st.title("בדיקת מערכת")
try:
    import cv2
    st.write("OpenCV נטען בהצלחה")
except Exception as e:
    st.error(f"שגיאה בטעינת OpenCV: {e}")

st.write(f"גרסת פייתון: {sys.version}")
