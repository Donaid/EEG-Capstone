import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier
import pickle


data = pd.read_csv('Main.csv')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

labels = data.iloc[:, 4:5]
features =data.iloc[:, 0:4]


train, test, train_labels, test_labels = train_test_split(features, labels, test_size = 0.3, random_state = 3)
scaler = MinMaxScaler()
train = scaler.fit_transform(train)
test = scaler.transform(test)

classifier = MLPClassifier(hidden_layer_sizes=(100,100,100), max_iter=1000,activation = 'relu',solver='adam',random_state=4)
model= classifier.fit(train, train_labels.values.ravel())
y_preds= classifier.predict_proba(test)
y_preds1= classifier.predict(test)
print(y_preds)
print(y_preds1)

