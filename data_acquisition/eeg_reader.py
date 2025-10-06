# -*- coding: utf-8 -*-
import serial
import struct
import time
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import serial.tools.list_ports
chunk_index = 0

SAMPLE_RATE_HZ = 860 #SPS
SAMPLE_INTERVAL = 1.0 / SAMPLE_RATE_HZ #Seconds per sample
SAMPLE_RANGE = 0.256 #Max voltage range for ADC PGA

# Number of samples per chunk (must match Raspberry Pi CHUNK_SIZE)
CHUNK_DURATION_SECONDS = 0.15
CHUNK_SIZE = int(SAMPLE_RATE_HZ * CHUNK_DURATION_SECONDS)

CIRCUIT_GAIN = 1164.44 #Circuit gain

CSV_FILE = "eeg_data.csv"

GRAPH_BOUNDS = SAMPLE_RANGE/(2*CIRCUIT_GAIN) # Expected voltage range

# Check if the file exists, then delete it
if os.path.exists(CSV_FILE):
    os.remove(CSV_FILE)
    print(f"{CSV_FILE} has been deleted.")
else:
    print(f"{CSV_FILE} does not exist.")

# Setup real-time plot
plt.ion()
fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=False)

#Full history plot
line, = ax[0].plot([], [])
ax[0].set_ylim(-GRAPH_BOUNDS, GRAPH_BOUNDS)
ax[0].set_xlim(0, CHUNK_DURATION_SECONDS)
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Amplitude (V)')
ax[0].grid(True)

# Last 3 seconds plot
line_last, = ax[1].plot([], [])
ax[1].set_ylim(-GRAPH_BOUNDS, GRAPH_BOUNDS)
ax[1].set_xlim(0, 3)
ax[1].set_title("Last 3 Seconds")
ax[1].set_ylabel("Amplitude (V)")
ax[1].grid(True)

# Current chunk plot
line_chunk, = ax[2].plot([], [])
ax[2].set_ylim(-GRAPH_BOUNDS, GRAPH_BOUNDS)
ax[2].set_xlim(0, CHUNK_DURATION_SECONDS)
ax[2].set_title("Current Chunk")
ax[2].set_xlabel("Time (s)")
ax[2].set_ylabel("Amplitude (V)")
ax[2].grid(True)

fig.tight_layout()

# Store signal data
time_data = []
signal_data = []

t_chunk = np.linspace(0, CHUNK_DURATION_SECONDS, CHUNK_SIZE, endpoint=False)

# Finds serial ports to improve device compatability... Better hope you don't have anything else connected...
def find_serial_port(retries=5, delay=2):
    keywords = ['raspberry', 'usb serial', 'usbmodem', 'ttyusb', 'ch340', 'cp210', 'ftdi']

    for attempt in range(retries):
        ports = list(serial.tools.list_ports.comports())
        if not ports:
            print(f"No serial ports found (attempt {attempt+1}/{retries})...")
            time.sleep(delay)
            continue

        for port in ports:
            desc = port.description.lower()
            device = port.device.lower()
            hwid = port.hwid.lower()

            # Match on device description or hardware ID
            if any(k in desc or k in device or k in hwid for k in keywords):
                print(f"Found Raspberry Pi (or similar device): {port.device} — {port.description}")
                return port.device

        print(f"No matching device found (attempt {attempt+1}/{retries})...")
        time.sleep(delay)

    raise RuntimeError("Could not detect Raspberry Pi serial connection.")
    
# Read chunk sent over serial
def read_chunk(ser, chunk_size):
    num_bytes = chunk_size * 4  # 4 bytes per float
    data = b''
    while len(data) < num_bytes:
        data += ser.read(num_bytes - len(data))
    
    # Convert binary data to floats
    chunk = struct.unpack(f'{chunk_size}f', data)
    #print(f"Chunk {chunk_index} received: {chunk}")
    return np.array(chunk)/CIRCUIT_GAIN

# Appends chunk to created CSV. This CSV will be overwritten on startup so move somewhere else if you would like to save it
def append_chunk_to_csv(time_array, signal_array, filename=CSV_FILE):
    file_exists = os.path.exists(filename)
    
    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["time", "signal"])  # write header only if file is new
        for t, s in zip(time_array, signal_array):
            writer.writerow([t, s])

if __name__ == "__main__":
    try:
        port = find_serial_port()
        ser = serial.Serial(port, 115200, timeout=None)
        print(f"Connected on {ser.port}")
        
        chunk_index = 0
        
        while True:
            print("Waiting for data...")
            chunk = read_chunk(ser, CHUNK_SIZE)
            
            # Compute voltage range
            v_min = np.min(chunk)
            v_max = np.max(chunk)
            v_pp = v_max - v_min
            print(f"Chunk {chunk_index}: min={v_min*10**6:.4f} µV, max={v_max*10**6:.4f} µV, peak-to-peak={v_pp*10**6:.4f} µV")
        
            # Append time-shifted data
            t_shifted = t_chunk + chunk_index * CHUNK_DURATION_SECONDS
            time_data.extend(t_shifted)
            signal_data.extend(chunk)
        
            # Update plot with appended data
            line.set_data(time_data, signal_data)
            ax[0].set_xlim(0, (chunk_index+1) * CHUNK_DURATION_SECONDS)
            
            if(chunk_index * CHUNK_DURATION_SECONDS > 3):
                # Last 3 seconds
                t_min = max(0, (chunk_index + 1) * CHUNK_DURATION_SECONDS - 3)
                mask = np.array(time_data) >= t_min
                line_last.set_data(np.array(time_data)[mask], np.array(signal_data)[mask])
                ax[1].set_xlim(t_min, t_min + 3)
        
            # Current chunk
            line_chunk.set_data(t_chunk, chunk)
            
            append_chunk_to_csv(t_shifted, chunk)
        
            fig.canvas.flush_events()
            plt.pause(0.001)  # force update
        
            chunk_index += 1
            
    except Exception as e:
        print("Serial connection failed:", e)
