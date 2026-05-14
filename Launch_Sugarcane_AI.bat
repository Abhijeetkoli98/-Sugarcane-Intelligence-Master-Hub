@echo off
title Sugarcane AI Industrial Hub Launcher
echo Starting Industrial Sugarcane AI System...
echo Please wait while the AI engine initializes...
start /min cmd /c "streamlit run c:\Users\ABHIJEET\OneDrive\Desktop\app.py --server.headless true"
timeout /t 5 /nobreak > nul
start http://localhost:8501
exit
