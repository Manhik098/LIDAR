import serial

ser = serial.Serial('COM3', 115200, timeout=1)

# Try multiple common commands
commands = [b'*IDN?\n', b'VER?\n', b'START\n', b'\n']

for cmd in commands:
    print(f"Sending: {cmd}")
    ser.write(cmd)
    response = ser.readline()
    print("Response:", response)

ser.close()