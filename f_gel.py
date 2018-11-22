import numpy as np
import pandas as pd
from scipy.linalg import block_diag


def get_diag_index(d_, l):
    idx = d_[d_.Class == d_.Class.value_counts().index[l]].index
    return idx


def row_feature_rep(rows_, features_):
    r_1 = rows_.mean(axis=1).as_matrix()
    f_1 = features_.mean(axis=0).as_matrix()

    r_0 = 1 - r_1
    f_0 = 1 - f_1

    f = np.array([f_0, f_1])
    r = np.array([r_0, r_1])

    Q_ = np.matmul(f.transpose(), r)

    return Q_


def get_diag(d_, diag_idx_, i):
    gd = row_feature_rep(rows_=d_.iloc[diag_idx_[i]]
                         .drop("Class", axis=1),
                         features_=d_.iloc[diag_idx_[i]]
                         .drop("Class", axis=1))

    return gd


def gel(source_data_, k=10, learning_method="unsupervised", class_var=None):
    """
       Args:
           source_data_: a one-hot encoded dataframe
           k: number of eigenvectors to use for new embedding, if  'max' dim(source_data_) = dim(emb)
           learning_method: 'unsupervised' indicates no class label, otherwise 'supervised'
       Returns:
           emb: new embedded space
           v_t: vectors generated from svd
           mb: one-hot data
           source_data_: original data frame
    """

    if learning_method == 'supervised':
        source_data_ = source_data_.rename(columns={class_var: "Class"})
        mb_ = source_data_.drop("Class", axis=1)
        mb_['Class'] = pd.Categorical(source_data_.Class,
                                      categories=source_data_.Class.value_counts()
                                      .keys()
                                      .tolist(),
                                      ordered=True)
        mb = mb_.sort_values(by='Class')

        diag_idx = [get_diag_index(mb, l) for l in range(len(mb.Class.unique()))]

        D = [get_diag(mb, diag_idx, x) for x in range(len(mb.Class.unique()))]

        b = block_diag(*D)

        S_ = np.matmul(b, mb.drop("Class", axis=1).as_matrix())

        U, s, V = np.linalg.svd(S_)


    else:
        mb = source_data_
        u = row_feature_rep(rows_=mb, features_=mb)
        S_ = np.matmul(u, mb.as_matrix())
        U, s, V = np.linalg.svd(S_)

    if k == 'max':
        v_t = V.transpose()
    else:
        v_t = V.transpose()[:, 0:k]

    if learning_method == 'supervised':
        emb = np.matmul(mb.drop("Class", axis=1).as_matrix(), v_t)
    else:
        emb = np.matmul(mb.as_matrix(), v_t)

    return emb, v_t, mb, source_data_.rename(columns={"Class": class_var})

############
###
#


from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

dd = pd.read_csv("https://s3-us-west-2.amazonaws.com/researchs/GFEL_data/car.csv")


def gel_v_base(k):

    X = pd.get_dummies(dd.drop("Class", axis=1))
    X["Class"] = dd.Class

    idx = np.random.uniform(0, 1, len(X)) <= .8

    cp = gel(source_data_ = X[idx == True].reset_index().drop('index', axis = 1),
              k = k, learning_method = 'supervised', class_var = "Class")

    print("GEL complete")

    clf = XGBClassifier()
    clf.fit(X = cp[0], y = cp[2].Class)
    pred = clf.predict(np.matmul(X.drop("Class", axis = 1)[idx == False], cp[1]))

    pd.crosstab(X[idx == False].Class, pred, rownames=['Actual'], colnames=['Predicted'])
    g = accuracy_score(X[idx == False].Class, pred)

    b_clf = XGBClassifier()
    b_clf.fit(X=X.drop("Class", axis = 1)[idx == True], y=X[idx == True].Class)
    b_pred = b_clf.predict(X.drop("Class", axis=1)[idx == False])

    pd.crosstab(X[idx == False].Class, b_pred, rownames=['Actual'], colnames=['Predicted'])
    b = accuracy_score(X[idx == False].Class, b_pred)

    return b, g