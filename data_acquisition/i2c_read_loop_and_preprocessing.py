# -*- coding: utf-8 -*-
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np
from threading import Thread, Lock
import serial
import struct
from collections import deque

SAMPLE_RATE_HZ = 860 #SPS
SAMPLE_INTERVAL = 1.0 / SAMPLE_RATE_HZ #Seconds per sample

SLIDING_BUFFER_SECONDS = 5
SLIDING_BUFFER_SIZE = SLIDING_BUFFER_SECONDS * SAMPLE_RATE_HZ

CHUNK_DURATION_SECONDS = 0.15 #Amount of data sent per step size
CHUNK_SIZE = int(SAMPLE_RATE_HZ * CHUNK_DURATION_SECONDS)

PAD_DURATION_SECONDS = 0.05 #Seconds to pad around data (adds a delay to data received)
PAD_SIZE = int(SAMPLE_RATE_HZ * PAD_DURATION_SECONDS)

i2c = busio.I2C(board.SCL, board.SDA)

ser = serial.Serial('/dev/serial0', 115200)

lock = Lock()

# Create the ADS object and specify the gain
ads = ADS.ADS1115(i2c)
ads.gain = 16
ads.data_rate = 860
chan = AnalogIn(ads, ADS.P0)

#Bandpass filter 1-50 Hz
from scipy.signal import butter, filtfilt

def bandpass_filter(signal, low, high, fs, order=4):
    nyq = 0.5 * fs
    b, a = butter(order, [low / nyq, high / nyq], btype='band')
    
    return filtfilt(b, a, signal)

#Artifact rejection
def interpolate_artifacts(signal, threshold=0.252/2): #ADC clips at 0.253V and 0V
    signal = np.copy(signal)
    artifact_mask = np.abs(signal) > threshold
 
    if np.all(artifact_mask):
            return np.zeros_like(signal)
    
    good_idx = np.where(~artifact_mask)[0]
    bad_idx = np.where(artifact_mask)[0]
    
    #Linear interpolation
    interpolated = np.interp(bad_idx, good_idx, signal[good_idx])
    signal[bad_idx] = interpolated
    
    return signal

# Serialize chunk as binary
def serialize_chunk_binary(chunk):
    return struct.pack(f'{len(chunk)}f', *chunk)

# Worker thread to filter and send chunks
def process_and_send():
    global active_buffer
    prev_pad = None
    
    while True:
        lock.acquire()
        buffer_to_process = active_buffer.copy()
        lock.release()
        
        #Chunk and padding logic to avoid bandpass edge artifacts
        try:
            raw_chunk = buffer_to_process[-(CHUNK_SIZE + PAD_SIZE):]
            if prev_pad is not None:
                chunk_with_pad = np.concatenate([prev_pad, raw_chunk])
            elif len(buffer_to_process) >= (CHUNK_SIZE + 2 * PAD_SIZE):
                chunk_with_pad = np.array(buffer_to_process)
            filtered = bandpass_filter(chunk_with_pad, 1, 50, SAMPLE_RATE_HZ)
            clean = interpolate_artifacts(filtered)
            latest_chunk = clean[PAD_SIZE:-PAD_SIZE]
            prev_pad = raw_chunk[-PAD_SIZE:]
            ser.write(serialize_chunk_binary(latest_chunk))
        finally:
            continue
        time.sleep(CHUNK_DURATION_SECONDS)  # throttle processing

# Start worker thread
active_buffer = deque(maxlen=SLIDING_BUFFER_SIZE)
thread = Thread(target=process_and_send, daemon=True)
thread.start()

# Main loop: continuously read ADC into the active buffer
sample_counter = 0
start_time = time.perf_counter()
while True:
    current_time = time.perf_counter()
    elapsed = current_time - start_time
    target_time = sample_counter * SAMPLE_INTERVAL
    sleep_time = target_time - elapsed
    if sleep_time > 0:
        time.sleep(sleep_time)
    
    # Read ADC sample
    sample = chan.voltage
    
    lock.acquire()
    active_buffer.append(sample)
    lock.release()
    
    sample_counter += 1