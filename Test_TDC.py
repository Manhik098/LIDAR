import serial
import serial.tools.list_ports

print("Available Ports:")
ports = serial.tools.list_ports.comports()

for port in ports:
    print(port.device)

try:
    ser = serial.Serial('COM3', 115200, timeout=1)
    print("✅ Connected to TDC")

    ser.write(b'\n')
    response = ser.readline()

    print("Response:", response)

    ser.close()

except Exception as e:
    print("❌ Error:", e)