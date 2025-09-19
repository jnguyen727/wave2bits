import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, hilbert

# an oscilator ticks at GHz speeds, so we need to simulate a time axis

fs = 10000 # 10 kHz frequency (10000 samples per second)
T = 1.0 # one second
t = np.linspace(0, T, int(fs*T), endpoint=False)

print(f"{len(t)=}, dt={t[1]-t[0]:.6f}s")