
# meant to be a minimal example for using qGEL

from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

dd = pd.read_csv("https://s3-us-west-2.amazonaws.com/researchs/GFEL_data/car.csv")


def gel_v_base(k):

    X = pd.get_dummies(dd.drop("Class", axis=1))
    X["Class"] = dd.Class

    idx = np.random.uniform(0, 1, len(X)) <= .8

    cp = qgel(source_data_ = X[idx == True].reset_index().drop('index', axis = 1),
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