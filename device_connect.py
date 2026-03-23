import pyTempico as tp

def connect_tdc():
    devices = tp.TempicoDevicesSearch()
    device_list = devices.findDevices()

    if len(device_list) == 0:
        print("❌ No TDC found")
        return None

    device = tp.TempicoDevice(device_list[0])
    device.open()

    print("✅ TDC Connected")

    # Channel mapping
    START = 1
    A = 2

    # Enable channels
    device.enableChannel(START)
    device.enableChannel(A)

    # ✅ CORRECT EDGE FORMAT (VERY IMPORTANT)
    device.setStartEdge(START, "RISe")
    device.setStopEdge(A, "RISe")

    # Basic config
    device.setNumberOfRuns(100)

    return device