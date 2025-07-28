# Low-Cost EEG Acquisition & Processing Pipeline

## What This Is
This project demonstrates the design and development of a low-cost, open-source EEG acquisition and preprocessing system. It spans circuit-level prototyping, simulation (Simscape), digital signal acquisition via an ADS1115 ADC and Raspberry Pi Zero V1.3, and software preprocessing using Python and MATLAB.

## Motivation
Driven by my interest in brain–computer interfaces (BCIs) and brain-controlled robotics/prosthetics, I set out to replicate the full EEG feature extraction workflow—from electrode input to feature vector output. The goal is to build a simplified, modular, and affordable 2-lead EEG system suitable for future machine learning applications.

## File System Plan and Completion
```plaintext
EEG-Neuroengineering-Portfolio/
│
├── hardware/
│   ├── CircuitDiagram.pdf          # (90%)    PDF:         Schematic of full analog chain
│   ├── SimscapeModel.slx           # (100%)   Simscape:    Simulated signal path and filter behavior
│   └── BreadboardDesign.jpg        # (75%)    PDF/KiCad:   Prototyped version; awaiting ADS1115 board
│
├── data_acquisition/
│   └── i2c_read_loop.py            # (0%)     Python:      ADC data acquisition over I2C
│
├── preprocessing/
│   ├── bandpass_filter.py          # (0%)     Python:      Digital bandpass (1–50 Hz)
│   ├── artifact_rejection.py       # (0%)     Python:      Eye blink/motion artifact rejection
│
├── feature_extraction/
│   ├── erp_analysis.m              # (0%)     MATLAB:      ERP (event-related potential) extraction
│   └── fft_bandpower.m             # (0%)     MATLAB:      Alpha/Beta bandpower computation
│
├── notebooks/
│   └── Exploration.ipynb           # (0%)     Jupyter:     Exploratory signal processing and visualizations
│
└── writeups/
    └── EEG_Pipeline_Whitepaper.pdf # (0%)     PDF:         Describing the end-to-end system design
```
## Sources
- cah6, "DIY EEG and ECG Circuit," *Instructables*. https://www.instructables.com/DIY-EEG-and-ECG-Circuit/
- C. Epstein, "Homebrew Do-It-Yourself EEG, EKG and EMG," *Google Sites*. https://sites.google.com/site/chipstein/homebrew-do-it-yourself-eeg-ekg-and-emg?authuser=0
- M. Ricker, "DIY EEG Headset," *MIT Media Lab, 2015*. https://fab.cba.mit.edu/classes/863.15/section.Harvard/people/Ricker/htm/Final_Project.html
