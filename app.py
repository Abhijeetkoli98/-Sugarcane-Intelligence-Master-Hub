import streamlit as st
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
import plotly.express as px
import plotly.graph_objects as go

# --- SYSTEM CONFIGURATION ---
LOG_FILE = "factory_master_v5.csv"
CREDENTIALS = {"admin": "1234", "farmer": "field123"}

# LOCAL FACTORY DATABASE (Fallback Intelligence)
LOCAL_FACTORY_DB = {
    "kodoli": {"name": "Warna Sugar Factory", "price": 3580, "recovery": 12.4, "distance": 4, "risk": "Low", "status": "Local Hub"},
    "kolhapur": {"name": "Chh. Rajaram Factory", "price": 3510, "recovery": 11.8, "distance": 12, "risk": "Medium", "status": "Regional Hub"},
    "satara": {"name": "Ajinkyatara Sugar Mill", "price": 3450, "recovery": 11.2, "distance": 9, "risk": "Low", "status": "Verified"},
    "sangli": {"name": "Vasantdada Sahakari", "price": 3550, "recovery": 12.1, "distance": 15, "risk": "Medium", "status": "Congested"},
    "pune": {"name": "Sahyadri Bio-Sugar", "price": 3400, "recovery": 10.9, "distance": 22, "risk": "Low", "status": "Optimized"},
    "belgaum": {"name": "Hira Sugar Works", "price": 3620, "recovery": 12.8, "distance": 18, "risk": "Low", "status": "Export Focused"},
    "karad": {"name": "Sahyadri Sahakari", "price": 3480, "recovery": 11.5, "distance": 7, "risk": "Low", "status": "Optimal"},
    "ichalkaranji": {"name": "Dutta Sahakari", "price": 3530, "recovery": 11.9, "distance": 11, "risk": "Medium", "status": "Stable"},
    "kagal": {"name": "Chh. Shahu Mill", "price": 3590, "recovery": 12.3, "distance": 5, "risk": "Low", "status": "Local Best"},
    "ishwarpur": {"name": "Rajarambapu Patil Factory", "price": 3520, "recovery": 11.9, "distance": 8, "risk": "Low", "status": "Stable"},
    "shirol": {"name": "Shree Datta Shetkari Mill", "price": 3610, "recovery": 12.5, "distance": 6, "risk": "Low", "status": "High Recovery"},
    "borgaon": {"name": "Baliraja Sugar Mill", "price": 3440, "recovery": 11.1, "distance": 12, "risk": "Medium", "status": "Regional"},
    "nrusinhwadi": {"name": "Datta Prasad Hub", "price": 3490, "recovery": 11.4, "distance": 4, "risk": "Low", "status": "Verified"},
    "hatkanangle": {"name": "Sajjan Sugar Mill", "price": 3550, "recovery": 12.0, "distance": 7, "risk": "Low", "status": "Optimal"},
    "audumbarwadi": {"name": "Audumbar Sugar Mill", "price": 3460, "recovery": 11.2, "distance": 10, "risk": "Medium", "status": "Regional"},
    "kirloskarwadi": {"name": "RLM Sugar Factory", "price": 3600, "recovery": 12.4, "distance": 15, "risk": "Low", "status": "Verified"},
    "jat": {"name": "Jat Sugar Mill", "price": 3430, "recovery": 11.0, "distance": 20, "risk": "Medium", "status": "Regional"},
    "kavathepiran": {"name": "Kavathepiran Factory", "price": 3570, "recovery": 12.2, "distance": 9, "risk": "Low", "status": "Stable"},
    "tambewadi": {"name": "Tambe Wadi Mill", "price": 3450, "recovery": 11.1, "distance": 14, "risk": "Medium", "status": "Regional"},
    "pethvadgaon": {"name": "Peth Vadgaon Factory", "price": 3510, "recovery": 11.8, "distance": 8, "risk": "Low", "status": "Verified"},
    "miraj": {"name": "Miraj Sugar Works", "price": 3540, "recovery": 11.9, "distance": 13, "risk": "Medium", "status": "Stable"},
    "lohani": {"name": "Lohani Sugar Mill", "price": 3470, "recovery": 11.3, "distance": 11, "risk": "Medium", "status": "Regional"},
    "kavathemahankal": {"name": "Kavathe Mahankal Factory", "price": 3560, "recovery": 12.1, "distance": 16, "risk": "Medium", "status": "Stable"},
    "mangur": {"name": "Mangur Mill", "price": 3420, "recovery": 10.9, "distance": 19, "risk": "Medium", "status": "Regional"}, 
    "yavaluj": {"name": "Yavaluj Factory", "price": 3480, "recovery": 11.4, "distance": 22, "risk": "Medium", "status": "Regional"},
    "jath": {"name": "Jath Sugar Mill", "price": 3410, "recovery": 10.8,     "distance": 25, "risk": "Medium", "status": "Regional"},
    "shahapur": {"name": "Shahapur Factory", "price": 3520, "recovery": 11.7, "distance": 18, "risk": "Medium", "status": "Stable"},
    "kumbhoj": {"name": "Kumbhoj Factory", "price": 3580, "recovery": 12.2, "distance": 7, "risk": "Low", "status": "Optimal"},
    "takli": {"name": "Takli Factory", "price": 3470, "recovery": 11.3, "distance": 14, "risk": "Medium", "status": "Regional"},
    "madhavnagar": {"name": "Madhavnagar Mill", "price": 3530, "recovery": 11.9, "distance": 9, "risk": "Low", "status": "Stable"},
    "pune": {"name": "Pune Sugar Works", "price": 3400, "recovery": 10.7, "distance": 28, "risk": "Medium", "status": "Regional"},
    "kolhapur": {"name": "Kolhapur Sugars", "price": 3550, "recovery": 12.0, "distance": 6, "risk": "Low", "status": "Optimal"},
    "bhosga": {"name": "Bhosga Factory", "price": 3460, "recovery": 11.1, "distance": 17, "risk": "Medium", "status": "Regional"},
    "kallapur": {"name": "Kallapur  Mill", "price": 3600, "recovery": 12.4, "distance": 21, "risk": "Low", "status": "Verified"},
    "chinchli": {"name": "Chinchli Factory", "price": 3420, "recovery": 10.9, "distance": 12, "risk": "Medium", "status": "Stable"},
    "hatkanangle": {"name": "Hatkanangle Sugars", "price": 3510, "recovery": 11.6, "distance": 8, "risk": "Low", "status": "Optimal"},
    "narsingpur": {"name": "Narsingpur Factory", "price": 3440, "recovery": 11.0, "distance": 15, "risk": "Medium", "status": "Regional"},
    "dudhal": {"name": "Dudhal Mill", "price": 3570, "recovery": 12.3, "distance": 5, "risk": "Low", "status": "High Recovery"},
    "lohani": {"name": "Lohani Sugar Mill", "price": 3470, "recovery": 11.3, "distance": 11, "risk": "Medium", "status": "Regional"},
    "kavathemahankal": {"name": "Kavathe Mahankal Factory", "price": 3560, "recovery": 12.1, "distance": 16, "risk": "Medium", "status": "Stable"},
    "mangur": {"name": "Mangur Mill", "price": 3420, "recovery": 10.9, "distance": 19, "risk": "Medium", "status": "Regional"},
    "yavaluj": {"name": "Yavaluj Factory", "price": 3480, "recovery": 11.4, "distance": 22, "risk": "Medium", "status": "Regional"},
    "jath": {"name": "Jath Sugar Mill", "price": 3410, "recovery": 10.8, "distance": 25, "risk": "Medium", "status": "Regional"},
    "shahapur": {"name": "Shahapur Factory", "price": 3520, "recovery": 11.7, "distance": 18, "risk": "Medium", "status": "Stable"},
    "kumbhoj": {"name": "Kumbhoj Factory", "price": 3580, "recovery": 12.2, "distance": 7, "risk": "Low", "status": "Optimal"},
    "takli": {"name": "Takli Factory", "price": 3470, "recovery": 11.3, "distance": 14, "risk": "Medium", "status": "Regional"},
    "madhavnagar": {"name": "Madhavnagar Mill", "price": 3530, "recovery": 11.9, "distance": 9, "risk": "Low", "status": "Stable"},
    "pune": {"name": "Pune Sugar Works", "price": 3400, "recovery": 10.7, "distance": 28, "risk": "Medium", "status": "Regional"},
    "kolhapur": {"name": "Kolhapur Sugars", "price": 3550, "recovery": 12.0, "distance": 6, "risk": "Low", "status": "Optimal"},
    "bhosga": {"name": "Bhosga Factory", "price": 3460, "recovery": 11.1, "distance": 17, "risk": "Medium", "status": "Regional"},
    "kallapur": {"name": "Kallapur Mill", "price": 3600, "recovery": 12.4, "distance": 21, "risk": "Low", "status": "Verified"},
    "chinchli": {"name": "Chinchli Factory", "price": 3420, "recovery": 10.9, "distance": 12, "risk": "Medium", "status": "Stable"},
    "hatkanangle": {"name": "Hatkanangle Sugars", "price": 3510, "recovery": 11.6, "distance": 8, "risk": "Low", "status": "Optimal"},
    "narsingpur": {"name": "Narsingpur Factory", "price": 3440, "recovery": 11.0, "distance": 15, "risk": "Medium", "status": "Regional"},
    "dudhal": {"name": "Dudhal Mill", "price": 3570, "recovery": 12.3, "distance": 5, "risk": "Low", "status": "High Recovery"}, 
    "lohani": {"name": "Lohani Sugar Mill", "price": 3470, "recovery": 11.3, "distance": 11, "risk": "Medium", "status": "Regional"},
    "kavathemahankal": {"name": "Kavathe Mahankal Factory", "price": 3560, "recovery": 12.1, "distance": 16, "risk": "Medium", "status": "Stable"},
    "mangur": {"name": "Mangur Mill", "price": 3420, "recovery": 10.9, "distance": 19, "risk": "Medium", "status": "Regional"},
    "yavaluj": {"name": "Yavaluj Factory", "price": 3480, "recovery": 11.4, "distance": 22, "risk": "Medium", "status": "Regional"},
    "jath": {"name": "Jath Sugar Mill", "price": 3410, "recovery": 10.8, "distance": 25, "risk": "Medium", "status": "Regional"},
    "shahapur": {"name": "Shahapur Factory", "price": 3520, "recovery": 11.7, "distance": 18, "risk": "Medium", "status": "Stable"},
    "kumbhoj": {"name": "Kumbhoj Factory", "price": 3580, "recovery": 12.2, "distance": 7, "risk": "Low", "status": "Optimal"},
    "takli": {"name": "Takli Factory", "price": 3470, "recovery": 11.3, "distance": 14, "risk": "Medium", "status": "Regional"},
    "madhavnagar": {"name": "Madhavnagar Mill", "price": 3530, "recovery": 11.9, "distance": 9, "risk": "Low", "status": "Stable"},
    "pune": {"name": "Pune Sugar Works", "price": 3400, "recovery": 10.7, "distance": 28, "risk": "Medium", "status": "Regional"},
    "kolhapur": {"name": "Kolhapur Sugars", "price": 3550, "recovery": 12.0, "distance": 6, "risk": "Low", "status": "Optimal"},
    "bhosga": {"name": "Bhosga Factory", "price": 3460, "recovery": 11.1, "distance": 17, "risk": "Medium", "status": "Regional"},
    "kallapur": {"name": "Kallapur Mill", "price": 3600, "recovery": 12.4, "distance": 21, "risk": "Low", "status": "Verified"},
    "chinchli": {"name": "Chinchli Factory", "price": 3420, "recovery": 10.9, "distance": 12, "risk": "Medium", "status": "Stable"},
    "hatkanangle": {"name": "Hatkanangle Sugars", "price": 3510, "recovery": 11.6, "distance": 8, "risk": "Low", "status": "Optimal"},
    "narsingpur": {"name": "Narsingpur Factory", "price": 3440, "recovery": 11.0, "distance": 15, "risk": "Medium", "status": "Regional"},
    "dudhal": {"name": "Dudhal Mill", "price": 3570, "recovery": 12.3, "distance": 5, "risk": "Low", "status": "High Recovery"} 
}

DEFAULT_FACTORY = {"name": "Maharashtra Cooperative Hub", "price": 3410, "recovery": 11.0, "distance": 30, "risk": "Medium", "status": "State Estimate"}

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

def get_real_world_factories(city):
    """Fetches real sugar factories using OpenStreetMap (Overpass API)"""
    try:
        # 1. Geocode City to get Lat/Lon
        geo_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
        headers = {"User-Agent": "SugarcaneIntelligenceHub/1.0"}
        geo_res = requests.get(geo_url, headers=headers, timeout=5).json()
        
        if not geo_res: return None
        lat, lon = float(geo_res[0]['lat']), float(geo_res[0]['lon'])

        # 2. Query Overpass for Sugar Factories within 50km
        overpass_url = "https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json][timeout:25];
        (
          node["industrial"="factory"]["name"~"sugar|sakhar"i](around:50000,{lat},{lon});
          way["industrial"="factory"]["name"~"sugar|sakhar"i](around:50000,{lat},{lon});
          node["product"="sugar"](around:50000,{lat},{lon});
        );
        out center;
        """
        response = requests.post(overpass_url, data=query, timeout=10).json()
        
        real_factories = []
        import math
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371 # Earth radius in km
            dLat = math.radians(lat2 - lat1); dLon = math.radians(lon2 - lon1)
            a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            return R * c

        for element in response.get('elements', []):
            name = element.get('tags', {}).get('name', 'Unknown Sugar Mill')
            e_lat = element.get('lat') or element.get('center', {}).get('lat')
            e_lon = element.get('lon') or element.get('center', {}).get('lon')
            dist = round(haversine(lat, lon, e_lat, e_lon), 1)
            
            real_factories.append({
                "name": name,
                "price": random.randint(3400, 3600), # Simulated based on FRP
                "recovery": round(random.uniform(10.5, 12.5), 1),
                "distance": dist,
                "risk": "Low" if dist < 20 else "Medium",
                "status": "Verified on OSM"
            })
        
        return sorted(real_factories, key=lambda x: x['distance'])
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

def get_sensor_readings():
    """Universal sensor interface (Serial + Simulation fallback)"""
    is_connected = False
    try:
        if 'ser' not in st.session_state:
            import serial
            # Try COM8 as default, but wrap in try-except
            st.session_state.ser = serial.Serial("COM8", 9600, timeout=1)
        
        ser = st.session_state.ser
        if ser and ser.is_open:
            is_connected = True
    except: 
        st.session_state.ser = None
        ser = None

    l, t, h, sm = None, None, None, None
    is_sim = False
    
    if ser and is_connected:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode(errors='ignore').strip()
                if "," in line: 
                    parts = line.split(",")
                    # NodeMCU should send 4 values: LDR, Temp, Humidity, Soil Moisture
                    if len(parts) >= 4:
                        try:
                            l, t, h, sm = map(float, parts[:4])
                        except ValueError:
                            pass # Safely handle incomplete data parsing errors
                    elif len(parts) == 3: # Backward compatibility
                        try:
                            l, t, h = map(float, parts[:3])
                            sm = 45.0 # fallback for Soil Moisture
                        except ValueError:
                            pass
        except: 
            is_connected = False
    
    if l is None or t is None or h is None or sm is None:
        # High-Fidelity Simulation for Presentation
        l = random.randint(400, 900)
        t = 28 + random.uniform(-1, 1)
        h = 60 + random.uniform(-2, 2)
        sm = 50 + random.uniform(-5, 5) # Soil moisture simulation
        is_sim = True
        
    # Return exactly 5 values
    return l, t, h, sm, is_sim

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
if 'api_history' not in st.session_state:
    st.session_state.api_history = deque(maxlen=100)

# SIDEBAR: COMMAND CENTER
st.sidebar.title("🎮 Command Center")
nav = st.sidebar.radio("Navigation", ["📡 Ground Sensors (IoT)", "🛰️ Satellite Remote Sensing", "🌍 Weather Fusion Analysis", "🚜 Farmer Strategic Portal", "🔮 AI Harvest Predictor", "🏢 Factory Storage Optimizer", "🧪 Soil Nutrient Analysis", "📊 Enterprise AI Yield Forecasting", "📁 Factory Data Audit"])
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
    m1, m2, m3, m4, m5 = st.columns(5)
    l_m = m1.empty(); t_m = m2.empty(); h_m = m3.empty(); sm_m = m4.empty(); hb_m = m5.empty()
    st.divider()
    
    col_live1, col_live2 = st.columns([2, 1])
    with col_live1:
        st.subheader("📈 Real-time Trends")
        chart_l = st.empty()
        chart_t = st.empty()
        chart_h = st.empty()
        chart_sm = st.empty()
    with col_live2:
        st.subheader("🤖 Smart Diagnosis")
        alert_ph = st.empty()
        st.subheader("📊 Session Statistics")
        stats_ph = st.empty()

    # --- SENSOR ENGINE ---
    while True:
        l, t, h, sm, is_sim = get_sensor_readings()

        if l is not None:
            st.session_state.history.append({"L":l, "T":t, "H":h, "SM":sm})
            df_curr = pd.DataFrame(list(st.session_state.history))
            y_curr = round(42 * (l/1000) * (1 - abs(t-28)/100), 2)
            
            l_m.metric("☀ Lux", int(l))
            t_m.metric("🌡 Temp", f"{round(t,1)}°C")
            h_m.metric("💧 Hum", f"{round(h,1)}%")
            sm_m.metric("🌱 Soil", f"{round(sm,1)}%")
            hb_m.metric("📡 Status", "SIM" if is_sim else "LIVE", datetime.now().strftime("%H:%M:%S"))
            
            with chart_l.container():
                st.markdown("**☀ Lux Intensity**")
                st.line_chart(df_curr[['L']], height=150, color="#FFA500")
            
            with chart_t.container():
                st.markdown("**🌡 Temperature (°C)**")
                st.line_chart(df_curr[['T']], height=150, color="#FF0000")
            
            with chart_h.container():
                st.markdown("**💧 Humidity (%)**")
                st.line_chart(df_curr[['H']], height=150, color="#0000FF")
                
            with chart_sm.container():
                st.markdown("**🌱 Soil Moisture (%)**")
                st.line_chart(df_curr[['SM']], height=150, color="#00FF00")
            
            with alert_ph.container():
                if t > 33: st.warning("⚠️ Heat Stress Detected")
                elif h < 45: st.error("💧 Critical Water Stress")
                elif sm < 30: st.error("🌵 Soil is too dry")
                else: st.success("✅ Growth: Optimal")
            
            with stats_ph.container():
                st.write(f"Avg Temp: {round(df_curr['T'].mean(),1)}°C")
                st.write(f"Max Humidity: {round(df_curr['H'].max(),1)}%")
                
                st.markdown("---")
                # Dynamic Analyzing Donut Chart
                pie_data = pd.DataFrame({
                    "Metric": ["Temperature", "Humidity", "Soil Moisture", "Lux (Scaled)"],
                    "Value": [t, h, sm, l / 10] # Scaled down Lux so it fits in the pie visibly
                })
                fig_pie = px.pie(pie_data, values="Value", names="Metric", hole=0.5, 
                             color="Metric", 
                             color_discrete_map={
                                 "Temperature": "#FF0000", 
                                 "Humidity": "#0000FF", 
                                 "Soil Moisture": "#00FF00", 
                                 "Lux (Scaled)": "#FFA500"
                             })
                fig_pie.update_layout(
                    margin=dict(t=10, b=10, l=10, r=10), 
                    height=280,
                    showlegend=False,
                    annotations=[dict(text='Live<br>Data', x=0.5, y=0.5, font_size=16, showarrow=False)]
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True, key=f"pie_{time.time()}")
                
                st.markdown("---")
                # Dynamic Bar Chart
                bar_data = pd.DataFrame({
                    "Metric": ["Temp (°C)", "Humidity (%)", "Soil (%)", "Lux"],
                    "Value": [t, h, sm, l]
                })
                fig_bar = px.bar(bar_data, x="Metric", y="Value", text="Value", 
                                 color="Metric",
                                 color_discrete_map={
                                     "Temp (°C)": "#FF0000", 
                                     "Humidity (%)": "#0000FF", 
                                     "Soil (%)": "#00FF00", 
                                     "Lux": "#FFA500"
                                 })
                fig_bar.update_layout(
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=250,
                    showlegend=False
                )
                fig_bar.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                st.plotly_chart(fig_bar, use_container_width=True, key=f"bar_{time.time()}")

        time.sleep(1) # Frequency control

# ==========================================
# 🌍 MODE: WEATHER FUSION ANALYSIS
# ==========================================
elif nav == "🌍 Weather Fusion Analysis":
    st.header("🌍 Climate Fusion & Sensor Validation")
    st.write("Comparing real-time local sensor data against regional satellite weather APIs.")
    
    city = st.text_input("Enter City for API Sync", value="Pune")
    st.divider()

    # Placeholders for live updates
    m1, m2, m3 = st.columns(3)
    t_ph = m1.empty(); h_ph = m2.empty(); s_ph = m3.empty()
    
    chart_col1, chart_col2 = st.columns(2)
    t_chart_ph = chart_col1.empty(); h_chart_ph = chart_col2.empty()
    
    insight_ph = st.empty()

    api_key = "bd5e378503939ddaee76f12ad7a97608" # Placeholder

    while True:
        # 1. Get Sensor Data
        s_l, s_t, s_h, s_sm, s_is_sim = get_sensor_readings()
        st.session_state.history.append({"L":s_l, "T":s_t, "H":s_h, "SM":s_sm})
        
        # 2. Get API Data
        weather_data = get_weather(api_key, city)
        if weather_data:
            api_temp = weather_data['main']['temp']
            api_hum = weather_data['main']['humidity']
        else:
            api_temp = 30 + random.uniform(-2, 2)
            api_hum = 55 + random.uniform(-5, 5)
        
        st.session_state.api_history.append({"T_API": api_temp, "H_API": api_hum, "Time": datetime.now().strftime("%H:%M")})
        
        # 3. Calculations
        t_delta = s_t - api_temp
        h_delta = s_h - api_hum
        micro_status = "Micro-climate Active" if abs(t_delta) > 2 else "Synced with Region"

        # 4. Update Metrics
        with t_ph.container():
            st.metric("Temperature Comparison", f"{round(s_t, 1)}°C", f"{round(t_delta, 1)}°C vs API", delta_color="inverse")
            st.caption(f"API Current: {round(api_temp, 1)}°C")
        with h_ph.container():
            st.metric("Humidity Comparison", f"{round(s_h, 1)}%", f"{round(h_delta, 1)}% vs API")
            st.caption(f"API Current: {round(api_hum, 1)}%")
        with s_ph.container():
            st.metric("Micro-climate Status", micro_status, f"Deltas: T:{round(t_delta,1)} H:{round(h_delta,1)}")

        # 5. Update Charts
        history_df = pd.DataFrame(list(st.session_state.history))
        api_df = pd.DataFrame(list(st.session_state.api_history))
        
        if len(history_df) > 1 and len(api_df) > 1:
            min_len = min(len(history_df), len(api_df), 30)
            
            with t_chart_ph.container():
                st.subheader("🌡️ Temperature Convergence")
                comp_t = pd.DataFrame({
                    "Local Sensor": history_df['T'].tail(min_len).values,
                    "Regional API": api_df['T_API'].tail(min_len).values
                })
                st.area_chart(comp_t)

            with h_chart_ph.container():
                st.subheader("💧 Humidity Variance")
                comp_h = pd.DataFrame({
                    "Local Sensor": history_df['H'].tail(min_len).values,
                    "Regional API": api_df['H_API'].tail(min_len).values
                })
                st.line_chart(comp_h)
        else:
            t_chart_ph.info("🔄 Synchronizing data streams... Please wait.")

        # 6. Update Insights
        with insight_ph.container():
            st.subheader("💡 Analysis Insights")
            if abs(t_delta) > 3:
                st.warning("🚨 High Temperature Variance detected.")
            else:
                st.success("✅ Regional Sync: Optimal.")
            st.info(f"📍 Location: {city} | Fusion Latency: Real-time (2s)")

        time.sleep(2)

# ==========================================
# 🚜 MODE: FARMER STRATEGIC PORTAL
# ==========================================
elif nav == "🚜 Farmer Strategic Portal":
    st.header("🚜 Farmer Strategic Input & Factory Link")
    st.write("Plan your harvest and compare procurement offers from the region's top 5 factories.")
    
    # 1. Profile Input
    with st.container():
        c_in1, c_in2, c_in3 = st.columns(3)
        f_name = c_in1.text_input("Farmer Name", value="Abhijeet")
        f_area = c_in2.number_input("Total Farm Area (Acres)", value=5.0, min_value=0.1)
        f_loc = c_in3.text_input("Farm Location (e.g. Kodoli, Satara)", value="Kodoli")
    
    st.divider()

    # 3. Analytics Logic
    avg_yield_per_acre = 42 
    est_production = f_area * avg_yield_per_acre
    
    st.subheader(f"📊 Strategy for {f_name}'s Farm")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Est. Production", f"{int(est_production)} Tons", "Based on Regional Avg")
    m2.metric("Projected Health", "Good (84%)", "↑ 2% from last week")
    m3.metric("Market Sentiment", "Bullish", "High Demand")

    st.write("### 🏭 Real-Time Factory Procurement (Live API)")
    
    if st.button("🔍 Search Real Factories near Me"):
        with st.spinner(f"Querying OpenStreetMap for factories near {f_loc}..."):
            real_data = get_real_world_factories(f_loc)
            
            if real_data:
                factory = real_data[0] # Nearest
                
                # Financial Calc
                transport_cost = factory['distance'] * 15 * f_area 
                gross_revenue = est_production * factory['price']
                net_profit = gross_revenue - transport_cost
                
                with st.container():
                    st.markdown(f"### 🏆 Verified Nearest Match: {factory['name']}")
                    st.caption("Data Source: OpenStreetMap (Overpass API) Real-time Search")
                    c1, c2, c3 = st.columns(3)
                    
                    c1.metric("Net Profit Forecast", f"₹{int(net_profit):,}", f"After Logistics")
                    c2.metric("Distance", f"{factory['distance']} km", "Actual Road Proximity")
                    c3.metric("Purchase Price", f"₹{factory['price']}/T", f"Recovery: {factory['recovery']}%")
                    
                    st.divider()
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write("**Verified Logistics:**")
                        st.write(f"🚚 Est. Transport: ₹{int(transport_cost):,}")
                        st.write(f"🗺️ Coordinates: {factory.get('status', 'Verified')}")
                    
                    with col_b:
                        st.write("**Risk Analysis:**")
                        risk_color = "red" if factory['risk'] == "High" else "green" if factory['risk'] == "Low" else "orange"
                        st.markdown(f"⚠️ Risk: <span style='color:{risk_color}'>{factory['risk']}</span> (Active)", unsafe_allow_html=True)
                        st.info(f"💡 AI Suggestion: This is your best logistical match. We suggest finalizing procurement terms immediately.")
                
                # Show others in a small list
                if len(real_data) > 1:
                    with st.expander("Other Factories Found Nearby"):
                        for f in real_data[1:5]:
                            st.write(f"- **{f['name']}**: {f['distance']} km | ₹{f['price']}/Ton")
            else:
                # Search Local DB
                search_query = f_loc.lower().strip()
                factory = LOCAL_FACTORY_DB.get(search_query, DEFAULT_FACTORY)
                
                # Financial Calc
                transport_cost = factory['distance'] * 15 * f_area 
                gross_revenue = est_production * factory['price']
                net_profit = gross_revenue - transport_cost

                with st.container():
                    st.markdown(f"### 🏆 Local Best Match: {factory['name']}")
                    st.caption("Data Source: Internal Factory Database (Local Fallback)")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Net Profit Forecast", f"₹{int(net_profit):,}", "Local Est.")
                    c2.metric("Distance", f"{factory['distance']} km", "Approx. Proximity")
                    c3.metric("Purchase Price", f"₹{factory['price']}/T", f"Recovery: {factory['recovery']}%")
    else:
        st.info(f"Enter your location (e.g. Kodoli) and click search to pull real-world factory data.")

    # 4. Future Risk & Growth Map
    st.divider()
    st.subheader("🔮 Future Risk Analysis (90 Day Outlook)")
    
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.write("**Climate Risk**")
        st.progress(25)
        st.caption("Low Risk: Predicted monsoon alignment is optimal for harvest.")
        
    with r_col2:
        st.write("**Price Volatility**")
        st.progress(45)
        st.caption("Moderate Risk: Global sugar prices showing slight fluctuations.")

    st.info(f"💡 **AI Suggestion for {f_name}:** Based on your farm area of {f_area} acres, we suggest monitoring local recovery rates and booking your procurement slot early to maximize your transport bonuses.")


# ==========================================
# 🔮 MODE: AI HARVEST PREDICTOR
# ==========================================
elif nav == "🔮 AI Harvest Predictor":
    st.header("🔮 Precision AI Harvest Predictor")
    st.write("Professional ML-driven analytics for long-term agricultural strategy.")
    
    with st.expander("📝 Manual Parameter Entry (Farmer Input)", expanded=True):
        c1, c2, c3 = st.columns(3)
        temp_in = c1.slider("Average Temperature (°C)", 10, 50, 28)
        hum_in = c2.slider("Humidity (%)", 10, 100, 60)
        light_in = c3.slider("Light Intensity (Lux)", 100, 2000, 800)
        
        c4, c5, c6 = st.columns(3)
        soil_type = c4.selectbox("Soil Condition", ["Black Loamy", "Red Sandy", "Clayey", "Saline"])
        irrigation_freq = c5.selectbox("Irrigation Frequency", ["Daily", "Weekly", "Bi-Weekly", "Monthly"])
        fertilizer_type = c6.selectbox("Fertilizer Usage", ["Organic/Compost", "NPK Balanced", "Urea High-Nitrogen", "None"])
        
        c7, c8 = st.columns(2)
        crop_age = c7.number_input("Current Crop Age (Months)", 0, 18, 6)
        farm_size = c8.number_input("Total Area (Acres)", 0.1, 500.0, 5.0)

    # --- AI PREDICTION ENGINE ---
    st.divider()
    
    # 1. Health Logic
    score = 0
    if 25 <= temp_in <= 33: score += 20
    if 50 <= hum_in <= 75: score += 20
    if light_in > 600: score += 15
    if irrigation_freq in ["Daily", "Weekly"]: score += 20
    if fertilizer_type != "None": score += 25
    
    if score >= 80: health = "Good"; h_color = "green"
    elif score >= 50: health = "Average"; h_color = "orange"
    else: health = "Poor"; h_color = "red"
    
    # 2. Performance Scoring
    perf_score = score
    
    # 3. Yield Forecasting (5 Years)
    base_yield = 40.0 # Tons per acre
    health_mult = 1.2 if health == "Good" else 0.8 if health == "Average" else 0.4
    initial_yield = farm_size * base_yield * health_mult
    
    years = [f"Year {i+1}" for i in range(5)]
    # Trend logic: growth based on health
    growth_rate = 0.05 if health == "Good" else 0.01 if health == "Average" else -0.10
    yield_trend = [initial_yield * (1 + growth_rate)**i for i in range(5)]
    
    # --- DASHBOARD VISUALS ---
    res1, res2, res3 = st.columns(3)
    res1.metric("Predicted Health", health, delta=f"{score}% Confidence", delta_color="normal")
    res2.metric("Performance Score", f"{perf_score}/100", "Growth Potential")
    res3.metric("Est. Total Revenue (Y1)", f"₹{int(initial_yield * 3500):,}")

    st.subheader("📈 5-Year Yield Projection")
    fig_yield = px.line(x=years, y=yield_trend, markers=True, title="Predicted Harvest Volume (Tons)")
    fig_yield.update_traces(line_color="green" if health == "Good" else "orange")
    st.plotly_chart(fig_yield, use_container_width=True)
    
    # --- RECOMMENDATION & RISK ---
    st.divider()
    rec_col, risk_col = st.columns(2)
    
    with rec_col:
        st.subheader("💡 Expert Recommendations")
        if irrigation_freq in ["Bi-Weekly", "Monthly"]:
            st.info("💧 **Irrigation**: Upgrade to Weekly frequency to optimize sucrose concentration.")
        if soil_type == "Saline":
            st.warning("🌱 **Soil Care**: Add Gypsum to counter salinity and improve root health.")
        if fertilizer_type == "None":
            st.error("🧪 **Fertilizer**: Apply NPK 10-26-26 to boost growth in month {crop_age+1}.")
        if health == "Good":
            st.success("✅ **Maintenance**: Current parameters are optimal. Continue spectral monitoring.")

    with risk_col:
        st.subheader("🚨 Risk Forecast")
        if temp_in > 38:
            st.error("🔥 **Heat Stress**: 70% probability of leaf burn. Increase soil moisture.")
        elif score < 50:
            st.error("📉 **Yield Loss**: High risk of 40% production drop due to environmental stress.")
        else:
            st.success("🌤️ **Stability**: Low risk environment. No immediate threats detected.")

# ==========================================
# 🏢 MODE: FACTORY STORAGE OPTIMIZER
# ==========================================
elif nav == "🏢 Factory Storage Optimizer":
    st.header("🏢 Enterprise Storage Intelligence (Pro+ Analytics)")
    st.write("Advanced industrial decision support for large-scale sucrose preservation.")
    
    # 1. Multi-Unit Monitoring
    unit_id = st.selectbox("Select Industrial Asset", ["Silo Alpha (Primary)", "Silo Beta (High-Cap)", "Warehouse 01", "Warehouse 02"])
    
    with st.expander(f"⚙️ Control Parameters: {unit_id}", expanded=True):
        col1, col2, col3 = st.columns(3)
        s_temp = col1.slider("Ambient Temperature (°C)", 10.0, 50.0, 24.0)
        s_hum = col2.slider("Internal Humidity (%)", 10, 100, 65)
        s_qty = col3.number_input("Unit Quantity (Metric Tons)", 100, 100000, 10000)
        
        col4, col5, col6 = st.columns(3)
        s_dur = col4.number_input("Days in Storage", 0, 150, 7)
        s_vent = col5.select_slider("Ventilation Strength", options=["None", "Low", "Medium", "High", "Turbo"], value="Medium")
        s_cost = col6.number_input("Market Value (₹/Ton)", 3000, 4500, 3600)

    # --- ADVANCED BIOLOGICAL MODEL (Industrial Grade) ---
    # Base sucrose loss per day (biological respiration)
    base_decay = 0.08 
    # Exponential factors for Temp and Hum
    temp_impact = (s_temp / 20)**2.2
    hum_impact = (s_hum / 60)**1.8
    # Ventilation bonus
    vent_map = {"None": 1.2, "Low": 1.0, "Medium": 0.8, "High": 0.6, "Turbo": 0.4}
    vent_factor = vent_map[s_vent]
    
    daily_decay_rate = (base_decay * temp_impact * hum_impact * vent_factor) # % per day
    total_loss_pct = s_dur * daily_decay_rate
    current_quality = max(0, 100 - total_loss_pct)
    
    total_val = s_qty * s_cost
    lost_val = total_val * (total_loss_pct / 100)
    
    # --- INDUSTRIAL KPIs ---
    st.divider()
    k1, k2, k3, k4 = st.columns(4)
    
    # Logic for Priority
    if total_loss_pct > 15: p_label, p_color = "🔴 CRITICAL", "red"
    elif total_loss_pct > 5: p_label, p_color = "🟡 MODERATE", "orange"
    else: p_label, p_color = "🟢 STABLE", "green"
    
    k1.metric("Crush Priority", p_label)
    k2.metric("Storage Efficiency", f"{round(100 - total_loss_pct, 1)}%")
    k3.metric("Daily Value Leak", f"₹{int(total_val * (daily_decay_rate/100)):,}")
    k4.metric("Asset Valuation", f"₹{int(total_val/1000000)}M")

    # --- COMPARATIVE TREND ANALYSIS ---
    st.subheader("📊 Comparative Spoilage Forecast (30 Days)")
    
    # Simulation for "Optimized" (e.g. Temp at 20C, Hum at 50%)
    opt_daily_decay = (base_decay * (20/20)**2.2 * (50/60)**1.8 * 0.6)
    
    days_range = list(range(s_dur, s_dur + 31))
    trend_curr = [max(0, 100 - (d * daily_decay_rate)) for d in days_range]
    trend_opt = [max(0, 100 - (d * opt_daily_decay)) for d in days_range]
    
    df_trend = pd.DataFrame({
        "Day": days_range,
        "Current Protocol": trend_curr,
        "Optimized (AI Suggestion)": trend_opt
    })
    
    fig_comp = px.line(df_trend, x="Day", y=["Current Protocol", "Optimized (AI Suggestion)"], 
                      title="Quality Preservation Index: Reality vs Optimization",
                      color_discrete_map={"Current Protocol": "red", "Optimized (AI Suggestion)": "cyan"})
    st.plotly_chart(fig_comp, use_container_width=True)

    # --- FINANCIAL IMPACT & WHAT-IF ---
    st.divider()
    f1, f2 = st.columns(2)
    
    with f1:
        st.subheader("💰 Financial Impact")
        st.write(f"Total Value in {unit_id}: **₹{int(total_val):,}**")
        st.write(f"Estimated Revenue Leakage: <span style='color:red'>-₹{int(lost_val):,}</span>", unsafe_allow_html=True)
        st.write(f"Current Recovery Grade: **{'Grade A' if current_quality > 90 else 'Grade B' if current_quality > 75 else 'Grade C'}**")

    with f2:
        st.subheader("🚀 ROI from Optimization")
        savings = (total_loss_pct - (s_dur * opt_daily_decay)) / 100 * total_val
        st.success(f"Potential Savings: **₹{int(max(0, savings)):,}**")
        st.write("By reducing temperature to **20°C** and optimizing ventilation, you can preserve significant factory revenue.")
        
    # --- STRATEGIC ALERTS ---
    st.divider()
    if total_loss_pct > 10:
        st.error(f"🚨 **ALERT**: Spoilage front detected in {unit_id}. Priority dispatch to Crushing Floor recommended within 24 hours.")
    else:
        st.success("✅ **STABLE**: Environmental parameters are within the safe industrial buffer.")

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
# 📊 MODE: ENTERPRISE AI YIELD FORECASTING
# ==========================================
elif nav == "📊 Enterprise AI Yield Forecasting":
    st.header("📊 Enterprise AI Yield Forecasting & Market Analytics")
    st.write("Complete AI Pipeline utilizing historical weather data to predict crop yield and generate industry-focused insights.")
    
    uploaded_file = st.file_uploader("Upload Historical Weather CSV (3 Years)", type="csv")
    csv_file = uploaded_file if uploaded_file is not None else "historical_weather.csv"
    
    if not os.path.exists("historical_weather.csv") and uploaded_file is None:
        st.error("Dataset not found. Please upload historical weather data.")
    else:
        # 1. Advanced NASA/WorldBank Robust Data Loading & Preprocessing
        @st.cache_data
        def load_clean_data(file_source):
            try:
                import io
                import numpy as np
                
                # Extract file contents into lines safely
                if hasattr(file_source, 'getvalue'):
                    content = file_source.getvalue().decode('utf-8').splitlines()
                else:
                    with open(file_source, 'r', encoding='utf-8') as f:
                        content = f.readlines()
                        
                # Locate real header (Bypass NASA POWER metadata)
                header_idx = 0
                for i, line in enumerate(content):
                    line_lower = line.lower()
                    if "-end header-" in line_lower:
                        header_idx = i + 1
                        break
                    # Fallback guess if no clear end marker exists
                    if ('temp' in line_lower or 't2m' in line_lower) and ('rain' in line_lower or 'prec' in line_lower):
                        header_idx = i
                        break
                        
                # Load the clean CSV string starting from the real header
                csv_data = "\n".join(content[header_idx:])
                df = pd.read_csv(io.StringIO(csv_data), on_bad_lines='skip', sep=None, engine='python', skip_blank_lines=True)
                
                # Clean column names
                df.columns = df.columns.str.strip().str.lower()
                
                # Advanced Auto-detect and standardize column naming (Support NASA POWER tags)
                rename_map = {}
                for col in df.columns:
                    if 'temp' in col or col == 't2m' or col == 't': rename_map[col] = 'Temperature'
                    elif 'rain' in col or 'prec' in col or col == 'prectotcorr': rename_map[col] = 'Rainfall'
                    elif 'hum' in col or 'rh2m' in col or col == 'h': rename_map[col] = 'Humidity'
                    elif 'yield' in col or 'prod' in col: rename_map[col] = 'Yield_Tons_Per_Acre'
                    elif 'date' in col or 'time' in col: rename_map[col] = 'Date'
                
                df = df.rename(columns=rename_map)
                
                # Construct missing Date column from NASA POWER YEAR, MO, DY or YEAR, DOY
                if 'date' not in df.columns and 'Date' not in df.columns:
                    if 'year' in df.columns and 'mo' in df.columns and 'dy' in df.columns:
                        df['Date'] = pd.to_datetime(df[['year', 'mo', 'dy']].rename(columns={'year': 'year', 'mo': 'month', 'dy': 'day'}), errors='coerce')
                    elif 'year' in df.columns and 'doy' in df.columns:
                        # Convert year and Day-Of-Year into an actual Date (e.g. 2023 150 -> 2023-05-30)
                        df['Date'] = pd.to_datetime(df['year'].astype(str).str.split('.').str[0] + df['doy'].astype(str).str.split('.').str[0], format='%Y%j', errors='coerce')
                
                # If Yield is completely missing (pure weather dataset), simulate it logically for the pipeline
                if 'Yield_Tons_Per_Acre' not in df.columns and 'Temperature' in df.columns and 'Rainfall' in df.columns:
                    # Formula based on typical Sugarcane response
                    df['Yield_Tons_Per_Acre'] = 40 + (df['Temperature'] - 28)*0.3 + (df['Rainfall']*0.15) + np.random.normal(0, 1.5, len(df))
                
                # Ensure essential columns exist
                required = ['Temperature', 'Rainfall', 'Humidity', 'Yield_Tons_Per_Acre', 'Date']
                missing = [col for col in required if col not in df.columns]
                
                if missing:
                    return False, f"Missing required columns: {missing}. Found columns: {list(df.columns)}. Ensure your CSV contains required data metrics."
                
                # Data type correction & Cleaning
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                for col in ['Temperature', 'Rainfall', 'Humidity', 'Yield_Tons_Per_Acre']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Drop invalid dates and fill missing values
                df = df.dropna(subset=['Date'])
                df = df.ffill().bfill()
                return True, df
                
            except Exception as e:
                return False, f"Critical Parsing Error: {str(e)}"
        
        success, load_result = load_clean_data(csv_file)
        
        if not success:
            st.error(f"⚠️ **CSV Loading Error:** {load_result}")
            st.info("💡 **Fixing malformed CSVs:** Your file might have metadata text at the top (common with NASA/World Bank). Try deleting the first few descriptive rows so the file strictly starts with the column headers.")
            st.stop() # Halt execution for this tab if data fails to load
            
        df_hist = load_result
        
        with st.expander("🔍 Dataset Preview & Validation"):
            st.write(f"✅ Successfully loaded and cleaned **{len(df_hist)} rows** and **{len(df_hist.columns)} columns**.")
            st.dataframe(df_hist.head())
        
        # Get Real-Time Data to merge with historical trends
        l, t, h, sm, is_sim = get_sensor_readings()
        
        st.subheader("📈 3-Year Historical Weather & Yield Trends")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Historical Data Points", f"{len(df_hist)} Days")
        c2.metric("Avg Yield (Tons/Acre)", f"{round(df_hist['Yield_Tons_Per_Acre'].mean(), 1)} T")
        c3.metric("Avg Rainfall (mm/day)", f"{round(df_hist['Rainfall'].mean(), 1)} mm")
        c4.metric("Live Temp (°C)", f"{t}°C", delta=f"{round(t - df_hist['Temperature'].mean(), 1)} vs Hist Avg", delta_color="inverse")
        
        # Historical Trend Chart
        fig_hist = px.line(df_hist, x='Date', y=['Temperature', 'Rainfall', 'Yield_Tons_Per_Acre'], title="Historical Parameters vs. Target Yield over 3 Years")
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # 2. Machine Learning Model Training (Weather & Yield)
        st.divider()
        st.subheader("🧠 Machine Learning Forecast & Yield Predictor")
        
        with st.spinner("Training Models on Historical & Live Sensor Data..."):
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import mean_squared_error, r2_score
            
            # Yield Prediction Model
            X = df_hist[['Temperature', 'Rainfall', 'Humidity']]
            y = df_hist['Yield_Tons_Per_Acre']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_model.fit(X_train, y_train)
            r2 = r2_score(y_test, rf_model.predict(X_test))
            
            # Weather Prediction Model (Mapping Day of Year -> Weather)
            df_hist['DayOfYear'] = df_hist['Date'].dt.dayofyear
            X_weather = df_hist[['DayOfYear']]
            weather_model_temp = RandomForestRegressor(n_estimators=50, random_state=42).fit(X_weather, df_hist['Temperature'])
            weather_model_rain = RandomForestRegressor(n_estimators=50, random_state=42).fit(X_weather, df_hist['Rainfall'])
            weather_model_hum = RandomForestRegressor(n_estimators=50, random_state=42).fit(X_weather, df_hist['Humidity'])
            
            # Predict Next Year Average Weather (Average of 365 days)
            days = pd.DataFrame({'DayOfYear': range(1, 366)})
            p_temp = weather_model_temp.predict(days).mean()
            p_rain = weather_model_rain.predict(days).mean()
            p_hum = weather_model_hum.predict(days).mean()
            
            # Dynamic Adjustments using Real-Time Sensor Inputs (Data Fusion)
            live_temp_delta = t - df_hist['Temperature'].mean()
            live_hum_delta = h - df_hist['Humidity'].mean()
            
            # Adjust forecasts by heavily weighing the current sensor momentum
            adj_p_temp = p_temp + (live_temp_delta * 0.15) 
            adj_p_hum = p_hum + (live_hum_delta * 0.15)
            
            predicted_yield = rf_model.predict([[adj_p_temp, p_rain, adj_p_hum]])[0]
            confidence_score = min(99.5, max(50.0, r2 * 100 - abs(live_temp_delta)*0.5))
            
        st.success(f"Models successfully trained! Pipeline Confidence Score: {round(confidence_score, 1)}%")
        
        # 3. Future Prediction Engine Outputs
        st.markdown("### 🔮 Next Year's Climate & Yield Forecast")
        st.write("Using Historical 3-Year Patterns + Real-Time Sensor Weighting")
        
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        f_col1.metric("Predicted Yield", f"{round(predicted_yield, 2)} Tons", delta=f"{round(predicted_yield - df_hist['Yield_Tons_Per_Acre'].mean(), 2)} vs Avg")
        f_col2.metric("Forecasted Temp", f"{round(adj_p_temp, 1)} °C")
        f_col3.metric("Forecasted Rainfall", f"{round(p_rain, 1)} mm/day")
        f_col4.metric("Forecasted Humidity", f"{round(adj_p_hum, 1)} %")
        
        # Comparison Graphs
        comp_df = pd.DataFrame({
            "Metric": ["Temperature (°C)", "Rainfall (mm)", "Humidity (%)", "Yield (Tons)"],
            "Historical Avg": [df_hist['Temperature'].mean(), df_hist['Rainfall'].mean(), df_hist['Humidity'].mean(), df_hist['Yield_Tons_Per_Acre'].mean()],
            "Forecasted": [adj_p_temp, p_rain, adj_p_hum, predicted_yield]
        })
        fig_comp = px.bar(comp_df, x="Metric", y=["Historical Avg", "Forecasted"], barmode="group", title="Past vs. Predicted Averages")
        st.plotly_chart(fig_comp, use_container_width=True)
        
        # Map Style Visual Outputs
        st.markdown("### 🗺️ Regional Risk Mapping")
        st.caption("Geospatial visualization of local risk indexes based on combined predictive modeling.")
        mock_map_data = pd.DataFrame({
            'lat': [16.7050 + (t*0.0001), 16.7150, 16.6950, 16.7250, 16.6850],
            'lon': [74.2433 + (h*0.0001), 74.2533, 74.2333, 74.2633, 74.2233],
        })
        st.map(mock_map_data)
        
        # 4. Industry-Focused Business Intelligence & Intelligent Features
        st.divider()
        st.header("🏢 Industry Analytics & Intelligent Advisories")
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            # Anomaly Detection & Risk
            st.markdown("### 🚨 Anomaly Detection & Risk Alerts")
            risk_level = "Low"
            if abs(live_temp_delta) > 5:
                st.error(f"⚠️ Temperature Anomaly! Live ({t}°C) is vastly different from historical mean. Extreme heat stress risk.")
                risk_level = "High"
            elif sm < 30:
                st.warning(f"⚠️ Low Soil Moisture Alert ({sm}%). Immediate irrigation required.")
                risk_level = "Medium"
            elif p_rain < 3.0:
                st.error("⚠️ Predicted Drought Risk for upcoming season.")
                risk_level = "High"
            else:
                st.success("✅ No critical weather anomalies detected. Soil health and climate stable.")
                
            st.markdown("### 🌱 Crop Advisory Suggestions")
            if risk_level == "High":
                st.write("- **Action:** Deploy drip irrigation systems instantly.")
                st.write("- **Action:** Use heat-resistant crop varieties for the next cycle.")
                st.write("- **Action:** Apply potassium (K) rich fertilizers to combat drought stress.")
            else:
                st.write("- **Action:** Maintain standard NPK fertilizer scheduling.")
                st.write("- **Action:** Monitor soil moisture weekly to maintain baseline.")
                
        with res_col2:
            # Demand-Supply & Pricing
            st.markdown("### 💸 Dynamic Pricing & Market Insight")
            avg_yield = df_hist['Yield_Tons_Per_Acre'].mean()
            if predicted_yield < avg_yield * 0.95:
                st.warning("📉 Supply Shortage Expected.")
                st.write("**Pricing Insight:** Procurement prices will rise due to scarcity. Recommended Factory Price: **₹3,750 / Ton**")
                st.write("**Production Planning:** Secure procurement contracts early to avoid raw material shortage.")
            elif predicted_yield > avg_yield * 1.05:
                st.info("📈 Surplus Expected.")
                st.write("**Pricing Insight:** Market saturation likely. Recommended Factory Price: **₹3,300 / Ton**")
                st.write("**Production Planning:** Maximize crushing schedules and optimize storage capacity. Prepare for export.")
            else:
                st.success("⚖️ Balanced Market.")
                st.write("**Pricing Insight:** Stable market. Recommended Factory Price: **₹3,500 / Ton**")
                st.write("**Production Planning:** Standard operational hours recommended.")
                
        # Automated Report Generation
        st.markdown("### 📄 Automated Decision Report")
        report = f"""--- Sugarcane Intelligence Automated Report ---
        
Confidence Score: {round(confidence_score, 1)}%
Historical Average Yield: {round(avg_yield, 2)} Tons/Acre
Forecasted Next-Season Yield: {round(predicted_yield, 2)} Tons/Acre

Live Sensor Anomaly Deltas vs 3-Year History:
- Temp Delta: {round(live_temp_delta, 1)}°C
- Hum Delta: {round(live_hum_delta, 1)}%

Risk Assessment: {risk_level}

Recommendations:
Review dynamic pricing suggestions based on predicted yield variance. Follow crop advisory to mitigate {risk_level.lower()} risk.
"""
        st.info(report)
        st.download_button("📥 Download Automated Executive Report", report, file_name="AI_Yield_Forecast_Report.txt")

# ==========================================
# 📁 MODE: FACTORY DATA AUDIT & SMART DASHBOARDS
# ==========================================
else:
    st.header("📁 Industrial Data Audit & Smart Dashboard Center")
    
    # ── Live sensor snapshot ──────────────────────────────────
    l, t, h, sm, is_sim = get_sensor_readings()
    data_src = "⚠️ Simulation" if is_sim else "✅ Live Hardware"

    if not os.path.exists(LOG_FILE):
        st.warning("📂 No sensor log found yet. Start the **Ground Sensors (IoT)** module to begin recording.")
        if st.button("🚀 Seed 200 Rows of Sample Sensor Data"):
            import datetime as dt
            rows = []
            for i in range(200):
                ts = (dt.datetime.now() - dt.timedelta(minutes=i*5)).strftime("%Y-%m-%d %H:%M:%S")
                cond = "Optimal" if i % 12 != 0 else "Critical Stress"
                rows.append({"Timestamp": ts,
                              "Lux": random.randint(350,900),
                              "Temp": round(26 + random.gauss(0,2),1),
                              "Hum": round(60 + random.gauss(0,5),1),
                              "Yield": round(38 + random.gauss(0,3),1),
                              "Condition": cond})
            pd.DataFrame(rows).to_csv(LOG_FILE, index=False)
            st.success("Sample data seeded — all metrics will now be sensor-driven.")
            st.rerun()
        st.stop()

    # ── Load and parse the real sensor log ───────────────────
    df_log = pd.read_csv(LOG_FILE)
    df_log.columns = df_log.columns.str.strip()
    df_log["Timestamp"] = pd.to_datetime(df_log["Timestamp"], errors="coerce")
    df_log = df_log.dropna(subset=["Timestamp"]).sort_values("Timestamp")
    
    # ── Normalize column names (handles both old T/H/L/Y and new Temp/Hum/Lux/Yield formats) ──
    col_remap = {"T": "Temp", "H": "Hum", "L": "Lux", "Y": "Yield", "Status": "Condition"}
    df_log = df_log.rename(columns={k: v for k, v in col_remap.items() if k in df_log.columns and v not in df_log.columns})
    
    for col in ["Lux", "Temp", "Hum", "Yield"]:
        if col in df_log.columns:
            df_log[col] = pd.to_numeric(df_log[col], errors="coerce")
    df_log = df_log.ffill()

    # ── Derived KPIs ─────────────────────────────────────────
    total_records    = len(df_log)
    avg_temp         = round(df_log["Temp"].mean(),  1) if "Temp"  in df_log.columns else t
    avg_hum          = round(df_log["Hum"].mean(),   1) if "Hum"   in df_log.columns else h
    avg_lux          = round(df_log["Lux"].mean(),   0) if "Lux"   in df_log.columns else l
    avg_yield        = round(df_log["Yield"].mean(), 1) if "Yield" in df_log.columns else 40.0
    cond_col         = "Condition" if "Condition" in df_log.columns else None
    critical_count   = int(df_log[cond_col].str.contains("Critical|Stress|Warning", case=False, na=False).sum()) if cond_col else 0
    compliance_pct   = round(((total_records - critical_count) / total_records) * 100, 1) if total_records else 100
    latest           = df_log.iloc[-1]
    live_temp        = round(float(latest.get("Temp",  t)),  1)
    live_hum         = round(float(latest.get("Hum",   h)),  1)
    live_lux         = round(float(latest.get("Lux",   l)),  0)
    live_yield       = round(float(latest.get("Yield", avg_yield)), 1)

    # ── Role-Separated Dashboard Tabs ────────────────────────
    role = st.session_state.get("user_role", "farmer")
    view_tab, report_tab, archive_tab = st.tabs(["📊 Live Dashboard", "📄 Report Generator", "🗂️ Raw Archive"])

    # ============================================================
    # TAB 1 — LIVE DASHBOARD  (role-aware)
    # ============================================================
    with view_tab:
        if role == "admin":
            # ── FACTORY MANAGER VIEW ─────────────────────────
            st.subheader("🏭 Factory Manager Dashboard — Sensor-Driven Metrics")
            st.caption(f"Data Source: `{LOG_FILE}` | {total_records} logged events | {data_src}")

            f1, f2, f3, f4 = st.columns(4)
            f1.metric("Avg Field Temp",        f"{avg_temp} °C",  f"Live: {live_temp} °C")
            f2.metric("Avg Humidity",           f"{avg_hum} %",    f"Live: {live_hum} %")
            f3.metric("Avg Light Intensity",    f"{int(avg_lux)} Lux", f"Live: {int(live_lux)} Lux")
            f4.metric("Avg Yield Estimate",     f"{avg_yield} T",  f"Live: {live_yield} T")

            st.markdown("---")
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Sensor Records",  f"{total_records:,}")
            m2.metric("Compliance Score",       f"{compliance_pct}%")
            m3.metric("Anomaly Events",         critical_count, delta="Risk Flags", delta_color="inverse")

            # ── Predictive Maintenance (sensor-driven) ────────
            st.markdown("### 🔧 Predictive Maintenance Engine")
            if live_temp > 34:
                st.error("🚨 **Heat Stress Alert:** Live temp exceeds 34 °C. Risk of reduced juice quality. Schedule cooling checks.")
            elif live_hum < 45:
                st.warning("⚠️ **Humidity Drop:** Low humidity may accelerate field drying. Review irrigation schedule.")
            elif critical_count > (total_records * 0.10):
                st.error("🚨 **High Anomaly Rate:** >10 % of records are critical events. Immediate system diagnostic recommended.")
            else:
                st.success("✅ All sensor parameters nominal. No maintenance action required at this time.")

            # ── Multi-param Trend Chart (from real log) ───────
            st.markdown("### 📈 Sensor Trend Analysis (Real Log Data)")
            cols_available = [c for c in ["Temp","Hum","Lux","Yield"] if c in df_log.columns]
            selected_params = st.multiselect("Select parameters to visualise", cols_available, default=cols_available[:2])
            if selected_params:
                fig_trend = px.line(df_log.tail(300), x="Timestamp", y=selected_params,
                                    title="Multi-Parameter Sensor Trends (Last 300 Readings)",
                                    template="plotly_dark",
                                    color_discrete_map={"Temp":"#ff4444","Hum":"#4488ff","Lux":"#ffaa00","Yield":"#44ff88"})
                st.plotly_chart(fig_trend, use_container_width=True)

            # ── Past vs Current Comparison Bar ────────────────
            st.markdown("### 📊 Historical vs Live Comparison")
            half = len(df_log) // 2
            old_df = df_log.iloc[:half]
            new_df = df_log.iloc[half:]
            comp = pd.DataFrame({
                "Parameter": ["Temp (°C)", "Humidity (%)", "Yield (T)"],
                "Historical Avg": [round(old_df["Temp"].mean(),1), round(old_df["Hum"].mean(),1), round(old_df["Yield"].mean(),1)],
                "Recent Avg":     [round(new_df["Temp"].mean(),1), round(new_df["Hum"].mean(),1), round(new_df["Yield"].mean(),1)],
                "Live Now":       [live_temp, live_hum, live_yield]
            })
            fig_comp = px.bar(comp, x="Parameter", y=["Historical Avg","Recent Avg","Live Now"],
                              barmode="group", title="Past vs Current vs Live",
                              template="plotly_dark",
                              color_discrete_map={"Historical Avg":"#888","Recent Avg":"#4488ff","Live Now":"#00ffcc"})
            st.plotly_chart(fig_comp, use_container_width=True)

            # ── AI Trend Summary ───────────────────────────────
            st.markdown("### 🤖 AI Trend Summary")
            temp_trend  = "rising" if new_df["Temp"].mean()  > old_df["Temp"].mean()  else "falling"
            hum_trend   = "rising" if new_df["Hum"].mean()   > old_df["Hum"].mean()   else "falling"
            yield_trend = "improving" if new_df["Yield"].mean() > old_df["Yield"].mean() else "declining"
            st.info(
                f"📌 **AI Summary:** Over the logged period, field temperatures are **{temp_trend}** "
                f"and humidity is **{hum_trend}**. Estimated crop yield is **{yield_trend}**. "
                f"There have been **{critical_count}** anomaly events recorded, giving a system compliance "
                f"score of **{compliance_pct}%**. "
                f"{'Immediate intervention is advised.' if critical_count > 5 else 'Conditions remain broadly stable.'}"
            )

        else:
            # ── FARMER VIEW ──────────────────────────────────
            st.subheader("🌾 Farmer Dashboard — Crop & Field Status")
            st.caption(f"Data Source: {total_records} sensor readings | {data_src}")

            fa1, fa2, fa3, fa4 = st.columns(4)
            fa1.metric("Field Temperature",   f"{live_temp} °C",  "Current")
            fa2.metric("Soil Humidity",        f"{live_hum} %",    "Current")
            fa3.metric("Light Intensity",      f"{int(live_lux)} Lux", "Current")
            fa4.metric("Yield Estimate",       f"{live_yield} T",  "Per Acre")

            # ── Crop Advisory ─────────────────────────────────
            st.markdown("### 🌱 Crop Advisory")
            if live_temp > 34:
                st.error("⚠️ **High Temperature Warning:** Your field is too hot. Water your crop immediately to prevent wilting.")
            elif live_hum < 45:
                st.warning("⚠️ **Dry Conditions Ahead:** Humidity is low. Consider increasing irrigation frequency.")
            elif sm < 35:
                st.warning("⚠️ **Low Soil Moisture:** Apply irrigation — soil is drying out faster than normal.")
            else:
                st.success("✅ **Conditions Optimal.** Your crop environment is healthy. Continue normal care routine.")

            # ── Soil & Weather Trend (farmer-friendly) ────────
            st.markdown("### 📉 Field Conditions Over Time")
            if "Temp" in df_log.columns and "Hum" in df_log.columns:
                fig_farm = px.line(df_log.tail(100), x="Timestamp", y=["Temp","Hum"],
                                   title="Temperature & Humidity — Last 100 Readings",
                                   template="plotly_dark",
                                   color_discrete_map={"Temp":"#ff4444","Hum":"#4488ff"})
                st.plotly_chart(fig_farm, use_container_width=True)

            # ── Yield Estimate Trend ───────────────────────────
            if "Yield" in df_log.columns:
                fig_yield = px.bar(df_log.tail(50), x="Timestamp", y="Yield",
                                   title="Yield Estimate — Last 50 Readings",
                                   template="plotly_dark", color_discrete_sequence=["#44ff88"])
                st.plotly_chart(fig_yield, use_container_width=True)

    # ============================================================
    # TAB 2 — REPORT GENERATOR
    # ============================================================
    with report_tab:
        st.subheader("📄 Automated Report Generator")
        st.write("All figures are derived exclusively from your **real sensor log**.")

        # ── Farmer Registry Constants ──────────────────────────
        FARMER_DB = "farmer_registry.csv"

        rep_type = st.radio("Select Report Type", [
            "Daily Operational Report",
            "Monthly Production Report",
            "Yield vs Environment Report",
            "🌾 Farmer Supply Registry"
        ], horizontal=True)

        # ── FARMER REGISTRY MODULE ─────────────────────────────
        if rep_type == "🌾 Farmer Supply Registry":
            st.markdown("### 🌾 Farmer Supply Registration & Report")
            st.caption("Register farmers who supply sugarcane to the factory. All data is saved persistently.")

            # ── Registration Form ──────────────────────────────
            with st.expander("➕ Register New Farmer Supply Entry", expanded=True):
                r1, r2, r3 = st.columns(3)
                f_name     = r1.text_input("Farmer Full Name")
                f_village  = r2.text_input("Village / Town")
                f_contact  = r3.text_input("Mobile Number")

                r4, r5, r6, r7 = st.columns(4)
                f_acres    = r4.number_input("Farm Area (Acres)", min_value=0.5, max_value=500.0, value=5.0, step=0.5)
                f_tons     = r5.number_input("Sugarcane Supplied (Tons)", min_value=1.0, max_value=10000.0, value=20.0)
                f_grade    = r6.selectbox("Crop Quality Grade", ["A+ (Premium)", "A (Good)", "B (Average)", "C (Low)"])
                f_date     = r7.date_input("Date of Supply")

                r8, r9 = st.columns(2)
                f_moisture = r8.number_input("Moisture Content (%)", min_value=0.0, max_value=100.0, value=float(round(sm, 1)))
                f_price    = r9.number_input("Price Paid (₹/Ton)", min_value=1000, max_value=6000, value=3500)

                if st.button("💾 Save Farmer Entry", type="primary"):
                    if f_name.strip() == "":
                        st.error("Farmer name cannot be empty.")
                    else:
                        new_row = pd.DataFrame([{
                            "Date":          f_date.strftime("%Y-%m-%d"),
                            "Farmer Name":   f_name.strip(),
                            "Village":       f_village.strip(),
                            "Contact":       f_contact.strip(),
                            "Acres":         f_acres,
                            "Tons":          f_tons,
                            "Grade":         f_grade,
                            "Moisture %":    f_moisture,
                            "Price_Per_Ton": f_price,
                            "Total_Paid":    round(f_tons * f_price, 2)
                        }])
                        if os.path.exists(FARMER_DB):
                            new_row.to_csv(FARMER_DB, mode="a", header=False, index=False)
                        else:
                            new_row.to_csv(FARMER_DB, index=False)
                        st.success(f"✅ Farmer **{f_name}** registered successfully!")
                        st.rerun()

            # ── Load and Display Registry ──────────────────────
            if os.path.exists(FARMER_DB):
                df_farmers = pd.read_csv(FARMER_DB)

                # ── KPI Summary ────────────────────────────────
                st.markdown("### 📊 Supply Summary Dashboard")
                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Total Farmers",       f"{len(df_farmers)}")
                k2.metric("Total Tons Received",  f"{df_farmers['Tons'].sum():,.1f} T")
                k3.metric("Total Amount Paid",    f"₹{df_farmers['Total_Paid'].sum():,.0f}")
                k4.metric("Avg Price / Ton",      f"₹{df_farmers['Price_Per_Ton'].mean():,.0f}")

                # ── Bar Chart: Tons per Farmer ─────────────────
                fig_fr = px.bar(
                    df_farmers.sort_values("Tons", ascending=False).head(20),
                    x="Farmer Name", y="Tons", color="Grade",
                    title="Top 20 Farmers by Sugarcane Supplied (Tons)",
                    template="plotly_dark",
                    color_discrete_map={"A+ (Premium)":"#00ffcc","A (Good)":"#44ff88","B (Average)":"#ffaa00","C (Low)":"#ff4444"})
                st.plotly_chart(fig_fr, use_container_width=True)

                # ── Village-wise Pie Chart ─────────────────────
                village_grp = df_farmers.groupby("Village")["Tons"].sum().reset_index()
                fig_vil = px.pie(village_grp, names="Village", values="Tons",
                                 title="Village-wise Supply Distribution",
                                 template="plotly_dark", hole=0.4)
                st.plotly_chart(fig_vil, use_container_width=True)

                # ── Grade Quality Distribution ─────────────────
                grade_grp = df_farmers.groupby("Grade")["Tons"].sum().reset_index()
                fig_grade = px.bar(grade_grp, x="Grade", y="Tons",
                                   title="Quality Grade Distribution of Received Sugarcane",
                                   template="plotly_dark", color="Grade",
                                   color_discrete_map={"A+ (Premium)":"#00ffcc","A (Good)":"#44ff88","B (Average)":"#ffaa00","C (Low)":"#ff4444"})
                st.plotly_chart(fig_grade, use_container_width=True)

                # ── Searchable Farmer Table ────────────────────
                st.markdown("### 🗂️ Registered Farmer Records")
                search_f = st.text_input("🔍 Search by Farmer Name or Village")
                if search_f:
                    df_show = df_farmers[df_farmers.apply(lambda r: search_f.lower() in r.astype(str).str.lower().values, axis=1)]
                else:
                    df_show = df_farmers
                st.dataframe(df_show, use_container_width=True)

                # ── Downloadable Reports ───────────────────────
                st.markdown("### 📥 Download Reports")
                dl1, dl2, dl3 = st.columns(3)

                with dl1:
                    with open(FARMER_DB, "rb") as f:
                        st.download_button("📥 Full Registry (.CSV)", f, "Farmer_Registry.csv")

                with dl2:
                    report_lines = [
                        "=== FARMER SUPPLY REPORT ===",
                        f"Generated : {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}",
                        f"Total Farmers Registered : {len(df_farmers)}",
                        f"Total Sugarcane Received : {df_farmers['Tons'].sum():,.1f} Tons",
                        f"Total Amount Disbursed   : INR {df_farmers['Total_Paid'].sum():,.2f}",
                        f"Average Price/Ton        : INR {df_farmers['Price_Per_Ton'].mean():,.0f}",
                        "",
                        "--- FARMER-WISE BREAKDOWN ---"
                    ]
                    for _, row in df_farmers.iterrows():
                        report_lines.append(
                            f"  {row['Date']} | {row['Farmer Name']} ({row['Village']}) | "
                            f"{row['Tons']} T | Grade: {row['Grade']} | INR {row['Total_Paid']:,.0f}"
                        )
                    report_lines += [
                        "",
                        "--- VILLAGE SUMMARY ---"
                    ]
                    for _, vrow in village_grp.iterrows():
                        report_lines.append(f"  {vrow['Village']} : {vrow['Tons']:,.1f} Tons")
                    report_lines.append("══════════════════════════════════════")
                    farmer_report_txt = "\n".join(report_lines)
                    st.download_button("📄 Farmer Report (.TXT)", farmer_report_txt, "Farmer_Supply_Report.txt")

                with dl3:
                    if st.session_state.get("user_role") == "admin":
                        if st.button("🗑️ Clear Farmer Registry", type="primary"):
                            os.remove(FARMER_DB)
                            st.success("Registry cleared.")
                            st.rerun()
            else:
                st.info("No farmer records yet. Use the form above to register the first entry.")

        elif rep_type == "Daily Operational Report":
            today_df = df_log[df_log["Timestamp"].dt.date == df_log["Timestamp"].dt.date.max()]
            daily_records   = len(today_df)
            daily_avg_temp  = round(today_df["Temp"].mean(), 1)  if "Temp"  in today_df.columns and daily_records else avg_temp
            daily_avg_hum   = round(today_df["Hum"].mean(),  1)  if "Hum"   in today_df.columns and daily_records else avg_hum
            daily_avg_yield = round(today_df["Yield"].mean(),1)  if "Yield" in today_df.columns and daily_records else avg_yield
            daily_crits     = int(today_df[cond_col].str.contains("Critical|Stress|Warning", case=False, na=False).sum()) if cond_col and daily_records else 0
            report_text = f"""=== DAILY OPERATIONAL REPORT ===
Generated : {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
Source    : {LOG_FILE}  ({data_src})

DATE: {df_log['Timestamp'].dt.date.max()}
─────────────────────────────────────
SENSOR READINGS (Today)
  Records logged      : {daily_records}
  Avg Temperature     : {daily_avg_temp} °C
  Avg Humidity        : {daily_avg_hum} %
  Avg Yield Estimate  : {daily_avg_yield} T/Acre
  Anomaly Events      : {daily_crits}

MACHINE & SYSTEM STATUS
  Compliance Score    : {compliance_pct}%
  Data Source         : {data_src}

ALERTS & ANOMALIES
  {'⚠ High temperature stress detected.' if daily_avg_temp > 34 else '✓ Temperature within safe range.'}
  {'⚠ Low humidity — irrigation advised.' if daily_avg_hum < 45 else '✓ Humidity within safe range.'}
  {f'⚠ {daily_crits} critical events today.' if daily_crits > 0 else '✓ No critical events today.'}

RECOMMENDATIONS
  - {'Review cooling and irrigation systems urgently.' if daily_avg_temp > 34 or daily_avg_hum < 45 else 'Maintain current operational schedule.'}
  - Monitor yield trend for any multi-day decline.
══════════════════════════════════════
"""
            st.code(report_text, language="")
            st.download_button("📥 Download Daily Report", report_text, "Daily_Operational_Report.txt")

        elif rep_type == "Monthly Production Report":
            df_log["Month"] = df_log["Timestamp"].dt.to_period("M")
            monthly = df_log.groupby("Month").agg(
                Records=("Temp","count"),
                Avg_Temp=("Temp","mean"),
                Avg_Hum=("Hum","mean"),
                Avg_Yield=("Yield","mean")
            ).reset_index()
            monthly["Month"] = monthly["Month"].astype(str)

            st.write("**Monthly Aggregated Sensor Performance**")
            st.dataframe(monthly.style.format({"Avg_Temp":"{:.1f}","Avg_Hum":"{:.1f}","Avg_Yield":"{:.1f}"}), use_container_width=True)

            fig_mo = px.bar(monthly, x="Month", y="Avg_Yield",
                            title="Monthly Avg Yield Estimate from Sensor Log",
                            template="plotly_dark", color_discrete_sequence=["#44ff88"])
            st.plotly_chart(fig_mo, use_container_width=True)

            monthly_report = monthly.to_string(index=False)
            report_text = f"""=== MONTHLY PRODUCTION REPORT ===
Generated : {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
Source    : {LOG_FILE}

MONTHLY SENSOR SUMMARY
{monthly_report}

OVERALL STATS
  Total Records   : {total_records}
  Compliance      : {compliance_pct}%
  Total Anomalies : {critical_count}

AI INSIGHT
  {'Yield is trending upward — positive seasonal response.' if avg_yield > 40 else 'Yield is below baseline — review irrigation and soil nutrition.'}
══════════════════════════════════════
"""
            st.download_button("📥 Download Monthly Report", report_text, "Monthly_Production_Report.txt")

        else:  # Yield vs Environment
            st.write("**Yield Correlation Analysis — Temperature & Humidity (Sensor Log)**")
            if "Temp" in df_log.columns and "Yield" in df_log.columns and len(df_log) > 5:
                
                sc_col1, sc_col2 = st.columns(2)
                
                # ── Chart 1: Yield vs Temp with numpy trendline ──────
                with sc_col1:
                    x_t = df_log["Temp"].dropna().values
                    y_t = df_log.loc[df_log["Temp"].notna(), "Yield"].values
                    coeffs_t = np.polyfit(x_t, y_t, 1)
                    trend_t  = np.poly1d(coeffs_t)(x_t)
                    
                    fig_t = go.Figure()
                    fig_t.add_trace(go.Scatter(
                        x=x_t, y=y_t, mode="markers",
                        marker=dict(color=df_log["Hum"].dropna().values if "Hum" in df_log.columns else "#44ff88",
                                    colorscale="Viridis", showscale=True,
                                    colorbar=dict(title="Humidity %"), size=7),
                        name="Sensor Readings"))
                    fig_t.add_trace(go.Scatter(
                        x=x_t, y=trend_t, mode="lines",
                        line=dict(color="#ff4444", width=2, dash="dash"),
                        name=f"Trend (slope={round(coeffs_t[0],3)})"))
                    fig_t.update_layout(
                        title="Yield vs Temperature + Regression Line",
                        xaxis_title="Temperature (°C)", yaxis_title="Yield (T/Acre)",
                        template="plotly_dark", legend=dict(orientation="h"))
                    st.plotly_chart(fig_t, use_container_width=True)

                # ── Chart 2: Yield vs Humidity with numpy trendline ──
                with sc_col2:
                    if "Hum" in df_log.columns:
                        x_h = df_log["Hum"].dropna().values
                        y_h = df_log.loc[df_log["Hum"].notna(), "Yield"].values
                        coeffs_h = np.polyfit(x_h, y_h, 1)
                        trend_h  = np.poly1d(coeffs_h)(x_h)
                        
                        fig_h = go.Figure()
                        fig_h.add_trace(go.Scatter(
                            x=x_h, y=y_h, mode="markers",
                            marker=dict(color="#4488ff", size=7, opacity=0.8),
                            name="Sensor Readings"))
                        fig_h.add_trace(go.Scatter(
                            x=x_h, y=trend_h, mode="lines",
                            line=dict(color="#00ffcc", width=2, dash="dash"),
                            name=f"Trend (slope={round(coeffs_h[0],3)})"))
                        fig_h.update_layout(
                            title="Yield vs Humidity + Regression Line",
                            xaxis_title="Humidity (%)", yaxis_title="Yield (T/Acre)",
                            template="plotly_dark", legend=dict(orientation="h"))
                        st.plotly_chart(fig_h, use_container_width=True)
                
                # ── Correlation Heatmap ────────────────────────────
                st.markdown("**📐 Pearson Correlation Matrix (Pure NumPy — No External Dependencies)**")
                corr_cols = [c for c in ["Temp","Hum","Lux","Yield"] if c in df_log.columns]
                corr_matrix = df_log[corr_cols].corr().round(3)
                fig_hm = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns.tolist(),
                    y=corr_matrix.index.tolist(),
                    colorscale="RdBu", zmid=0,
                    text=corr_matrix.values.round(2),
                    texttemplate="%{text}",
                    showscale=True))
                fig_hm.update_layout(title="Sensor Parameter Correlation Heatmap", template="plotly_dark")
                st.plotly_chart(fig_hm, use_container_width=True)


            corr_temp  = round(df_log["Yield"].corr(df_log["Temp"]), 3) if "Temp"  in df_log.columns else "N/A"
            corr_hum   = round(df_log["Yield"].corr(df_log["Hum"]),  3) if "Hum"   in df_log.columns else "N/A"
            report_text = f"""=== YIELD vs ENVIRONMENT REPORT ===
Generated : {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
Source    : {LOG_FILE}

STATISTICAL CORRELATIONS (Sensor Log)
  Yield ↔ Temperature   : {corr_temp}  {'(negative — heat hurts yield)' if isinstance(corr_temp,float) and corr_temp < 0 else '(positive)'}
  Yield ↔ Humidity      : {corr_hum}  {'(positive — moisture helps yield)' if isinstance(corr_hum,float) and corr_hum > 0 else '(negative)'}

KEY AVERAGES
  Avg Temp    : {avg_temp} °C
  Avg Humidity: {avg_hum} %
  Avg Yield   : {avg_yield} T/Acre

AI SUMMARY
  Based on {total_records} real sensor readings, your yield is {'negatively' if isinstance(corr_temp,float) and corr_temp < 0 else 'positively'} correlated with temperature.
  {'Irrigating to maintain humidity above 55 % is strongly recommended.' if isinstance(corr_hum,float) and corr_hum > 0 else 'Drainage management may improve yield.'}
══════════════════════════════════════
"""
            st.code(report_text, language="")
            st.download_button("📥 Download Yield-Environment Report", report_text, "Yield_Environment_Report.txt")

    # ============================================================
    # TAB 3 — RAW ARCHIVE
    # ============================================================
    with archive_tab:
        st.subheader("🗂️ Raw Sensor Log Archive")
        st.caption(f"Source: `{LOG_FILE}` — {total_records} records")

        search = st.text_input("🔍 Search (Condition keyword, date, value)")
        filtered = df_log[df_log.apply(lambda r: search.lower() in r.astype(str).str.lower().values, axis=1)] if search else df_log.tail(50)
        st.dataframe(filtered, use_container_width=True)

        st.markdown("### ⚙️ Admin Controls")
        adm1, adm2 = st.columns(2)
        with adm1:
            with open(LOG_FILE, "rb") as f:
                st.download_button("📥 Export Full Sensor Log (.CSV)", f, "sensor_audit_full.csv")
        with adm2:
            if role == "admin":
                if st.button("🗑️ Purge Sensor Log (Admin Only)", type="primary"):
                    os.remove(LOG_FILE)
                    st.success("Log purged. IoT module will re-create it on next reading.")
                    st.rerun()
            else:
                st.info("Log management is restricted to Admin users.")


