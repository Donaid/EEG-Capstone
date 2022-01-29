import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from imblearn.over_sampling import SMOTE
from sklearn.neighbors import NearestNeighbors
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import DBSCAN
from collections import Counter
import pickle
from sklearn.linear_model import LogisticRegression
import joblib
from sklearn.metrics import accuracy_score

data = pd.read_csv('newtest.csv')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

labels = data.iloc[:, 4:5]
features =data.iloc[:, 0:4]

train, test, train_labels, test_labels = train_test_split(features, labels, test_size = 0.4, random_state = 3)

scaler = MinMaxScaler()
train = scaler.fit_transform(train)
test = scaler.transform(test)

"""
knn = KNeighborsClassifier(n_neighbors=7)
model= knn.fit(train, train_labels.values.ravel())
y_preds = model.predict(test)
"""
"""
rfc =RandomForestClassifier(n_estimators=500, oob_score = True)
model=rfc.fit(train, train_labels.values.ravel())
y_preds = model.predict(test)
"""

classifier = MLPClassifier(hidden_layer_sizes=(100,50,10), max_iter=1000,activation = 'relu',solver='adam',random_state=4)
model = classifier.fit(train, train_labels.values.ravel())
y_preds1= model.predict_proba(test)
y_preds= model.predict(test)

filename = 'model_pickle.sav'
pickle.dump(model, open(filename, 'wb'))

print('Model accuracy score: {0:0.4f}'. format(accuracy_score(test_labels , y_preds)))
cm = confusion_matrix(test_labels, y_preds)
sns.heatmap(cm, annot=True,fmt='g')
plt.show()

print(y_preds1)
print(y_preds)