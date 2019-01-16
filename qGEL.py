import numpy as np
import pandas as pd
from scipy.linalg import block_diag


def get_diag_index(d_, l):
    idx = d_[d_.Class == d_.Class.value_counts().index[l]].index
    return idx


def row_feature_rep(rows_, features_):
    r_1 = rows_.mean(axis=1).values
    f_1 = features_.mean(axis=0).values

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


def qgel(source_data_, k=10, learning_method="unsupervised", class_var=None):
    """
       Args:
           source_data_: a one-hot encoded dataframe
           k: number of eigenvectors to use for new embedding, if  'max' dim(source_data_) = dim(emb)
           learning_method: 'unsupervised' indicates no class label, otherwise 'supervised'
           class_var: string - name of class variable
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

        S_x = np.matmul(np.divide(b, np.max(b)), mb.drop("Class", axis=1).values)

        S_ = np.matmul(np.transpose(S_x), S_x)

        U, s, V = np.linalg.svd(S_)


    else:
        mb = source_data_
        u = row_feature_rep(rows_=mb, features_=mb)
        S_x = np.matmul(np.divide(u, np.max(u)), mb.values)
        S_ = np.matmul(np.transpose(S_x), S_x)
        U, s, V = np.linalg.svd(S_)

    if k == 'max':
        v_t = V.transpose()
    else:
        v_t = V.transpose()[:, 0:k]

    if learning_method == 'supervised':
        emb = np.matmul(mb.drop("Class", axis=1).values, v_t)
    else:
        emb = np.matmul(mb.values, v_t)

    return emb, v_t, mb, source_data_.rename(columns={"Class": class_var})
