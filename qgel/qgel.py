import numpy as np
import pandas as pd
from scipy.linalg import block_diag


def get_diag_index(df: pd.DataFrame, diag: int) -> pd.core.indexes.numeric.Int64Index:
    """Finds the index values of class labels.

    Args:
        df (pd.DataFrame): Dataframe.
        diag (int): Index values.

    Returns:
        pd.core.indexes.numeric.Int64Index: _description_
    """
    idx = df[df.Class == df.Class.value_counts().index[diag]].index
    return idx


def row_feature_rep(df: pd.DataFrame) -> np.ndarray:
    """Creates the row and column binary representations of data.

    Args:
        df (pd.DataFrame): Input data.

    Returns:
        np.ndarray: Matrix multipled data.
    """
    row_mean = df.mean(axis=1).values
    feature_mean = df.mean(axis=0).values

    row_conjugate = 1 - row_mean
    feature_conjugate = 1 - feature_mean

    features = np.array([feature_mean, feature_conjugate])

    rows = np.array([row_mean, row_conjugate])

    Q = np.matmul(features.transpose(), rows)

    return Q


def get_diag(
    df: pd.DataFrame, diag_idx_: pd.core.indexes.numeric.Int64Index, i: int
) -> np.ndarray:
    """Finds diagonal value of input.

    Args:
        df (pd.DataFrame): Input data.
        diag_idx_ (pd.core.indexes.numeric.Int64Index): Indices of class index values.
        i (int): Iteration through index.

    Returns:
        np.ndarray: Diagonal output.
    """
    current_diag = row_feature_rep(df.iloc[diag_idx_[i]].drop("Class", axis=1))

    return current_diag


def qgel(
    one_hot_data: pd.DataFrame,
    k: int = 10,
    learning_method: str = "unsupervised",
    class_var: str = None,
) -> list:
    """
    Args:
        one_hot_data: a one-hot encoded dataframe
        k: number of eigenvectors to use for new embedding,
            if  'max' dim(one_hot_data) = dim(emb)
        learning_method: 'unsupervised' indicates no class label,
            otherwise 'supervised'
        class_var: string - name of class variable
    Returns:
        emb: new embedded space
        v_t: vectors generated from svd
        feature_df_sorted: one-hot data
        one_hot_data: original data frame
    """

    if learning_method == "supervised":
        one_hot_data = one_hot_data.rename(columns={class_var: "Class"})

        feature_df = one_hot_data.drop("Class", axis=1)

        feature_df["Class"] = pd.Categorical(
            one_hot_data.Class,
            categories=one_hot_data.Class.value_counts().keys().tolist(),
            ordered=True,
        )

        feature_df_sorted = feature_df.sort_values(by="Class")

        diag_idx = [
            get_diag_index(feature_df_sorted, class_idx)
            for class_idx in range(len(feature_df_sorted.Class.unique()))
        ]
        D = [
            get_diag(feature_df_sorted, diag_idx, diag_block)
            for diag_block in range(len(feature_df_sorted.Class.unique()))
        ]

        B = block_diag(*D)

        S_norm = np.matmul(
            np.divide(B, np.max(B)), feature_df_sorted.drop("Class", axis=1).values
        )

        S_kernel = np.matmul(np.transpose(S_norm), S_norm)

        U, s, V = np.linalg.svd(S_kernel)

    else:
        feature_df_sorted = one_hot_data
        u = row_feature_rep(feature_df_sorted)
        S_norm = np.matmul(np.divide(u, np.max(u)), feature_df_sorted.values)
        S_kernel = np.matmul(np.transpose(S_norm), S_norm)
        U, s, V = np.linalg.svd(S_kernel)

    if k == "max":
        v_t = V.transpose()
    else:
        v_t = V.transpose()[:, 0:k]

    if learning_method == "supervised":
        emb = np.matmul(feature_df_sorted.drop("Class", axis=1).values, v_t)
    else:
        emb = np.matmul(feature_df_sorted.values, v_t)

    return emb, v_t, feature_df_sorted
