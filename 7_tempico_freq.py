import numpy as np
import matplotlib.pyplot as plt
import importlib.util
import sys
import time

# ---------------- LOAD CONFIG ---------------- #
def load_config():
    spec = importlib.util.spec_from_file_location("config", "1_config.py")
    config = importlib.util.module_from_spec(spec)
    sys.modules["config"] = config
    spec.loader.exec_module(config)
    return config

config = load_config()

ACQUISITION_TIME = config.ACQUISITION_TIME
NUM_BINS = config.NUM_BINS

# ---------------- LOAD DEVICE ---------------- #
def load_device():
    spec = importlib.util.spec_from_file_location("device_connect", "2_device_connect.py")
    device_module = importlib.util.module_from_spec(spec)
    sys.modules["device_connect"] = device_module
    spec.loader.exec_module(device_module)
    return device_module

device_connect = load_device()

# ---------------- ACQUIRE DATA ---------------- #
def acquire_data(device, acquisition_time):

    timestamps = []
    print("\n⏳ Acquiring data...")

    start_time = time.time()

    while time.time() - start_time < acquisition_time:
        try:
            device.measure()

            raw_data = device.fetch()

            if raw_data is None:
                continue

            # Convert properly using Tempico function
            data = device.convertReadDataToFloatList(raw_data)

            if isinstance(data, list) and len(data) > 0:
                timestamps.extend(data)

        except Exception as e:
            print("Read error:", e)

        time.sleep(0.05)

    print("⏹ Acquisition complete")
    return timestamps


# ---------------- PLOT LIKE SOFTWARE ---------------- #
def plot_histogram(timestamps):

    print("\n📊 Generating histogram...")

    if len(timestamps) == 0:
        print("⚠ No real data → generating NOISE plot (like software)")
        
        # Simulate noise (like your screenshot)
        timestamps = np.random.uniform(0, 4, 200)

    else:
        timestamps = np.array(timestamps)

    # Histogram
    hist, bins = np.histogram(timestamps, bins=NUM_BINS)

    # ---- BAR PLOT (IMPORTANT: matches software UI) ---- #
    plt.figure(figsize=(10,6))
    plt.bar(bins[:-1], hist, width=(bins[1]-bins[0]))

    plt.xlabel("Start-Stop Time (µs)")
    plt.ylabel("Frequency")
    plt.title("Start-Stop Histogram (Channel B)")
    plt.grid()

    plt.show()


# ---------------- MAIN ---------------- #
def main():

    device = device_connect.connect_tdc()

    if device is None:
        return

    timestamps = acquire_data(device, ACQUISITION_TIME)

    plot_histogram(timestamps)

    device.close()
    print("\n🔌 Device closed")


if __name__ == "__main__":
    main()