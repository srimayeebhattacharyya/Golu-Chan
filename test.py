import sounddevice as sd

devices = sd.query_devices()

for i, d in enumerate(devices):
    print(i, ":", d["name"], "| IN:", d["max_input_channels"], "| OUT:", d["max_output_channels"])