import streamlit as st
import cv2
import sys

st.title("בדיקת מערכת - בניה")

try:
    import cv2
    st.success("OpenCV נטען בהצלחה!")
except Exception as e:
    st.error(f"שגיאה: {e}")

st.write(f"גרסת פייתון: {sys.version}")

st.divider()
st.write("אם אתה רואה את זה, האתר עובד. עכשיו אפשר להעלות את הקוד של הטרקר.")
