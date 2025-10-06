# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from collections import deque
import time
import os
import io

SAMPLE_RATE = 860
CSV_FILE = "../data_acquisition/eeg_data.csv"
NO_DATA_TIMEOUT = 5 #Seconds of no-data to turn off interactive plot
MAX_TIME_WINDOW = 10 #Seconds to display

WINDOW_SIZE = int(SAMPLE_RATE/2)  # samples per window
STEP_SIZE = 64 # step size for moving window
POLL_INTERVAL = 0.2 # seconds between file checks
TAIL_SECONDS = 3 # read last N seconds of samples


def read_latest_samples_tail(filename, seconds=TAIL_SECONDS):
    if not os.path.exists(filename):
        return np.array([]), np.array([])
    n_rows = int(seconds * SAMPLE_RATE)
    # Use deque to keep last n_rows + header line
    try:
        with open(filename, 'r') as f:
            # keep header + last n_rows lines
            tail = deque(f, maxlen=n_rows + 1)
    except Exception:
        return np.array([]), np.array([])

    if not tail:
        return np.array([]), np.array([])

    # Ensure header is first line; if header not in deque, read header separately
    first_line = tail[0].strip()
    if not first_line.startswith("time"):
        # header likely not in tail -> read header from file start then combine last n rows
        with open(filename, 'r') as f:
            header = f.readline()
        text = header + "".join(list(tail))
    else:
        text = "".join(list(tail))

    try:
        df = pd.read_csv(io.StringIO(text))
        return df['time'].to_numpy(), df['signal'].to_numpy()
    except Exception:
        return np.array([]), np.array([])

# Computes Hjorth Params in microvolts^2 for Activity
def hjorth_parameters(signal):
    signal = signal * (10**6) #Convert uV signal to V
    
    if len(signal) < 2:
        return np.nan, np.nan, np.nan  # Not enough data
    
    # Activity
    activity = np.var(signal)

    # First derivative
    diff_signal = np.diff(signal)
    
    # Mobility
    mobility = np.sqrt(np.var(diff_signal) / activity)

    # Complexity
    diff2_signal = np.diff(diff_signal)
    mobility_diff = np.sqrt(np.var(diff2_signal) / np.var(diff_signal))
    complexity = mobility_diff / mobility

    return activity, mobility, complexity

# Computes FFT Power
def compute_fft(signal, fs=SAMPLE_RATE):
    signal = signal * (10**6) #Convert uV signal to V
    N = len(signal)
    yf = rfft(signal)
    xf = rfftfreq(N, 1/fs)
    psd = np.abs(yf)**2 / N  # Power spectral density
    return xf, psd

if __name__ == "__main__":
    try:
        # --- Real-time Plotting ---
        max_len = int((1 / POLL_INTERVAL) * MAX_TIME_WINDOW)
        
        activity_history = deque(maxlen=max_len)
        mobility_history = deque(maxlen=max_len)
        complexity_history = deque(maxlen=max_len)
        time_history = deque(maxlen=max_len)
        
        plt.ion()
        fig, ax = plt.subplots(4, 1, figsize=(12, 10))
       
        last_mtime = 0.0
        last_update = time.time()
        
        
        print("Waiting for EEG data...")
        
        while True:
            # Sleep is file does not exist
            if not os.path.exists(CSV_FILE):
                time.sleep(POLL_INTERVAL)
                continue
            
            # quick check: only read file if it changed
            try:
                mtime = os.path.getmtime(CSV_FILE)
            except Exception:
                time.sleep(POLL_INTERVAL)
                continue

            if mtime == last_mtime:
                # no change in file; check timeout and sleep
                if time.time() - last_update > NO_DATA_TIMEOUT:
                    print("No new data received. Graph timed out. Stopping interactive updates...")
                    plt.ioff(); plt.show(); break
                time.sleep(POLL_INTERVAL)
                continue

            last_mtime = mtime
            time_array, signal_array = read_latest_samples_tail(CSV_FILE, seconds=TAIL_SECONDS)
            n_samples = len(signal_array)
            if n_samples < WINDOW_SIZE:
                time.sleep(POLL_INTERVAL)
                continue
            
            window_signal = signal_array[-WINDOW_SIZE:]
            window_time = time_array[-WINDOW_SIZE:]
        
            # Hjorth
            activity, mobility, complexity = hjorth_parameters(window_signal)
            activity_history.append(activity)
            mobility_history.append(mobility)
            complexity_history.append(complexity)
            time_history.append(window_time[-1])
                            
            # FFT
            freqs, psd = compute_fft(window_signal)
        
            # Clear and plot
            for a in ax:
                a.cla()
        
            # Hjorth plots
            ax[0].plot(time_history, activity_history, color='r')
            ax[0].set_title("Hjorth Activity")
            ax[0].set_xlabel("Time (s)")
            ax[0].set_ylabel("Activity")
            ax[0].set_ylim([0, max(activity_history)*1.2])  # consistent scaling
            
            ax[1].plot(time_history, mobility_history, color='g')
            ax[1].set_title("Hjorth Mobility")
            ax[1].set_xlabel("Time (s)")
            ax[1].set_ylabel("Mobility")
            ax[1].set_ylim([0, max(mobility_history)*1.2])
            
            ax[2].plot(time_history, complexity_history, color='b')
            ax[2].set_title("Hjorth Complexity")
            ax[2].set_xlabel("Time (s)")
            ax[2].set_ylabel("Complexity")
            ax[2].set_ylim([0, max(complexity_history)*1.2])
        
            # FFT bar chart up to 50 Hz
            idx = freqs <= 50
            ax[3].bar(freqs[idx], psd[idx], width=0.5, color='purple')
            ax[3].set_xlim(0,50)
            ax[3].set_xlabel("Frequency (Hz)")
            ax[3].set_ylabel("Power")
            ax[3].set_title("FFT Power Spectrum")
            
            fig.canvas.flush_events()
            plt.tight_layout()
            plt.pause(0.001)  # force update
            
            last_update = time.time()
        
            #If no new data will freeze graphs and stop waiting for data
            if time.time() - last_update > NO_DATA_TIMEOUT:
                print("No new data received. Graph timed out. Stopping interactive updates...")
                print(time_history)
                plt.ioff()
                plt.show()
                break
            
    except Exception:
        print("\n--- ERROR OCCURRED ---")