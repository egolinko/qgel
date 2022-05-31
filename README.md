# qgel
Python implementation of `qgel`, a quick way to Generalize, Embed, and Learn from data. A dimension reduction technique using naive distribution assumptions and simple matrix operations.

# Install

Included in the repo is a Dockerfile which will load the environment. Development was done within a devcontainer (recommended) [devcontainer](https://code.visualstudio.com/docs/remote/containers).

### To install from this repo, clone

```{shell}
git clone https://github.com/egolinko/qgel.git
```

### Install the conda environment from scratch

```{shell}
conda env create -f environment.yml

conda activate qgel
```

###  Follow instructions to install [pre-commit](https://pre-commit.com/) which is used in commiting to repo to aid in uniform styling.

```{shell}
pre-commit install
```

###  Then install via `pip`

```{shell}
pip install .
```


# Minimal Example
```{shell}
import pandas as pd
import numpy as np
import qgel

dd = pd.read_csv("https://s3-us-west-2.amazonaws.com/researchs/GFEL_data/car.csv")

X = pd.get_dummies(dd.drop("Class", axis=1))
X["Class"] = dd.Class

embedding, vectors, source_data_ = qgel.qgel(source_data_ = X,
                                             k = 10,
                                             learning_method = 'supervised',
                                             class_var = "Class"
                                        )

```

# Based on the Paper
Golinko, Eric, and Xingquan Zhu. "Generalized feature embedding for supervised, unsupervised, and online learning tasks." Information Systems Frontiers 21.1 (2019): 125-142.
