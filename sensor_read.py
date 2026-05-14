import serial
import time

ser = serial.Serial("COM8", 9600)   # use your correct COM
time.sleep(2)

while True:
    data = ser.readline().decode(errors='ignore').strip()
    print("Light:", data)