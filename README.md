# Low-Cost Single-Lead EEG Acquisition & Processing Pipeline

## What This Is
This project demonstrates the design and development of an open-source, homebrew single-lead EEG acquisition and preprocessing system. It spans circuit-level prototyping, simulation (Simscape), digital signal acquisition via an ADS1115 ADC and Raspberry Pi Zero V1.3, and software preprocessing using Python and MATLAB.

## Motivation
Driven by my interest in brain–computer interfaces (BCIs) and brain-controlled robotics/prosthetics, I set out to replicate the complete EEG feature extraction workflow—from electrode input to feature vector output. The goal is to build a simplified, modular, and affordable 2-lead EEG system suitable for future machine learning and neuroscience applications.

## Modes of Operation
Single-Lead Mode (e.g., F3 vs A1): Allows localized activity measurement but only from one site at a time.

## File System Plan and Completion
```plaintext
EEG-Neuroengineering-Portfolio/
│
├── hardware/
│   ├── EEG_Circuit.pdf                   # (100%)   PDF:         Schematic of full analog chain
│   ├── EEG_Characterization_Model.slx    # (100%)   Simscape:    Simulated signal path and filter behavior
│   └── breadboard_design.jpg              # (75%)    PDF/KiCad:   Prototype version; awaiting ADS1115 board
│
├── data_acquisition/
│   └── i2c_read_loop.py                  # (0%)     Python:      ADC data acquisition over I2C
│
├── preprocessing/
│   ├── bandpass_filter.py                # (0%)     Python:      Digital bandpass (1–50 Hz)
│   ├── artifact_rejection.py             # (0%)     Python:      Eye blink/motion artifact rejection
│   └── simscape_output_testing/
│   	├── simscape_output.csv           # (100%)   CSV:         Voltage over time data from Simscape
│   	└── simscape_output_processing.py # (100%)   Python:      Testing filters for eventual implementation on RPi Zero
│
├── feature_extraction/
│   ├── erp_analysis.m                    # (0%)     MATLAB:      ERP (event-related potential) extraction
│   └── fft_bandpower.m                   # (0%)     MATLAB:      Alpha/Beta bandpower computation
│
├── notebooks/
│   └── exploration.ipynb                 # (0%)     Jupyter:     Exploratory signal processing and visualizations
│
└── writeups/
    └── EEG_pipeline_whitepaper.pdf       # (0%)     PDF:         Describing the end-to-end system design
```
## Sources
[1] C. Epstein, “chipstein - Homebrew Do-it-yourself EEG, EKG, and EMG.” https://sites.google.com/site/chipstein/homebrew-do-it-yourself-eeg-ekg-and-emg/ (accessed Jul. 30, 2025).

[2] cah6, “DIY EEG (and ECG) Circuit,” Instructables. https://www.instructables.com/DIY-EEG-and-ECG-Circuit/ (accessed Jul. 29, 2025).

[3] E. Ricker, “Elizabeth Ricker,” fab.cba.mit.edu, 2015. https://fab.cba.mit.edu/classes/863.15/section.Harvard/people/Ricker/htm/Final_Project.html (accessed Jul. 29, 2025).

[4] A. Marblestone, “Adam Marblestone,” Mit.edu, 2025. https://fab.cba.mit.edu/classes/863.12/people/Adam.Marblestone/AHM_week05.html (accessed Jul. 30, 2025).

[5] C. Moyes and M. Jiang, “Brain-Computer Interface Using Single-Channel Electroencephalography,” people.ece.cornell.edu, 2012. https://people.ece.cornell.edu/land/courses/ece4760/FinalProjects/s2012/cwm55/cwm55_mj294/index.html (accessed Jul. 29, 2025).

[6] A. Ortiz and J. Minguz, “Main features of the EEG amplifier explained,” Bitbrain, Apr. 03, 2020. https://www.bitbrain.com/blog/eeg-amplifier (accessed Jul. 29, 2025).

[7] “Summing Amplifier is an Op-amp Voltage Adder,” Basic Electronics Tutorials, Feb. 2019. https://www.electronics-tutorials.ws/opamp/opamp_4.html (accessed Jul. 29, 2025).

[8] R. Rager, “Tools of the Trade,” Jan. 2022. Accessed: Jul. 29, 2025. [Online]. Available: https://aset.org/wp-content/uploads/2022/01/10-20_System_Demonstration.pdf

[9] J. Acharya, A. Hani, P. Thirumala, and T. Tsuchida, “American Clinical Neurophysiology Society Guideline 3: A Proposal for Standard Montages to Be Used in Clinical EEG,” American Clinical Neurophysiology Society, 2016. Accessed: Jul. 29, 2025. [Online]. Available: https://www.acns.org/UserFiles/file/EEGGuideline3Montage.pdf
