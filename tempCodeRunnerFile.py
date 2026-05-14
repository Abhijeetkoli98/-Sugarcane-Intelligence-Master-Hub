import streamlit as st
import serial
import time

ser = serial.Serial("COM8", 9600)  # use your COM port
time.sleep(2)

st.title("🌱 Smart Agriculture Dashboard")

while True:
    data = ser.readline().decode(errors='ignore').strip()
    
    if data != "":
        st.metric("Light Value", data)