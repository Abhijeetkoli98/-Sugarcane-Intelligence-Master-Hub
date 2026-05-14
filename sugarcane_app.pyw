import webview
import subprocess
import time
import sys
import os

# --- CONFIG ---
STREAMLIT_PATH = r"c:\Users\ABHIJEET\OneDrive\Desktop\app.py"

def start_streamlit():
    """Starts the Streamlit server in the background"""
    # Use 'python -m streamlit' for better compatibility
    cmd = ["python", "-m", "streamlit", "run", STREAMLIT_PATH, "--server.headless", "true"]
    
    # DETACHED_PROCESS flag ensures the console window stays hidden on Windows
    if os.name == 'nt':
        return subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        return subprocess.Popen(cmd)

def main():
    print("Launching Sugarcane AI Desktop...")
    
    # 1. Start the backend engine
    server_process = start_streamlit()
    
    # 2. Wait for the server to warm up
    time.sleep(5)
    
    # 3. Create the Desktop Window
    window = webview.create_window(
        'Sugarcane AI Industrial Pro+', 
        'http://localhost:8501',
        width=1200, 
        height=800,
        resizable=True,
        confirm_close=True
    )
    
    # 4. Start the Window
    try:
        webview.start()
    finally:
        # 5. Clean up: Kill the background server when window closes
        server_process.terminate()

if __name__ == '__main__':
    main()
