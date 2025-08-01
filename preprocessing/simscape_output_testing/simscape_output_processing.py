# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

#Load CSV
data = pd.read_csv('simscape_output.csv')
eeg_signal = data.iloc[:, 1].values
fs = 1000 #ADS1115 can sample at 860Hz maximum, Simscape is at 1000Hz

#Bandpass filter 1-50 Hz
from scipy.signal import butter, filtfilt

def bandpass_filter(signal, low, high, fs, order=4):
    nyq = 0.5*fs
    b, a = butter(order,[low/nyq, high/nyq], btype='band')
    return filtfilt(b, a, signal) #research filtfilt

filtered_signal = bandpass_filter(eeg_signal, 1, 50, fs) #This removes DC offset, and the system is now centerd around 0V

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

clean_signal = interpolate_artifacts(filtered_signal)

def chunk_signal(signal, chunk_size):
    return np.array([signal[i:i + chunk_size]
                    for i in range(0, len(signal), chunk_size)
                    if i + chunk_size <= len(signal)])
                    
chunk_size = int(fs*1) # 1-second chunks
chunks = chunk_signal(clean_signal, chunk_size)

def serialize_chunk(chunk):
    return ','.join(map(str, chunk)) + '\n'

for chunk in chunks:
    serialized = serialize_chunk(chunk)
    print(serialized)
    
    
import matplotlib.pyplot as plt
for i, chunk in enumerate(chunks):
    start_time = i #seconds
    time_axis = np.linspace(start_time + 0.001, start_time+1.0, chunk_size)
    
    plt.figure(figsize=(6, 2))
    plt.plot(time_axis, chunk)
    plt.title(f'Chunk {i+1} | Time: {start_time + 0.001:.3f}s to {start_time + 1.0:.3f}s')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.tight_layout()
    plt.show()