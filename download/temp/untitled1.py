# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 08:50:08 2021

@author: k
"""

import pandas as pd
from matplotlib import pyplot as plt

df1=pd.read_csv("insurance.csv")
df1

# 0 means person will not buy an insurance and 1 means yes person will buy an insurance
plt.scatter(df1['age'],df1['bought_insurance'],marker='+',color='red')
plt.xlabel("Age")
plt.ylabel("A person will buy an insurance or not")


# Split data into features and target
X=df1.drop('bought_insurance', axis=1)
Y=df1.bought_insurance

# split data in train and test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,Y,train_size=0.8, random_state=0)

len(y_test)
len(y_train)

# model creation

from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)

model.predict(X_test)

model.score(X_test,y_test)

y_predicted = model.predict(X_test)

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_predicted)

import seaborn as sn
import matplotlib.pyplot as plt

plt.figure(figsize = (10,7))
sn.heatmap(cm, annot=True)
plt.xlabel('Predicted')
plt.ylabel('Truth')

from sklearn.metrics import classification_report

predictions=model.predict(X_test)
print(classification_report(y_test,predictions))

##############2
df2=pd.read_csv("HR_data.csv")
df2.head()

df2.info()
df2.shape

# no. of employees who left
# 1 means left and 0 means retained
left=df2[df2['left']==1]
left.shape

# no. of employees who retained
retain=df2[df2['left']==0]
retain.shape

df2.corr()

subdf = df2[['satisfaction_level','average_montly_hours','promotion_last_5years','salary']]
subdf.head()

# lets convert salary from categorical to numerical variable

salary_dummies = pd.get_dummies(subdf.salary, prefix="salary")
df_with_dummies = pd.concat([subdf,salary_dummies],axis='columns')
df_with_dummies.head(10)

df_with_dummies.drop('salary',axis='columns',inplace=True)
df_with_dummies.head()

# split data into feature and target
X=df_with_dummies
X.head()

#choosing target variable
y=df2.left
y

from sklearn.model_selection import train_test_split
#splitting data set into training and testing
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3, random_state=0)

from sklearn.linear_model import LogisticRegression
#making a model for logistic reg.
model = LogisticRegression()


#training model
model.fit(X_train, y_train)

model.score(X_test,y_test)

# using confusion matrix

y_predicted = model.predict(X_test)
from sklearn.metrics import confusion_matrix

# we are supplying actual value and predicted value
cm = confusion_matrix(y_test, y_predicted)
cm







