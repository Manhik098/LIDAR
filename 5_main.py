# 5_main.py

import importlib.util
import sys

# Function to load module from file
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# Load modules
config = load_module("config_mod", "1_config.py")
device_connect = load_module("device_connect_mod", "2_device_connect.py")
acquisition = load_module("acquisition_mod", "3_acquisition.py")
processing = load_module("processing_mod", "4_processing.py")


def main():
    print("🔌 Connecting to TDC...")
    device = device_connect.connect_tdc()

    if device is None:
        return
    
    # 🔥 PRINT DEVICE METHODS (CRITICAL STEP)
    print("\n📡 AVAILABLE DEVICE METHODS:\n")
    for method in dir(device):
        if not method.startswith("_"):
            print(method)

    print("\n⏳ Starting data acquisition...\n")

    try:
        timestamps = acquisition.acquire_data(device, config.ACQUISITION_TIME)
    except Exception as e:
        print("❌ Acquisition Error:", e)
        device.close()
        return

    print("\n📊 Processing data...\n")
    processing.process_data(timestamps)

    device.close()
    print("\n🔌 Device closed successfully")


if __name__ == "__main__":
    main()