# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import time
from collections import deque

#Simulate ADC SPS
SAMPLE_RATE_HZ = 1000 #Simscape samples every 1ms real ADC will be every 2.5ms
SAMPLE_INTERVAL = 1.0 / SAMPLE_RATE_HZ

SLIDING_BUFFER_SECONDS = 5
SLIDING_BUFFER_SIZE = SLIDING_BUFFER_SECONDS * SAMPLE_RATE_HZ

CHUNK_DURATION_SECONDS = 1 #Amount of data sent per step size
CHUNK_SIZE = int(SAMPLE_RATE_HZ * CHUNK_DURATION_SECONDS)

PAD_DURATION_SECONDS = 0.25 #Seconds to Pad around Chunk Sent
PAD_SIZE = int(SAMPLE_RATE_HZ * PAD_DURATION_SECONDS)

STEP_DURATION_SECONDS = 0.1 #How often samples are sent
STEP_SIZE = int(SAMPLE_RATE_HZ * STEP_DURATION_SECONDS)

CSV_FILE = 'simscape_output.csv'

#Load CSV
data = pd.read_csv('simscape_output.csv')
eeg_signal = data.iloc[:, 1].values


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

#Chunking
def serialize_chunk(chunk):
    return ','.join(map(str, chunk)) + '\n'
                    
#Plotting
def plot_chunk(chunk, sample_counter, chunk_index):
    start_time = (sample_counter - CHUNK_SIZE - PAD_SIZE)/SAMPLE_RATE_HZ 
    end_time = (sample_counter - PAD_SIZE)/SAMPLE_RATE_HZ 
    time_axis = np.linspace(start_time, end_time, CHUNK_SIZE)
    
    plt.figure(figsize=(6, 2))
    plt.plot(time_axis, chunk)
    plt.title(f'Chunk {chunk_index + 1} | Time: {start_time:.3f}s to {end_time:.3f}s')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#Pretending there is a data stream like with an ADC
def stream_csv(CSV_FILE):
    buffer = deque(maxlen=SLIDING_BUFFER_SIZE)
    chunk_index = 0
    sample_counter = 0
    
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file)
        
        start_time = time.perf_counter()
        
        for i, row in enumerate(reader):
            current_time = time.perf_counter()
            elapsed  = current_time - start_time
            target_time = i * SAMPLE_INTERVAL
            sleep_time = target_time - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
            
            try:
                sample = float(row[1])
            except ValueError:
                continue
            
            buffer.append(sample)
            sample_counter += 1
            
            #Sliding buffer that starts after 1s and grows to 5s
            if len(buffer) >= (CHUNK_SIZE + 2 * PAD_SIZE) and (sample_counter % STEP_SIZE) == 0:
                full_buffer = np.array(buffer)
                filtered = bandpass_filter(full_buffer, 1, 50, SAMPLE_RATE_HZ)
                clean = interpolate_artifacts(filtered)

                latest_chunk = clean[-(CHUNK_SIZE+PAD_SIZE):-PAD_SIZE]  #Take sample with PAD_SIZE padding from end of data
                
                serialized = serialize_chunk(clean) #Pretend output for sending to MATLAB
                plot_chunk(latest_chunk, sample_counter, chunk_index)
                chunk_index += 1

stream_csv(CSV_FILE) #Run process