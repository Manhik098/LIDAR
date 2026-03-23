import numpy as np
import matplotlib.pyplot as plt
import importlib.util
import sys

# Load config from 1_config.py
def load_config():
    spec = importlib.util.spec_from_file_location("config", "1_config.py")
    config = importlib.util.module_from_spec(spec)
    sys.modules["config"] = config
    spec.loader.exec_module(config)
    return config

config = load_config()

C = config.C
TIME_RESOLUTION = config.TIME_RESOLUTION
NUM_BINS = config.NUM_BINS


def process_data(timestamps):
    if len(timestamps) == 0:
        print("❌ No data received")
        return

    # Convert to time
    times = np.array(timestamps) * TIME_RESOLUTION

    # Histogram
    hist, bins = np.histogram(times, bins=NUM_BINS)

    # Plot histogram
    plt.figure()
    plt.plot(bins[:-1], hist)
    plt.xlabel("Time (s)")
    plt.ylabel("Photon Counts")
    plt.title("Histogram")
    plt.grid()
    plt.show()

    # Peak detection
    peak_index = np.argmax(hist)
    peak_time = bins[peak_index]

    # Distance calculation
    distance = (C * peak_time) / 2

    print(f"📏 Estimated Distance: {distance:.3f} meters")