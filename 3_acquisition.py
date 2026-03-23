# 3_acquisition.py

import time

def acquire_data(device, acquisition_time):
    timestamps = []

    print("▶ Starting measurement...")

    start_time = time.time()

    while time.time() - start_time < acquisition_time:
        try:
            # Trigger measurement
            device.measure()

            # Fetch data
            data = device.fetch()

            # 🔥 FIX: handle LIST directly
            if isinstance(data, list) and len(data) > 0:
                timestamps.extend(data)

        except Exception as e:

            print("Read error:", e)

        time.sleep(0.1)

    print("⏹ Acquisition complete")
    return timestamps 