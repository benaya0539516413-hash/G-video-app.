import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="מנתח נתונים מהגלריה", layout="centered")
st.title("📊 מנתח וידאו וגרפים")

# העלאת סרטון מהגלריה
uploaded_file = st.file_uploader("לחץ כאן לבחירת סרטון מהגלריה", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.video(uploaded_file)
    st.success("הסרטון נטען בהצלחה!")
    
    # יצירת נתונים לגרף (כאן יבוא הניתוח בעתיד)
    st.subheader("ניתוח מגמות")
    df = pd.DataFrame({
        'זמן (שניות)': np.arange(0, 20),
        'ערך שנמדד': np.random.normal(50, 10, 20).cumsum()
    })

    # בחירת סוג קו מגמה
    trend_option = st.selectbox("בחר סוג קו מגמה להצגה:", 
                               options=["ols", "lowess"], 
                               format_func=lambda x: "קו ישר (ליניארי)" if x=="ols" else "קו גמיש (מקומי)")

    # יצירת הגרף עם Plotly
    fig = px.scatter(df, x='זמן (שניות)', y='ערך שנמדד', 
                     trendline=trend_option, 
                     title="גרף נתונים עם קו מגמה")
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("ממתין להעלאת סרטון כדי להתחיל בניתוח...")
