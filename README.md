# RF-to-Bits (AM Radio Simulation)

This project is a simple Python simulation of how analog RF signals carry information.  
It shows how a baseband message can be modulated, transmitted, and recovered.

## Steps
1. **Message signal (m):** A low-frequency sine wave (simulates voice or data).  
2. **Carrier (c):** A higher-frequency oscillator tone.  
3. **Amplitude modulation (s):** The message is imposed on the carrier’s amplitude.  
4. **Channel:** Noise is added to represent transmission through air.  
5. **Demodulation:** The receiver uses an envelope detector to recover the message.  
6. **Filtering:** A low-pass filter removes the carrier, leaving the baseband signal.

## Spectrum Example
![Spectrum of AM signal](figure.png)  

*Figure 1: Spectrum of the AM signal. The tall peak at 1000 Hz is the carrier, and the smaller sidebands around it represent the message information. Noise is visible at lower levels across the band.*

## Requirements
- Python 3
- NumPy
- SciPy
- Matplotlib

Install dependencies:
```bash
pip install numpy scipy matplotlib
