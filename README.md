# qGELpy
Python implementation of qGEL, a quick way to Generalize, Embed, and Learn from data. A dimension reduction technique using naive distribution assumptions and simple matrix operations.

# Based on the Paper 

Golinko, Eric, and Xingquan Zhu. "Generalized feature embedding for supervised, unsupervised, and online learning tasks." Information Systems Frontiers 21.1 (2019): 125-142.

# Minimal Example

```{md}
import qGEL

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

dd = pd.read_csv("https://s3-us-west-2.amazonaws.com/researchs/GFEL_data/car.csv")

X = pd.get_dummies(dd.drop("Class", axis=1))
X["Class"] = dd.Class

idx = np.random.uniform(0, 1, len(X)) <= .8

cp = qGEL.qgel(source_data_ = X[idx == True].reset_index().drop('index', axis = 1),
               k = 10, learning_method = 'supervised', class_var = "Class")
               
```               
