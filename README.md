# A Low-Cost Modular EEG System and Software for Educational and Prototyping Applications

## Abstract
Brain-computer interfaces (BCIs) offer a wealth of educational value and research potential; however, the high cost of EEG hardware limits accessibility to beginners, hobbyists, students, and independent researchers. This project presents a low-cost modular EEG data acquisition system designed for educational and prototyping purposes. The system is built around three-electrode modules featuring AD620 instrumentation amplifiers, ADS1115 analog-to-digital converters, and operates on a single Raspberry Pi Zero v1.3. Each module is capable of recording signals from either a single referential site or a pair of electrodes in a bipolar configuration. By utilizing four modules, a single Raspberry Pi can record up to five bipolar channels with low latency. Custom Python code performs bandpass filtering, artifact interpolation, USB communication, and real-time visualization. It also supports near-real-time Hjorth parameter visualization and power spectral analysis. Tests using a breadboard prototype indicate that the system can reliably process, capture, and visualize EEG signals, and offers an accessible and engaging introduction to neuroengineering and brain–computer interfaces.

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
│   ├── serial_reader_for_windows.py          # (100%)    Python:     Receives data sent over serial from the microcontroller and visualizes the EEG signal
│   └── Waveform.png                          # (100%)    PNG:        Screenshot of waveform visualizer with live data
│
├── feature_extraction/
│   ├── hjorth_params_and_fft_viewer.py       # (100%)    Python:     Real-time bandpower computation and Hjorth parameters visualizer
│   └── Feature_Extraction.png                # (100%)    PNG:        Screenshot of Hjorth parameter and FFT visualizer with live data
│
└── writeups/
    └── Whitepaper.pdf                        # (90%)     PDF:        Describes the end-to-end system design, code, and considerations, along with showcased visualizations (Need to add images of the signals received and edit the paper)
```
## Sources
[1] “Biosensing Starter Bundle,” OpenBCI, 2015. https://shop.openbci.com/products/biosensing-starter-bundle?srsltid=AfmBOooZW34DXjRMADrFQMKMT046x-OEp9Lo4T9CD59FJCSn6VKfGpQm (accessed Oct. 07, 2025).

[2] C. Epstein, “chipstein - Homebrew Do-it-yourself EEG, EKG, and EMG,” Mar. 28, 2022. https://sites.google.com/site/chipstein/homebrew-do-it-yourself-eeg-ekg-and-emg/ (accessed Jul. 30, 2025).

[3] cah6, “DIY EEG (and ECG) Circuit,” Instructables. https://www.instructables.com/DIY-EEG-and-ECG-Circuit/ (accessed Jul. 28, 2025).

[4] E. Ricker, “Final Project: DIY EEG, EEG: Cheap and Small,” fab.cba.mit.edu, Dec. 2015. https://fab.cba.mit.edu/classes/863.15/section.Harvard/people/Ricker/htm/Final_Project.html (accessed Jul. 29, 2025).

[5] Marblestone and Fracchia, “FabECG: a simple electrocardiogram board,” fab.cba.mit.edu. https://fab.cba.mit.edu/classes/863.12/people/Adam.Marblestone/AHM_week05.html (accessed 7AD).

[6] C. Moyes and M. Jiang, “Brain-Computer Interface Using Single-Channel Electroencephalography,” people.ece.cornell.edu, 2012. https://people.ece.cornell.edu/land/courses/ece4760/FinalProjects/s2012/cwm55/cwm55_mj294/index.html (accessed Jul. 30, 2025).

[7] L. Hirsch and R. Brenner, Atlas of EEG in Critical Care. John Wiley & Sons. Accessed: Oct. 10, 2025. [Online]. Available: https://www.ilae.org/files/ilaeBook/samplePages/Atlas%20of%20EEG%20Sample%20Pages%2012%20pg.pdf

[8] P. L. Nunez and Ramesh Srinivasan, Electric fields of the brain: the neurophysics of EEG. Oxford: Oxford University Press, 2006, pp. 24, 42–45.

[9] Analog Devices, “AD620 Low Cost Low Power Instrumentation Amplifier,” Rev. H, 2009. [Online]. Available: https://www.analog.com/media/en/technical-documentation/data-sheets/AD620.pdf

[10] Texas Instruments, “ADS1113, ADS1114, and ADS1115 Ultra-Small, Low-Power, 16-Bit ADCs With Internal Reference,” SBAS444B, May 2009, revised October 2009. [Online]. Available: https://cdn-shop.adafruit.com/datasheets/ads1115.pdf

[11] Adafruit Industries, ADS1115 16-Bit ADC - 4 Channel with Programmable Gain Amplifier - STEMMA QT / Qwiic, Product ID 1085. [Online]. Available: https://www.adafruit.com/product/1085

[12] L. Clark, “Adafruit 4-Channel ADC Breakouts,” Adafruit Learning System, Nov. 29, 2012. https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/assembly-and-wiring (accessed Jul. 30, 2025).

[13] B. Olshausen, “Aliasing, PSC 129 - Sensory Processes,” Redwood Center for Theoretical Neuroscience, Oct. 2000. Accessed: Oct. 10, 2025. [Online]. Available: https://www.rctn.org/bruno/npb261/aliasing.pdf

[14] Raspberry Pi Foundation, "Raspberry Pi Zero — Reduced Schematics," Nov. 16, 2016. [Online]. Available: https://datasheets.raspberrypi.com/rpizero/raspberry-pi-zero-reduced-schematics.pdf

[15] Renesas Electronics Corporation, “CA3130, CA3130A 15MHz, BiMOS Operational Amplifier with MOSFET Input/CMOS Output,” FN817, Rev.6.00 Aug 1, 2005. [Online]. Available: https://www.renesas.com/en/document/dst/ca3130-ca3130a-datasheet

[16] Texas Instruments, “Industry-Standard Dual Operational Amplifiers,” SLOS068AB, June 1979, revised October 2024. [Online]. Available: https://www.ti.com/lit/ds/symlink/lm358.pdf

[17] “CA3130EZ,” DigiKey. https://www.digikey.com/en/products/detail/renesas-electronics-corporation/CA3130EZ/1060748 (accessed Oct. 10, 2025).

[18] “LM358P,” DigiKey. https://www.digikey.com/en/products/detail/texas-instruments/LM358P/277042 (accessed Oct. 10, 2025).

[19] L. Clark, “Adafruit 4-Channel ADC Breakouts,” Adafruit Learning System, Jun. 29, 2025. https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/python-circuitpython (accessed Oct. 10, 2025).

[20] S.-H. Oh, Y.-R. Lee, and H.-N. Kim, “A Novel EEG Feature Extraction Method Using Hjorth Parameter,” International Journal of Electronics and Electrical Engineering, vol. 2, no. 2, pp. 106–110, Jun. 2014, doi: https://doi.org/10.12720/ijeee.2.2.106-110.

[21] A. Ortiz and J. Minguz, “Main features of the EEG amplifier explained,” Bitbrain, Apr. 03, 2020. https://www.bitbrain.com/blog/eeg-amplifier (accessed Jul. 29, 2025).

[22] “Summing Amplifier is an Op-amp Voltage Adder,” Basic Electronics Tutorials, Feb. 2019. https://www.electronics-tutorials.ws/opamp/opamp_4.html (accessed Jul. 29, 2025).

[23] R. Rager, “Tools of the Trade,” Jan. 2022. [Online]. Available: https://aset.org/wp-content/uploads/2022/01/10-20_System_Demonstration.pdf (accessed Jul. 29, 2025).

[24] “Connect to a Raspberry Pi Zero W via USB - No Mini HDMI Cable Needed,” YouTube, https://www.youtube.com/watch?v=xj3MPmJhAPU (accessed May 09, 2024).

[25] Mahmoodmustafashilleh, “How to Use ADS1115 With the Raspberry Pi (Part 1),” Instructables, https://www.instructables.com/How-to-Use-ADS1115-With-the-Raspberry-Pi-Part-1/ (accessed Jul. 29, 2025).
