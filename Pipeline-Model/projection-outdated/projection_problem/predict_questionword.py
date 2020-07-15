# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

#import os
#print(os.listdir("../input"))
dataset = pd.read_csv('merged_train.csv')
# print(dataset.info());

# Any results you write to the current directory are saved as output.
columns= ["id question","index word from question","PERSON","LOCATION","DATETIME","QUANTITY","ORGANISATION","NONE",
"ADV","VERB","DET","ADJ","PROPN","ADP","PART","NOUN","NUM","PRON","INTJ","CCONJ",
"acl","advcl","advmod","amod","appos","aux","case","cc","ccomp","clf","compound","conj",
"cop","csubj","dep","det","discourse","dislocated","expl","fixed","flat","goeswith","iobj",
"list","mark","nmod","nsubj","nummod","obj","obl","orphan","parataxis","punct","reparandum",
"root","vocative","xcomp",
"is_stop",
"w2v",
"num_of_rows",
"word from question in where clause"]

ner = ["PERSON","LOCATION","DATETIME","QUANTITY","ORGANISATION","NONE"]
subject = ["csubj","nsubj"]
obj = ["iobj","obj"]
mod = ["advmod","amod","nmod","nummod"]
w2v = ["w2v"]
num_of_rows = ["num_of_rows"]
pos = ["ADV","VERB","DET","ADJ","PROPN","ADP","PART","NOUN","NUM","PRON","INTJ","CCONJ"]

x = dataset[ pos + mod + ner + ["is_stop"] + w2v+num_of_rows].values#dataset.iloc[:,2:5]values
y = dataset.iloc[:,60].values

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25,random_state=0)

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
sc = StandardScaler()

x_train = sc.fit_transform(x_train)
x_test = sc.fit_transform(x_test)

# print(x_train)

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(x_train,y_train)

y_pred = classifier.predict(x_test)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_pred)
cr = classification_report(y_test, y_pred)

print(cm)
print("*"*40)
print(cr)

from sklearn.tree import DecisionTreeClassifier
clf_tree=DecisionTreeClassifier(criterion='entropy', random_state=0)
clf_tree.fit(x_train,y_train)
y_pred = clf_tree.predict(x_test)
cm_2=confusion_matrix(y_test,y_pred)
cr = classification_report(y_test, y_pred)
np.savetxt("out.csv", np.asarray(y_pred), delimiter=",")
print(cm_2)
print("*"*40)
print(cr)

from sklearn.neighbors import KNeighborsClassifier


knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(x_train, y_train)
knn.score(x_test, y_test)

pred = knn.predict(x_test)
cm = confusion_matrix(y_test, pred)
cr = classification_report(y_test, pred)

print(cm)
print("*"*40)
print(cr)


from sklearn.naive_bayes import GaussianNB

naive_classifier = GaussianNB()
naive_classifier.fit(x_train, y_train)
y_pred = naive_classifier.predict(x_test)

cm = confusion_matrix(y_test, pred)
cr = classification_report(y_test, pred)

print(cm)
print("*"*40)
print(cr)
