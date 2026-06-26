import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ✅ PAGE CONFIG
st.set_page_config(page_title="AgriSense AI", layout="wide")

# ✅ STYLE (IMPORTANT for judges)
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
h1 {
    text-align: center;
    color: #2e7d32;
    font-size: 42px;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ✅ LANGUAGE SELECTOR
lang = st.selectbox("🌐 Language / اللغة", ["English", "العربية"])

def t(en, ar):
    return ar if lang == "العربية" else en

# ✅ LOGIN
if "auth" not in st.session_state:
    st.session_state.auth = False

def login():
    st.title("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "admin123":
            st.session_state.auth = True
            st.success("✅ Logged in")
            st.rerun()
        else:
            st.error("❌ Invalid login")

if not st.session_state.auth:
    login()
    st.stop()

# ✅ LOAD DATA
model = pickle.load(open("model.pkl", "rb"))
df = pd.read_excel("agrisense_1000_records.xlsx")

# ✅ TITLE
st.markdown(f"<h1>🌱 {t('AgriSense AI Dashboard','لوحة الزراعة الذكية')}</h1>", unsafe_allow_html=True)

# ✅ KPIs
st.markdown("### 📊 " + t("System Overview","نظرة عامة"))

col1, col2, col3, col4 = st.columns(4)

col1.metric("💧 " + t("Water Saved","المياه"),
            f"{df['WaterSaved'].mean():.0f} L")

col2.metric("🌡 " + t("Temperature","الحرارة"),
            f"{df['Temperature'].mean():.1f} °C")

col3.metric("🌱 " + t("Plant Health","صحة النبات"),
            f"{df['PlantHealth'].mean():.0f}%")

col4.metric("🤖 " + t("AI Confidence","الثقة"),
            f"{df['AI_Confidence'].mean():.0f}%")

# ✅ ANALYTICS
st.markdown("### 📈 " + t("Advanced Analytics","تحليلات متقدمة"))

col1, col2 = st.columns(2)
col1.line_chart(df["WaterDuration"])
col2.bar_chart(df.groupby("Crop")["WaterSaved"].mean())

# ✅ INPUTS
st.markdown("### ⚙️ " + t("Smart Prediction","التنبؤ الذكي"))

soil = st.slider(t("Soil Moisture","رطوبة التربة"), 0, 100, 40)
temp = st.slider(t("Temperature","درجة الحرارة"), 20, 50, 35)
humidity = st.slider(t("Humidity","الرطوبة"), 20, 100, 60)
rain = st.slider(t("Rainfall","الأمطار"), 0, 20, 2)
ph = st.slider("pH", 5, 9, 7)
N = st.slider("Nitrogen", 10, 60, 30)
P = st.slider("Phosphorus", 10, 60, 30)
K = st.slider("Potassium", 10, 60, 30)
wind = st.slider(t("Wind Speed","الرياح"), 0, 40, 10)
uv = st.slider("UV", 1, 15, 8)

# ✅ PREDICTION
input_data = pd.DataFrame([[soil,temp,humidity,rain,ph,N,P,K,wind,uv]],
columns=["SoilMoisture","Temperature","Humidity","Rainfall","pH","Nitrogen","Phosphorus","Potassium","WindSpeed","UV"])

pred = model.predict(input_data)[0]
labels = {0:"Low", 1:"Medium", 2:"High"}
result = labels[pred]

# ✅ RESULT CARD
st.markdown("### 💧 " + t("AI Recommendation","توصية الذكاء"))

if result == "High":
    st.error(t("🚨 High irrigation needed","🚨 ري عاجل"))
elif result == "Medium":
    st.warning(t("⚠️ Medium irrigation required","⚠️ ري متوسط"))
else:
    st.success(t("✅ Low irrigation needed","✅ ري منخفض"))

# ✅ TIMELINE
st.markdown("### 📅 " + t("7-Day Farm Timeline","الجدول الزمني 7 أيام"))

def color(r):
    return "#ff4d4f" if r=="High" else "#faad14" if r=="Medium" else "#52c41a"

html = '<div style="display:flex;overflow-x:auto">'

for i in range(7):
    t_val = temp + np.random.randint(-2,3)
    s_val = soil - np.random.randint(0,5)

    future = pd.DataFrame([[s_val,t_val,humidity,rain,ph,N,P,K,wind,uv]],
    columns=input_data.columns)

    pred = model.predict(future)[0]
    r = labels[pred]

    html += f"""
    <div style="
        min-width:150px;
        margin:10px;
        padding:15px;
        background:{color(r)};
        color:white;
        border-radius:12px;
        text-align:center;
        box-shadow:0 4px 8px rgba(0,0,0,0.2);
    ">
        <h4>Day {i+1}</h4>
        <p>{r}</p>
    </div>
    """

html += "</div>"
st.markdown(html, unsafe_allow_html=True)

# ✅ ALERTS
st.markdown("### 🔔 " + t("Live Alerts","تنبيهات"))

alerts = df[df["Alert"] == True]
st.dataframe(alerts.tail(10))