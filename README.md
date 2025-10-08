# A Low-Cost, Modular EEG Acquisition System for Educational and Prototyping Applications

## Abstract
The field of brain-computer interfaces presents significant learning opportunities but is often limited by the high cost of EEG hardware and the lack of accessible software for custom solutions. This project presents a low-cost, modular EEG data acquisition system designed for educational and prototyping purposes. The system integrates three-electrode modules with AD620 instrumentation amplifiers, ADS1115 
16-bit analog-to-digital converters, and a Raspberry Pi Zero v1.3 for real-time data acquisition and preprocessing. Each module currently acquires data from either a single common-reference site or a pair of electrodes in a bipolar configuration, with potential expansion to four in a multi-module system. Custom Python code performs digital bandpass filtering, artifact interpolation, serial communication, and real-time visualization and feature extraction, including Hjorth parameters and power spectral analysis. Preliminary testing demonstrates the system's ability to acquire, process, and visualize EEG signals effectively. This platform offers a beginner-friendly introduction to neuroengineering, and lays the foundation for future enhancements, such as improved shielding, low-noise amplifiers, and multi-module expansion

## File System Plan and Completion
```plaintext
EEG-Neuroengineering-Portfolio/
│
├── hardware/
│   ├── EEG_Circuit.pdf                       # (100%)    PDF/KiCad:  Schematic of full analog circuit
│   ├── EEG_LTspice Simulation/
│   │	├── EEG.asc                           # (100%)    LTspice:    Simulated analog circuit and filter behavior
│   │	└── *Supporting .raw and .lib         # (100%)    LTspice:    Required files for LTspice Simulation, including AD620 module
│   └── Breadboard.jpg                        # (100%)    JPEG:       Image of the final circuit
│
├── data_acquisition/
│   ├── i2c_read_loop_and_preprocessing.py    # (100%)    Python:     ADC data acquisition over I2C with chunking digital bandpass (1–50 Hz) and eye blink/motion artifact rejection
│   └── serial_reader_for_windows.py          # (100%)    Python:     Receives data sent over serial from the microcontroller and visualizes the EEG signal
│
├── feature_extraction/
│   └── hjorth_params_and_fft_viewer.py       # (100%)    Python:     Real-time bandpower computation and Hjorth parameters visualizer
│
└── writeups/
    └── Whitepaper.pdf                        # (90%)    PDF:        Describes the end-to-end system design, code, and considerations, along with showcased visualizations (Need to add images of the signals received and edit the paper)
```
## Sources
[1] “Biosensing Starter Bundle,” OpenBCI Shop, 2015. [Online]. Available: https://shop.openbci.com/products/biosensing-starter-bundle?srsltid=AfmBOooZW34DXjRMADrFQMKMT046x-OEp9Lo4T9CD59FJCSn6VKfGpQm (accessed Oct. 07, 2025).

[2] C. Epstein, “chipstein - Homebrew Do-it-yourself EEG, EKG, and EMG.” [Online]. Available: https://sites.google.com/site/chipstein/homebrew-do-it-yourself-eeg-ekg-and-emg/ (accessed Jul. 30, 2025).

[3] cah6, “DIY EEG (and ECG) Circuit,” Instructables. [Online]. Available: https://www.instructables.com/DIY-EEG-and-ECG-Circuit/ (accessed Jul. 29, 2025).

[4] E. Ricker, “Elizabeth Ricker,” fab.cba.mit.edu, 2015. [Online]. Available: https://fab.cba.mit.edu/classes/863.15/section.Harvard/people/Ricker/htm/Final_Project.html (accessed Jul. 29, 2025).

[5] A. Marblestone, “Adam Marblestone,” Mit.edu, 2025. [Online]. Available: https://fab.cba.mit.edu/classes/863.12/people/Adam.Marblestone/AHM_week05.html (accessed Jul. 30, 2025).

[6] C. Moyes and M. Jiang, “Brain-Computer Interface Using Single-Channel Electroencephalography,” people.ece.cornell.edu, 2012. https://people.ece.cornell.edu/land/courses/ece4760/FinalProjects/s2012/cwm55/cwm55_mj294/index.html (accessed Jul. 29, 2025).

[7] *Analog Devices, AD620 Low Cost Low Power Instrumentation Amplifier,* Rev. H, 2009. [Online]. Available: https://www.analog.com/media/en/technical-documentation/data-sheets/AD620.pdf

[8] *Texas Instruments, ADS1113, ADS1114, and ADS1115 Ultra-Small, Low-Power, 16-Bit ADCs With Internal Reference,* SBAS444B, May 2009, revised October 2009. [Online]. Available: https://cdn-shop.adafruit.com/datasheets/ads1115.pdf

[9] *Adafruit Industries, ADS1115 16-Bit ADC - 4 Channel with Programmable Gain Amplifier - STEMMA QT / Qwiic,* Product ID 1085. [Online]. Available: https://www.adafruit.com/product/1085

[10] L. Clark, “Adafruit 4-Channel ADC Breakouts,” Adafruit Learning System, Nov. 29, 2012. [Online]. Available: https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/assembly-and-wiring (accessed Jul. 30, 2025).

[11] Raspberry Pi Foundation, "Raspberry Pi Zero — Reduced Schematics," Nov. 16, 2016. [Online]. Available: https://datasheets.raspberrypi.com/rpizero/raspberry-pi-zero-reduced-schematics.pdf

[12] Adafruit Industries, “Adafruit 4-Channel ADC Breakouts, Python & CircuitPython,” Adafruit Learning System. [Online]. Available: https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/python-circuitpython (accessed Jul. 30, 2025).

[13] A. Ortiz and J. Minguz, “Main features of the EEG amplifier explained,” Bitbrain, Apr. 03, 2020. https://www.bitbrain.com/blog/eeg-amplifier (accessed Jul. 29, 2025).

[14] “Summing Amplifier is an Op-amp Voltage Adder,” Basic Electronics Tutorials, Feb. 2019. https://www.electronics-tutorials.ws/opamp/opamp_4.html (accessed Jul. 29, 2025).

[15] R. Rager, “Tools of the Trade,” Jan. 2022. Accessed: Jul. 29, 2025. [Online]. Available: https://aset.org/wp-content/uploads/2022/01/10-20_System_Demonstration.pdf

[16] “Connect to a Raspberry Pi Zero W via USB - No Mini HDMI Cable Needed,” www.youtube.com. https://www.youtube.com/watch?v=xj3MPmJhAPU (accessed May 09, 2024).

[17] Mahmoodmustafashilleh, “How to Use ADS1115 With the Raspberry Pi (Part 1),” Instructables, May 27, 2024. https://www.instructables.com/How-to-Use-ADS1115-With-the-Raspberry-Pi-Part-1/
‌
‌
