import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import time
import pyTempico as tp

# ==============================
# CONFIG
# ==============================

TIME_RESOLUTION = 1e-10   # 100 ps
NUM_BINS = 200
WINDOW_SIZE = 5000
REFRESH_RATE = 0.2

START_CHANNEL = 1
STOP_CHANNEL = 2


# ==============================
# CONNECT TO TDC
# ==============================

def connect_tdc():
    devices = tp.TempicoDevicesSearch()
    device_list = devices.findDevices()

    if len(device_list) == 0:
        print("❌ No TDC found")
        return None

    device = tp.TempicoDevice(device_list[0])
    device.open()

    print("✅ TDC Connected")

    # Enable channels
    device.enableChannel(START_CHANNEL)
    device.enableChannel(STOP_CHANNEL)

    # Edge config
    device.setStartEdge(START_CHANNEL, "RISe")
    device.setStopEdge(STOP_CHANNEL, "RISe")

    device.setNumberOfRuns(100)

    return device


# ==============================
# FETCH DATA (FAST LOOP)
# ==============================

def fetch_data(device):

    timestamps = []

    try:
        device.measure()
        data = device.fetch()

        if isinstance(data, list) and len(data) > 0:
            timestamps.extend(data)

    except Exception as e:
        print("Read error:", e)

    return timestamps


# ==============================
# LIVE STREAMING
# ==============================

def live_stream(device):

    buffer = deque(maxlen=WINDOW_SIZE)

    plt.ion()
    fig, ax = plt.subplots(figsize=(9,5))

    print("📡 Starting LIVE acquisition...\n")

    while True:

        # 🔥 GET REAL DATA FROM TDC
        new_data = fetch_data(device)

        buffer.extend(new_data)

        if len(buffer) == 0:
            continue

        # Convert to time
        delta_t = np.array(buffer) * TIME_RESOLUTION
        delta_t_ns = delta_t * 1e9

        # Histogram
        hist, bins = np.histogram(delta_t_ns, bins=NUM_BINS)
        bin_centers = (bins[:-1] + bins[1:]) / 2

        # Plot update
        ax.clear()

        ax.bar(bin_centers, hist,
               width=(bins[1]-bins[0]),
               alpha=0.4,
               label="Counts")

        ax.plot(bin_centers, hist, lw=2, label="Trend")

        ax.set_xlabel("Start-Stop Time (ns)")
        ax.set_ylabel("Counts")
        ax.set_title("🔴 Live Tempico-style Histogram (REAL DATA)")
        ax.grid()
        ax.legend()

        plt.pause(REFRESH_RATE)


# ==============================
# MAIN
# ==============================

def main():

    print("🔌 Connecting to TDC...\n")

    device = connect_tdc()

    if device is None:
        return

    try:
        live_stream(device)

    except KeyboardInterrupt:
        print("\n⏹ Stopping...")

    finally:
        device.close()
        print("🔌 Device closed")


if __name__ == "__main__":
    main()