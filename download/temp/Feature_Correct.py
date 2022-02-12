import numpy as np
import pandas as pd
from scipy.signal import filtfilt
import scipy
import matplotlib.pyplot as plt
from scipy import signal

#this must be the input from filter
data = pd.read_csv('Sleep2.csv') 
data = data[["eegRawValueVolts"]]

#data = pd.read_csv('1-filtered.csv') 
#data = data[["Raw"]]


#the sampling frequency is 512hz based on neurosky documentation
fs = 512. 

data = data.to_numpy()
data = data.reshape(-1) #must turn column to array

freqs, psd = signal.welch(data, fs, nperseg=None)

eeg_bands = {'Delta': (0, 3),
             'Theta': (4, 8),
             'Alpha': (8, 12),
             'Beta': (12, 30),

             'Gamma': (30, 100)}

# Take the max of the psd amplitude for each EEG band
eeg_band_fft = dict()
for band in eeg_bands:
    #looking for frequencies associated to each frequency band
    freq_ix = np.where((freqs >= eeg_bands[band][0]) &     
                       (freqs <= eeg_bands[band][1]))[0]
    #looking for the amplitudes associated to the frequency found
    eeg_band_fft[band] = np.max(psd[freq_ix]) 

df = pd.DataFrame(columns=['band', 'val'])
df['band'] = eeg_bands.keys()
df['val'] = [eeg_band_fft[band] for band in eeg_bands]

print(df) #must pass these values to ML model for prediction

df.shape





from sklearn.model_selection import train_test_split

x_train, y_train, x_test, y_test = train_test_split(df, test_size=0.4)
x_train, x_test= train_test_split(df, test_size=0.4)
