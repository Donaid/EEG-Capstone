import pandas as pd
import numpy as np
import scipy
from scipy import signal
from scipy.integrate import simps
import pickle


data = pd.read_csv('demo.csv') #this will the different csv files from neurosky#must find a way to readallcsv files by produced by the eneurosky

data = data["rawEeg"] # we want only the raw signal values

def bandpassfilter(signal):

    fs = 160
    lowcut = 0.5
    highcut = 30
    nyq = 0.5 * fs

    low = lowcut/nyq
    high = highcut/nyq

    order =1
    b, a = scipy.signal.butter(order, [low,high], 'bandpass', analog=False)
    y = scipy.signal.lfilter(b, a, signal, axis=0)

    return y

filtered = bandpassfilter(data)

data = filtered.reshape(-1)

fs = 160. # this value will depend on the sampling frequency

eeg_bands = {'Delta': (0.5, 4),
             'Theta': (4, 8),
             'Alpha': (8, 12),
             'Beta': (12, 30)}

segment_size = 0.25*data.size
overlap = 0.5*segment_size

freqs, psd = signal.welch(data, fs, nperseg=segment_size,noverlap=overlap,window="hann")

eeg_band_fft = dict()
for band in eeg_bands:
    freq_ix = np.where((freqs >= eeg_bands[band][0]) &
                       (freqs <= eeg_bands[band][1]))[0]
    eeg_band_fft[band] = simps(psd [freq_ix],even = 'avg')


data = np.array([eeg_band_fft[band] for band in eeg_bands])
data = np.reshape(data, (-1, 4))
print(data)

pickled_model = pickle.load(open('New_model.sav', 'rb'))

print(pickled_model.predict(data)) ## binary result 0 = inattentive , 1 = attentive
probability = (pickled_model.predict_proba(data)) ## probability

result = probability[0][0]*100

print(probability[0][0]) #left
print(probability[0][1]) #right


import websocket
import json

ws = websocket.WebSocket()
ws.connect('ws://localhost:8000/ws/test1')
ws.send(json.dumps({'Attention': result}))