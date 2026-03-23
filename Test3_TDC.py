import pyTempico as tp

# STEP 1: Create search object
devices = tp.TempicoDevicesSearch()

# STEP 2: Find devices
device_list = devices.findDevices()

print("Devices found:", device_list)

# STEP 3: Connect if available
if len(device_list) > 0:
    device = tp.TempicoDevice(device_list[0])

    device.open()
    print("✅ Connected to TDC")

    device.close()
else:
    print("❌ No TDC device found")