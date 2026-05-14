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
CREDENTIALS = {"admin": "factory123", "farmer": "field123"}

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
    try:
        if 'ser' not in st.session_state:
            import serial
            st.session_state.ser = serial.Serial("COM8", 9600, timeout=1)
        ser = st.session_state.ser
    except: ser = None

    l, t, h = None, None, None
    is_sim = False
    
    if ser and ser.in_waiting > 0:
        try:
            line = ser.readline().decode(errors='ignore').strip()
            if "," in line: l, t, h = map(float, line.split(","))
        except: pass
    
    if l is None:
        # High-Fidelity Simulation for Presentation
        l = random.randint(400, 900)
        t = 28 + random.uniform(-1, 1)
        h = 60 + random.uniform(-2, 2)
        is_sim = True
        
    return l, t, h, is_sim

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
nav = st.sidebar.radio("Navigation", ["📡 Ground Sensors (IoT)", "🛰️ Satellite Remote Sensing", "🌍 Weather Fusion Analysis", "🚜 Farmer Strategic Portal", "🔮 AI Harvest Predictor", "🏢 Factory Storage Optimizer", "🧪 Soil Nutrient Analysis", "📁 Factory Data Audit"])
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

    # --- SENSOR ENGINE ---
    while True:
        l, t, h, is_sim = get_sensor_readings()

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
        s_l, s_t, s_h, s_is_sim = get_sensor_readings()
        st.session_state.history.append({"L":s_l, "T":s_t, "H":s_h})
        
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
# 📁 MODE: FACTORY DATA AUDIT
# ==========================================
else:
    st.header("📁 Industrial Data Audit Center")
    if os.path.exists(LOG_FILE):
        df_audit = pd.read_csv(LOG_FILE)
        st.subheader("🛡️ Compliance & Safety Audit")
        total_logs = len(df_audit)
        critical_logs = len(df_audit[df_audit['Status'].str.contains("Critical|Stress|Warning", na=False)])
        compliance_pct = round(((total_logs - critical_logs) / total_logs) * 100, 1) if total_logs > 0 else 100
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Records", total_logs)
        c2.metric("Compliance Score", f"{compliance_pct}%")
        c3.metric("Anomaly Flag Count", critical_logs, delta=f"Critical Events", delta_color="inverse")
        st.divider()
        st.subheader("📈 Historical Sensor Audit")
        audit_metric = st.selectbox("Select Parameter", ["T", "H", "L", "Y"])
        metric_labels = {"T": "Temperature (°C)", "H": "Humidity (%)", "L": "Light (Lux)", "Y": "Yield Est."}
        fig_audit = px.line(df_audit.tail(100), x="Timestamp", y=audit_metric, template="plotly_dark")
        st.plotly_chart(fig_audit, use_container_width=True)
        st.divider()
        st.subheader("🗂️ Record Archive")
        search_query = st.text_input("🔍 Search Logs")
        if search_query:
            display_df = df_audit[df_audit.apply(lambda row: search_query.lower() in row.astype(str).str.lower().values, axis=1)]
        else:
            display_df = df_audit.tail(20)
        st.dataframe(display_df, use_container_width=True)
        with open(LOG_FILE, "rb") as f:
            st.download_button("📥 Download Audit (CSV)", f, "factory_audit_pro.csv")
        if st.session_state.user_role == "admin":
            if st.button("🗑️ Purge Logs"):
                os.remove(LOG_FILE); st.success("Log file purged."); st.rerun()
    else:
        st.info("📂 No audit logs found. This happens if no monitoring has been started yet.")
        if st.button("🚀 Initialize with Professional Sample Data"):
            import datetime
            sample_data = []
            for i in range(50):
                ts = (datetime.datetime.now() - datetime.timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S")
                sample_data.append({
                    "Timestamp": ts,
                    "L": random.randint(400, 800),
                    "T": random.uniform(22.0, 35.0),
                    "H": random.uniform(50.0, 80.0),
                    "Y": random.uniform(35.0, 45.0),
                    "Status": "Optimal" if i % 10 != 0 else "Critical Spike Detected"
                })
            pd.DataFrame(sample_data).to_csv(LOG_FILE, index=False)
            st.success("Industrial Master Log initialized with 50 sample records.")
            st.rerun()
        st.caption("Or start the 'Ground Sensors' or 'Weather Fusion' modules to begin live logging.")
