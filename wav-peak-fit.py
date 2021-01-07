#Written by Andrew Murphy, 2021

from scipy.optimize import curve_fit
from scipy.io import wavfile 
from scipy.fftpack import fft 
import numpy as np
import matplotlib.pyplot as plt
#-------------------------------------------------------------------------------------------------------------------------------
#Preparing the Audio Data
#-------------------------------------------------------------------------------------------------------------------------------
infile = 'samples/instruments/trumpet-C6.wav'  #enter input file name (.wav format)
outfile = 'reports/trumpet-c6_peak-fit.txt'    #enter output file name (.txt format)
print('Preparing Audio File:' , infile)
fs, Audiodata = wavfile.read(infile)


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

freq_values = (np.arange(0,int(np.ceil((n+1)/2.0)), 1.0) * (fs / n))/1000   #'x-values' of frequency plot (Khz)
db_amp_values = 10*np.log10(MagFreq)                                        #'y-values' of frequency plot (dB)

plt.plot(freq_values,db_amp_values) #Plot Frequency Spectrum
sample_interval = float(len(freq_values))/(np.amax(freq_values) - np.amin(freq_values))
print('Audio Data Extraction Complete')

#---------------------------------------------------------------------------------------------------------------------
# Obtaining Initial Guesses for Params
#----------------------------------------------------------------------------------------------------------------------

#The section in block quotes takes user input as guessesd for the initial parameters. For this example, I have manually entered guesses.
"""
N_peaks = int(input('Number of Peaks: '))
centers = []
widths = []
amps = []
scopes =[]

for i in range(N_peaks):
  print('~~~~~~~~~~~~~~~~')
  print('Peak:' , i+1)
  c_0 = float(input('Guess for Center:'))       #Center of Peak (kHz)
  w_0 = float(input('Guess for Width:'))        #Half-Width at Half-Maximum (kHz)
  a_0 = float(input('Guess for Amplitude:'))    #Amplitude (dB)
  scope = float(input('Scope Half-width: '))    #Scope (kHz)
  
  centers.append(c_0)
  widths.append(w_0)
  amps.append(a_0)
  scopes.append(scope) 
"""

#Manually entered parameter guesses
N_peaks = 4
centers = [1.047, 2.094, 3.141, 4.186]
widths = [.001, .001, .001, .004]
amps = [52.4, 35.2, 29.2, 13.6]
scopes = [.05, .05, .05, .05]
#---------------------------------------------------------------------------------------------------------------------
# Fit the Data
# --------------------------------------------------------------------------------------------------------------------

#Cauchy/Lorentz Ditribution
def cauchy(x,center,width, amp):
    return amp - 10*np.log10(1.0 + ((x - center)/width)**2)

opt_data = []
for i in range(N_peaks):

  max_scope = int((centers[i] - np.amin(freq_values) + scopes[i])*sample_interval)
  min_scope = int((centers[i] - np.amin(freq_values) - scopes[i])*sample_interval)

  xdata =  freq_values[min_scope:max_scope]
  ydata = db_amp_values[min_scope:max_scope]
  
  popt, pcov = curve_fit(cauchy, xdata, ydata, p0 = [centers[i], widths[i], amps[i]])
  opt_data.append(popt)
  
  plt.plot(xdata, popt[2] - 10*np.log10(1.0 + ((xdata - popt[0])/popt[1])**2)) #Plot Peak-Fit

plt.show()

#------------------------------------------------------------------------------------
# Write Fit Data to Output File
#-------------------------------------------------------------------------------------

f = open(outfile, 'w')
f.write(infile)
f.write('\r')

for i in range(N_peaks):
  f.write('~~~~~~~~~~~~~~~~')
  f.write('\r')
  f.write('PEAK: ')
  f.write(str(i+1))
  f.write('\r')
  f.write('CEN: ')
  f.write(str(opt_data[i][0]))
  f.write('\r')
  f.write('WID: ')
  f.write(str(opt_data[i][1]))
  f.write('\r' )
  f.write('AMP: ')
  f.write(str(opt_data[i][2]))
  f.write('\r')

f.close()  
