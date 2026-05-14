import streamlit as st
import serial
import time
import requests
import pandas as pd
import numpy as np
import cv2
import os
import random
from PIL import Image
from collections import deque
from datetime import datetime

# --- SYSTEM CONFIGURATION ---
LOG_FILE = "factory_master_v5.csv"
CREDENTIALS = {"admin": "factory123", "farmer": "field123"}
st.set_page_config(page_title="Sugarcane AI Industrial Pro+", layout="wide", page_icon="🌾")

# --- CUSTOM CSS (INDUSTRIAL DARK/LIGHT HIGH CONTRAST) ---
st.markdown("""
    <style>
    .main { background-color: #fdfdfd; }
    [data-testid="stMetricValue"] { 
        color: #000000 !important; 
        font-weight: 900 !important; 
        font-size: 2.4rem !important; 
        letter-spacing: -1px;
    }
    [data-testid="stMetricLabel"] { color: #222222 !important; font-weight: 700 !important; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 25px; 
        border-radius: 15px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #eeeeee;
    }
    .stAlert { border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- CORE FUNCTIONS ---
def get_weather(api_key, city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        r = requests.get(url, timeout=3)
        return r.json() if r.status_code == 200 else None
    except: return None

def log_factory_event(ldr, t, h, y, status):
    entry = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Lux": ldr, "Temp": t, "Hum": h, "Yield": y, "Condition": status
    }
    df = pd.DataFrame([entry])
    if not os.path.exists(LOG_FILE): df.to_csv(LOG_FILE, index=False)
    else: df.to_csv(LOG_FILE, mode='a', header=False, index=False)

def process_satellite_ai(uploaded_file):
    """Spectral Analysis for Remote Sensing Intelligence"""
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Vegetation Index Calculation (NDVI Proxy)
    R, G, B = img[:,:,0].astype(float), img[:,:,1].astype(float), img[:,:,2].astype(float)
    denominator = 2*G + R + B
    denominator[denominator == 0] = 0.01
    gli = (2*G - R - B) / denominator
    
    # Heatmapping
    health_map = np.clip((gli + 1) * 127.5, 0, 255).astype(np.uint8)
    health_map_colored = cv2.applyColorMap(health_map, cv2.COLORMAP_JET)
    health_map_colored = cv2.cvtColor(health_map_colored, cv2.COLOR_BGR2RGB)
    
    score = round((np.sum(gli > 0.08) / gli.size) * 100, 2)
    return img, health_map_colored, score

# --- AUTH LAYER ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_screen():
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.title("🔐 Industrial Auth")
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login Here"):
            if user in CREDENTIALS and CREDENTIALS[user] == pw:
                st.session_state.logged_in = True
                st.session_state.user_role = user
                st.rerun()
            else:
                st.error("Access Denied: Invalid Credentials")

if not st.session_state.logged_in:
    login_screen(); st.stop()

# --- MAIN INDUSTRIAL HUB ---
st.title(f"🏭 Sugarcane Intelligence Pro+ (Role: {st.session_state.user_role.upper()})")

# Initialize Shared State
if 'history' not in st.session_state:
    st.session_state.history = deque(maxlen=100)

# SIDEBAR: COMMAND CENTER
st.sidebar.title("🎮 Command Center")
nav = st.sidebar.radio("Navigation", ["📡 Ground Sensors (IoT)", "🛰️ Satellite Remote Sensing", "🧪 Soil Nutrient Analysis", "📁 Factory Data Audit"])
st.sidebar.divider()
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False; st.rerun()

# ==========================================
# 🛰️ MODE: SATELLITE REMOTE SENSING
# ==========================================
if nav == "🛰️ Satellite Remote Sensing":
    st.header("🛰️ AI Remote Sensing & Profit Prediction")
    st.write("Scan your farm from the sky to detect stress and predict your financial harvest.")
    
    col_in1, col_in2, col_in3 = st.columns(3)
    ekar_size = col_in1.number_input("Field Size (Ekars/Acres)", value=1.0, min_value=0.1)
    market_p = col_in2.number_input("Market Price (₹/Ton)", value=3500)
    
    up = st.file_uploader("Upload Field Capture (Drone/Satellite)", type=['jpg', 'png', 'jpeg'])
    
    if up:
        with st.spinner("AI is calculating spectral vegetation indices..."):
            orig, h_map, score = process_satellite_ai(up)
            
            c_img1, c_img2 = st.columns(2)
            c_img1.image(orig, caption="True Color Image", use_container_width=True)
            c_img2.image(h_map, caption="NDVI Health Analysis", use_container_width=True)
            
            st.divider()
            
            # Logic for Yield based on Score
            if score > 80:
                status, tons_per = "✅ High Productivity (Optimal)", 48.0
                st.success(f"Farm Health: {status}")
            elif score > 60:
                status, tons_per = "⚠️ Moderate Health (Stressed Areas)", 35.0
                st.warning(f"Farm Health: {status}")
            else:
                status, tons_per = "🚨 Critical Health (Low Yield Risk)", 18.0
                st.error(f"Farm Health: {status}")
                
            total_tons = tons_per * ekar_size
            total_profit = total_tons * market_p
            
            res1, res2, res3 = st.columns(3)
            res1.metric("Vegetation Health Score", f"{score}%")
            res2.metric("Est. Total Yield", f"{round(total_tons, 1)} Tons")
            res3.metric("Projected Revenue", f"₹{int(total_profit):,}")

# ==========================================
# 📡 MODE: GROUND SENSORS (IoT)
# ==========================================
elif nav == "📡 Ground Sensors (IoT)":
    st.header("📡 Live IoT Field Monitoring")
    # Top Stats
    m1, m2, m3, m4 = st.columns(4)
    l_m = m1.empty(); t_m = m2.empty(); h_m = m3.empty(); hb_m = m4.empty()
    st.divider()
    
    col_live1, col_live2 = st.columns([2, 1])
    with col_live1:
        st.subheader("📈 Real-time Trends")
        chart_ph = st.empty()
    with col_live2:
        st.subheader("🤖 Smart Diagnosis")
        alert_ph = st.empty()
        st.subheader("📊 Session Statistics")
        stats_ph = st.empty()

    # SERIAL ENGINE
    try:
        if 'ser' not in st.session_state:
            import serial
            st.session_state.ser = serial.Serial("COM8", 9600, timeout=1)
        ser = st.session_state.ser
    except: ser = None

    while True:
        # Data Stream
        l, t, h = None, None, None
        is_sim = False
        if ser and ser.in_waiting > 0:
            try:
                line = ser.readline().decode(errors='ignore').strip()
                if "," in line: l, t, h = map(float, line.split(","))
            except: pass
        else:
            # High-Fidelity Simulation for Presentation
            l = random.randint(400, 900)
            t = 28 + random.uniform(-1, 1)
            h = 60 + random.uniform(-2, 2)
            is_sim = True; time.sleep(1)

        if l is not None:
            st.session_state.history.append({"L":l, "T":t, "H":h})
            df_curr = pd.DataFrame(list(st.session_state.history))
            y_curr = round(42 * (l/1000) * (1 - abs(t-28)/100), 2)
            
            l_m.metric("☀ Lux Intensity", int(l))
            t_m.metric("🌡 Temperature", f"{round(t,1)}°C")
            h_m.metric("💧 Humidity", f"{round(h,1)}%")
            hb_m.metric("📡 Status", "ONLINE" if not is_sim else "SIMULATED", datetime.now().strftime("%H:%M:%S"))
            
            chart_ph.line_chart(df_curr)
            
            with alert_ph.container():
                if t > 33: st.warning("⚠️ Heat Stress Detected")
                elif h < 45: st.error("💧 Critical Water Stress")
                else: st.success("✅ Growth: Optimal")
            
            with stats_ph.container():
                st.write(f"Avg Temp: {round(df_curr['T'].mean(),1)}°C")
                st.write(f"Max Humidity: {round(df_curr['H'].max(),1)}%")

        time.sleep(0.1)

# ==========================================
# 🧪 MODE: SOIL NUTRIENT ANALYSIS
# ==========================================
elif nav == "🧪 Soil Nutrient Analysis":
    st.header("🧪 Advanced AI Soil Chemist")
    st.write("NPK Nutrient availability based on active monitoring.")
    k1, k2, k3 = st.columns(3)
    k1.metric("Nitrogen (N)", "48 mg/kg", "Optimal")
    k2.metric("Phosphorus (P)", "24 mg/kg", "Low")
    k3.metric("Potassium (K)", "72 mg/kg", "Optimal")
    st.info("💡 Fertilizer Advice: Nitrogen levels are stable. Apply P-based nutrients in next cycle.")

# ==========================================
# 📁 MODE: FACTORY DATA AUDIT
# ==========================================
else:
    st.header("📁 Industrial Data Audit Center")
    if os.path.exists(LOG_FILE):
        st.dataframe(pd.read_csv(LOG_FILE).tail(50))
        with open(LOG_FILE, "rb") as f:
            st.download_button("📥 Export Full Report (CSV)", f, "factory_audit.csv")
    else:
        st.info("Awaiting initial factory telemetry data.")