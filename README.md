# qGELpy
Python implementation of qGEL, a quick way to Generalize, Embed, and Learn from data. A dimension reduction technique using naive distribution assumptions and simple matrix operations.

# Based on the Paper 
Golinko, Eric, and Xingquan Zhu. "Generalized feature embedding for supervised, unsupervised, and online learning tasks." Information Systems Frontiers 21.1 (2019): 125-142.

# Install
Via pip

```{md}
pip install qGEL
```

# Minimal Example
```{md}
import pandas as pd
import numpy as np
import qGEL

dd = pd.read_csv("https://s3-us-west-2.amazonaws.com/researchs/GFEL_data/car.csv")

X = pd.get_dummies(dd.drop("Class", axis=1))
X["Class"] = dd.Class
               
embedding, vectors, sorted_X, orig_X = qGEL.qgel(source_data_ = X, 
                                                 k = 10, 
                                                 learning_method = 'supervised', 
                                                 class_var = "Class"
                                                )               
               
```               
