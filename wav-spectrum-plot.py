from scipy.io import wavfile 
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft 

#Read the Audio File
filename = 'samples/instruments/Flute-C6.wav' #enter file name
fs, Audiodata = wavfile.read(filename)



#Take Fast Fourier Transform
n = len(Audiodata) 
AudioFreq = fft(Audiodata)
AudioFreq = AudioFreq[0:int(np.ceil((n+1)/2.0))] #Half of the spectrum
MagFreq = np.abs(AudioFreq) # Magnitude
MagFreq = MagFreq / float(n)# Normalize power spectrum
MagFreq = MagFreq**2
if n % 2 > 0: # fft odd 
    MagFreq[1:len(MagFreq)] = MagFreq[1:len(MagFreq)] * 2
else:# fft even
    MagFreq[1:len(MagFreq) -1] = MagFreq[1:len(MagFreq) - 1] * 2 


#Plotting the Result
plt.figure()
freqAxis = np.arange(0,int(np.ceil((n+1)/2.0)), 1.0) * (fs / n)
print(len(freqAxis/1000.0), len(10*np.log10(MagFreq)))
plt.plot(freqAxis/1000.0, 10*np.log10(MagFreq)) #Power spectrum
plt.xlabel('Frequency (kHz)')
plt.ylabel('Power spectrum (dB)')
plt.title('Frequency Spectrum of %s' % filename)
plt.grid(True, which='both')

plt.show()
