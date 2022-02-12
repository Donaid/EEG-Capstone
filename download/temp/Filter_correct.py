import pandas as pd
import numpy as np
from scipy.signal import filtfilt
import scipy
from scipy.signal import lfilter

data = pd.read_csv('Sleep2.csv') #this will the different csv files from neurosky#must find a way to readallcsv files by produced by the eneurosky

data = data["eegRawValue"] # we want only the raw signal values

def bandpassfilter(signal):

    fs = 512
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
# we won't need this line for the system because we can pass the values directly to extraction
df.to_csv('5_F.csv', index = False, header=["Raw"]) 



data = pd.read_csv('5_F.csv') #this must be the input from filter
data =data[["Raw"]]#this line wont be necessary

fs = 512.

fft_vals = np.absolute(np.fft.rfft(data))

fft_freq = np.fft.rfftfreq(len(data), 1.0/fs)


eeg_bands = {'Delta': (0.5, 3),
             'Theta': (4, 8),
             'Alpha': (8, 12),
             'Beta': (12, 30)}


eeg_band_fft = dict()
for band in eeg_bands:
    freq_ix = np.where((fft_freq >= eeg_bands[band][0]) &
                       (fft_freq <= eeg_bands[band][1]))[0]
    eeg_band_fft[band] = np.max(fft_vals[freq_ix])

filter_df = pd.DataFrame(columns=['band', 'val'])
filter_df['band'] = eeg_bands.keys()
filter_df['val'] = [eeg_band_fft[band] for band in eeg_bands]

#we need to normalize the values before bassing it to the ML, must add a min maxscaler fnction here
print(filter_df) #must pass these values to ML model for prediction #this line wont be necessary

val1 = filter_df.iloc[0]['val']
val2 = filter_df.iloc[1]['val']
val3 = filter_df.iloc[2]['val']
val4 = filter_df.iloc[3]['val']

dict1 = {"Delta": [val1], "Theta": [val2], "Alpha": [val3], "Beta": [val4]}

df1 = pd.DataFrame(dict1)


