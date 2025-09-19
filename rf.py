import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, hilbert

# -------------------------------
# TIME AXIS = the sampling clock
# -------------------------------
# In real radios, an oscillator defines time. Here we simulate it.
fs = 10000   # sampling rate = 10 kHz (like an ADC taking 10,000 samples/sec)
T  = 1.0     # simulate 1 second
t  = np.linspace(0, T, int(fs*T), endpoint=False)

print(f"{len(t)=}, dt={t[1]-t[0]:.6f}s")  # dt is the time step

# -------------------------------
# MESSAGE SIGNAL (baseband)
# -------------------------------
# This is what we want to transmit, like voice or data.
fm = 2.0
m = np.sin(2*np.pi*fm*t)   # slow "message" tone at 2 Hz

# -------------------------------
# CARRIER SIGNAL (oscillator)
# -------------------------------
# Radios use oscillators (crystals, LC circuits) to generate a stable RF tone.
fc = 1000.0
c = np.cos(2*np.pi*fc*t)   # fast cosine at 1 kHz = carrier

# -------------------------------
# MODULATION (AM)
# -------------------------------
# The carrier's amplitude is varied according to the message signal.
# This is how AM radio works physically.
mu = 0.7
s = (1 + mu*m) * c   # transmit signal

# -------------------------------
# SPECTRUM VIEW
# -------------------------------
# Equivalent of a spectrum analyzer: shows carrier + sidebands.
S = np.fft.rfft(s)
freqs = np.fft.rfftfreq(len(s), 1/fs)

plt.figure()
plt.semilogy(freqs, np.abs(S) + 1e-12)
plt.xlim(0, 2000)
plt.title("Spectrum |S(f)|")
plt.xlabel("Hz"); plt.ylabel("|S|")
plt.show()

# -------------------------------
# CHANNEL (air + noise)
# -------------------------------
# In real life, the wave travels through the air and picks up noise.
def awgn(x, snr_db):
    p_sig   = np.mean(x**2)               # signal power
    snr_lin = 10**(snr_db/10)
    p_noise = p_sig / snr_lin             # noise power
    n       = np.random.normal(0, np.sqrt(p_noise), size=x.shape)
    return x + n

r = awgn(s, snr_db=5)  # received noisy signal

# -------------------------------
# DEMODULATION (envelope detector)
# -------------------------------
# AM radios use a diode-capacitor circuit to follow the envelope.
# Here we use the Hilbert transform to simulate that.
analytic  = hilbert(r)
envelope  = np.abs(analytic)   # approx. 1 + mu*m(t)

# -------------------------------
# BASEBAND RECOVERY
# -------------------------------
# Remove the DC offset and scale back down to recover the message.
m_env = (envelope - np.mean(envelope)) / mu

# -------------------------------
# LOW-PASS FILTER
# -------------------------------
# A filter removes the high-frequency carrier, leaving just the baseband message.
def lowpass(x, fc_hz, fs, order=4):
    b,a = butter(order, fc_hz/(fs/2), btype='low')
    return lfilter(b, a, x)

m_hat = lowpass(m_env, fc_hz=10, fs=fs)   # recovered message (≈ original m)
