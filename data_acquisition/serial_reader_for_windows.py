# -*- coding: utf-8 -*-
import serial
import struct
import numpy as np
import matplotlib.pyplot as plt

chunk_index = 0

# Serial port for Windows (update COM port as needed)
ser = serial.Serial('COM3', 115200, timeout=None)  # blocking read

SAMPLE_RATE_HZ = 860 #SPS
SAMPLE_INTERVAL = 1.0 / SAMPLE_RATE_HZ #Seconds per sample

# Number of samples per chunk (must match Raspberry Pi CHUNK_SIZE)
CHUNK_DURATION_SECONDS = 0.15
CHUNK_SIZE = int(SAMPLE_RATE_HZ * CHUNK_DURATION_SECONDS)

def read_chunk(ser, chunk_size):
    """
    Blocking read: reads exactly one chunk of floats from the serial port
    """
    num_bytes = chunk_size * 4  # 4 bytes per float
    data = b''
    while len(data) < num_bytes:
        data += ser.read(num_bytes - len(data))
    
    # Convert binary data to floats
    chunk = struct.unpack(f'{chunk_size}f', data)
    #print(f"Chunk {chunk_index} received: {chunk}")
    return np.array(chunk)

# Setup real-time plot
plt.ion()
fig, ax = plt.subplots(figsize=(8, 3))
line, = ax.plot([], [])
ax.set_ylim(-0.003, 0.003)  # expected voltage range
ax.set_xlim(0, CHUNK_DURATION_SECONDS)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude (V)')
ax.grid(True)

t = np.linspace(0, CHUNK_DURATION_SECONDS, CHUNK_SIZE)

chunk_index = 0
while True:
    print("Waiting for data...")
    chunk = read_chunk(ser, CHUNK_SIZE)
    
    # Compute voltage range
    v_min = np.min(chunk)
    v_max = np.max(chunk)
    v_pp = v_max - v_min
    print(f"Chunk {chunk_index}: min={v_min:.4f} V, max={v_max:.4f} V, peak-to-peak={v_pp:.4f} V")

    # Update plot
    line.set_data(t, chunk)
    ax.set_title(f'Chunk {chunk_index}')
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.001)  # force update

    chunk_index += 1
