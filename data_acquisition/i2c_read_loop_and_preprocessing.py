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

SAMPLE_RATE_HZ = 860 #SPS
SAMPLE_INTERVAL = 1.0 / SAMPLE_RATE_HZ

SLIDING_BUFFER_SECONDS = 5
SLIDING_BUFFER_SIZE = SLIDING_BUFFER_SECONDS * SAMPLE_RATE_HZ

CHUNK_DURATION_SECONDS = 1 #Amount of data sent per step size
CHUNK_SIZE = int(SAMPLE_RATE_HZ * CHUNK_DURATION_SECONDS)

PAD_DURATION_SECONDS = 0.25 #Seconds to Pad around Chunk Sent
PAD_SIZE = int(SAMPLE_RATE_HZ * PAD_DURATION_SECONDS)

STEP_DURATION_SECONDS = 0.1 #How often samples are sent
STEP_SIZE = int(SAMPLE_RATE_HZ * STEP_DURATION_SECONDS)

i2c = busio.I2C(board.SCL, board.SDA)

ser = serial.Serial('/dev/ttyUSB0', 115200)

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
    chunk_index = 0
    while True:
        lock.acquire()
        buffer_to_process = active_buffer.copy()
        lock.release()
        
        if len(buffer_to_process) >= (CHUNK_SIZE + 2 * PAD_SIZE):
            full_buffer = np.array(buffer_to_process)
            filtered = bandpass_filter(full_buffer, 1, 50, SAMPLE_RATE_HZ)
            clean = interpolate_artifacts(filtered)
            
            latest_chunk = clean[-(CHUNK_SIZE + PAD_SIZE):-PAD_SIZE]
            ser.write(serialize_chunk_binary(latest_chunk))
            chunk_index += 1
        time.sleep(STEP_DURATION_SECONDS)  # throttle processing

# Start worker thread
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