import pandas as pd
import numpy as np
import scipy
from scipy import signal
from scipy.integrate import simps
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv('50.csv') #this will the different csv files from neurosky#must find a way to readallcsv files by produced by the eneurosky

data = data["eegRawValue"] # we want only the raw signal values

def bandpassfilter(signal):

    fs = 150
    lowcut = 0.5
    highcut = 30
    nyq = 0.5 * fs

    low = lowcut/nyq
    high = highcut/nyq

    order =1
    b, a = scipy.signal.butter(order, [low,high], 'bandpass', analog=False)
    y = scipy.signal.lfilter(b, a, signal, axis =0)

    return y


filtered = bandpassfilter(data)
df = pd. DataFrame(filtered)
df.to_csv('5_F.csv', index = False, header=["Raw"]) # we won't need this line for the system because we can pass the values directly to extraction

data = pd.read_csv('5_F.csv') #this must be the input from filter
data =data[["Raw"]]#this line wont be necessary

data = data.to_numpy()
data= data.reshape(-1)
fs = 150.

eeg_bands = {'Delta': (0.5, 4),
             'Theta': (4, 8),
             'Alpha': (8, 12),
             'Beta': (12, 30)}


freqs, psd = signal.welch(data, fs, nperseg=150)

eeg_band_fft = dict()
for band in eeg_bands:
    freq_ix = np.where((freqs >= eeg_bands[band][0]) &
                       (freqs <= eeg_bands[band][1]))[0]
    eeg_band_fft[band] = simps(psd [freq_ix])

df = pd.DataFrame(columns=['band', 'val'])
df['band'] = eeg_bands.keys()
df['val'] = [eeg_band_fft[band] for band in eeg_bands]

"""" # please add this part in your code man
scaler = MinMaxScaler()
train = scaler.fit_transform(train)
test = scaler.transform(test)
"""

print(df)